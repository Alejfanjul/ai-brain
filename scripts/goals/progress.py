#!/usr/bin/env python3
"""
Progress calculator for goals tracking.
Calculates metrics from parsed data.
"""

from datetime import date, timedelta
from typing import Optional

try:
    from .parser import parse_saude, parse_maconha
except ImportError:
    from parser import parse_saude, parse_maconha


WEEKDAY_PT = {
    0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta',
    4: 'Sexta', 5: 'Sábado', 6: 'Domingo',
}

WEEKDAY_ABBREV = {
    0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui',
    4: 'Sex', 5: 'Sáb', 6: 'Dom',
}


def calculate_saude_progress(data: Optional[dict] = None) -> dict:
    """
    Calculate training progress metrics.

    Cycle has 3 weeks (3/5/1), 4 lifts per week = 12 total.
    Progress = completed lifts position / 12.
    """
    if data is None:
        data = parse_saude()

    ciclo = data['ciclo']
    semana = data['semana']
    semana_tipo = data['semana_tipo']
    ordem = data['ordem_lifts']
    completados = data['lifts_completados']

    # 3 weeks per cycle, N lifts per week
    lifts_done = len(completados)
    total_position = (semana - 1) * len(ordem) + lifts_done
    total_lifts = 3 * len(ordem)
    progresso_ciclo = total_position / total_lifts

    lifts_restantes = [l for l in ordem if l not in completados]

    semana_display = {'5s': '5s', '3s': '3s', '1s': '1s'}.get(semana_tipo, semana_tipo)

    return {
        'ciclo': ciclo,
        'semana': semana,
        'semana_tipo': semana_tipo,
        'progresso_ciclo': progresso_ciclo,
        'proximo_treino': data.get('proximo_treino'),
        'lifts_restantes': lifts_restantes,
        'lifts_completados': completados,
        'titulo': '5/3/1 Prep & Fat Loss',
        'subtitulo': f'Ciclo {ciclo} | Semana {semana} ({semana_display})',
    }


def calculate_maconha_progress(data: Optional[dict] = None) -> dict:
    """
    Calculate usage info for reflective model.

    No streak counting, no progress bars, no rigid alerts.
    Shows latest week's reflection and pattern.
    """
    if data is None:
        data = parse_maconha()

    hoje = date.today()
    hoje_dia = WEEKDAY_PT[hoje.weekday()]

    semanas = data.get('semanas', [])
    ultima = semanas[0] if semanas else {}

    return {
        'modelo': data.get('modelo', 'reflexivo'),
        'padrao_natural': data.get('padrao_natural', ''),
        'criterio': data.get('criterio', ''),
        'hoje_dia': hoje_dia,
        'ultima_semana': ultima,
        'total_semanas': len(semanas),
    }


def get_today_focus(saude: Optional[dict] = None, maconha: Optional[dict] = None) -> list[str]:
    """Get 3 focus items for today."""
    if saude is None:
        saude = calculate_saude_progress()
    if maconha is None:
        maconha = calculate_maconha_progress()

    focus = []

    # Training focus
    proximo = saude.get('proximo_treino')
    if proximo:
        focus.append(f"Treino: {proximo} ({saude['semana_tipo']})")
    else:
        focus.append("Todos os lifts da semana completos!")

    # Maconha focus
    ultima = maconha.get('ultima_semana', {})
    impacto = ultima.get('impacto', '')
    if impacto and 'nenhum' in impacto.lower():
        focus.append("Maconha: uso sem impacto esta semana")
    elif impacto:
        focus.append(f"Maconha: {impacto[:50]}")
    else:
        focus.append("Maconha: sem registro esta semana")

    # Mobility
    focus.append("Mobilidade: 10-15 min (trapézio + cervical)")

    return focus[:3]


if __name__ == "__main__":
    print("=== SAUDE PROGRESS ===")
    saude = calculate_saude_progress()
    for key, value in saude.items():
        print(f"{key}: {value}")

    print("\n=== MACONHA PROGRESS ===")
    maconha = calculate_maconha_progress()
    for key, value in maconha.items():
        print(f"{key}: {value}")

    print("\n=== TODAY'S FOCUS ===")
    focus = get_today_focus(saude, maconha)
    for i, item in enumerate(focus, 1):
        print(f"{i}. {item}")
