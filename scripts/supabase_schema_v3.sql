-- Schema AI Brain v3 - Sistema Completo de Conhecimento
-- Executar no Supabase SQL Editor

-- ============================================================
-- CONVERSAS (sessões de chat)
-- ============================================================
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS parent_session_id TEXT;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS is_subagent BOOLEAN DEFAULT FALSE;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS agent_id TEXT;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS objetivo TEXT;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS resultado TEXT; -- 'sucesso', 'falha', 'parcial', 'em_andamento'
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS tags TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS arquivos_criados TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS arquivos_modificados TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS comandos_executados TEXT[];
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS total_erros INTEGER DEFAULT 0;
ALTER TABLE conversas ADD COLUMN IF NOT EXISTS total_correcoes INTEGER DEFAULT 0;

-- Indice para buscar subagentes
CREATE INDEX IF NOT EXISTS idx_conversas_parent ON conversas(parent_session_id);
CREATE INDEX IF NOT EXISTS idx_conversas_is_subagent ON conversas(is_subagent);
CREATE INDEX IF NOT EXISTS idx_conversas_tags ON conversas USING GIN(tags);

-- ============================================================
-- MENSAGENS (já existe, adicionar campos)
-- ============================================================
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS is_error BOOLEAN DEFAULT FALSE;
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS is_correction BOOLEAN DEFAULT FALSE;
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS intent TEXT; -- 'pergunta', 'comando', 'correcao', 'confirmacao'
ALTER TABLE mensagens ADD COLUMN IF NOT EXISTS tokens_estimado INTEGER;

CREATE INDEX IF NOT EXISTS idx_mensagens_is_error ON mensagens(is_error) WHERE is_error = TRUE;
CREATE INDEX IF NOT EXISTS idx_mensagens_is_correction ON mensagens(is_correction) WHERE is_correction = TRUE;

-- ============================================================
-- APRENDIZADOS (já existe, garantir estrutura)
-- ============================================================
-- Tipos: 'erro', 'correcao', 'decisao', 'padrao', 'insight', 'preferencia', 'sop'
ALTER TABLE aprendizados ADD COLUMN IF NOT EXISTS fonte_conversa_id UUID REFERENCES conversas(id);
ALTER TABLE aprendizados ADD COLUMN IF NOT EXISTS aplicavel_a TEXT[]; -- repos, projetos onde se aplica
ALTER TABLE aprendizados ADD COLUMN IF NOT EXISTS vezes_aplicado INTEGER DEFAULT 0;
ALTER TABLE aprendizados ADD COLUMN IF NOT EXISTS ultima_aplicacao TIMESTAMPTZ;

-- ============================================================
-- WORKFLOWS (sequências de ações repetidas)
-- ============================================================
CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    descricao TEXT,
    passos JSONB NOT NULL, -- array de {acao, tool, parametros}
    trigger_pattern TEXT, -- regex para detectar quando usar
    vezes_executado INTEGER DEFAULT 0,
    ultima_execucao TIMESTAMPTZ,
    conversas_origem UUID[], -- de quais conversas foi extraído
    tags TEXT[],
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workflows_tags ON workflows USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_workflows_ativo ON workflows(ativo);

-- RLS para workflows
ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for workflows" ON workflows;
CREATE POLICY "Allow all for workflows" ON workflows FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- SOPS (Procedimentos Operacionais Padrão)
-- ============================================================
CREATE TABLE IF NOT EXISTS sops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo TEXT NOT NULL,
    categoria TEXT, -- 'git', 'deploy', 'debug', 'setup', etc
    problema TEXT, -- qual problema resolve
    solucao TEXT NOT NULL, -- passos em markdown
    comandos TEXT[], -- comandos específicos usados
    arquivos_relacionados TEXT[],
    extraido_de UUID[], -- conversas de origem
    vezes_referenciado INTEGER DEFAULT 0,
    tags TEXT[],
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sops_categoria ON sops(categoria);
CREATE INDEX IF NOT EXISTS idx_sops_tags ON sops USING GIN(tags);

-- RLS para sops
ALTER TABLE sops ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for sops" ON sops;
CREATE POLICY "Allow all for sops" ON sops FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- ERROS (padrões de erros encontrados)
-- ============================================================
CREATE TABLE IF NOT EXISTS erros (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo TEXT NOT NULL, -- 'sintaxe', 'runtime', 'logica', 'config', etc
    mensagem_erro TEXT NOT NULL,
    contexto TEXT, -- onde/quando acontece
    solucao TEXT, -- como resolver
    arquivo_pattern TEXT, -- em quais arquivos costuma ocorrer
    ocorrencias INTEGER DEFAULT 1,
    conversas_origem UUID[],
    tags TEXT[],
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_erros_tipo ON erros(tipo);
CREATE INDEX IF NOT EXISTS idx_erros_tags ON erros USING GIN(tags);

-- RLS para erros
ALTER TABLE erros ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for erros" ON erros;
CREATE POLICY "Allow all for erros" ON erros FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- DECISOES (decisões tomadas em conversas)
-- ============================================================
CREATE TABLE IF NOT EXISTS decisoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID REFERENCES conversas(id),
    contexto TEXT NOT NULL, -- situação
    opcoes_consideradas JSONB, -- [{opcao, pros, cons}]
    decisao_tomada TEXT NOT NULL,
    razao TEXT, -- por que essa decisão
    resultado TEXT, -- como foi o resultado
    tags TEXT[],
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_decisoes_conversa ON decisoes(conversa_id);
CREATE INDEX IF NOT EXISTS idx_decisoes_tags ON decisoes USING GIN(tags);

-- RLS para decisoes
ALTER TABLE decisoes ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for decisoes" ON decisoes;
CREATE POLICY "Allow all for decisoes" ON decisoes FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- PREFERENCIAS (preferências do usuário aprendidas)
-- ============================================================
CREATE TABLE IF NOT EXISTS preferencias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    categoria TEXT NOT NULL, -- 'codigo', 'comunicacao', 'ferramentas', etc
    preferencia TEXT NOT NULL,
    contexto TEXT, -- quando se aplica
    fonte_conversas UUID[],
    confianca FLOAT DEFAULT 0.5, -- 0-1, quão certo estamos
    vezes_confirmado INTEGER DEFAULT 1,
    ultima_confirmacao TIMESTAMPTZ,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_preferencias_categoria ON preferencias(categoria);
CREATE INDEX IF NOT EXISTS idx_preferencias_ativo ON preferencias(ativo);

-- RLS para preferencias
ALTER TABLE preferencias ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for preferencias" ON preferencias;
CREATE POLICY "Allow all for preferencias" ON preferencias FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- VIEW: Conversas com subagentes
-- ============================================================
CREATE OR REPLACE VIEW conversas_completas AS
SELECT
    c.*,
    (SELECT COUNT(*) FROM conversas sub WHERE sub.parent_session_id = c.session_id) as total_subagentes,
    (SELECT array_agg(sub.session_id) FROM conversas sub WHERE sub.parent_session_id = c.session_id) as subagentes_ids
FROM conversas c
WHERE c.is_subagent = FALSE;

-- ============================================================
-- VIEW: Resumo de conhecimento
-- ============================================================
CREATE OR REPLACE VIEW resumo_conhecimento AS
SELECT
    (SELECT COUNT(*) FROM conversas) as total_conversas,
    (SELECT COUNT(*) FROM conversas WHERE is_subagent = FALSE) as conversas_principais,
    (SELECT COUNT(*) FROM conversas WHERE is_subagent = TRUE) as subagentes,
    (SELECT COUNT(*) FROM mensagens) as total_mensagens,
    (SELECT COUNT(*) FROM conversas WHERE teve_erros = TRUE) as conversas_com_erros,
    (SELECT COUNT(*) FROM conversas WHERE teve_correcoes = TRUE) as conversas_com_correcoes,
    (SELECT COUNT(*) FROM aprendizados) as total_aprendizados,
    (SELECT COUNT(*) FROM workflows) as total_workflows,
    (SELECT COUNT(*) FROM sops) as total_sops,
    (SELECT COUNT(*) FROM erros) as padroes_erro,
    (SELECT COUNT(*) FROM decisoes) as total_decisoes,
    (SELECT COUNT(*) FROM preferencias WHERE ativo = TRUE) as preferencias_ativas;
