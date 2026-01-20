#!/usr/bin/env python3
"""
Parser for goals markdown files (SAUDE.md and MACONHA.md).
Extracts structured data for progress tracking.
"""

import re
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# Base paths
AI_BRAIN = Path.home() / "ai-brain"
METAS_DIR = AI_BRAIN / "projects" / "ai-brain" / "metas"


def parse_saude(filepath: Optional[Path] = None) -> dict:
    """
    Parse SAUDE.md and extract training data.

    Returns:
        dict with keys:
        - ciclo: int (cycle number)
        - semana: int (week number, 1-4)
        - semana_tipo: str ('5s', '3s', '1s', 'deload')
        - tms: dict[str, int] (lift -> TM in kg)
        - proximo_treino: str (next lift name)
        - ordem_lifts: list[str] (lift order)
        - log_semanal: list[dict] (weekly log entries)
        - lifts_completados: list[str] (lifts done this week)
    """
    if filepath is None:
        filepath = METAS_DIR / "SAUDE.md"

    content = filepath.read_text(encoding='utf-8')

    result = {
        'ciclo': 1,
        'semana': 1,
        'semana_tipo': '5s',
        'tms': {},
        'proximo_treino': None,
        'ordem_lifts': ['Deadlift', 'Bench', 'Squat', 'OHP'],
        'log_semanal': [],
        'lifts_completados': [],
    }

    # Extract cycle and week: **Ciclo X, Semana Y** (semana das Xs)
    ciclo_match = re.search(r'\*\*Ciclo\s+(\d+),\s+Semana\s+(\d+)\*\*\s*\(semana das (\d+)', content)
    if ciclo_match:
        result['ciclo'] = int(ciclo_match.group(1))
        result['semana'] = int(ciclo_match.group(2))
        reps = ciclo_match.group(3)
        result['semana_tipo'] = f"{reps}s"

    # Fallback: check timeline for "← AQUI" marker
    if not ciclo_match:
        timeline_match = re.search(r'├── Semana (\d+) \((\d+)s\) ← AQUI', content)
        if timeline_match:
            result['semana'] = int(timeline_match.group(1))
            result['semana_tipo'] = f"{timeline_match.group(2)}s"

    # Extract TMs from table
    # | Lift | 1RM Estimado | TM (80%) |
    tm_pattern = r'\|\s*(Squat|Bench|Deadlift|OHP)\s*\|\s*[\d.]+kg\s*\|\s*(\d+)kg\s*\|'
    for match in re.finditer(tm_pattern, content):
        lift = match.group(1)
        tm = int(match.group(2))
        result['tms'][lift] = tm

    # Extract próximo treino
    proximo_match = re.search(r'\*\*Próximo treino:\*\*\s*(\w+)', content)
    if proximo_match:
        result['proximo_treino'] = proximo_match.group(1)

    # Extract lift order
    ordem_match = re.search(r'\*\*Ordem dos lifts:\*\*\s*(.+)', content)
    if ordem_match:
        lifts_str = ordem_match.group(1)
        result['ordem_lifts'] = [l.strip() for l in lifts_str.split('→')]

    # Extract log semanal (current week)
    # Pattern: | DD/MM | Treino | Sim/Não/? | energia | notas |
    log_pattern = r'\|\s*(\d{2}/\d{2})\s+\w+\s*\|\s*([^|]+)\|\s*(Sim|Não|[^|]*)\s*\|\s*([^|]*)\|\s*([^|]*)\|'
    for match in re.finditer(log_pattern, content):
        date_str = match.group(1)
        treino = match.group(2).strip()
        completou = match.group(3).strip()
        energia = match.group(4).strip()
        notas = match.group(5).strip()

        entry = {
            'data': date_str,
            'treino': treino,
            'completou': completou == 'Sim',
            'energia': energia,
            'notas': notas,
        }
        result['log_semanal'].append(entry)

        # Track completed lifts
        if completou == 'Sim' and treino:
            # Extract lift name from "Deadlift (S2)"
            lift_match = re.match(r'(\w+)', treino)
            if lift_match:
                result['lifts_completados'].append(lift_match.group(1))

    return result


def parse_maconha(filepath: Optional[Path] = None) -> dict:
    """
    Parse MACONHA.md and extract reduction plan data.

    Returns:
        dict with keys:
        - fase_atual: int (current phase number)
        - fase_padrao: str (allowed pattern, e.g., "Sex-Sáb-Dom")
        - fase_inicio: date
        - fase_fim: date
        - dias_permitidos: list[str] (allowed day names)
        - log_semanal: list[dict] (weekly log entries)
        - streak: int (consecutive days without smoking)
        - ultimo_uso: date or None
    """
    if filepath is None:
        filepath = METAS_DIR / "MACONHA.md"

    content = filepath.read_text(encoding='utf-8')

    result = {
        'fase_atual': 1,
        'fase_padrao': '',
        'fase_inicio': None,
        'fase_fim': None,
        'dias_permitidos': [],
        'log_semanal': [],
        'streak': 0,
        'ultimo_uso': None,
    }

    # Extract current phase from table (look for **ATUAL**)
    # Pattern: | 1 | **Sex-Sáb-Dom** (3 dias) | 2 semanas | **ATUAL** |
    fase_pattern = r'\|\s*(\d+)\s*\|\s*\*?\*?([A-Za-záéíóúÁÉÍÓÚ\-]+)\*?\*?[^|]*\|\s*[^|]+\|\s*\*\*ATUAL\*\*\s*\|'
    fase_match = re.search(fase_pattern, content)
    if fase_match:
        result['fase_atual'] = int(fase_match.group(1))
        padrao = fase_match.group(2).strip().strip('*')
        result['fase_padrao'] = padrao

        # Extract allowed days from pattern (e.g., "Sex-Sáb-Dom")
        dias_map = {
            'Seg': 'Segunda',
            'Ter': 'Terça',
            'Qua': 'Quarta',
            'Qui': 'Quinta',
            'Sex': 'Sexta',
            'Sáb': 'Sábado',
            'Sab': 'Sábado',
            'Dom': 'Domingo',
        }
        for abbrev in padrao.split('-'):
            abbrev = abbrev.strip().strip('*')
            if abbrev in dias_map:
                result['dias_permitidos'].append(dias_map[abbrev])

    # Extract phase dates
    # **Início da Fase X:** YYYY-MM-DD
    inicio_match = re.search(r'\*\*Início da Fase \d+:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    if inicio_match:
        result['fase_inicio'] = datetime.strptime(inicio_match.group(1), '%Y-%m-%d').date()

    fim_match = re.search(r'\*\*Fim da Fase \d+:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    if fim_match:
        result['fase_fim'] = datetime.strptime(fim_match.group(1), '%Y-%m-%d').date()

    # Extract log entries and calculate streak
    # Pattern: | DD/MM | Dia | Não/Sim | energia | sono | notas |
    log_pattern = r'\|\s*(\d{2}/\d{2})\s*\|\s*(\w+)\s*\|\s*(Sim|Não|[^|]*)\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|'

    all_entries = []
    for match in re.finditer(log_pattern, content):
        date_str = match.group(1)
        dia = match.group(2).strip()
        fumou_raw = match.group(3).strip()
        energia = match.group(4).strip()
        sono = match.group(5).strip()
        notas = match.group(6).strip()

        # Parse fumou status
        fumou = None
        if fumou_raw == 'Sim':
            fumou = True
        elif fumou_raw == 'Não':
            fumou = False
        # else: None (not recorded yet)

        entry = {
            'data': date_str,
            'dia': dia,
            'fumou': fumou,
            'energia': energia,
            'sono': sono,
            'notas': notas,
        }
        all_entries.append(entry)
        result['log_semanal'].append(entry)

    # Calculate streak (consecutive "Não" from most recent entry going backwards)
    # Only count entries that have been filled in (fumou is not None)
    filled_entries = [e for e in all_entries if e['fumou'] is not None]

    # Sort by date (assuming DD/MM format, year is 2026)
    def parse_date(entry):
        day, month = entry['data'].split('/')
        return date(2026, int(month), int(day))

    filled_entries.sort(key=parse_date, reverse=True)

    streak = 0
    for entry in filled_entries:
        if entry['fumou'] is False:
            streak += 1
        else:
            if entry['fumou'] is True:
                result['ultimo_uso'] = parse_date(entry)
            break

    result['streak'] = streak

    return result


if __name__ == "__main__":
    # Test parsing
    print("=== SAÚDE ===")
    saude = parse_saude()
    for key, value in saude.items():
        print(f"{key}: {value}")

    print("\n=== MACONHA ===")
    maconha = parse_maconha()
    for key, value in maconha.items():
        print(f"{key}: {value}")
