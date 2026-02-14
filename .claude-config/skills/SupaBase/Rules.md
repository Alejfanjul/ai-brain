# Regras do Banco de Dados — Sistema OS

12 regras extraidas do `~/sistema-os/docs/LEARNINGS.md`. Seguir TODAS antes de gerar SQL ou migrations.

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
