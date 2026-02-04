# MEMORY - Sistema File-Based (PAI-style) + Captura Inteligente

Sistema de memória persistente que o Claude Code lê nativamente, com extração automática de learnings via Haiku.

## Por que file-based?

| Embeddings/Supabase | File-based |
|---------------------|------------|
| Requer scripts externos | Claude lê direto |
| Processamento de embeddings | Zero processamento |
| Infraestrutura externa | Apenas arquivos |
| Busca via API | Grep/Read nativos |

## Captura Inteligente (v2 - 2026-02-03)

```
Cada resposta (Stop)              Fim da sessão (SessionEnd)
       │                                 │
       ▼                                 ▼
   stop-hook.ts                   session-capture.ts
       │                                 │
       ├─► Haiku classifica              ├─► minimal? → SKIP
       │                                 │
       └─► learning?                     └─► Haiku resume
           │                                 │
           ▼                                 ▼
   learnings/{PHASE}/                  sessions/
```

- **Sessões vazias NÃO são salvas** (filtro: `interactions < 2` sem arquivos)
- **Learnings extraídos automaticamente** via Haiku a cada resposta
- **Resumos inteligentes** quando não há summary do Claude

## Estrutura

```
MEMORY/
├── sessions/          # Sessões produtivas (filtradas)
├── decisions/         # Decisões importantes (manual)
├── learnings/         # Aprendizados AUTO-EXTRAÍDOS via Haiku
│   ├── OBSERVE/       # Descobertas sobre sistemas/domínios
│   ├── THINK/         # Conclusões de análises
│   ├── PLAN/          # Decisões estratégicas/arquiteturais
│   ├── BUILD/         # Padrões de implementação
│   ├── EXECUTE/       # Learnings operacionais
│   └── VERIFY/        # Insights de validação
├── State/             # Estado ativo
│   └── active-work.json
└── Signals/           # Sinais para padrões
    ├── failures.jsonl
    └── patterns.jsonl
```

## sessions/

Sessões **produtivas** criadas automaticamente pelo hook `session-capture.ts`.

**Filtro:** Sessões com `interactions < 2` e sem arquivos modificados NÃO são salvas.

**Formato:** `YYYY-MM-DD_HH-mm-ss_{session_id}.md`

**Exemplo:** `2026-02-03_15-30-45_45e2aea2.md`

**Conteúdo:**
```yaml
---
session_id: abc123
timestamp: 2026-01-20T10:30:00Z
project: ai-brain
cwd: /home/alejandro/ai-brain
branch: main
interactions: 15
---

# Session abc123

## Topic
[Resumo via Haiku se não houver summary do Claude]

## Files Modified
[Lista de arquivos]

## Tools Used
[Lista de tools]
```

## decisions/

Decisões importantes extraídas ou documentadas manualmente.

**Formato:** `YYYY-MM-DD-{titulo-slug}.md`

## learnings/

Aprendizados **AUTO-EXTRAÍDOS** pelo hook `stop-hook.ts` usando Haiku.

**Quando:** Após cada resposta do Claude (evento Stop)

**Classificação:** Haiku analisa se a resposta contém insight generalizável

**Fases:**
- **OBSERVE:** Descobertas sobre codebases, sistemas, domínios
- **THINK:** Conclusões de análises, hipóteses confirmadas/rejeitadas
- **PLAN:** Decisões estratégicas, escolhas arquiteturais
- **BUILD:** Padrões de implementação, técnicas de código
- **EXECUTE:** Learnings operacionais, insights de deploy
- **VERIFY:** Insights de testes, padrões de validação

**Formato:** `YYYY-MM-DD_HH-mm-ss_{hash}.md`

**Exemplo:** `2026-02-03_15-31-12_45e2ae.md`

**Conteúdo:**
```yaml
---
timestamp: 2026-02-03T15:45:00Z
session_id: abc123
phase: BUILD
confidence: 0.85
---

# Learning: BUILD

[Insight extraído pelo Haiku em português]

---
*Auto-extracted by stop-hook.ts*
```

## State/

Estado ativo do trabalho atual.

**active-work.json:**
```json
{
  "current_project": "ai-brain",
  "current_task": "migration to file-based",
  "blockers": []
}
```

## Signals/

Arquivos JSONL para captura de padrões ao longo do tempo.

**failures.jsonl:** Erros e falhas para análise de padrões
**patterns.jsonl:** Padrões detectados que podem virar automações

## Como usar

### Ver sessões recentes
```bash
ls -la ~/ai-brain/MEMORY/sessions/
```

### Buscar em sessões
```bash
grep -r "termo" ~/ai-brain/MEMORY/
```

### Claude lê direto
O Claude Code pode ler qualquer arquivo com `Read` ou `Grep` sem scripts intermediários.
