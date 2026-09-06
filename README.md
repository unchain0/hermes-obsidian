# Hermes + Obsidian em uma VPS com Ansible

Projeto público para reconstruir, de forma documentada, um ambiente semelhante ao setup usado em produção: **Debian 13 + Docker/Coolify + Hermes Agent + vault Obsidian + automações + backup criptografado no Backblaze B2**.

> Este repositório contém infraestrutura e exemplos, não o vault pessoal nem credenciais. Ele não é afiliado à Nous Research, Obsidian, Backblaze, Coolify ou JW.org.

## O que é provisionado

- Base Debian 12/13 e timezone `America/Sao_Paulo`.
- Docker Engine e Compose v2 pelo repositório oficial.
- Coolify opcional, com instalador baixado e checksum obrigatório.
- Hermes Agent em containers, com gateway, painel opcional e volumes persistentes.
- Esqueleto Zettelkasten para um vault Obsidian.
- Voz e transcrição em português: Whisper `base` e Edge TTS masculino.
- Backup restic criptografado para Backblaze B2 usando API compatível com S3.
- CI para lint, syntax-check, Molecule e detecção de segredos.

## Arquitetura

```text
Internet/Telegram
       |
       v
+--------------------- VPS Debian ----------------------+
| Docker ou Coolify                                     |
|  +------------------+   +---------------------------+ |
|  | Hermes gateway   |   | Hermes dashboard (local) | |
|  +---------+--------+   +-------------+-------------+ |
|            |                          |               |
|      /srv/hermes/{home,vault,workspace,scripts}       |
|            |                                          |
|            +---- restic (criptografia local) ---------+----> Backblaze B2 S3
+-------------------------------------------------------+
```

## Início rápido

### 1. Máquina de controle

```bash
git clone https://github.com/SEU-USUARIO/hermes-obsidian-ansible.git
cd hermes-obsidian-ansible
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
ansible-galaxy collection install -r collections/requirements.yml
```

### 2. Inventário e segredos

Copie `inventories/example` para `inventories/production` e ajuste o IP e o usuário SSH. O diretório de produção é ignorado pelo Git.

```bash
cp -r inventories/example inventories/production
mkdir -p inventories/production/group_vars/all
cp group_vars/all.yml inventories/production/group_vars/all/settings.yml
cp group_vars/vault.yml.example inventories/production/group_vars/all/vault.yml
ansible-vault encrypt inventories/production/group_vars/all/vault.yml
```

Use um **Application Key do Backblaze limitado ao bucket**. O restic precisa listar, gravar e apagar arquivos para executar retenção e `prune`.

### 3. Validar e aplicar

```bash
./scripts/validate.sh
ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml   --ask-become-pass --ask-vault-pass
```

Para não instalar nem executar o Coolify, mantenha:

```yaml
install_coolify: false
hermes_deployment_mode: direct
```

Para usar Coolify, consulte [`docs/coolify.md`](docs/coolify.md). Nunca deixe `direct` e Coolify controlarem a mesma pilha ao mesmo tempo.

O backup começa desabilitado por segurança. Depois de preencher e criptografar os dados do B2, defina `restic_enabled: true`. Para um bucket novo, use `restic_initialize_repository: true` somente na primeira execução.

## Primeiro acesso

No modo direto:

```bash
ssh deploy@SEU_SERVIDOR
cd /opt/hermes-stack
sudo docker compose ps
sudo docker compose exec gateway hermes doctor
sudo docker compose exec gateway hermes gateway status
```

O painel fica apenas em `127.0.0.1:9119`. Acesse por túnel:

```bash
ssh -L 9119:127.0.0.1:9119 deploy@SEU_SERVIDOR
```

Depois abra `http://127.0.0.1:9119`.

## Documentação

- [`docs/segredos.md`](docs/segredos.md)
- [`docs/coolify.md`](docs/coolify.md)
- [`docs/backups.md`](docs/backups.md)
- [`docs/obsidian.md`](docs/obsidian.md)
- [`docs/automacoes-jw.md`](docs/automacoes-jw.md)
- [`docs/recuperacao-de-desastre.md`](docs/recuperacao-de-desastre.md)
- [`SECURITY.md`](SECURITY.md)

## Limites de validação

O ambiente onde este projeto foi gerado não expõe o socket Docker do host. Nele foram executados lint, syntax-check, testes de templates e scanner de segredos. O cenário Molecule do CI cobre a role base no Debian 13; Docker, Coolify e restore B2 devem ser validados em uma VPS descartável antes de migrar produção.

## Licença

MIT. Consulte [`LICENSE`](LICENSE).
