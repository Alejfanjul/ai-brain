-- Schema para source_chunks (Fase 2.5 do Memory Lane)
-- Rodar no Supabase Dashboard > SQL Editor

-- Tabela para chunks dos sources (transcripts, artigos)
CREATE TABLE IF NOT EXISTS source_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file TEXT NOT NULL,           -- nome do arquivo (ex: "2025-12-13-alex-hillman-jfdi...")
    autor TEXT,                          -- autor extraído (ex: "alex-hillman")
    data_source DATE,                    -- data extraída do nome do arquivo
    chunk_index INTEGER NOT NULL,        -- posição do chunk no arquivo (0, 1, 2...)
    content TEXT NOT NULL,               -- texto do chunk
    embedding VECTOR(768),               -- embedding via Ollama nomic-embed-text
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Evitar duplicatas
    UNIQUE(source_file, chunk_index)
);

-- Índice para busca vetorial (cosine similarity)
CREATE INDEX IF NOT EXISTS idx_source_chunks_embedding
    ON source_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Índice para filtrar por autor
CREATE INDEX IF NOT EXISTS idx_source_chunks_autor
    ON source_chunks (autor);

-- Índice para filtrar por arquivo
CREATE INDEX IF NOT EXISTS idx_source_chunks_file
    ON source_chunks (source_file);

-- Comentários
COMMENT ON TABLE source_chunks IS 'Chunks dos arquivos em sources/ com embeddings para busca semântica';
COMMENT ON COLUMN source_chunks.embedding IS 'Vetor 768-dim gerado via Ollama nomic-embed-text';
