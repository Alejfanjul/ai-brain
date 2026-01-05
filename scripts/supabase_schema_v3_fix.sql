-- Fix para adicionar colunas faltantes do v3
-- Executar no Supabase SQL Editor

-- Colunas faltantes em conversas
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS objetivo TEXT;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS resultado TEXT;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS tags TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS arquivos_criados TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS arquivos_modificados TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS comandos_executados TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS total_erros INTEGER DEFAULT 0;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS total_correcoes INTEGER DEFAULT 0;

-- Indice para tags
CREATE INDEX IF NOT EXISTS idx_conversas_tags ON conversas USING GIN(tags);

-- Colunas faltantes em mensagens
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS is_error BOOLEAN DEFAULT FALSE;
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS is_correction BOOLEAN DEFAULT FALSE;
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS intent TEXT;
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS tokens_estimado INTEGER;

-- Indices
CREATE INDEX IF NOT EXISTS idx_mensagens_is_error ON mensagens(is_error) WHERE is_error = TRUE;
CREATE INDEX IF NOT EXISTS idx_mensagens_is_correction ON mensagens(is_correction) WHERE is_correction = TRUE;
