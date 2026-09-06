# Coolify

## Instalação segura

A role é opt-in. O script oficial do Coolify é mutável; por isso o Ansible exige que o operador o baixe, revise e fixe o SHA-256:

```bash
curl -fsSLo /tmp/coolify-install.sh https://cdn.coollabs.io/coolify/install.sh
less /tmp/coolify-install.sh
sha256sum /tmp/coolify-install.sh
```

Defina no inventário:

```yaml
install_coolify: true
coolify_installer_sha256: "COLE_O_SHA256_REVISADO"
hermes_deployment_mode: coolify
```

A role cria `/opt/hermes-stack/compose.yml`, sem materializar `hermes.env`, e não sobe a pilha quando o modo é `coolify`.

## Criar o recurso no Coolify

1. Crie um recurso **Docker Compose**.
2. Use o Compose renderizado ou adapte `roles/hermes_agent/templates/compose.yml.j2`.
3. Cadastre `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS` e a chave do provedor pela interface do Coolify, nunca no Git.
4. Configure bind mounts persistentes para `/srv/hermes`.
5. O Compose omite o dashboard no modo Coolify. Habilite-o separadamente apenas com um provedor de autenticação compatível.
6. Confirme que o gateway reinicia sem perder `/opt/data` e `/vault`.

Coolify e Ansible não devem executar `compose up` sobre o mesmo projeto simultaneamente.
