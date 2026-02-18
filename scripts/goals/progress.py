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
    Calculate usage progress metrics for Livre model.

    Progress bar represents streak toward 7-day target.
    Alert triggers if 2+ days smoked for 2 consecutive weeks.
    """
    if data is None:
        data = parse_maconha()

    hoje = date.today()
    hoje_dia = WEEKDAY_PT[hoje.weekday()]

    streak = data['streak']
    fumou_esta = data.get('fumou_esta_semana', 0)
    fumou_passada = data.get('fumou_semana_passada', 0)
    alerta = data.get('alerta', False)
    week_start = data.get('week_start', hoje - timedelta(days=hoje.weekday()))

    # Progress: streak toward 7-day target
    progresso_streak = min(1.0, streak / 7)

    # Alert text
    alerta_texto = ''
    if alerta:
        alerta_texto = '⚠ ALERTA: 2+ dias por 2 semanas seguidas'
    elif fumou_passada >= 2:
        alerta_texto = f'⚠ Semana passada: {fumou_passada} dia(s) — acima de 1x'

    return {
        'modelo': data.get('modelo', 'livre'),
        'padrao': data.get('padrao', '~1x/semana'),
        'streak': streak,
        'progresso_streak': progresso_streak,
        'fumou_esta_semana': fumou_esta,
        'fumou_semana_passada': fumou_passada,
        'alerta': alerta,
        'alerta_texto': alerta_texto,
        'ultimo_uso': data.get('ultimo_uso'),
        'hoje_dia': hoje_dia,
        'week_start': week_start,
        'titulo': f"Livre ({data.get('padrao', '~1x/semana')})",
        'subtitulo': f'Streak: {streak} dias sem fumar',
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
    streak = maconha['streak']
    if maconha.get('alerta'):
        focus.append(f"⚠ Atenção: uso acima de 1x/semana por 2 semanas")
    elif streak >= 5:
        focus.append(f"Streak: {streak} dias ✓")
    else:
        focus.append(f"Streak: {streak} dias — meta ~7 entre usos")

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
