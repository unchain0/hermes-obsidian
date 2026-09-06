# Esquema do vault

Este vault usa Zettelkasten + PARA + MOCs e preserva fontes separadamente.

## Estrutura

- `00-inbox/files`: entrada bruta; `processed`: originais já processados.
- `10-fleeting-notes`: ideias rápidas a processar em até sete dias.
- `20-literature-notes`: sínteses próprias ligadas às fontes.
- `30-permanent-notes`: uma ideia atômica por arquivo `YYYYMMDDHHMM-slug.md`.
- `40-mocs`: mapas temáticos curados (`MOC-topico.md`).
- `50-projects`: entregáveis ativos e seus estados.
- `60-sources`: originais permitidos, capturas e manifestos.
- `70-queries`: consultas e painéis.
- `80-daily`: notas `YYYY-MM-DD.md`.
- `90-archive`: material inativo; arquivar em vez de apagar.

## Regras

1. Escrever em português do Brasil, em palavras próprias.
2. Permanente deve conter `## Fontes` e pelo menos um `[[wikilink]]` existente.
3. Literature note usa prefixo `lit-`; permanente usa timestamp; MOC usa `MOC-`.
4. Dentro das notas, usar links por slug, sem caminho. Em tabelas, nunca usar alias com pipe.
5. Ao criar/remover uma nota, atualizar o MOC correspondente e seu rodapé.
6. Preservar a origem em `60-sources`; autoria desconhecida não deve ser inferida.
7. Após mudanças, executar o validador de wikilinks e registrar em `log.md`.
8. A raiz deve conter apenas `SCHEMA.md`, `index.md` e `log.md`, além das pastas canônicas.
