# Política de segurança

## Nunca publique

- `.env`, `auth.json`, `config.yaml` reais ou arquivos descriptografados do Ansible Vault.
- Tokens de Telegram, Discord, GitHub, provedores LLM, Coolify ou Backblaze.
- O conteúdo pessoal do vault Obsidian, extratos, contabilidade ou dados congregacionais.
- IDs de chat, e-mails, domínios privados, IPs ou chaves SSH reais.

Os exemplos deste projeto usam somente valores inertes. Segredos de produção devem ficar em `group_vars/vault.yml`, criptografado com `ansible-vault encrypt`, ou em um gerenciador externo.

## Relatar vulnerabilidade

Abra um aviso privado de segurança no GitHub. Não inclua credenciais reais no relato.
