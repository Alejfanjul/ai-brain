# AI Brain

Hub central de conhecimento e projetos para construção de uma empresa de uma pessoa só, baseada em IA.

## Estrutura

```
ai-brain/
├── sources/           ← Conhecimento capturado (newsletters, vídeos, cursos, artigos)
├── projects/          ← Projetos em andamento
├── templates/         ← Templates para capturas e projetos
├── scripts/           ← Scripts de captura automática
└── CONTEXT.md         ← Guia de autores e como usar o repositório
```

## Fontes de Conhecimento

### Automatizadas (GitHub Actions - diário às 11h)
- **Nate** - IA, agentes, desenvolvimento de software
- **Simon Willison** - IA, ferramentas

### Manuais

| Comando | Uso |
|---------|-----|
| `python3 scripts/capture_youtube.py <URL>` | Vídeo único |
| `python3 scripts/capture_playlist.py <URL>` | Playlist inteira |
| `python3 scripts/capture_article.py <URL>` | Artigo web |
| `python3 scripts/capture_epub.py <file>` | Livro EPUB |
| `python3 scripts/capture_course.py` | Curso (cola transcript) |

## Projetos

| Projeto | Estágio | Descrição |
|---------|---------|-----------|
| marca-pessoal | Exploração | Construção de presença pessoal |

### Criar novo projeto

```bash
cp templates/PROJECT-EXPLORATION.md projects/nome-do-projeto/README.md
```

## Guia de Autores

| Autor | Domínio | Quando usar |
|-------|---------|-------------|
| Seth Godin | Marketing, direção | "Para onde ir?" |
| Derek Sivers | Filosofia, decisões | "Como pensar sobre isso?" |
| Nate | IA, agentes, execução | "Como construir com IA?" |
| Joe Hudson | Desenvolvimento pessoal | "Como lidar com isso?" |
| Bruno Perini | Marca pessoal, finanças | "Como me posicionar?" |

Detalhes completos em [CONTEXT.md](CONTEXT.md).

## Princípios

- **Raw over polished** - conteúdo original > resumos
- **Capture fast** - não deixar para depois
- **Claude does the work** - classificação e conexões na consulta
- **Projetos evoluem** - de Exploração → Definição → Execução
