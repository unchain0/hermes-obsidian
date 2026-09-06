# Recuperação de desastre

1. Crie uma VPS Debian limpa.
2. Clone este repositório em uma máquina de controle.
3. Recrie o inventário e disponibilize o arquivo Ansible Vault fora do Git.
4. Execute `playbooks/site.yml`.
5. Pare os containers Hermes antes de restaurar arquivos ativos.
6. Carregue `/etc/restic/b2.env` e restaure o snapshot para `/` ou para um staging directory.
7. Corrija ownership para o UID/GID configurado.
8. Suba a pilha e execute `hermes doctor`, `hermes gateway status` e `hermes cron list`.
9. Valide Telegram, acesso ao vault e um restore de nota.
10. Rotacione credenciais se a VPS anterior foi comprometida.

Teste esse runbook em uma VPS descartável antes de depender dele.
