-- Schema AI Brain v4 - Memory Lane System
-- Executar no Supabase SQL Editor
-- Referência: memory_lane_plan.md (Fase 3 do AI Brain)

-- ============================================================
-- HABILITAR PGVECTOR (para embeddings)
-- ============================================================
-- Nota: pgvector já vem habilitado no Supabase por padrão
-- Se der erro, vá em Database > Extensions e habilite "vector"
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- MEMORIAS (tabela principal do Memory Lane)
-- ============================================================
CREATE TABLE IF NOT EXISTS memorias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID REFERENCES conversas(id) ON DELETE CASCADE,
    mensagem_id UUID REFERENCES mensagens(id) ON DELETE SET NULL,

    -- Conteúdo da memória
    tipo TEXT NOT NULL, -- decisao, insight, padrao, aprendizado, correcao, workflow, gap
    titulo TEXT NOT NULL,
    resumo TEXT NOT NULL,
    reasoning TEXT, -- por que essa memória foi capturada
    contexto_original TEXT, -- trecho do transcript

    -- Scores
    confidence_score FLOAT DEFAULT 0.5, -- 0-1, confiança na extração
    surprise_score FLOAT DEFAULT 0.0, -- 0-1, boost de surprise triggers
    feedback_score FLOAT DEFAULT 0.0, -- acumulado de +/- feedback

    -- Relacionamentos
    entidades_relacionadas JSONB DEFAULT '[]', -- [{type, name, id}]
    arquivos_relacionados TEXT[],

    -- Embedding (nomic-embed-text = 768 dimensões)
    embedding vector(768),

    -- Timestamps
    formada_em TIMESTAMPTZ, -- quando o momento original aconteceu
    salva_em TIMESTAMPTZ DEFAULT NOW(),
    ultima_recuperacao TIMESTAMPTZ,
    vezes_recuperada INTEGER DEFAULT 0,

    -- Controle
    ativo BOOLEAN DEFAULT TRUE
);

-- Índices para memorias
CREATE INDEX IF NOT EXISTS idx_memorias_tipo ON memorias(tipo);
CREATE INDEX IF NOT EXISTS idx_memorias_conversa ON memorias(conversa_id);
CREATE INDEX IF NOT EXISTS idx_memorias_formada ON memorias(formada_em DESC);
CREATE INDEX IF NOT EXISTS idx_memorias_ativo ON memorias(ativo) WHERE ativo = TRUE;
CREATE INDEX IF NOT EXISTS idx_memorias_confidence ON memorias(confidence_score DESC);

-- Índice para busca vetorial (IVFFlat - bom para datasets médios)
-- Nota: Só criar após ter algumas memórias, senão dá erro
-- CREATE INDEX IF NOT EXISTS idx_memorias_embedding ON memorias
--     USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================================
-- MEMORIA_RECUPERACOES (tracking de quando memórias são surfaceadas)
-- ============================================================
CREATE TABLE IF NOT EXISTS memoria_recuperacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memoria_id UUID REFERENCES memorias(id) ON DELETE CASCADE,
    sessao_id TEXT NOT NULL, -- Claude Code session ID
    query_original TEXT, -- o que triggou o recall
    similarity_score FLOAT,
    foi_util BOOLEAN, -- thumbs up/down
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_recuperacoes_memoria ON memoria_recuperacoes(memoria_id);
CREATE INDEX IF NOT EXISTS idx_recuperacoes_sessao ON memoria_recuperacoes(sessao_id);
CREATE INDEX IF NOT EXISTS idx_recuperacoes_criado ON memoria_recuperacoes(criado_em DESC);

-- ============================================================
-- ENTIDADES (pessoas, projetos, arquivos detectados)
-- ============================================================
CREATE TABLE IF NOT EXISTS entidades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo TEXT NOT NULL, -- pessoa, projeto, arquivo, repositorio, termo
    nome TEXT NOT NULL,
    nome_normalizado TEXT, -- lowercase, sem acentos, para matching
    aliases TEXT[], -- nomes alternativos
    metadata JSONB DEFAULT '{}',
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tipo, nome_normalizado)
);

CREATE INDEX IF NOT EXISTS idx_entidades_tipo ON entidades(tipo);
CREATE INDEX IF NOT EXISTS idx_entidades_nome ON entidades(nome_normalizado);

-- ============================================================
-- MEMORIA_ENTIDADE (link entre memórias e entidades)
-- ============================================================
CREATE TABLE IF NOT EXISTS memoria_entidade (
    memoria_id UUID REFERENCES memorias(id) ON DELETE CASCADE,
    entidade_id UUID REFERENCES entidades(id) ON DELETE CASCADE,
    relevancia FLOAT DEFAULT 1.0, -- quão relevante é essa entidade para a memória
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (memoria_id, entidade_id)
);

-- ============================================================
-- PROCESSAMENTO_MEMORIA (tracking de quais conversas já foram processadas)
-- ============================================================
CREATE TABLE IF NOT EXISTS processamento_memoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID REFERENCES conversas(id) ON DELETE CASCADE UNIQUE,
    processado_em TIMESTAMPTZ DEFAULT NOW(),
    memorias_extraidas INTEGER DEFAULT 0,
    status TEXT DEFAULT 'sucesso', -- sucesso, erro, pendente
    erro_msg TEXT,
    versao_processador TEXT DEFAULT 'v1' -- para reprocessar se mudar o prompt
);

CREATE INDEX IF NOT EXISTS idx_processamento_conversa ON processamento_memoria(conversa_id);
CREATE INDEX IF NOT EXISTS idx_processamento_status ON processamento_memoria(status);

-- ============================================================
-- RLS (Row Level Security)
-- ============================================================
ALTER TABLE memorias ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for memorias" ON memorias;
CREATE POLICY "Allow all for memorias" ON memorias FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE memoria_recuperacoes ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for memoria_recuperacoes" ON memoria_recuperacoes;
CREATE POLICY "Allow all for memoria_recuperacoes" ON memoria_recuperacoes FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE entidades ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for entidades" ON entidades;
CREATE POLICY "Allow all for entidades" ON entidades FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE memoria_entidade ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for memoria_entidade" ON memoria_entidade;
CREATE POLICY "Allow all for memoria_entidade" ON memoria_entidade FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE processamento_memoria ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for processamento_memoria" ON processamento_memoria;
CREATE POLICY "Allow all for processamento_memoria" ON processamento_memoria FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- VIEW: Resumo do Memory Lane
-- ============================================================
CREATE OR REPLACE VIEW resumo_memory_lane AS
SELECT
    (SELECT COUNT(*) FROM memorias WHERE ativo = TRUE) as total_memorias,
    (SELECT COUNT(*) FROM memorias WHERE tipo = 'decisao') as decisoes,
    (SELECT COUNT(*) FROM memorias WHERE tipo = 'insight') as insights,
    (SELECT COUNT(*) FROM memorias WHERE tipo = 'padrao') as padroes,
    (SELECT COUNT(*) FROM memorias WHERE tipo = 'aprendizado') as aprendizados,
    (SELECT COUNT(*) FROM memorias WHERE tipo = 'correcao') as correcoes,
    (SELECT COUNT(*) FROM memorias WHERE tipo = 'workflow') as workflows,
    (SELECT COUNT(*) FROM memorias WHERE tipo = 'gap') as gaps,
    (SELECT COUNT(*) FROM entidades) as total_entidades,
    (SELECT COUNT(*) FROM memoria_recuperacoes) as total_recuperacoes,
    (SELECT COUNT(*) FROM memoria_recuperacoes WHERE foi_util = TRUE) as recuperacoes_uteis,
    (SELECT COUNT(*) FROM processamento_memoria WHERE status = 'sucesso') as conversas_processadas;

-- ============================================================
-- FUNÇÃO: Busca semântica de memórias
-- ============================================================
CREATE OR REPLACE FUNCTION buscar_memorias_similares(
    query_embedding vector(768),
    limite INTEGER DEFAULT 5,
    threshold FLOAT DEFAULT 0.65
)
RETURNS TABLE (
    id UUID,
    tipo TEXT,
    titulo TEXT,
    resumo TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.id,
        m.tipo,
        m.titulo,
        m.resumo,
        1 - (m.embedding <=> query_embedding) as similarity
    FROM memorias m
    WHERE m.ativo = TRUE
        AND m.embedding IS NOT NULL
        AND 1 - (m.embedding <=> query_embedding) >= threshold
    ORDER BY m.embedding <=> query_embedding
    LIMIT limite;
END;
$$ LANGUAGE plpgsql;
