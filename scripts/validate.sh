#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

command -v yamllint >/dev/null || { echo "yamllint não instalado" >&2; exit 1; }
command -v ansible-lint >/dev/null || { echo "ansible-lint não instalado" >&2; exit 1; }
command -v ansible-playbook >/dev/null || { echo "ansible-core não instalado" >&2; exit 1; }
gitleaks_bin="$(command -v gitleaks || true)"
if [[ -z "$gitleaks_bin" && -x .tools/gitleaks ]]; then
  gitleaks_bin="$PWD/.tools/gitleaks"
fi
[[ -n "$gitleaks_bin" ]] || {
  echo "gitleaks não instalado; execute ./scripts/install-gitleaks.sh" >&2
  exit 1
}

yamllint .
ansible-lint playbooks roles
ansible-playbook -i tests/inventory/hosts.yml playbooks/site.yml --syntax-check -e @tests/vars/ci.yml
ansible-playbook -i tests/inventory/hosts.yml tests/render.yml
rm -rf /tmp/hermes-profile-ci
ansible-playbook -i tests/inventory/hosts.yml tests/profile.yml
profile_second_run="$(ansible-playbook -i tests/inventory/hosts.yml tests/profile.yml)"
printf '%s\n' "$profile_second_run"
printf '%s\n' "$profile_second_run" | grep -Eq 'changed=0.*failed=0'
rm -rf /tmp/hermes-profile-guard-ci
ansible-playbook -i tests/inventory/hosts.yml tests/vault_merge_guard.yml
python3 tests/test_repository.py
python3 tests/test_rendered.py
python3 tests/test_replica_profile.py

"$gitleaks_bin" dir . --redact
"$gitleaks_bin" git . --redact
