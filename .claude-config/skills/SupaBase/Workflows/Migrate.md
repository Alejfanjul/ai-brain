# Migrate Workflow

Cria migrations SQL para o banco do sistema-os seguindo todas as convencoes do projeto.

## Steps

### 1. Carregar regras

Ler `Rules.md` (na raiz do skill). Todas as 16 regras se aplicam a migrations.

### 2. Consultar schema atual

Verificar o estado atual do banco antes de alterar:
```bash
# Schema mais recente
ls -lt ~/sistema-os/docs/schemas/supabase_full_schema_*.sql | head -1

# Ver tabela especifica
grep -A 40 "CREATE TABLE nome_tabela" ~/sistema-os/docs/schemas/supabase_full_schema_*.sql
```

### 3. Verificar migrations existentes

Checar se ja existe migration parecida ou conflitante:
```bash
ls ~/sistema-os/scripts/migrations/ | sort
```

### 4. Definir naming

Formato: `YYYYMMDD_NNN_descricao.sql`

Exemplos:
- `20260214_001_add_observacoes_to_reservas.sql`
- `20260214_002_create_enum_status_pagamento.sql`

Usar a data de hoje. Incrementar NNN se ja existir migration do mesmo dia.

### 5. Gerar SQL da migration

Seguir o template abaixo. TODA migration deve ser idempotente.

### 6. Checklist de validacao

Antes de salvar, verificar TODOS os itens:

- [ ] ENUMs em lowercase (`'confirmada'`, nunca `'CONFIRMADA'`)
- [ ] `IF NOT EXISTS` para CREATE TABLE e CREATE TYPE
- [ ] `DO $$ BEGIN ... END $$` block para CREATE TYPE quando enum pode ja existir
- [ ] Colunas BaseModel presentes (id, created_at, updated_at, deleted_at)
- [ ] `server_default` (nao `default`) para valores padrao
- [ ] Timestamps como `TIMESTAMP` (sem timezone), default `timezone('utc', now())`
- [ ] Foreign keys com ON DELETE adequado (CASCADE, SET NULL, ou RESTRICT)
- [ ] Indices para colunas usadas em WHERE/JOIN frequentes
- [ ] Comentario descritivo no topo do arquivo

### 7. Salvar migration

Salvar em `~/sistema-os/scripts/migrations/` com o naming definido no step 4.

### 8. Atualizar model SQLAlchemy (se aplicavel)

Se a migration cria/altera tabela que tem model Python:
- Atualizar model em `~/sistema-os/app/models/`
- Atualizar enums em `~/sistema-os/app/models/enums.py` se novo enum
- Atualizar schema Pydantic em `~/sistema-os/app/schemas/` se necessario

---

## Template de Migration

```sql
-- Migration: YYYYMMDD_NNN_descricao
-- Descricao: [O que essa migration faz]
-- Autor: Ale + Claude
-- Data: YYYY-MM-DD

-- ============================================================
-- 1. Enums (se necessario)
-- ============================================================

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'nome_enum') THEN
        CREATE TYPE nome_enum AS ENUM (
            'valor_a',      -- descricao
            'valor_b'       -- descricao (SEMPRE lowercase)
        );
    END IF;
END $$;

-- ============================================================
-- 2. Tabela (se necessario)
-- ============================================================

CREATE TABLE IF NOT EXISTS nome_tabela (
    id SERIAL PRIMARY KEY,
    -- campos especificos
    campo_texto VARCHAR(255) NOT NULL,
    campo_enum VARCHAR(50) NOT NULL DEFAULT 'valor_a',
    campo_fk INTEGER REFERENCES outra_tabela(id) ON DELETE CASCADE,
    -- BaseModel columns (OBRIGATORIO)
    created_at TIMESTAMP NOT NULL DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP NOT NULL DEFAULT timezone('utc', now()),
    deleted_at TIMESTAMP
);

-- ============================================================
-- 3. Indices
-- ============================================================

CREATE INDEX IF NOT EXISTS ix_nome_tabela_campo
    ON nome_tabela(campo_texto);

-- ============================================================
-- 4. Alteracoes em tabela existente (se necessario)
-- ============================================================

-- ALTER TABLE nome_tabela ADD COLUMN IF NOT EXISTS novo_campo VARCHAR(500);

-- ============================================================
-- 5. RLS (Row Level Security) — OBRIGATORIO para tabelas novas
-- ============================================================

ALTER TABLE nome_tabela ENABLE ROW LEVEL SECURITY;

-- Policy padrao: acesso total via service_role (backend), bloqueio via anon
CREATE POLICY "service_role_full_access" ON nome_tabela
    FOR ALL USING (auth.role() = 'service_role');
```
