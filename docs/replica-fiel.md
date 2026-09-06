# Perfil público fiel e sanitizado do setup

Este perfil reproduz a arquitetura publicável, regras e contratos operacionais
do ambiente de referência. Ele deliberadamente não copia identidade, memória,
sessões, notas pessoais, conteúdo protegido, estados, destinos ou credenciais.

## O que é reproduzido

- Debian 13, Docker/Coolify, imagem Hermes fixada e volumes persistentes.
- `HERMES_HOME`, vault, workspace, scripts, skills, cron, estado e memória com permissões restritas.
- Configuração detalhada: ferramentas, STT Whisper `base`, Edge TTS `pt-BR-AntonioNeural`, memória, delegação, curator, sessões, aprovações e proteção de segredos.
- Manifesto das capacidades de skills do perfil e implementações públicas clean-room.
- Nove padrões de automação, todos desabilitados até a configuração privada.
- Vault-modelo completo com as dez pastas, arquivos fundamentais e um fluxo fictício conectado.
- Restic/B2 fail-closed e modos `direct`/`coolify` exclusivos.

## Limite entre público e privado

Nunca são exportados: `.env`, `auth.json`, `state.db*`, `jobs.json`, `.usage.json`, sessões, memórias reais, prompts, logs, IDs de chat, webhooks, notas do usuário, fontes protegidas, extratos, bancos, cookies ou workspace do Obsidian.

Skills `bundled` são fornecidas pela imagem Hermes fixada. Skills `profile` são instaladas deste repositório. O item `external` documenta integrações que exigem artefatos privados. Isso evita redistribuir código sem licença confirmada.

## Aplicação

```bash
./scripts/install-gitleaks.sh
./scripts/validate.sh
ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml   --ask-become-pass --ask-vault-pass
```

Para materializar o exemplo, use um destino novo e vazio e defina
`vault_seed_example: true`. O padrão é `false`; merge em vault existente exige
`vault_allow_example_merge: true` e deve ser precedido de backup.

Depois da implantação:

```bash
sudo python3 /srv/hermes/home/profile/profile_healthcheck.py   --hermes-home /srv/hermes/home --vault /srv/hermes/vault
sudo docker compose -f /opt/hermes-stack/compose.yml exec gateway hermes doctor
sudo docker compose -f /opt/hermes-stack/compose.yml exec gateway hermes skills list
sudo docker compose -f /opt/hermes-stack/compose.yml exec gateway hermes cron list --all
```

## Ativação das automações

`manifests/automations.yml` é documentação declarativa e não é copiado diretamente para `jobs.json`. Para cada item:

1. instale/audite o script indicado;
2. configure credenciais em Ansible Vault ou no Coolify;
3. rode o script em modo de teste;
4. crie o job pela CLI suportada (`hermes cron create ...`);
5. execute manualmente uma vez e confirme o resultado;
6. só então habilite a agenda.

IDs runtime e destinos nunca pertencem ao Git público.

## Grau de fidelidade

O perfil é fiel no comportamento que pode ser publicado. Dados pessoais e
componentes sem licença/origem verificável são representados por contratos,
manifestos e pontos de extensão, não por cópia cega. O CI valida estrutura,
idempotência, segredos e a configuração contra a imagem Hermes fixada; scripts
marcados como `external` continuam fora do escopo reproduzível.
