# AI Brain

Sistema de captura e organização de conhecimento para alimentar conversas com Claude.

## O que é

Repositório pessoal que captura conteúdo de múltiplas fontes (newsletters, vídeos, cursos, artigos) em formato que o Claude pode acessar via Project Knowledge.

## Setup

Para ativar o ambiente virtual antes de usar os scripts de captura:

```bash
source venv/bin/activate
```

## Fontes Automatizadas (diárias)

| Fonte | Autor | Tipo |
|-------|-------|------|
| Nate's Newsletter | Nate | newsletter |
| Seth's Blog | Seth Godin | blog |
| Simon Willison's Newsletter | Simon Willison | newsletter |

O GitHub Actions roda diariamente às 11h (Brasília) e captura novos posts automaticamente.

## Comandos Manuais

### YouTube (vídeo único)
```bash
python3 scripts/capture_youtube.py "<URL>"
```

### YouTube (playlist inteira)
```bash
python3 scripts/capture_playlist.py "<URL_DA_PLAYLIST>"
```

### Artigo Web
```bash
python3 scripts/capture_article.py "<URL>"
```

### Curso (Udemy, Coursera, etc)
```bash
python3 scripts/capture_course.py
# Preenche interativamente e cola o transcript
```

## Estrutura
```
ai-brain/
├── sources/              # Conteúdo capturado
├── scripts/              # Scripts de captura
│   ├── email_capture.py      # Automático (GitHub Actions)
│   ├── rss_capture.py        # Automático (pausado)
│   ├── capture_youtube.py    # Manual
│   ├── capture_playlist.py   # Manual
│   ├── capture_article.py    # Manual
│   └── capture_course.py     # Manual
├── .claude/skills/       # Skills para Claude Code
└── .github/workflows/    # Automação diária
```

## Como Usar com Claude

1. Adicione este repositório como Project Knowledge em um Projeto do Claude
2. Faça perguntas normalmente - Claude vai buscar nos conteúdos automaticamente
3. Não precisa dizer "procura no artigo X", apenas pergunte

## Princípios

- **Raw over polished**: Conteúdo original, não resumido
- **Capture fast**: Automatiza o que for possível
- **Claude does the work**: Classificação e conexões acontecem na consulta
