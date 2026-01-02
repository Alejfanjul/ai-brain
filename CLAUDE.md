# AI Brain - Contexto para Claude

Este é um repositório de conhecimento pessoal. O objetivo é capturar conteúdo de diversas fontes (newsletters, vídeos, artigos, cursos) em formato que possa ser consultado posteriormente via Claude.

## Estrutura

```
ai-brain/
├── sources/              ← Conteúdo capturado (raw + metadata)
├── notes/                ← Reflexões e conexões do usuário
├── .claude/skills/       ← Skills de captura
├── TEMPLATE.md           ← Template para capturas manuais
└── README.md
```

## Comandos Disponíveis

### /capture youtube <url>
Extrai transcript de vídeo do YouTube e salva em sources/.

### /capture article <url>
Extrai conteúdo de artigo/post web e salva em sources/.

### /capture manual
Fluxo guiado para salvar conteúdo copiado manualmente.

### /capture course
Captura conteúdo de cursos (Udemy, etc) onde o usuário cola o transcript.
Executa: `python3 scripts/capture_course.py`

### /capture playlist <url>
Captura playlist inteira do YouTube, extraindo transcripts de todos os vídeos.
Executa: `python3 scripts/capture_playlist.py "<url>"`

### /capture epub <file_path>
Extrai conteúdo de livro EPUB e salva em sources/.
Executa: `python3 scripts/capture_epub.py "<file_path>"`

## Convenções

### Nomes de arquivo
- Formato: `YYYY-MM-DD-titulo-slug.md`
- Exemplo: `2025-12-27-nate-correctness-ai-systems.md`

### Commits
- Formato: `capture: [titulo do conteúdo]`
- Exemplo: `capture: The Art of Defining Correct`

### Tipos de conteúdo
- newsletter
- video
- artigo
- blog
- curso
- livro
- podcast

## Fontes Frequentes

| Autor | Domínio | Tipo |
|-------|---------|------|
| Nate | natesnewsletter.substack.com | newsletter |
| Seth Godin | seths.blog | blog |
| Dan Shipper | every.to | newsletter |

## Princípios

1. **Raw over polished**: Manter conteúdo original, não resumir demais
2. **Capture fast**: Não deixar para depois
3. **Metadata matters**: Sempre incluir fonte, autor, data, URL
4. **Git everything**: Todo conteúdo versionado

## Usuário

- Nome: Ale
- Contexto: Construindo sistemas de IA para hotelaria (Duke Beach Hotel)
- Projetos relacionados: sistema-os, RM module
- Objetivo: Acumular conhecimento para alimentar decisões e conversas com Claude