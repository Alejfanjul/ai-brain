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


# Weekday mapping (Python: 0=Monday, 6=Sunday)
WEEKDAY_PT = {
    0: 'Segunda',
    1: 'Terça',
    2: 'Quarta',
    3: 'Quinta',
    4: 'Sexta',
    5: 'Sábado',
    6: 'Domingo',
}

WEEKDAY_ABBREV = {
    0: 'Seg',
    1: 'Ter',
    2: 'Qua',
    3: 'Qui',
    4: 'Sex',
    5: 'Sáb',
    6: 'Dom',
}


def calculate_saude_progress(data: Optional[dict] = None) -> dict:
    """
    Calculate training progress metrics.

    Returns:
        dict with keys:
        - ciclo: int
        - semana: int
        - semana_tipo: str
        - progresso_ciclo: float (0-1, percentage of cycle completed)
        - proximo_treino: str (next lift)
        - proximo_treino_tipo: str ('lift' or 'cardio')
        - lifts_restantes: list[str]
        - lifts_completados: list[str]
        - titulo: str (display title)
        - subtitulo: str (display subtitle)
    """
    if data is None:
        data = parse_saude()

    ciclo = data['ciclo']
    semana = data['semana']
    semana_tipo = data['semana_tipo']
    ordem = data['ordem_lifts']
    completados = data['lifts_completados']

    # Calculate cycle progress (4 weeks per cycle, 4 lifts per week)
    # Total: 16 lift sessions per cycle
    # Current position: (semana-1)*4 + lifts_done_this_week
    lifts_done = len(completados)
    total_position = (semana - 1) * 4 + lifts_done
    progresso_ciclo = total_position / 16

    # Find next lift
    proximo = data.get('proximo_treino')
    if not proximo and completados:
        # Infer from completed lifts
        for lift in ordem:
            if lift not in completados:
                proximo = lift
                break

    # Calculate remaining lifts for the week
    lifts_restantes = [l for l in ordem if l not in completados]
    if proximo and proximo in lifts_restantes:
        # Move proximo to front
        lifts_restantes.remove(proximo)
        lifts_restantes.insert(0, proximo)

    # Check if next planned is cardio based on log
    # Find the next incomplete entry starting from today or after
    proximo_tipo = 'lift'
    hoje = date.today()

    for entry in data['log_semanal']:
        # Parse entry date (DD/MM format, assume current year)
        try:
            day, month = entry['data'].split('/')
            entry_date = date(hoje.year, int(month), int(day))
        except (ValueError, KeyError):
            continue

        # Skip past dates that weren't completed
        if entry_date < hoje and not entry['completou']:
            continue

        # Check this entry
        if not entry['completou'] and entry.get('treino'):
            treino = entry['treino']
            if 'Cardio' in treino or 'Metcon' in treino:
                proximo = treino
                proximo_tipo = 'cardio'
                break
            else:
                lift_match = treino.split()[0] if treino else None
                if lift_match and lift_match in ordem:
                    proximo = lift_match
                    proximo_tipo = 'lift'
                break

    # Format week type for display
    semana_display = {
        '5s': '5s',
        '3s': '3s',
        '1s': '1s',
        'deload': 'Deload',
    }.get(semana_tipo, semana_tipo)

    return {
        'ciclo': ciclo,
        'semana': semana,
        'semana_tipo': semana_tipo,
        'progresso_ciclo': progresso_ciclo,
        'proximo_treino': proximo,
        'proximo_treino_tipo': proximo_tipo,
        'lifts_restantes': lifts_restantes,
        'lifts_completados': completados,
        'titulo': '5/3/1 Prep & Fat Loss',
        'subtitulo': f'Ciclo {ciclo} | Semana {semana} ({semana_display})',
    }


def calculate_maconha_progress(data: Optional[dict] = None) -> dict:
    """
    Calculate reduction progress metrics.

    Returns:
        dict with keys:
        - fase: int
        - fase_padrao: str
        - progresso_fase: float (0-1)
        - dias_na_fase: int
        - dias_total_fase: int
        - streak: int (days without smoking)
        - proximo_permitido: date
        - proximo_permitido_str: str
        - hoje_permitido: bool
        - hoje_dia: str (weekday name)
        - titulo: str
        - subtitulo: str
    """
    if data is None:
        data = parse_maconha()

    hoje = date.today()
    hoje_dia = WEEKDAY_PT[hoje.weekday()]

    fase = data['fase_atual']
    padrao = data['fase_padrao']
    inicio = data['fase_inicio']
    fim = data['fase_fim']
    dias_permitidos = data['dias_permitidos']
    streak = data['streak']

    # Calculate phase progress
    dias_na_fase = 1
    dias_total_fase = 14  # 2 weeks default
    progresso_fase = 0.0

    if inicio and fim:
        dias_total_fase = (fim - inicio).days + 1
        dias_na_fase = (hoje - inicio).days + 1
        dias_na_fase = max(1, min(dias_na_fase, dias_total_fase))
        progresso_fase = dias_na_fase / dias_total_fase

    # Check if today is an allowed day
    hoje_permitido = hoje_dia in dias_permitidos

    # Find next allowed day
    proximo_permitido = None
    for i in range(1, 8):
        check_date = hoje + timedelta(days=i)
        check_dia = WEEKDAY_PT[check_date.weekday()]
        if check_dia in dias_permitidos:
            proximo_permitido = check_date
            break

    # If today is allowed and not yet passed (before 6pm), consider today
    if hoje_permitido:
        proximo_permitido = hoje

    proximo_str = ''
    if proximo_permitido:
        if proximo_permitido == hoje:
            proximo_str = 'Hoje!'
        else:
            dia_abbrev = WEEKDAY_ABBREV[proximo_permitido.weekday()]
            proximo_str = f'{dia_abbrev} {proximo_permitido.day:02d}/{proximo_permitido.month:02d}'

    return {
        'fase': fase,
        'fase_padrao': padrao,
        'progresso_fase': progresso_fase,
        'dias_na_fase': dias_na_fase,
        'dias_total_fase': dias_total_fase,
        'streak': streak,
        'proximo_permitido': proximo_permitido,
        'proximo_permitido_str': proximo_str,
        'hoje_permitido': hoje_permitido,
        'hoje_dia': hoje_dia,
        'titulo': f'Fase {fase} ({padrao})',
        'subtitulo': f'Dia {dias_na_fase} de {dias_total_fase} | Streak: {streak} dias sem fumar',
    }


def get_today_focus(saude: Optional[dict] = None, maconha: Optional[dict] = None) -> list[str]:
    """
    Get 3 focus items for today.

    Returns:
        list of 3 action items
    """
    if saude is None:
        saude = calculate_saude_progress()
    if maconha is None:
        maconha = calculate_maconha_progress()

    focus = []

    # Training focus
    proximo = saude.get('proximo_treino')
    if proximo:
        if saude.get('proximo_treino_tipo') == 'cardio':
            focus.append(f"Cardio: {proximo}")
        else:
            focus.append(f"Treino: {proximo} ({saude['semana_tipo']})")

    # Maconha focus
    if maconha['hoje_permitido']:
        focus.append("Hoje é dia permitido - aproveite se quiser")
    else:
        focus.append(f"Dia de resistir - próximo permitido: {maconha['proximo_permitido_str']}")

    # Add mobility/recovery focus
    focus.append("Mobilidade: 10-15 min (trapézio + cervical)")

    return focus[:3]


if __name__ == "__main__":
    print("=== SAÚDE PROGRESS ===")
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
