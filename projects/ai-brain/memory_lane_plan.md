# Plano: Memory Lane System (baseado no JFDI do Hillman)

> **Contexto:** Este plano implementa a **Fase 3: Memória e Síntese** do documento `ai_brain_parceiro_digital-v0.3.md`.
>
> As fases anteriores já foram concluídas:
> - ✅ Fase 1: Audit Trail (hooks + Supabase)
> - ✅ Fase 2: Persistência de Conversas (81 sessões, 1000+ mensagens salvas)

## Objetivo
Implementar sistema completo de memória para o AI Brain, similar ao Memory Lane do Alex Hillman.

## Decisões do usuário
- **Embeddings:** Ollama (local, gratuito)
- **Frequência:** 5 min sync sessões, 15 min extração memórias
- **Interface:** Backend primeiro (sem UI)
- **Scheduler:** Cron (simples)

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                      MEMORY LANE SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CRON JOBS                           CLAUDE CODE HOOKS          │
│   ┌──────────────────┐               ┌──────────────────┐       │
│   │ */5 min          │               │ user_prompt_submit│       │
│   │ sync_sessions.py │               │ → busca memórias │       │
│   └────────┬─────────┘               │ → injeta contexto│       │
│            │                         └────────┬─────────┘       │
│   ┌────────┴─────────┐               ┌────────┴─────────┐       │
│   │ */15 min         │               │ tool_use (file)  │       │
│   │ extract_memories │               │ → memórias de    │       │
│   │ .py              │               │   arquivos       │       │
│   └────────┬─────────┘               └────────┬─────────┘       │
│            │                                  │                  │
│            v                                  v                  │
│   ┌─────────────────────────────────────────────────────┐       │
│   │              SUPABASE + PGVECTOR                     │       │
│   │  conversas │ mensagens │ memorias │ entidades        │       │
│   │            │           │          │                  │       │
│   │  embedding vector(768) via Ollama nomic-embed-text   │       │
│   └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fases de Implementação

### Fase 1: Sync Periódico + Extração Básica
**Arquivos:**
- Modificar: `~/.claude/hooks/sync_sessions.py` (adicionar modo --cron)
- Criar: `~/ai-brain/scripts/extract_memories.py`
- Criar: `~/ai-brain/scripts/supabase_schema_v4.sql`

**Tarefas:**
1. Instalar Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Baixar modelo: `ollama pull nomic-embed-text`
3. Modificar sync_sessions.py para rodar via cron (incremental)
4. Criar extract_memories.py com prompt de extração
5. Configurar cron jobs
6. Executar schema v4 no Supabase

### Fase 2: Embeddings e pgvector
**Arquivos:**
- Criar: `~/ai-brain/scripts/generate_embeddings.py`

**Tarefas:**
1. Habilitar pgvector no Supabase
2. Criar script que gera embeddings via Ollama
3. Integrar embeddings no pipeline de extração

### Fase 3: Hooks de Retrieval
**Arquivos:**
- Criar: `~/.claude/hooks/memory_retrieval_hook.py`
- Criar: `~/.claude/hooks/file_memory_hook.py`
- Modificar: `~/.claude/settings.json`

**Tarefas:**
1. Hook user_prompt_submit → busca memórias → injeta contexto
2. Hook tool_use (Edit/Write/Read) → memórias de arquivo
3. Algoritmo de retrieval (entidades + semântico + filtros)

### Fase 4: Surprise Triggers
**Tarefas:**
1. Detectar recovery patterns (erro → sucesso)
2. Detectar correções do usuário
3. Detectar entusiasmo ("perfeito!", "exatamente!")
4. Detectar reações negativas ("nunca faça isso")
5. Boost no surprise_score das memórias

### Fase 5: Feedback Loop
**Tarefas:**
1. Registrar quais memórias foram surfaceadas
2. Coletar feedback (útil/não útil)
3. Re-ranking baseado em feedback (+/-5% por voto)

---

## Schema v4 (novas tabelas)

```sql
-- Habilitar pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabela principal de memórias
CREATE TABLE memorias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID REFERENCES conversas(id),
    mensagem_id UUID REFERENCES mensagens(id),
    tipo TEXT NOT NULL, -- decisao, insight, padrao, aprendizado, correcao, workflow, gap
    titulo TEXT NOT NULL,
    resumo TEXT NOT NULL,
    reasoning TEXT,
    contexto_original TEXT,
    confidence_score FLOAT DEFAULT 0.5,
    surprise_score FLOAT DEFAULT 0.0,
    feedback_score FLOAT DEFAULT 0.0,
    entidades_relacionadas JSONB DEFAULT '[]',
    arquivos_relacionados TEXT[],
    embedding vector(768),
    formada_em TIMESTAMPTZ,
    salva_em TIMESTAMPTZ DEFAULT NOW(),
    ultima_recuperacao TIMESTAMPTZ,
    vezes_recuperada INTEGER DEFAULT 0
);

-- Tracking de recuperações
CREATE TABLE memoria_recuperacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memoria_id UUID REFERENCES memorias(id),
    sessao_id TEXT NOT NULL,
    query_original TEXT,
    similarity_score FLOAT,
    foi_util BOOLEAN,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Entidades detectadas
CREATE TABLE entidades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo TEXT NOT NULL, -- pessoa, projeto, arquivo, repositorio
    nome TEXT NOT NULL,
    nome_normalizado TEXT,
    aliases TEXT[],
    metadata JSONB DEFAULT '{}',
    UNIQUE(tipo, nome_normalizado)
);

-- Tracking de processamento
CREATE TABLE processamento_memoria (
    conversa_id UUID PRIMARY KEY REFERENCES conversas(id),
    processado_em TIMESTAMPTZ DEFAULT NOW(),
    memorias_extraidas INTEGER DEFAULT 0,
    status TEXT DEFAULT 'sucesso'
);
```

---

## Cron Setup

```crontab
# Session sync - cada 5 minutos
*/5 * * * * python3 ~/.claude/hooks/sync_sessions.py --cron >> /tmp/ml_sync.log 2>&1

# Extração de memórias - cada 15 minutos
*/15 * * * * python3 ~/ai-brain/scripts/extract_memories.py >> /tmp/ml_extract.log 2>&1

# Geração de embeddings - cada 15 min (5 min após extração)
5,20,35,50 * * * * python3 ~/ai-brain/scripts/generate_embeddings.py >> /tmp/ml_embed.log 2>&1
```

---

## Tipos de Memória (como Hillman)

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| decisao | Escolha feita | "Decidimos usar Supabase ao invés de Firebase" |
| insight | Realização | "Descobri que hooks rodam antes do output" |
| padrao | Comportamento repetido | "Sempre commitar antes de push" |
| aprendizado | Conhecimento novo | "pgvector usa cosine similarity" |
| correcao | Erro corrigido | "UUID precisa de aspas no SQL" |
| workflow | Sequência de ações | "Para deploy: test → build → push" |
| gap | Desconexão identificada | "Sistema X e Y não conversam" |

---

## Surprise Triggers (boost de prioridade)

| Trigger | Peso | Detecção |
|---------|------|----------|
| Recovery pattern | +0.30 | Erro seguido de sucesso |
| User correction | +0.25 | "não, faça assim" |
| Enthusiasm | +0.20 | "perfeito!", "exatamente!" |
| Negative reaction | +0.25 | "nunca faça isso" |
| Repeat request | +0.15 | Mesmo pedido múltiplas vezes |

---

## Hook settings.json

```json
{
  "hooks": {
    "Stop": [...],
    "user_prompt_submit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/memory_retrieval_hook.py",
        "timeout": 5000
      }]
    }],
    "tool_use": [{
      "matcher": "Edit|Write|Read",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/file_memory_hook.py",
        "timeout": 3000
      }]
    }]
  }
}
```

---

## Arquivos a Criar/Modificar

| Arquivo | Ação | Fase |
|---------|------|------|
| `~/.claude/hooks/sync_sessions.py` | Modificar | 1 |
| `~/ai-brain/scripts/supabase_schema_v4.sql` | Criar | 1 |
| `~/ai-brain/scripts/extract_memories.py` | Criar | 1 |
| `~/ai-brain/scripts/generate_embeddings.py` | Criar | 2 |
| `~/.claude/hooks/memory_retrieval_hook.py` | Criar | 3 |
| `~/.claude/hooks/file_memory_hook.py` | Criar | 3 |
| `~/.claude/settings.json` | Modificar | 3 |

---

## Resultado Esperado
Sistema que:
1. Sincroniza sessões automaticamente a cada 5 min
2. Extrai memórias (decisões, insights, correções) a cada 15 min
3. Gera embeddings localmente via Ollama
4. Injeta memórias relevantes no contexto do Claude em tempo real
5. Aprende com feedback (memórias úteis sobem, inúteis descem)
