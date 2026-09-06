#!/usr/bin/env python3
from pathlib import Path
import subprocess
import yaml

compose = yaml.safe_load(Path("/tmp/hermes-compose-ci.yml").read_text())
coolify_compose = yaml.safe_load(Path("/tmp/hermes-compose-coolify-ci.yml").read_text())
config = yaml.safe_load(Path("/tmp/hermes-config-ci.yml").read_text())

assert "gateway" in compose["services"]
assert "dashboard" in compose["services"]
assert "env_file" in compose["services"]["gateway"]
assert "dashboard" not in coolify_compose["services"]
assert "env_file" not in coolify_compose["services"]["gateway"]
assert config["stt"]["local"]["model"] == "base"
assert config["tts"]["edge"]["voice"] == "pt-BR-AntonioNeural"
assert config["timezone"] == "America/Sao_Paulo"
assert config["security"]["redact_secrets"] is True
assert config["security"]["tirith_fail_open"] is False
assert config["privacy"]["redact_pii"] is True
assert config["gateway"]["strict"] is True
assert config["skills"]["guard_agent_created"] is True
assert config["sessions"]["auto_prune"] is True
assert config["code_execution"]["mode"] == "strict"
assert config["platform_toolsets"]["cli"] == ["hermes-cli"]
assert config["platform_toolsets"]["telegram"] == ["hermes-telegram"]
subprocess.run(["bash", "-n", "/tmp/hermes-backup-ci.sh"], check=True)
backup = Path("/tmp/hermes-backup-ci.sh").read_text()
service = Path("/tmp/hermes-restic-service-ci").read_text()
assert "source /etc/restic" not in backup
assert "EnvironmentFile=/etc/restic/b2.env" in service
print("OK: Compose, config Hermes e script restic renderizados corretamente")
