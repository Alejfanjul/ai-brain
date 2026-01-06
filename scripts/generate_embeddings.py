#!/usr/bin/env python3
"""
Gera embeddings para memórias usando Ollama (nomic-embed-text).
Parte do Memory Lane System - Fase 2.
Roda após extract_memories.py ou sob demanda.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

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
            embedding = result.get("embedding", [])

            if len(embedding) != EMBEDDING_DIM:
                print(f"  Aviso: embedding tem {len(embedding)} dims (esperado {EMBEDDING_DIM})", file=sys.stderr)

            return embedding
    except urllib.error.URLError as e:
        print(f"Erro conectando ao Ollama: {e}", file=sys.stderr)
        print("Certifique-se que o Ollama está rodando: ollama serve", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Erro gerando embedding: {e}", file=sys.stderr)
        raise


def get_memories_without_embedding(limit: int = 50) -> list:
    """Busca memórias que ainda não têm embedding."""
    query = (
        f"memorias?select=id,titulo,resumo,contexto_original"
        f"&embedding=is.null"
        f"&ativo=eq.true"
        f"&order=salva_em.desc"
        f"&limit={limit}"
    )
    return supabase_request(query)


def format_memory_text(memory: dict) -> str:
    """Formata texto da memória para embedding."""
    parts = []

    if memory.get("titulo"):
        parts.append(memory["titulo"])

    if memory.get("resumo"):
        parts.append(memory["resumo"])

    # Contexto original é mais detalhado, incluir parcialmente
    if memory.get("contexto_original"):
        contexto = memory["contexto_original"][:500]  # Limitar tamanho
        parts.append(contexto)

    return " | ".join(parts)


def update_memory_embedding(memory_id: str, embedding: list[float]) -> bool:
    """Atualiza embedding de uma memória no Supabase."""
    # pgvector espera formato de array PostgreSQL
    embedding_str = f"[{','.join(str(x) for x in embedding)}]"

    try:
        # PATCH para atualizar
        url = f"{SUPABASE_URL}/rest/v1/memorias?id=eq.{memory_id}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        data = json.dumps({"embedding": embedding_str}).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")

        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status in (200, 204)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"Erro atualizando embedding: {e.code} - {error_body}", file=sys.stderr)
        return False


def check_ollama_available() -> bool:
    """Verifica se Ollama está disponível."""
    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/tags",
            method="GET"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode())
            models = [m["name"] for m in result.get("models", [])]

            # Verificar se o modelo está disponível
            model_available = any(OLLAMA_MODEL in m for m in models)
            if not model_available:
                print(f"Modelo {OLLAMA_MODEL} não encontrado. Modelos disponíveis: {models}", file=sys.stderr)
                print(f"Instale com: ollama pull {OLLAMA_MODEL}", file=sys.stderr)
                return False

            return True
    except Exception as e:
        print(f"Ollama não disponível: {e}", file=sys.stderr)
        print("Inicie o Ollama com: ollama serve", file=sys.stderr)
        return False


def process_memories():
    """Processa memórias sem embedding."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando geração de embeddings...")

    # Verificar Ollama
    if not check_ollama_available():
        sys.exit(1)

    # Buscar memórias sem embedding
    memories = get_memories_without_embedding()

    if not memories:
        print("Nenhuma memória pendente de embedding")
        return

    print(f"Encontradas {len(memories)} memórias para processar\n")

    success_count = 0
    error_count = 0

    for i, memory in enumerate(memories, 1):
        memory_id = memory["id"]
        titulo = memory.get("titulo", "")[:50]

        print(f"[{i}/{len(memories)}] {titulo}...", end=" ")

        try:
            # Formatar texto
            text = format_memory_text(memory)

            # Gerar embedding
            embedding = get_embedding(text)

            if not embedding:
                print("ERRO: embedding vazio")
                error_count += 1
                continue

            # Salvar no Supabase
            if update_memory_embedding(memory_id, embedding):
                print(f"OK ({len(embedding)} dims)")
                success_count += 1
            else:
                print("ERRO ao salvar")
                error_count += 1

        except Exception as e:
            print(f"ERRO: {e}")
            error_count += 1

    print(f"\nResultado: {success_count} sucesso, {error_count} erros")


def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados", file=sys.stderr)
        sys.exit(1)

    process_memories()


if __name__ == "__main__":
    main()
