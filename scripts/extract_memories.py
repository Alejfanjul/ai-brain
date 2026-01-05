#!/usr/bin/env python3
"""
Extrai memórias de conversas do Claude Code.
Roda a cada 15 minutos via cron.
Baseado no Memory Lane do Alex Hillman (JFDI System).
"""

import json
import os
import sys
import urllib.request
import urllib.error
import re
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
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Prompt de extração de memórias
MEMORY_EXTRACTION_PROMPT = """Analise este transcript de conversa e extraia momentos memoráveis.

Procure por estes tipos de memórias:
1. **decisao** - Escolhas feitas sobre implementação, arquitetura, abordagem
2. **insight** - Realizações sobre como algo funciona ou deveria funcionar
3. **padrao** - Comportamentos repetidos, workflows, abordagens
4. **aprendizado** - Conhecimento novo adquirido ou ensinado
5. **correcao** - Erros identificados e corrigidos (em qualquer direção)
6. **workflow** - Sequências de ações para tarefas específicas
7. **gap** - Desconexões identificadas entre sistemas que deveriam se comunicar

SURPRISE TRIGGERS (priorize estes):
- Recovery patterns: tentou X, falhou, fez Y, funcionou
- Correções do usuário: "não, faça assim", "errado", "na verdade"
- Sinais de entusiasmo: "perfeito!", "exatamente!", "muito bom!"
- Reações negativas: "nunca faça isso", "não quero", "para"
- Pedidos repetidos: mesma coisa pedida múltiplas vezes

Para cada memória, retorne JSON com:
- tipo: um de [decisao, insight, padrao, aprendizado, correcao, workflow, gap]
- titulo: título breve (max 80 chars)
- resumo: 1-2 frases resumindo
- reasoning: por que isso vale lembrar
- confidence_score: 0.0-1.0 (quão confiante que é memorável)
- surprise_score: 0.0-1.0 (quão forte são os surprise triggers)
- entidades: lista de {type: pessoa|projeto|arquivo, name: string}
- contexto_original: o trecho relevante do transcript
- formada_em: timestamp aproximado (do transcript)

Retorne um JSON array. Retorne [] se não houver memórias relevantes.
Foque em qualidade, não quantidade. Máximo 5 memórias por conversa.

TRANSCRIPT:
{transcript}

Responda APENAS com o JSON array, sem explicações."""


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


def call_claude_api(prompt: str, max_tokens: int = 4000) -> str:
    """Chama a API do Claude para extração de memórias."""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    data = {
        "model": "claude-3-5-haiku-20241022",  # Haiku para custo/velocidade
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"Claude API Error {e.code}: {error_body}", file=sys.stderr)
        raise


def get_unprocessed_conversations() -> list:
    """Busca conversas que ainda não foram processadas para memórias."""
    # Buscar conversas que:
    # 1. Têm mais de 5 mensagens (conversas significativas)
    # 2. Não estão na tabela processamento_memoria
    # 3. Não são subagentes (processar só conversas principais)

    query = (
        "conversas?select=id,session_id,resumo,objetivo,total_mensagens,repositorio,iniciado_em"
        "&is_subagent=eq.false"
        "&total_mensagens=gte.5"
        "&order=iniciado_em.desc"
        "&limit=10"
    )

    conversas = supabase_request(query)

    # Filtrar as que já foram processadas
    if not conversas:
        return []

    conversa_ids = [c["id"] for c in conversas]
    ids_str = ",".join(f'"{id}"' for id in conversa_ids)

    processadas = supabase_request(f"processamento_memoria?conversa_id=in.({ids_str})&select=conversa_id")
    processadas_ids = {p["conversa_id"] for p in processadas}

    return [c for c in conversas if c["id"] not in processadas_ids]


def get_conversation_messages(conversa_id: str) -> list:
    """Busca mensagens de uma conversa."""
    messages = supabase_request(
        f"mensagens?conversa_id=eq.{conversa_id}&select=tipo,conteudo,timestamp_original&order=timestamp_original.asc"
    )
    return messages


def format_transcript(messages: list, max_chars: int = 15000) -> str:
    """Formata mensagens em transcript legível."""
    lines = []
    for msg in messages:
        tipo = "USER" if msg["tipo"] == "user" else "ASSISTANT"
        conteudo = msg.get("conteudo", "")[:2000]  # Limitar cada mensagem
        timestamp = msg.get("timestamp_original", "")[:19] if msg.get("timestamp_original") else ""
        lines.append(f"[{timestamp}] {tipo}: {conteudo}")

    transcript = "\n\n".join(lines)

    # Truncar se muito longo
    if len(transcript) > max_chars:
        transcript = transcript[:max_chars] + "\n\n[... transcript truncado ...]"

    return transcript


def extract_memories(transcript: str) -> list:
    """Usa Claude para extrair memórias do transcript."""
    prompt = MEMORY_EXTRACTION_PROMPT.format(transcript=transcript)

    try:
        response = call_claude_api(prompt)

        # Extrair JSON da resposta
        # Às vezes vem com ```json ... ```
        json_match = re.search(r'\[[\s\S]*\]', response)
        if json_match:
            return json.loads(json_match.group())
        return []
    except Exception as e:
        print(f"Erro ao extrair memórias: {e}", file=sys.stderr)
        return []


def save_memory(conversa_id: str, memory: dict) -> bool:
    """Salva uma memória no Supabase."""
    try:
        data = {
            "conversa_id": conversa_id,
            "tipo": memory.get("tipo", "insight"),
            "titulo": memory.get("titulo", "")[:200],
            "resumo": memory.get("resumo", "")[:1000],
            "reasoning": memory.get("reasoning", "")[:500],
            "contexto_original": memory.get("contexto_original", "")[:2000],
            "confidence_score": float(memory.get("confidence_score", 0.5)),
            "surprise_score": float(memory.get("surprise_score", 0.0)),
            "entidades_relacionadas": memory.get("entidades", []),
            "formada_em": memory.get("formada_em"),
            "ativo": True
        }

        supabase_request("memorias", method="POST", data=data)
        return True
    except Exception as e:
        print(f"Erro ao salvar memória: {e}", file=sys.stderr)
        return False


def mark_conversation_processed(conversa_id: str, memorias_count: int, status: str = "sucesso", erro: str = None):
    """Marca conversa como processada."""
    data = {
        "conversa_id": conversa_id,
        "memorias_extraidas": memorias_count,
        "status": status,
        "erro_msg": erro,
        "versao_processador": "v1"
    }

    try:
        supabase_request("processamento_memoria", method="POST", data=data)
    except Exception as e:
        print(f"Erro ao marcar processamento: {e}", file=sys.stderr)


def process_conversation(conversa: dict) -> int:
    """Processa uma conversa e extrai memórias."""
    conversa_id = conversa["id"]
    session_id = conversa["session_id"]

    print(f"Processando: {session_id[:12]}... ({conversa['total_mensagens']} msgs)")

    # Buscar mensagens
    messages = get_conversation_messages(conversa_id)
    if not messages:
        mark_conversation_processed(conversa_id, 0, "erro", "Sem mensagens")
        return 0

    # Formatar transcript
    transcript = format_transcript(messages)

    # Extrair memórias
    memories = extract_memories(transcript)

    # Salvar memórias
    saved_count = 0
    for memory in memories:
        if save_memory(conversa_id, memory):
            saved_count += 1
            print(f"  + [{memory.get('tipo')}] {memory.get('titulo', '')[:50]}")

    # Marcar como processada
    mark_conversation_processed(conversa_id, saved_count)

    return saved_count


def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados", file=sys.stderr)
        sys.exit(1)

    if not ANTHROPIC_API_KEY:
        print("ANTHROPIC_API_KEY deve estar configurado para extração de memórias", file=sys.stderr)
        sys.exit(1)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando extração de memórias...")

    # Buscar conversas não processadas
    conversas = get_unprocessed_conversations()

    if not conversas:
        print("Nenhuma conversa nova para processar")
        return

    print(f"Encontradas {len(conversas)} conversas para processar\n")

    total_memories = 0
    for conversa in conversas:
        try:
            count = process_conversation(conversa)
            total_memories += count
        except Exception as e:
            print(f"Erro processando {conversa['session_id'][:12]}: {e}", file=sys.stderr)
            mark_conversation_processed(conversa["id"], 0, "erro", str(e))

    print(f"\nTotal de memórias extraídas: {total_memories}")


if __name__ == "__main__":
    main()
