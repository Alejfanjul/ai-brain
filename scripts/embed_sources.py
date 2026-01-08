#!/usr/bin/env python3
"""
Gera embeddings para arquivos em sources/ usando Ollama.
Parte do Memory Lane System - Fase 2.5.

Uso:
    python3 scripts/embed_sources.py              # Processa todos os arquivos novos
    python3 scripts/embed_sources.py --force      # Reprocessa tudo
    python3 scripts/embed_sources.py --dry-run    # Mostra o que faria sem executar
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# Configurações de chunking
CHUNK_SIZE_WORDS = 600      # ~600 palavras por chunk
OVERLAP_PERCENT = 0.15      # 15% de overlap
OVERLAP_WORDS = int(CHUNK_SIZE_WORDS * OVERLAP_PERCENT)

# Carregar .env
env_file = Path.home() / "ai-brain" / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"
EMBEDDING_DIM = 768

SOURCES_DIR = Path.home() / "ai-brain" / "sources"

# Palavras que indicam início do título (para separar autor)
TITLE_MARKERS = [
    'the', 'how', 'why', 'my', 'your', 'a', 'an', 'i', 'we', 'what',
    'from', 'to', 'new', 'vale', 'voce', 'using', 'making', 'building',
    'lesson', 'networks', 'correctness', 'memory', 'super', 'just'
]


def supabase_request(endpoint: str, method: str = "GET", data: dict = None):
    """Faz request para Supabase REST API."""
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    req_data = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        raise


def get_embedding(text: str) -> list[float]:
    """Gera embedding via Ollama API."""
    data = {
        "model": OLLAMA_MODEL,
        "prompt": text
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
            return result.get("embedding", [])
    except urllib.error.URLError as e:
        print(f"Erro conectando ao Ollama: {e}", file=sys.stderr)
        raise


def check_ollama_available() -> bool:
    """Verifica se Ollama está disponível."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode())
            models = [m["name"] for m in result.get("models", [])]
            return any(OLLAMA_MODEL in m for m in models)
    except Exception:
        return False


def extract_metadata(filename: str) -> tuple[str, str]:
    """
    Extrai data e autor do nome do arquivo.
    Formato esperado: YYYY-MM-DD-autor-titulo.md

    Returns:
        (data_str, autor) - ex: ("2025-12-13", "alex-hillman")
    """
    # Remove extensão
    name = filename.replace('.md', '')

    # Extrai data (primeiros 10 caracteres: YYYY-MM-DD)
    date_match = re.match(r'^(\d{4}-\d{2}-\d{2})-(.+)$', name)
    if not date_match:
        return None, None

    data_str = date_match.group(1)
    resto = date_match.group(2)

    # Encontra onde começa o título (primeira palavra marcadora)
    words = resto.split('-')
    autor_parts = []

    for i, word in enumerate(words):
        word_lower = word.lower()
        if word_lower in TITLE_MARKERS:
            break
        # Se for número (ex: "1", "2" em "lesson-1"), é parte do título
        if word.isdigit():
            break
        autor_parts.append(word)

    autor = '-'.join(autor_parts) if autor_parts else None

    return data_str, autor


def chunk_text(text: str) -> list[str]:
    """
    Divide texto em chunks de ~600 palavras com 15% overlap.

    Returns:
        Lista de chunks
    """
    words = text.split()

    if len(words) <= CHUNK_SIZE_WORDS:
        return [text]

    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE_WORDS
        chunk_words = words[start:end]
        chunks.append(' '.join(chunk_words))

        # Próximo chunk começa com overlap
        start = end - OVERLAP_WORDS

        # Evitar loop infinito
        if start >= len(words) - OVERLAP_WORDS:
            break

    return chunks


def get_processed_chunks() -> set[tuple[str, int]]:
    """Retorna set de (source_file, chunk_index) já processados."""
    try:
        result = supabase_request("source_chunks?select=source_file,chunk_index&limit=10000")
        return set((r["source_file"], r["chunk_index"]) for r in result)
    except Exception as e:
        print(f"Aviso: não foi possível verificar chunks existentes: {e}", file=sys.stderr)
        return set()


def insert_chunk(source_file: str, autor: str, data_source: str,
                 chunk_index: int, content: str, embedding: list[float]) -> bool:
    """Insere chunk no Supabase."""
    embedding_str = f"[{','.join(str(x) for x in embedding)}]"

    data = {
        "source_file": source_file,
        "autor": autor,
        "data_source": data_source,
        "chunk_index": chunk_index,
        "content": content,
        "embedding": embedding_str
    }

    try:
        supabase_request("source_chunks", method="POST", data=data)
        return True
    except Exception as e:
        print(f"Erro inserindo chunk: {e}", file=sys.stderr)
        return False


def process_file(filepath: Path, processed_chunks: set, dry_run: bool = False) -> tuple[int, int, int]:
    """
    Processa um arquivo: extrai metadados, divide em chunks, gera embeddings.

    Returns:
        (chunks_success, chunks_skipped, chunks_error)
    """
    filename = filepath.name
    data_str, autor = extract_metadata(filename)

    # Ler conteúdo
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Erro lendo arquivo: {e}")
        return 0, 0, 1

    # Dividir em chunks
    chunks = chunk_text(content)

    if dry_run:
        print(f"  {len(chunks)} chunks | autor: {autor} | data: {data_str}")
        return len(chunks), 0, 0

    success = 0
    skipped = 0
    errors = 0

    for i, chunk_content in enumerate(chunks):
        # Verificar se já foi processado
        if (filename, i) in processed_chunks:
            skipped += 1
            continue

        try:
            # Gerar embedding
            embedding = get_embedding(chunk_content)

            if not embedding:
                print(f"  Chunk {i}: embedding vazio")
                errors += 1
                continue

            # Inserir no Supabase
            if insert_chunk(filename, autor, data_str, i, chunk_content, embedding):
                success += 1
            else:
                errors += 1

        except Exception as e:
            print(f"  Chunk {i}: erro - {e}")
            errors += 1

    return success, skipped, errors


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Gera embeddings para arquivos em sources/')
    parser.add_argument('--force', action='store_true', help='Reprocessa todos os arquivos (ignora cache)')
    parser.add_argument('--dry-run', action='store_true', help='Mostra o que faria sem executar')
    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run and not check_ollama_available():
        print("Ollama não disponível. Inicie com: sudo systemctl start ollama", file=sys.stderr)
        sys.exit(1)

    # Listar arquivos .md em sources/
    if not SOURCES_DIR.exists():
        print(f"Diretório não encontrado: {SOURCES_DIR}", file=sys.stderr)
        sys.exit(1)

    all_files = sorted(SOURCES_DIR.glob("*.md"))
    print(f"Encontrados {len(all_files)} arquivos em sources/\n")

    # Verificar quais chunks já foram processados
    if args.force:
        processed_chunks = set()
        print("Modo --force: ignorando cache de chunks processados\n")
    else:
        processed_chunks = get_processed_chunks()
        print(f"Chunks já processados: {len(processed_chunks)}\n")

    if args.dry_run:
        print("=== DRY RUN (sem executar) ===\n")
        processed_chunks = set()  # Mostra todos no dry-run

    total_success = 0
    total_skipped = 0
    total_errors = 0

    for i, filepath in enumerate(all_files, 1):
        print(f"[{i}/{len(all_files)}] {filepath.name[:60]}...")

        success, skipped, errors = process_file(filepath, processed_chunks, dry_run=args.dry_run)
        total_success += success
        total_skipped += skipped
        total_errors += errors

        if not args.dry_run and (success > 0 or errors > 0):
            print(f"  {success} novos, {skipped} já existiam, {errors} erros")

    print(f"\n{'='*50}")
    print(f"Total: {total_success} novos, {total_skipped} já existiam, {total_errors} erros")


if __name__ == "__main__":
    main()
