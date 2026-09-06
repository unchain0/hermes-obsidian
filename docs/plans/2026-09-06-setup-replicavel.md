# Setup reproduzível Hermes + Obsidian Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Criar um repositório público Ansible que reproduza com segurança um servidor Debian 13 com Docker/Coolify, Hermes Agent, vault Obsidian e backups Backblaze B2.

**Architecture:** O Ansible prepara a VPS e renderiza uma pilha Docker baseada em bind mounts sob `/srv/hermes`. Segredos ficam exclusivamente em Ansible Vault e são materializados com modo `0600`; o backup usa restic sobre a API S3 do Backblaze B2. Coolify é opcional e separado da implantação direta para evitar dois controladores do mesmo Compose.

**Tech Stack:** Ansible Core, Docker Compose v2, Coolify, Hermes Agent, Obsidian Markdown vault, restic, Backblaze B2 S3 e GitHub Actions.

---

### Task 1: Base segura e Docker
- Criar roles `common` e `docker` com suporte a Debian 13.
- Validar syntax-check e idempotência dos arquivos gerados.
- Commit: `feat: provision Debian base and Docker`.

### Task 2: Hermes Agent e vault Obsidian
- Criar bind mounts persistentes, configuração sanitizada e Compose com imagem fixada.
- Criar esqueleto Zettelkasten e documentação de restauração.
- Commit: `feat: deploy Hermes Agent and Obsidian vault`.

### Task 3: Coolify e backups B2
- Tornar a instalação de Coolify opt-in e verificável.
- Configurar restic, timer systemd, retenção e teste de restore.
- Commit: `feat: add optional Coolify and Backblaze backups`.

### Task 4: Segurança, documentação e CI
- Adicionar exemplos de secrets, gitleaks, lint, syntax-check e Molecule.
- Documentar bootstrap, Coolify, Obsidian, JW e recuperação de desastre.
- Revisar diff, executar scanner e só então publicar.
- Commit: `docs: complete reproducible setup guide and CI`.
