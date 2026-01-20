# MEMORY - Sistema File-Based (PAI-style)

Sistema de memória persistente que o Claude Code lê nativamente.

## Por que file-based?

| Embeddings/Supabase | File-based |
|---------------------|------------|
| Requer scripts externos | Claude lê direto |
| Processamento de embeddings | Zero processamento |
| Infraestrutura externa | Apenas arquivos |
| Busca via API | Grep/Read nativos |

## Estrutura

```
MEMORY/
├── sessions/          # Captura automática via hook Stop
├── decisions/         # Decisões importantes (manual ou extraído)
├── learnings/         # Aprendizados por fase do ciclo PAI
│   ├── OBSERVE/       # Observações e descobertas
│   ├── THINK/         # Análises e reflexões
│   ├── PLAN/          # Planos e estratégias
│   ├── BUILD/         # Implementações e construções
│   ├── EXECUTE/       # Execuções e ações
│   └── VERIFY/        # Verificações e validações
├── State/             # Estado ativo
│   └── active-work.json
└── Signals/           # Sinais para padrões
    ├── failures.jsonl
    └── patterns.jsonl
```

## sessions/

Arquivos criados automaticamente pelo hook `session-capture.ts` ao encerrar uma sessão.

**Formato:** `YYYY-MM-DD-{session_id}.md`

**Conteúdo:**
```yaml
---
session_id: abc123
timestamp: 2026-01-20T10:30:00Z
cwd: /home/alejandro/ai-brain
---

[resumo da sessão]
```

## decisions/

Decisões importantes extraídas ou documentadas manualmente.

**Formato:** `YYYY-MM-DD-{titulo-slug}.md`

## learnings/

Aprendizados organizados por fase do ciclo cognitivo.

- **OBSERVE:** O que descobri observando
- **THINK:** O que concluí analisando
- **PLAN:** O que decidi planejar
- **BUILD:** O que aprendi construindo
- **EXECUTE:** O que aprendi executando
- **VERIFY:** O que validei

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
