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

# Session sync - cada 5 minutos
*/5 * * * * python3 ~/.claude/hooks/sync_sessions.py --cron >> /tmp/ml_sync.log 2>&1

# Extração de memórias - cada 15 minutos
*/15 * * * * python3 ~/ai-brain/scripts/extract_memories.py >> /tmp/ml_extract.log 2>&1
```

### Logs

- Sync: `/tmp/ml_sync.log`
- Extração: `/tmp/ml_extract.log`

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

---

## Scripts disponíveis

| Script | Descrição | Uso |
|--------|-----------|-----|
| `scripts/extract_memories.py` | Extrai memórias das conversas via Haiku | `python3 scripts/extract_memories.py` |
| `scripts/generate_embeddings.py` | Gera embeddings das memórias | `python3 scripts/generate_embeddings.py` |
| `scripts/embed_sources.py` | Gera embeddings dos sources | `python3 scripts/embed_sources.py` |
| `~/.claude/hooks/sync_sessions.py` | Sincroniza sessões com Supabase | `python3 ~/.claude/hooks/sync_sessions.py --cron` |

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
