# AI Brain - Contexto para Claude

Hub central de conhecimento e projetos pessoais.

## Usuário

- **Nome:** Ale
- **Contexto:** Empresa de uma pessoa só, baseada em IA
- **Trabalha em:** Duke Beach Hotel
- **Objetivo:** Sistemas que mostrem que "trabalho pode ser bacana"

## Estrutura

```
ai-brain/
├── sources/           ← Conhecimento capturado
├── projects/          ← Projetos em andamento
├── scripts/           ← Captura e processamento
├── .claude-config/    ← Skills e hooks (sincroniza via git)
└── CONTEXT.md         ← Guia de autores
```

## Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `/goals` ou `/metas` | Progresso das metas (treino + hábitos) |
| `/pdf` | Capturar PDF para sources |
| `python3 scripts/search.py "query"` | Busca semântica |
| `python3 scripts/capture_youtube.py <url>` | Capturar vídeo YouTube |
| `python3 scripts/capture_article.py <url>` | Capturar artigo web |

## Referências (consultar quando necessário)

| Recurso | Local | Quando usar |
|---------|-------|-------------|
| **PAI** | `~/Personal_AI_Infrastructure` | Criar skills, hooks |
| **Fabric** | `~/Fabric` + `guides/FABRIC-ALL-PATTERNS.md` | Buscar prompts prontos |
| **Substrate** | `~/Substrate` | Estruturar conhecimento |
| **Autores** | `CONTEXT.md` | Saber quem consultar |

## Ao trabalhar

1. Ler README.md do projeto antes de agir
2. Atualizar docs quando fizer mudanças significativas
3. Consultar Fabric antes de criar prompts do zero
4. Skills sempre em `.claude-config/` (nunca só em `~/.claude/` local)
