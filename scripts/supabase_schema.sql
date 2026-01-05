-- Schema AI Brain - Audit Trail
-- Executar no Supabase SQL Editor

-- Tabela de sessoes de chat
CREATE TABLE sessoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT UNIQUE,
    repositorio TEXT NOT NULL,
    cwd TEXT,
    primeira_mensagem TEXT,
    ultima_mensagem TEXT,
    mensagens_count INTEGER DEFAULT 0,
    arquivos_tocados TEXT[],
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de audit trails
CREATE TABLE audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sessao_id UUID REFERENCES sessoes(id),
    repositorio TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    tool_input JSONB,
    tool_output TEXT,
    file_path TEXT,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Indices para performance
CREATE INDEX idx_sessoes_repositorio ON sessoes(repositorio);
CREATE INDEX idx_sessoes_criado_em ON sessoes(criado_em DESC);
CREATE INDEX idx_audits_sessao_id ON audits(sessao_id);
CREATE INDEX idx_audits_repositorio ON audits(repositorio);
CREATE INDEX idx_audits_tool_name ON audits(tool_name);
CREATE INDEX idx_audits_criado_em ON audits(criado_em DESC);

-- Habilitar RLS (Row Level Security) - por enquanto desabilitado para simplicidade
ALTER TABLE sessoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE audits ENABLE ROW LEVEL SECURITY;

-- Politica para permitir todas as operacoes (ajustar depois se necessario)
CREATE POLICY "Allow all for sessoes" ON sessoes FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for audits" ON audits FOR ALL USING (true) WITH CHECK (true);
