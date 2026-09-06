#!/usr/bin/env python3
"""Contrato do perfil público que reproduz o setup sem copiar estado privado."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def require(path: str) -> Path:
    candidate = ROOT / path
    if not candidate.exists():
        errors.append(f"ausente: {path}")
    return candidate


expected_vault_dirs = {
    "00-inbox/files",
    "00-inbox/processed",
    "10-fleeting-notes",
    "20-literature-notes",
    "30-permanent-notes",
    "40-mocs",
    "50-projects",
    "60-sources",
    "70-queries",
    "80-daily",
    "90-archive",
}
for relative in expected_vault_dirs:
    require(f"examples/vault/{relative}/.gitkeep")

for relative in (
    "examples/vault/SCHEMA.md",
    "examples/vault/index.md",
    "examples/vault/log.md",
    "examples/vault/20-literature-notes/lit-anotacoes-conectadas.md",
    "examples/vault/30-permanent-notes/202601011005-notas-atomicas-reduzem-ambiguidade.md",
    "examples/vault/30-permanent-notes/202601011010-conexoes-contextualizam-ideias-atomicas.md",
    "examples/vault/40-mocs/MOC-gestao-do-conhecimento.md",
    "examples/vault/70-queries/consultas-uteis.md",
    "examples/vault/.obsidian/community-plugins.json",
    "manifests/skills.yml",
    "manifests/automations.yml",
    "manifests/scripts.yml",
    "roles/hermes_profile/tasks/main.yml",
    "docs/replica-fiel.md",
):
    require(relative)

skills_path = ROOT / "manifests/skills.yml"
if skills_path.exists():
    skills = yaml.safe_load(skills_path.read_text())
    names = {item["name"] for item in skills.get("skills", [])}
    required = {
        "zettelkasten-vault", "obsidian", "audio-inbox-processing",
        "jwpub-extractor", "ocr-and-documents", "jw-org-ingest",
        "jw-preparation", "hermes-agent", "scheduled-analysis-pipelines",
    }
    if missing := required - names:
        errors.append(f"skills principais ausentes: {sorted(missing)}")
    for item in skills.get("skills", []):
        if item.get("distribution") not in {"bundled", "profile", "external"}:
            errors.append(f"distribuição inválida para skill {item.get('name')}")
        if item.get("distribution") == "profile":
            skill_file = (
                ROOT
                / "roles/hermes_profile/files/profile-skills"
                / item["name"]
                / "SKILL.md"
            )
            if not skill_file.is_file():
                errors.append(f"skill profile não materializada: {item['name']}")

jobs_path = ROOT / "manifests/automations.yml"
if jobs_path.exists():
    jobs = yaml.safe_load(jobs_path.read_text())
    if jobs.get("timezone") != "America/Sao_Paulo":
        errors.append("timezone das automações deve ser America/Sao_Paulo")
    automations = jobs.get("automations", [])
    if len(automations) < 9:
        errors.append("manifesto deve representar os nove padrões de automação")
    if any(item.get("enabled", True) for item in automations):
        errors.append("automações públicas devem começar desabilitadas")
    if any(item.get("schedule_is_example") is not True for item in automations):
        errors.append("agendas públicas devem ser identificadas como exemplos")
    ids = [item.get("id") for item in automations]
    if len(ids) != len(set(ids)):
        errors.append("IDs lógicos de automação devem ser únicos")
    scripts = yaml.safe_load((ROOT / "manifests/scripts.yml").read_text())
    script_names = {item["name"] for item in scripts.get("scripts", [])}
    referenced = {item["script"] for item in automations if item.get("script")}
    if missing := referenced - script_names:
        errors.append(f"scripts de automação ausentes do manifesto: {sorted(missing)}")

config = (ROOT / "roles/hermes_agent/templates/config.yaml.j2").read_text()
vault_defaults = yaml.safe_load(
    (ROOT / "roles/vault/defaults/main.yml").read_text()
)
if vault_defaults.get("vault_seed_example") is not False:
    errors.append("vault-modelo deve ser opt-in por padrão")
compose_template = (
    ROOT / "roles/hermes_agent/templates/compose.yml.j2"
).read_text()
if "{{ hermes_root }}/scripts:/opt/data/scripts" in compose_template:
    errors.append("mount de scripts duplica e oculta HERMES_HOME/scripts")
for guard in (
    "gateway:", "strict: true", "allow_lazy_installs: false",
    "tirith_fail_open: false", "guard_agent_created: true",
    "auto_prune: true", "max_concurrent_children:", "platform_toolsets:",
):
    if guard not in config:
        errors.append(f"configuração fiel/fail-closed ausente: {guard}")

for skill in (ROOT / "roles/hermes_profile/files/profile-skills").glob("*/SKILL.md") if (ROOT / "roles/hermes_profile/files/profile-skills").exists() else []:
    text = skill.read_text()
    if "license:" not in text.split("---", 2)[1]:
        errors.append(f"skill sem licença declarada: {skill.relative_to(ROOT)}")

for path in ROOT.rglob("*"):
    if path.is_file() and any(part in {"examples", "manifests", "files"} for part in path.parts):
        forbidden = {"auth.json", "jobs.json", "state.db", "workspace.json", ".usage.json"}
        if path.name in forbidden or path.suffix in {".sqlite", ".db", ".pem", ".key"}:
            errors.append(f"artefato privado proibido: {path.relative_to(ROOT)}")
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        if re.search(r"telegram:\s*-?\d{8,}|chat_id:\s*-?\d{8,}", text, re.I):
            errors.append(f"possível ID de entrega real: {path.relative_to(ROOT)}")

if errors:
    print("FALHA")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print("OK: perfil, skills, automações e vault-modelo validados")
