# Backups com restic e Backblaze B2

O restic cifra e autentica o conteúdo antes do upload. O Backblaze recebe blocos criptografados.

## Variáveis

```yaml
restic_enabled: true
restic_bucket: meu-bucket
restic_bucket_prefix: hermes
restic_b2_region: us-west-004
```

Segredos ficam no Ansible Vault: `vault_restic_password`, `vault_b2_key_id` e `vault_b2_application_key`.

Em um bucket novo, execute o playbook uma vez com `restic_initialize_repository=true`. Em seguida, mantenha a variável como `false`; falhas de rede, autenticação ou senha passam a interromper o provisionamento em vez de iniciar outro repositório.

## Operação

```bash
systemctl status hermes-restic-backup.timer
systemctl start hermes-restic-backup.service
journalctl -u hermes-restic-backup.service --since today
```

## Verificação e restore de teste

Não use `source /etc/restic/b2.env`. O arquivo pertence ao root e é lido pelo systemd sem avaliação de shell. Para comandos manuais:

```bash
sudo systemd-run --wait --pipe --collect \
  --property=EnvironmentFile=/etc/restic/b2.env restic snapshots
sudo mkdir -p /tmp/restore-test
sudo systemd-run --wait --pipe --collect \
  --property=EnvironmentFile=/etc/restic/b2.env \
  restic restore latest --target /tmp/restore-test
sudo systemd-run --wait --pipe --collect \
  --property=EnvironmentFile=/etc/restic/b2.env restic check
```

Compare arquivos restaurados e apague `/tmp/restore-test` ao terminar. Faça um restore de teste periódico; snapshot sem restore testado não é garantia de recuperação.

Guarde a senha do restic fora da VPS. Sem ela, o backup não pode ser restaurado.
