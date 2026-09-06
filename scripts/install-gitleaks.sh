#!/usr/bin/env bash
set -Eeuo pipefail

version="8.30.1"
sha256="551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
destination="${1:-$root/.tools}"
archive="$(mktemp)"
trap 'rm -f "$archive"' EXIT

case "$(uname -m)" in
  x86_64|amd64) asset="gitleaks_${version}_linux_x64.tar.gz" ;;
  *) echo "Arquitetura não suportada pelo instalador fixado: $(uname -m)" >&2; exit 1 ;;
esac

curl --fail --location --proto '=https' --tlsv1.2 \
  "https://github.com/gitleaks/gitleaks/releases/download/v${version}/${asset}" \
  --output "$archive"
printf '%s  %s\n' "$sha256" "$archive" | sha256sum --check --status
mkdir -p "$destination"
tar -xzf "$archive" -C "$destination" gitleaks
chmod 0755 "$destination/gitleaks"
"$destination/gitleaks" version
