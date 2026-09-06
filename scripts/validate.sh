#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

command -v yamllint >/dev/null || { echo "yamllint não instalado" >&2; exit 1; }
command -v ansible-lint >/dev/null || { echo "ansible-lint não instalado" >&2; exit 1; }
command -v ansible-playbook >/dev/null || { echo "ansible-core não instalado" >&2; exit 1; }

yamllint .
ansible-lint playbooks roles
ansible-playbook -i tests/inventory/hosts.yml playbooks/site.yml --syntax-check -e @tests/vars/ci.yml
ansible-playbook -i tests/inventory/hosts.yml tests/render.yml
python3 tests/test_repository.py
python3 tests/test_rendered.py

if command -v gitleaks >/dev/null; then
  gitleaks dir . --redact
  gitleaks git . --redact
else
  echo "AVISO: gitleaks não instalado; o CI executará a varredura." >&2
fi
