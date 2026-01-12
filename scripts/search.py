#!/usr/bin/env python3
"""
Busca semântica unificada em memórias e sources.
Parte do Memory Lane System - Fase 3.4.

Uso:
    python3 scripts/search.py "como implementar agentes ia"
    python3 scripts/search.py "ideias do nate" --autor nate
    python3 scripts/search.py "decisões importantes" --memories-only
    python3 scripts/search.py "building agents" --sources-only --limit 20
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

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
        print("Inicie com: sudo systemctl start ollama", file=sys.stderr)
        sys.exit(1)


def supabase_rpc(function_name: str, params: dict) -> list:
    """Chama função RPC do Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/rpc/{function_name}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(params).encode(),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        if "function" in error_body.lower() and "does not exist" in error_body.lower():
            print(f"\nErro: Função RPC '{function_name}' não existe no Supabase.", file=sys.stderr)
            print("Execute o SQL em projects/ai-brain/SETUP.md para criar as funções.", file=sys.stderr)
            sys.exit(1)
        raise


def search_sources(embedding: list[float], limit: int = 5, autor: str = None) -> list:
    """Busca em source_chunks via RPC."""
    params = {
        "query_embedding": embedding,
        "match_count": limit
    }
    if autor:
        params["filter_autor"] = autor

    return supabase_rpc("search_sources", params)


def search_memories(embedding: list[float], limit: int = 5) -> list:
    """Busca em memorias via RPC."""
    params = {
        "query_embedding": embedding,
        "match_count": limit
    }
    return supabase_rpc("search_memories", params)


def format_memory(mem: dict) -> str:
    """Formata resultado de memória para exibição."""
    sim = mem.get("similarity", 0)
    tipo = mem.get("tipo", "?")
    titulo = mem.get("titulo", "")
    resumo = mem.get("resumo", "")

    # Truncar resumo se muito longo
    if len(resumo) > 200:
        resumo = resumo[:200] + "..."

    lines = [f"[{sim:.2f}] {tipo}: {titulo}"]
    if resumo:
        lines.append(f"       {resumo}")

    return "\n".join(lines)


def format_source(src: dict) -> str:
    """Formata resultado de source para exibição."""
    sim = src.get("similarity", 0)
    autor = src.get("autor", "?")
    source_file = src.get("source_file", "")
    chunk_index = src.get("chunk_index", 0)
    content = src.get("content", "")

    # Pegar primeira frase ou primeiros 150 chars
    preview = content[:150].replace("\n", " ")
    if len(content) > 150:
        preview += "..."

    lines = [f"[{sim:.2f}] {autor} | {source_file} (chunk {chunk_index})"]
    lines.append(f"       \"{preview}\"")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Busca semântica em memórias e sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scripts/search.py "como implementar agentes ia"
  python3 scripts/search.py "ideias do nate" --autor nate
  python3 scripts/search.py "decisões importantes" --memories-only
        """
    )
    parser.add_argument('query', help='Texto para buscar')
    parser.add_argument('--autor', '-a', help='Filtrar sources por autor')
    parser.add_argument('--limit', '-l', type=int, default=5, help='Resultados por tipo (default: 5)')
    parser.add_argument('--sources-only', '-s', action='store_true', help='Buscar apenas em sources')
    parser.add_argument('--memories-only', '-m', action='store_true', help='Buscar apenas em memórias')

    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados", file=sys.stderr)
        sys.exit(1)

    # Gerar embedding da query
    print(f"Buscando: \"{args.query}\"\n")
    embedding = get_embedding(args.query)

    if not embedding:
        print("Erro: não foi possível gerar embedding", file=sys.stderr)
        sys.exit(1)

    # Buscar memórias
    if not args.sources_only:
        try:
            memories = search_memories(embedding, limit=args.limit)
            print(f"=== MEMÓRIAS ({len(memories)} resultados) ===\n")
            if memories:
                for mem in memories:
                    print(format_memory(mem))
                    print()
            else:
                print("Nenhuma memória encontrada.\n")
        except Exception as e:
            print(f"Erro buscando memórias: {e}\n", file=sys.stderr)

    # Buscar sources
    if not args.memories_only:
        try:
            sources = search_sources(embedding, limit=args.limit, autor=args.autor)
            autor_info = f" (autor: {args.autor})" if args.autor else ""
            print(f"=== SOURCES ({len(sources)} resultados){autor_info} ===\n")
            if sources:
                for src in sources:
                    print(format_source(src))
                    print()
            else:
                print("Nenhum source encontrado.\n")
        except Exception as e:
            print(f"Erro buscando sources: {e}\n", file=sys.stderr)


if __name__ == "__main__":
    main()
