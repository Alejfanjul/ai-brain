-- ==================================================
-- SUPABASE AI BRAIN - SCHEMA EXTRACTION
-- Data: 2026-01-06 09:34:53
-- Projeto: czaknnzcqwvsdflrtjtq
-- ==================================================

-- NOTA: Schema inferido a partir dos dados existentes.
-- Tipos podem não ser 100% precisos.
-- Para schema exato, use pg_dump ou Supabase Dashboard.

-- RESUMO:
-- Tabelas encontradas: 8
-- Tabelas não encontradas: 5
-- Missing: workflows, sops, erros, decisoes, preferencias

-- CONTAGEM DE REGISTROS:
-- conversas: 10+ registros
-- mensagens: 10+ registros
-- memorias: 10+ registros
-- memoria_recuperacoes: 0+ registros
-- entidades: 0+ registros
-- memoria_entidade: 0+ registros
-- processamento_memoria: 10+ registros
-- aprendizados: 0+ registros


-- ==================================================
-- Table: conversas
-- Colunas detectadas: 25
-- Registros analisados: 10
-- ==================================================

CREATE TABLE conversas (
    id UUID NOT NULL,  -- ex: 'e7e2a91e-e05f-4340-83b3-da951bd6e2b5', 'f520bc7b-4da4-4d10-aef2-a3ed7e244bdb'
    session_id TEXT, UUID NOT NULL,  -- ex: '24034e49-b6c2-4125-aa26-5fe21b958bed', 'agent-a9467ec'
    repositorio TEXT NOT NULL,  -- ex: 'sistema-os', 'ai-brain'
    cwd TEXT NOT NULL,  -- ex: '/home/marketing/sistema-os', '/home/marketing/ai-brain'
    resumo TEXT,  -- ex: '# Prompt para Claude Code: Organizar Arquivos do M', 'Explore o codebase para encontrar todos os arquivo'
    total_mensagens INTEGER NOT NULL,  -- ex: '63', '46'
    arquivos_tocados JSONB/ARRAY NOT NULL,  -- ex: '[]', '['/home/marketing/ai-brain/sources/2025-12-21-alex'
    ferramentas_usadas JSONB/ARRAY NOT NULL,  -- ex: '['TodoWrite', 'Bash']', '['Grep', 'Glob', 'Bash', 'Read']'
    teve_erros BOOLEAN NOT NULL,  -- ex: 'False', 'True'
    teve_correcoes BOOLEAN NOT NULL,  -- ex: 'False', 'True'
    iniciado_em TIMESTAMPTZ NOT NULL,  -- ex: '2025-12-30T17:40:54.992+00:00', '2026-01-05T18:45:14.741+00:00'
    finalizado_em TIMESTAMPTZ NOT NULL,  -- ex: '2025-12-30T17:43:39.548+00:00', '2026-01-05T18:45:58.794+00:00'
    criado_em TIMESTAMPTZ NOT NULL,  -- ex: '2026-01-05T17:13:13.681055+00:00', '2026-01-05T18:50:09.555843+00:00'
    atualizado_em TIMESTAMPTZ NOT NULL,  -- ex: '2026-01-05T17:13:10.723044+00:00', '2026-01-05T18:50:08.816705+00:00'
    parent_session_id UUID,  -- ex: 'd35bee32-b240-458f-aed9-93f41b45134a', 'e89bec47-8942-4355-b1a6-ee60e2a28d6d'
    is_subagent BOOLEAN NOT NULL,  -- ex: 'False', 'True'
    agent_id TEXT,  -- ex: 'a9467ec', 'a7bd052'
    objetivo TEXT,  -- ex: '# Prompt para Claude Code: Organizar Arquivos do M', 'Explore o codebase para encontrar todos os arquivo'
    resultado TEXT NOT NULL,  -- ex: 'sucesso', 'em_andamento'
    tags JSONB/ARRAY NOT NULL,  -- ex: '['testes', 'git', 'setup']', '['codigo', 'dados', 'documentacao']'
    arquivos_criados JSONB/ARRAY NOT NULL,  -- ex: '[]', '['/home/marketing/.claude/plans/harmonic-knitting-'
    arquivos_modificados JSONB/ARRAY NOT NULL,  -- ex: '[]', '['/home/marketing/ai-brain/projects/ai-brain/ai_br'
    comandos_executados JSONB/ARRAY NOT NULL,  -- ex: '['git branch --show-current', 'mkdir -p docs/RM/PR', '['find /home/marketing/ai-brain -type f -name "*.p'
    total_erros INTEGER NOT NULL,  -- ex: '0', '1'
    total_correcoes INTEGER NOT NULL  -- ex: '0', '1'
);

-- ==================================================
-- Table: mensagens
-- Colunas detectadas: 16
-- Registros analisados: 10
-- ==================================================

CREATE TABLE mensagens (
    id UUID NOT NULL,  -- ex: '5a315ad7-8024-4a26-912e-d35b65f719b2', '832d5ef9-dc1c-42e3-926e-75b907fe80f1'
    conversa_id UUID NOT NULL,  -- ex: 'e7e2a91e-e05f-4340-83b3-da951bd6e2b5', '0446daf6-3335-4eec-9af1-06a9ec35eac6'
    uuid_original UUID NOT NULL,  -- ex: 'f04f9e2d-eceb-4883-a7ef-073af5cd22a0', 'e9a25f4b-9d25-4c2d-89b4-0dc424f88e11'
    tipo TEXT NOT NULL,  -- ex: 'user', 'assistant'
    conteudo TEXT NOT NULL,  -- ex: '# Prompt para Claude Code: Organizar Arquivos do M', ''
    conteudo_json JSONB/ARRAY,  -- ex: '[{'type': 'thinking', 'thinking': 'O usuário quer ', '[{'text': 'Vou organizar os arquivos do módulo RM '
    ferramentas_usadas JSONB/ARRAY,  -- ex: '['TodoWrite']', '['Bash']'
    arquivos_mencionados UNKNOWN,
    tem_erro BOOLEAN NOT NULL,  -- ex: 'False'
    tem_correcao BOOLEAN NOT NULL,  -- ex: 'False'
    timestamp_original TIMESTAMPTZ NOT NULL,  -- ex: '2025-12-30T17:40:54.992+00:00', '2025-12-30T17:40:59.396+00:00'
    criado_em TIMESTAMPTZ NOT NULL,  -- ex: '2026-01-05T17:13:13.821784+00:00', '2026-01-05T18:20:08.529019+00:00'
    is_error BOOLEAN NOT NULL,  -- ex: 'False'
    is_correction BOOLEAN NOT NULL,  -- ex: 'False'
    intent TEXT,  -- ex: 'comando'
    tokens_estimado INTEGER NOT NULL  -- ex: '887', '0'
);

-- ==================================================
-- Table: memorias
-- Colunas detectadas: 19
-- Registros analisados: 10
-- ==================================================

CREATE TABLE memorias (
    id UUID NOT NULL,  -- ex: '6a305f54-16a8-4788-a2a5-cf9ee9f665ed', 'dda91507-45bc-4dc8-9e68-c0c99b359371'
    conversa_id UUID NOT NULL,  -- ex: '0446daf6-3335-4eec-9af1-06a9ec35eac6', '56185b66-8d22-4dc4-bc13-29e1984d9e29'
    mensagem_id UNKNOWN,
    tipo TEXT NOT NULL,  -- ex: 'decisao', 'insight'
    titulo TEXT NOT NULL,  -- ex: 'Claude SDK vs API: Migração para CLI', 'Persistência como primeira vitória do projeto'
    resumo TEXT NOT NULL,  -- ex: 'Decisão de mudar da API direta para Claude Code CL', 'Começar salvando conversas e audit trail como prim'
    reasoning TEXT NOT NULL,  -- ex: 'Permite captura automática de conversas, reduz com', 'Permite capturar conhecimento imediatamente e cria'
    contexto_original TEXT NOT NULL,  -- ex: 'Estava vendo que o Hillman usa a Claude SDK - e nã', 'O que eu imagino para a primeira vitória deste pro'
    confidence_score FLOAT NOT NULL,  -- ex: '0.9', '0.85'
    surprise_score FLOAT NOT NULL,  -- ex: '0.7', '0.6'
    feedback_score INTEGER NOT NULL,  -- ex: '0'
    entidades_relacionadas JSONB/ARRAY NOT NULL,  -- ex: '[{'name': 'ai_brain_parceiro_digital', 'type': 'pr', '[{'name': '/login', 'type': 'comando'}, {'name': ''
    arquivos_relacionados UNKNOWN,
    embedding UNKNOWN,
    formada_em TIMESTAMPTZ NOT NULL,  -- ex: '2026-01-05T13:54:48+00:00', '2026-01-05T12:40:47+00:00'
    salva_em TIMESTAMPTZ NOT NULL,  -- ex: '2026-01-05T18:04:34.979186+00:00', '2026-01-05T18:04:35.169701+00:00'
    ultima_recuperacao UNKNOWN,
    vezes_recuperada INTEGER NOT NULL,  -- ex: '0'
    ativo BOOLEAN NOT NULL  -- ex: 'True'
);

-- ==================================================
-- Table: memoria_recuperacoes
-- Colunas detectadas: 0
-- Registros analisados: 0
-- ==================================================

CREATE TABLE memoria_recuperacoes (
);

-- ==================================================
-- Table: entidades
-- Colunas detectadas: 0
-- Registros analisados: 0
-- ==================================================

CREATE TABLE entidades (
);

-- ==================================================
-- Table: memoria_entidade
-- Colunas detectadas: 0
-- Registros analisados: 0
-- ==================================================

CREATE TABLE memoria_entidade (
);

-- ==================================================
-- Table: processamento_memoria
-- Colunas detectadas: 7
-- Registros analisados: 10
-- ==================================================

CREATE TABLE processamento_memoria (
    id UUID NOT NULL,  -- ex: '08a2fe9f-d829-43c8-805d-9296163b6d8a', 'fd13b73e-dfaa-4f3c-acd2-c8d23e271921'
    conversa_id UUID NOT NULL,  -- ex: 'f53537bf-6bb4-45b0-b6d2-4f4bc5e5c94d', '8dc73dde-aab4-4bd2-b312-e4b898fee166'
    processado_em TIMESTAMPTZ NOT NULL,  -- ex: '2026-01-05T18:05:15.647528+00:00', '2026-01-05T18:05:27.290356+00:00'
    memorias_extraidas INTEGER NOT NULL,  -- ex: '4', '3'
    status TEXT NOT NULL,  -- ex: 'sucesso'
    erro_msg UNKNOWN,
    versao_processador TEXT NOT NULL  -- ex: 'v1'
);

-- ==================================================
-- Table: aprendizados
-- Colunas detectadas: 0
-- Registros analisados: 0
-- ==================================================

CREATE TABLE aprendizados (
);

-- ==================================================
-- FIM DO SCHEMA
-- Gerado em: 2026-01-06 09:34:53
-- ==================================================