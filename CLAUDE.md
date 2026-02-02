# AI Brain - Contexto para Claude

Hub central de conhecimento e projetos pessoais.

## Contexto Pessoal

**Nome:** Ale
**Contexto:** Empresa de uma pessoa só, baseada em IA
**Trabalha em:** Duke Beach Hotel
**Objetivo:** Sistemas que mostrem que "trabalho pode ser bacana"

### Propósito (TELOS-inspired)

> "Criar sistemas que libertem pessoas do trabalho repetitivo para focarem no que realmente importa."

Esse AI Brain é protótipo do que funcionários de hotel usarão: falar naturalmente em vez de navegar menus.

### Princípios de Operação

1. **File-based > APIs externas** - Claude lê arquivos nativamente
2. **Zero infraestrutura** - Sem banco de dados externos
3. **Captura automática** - Hooks fazem o trabalho pesado
4. **Simplicidade** - Se precisa de script complexo, está errado

## Estrutura

```
ai-brain/
├── sources/           ← Conhecimento capturado (PDFs, artigos, vídeos)
├── projects/          ← Projetos em andamento
├── scripts/           ← Captura e processamento
├── MEMORY/            ← Memória persistente (PAI-style)
│   ├── sessions/      ← Logs de sessão (auto-capturados)
│   ├── decisions/     ← Decisões importantes
│   ├── learnings/     ← Aprendizados por fase
│   ├── State/         ← Estado ativo
│   └── Signals/       ← Padrões e falhas
├── .claude-config/    ← Skills e hooks (sincroniza via git)
└── CONTEXT.md         ← Guia de autores
```

## Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `/goals` ou `/metas` | Progresso das metas (treino + hábitos) |
| `/fim` ou `/end` | Salvar resumo da sessão antes de sair |
| `/pdf` | Capturar PDF para sources |
| `ls MEMORY/sessions/` | Ver sessões recentes |
| `python3 scripts/capture_youtube.py <url>` | Capturar vídeo YouTube |
| `python3 scripts/capture_article.py <url>` | Capturar artigo web |

## Session Memory

MEMORY é centralizado no ai-brain — sessões de qualquer projeto (sistema-os, etc.) são salvas aqui.

**Captura automática:** O hook `session-capture.ts` roda no SessionEnd e extrai conteúdo do JSONL (tópico, arquivos, tools).

**Captura rica:** Use `/fim` antes de sair para Claude gerar um resumo detalhado da sessão.

## Consultar Memória

```bash
# Sessões recentes
ls -la ~/ai-brain/MEMORY/sessions/

# Buscar termo em memória
grep -r "termo" ~/ai-brain/MEMORY/

# Ver estado ativo
cat ~/ai-brain/MEMORY/State/active-work.json
```

## Referências (consultar quando necessário)

| Recurso | Local | Quando usar |
|---------|-------|-------------|
| **PAI** | `~/Personal_AI_Infrastructure` | Criar skills, hooks |
| **Fabric** | `~/Fabric` + `guides/FABRIC-ALL-PATTERNS.md` | Buscar prompts prontos |
| **Substrate** | `~/Substrate` | Estruturar conhecimento |
| **Autores** | `CONTEXT.md` | Saber quem consultar |
| **TELOS** | `projects/ai-brain/telos/TELOS-ALE.md` | Contexto profundo pessoal |

## Ao trabalhar

1. Ler README.md do projeto antes de agir
2. Atualizar docs quando fizer mudanças significativas
3. Consultar Fabric antes de criar prompts do zero
4. Skills sempre em `.claude-config/` (nunca só em `~/.claude/` local)
5. Consultar MEMORY/ para contexto de sessões anteriores
