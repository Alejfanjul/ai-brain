#!/usr/bin/env python3
"""
Parser for goals markdown files (SAUDE.md and MACONHA.md).
Extracts structured data for progress tracking.
"""

import re
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

# Base paths
AI_BRAIN = Path.home() / "ai-brain"
METAS_DIR = AI_BRAIN / "projects" / "ai-brain" / "metas"

# Wendler 3/5/1 week type mapping (Prep & Fat Loss template)
WEEK_TYPE_351 = {1: '3s', 2: '5s', 3: '1s'}


def parse_saude(filepath: Optional[Path] = None) -> dict:
    """
    Parse SAUDE.md and extract training data.

    Handles current format:
    - Status Atual: **Ciclo N — Leader (Prep and Fat Loss)**
    - Week headers: ### Semana DD-DD Mmm (Ciclo N - Semana M)
    - TM table: | Lift | Ciclo 1 TM | Ciclo 2 TM |
    - Log: | DD/MM Dia | Treino | Notas |
    - Lift entries: "Lift Ciclo N Sem M" (e.g., "OHP Ciclo 2 Sem 1")
    """
    if filepath is None:
        filepath = METAS_DIR / "SAUDE.md"

    content = filepath.read_text(encoding='utf-8')

    result = {
        'ciclo': 1,
        'semana': 1,
        'semana_tipo': '3s',
        'tms': {},
        'proximo_treino': None,
        'ordem_lifts': ['Squat', 'OHP', 'Deadlift', 'Bench'],
        'lifts_completados': [],
        'log_semanal': [],
    }

    # --- 1. Extract cycle from Status Atual ---
    ciclo_match = re.search(r'\*\*Ciclo\s+(\d+)\s*[—–-]', content)
    if ciclo_match:
        result['ciclo'] = int(ciclo_match.group(1))

    # --- 2. Extract semana from latest week header ---
    # Pattern: ### Semana DD-DD Mmm (Ciclo N - Semana M)
    week_headers = list(re.finditer(
        r'###\s+Semana\s+.+?\(Ciclo\s+(\d+)\s*-\s*Semana\s+(\d+)\)',
        content
    ))
    if week_headers:
        last = week_headers[-1]
        result['ciclo'] = int(last.group(1))
        result['semana'] = int(last.group(2))

    # --- 3. Week type from 3/5/1 ordering ---
    result['semana_tipo'] = WEEK_TYPE_351.get(result['semana'], '3s')

    # --- 4. Lift order ---
    ordem_match = re.search(r'\*\*Ordem dos lifts:\*\*\s*(.+)', content)
    if ordem_match:
        result['ordem_lifts'] = [l.strip() for l in ordem_match.group(1).split('→')]

    # --- 5. TMs — last kg value per lift row ---
    for match in re.finditer(r'\|\s*(Squat|Bench|Deadlift|OHP)\s*\|(.+)', content):
        lift = match.group(1)
        kg_values = re.findall(r'([\d.]+)kg', match.group(2))
        if kg_values:
            result['tms'][lift] = float(kg_values[-1])

    # --- 6. Parse ALL log entries ---
    # Format: | DD/MM Dia | Treino text | Notas text |
    all_entries = []
    for match in re.finditer(
        r'\|\s*(\d{2}/\d{2})\s+\S+\s*\|\s*([^|]+)\|\s*([^|]*)\|',
        content
    ):
        date_str = match.group(1)
        treino = match.group(2).strip()
        notas = match.group(3).strip()
        try:
            day, month = date_str.split('/')
            entry_date = date(2026, int(month), int(day))
        except ValueError:
            continue
        all_entries.append({
            'data': date_str,
            'date': entry_date,
            'treino': treino,
            'notas': notas,
        })

    result['log_semanal'] = all_entries

    # --- 7. Find completed lifts for current cycle+semana ---
    ciclo = result['ciclo']
    semana = result['semana']
    main_lifts = set(result['ordem_lifts'])

    for entry in all_entries:
        treino = entry['treino']
        # "Lift Ciclo N Sem M" pattern
        m = re.match(r'(\w+)\s+Ciclo\s+(\d+)\s+Sem\s+(\d+)', treino)
        if m and int(m.group(2)) == ciclo and int(m.group(3)) == semana:
            lift = m.group(1)
            if lift in main_lifts and lift not in result['lifts_completados']:
                result['lifts_completados'].append(lift)

    # --- 8. Determine next lift ---
    completados = set(result['lifts_completados'])
    for lift in result['ordem_lifts']:
        if lift not in completados:
            result['proximo_treino'] = lift
            break

    if not result['proximo_treino'] and len(completados) >= len(result['ordem_lifts']):
        result['proximo_treino'] = result['ordem_lifts'][0]

    return result


def parse_maconha(filepath: Optional[Path] = None) -> dict:
    """
    Parse MACONHA.md and extract usage data.

    Handles reflective format (Feb 2026+):
    - Weekly narrative sections with **Uso:**, **Como me senti:**, **Impacto no resto:**
    - No daily tables, no streak counting, no rigid alerts.
    """
    if filepath is None:
        filepath = METAS_DIR / "MACONHA.md"

    content = filepath.read_text(encoding='utf-8')

    result = {
        'modelo': 'reflexivo',
        'padrao_natural': '',
        'criterio': '',
        'semanas': [],
    }

    # Extract current model info
    padrao_match = re.search(r'\*\*Padrão natural:\*\*\s*(.+)', content)
    if padrao_match:
        result['padrao_natural'] = padrao_match.group(1).strip()

    criterio_match = re.search(r'\*\*Critério real:\*\*\s*(.+)', content)
    if criterio_match:
        result['criterio'] = criterio_match.group(1).strip()

    # Parse weekly sections under "## Log Semanal"
    log_section = re.split(r'^## Log Semanal\s*$', content, flags=re.MULTILINE)
    if len(log_section) < 2:
        return result

    log_content = log_section[1]
    # Stop at next ## section
    log_content = re.split(r'^## (?!#)', log_content, flags=re.MULTILINE)[0]

    # Split by ### headers
    week_blocks = re.split(r'^### ', log_content, flags=re.MULTILINE)[1:]

    for block in week_blocks:
        lines = block.strip().split('\n')
        header = lines[0].strip() if lines else ''
        body = '\n'.join(lines[1:])

        uso_match = re.search(r'\*\*Uso:\*\*\s*(.+?)(?:\n\n|\n\*\*|$)', body, re.DOTALL)
        sentimento_match = re.search(r'\*\*Como me senti:\*\*\s*(.+?)(?:\n\n|\n\*\*|$)', body, re.DOTALL)
        impacto_match = re.search(r'\*\*Impacto no resto:\*\*\s*(.+?)(?:\n\n|\n\*\*|$)', body, re.DOTALL)

        semana = {
            'header': header,
            'uso': uso_match.group(1).strip() if uso_match else '',
            'sentimento': sentimento_match.group(1).strip() if sentimento_match else '',
            'impacto': impacto_match.group(1).strip() if impacto_match else '',
        }
        result['semanas'].append(semana)

    return result


if __name__ == "__main__":
    print("=== SAUDE ===")
    saude = parse_saude()
    for key, value in saude.items():
        if key == 'log_semanal':
            print(f"{key}: [{len(value)} entries]")
        else:
            print(f"{key}: {value}")

    print("\n=== MACONHA ===")
    maconha = parse_maconha()
    for key, value in maconha.items():
        if key == 'log_entries':
            print(f"{key}: [{len(value)} entries]")
        else:
            print(f"{key}: {value}")
