# Plano: Memory Lane System (baseado no JFDI do Hillman)

> **Contexto:** Este plano implementa o **Marco 3: Memória e Síntese** do documento [`ai_brain_parceiro_digital-v0.4.md`](./ai_brain_parceiro_digital-v0.4.md).
>
> Marcos anteriores já foram concluídos:
> - ✅ Marco 1: Audit Trail (hooks + Supabase)
> - ✅ Marco 2: Persistência de Conversas (81 sessões, 1000+ mensagens salvas)

## Objetivo
Implementar sistema completo de memória para o AI Brain, similar ao Memory Lane do Alex Hillman.

## Decisões do usuário
- **Embeddings:** Ollama (local, gratuito)
- **Frequência:** 5 min sync sessões, 15 min extração memórias
- **Interface:** Backend primeiro (sem UI)
- **Scheduler:** Cron (simples)

---

## Status de Implementação

| Fase | Status | Data |
|------|--------|------|
| Fase 1: Sync Periódico + Extração | ✅ Concluída | 2026-01-05 |
| Fase 2: Embeddings e pgvector | ✅ Concluída | 2026-01-06 |
| Fase 3: Hooks de Retrieval | 📋 Pendente | - |
| Fase 4: Surprise Triggers | 📋 Pendente | - |
| Fase 5: Feedback Loop | 📋 Pendente | - |
| Fase 6: Auto-Atualização de Planos | 📋 Pendente | - |

### Resultados da Fase 1
- **22 memórias extraídas** das conversas existentes
- Tipos: 8 workflows, 6 decisões, 6 insights, 1 correção, 1 padrão
- Cron jobs configurados e funcionando

### Resultados da Fase 2
- **40 memórias com embeddings** (768 dimensões via nomic-embed-text)
- Script `generate_embeddings.py` criado e funcionando
- Ollama instalado e configurado localmente
- Índice IVFFlat pendente (criar via Supabase Dashboard)

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                      MEMORY LANE SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CRON JOBS (✅ ATIVO)                CLAUDE CODE HOOKS (pendente)│
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
│   │              SUPABASE + PGVECTOR (✅ ATIVO)          │       │
│   │  conversas │ mensagens │ memorias │ entidades        │       │
│   │            │           │          │                  │       │
│   │  embedding vector(768) via Ollama nomic-embed-text   │       │
│   └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fases de Implementação

### ✅ Fase 1: Sync Periódico + Extração Básica (CONCLUÍDA)

**Arquivos criados/modificados:**
- ✅ `~/.claude/hooks/sync_sessions.py` - modo --cron adicionado
- ✅ `~/ai-brain/scripts/extract_memories.py` - extração via Claude Haiku
- ✅ `~/ai-brain/scripts/supabase_schema_v4.sql` - schema com pgvector

**Tarefas concluídas:**
1. ✅ Instalar Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. ✅ Baixar modelo: `ollama pull nomic-embed-text`
3. ✅ Modificar sync_sessions.py para rodar via cron (incremental)
4. ✅ Criar extract_memories.py com prompt de extração
5. ✅ Configurar cron jobs
6. ✅ Executar schema v4 no Supabase
7. ✅ Configurar ANTHROPIC_API_KEY no .env

### ✅ Fase 2: Embeddings e pgvector (CONCLUÍDA)

**Arquivos criados:**
- ✅ `~/ai-brain/scripts/generate_embeddings.py` - geração via Ollama

**Tarefas concluídas:**
1. ✅ Habilitar pgvector no Supabase (já estava no schema v4)
2. ✅ Instalar Ollama e modelo nomic-embed-text
3. ✅ Criar script que gera embeddings via Ollama
4. ✅ Processar 40 memórias existentes
5. 📋 Criar índice IVFFlat (pendente - rodar no Supabase Dashboard)

**SQL para criar índice (rodar no Supabase Dashboard > SQL Editor):**
```sql
CREATE INDEX IF NOT EXISTS idx_memorias_embedding ON memorias
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

**Contexto da conversa 2026-01-06:**
Durante a implementação, discutimos o artigo "Context Engineering for AI Agents" do Manus.
Decisão: AI Brain é a fundação (memória + contexto) para futuros sistemas agentic.

### 📋 Fase 3: Hooks de Retrieval (PENDENTE)

**Arquivos a criar:**
- `~/.claude/hooks/memory_retrieval_hook.py`
- `~/.claude/hooks/file_memory_hook.py`

**Tarefas:**
1. Hook user_prompt_submit → busca memórias → injeta contexto
2. Hook tool_use (Edit/Write/Read) → memórias de arquivo
3. Algoritmo de retrieval (entidades + semântico + filtros)

### 📋 Fase 4: Surprise Triggers (PENDENTE)

**Tarefas:**
1. Detectar recovery patterns (erro → sucesso)
2. Detectar correções do usuário
3. Detectar entusiasmo ("perfeito!", "exatamente!")
4. Detectar reações negativas ("nunca faça isso")
5. Boost no surprise_score das memórias

### 📋 Fase 5: Feedback Loop (PENDENTE)

**Tarefas:**
1. Registrar quais memórias foram surfaceadas
2. Coletar feedback (útil/não útil)
3. Re-ranking baseado em feedback (+/-5% por voto)

### 📋 Fase 6: Auto-Atualização de Planos (PENDENTE)

**Objetivo:** Sistema analisa conversas e atualiza automaticamente arquivos de planejamento.

**Arquivos a criar:**
- `~/ai-brain/scripts/update_plans.py`

**Tarefas:**
1. Analisar conversas em busca de:
   - Decisões tomadas (atualizar status de itens)
   - Novos itens identificados (adicionar ao roadmap)
   - Mudanças de escopo (ajustar descrições)
   - Conclusões de tarefas (marcar como ✅)
2. Gerar diff proposto antes de aplicar mudanças
3. Aplicar mudanças nos arquivos `.md` de planejamento
4. Commitar automaticamente com mensagem descritiva

**Arquivos monitorados:**
- `projects/ai-brain/ai_brain_parceiro_digital-v*.md`
- `projects/ai-brain/memory_lane_plan.md`
- `projects/*/README.md`

**Frequência:** Diária ou ao final de sessões significativas

**Insight:** Isso fecha o loop - o sistema não só aprende das conversas, mas mantém sua própria documentação atualizada.

---

## Cron Setup (✅ ATIVO)

```crontab
# Memory Lane System - AI Brain
# Session sync - cada 5 minutos
*/5 * * * * python3 ~/.claude/hooks/sync_sessions.py --cron >> /tmp/ml_sync.log 2>&1

# Extração de memórias - cada 15 minutos
*/15 * * * * python3 ~/ai-brain/scripts/extract_memories.py >> /tmp/ml_extract.log 2>&1
```

**Logs:**
- Sync: `/tmp/ml_sync.log`
- Extração: `/tmp/ml_extract.log`

---

## Tipos de Memória

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

## Configuração Necessária

### .env (~/ai-brain/.env)
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Dependências
- Python 3.x (já instalado)
- Ollama com modelo `nomic-embed-text`
- Supabase com schema v4 executado

---

## Referências
- [Documento principal do AI Brain](./ai_brain_parceiro_digital-v0.4.md)
- [Alex Hillman - Memory Lane](https://www.youtube.com/watch?v=Wpz7LNI737Q)
- [JFDI System](../../sources/2025-12-13-alex-hillman-jfdi-system-my-ai-executive-assistant-full-life-co.md)
