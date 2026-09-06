#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

required = [
    "README.md",
    "SECURITY.md",
    "playbooks/site.yml",
    "roles/hermes_agent/templates/compose.yml.j2",
    "roles/restic_b2/templates/backup.sh.j2",
]
for item in required:
    if not (ROOT / item).is_file():
        errors.append(f"arquivo obrigatório ausente: {item}")

public_files = subprocess.run(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
    cwd=ROOT,
    check=True,
    capture_output=True,
).stdout.decode().split("\0")

for relative in filter(None, public_files):
    path = ROOT / relative
    if not path.is_file():
        continue
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    text = re.sub(r"SUBSTITUA[A-Z0-9_-]*", "PLACEHOLDER", text)
    secret_pattern = r'''(?i)(api[_-]?key|token|password)\s*[=:]\s*['"][A-Za-z0-9_/-]{24,}'''
    if re.search(secret_pattern, text):
        errors.append(f"possível segredo literal: {relative}")

compose = (ROOT / "roles/hermes_agent/templates/compose.yml.j2").read_text()
for mount in ["/opt/data", "/vault", "/workspace"]:
    if mount not in compose:
        errors.append(f"mount Hermes ausente: {mount}")

backup = (ROOT / "roles/restic_b2/templates/backup.sh.j2").read_text()
hermes_tasks = (ROOT / "roles/hermes_agent/tasks/main.yml").read_text()
for guard in ["set -Eeuo pipefail", "flock -n", "restic forget --prune", "restic check"]:
    if guard not in backup:
        errors.append(f"proteção de backup ausente: {guard}")
if "source /etc/restic" in backup:
    errors.append("script de backup não deve avaliar o arquivo de ambiente como shell")
if hermes_tasks.count("remove_orphans: true") < 2:
    errors.append("implantação Hermes deve remover órfãos ao atualizar e migrar")
if hermes_tasks.find("Encerrar pilha direta") > hermes_tasks.find("Renderizar Docker Compose"):
    errors.append("a pilha direta deve ser encerrada antes de sobrescrever o Compose")

if errors:
    print("FALHA")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print("OK: estrutura, mounts, backup e heurística de segredos validados")
