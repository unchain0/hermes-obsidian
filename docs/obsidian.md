# Obsidian

O servidor mantém Markdown em `/srv/hermes/vault`; o aplicativo Obsidian roda no computador ou celular do usuário. Este projeto não publica nem sincroniza conteúdo pessoal automaticamente.

Opções de sincronização:

- Obsidian Sync: simples e com criptografia ponta a ponta.
- Syncthing: autogerenciado; exige cuidado com conflitos e exposição de portas.
- Processo próprio com SSH/rsync: adequado para usuários técnicos.

Nunca exponha o diretório do vault por HTTP sem autenticação.

## Leitura em voz alta

No desktop, o plugin comunitário Note Reader pode usar TTS neural online. Exemplo de voz masculina: `pt-BR-AntonioNeural`. Plugins comunitários devem ser revisados e instalados no cliente, não no servidor.
