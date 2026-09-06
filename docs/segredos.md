# Segredos

1. Nunca copie `~/.hermes/.env`, `auth.json`, credenciais do Coolify ou arquivos reais do vault para este repositório.
2. Mantenha os valores reais em `inventories/production/group_vars/all/vault.yml`.
3. Criptografe antes de qualquer commit:

```bash
ansible-vault encrypt inventories/production/group_vars/all/vault.yml
ansible-vault view inventories/production/group_vars/all/vault.yml
```

O inventário de produção inteiro é ignorado por padrão. Em equipes, prefira SOPS com age ou um secret manager e mantenha somente o arquivo criptografado.

## Rotação

Se uma credencial entrar no Git:

1. Revogue-a imediatamente no provedor.
2. Gere uma nova credencial de escopo mínimo.
3. Remova o valor de todo o histórico com `git filter-repo`.
4. Force o push somente depois de revisar clones e forks.
5. Rode `gitleaks git .` novamente.

A remoção no commit mais recente não torna um segredo antigo seguro.
