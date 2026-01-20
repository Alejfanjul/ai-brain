# AI Brain - Setup Técnico

## Variáveis de ambiente

```bash
# ~/ai-brain/.env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
ANTHROPIC_API_KEY=sk-ant-api03-...
```

## Dependências

- Python 3.x
- Ollama com modelo `nomic-embed-text`
- Supabase (free tier)

---

## Ollama (Embeddings locais)

### Comandos básicos

```bash
# Gerenciar serviço
sudo systemctl start ollama
sudo systemctl stop ollama
sudo systemctl status ollama

# Verificar se está rodando
curl localhost:11434/api/tags

# Ver modelos instalados
ollama list

# Instalar modelo de embeddings
ollama pull nomic-embed-text
```

### Verificar uso de GPU

```bash
# Ver se CUDA está disponível
nvidia-smi

# Verificar logs do Ollama (deve mostrar "using CUDA")
journalctl -u ollama -f
```

---

## Cron Jobs

```crontab
# Memory Lane System - AI Brain

# Extração de memórias + embeddings - cada 15 minutos
*/15 * * * * cd ~/ai-brain && python3 scripts/extract_memories.py >> /tmp/ml_extract.log 2>&1 && python3 scripts/generate_embeddings.py >> /tmp/ml_embeddings.log 2>&1
```

### Configurar cron

```bash
crontab -e
# Adicionar a linha acima
```

### Verificar se está configurado

```bash
crontab -l
```

### Logs

- Extração: `/tmp/ml_extract.log`
- Embeddings: `/tmp/ml_embeddings.log`

---

## Supabase - Schema

### Tabela: conversas

```sql
CREATE TABLE conversas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT UNIQUE,
    repositorio TEXT NOT NULL,
    primeira_mensagem TEXT,
    ultima_mensagem TEXT,
    transcript_completo JSONB,
    arquivos_tocados TEXT[],
    tool_calls JSONB,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);
```

### Tabela: memorias

```sql
CREATE TABLE memorias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sessao_id UUID REFERENCES conversas(id),
    tipo TEXT, -- 'decisao', 'insight', 'padrao', 'aprendizado', 'correcao', 'workflow', 'gap'
    resumo TEXT,
    contexto_original TEXT,
    confidence_score FLOAT,
    embedding VECTOR(768),
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Índice para busca vetorial
CREATE INDEX idx_memorias_embedding ON memorias
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### Tabela: source_chunks

```sql
CREATE TABLE source_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file TEXT,        -- ex: "2026-01-06-nate-..."
    autor TEXT,              -- ex: "nate", "hillman"
    chunk_index INTEGER,     -- posição no arquivo
    content TEXT,            -- o texto do chunk
    embedding VECTOR(768),
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Índice para busca vetorial
CREATE INDEX idx_source_chunks_embedding ON source_chunks
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### Habilitar pgvector

```sql
-- Rodar uma vez no Supabase Dashboard > SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

### Funções RPC para busca vetorial

```sql
-- Rodar no Supabase Dashboard > SQL Editor

-- Busca em source_chunks
CREATE OR REPLACE FUNCTION search_sources(
  query_embedding vector(768),
  match_count int DEFAULT 5,
  filter_autor text DEFAULT NULL
)
RETURNS TABLE (
  id uuid,
  source_file text,
  autor text,
  chunk_index int,
  content text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    sc.id,
    sc.source_file,
    sc.autor,
    sc.chunk_index,
    sc.content,
    1 - (sc.embedding <=> query_embedding) as similarity
  FROM source_chunks sc
  WHERE (filter_autor IS NULL OR sc.autor = filter_autor)
  ORDER BY sc.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- Busca em memorias
CREATE OR REPLACE FUNCTION search_memories(
  query_embedding vector(768),
  match_count int DEFAULT 5
)
RETURNS TABLE (
  id uuid,
  tipo text,
  titulo text,
  resumo text,
  contexto_original text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    m.id,
    m.tipo,
    m.titulo,
    m.resumo,
    m.contexto_original,
    1 - (m.embedding <=> query_embedding) as similarity
  FROM memorias m
  WHERE m.embedding IS NOT NULL AND m.ativo = true
  ORDER BY m.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

---

## Scripts disponíveis

| Script | Descrição | Uso |
|--------|-----------|-----|
| `scripts/extract_memories.py` | Extrai memórias das conversas via Haiku | `python3 scripts/extract_memories.py` |
| `scripts/generate_embeddings.py` | Gera embeddings das memórias | `python3 scripts/generate_embeddings.py` |
| `scripts/embed_sources.py` | Gera embeddings dos sources | `python3 scripts/embed_sources.py` |
| `scripts/search.py` | Busca semântica em memórias e sources | `python3 scripts/search.py "query"` |
| `scripts/show_goals.py` | Mostra progresso das metas pessoais | `python3 scripts/show_goals.py` |
| `scripts/daily_digest.py` | Gera relatório diário das metas | `python3 scripts/daily_digest.py` |

### Verificar progresso dos embeddings

```bash
# Ver quantos chunks foram processados
python3 -c "
from scripts.embed_sources import supabase_request
result = supabase_request('source_chunks?select=id&limit=10000')
print(f'Total chunks: {len(result)}')
"

# Dry run - ver quantos faltam
python3 scripts/embed_sources.py --dry-run
```

---

## Continuar processamento na máquina com GPU

1. **Verificar GPU:**
```bash
nvidia-smi
```

2. **Iniciar Ollama e verificar CUDA:**
```bash
sudo systemctl start ollama
journalctl -u ollama -f
# Deve mostrar "using CUDA" ou "GPU detected"
```

3. **Verificar modelo:**
```bash
ollama list
# Se não tiver nomic-embed-text:
ollama pull nomic-embed-text
```

4. **Atualizar repo e rodar:**
```bash
cd ~/ai-brain
git pull
python3 scripts/embed_sources.py
```

**Tempo estimado com GPU:** ~2-5 minutos para ~700 chunks restantes.

---

## Daily Digest / Goals System

Sistema para visualizar progresso das metas pessoais (treino e hábitos).

### Arquitetura

```
scripts/
├── goals/                    # Módulo de metas
│   ├── __init__.py
│   ├── parser.py             # Parse SAUDE.md e MACONHA.md
│   ├── progress.py           # Calcula métricas
│   └── ascii_charts.py       # Gráficos ASCII
├── daily_digest.py           # Gerador principal
└── show_goals.py             # Comando CLI

~/.claude/skills/DailyGoals/  # Skill para /goals
```

### Comandos

```bash
# Visão completa com ASCII art
python3 scripts/show_goals.py

# Só o foco do dia
python3 scripts/show_goals.py --today

# Só treino
python3 scripts/show_goals.py --saude

# Só redução de maconha
python3 scripts/show_goals.py --maconha

# Saída JSON
python3 scripts/show_goals.py --json

# Resumo em uma linha
python3 scripts/daily_digest.py --short
```

### Cron (opcional)

Para gerar relatório automático às 7h:

```crontab
0 7 * * * cd ~/ai-brain && python3 scripts/daily_digest.py >> /tmp/daily_digest.log 2>&1
```

### Skill PAI

O skill `/goals` ou `/metas` está em `~/.claude/skills/DailyGoals/SKILL.md`.

### Dados fonte

- `projects/ai-brain/metas/SAUDE.md` - Dados de treino (ciclos, semanas, log)
- `projects/ai-brain/metas/MACONHA.md` - Dados de redução (fases, streak, log)
