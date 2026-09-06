# Automações de pesquisa bíblica/JW

O repositório prepara o ambiente, mas não publica o conteúdo pessoal do vault nem materiais com acesso restrito. Automações devem:

- consultar somente fontes oficiais de `jw.org` e `wol.jw.org`;
- respeitar termos de uso, limites de acesso e direitos autorais;
- guardar referências e links, evitando redistribuir publicações completas;
- ser idempotentes e não criar notas duplicadas;
- usar Whisper `base` no mínimo; para áudio curto, `medium` pode melhorar a qualidade;
- manter scripts do usuário em `/srv/hermes/scripts` e estados em `/srv/hermes/home` ou no vault;
- validar wikilinks depois de modificar notas.

## Instalação de scripts privados

Crie fora deste Git um diretório local com os scripts e sincronize por Ansible ou rsync:

```bash
rsync -av --delete ./meus-scripts/ deploy@servidor:/srv/hermes/scripts/
```

Depois crie jobs com o CLI do Hermes dentro do container:

```bash
cd /opt/hermes-stack
sudo docker compose exec gateway hermes cron create '0 12 * * *'
sudo docker compose exec gateway hermes cron list
```

Não versione `jobs.json` de produção: prompts podem conter detalhes pessoais e IDs de entrega.
