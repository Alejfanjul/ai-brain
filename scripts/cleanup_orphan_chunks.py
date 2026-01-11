#!/usr/bin/env python3
"""
Remove chunks órfãos do Supabase (arquivos que não existem mais em sources/).
Parte do Memory Lane System.

Uso:
    python3 scripts/cleanup_orphan_chunks.py              # Mostra órfãos (dry-run)
    python3 scripts/cleanup_orphan_chunks.py --delete     # Remove órfãos do Supabase
    python3 scripts/cleanup_orphan_chunks.py --file X.md  # Remove chunks de arquivo específico
"""

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
SOURCES_DIR = Path.home() / "ai-brain" / "sources"


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


def get_unique_source_files() -> dict[str, int]:
    """Retorna dicionário {source_file: count} do Supabase."""
    try:
        # Buscar todos os source_file únicos com contagem
        result = supabase_request("source_chunks?select=source_file&limit=10000")

        # Contar chunks por arquivo
        counts = {}
        for r in result:
            sf = r["source_file"]
            counts[sf] = counts.get(sf, 0) + 1

        return counts
    except Exception as e:
        print(f"Erro ao buscar source_files: {e}", file=sys.stderr)
        return {}


def delete_chunks_by_file(source_file: str) -> int:
    """Deleta todos os chunks de um arquivo específico. Retorna quantidade deletada."""
    try:
        # Primeiro contar quantos vamos deletar
        count_result = supabase_request(f"source_chunks?source_file=eq.{source_file}&select=id")
        count = len(count_result)

        if count == 0:
            return 0

        # Deletar usando DELETE com filtro
        url = f"{SUPABASE_URL}/rest/v1/source_chunks?source_file=eq.{source_file}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        req = urllib.request.Request(url, headers=headers, method="DELETE")
        with urllib.request.urlopen(req, timeout=30) as response:
            pass

        return count
    except Exception as e:
        print(f"Erro ao deletar chunks de {source_file}: {e}", file=sys.stderr)
        return 0


def find_orphans() -> list[tuple[str, int]]:
    """Encontra arquivos no Supabase que não existem mais em sources/."""
    # Listar arquivos locais
    local_files = set(f.name for f in SOURCES_DIR.glob("*.md"))

    # Listar arquivos no Supabase
    supabase_files = get_unique_source_files()

    # Encontrar órfãos
    orphans = []
    for source_file, count in supabase_files.items():
        if source_file not in local_files:
            orphans.append((source_file, count))

    return sorted(orphans)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Remove chunks órfãos do Supabase')
    parser.add_argument('--delete', action='store_true',
                        help='Efetivamente deleta os chunks órfãos (sem isso, apenas lista)')
    parser.add_argument('--file', type=str,
                        help='Deleta chunks de um arquivo específico (ex: arquivo.md)')
    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados", file=sys.stderr)
        sys.exit(1)

    # Modo: deletar arquivo específico
    if args.file:
        print(f"Deletando chunks de: {args.file}")
        deleted = delete_chunks_by_file(args.file)
        print(f"✓ {deleted} chunks deletados")
        return

    # Modo: encontrar e listar/deletar órfãos
    print("Buscando chunks no Supabase...")
    supabase_files = get_unique_source_files()
    print(f"Arquivos no Supabase: {len(supabase_files)}")

    print(f"\nBuscando arquivos locais em {SOURCES_DIR}...")
    local_files = set(f.name for f in SOURCES_DIR.glob("*.md"))
    print(f"Arquivos locais: {len(local_files)}")

    print("\nProcurando órfãos...")
    orphans = find_orphans()

    if not orphans:
        print("\n✓ Nenhum chunk órfão encontrado!")
        return

    print(f"\n⚠️  Encontrados {len(orphans)} arquivos órfãos:\n")

    total_chunks = 0
    for source_file, count in orphans:
        print(f"  {source_file} ({count} chunks)")
        total_chunks += count

    print(f"\n  Total: {total_chunks} chunks órfãos")

    if args.delete:
        print("\nDeletando chunks órfãos...")
        deleted_total = 0
        for source_file, count in orphans:
            deleted = delete_chunks_by_file(source_file)
            deleted_total += deleted
            print(f"  ✓ {source_file}: {deleted} chunks deletados")

        print(f"\n✓ Total deletado: {deleted_total} chunks")
    else:
        print("\n💡 Execute com --delete para remover os chunks órfãos")


if __name__ == "__main__":
    main()
