# Capture Playlist

Captura playlist inteira do YouTube, extraindo transcript de todos os vídeos.

## Trigger

- `/capture playlist <url>`
- "captura essa playlist"
- "baixa os transcripts dessa playlist"

## Processo

Executar: `python3 scripts/capture_playlist.py "<URL>"`

O script vai:
1. Listar todos os vídeos da playlist
2. Pedir confirmação
3. Extrair transcript de cada vídeo
4. Criar arquivo único com todo o conteúdo

## Estrutura de Arquivo

Um arquivo por playlist:
`YYYY-MM-DD-playlist-nome-da-playlist.md`

## Exemplo

```bash
python3 scripts/capture_playlist.py "https://www.youtube.com/playlist?list=PLxxxxxx"
```
