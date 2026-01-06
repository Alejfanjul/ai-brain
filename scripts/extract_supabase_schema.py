#!/usr/bin/env python3
"""
Extrai schema do Supabase AI Brain via REST API.

Uso:
    python3 scripts/extract_supabase_schema.py

Gera arquivo em: docs/schemas/supabase_ai_brain_schema_YYYYMMDD.sql
"""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Carregar .env
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Erro: SUPABASE_URL e SUPABASE_ANON_KEY devem estar no .env")
    exit(1)


def supabase_request(endpoint: str, method: str = "GET", params: dict = None):
    """Faz request para Supabase REST API."""
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"HTTP Error {e.code}: {error_body}")
        return None


def get_table_data(table_name: str, limit: int = 5):
    """Obtém amostra de dados de uma tabela."""
    return supabase_request(table_name, params={"limit": str(limit)})


def infer_schema_from_data(table_name: str, data: list) -> dict:
    """Infere schema a partir dos dados."""
    if not data:
        return {"columns": [], "sample_count": 0}

    columns = {}
    for row in data:
        for key, value in row.items():
            if key not in columns:
                columns[key] = {
                    "name": key,
                    "types_seen": set(),
                    "nullable": False,
                    "sample_values": []
                }

            # Detectar tipo
            if value is None:
                columns[key]["nullable"] = True
            else:
                py_type = type(value).__name__
                if py_type == "str":
                    if len(value) == 36 and value.count("-") == 4:
                        columns[key]["types_seen"].add("UUID")
                    elif "T" in value and ("Z" in value or "+" in value):
                        columns[key]["types_seen"].add("TIMESTAMPTZ")
                    else:
                        columns[key]["types_seen"].add("TEXT")
                elif py_type == "int":
                    columns[key]["types_seen"].add("INTEGER")
                elif py_type == "float":
                    columns[key]["types_seen"].add("FLOAT")
                elif py_type == "bool":
                    columns[key]["types_seen"].add("BOOLEAN")
                elif py_type == "list":
                    columns[key]["types_seen"].add("JSONB/ARRAY")
                elif py_type == "dict":
                    columns[key]["types_seen"].add("JSONB")
                else:
                    columns[key]["types_seen"].add(py_type.upper())

            # Guardar sample
            if len(columns[key]["sample_values"]) < 2 and value is not None:
                sample = str(value)[:50]
                if sample not in columns[key]["sample_values"]:
                    columns[key]["sample_values"].append(sample)

    # Converter sets para lists para serialização
    for col in columns.values():
        col["types_seen"] = list(col["types_seen"])

    return {
        "columns": list(columns.values()),
        "sample_count": len(data)
    }


def format_table_sql(table_name: str, schema: dict) -> list:
    """Formata tabela como SQL."""
    lines = []
    lines.append("")
    lines.append("-- " + "=" * 50)
    lines.append(f"-- Table: {table_name}")
    lines.append(f"-- Colunas detectadas: {len(schema['columns'])}")
    lines.append(f"-- Registros analisados: {schema['sample_count']}")
    lines.append("-- " + "=" * 50)
    lines.append("")
    lines.append(f"CREATE TABLE {table_name} (")

    for i, col in enumerate(schema["columns"]):
        types = ", ".join(col["types_seen"]) if col["types_seen"] else "UNKNOWN"
        nullable = "" if col["nullable"] else " NOT NULL"
        comma = "," if i < len(schema["columns"]) - 1 else ""

        # Comentário com samples
        samples = col["sample_values"]
        sample_comment = ""
        if samples:
            sample_str = ", ".join(f"'{s}'" for s in samples[:2])
            sample_comment = f"  -- ex: {sample_str}"

        lines.append(f"    {col['name']} {types}{nullable}{comma}{sample_comment}")

    lines.append(");")
    return lines


def main():
    print("🔍 Extraindo schema do Supabase AI Brain...")
    print(f"   URL: {SUPABASE_URL}")

    # Tabelas conhecidas do schema (baseado nos arquivos .sql)
    known_tables = [
        "conversas",
        "mensagens",
        "memorias",
        "memoria_recuperacoes",
        "entidades",
        "memoria_entidade",
        "processamento_memoria",
        "aprendizados",
        "workflows",
        "sops",
        "erros",
        "decisoes",
        "preferencias",
    ]

    # Tentar descobrir mais tabelas fazendo request às conhecidas
    tables_found = {}

    print("\n📋 Verificando tabelas...")
    for table in known_tables:
        print(f"   Verificando {table}...", end=" ")
        data = get_table_data(table, limit=10)

        if data is not None:
            schema = infer_schema_from_data(table, data)
            tables_found[table] = {
                "schema": schema,
                "row_count": len(data),
                "exists": True
            }
            print(f"✓ ({len(data)} registros, {len(schema['columns'])} colunas)")
        else:
            tables_found[table] = {"exists": False}
            print("✗ (não existe ou vazia)")

    # Gerar arquivo SQL
    output_dir = Path(__file__).parent.parent / "docs" / "schemas"
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime('%Y%m%d')
    output_file = output_dir / f"supabase_ai_brain_schema_{today}.sql"

    lines = [
        "-- " + "=" * 50,
        "-- SUPABASE AI BRAIN - SCHEMA EXTRACTION",
        f"-- Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"-- Projeto: {SUPABASE_URL.split('//')[1].split('.')[0]}",
        "-- " + "=" * 50,
        "",
        "-- NOTA: Schema inferido a partir dos dados existentes.",
        "-- Tipos podem não ser 100% precisos.",
        "-- Para schema exato, use pg_dump ou Supabase Dashboard.",
        "",
    ]

    # Resumo
    existing = [t for t, info in tables_found.items() if info.get("exists")]
    missing = [t for t, info in tables_found.items() if not info.get("exists")]

    lines.append("-- RESUMO:")
    lines.append(f"-- Tabelas encontradas: {len(existing)}")
    lines.append(f"-- Tabelas não encontradas: {len(missing)}")
    if missing:
        lines.append(f"-- Missing: {', '.join(missing)}")
    lines.append("")

    # Contagem de registros
    lines.append("-- CONTAGEM DE REGISTROS:")
    for table, info in tables_found.items():
        if info.get("exists"):
            count = info.get("row_count", 0)
            lines.append(f"-- {table}: {count}+ registros")
    lines.append("")

    # Detalhe de cada tabela
    for table, info in tables_found.items():
        if info.get("exists"):
            schema = info["schema"]
            table_lines = format_table_sql(table, schema)
            lines.extend(table_lines)

    # Footer
    lines.extend([
        "",
        "-- " + "=" * 50,
        "-- FIM DO SCHEMA",
        f"-- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-- " + "=" * 50,
    ])

    # Salvar
    output_file.write_text('\n'.join(lines), encoding='utf-8')

    print(f"\n✅ Schema extraído!")
    print(f"   Arquivo: {output_file}")
    print(f"   Tabelas: {len(existing)} encontradas, {len(missing)} não encontradas")

    # Mostrar resumo de dados
    print("\n📊 Resumo dos dados:")
    total_rows = 0
    for table, info in tables_found.items():
        if info.get("exists"):
            count = info.get("row_count", 0)
            total_rows += count
            cols = len(info["schema"]["columns"])
            print(f"   {table}: {count}+ registros, {cols} colunas")

    print(f"\n   Total visível: {total_rows}+ registros")
    print("   (limitado a 10 por tabela na amostragem)")


if __name__ == "__main__":
    main()
