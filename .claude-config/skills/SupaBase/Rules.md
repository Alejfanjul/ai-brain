# Regras do Banco de Dados — Sistema OS

16 regras extraidas do `~/sistema-os/docs/LEARNINGS.md`. Seguir TODAS antes de gerar SQL ou migrations.

---

## 1. ENUMs SEMPRE lowercase

Valores no banco sao SEMPRE lowercase. Nunca inserir UPPERCASE.

```sql
-- ERRADO
INSERT INTO reservas (status) VALUES ('CONFIRMADA');
WHERE status = 'EM_ANDAMENTO';

-- CORRETO
INSERT INTO reservas (status) VALUES ('confirmada');
WHERE status = 'em_andamento';
```

**No Python:** `.lower()` obrigatorio antes de inserir valores enum.

---

## 2. Consultar schema ANTES de implementar

SEMPRE ler o schema real antes de assumir nomes de colunas ou tipos.

```bash
# Schema mais recente
ls -lt ~/sistema-os/docs/schemas/supabase_full_schema_*.sql | head -1

# Buscar definicao de tabela
grep -A 30 "CREATE TABLE hospedes" ~/sistema-os/docs/schemas/supabase_full_schema_*.sql
```

Nao assumir nomes — verificar. `is_active` vs `active`, `room_category` vs `category_name`.

---

## 3. Soft delete: sempre filtrar deleted_at

TODA query deve incluir `WHERE deleted_at IS NULL` para cada tabela envolvida.

```sql
-- ERRADO
SELECT * FROM hospedes WHERE nome_completo ILIKE '%joao%';

-- CORRETO
SELECT * FROM hospedes WHERE nome_completo ILIKE '%joao%' AND deleted_at IS NULL;
```

Em joins, filtrar em TODAS as tabelas:
```sql
SELECT h.nome_completo, r.numero
FROM hospedes h
JOIN reserva_hospedes rh ON rh.hospede_id = h.id AND rh.deleted_at IS NULL
JOIN reservas r ON r.id = rh.reserva_id AND r.deleted_at IS NULL
WHERE h.deleted_at IS NULL;
```

---

## 4. server_default (nao default do SQLAlchemy)

SQLAlchemy `default=` so funciona via ORM. Para queries via REST API/Supabase, usar `server_default`.

```python
# ERRADO — nao funciona via API REST
created_at = Column(DateTime, default=func.now())

# CORRETO — funciona sempre
created_at = Column(DateTime, server_default=sa.text("timezone('utc', now())"))
```

---

## 5. CAST de enums em WHERE (SQLAlchemy)

PostgreSQL enums exigem cast explicito em queries SQLAlchemy.

```python
# ERRADO — pode causar erro de tipo
query = query.where(OS.status == "confirmada")

# CORRETO
from sqlalchemy import cast, String
query = query.where(cast(OS.status, String) == "confirmada")
```

---

## 6. BaseModel columns obrigatorias

Toda tabela deve ter as colunas do BaseModel. Verificar antes de criar migration.

```sql
id SERIAL PRIMARY KEY,
created_at TIMESTAMP NOT NULL DEFAULT timezone('utc', now()),
updated_at TIMESTAMP NOT NULL DEFAULT timezone('utc', now()),
deleted_at TIMESTAMP  -- NULL = ativo, preenchido = soft deleted
```

---

## 7. Normalizar UMA VEZ no ponto de entrada

Normalizar dados (enum, formato) uma unica vez no parser/ponto de entrada. Consumidores assumem valor ja normalizado.

```python
# ERRADO — normalizar em multiplos pontos
def parse(): return "bb"
def display(val): return normalize(val)  # re-normaliza

# CORRETO — normalizar no parser, consumidores confiam
def parse(): return "bb"  # normalizado aqui
def display(val): return LABELS[val]  # confia no valor
```

---

## 8. ID e auto-increment — omitir em INSERTs

Tabelas usam `id SERIAL PRIMARY KEY`. Nunca enviar `id` em inserts.

```sql
-- ERRADO
INSERT INTO hospedes (id, nome_completo) VALUES (1, 'Joao');

-- CORRETO
INSERT INTO hospedes (nome_completo) VALUES ('Joao');
```

---

## 9. Async client obrigatorio em codigo async

Em codigo FastAPI (async), nunca usar `httpx.Client` sincrono.

```python
# ERRADO — bloqueia event loop
with httpx.Client() as client:
    response = client.get(url)

# CORRETO
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

---

## 10. Batch insert: mesmas chaves em todos objetos

Supabase REST API exige que batch inserts tenham exatamente as mesmas chaves em todos os objetos.

```python
# ERRADO — chaves diferentes
data = [
    {"nome": "A", "email": "a@x.com"},
    {"nome": "B"}  # falta email
]

# CORRETO
data = [
    {"nome": "A", "email": "a@x.com"},
    {"nome": "B", "email": None}  # mesmas chaves
]
```

---

## 11. Eager loading para relacionamentos

Usar joinedload/selectinload em queries que precisam de dados relacionados. Evita N+1.

```python
from sqlalchemy.orm import joinedload, selectinload

query = (
    select(OS)
    .options(
        joinedload(OS.hospede),
        selectinload(OS.itens).selectinload(OSItem.produto)
    )
    .where(OS.id == id, OS.deleted_at.is_(None))
)
```

---

## 12. Timestamps timezone-naive (UTC)

O banco usa timestamps sem timezone, assumindo UTC. Nao usar `timestamptz`.

```sql
-- Padrao do sistema
created_at TIMESTAMP NOT NULL DEFAULT timezone('utc', now())
-- NAO usar
created_at TIMESTAMPTZ
```

---

## 13. Session Pooler para asyncpg (porta 5432)

SQLAlchemy async com asyncpg exige **Session Pooler** (porta 5432). Transaction Pooler (porta 6543) nao suporta prepared statements.

```python
# ERRADO — Transaction Pooler, falha com asyncpg
DATABASE_URL = "postgresql+asyncpg://user:pass@host:6543/db"

# CORRETO — Session Pooler
DATABASE_URL = "postgresql+asyncpg://user:pass@host:5432/db"
```

| Feature | Transaction (6543) | Session (5432) |
|---------|-------------------|----------------|
| Prepared Statements | Nao | Sim |
| Conexoes simultaneas | >10k | ~200 |
| Compatibilidade asyncpg | Nao | Total |

---

## 14. WSL2: usar REST API para operacoes em massa

Em WSL2, conexao direta Python → Supabase PostgreSQL falha (firewall virtualizado). Usar REST API com httpx.

```python
# ERRADO em WSL2 — timeout/connection refused
engine = create_async_engine("postgresql+asyncpg://...")

# CORRETO em WSL2 — REST API com batch upsert
headers = {
    "apikey": SUPABASE_KEY,
    "Prefer": "resolution=merge-duplicates"
}
response = client.post(f"{SUPABASE_URL}/rest/v1/hospedes", json=batch)
```

Em producao (Linux real), SQLAlchemy direto funciona normalmente.

---

## 15. Indices em colunas de filtro

Colunas usadas em WHERE/JOIN frequentes devem ter indice. Sem indice = full table scan.

```sql
-- Campos que merecem indice
CREATE INDEX IF NOT EXISTS ix_hospedes_cpf ON hospedes(numero_documento);
CREATE INDEX IF NOT EXISTS ix_hospedes_celular ON hospedes(celular);
CREATE INDEX IF NOT EXISTS ix_hospedes_email ON hospedes(email);
CREATE INDEX IF NOT EXISTS ix_reservas_status ON reservas(status);
-- Foreign keys (se nao criados automaticamente)
CREATE INDEX IF NOT EXISTS ix_os_itens_os_id ON os_itens(os_id);
```

Regra: se voce faz `WHERE campo = valor` frequentemente, crie indice nesse campo.

---

## 16. RLS (Row Level Security) em toda tabela nova

Toda tabela nova deve ter RLS habilitado. Mesmo que o acesso seja via backend (FastAPI), previne exposicao acidental via anon key do Supabase.

```sql
-- OBRIGATORIO ao criar tabela
ALTER TABLE nome_tabela ENABLE ROW LEVEL SECURITY;

-- Policy minima (permite tudo via service_role, bloqueia anon)
CREATE POLICY "service_role_full_access" ON nome_tabela
    FOR ALL USING (auth.role() = 'service_role');

-- Se precisar acesso via anon key (raro no sistema-os)
CREATE POLICY "anon_read" ON nome_tabela
    FOR SELECT USING (true);
```

Sem RLS, qualquer pessoa com a anon key pode ler/escrever toda a tabela via PostgREST.
