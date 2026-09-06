#!/usr/bin/env python3
"""Valida somente artefatos públicos e diretórios esperados do perfil."""
import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--hermes-home", required=True, type=Path)
parser.add_argument("--vault", required=True, type=Path)
args = parser.parse_args()
errors = []
manifest_dir = args.hermes_home / "profile" / "manifests"
for name in ("skills.yml", "automations.yml", "scripts.yml"):
    path = manifest_dir / name
    if not path.is_file():
        errors.append(f"manifesto ausente: {path}")
        continue
    text = path.read_text()
    if "schema_version: 1" not in text:
        errors.append(f"schema inválido: {path}")
for name in ("skills", "scripts", "cron", "state", "memories"):
    if not (args.hermes_home / name).is_dir():
        errors.append(f"diretório Hermes ausente: {name}")
for name in ("SCHEMA.md", "index.md", "log.md"):
    if not (args.vault / name).is_file():
        errors.append(f"fundação do vault ausente: {name}")
if errors:
    print("FALHA\n" + "\n".join(errors))
    sys.exit(1)
print("OK: perfil público materializado")
