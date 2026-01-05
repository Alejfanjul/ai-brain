-- Schema AI Brain v2 - Conversas Completas
-- Executar no Supabase SQL Editor

-- Dropar tabelas antigas (opcional - descomente se quiser limpar)
-- DROP TABLE IF EXISTS audits;
-- DROP TABLE IF EXISTS sessoes;

-- Tabela de conversas (uma por sessao do Claude Code)
CREATE TABLE IF NOT EXISTS conversas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT UNIQUE NOT NULL,
    repositorio TEXT NOT NULL,
    cwd TEXT,
    resumo TEXT,
    total_mensagens INTEGER DEFAULT 0,
    total_tokens_estimado INTEGER DEFAULT 0,
    arquivos_tocados TEXT[],
    ferramentas_usadas TEXT[],
    teve_erros BOOLEAN DEFAULT FALSE,
    teve_correcoes BOOLEAN DEFAULT FALSE,
    iniciado_em TIMESTAMPTZ,
    finalizado_em TIMESTAMPTZ,
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de mensagens (cada mensagem user ou assistant)
CREATE TABLE IF NOT EXISTS mensagens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID REFERENCES conversas(id) ON DELETE CASCADE,
    uuid_original TEXT,
    tipo TEXT NOT NULL, -- 'user' ou 'assistant'
    conteudo TEXT, -- texto da mensagem
    conteudo_json JSONB, -- conteudo completo para assistant (tool_use, etc)
    ferramentas_usadas TEXT[], -- array de tools usadas nesta mensagem
    arquivos_mencionados TEXT[],
    tem_erro BOOLEAN DEFAULT FALSE,
    tem_correcao BOOLEAN DEFAULT FALSE,
    timestamp_original TIMESTAMPTZ,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de aprendizados extraidos (para Fase 2)
CREATE TABLE IF NOT EXISTS aprendizados (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID REFERENCES conversas(id),
    mensagem_id UUID REFERENCES mensagens(id),
    tipo TEXT NOT NULL, -- 'erro', 'correcao', 'decisao', 'padrao', 'insight'
    descricao TEXT NOT NULL,
    contexto TEXT,
    tags TEXT[],
    relevancia FLOAT DEFAULT 0.5,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Indices para performance
CREATE INDEX IF NOT EXISTS idx_conversas_repositorio ON conversas(repositorio);
CREATE INDEX IF NOT EXISTS idx_conversas_session_id ON conversas(session_id);
CREATE INDEX IF NOT EXISTS idx_conversas_iniciado_em ON conversas(iniciado_em DESC);
CREATE INDEX IF NOT EXISTS idx_mensagens_conversa_id ON mensagens(conversa_id);
CREATE INDEX IF NOT EXISTS idx_mensagens_tipo ON mensagens(tipo);
CREATE INDEX IF NOT EXISTS idx_mensagens_timestamp ON mensagens(timestamp_original DESC);
CREATE INDEX IF NOT EXISTS idx_aprendizados_tipo ON aprendizados(tipo);
CREATE INDEX IF NOT EXISTS idx_aprendizados_conversa_id ON aprendizados(conversa_id);

-- RLS
ALTER TABLE conversas ENABLE ROW LEVEL SECURITY;
ALTER TABLE mensagens ENABLE ROW LEVEL SECURITY;
ALTER TABLE aprendizados ENABLE ROW LEVEL SECURITY;

-- Politicas permissivas (ajustar depois se necessario)
DROP POLICY IF EXISTS "Allow all for conversas" ON conversas;
DROP POLICY IF EXISTS "Allow all for mensagens" ON mensagens;
DROP POLICY IF EXISTS "Allow all for aprendizados" ON aprendizados;

CREATE POLICY "Allow all for conversas" ON conversas FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for mensagens" ON mensagens FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for aprendizados" ON aprendizados FOR ALL USING (true) WITH CHECK (true);
