---
name: processamento-inbox
description: Processamento seguro do inbox.
version: 1.0.0
author: Projeto hermes-obsidian-ansible
license: MIT
---

# Processamento seguro do inbox

Processe um item por vez: preserve a fonte, extraia, crie nota de literatura, permanentes e MOC, releia tudo, valide wikilinks e somente então mova o original para processed. Em falha, mantenha o item recuperável.

## Segurança

Nunca inclua tokens, IDs de chat, dados pessoais, conteúdo do vault real, estados de execução ou credenciais em saídas públicas.
