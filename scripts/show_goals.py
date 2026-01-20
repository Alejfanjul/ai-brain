#!/usr/bin/env python3
"""
Show Goals - Quick CLI for viewing goal progress.

Usage:
    python3 scripts/show_goals.py           # Full view
    python3 scripts/show_goals.py --today   # Just today's focus
    python3 scripts/show_goals.py --saude   # Just training
    python3 scripts/show_goals.py --maconha # Just reduction
    python3 scripts/show_goals.py --json    # JSON output
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from goals.parser import parse_saude, parse_maconha
from goals.progress import calculate_saude_progress, calculate_maconha_progress, get_today_focus
from goals.ascii_charts import header_box, format_goal_section, checkmark, progress_bar


def show_saude(as_json: bool = False) -> None:
    """Display only training progress."""
    saude_data = parse_saude()
    saude = calculate_saude_progress(saude_data)
    hoje = date.today()

    if as_json:
        print(json.dumps({
            'ciclo': saude['ciclo'],
            'semana': saude['semana'],
            'semana_tipo': saude['semana_tipo'],
            'progresso': round(saude['progresso_ciclo'], 2),
            'proximo_treino': saude['proximo_treino'],
            'lifts_completados': saude['lifts_completados'],
            'lifts_restantes': saude['lifts_restantes'],
        }, indent=2, ensure_ascii=False))
        return

    lifts_restantes_str = ' → '.join(saude['lifts_restantes']) if saude['lifts_restantes'] else 'Semana completa!'

    # Determine next workout date from log
    proximo_data = ''
    for entry in saude_data.get('log_semanal', []):
        if not entry.get('completou', False) and entry.get('treino'):
            try:
                day, month = entry['data'].split('/')
                entry_date = date(hoje.year, int(month), int(day))
                if entry_date >= hoje:
                    weekday_abbrev = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'][entry_date.weekday()]
                    proximo_data = f" - {weekday_abbrev} {entry['data']}"
                    break
            except (ValueError, KeyError):
                continue

    saude_details = [
        f"Próximo: {saude['proximo_treino']}{proximo_data}",
        f"Lifts restantes: {lifts_restantes_str}",
    ]

    print(format_goal_section(
        f"TREINO - {saude['titulo']}",
        saude['subtitulo'],
        saude['progresso_ciclo'],
        saude_details
    ))


def show_maconha(as_json: bool = False) -> None:
    """Display only reduction progress."""
    maconha = calculate_maconha_progress()

    if as_json:
        print(json.dumps({
            'fase': maconha['fase'],
            'fase_padrao': maconha['fase_padrao'],
            'progresso': round(maconha['progresso_fase'], 2),
            'dias_na_fase': maconha['dias_na_fase'],
            'dias_total_fase': maconha['dias_total_fase'],
            'streak': maconha['streak'],
            'hoje_permitido': maconha['hoje_permitido'],
            'proximo_permitido': maconha['proximo_permitido_str'],
        }, indent=2, ensure_ascii=False))
        return

    hoje_status = "dia de resistir" if not maconha['hoje_permitido'] else "dia permitido"
    mark = checkmark(not maconha['hoje_permitido'])

    # Weekly usage stats
    week_start_str = maconha['week_start'].strftime('%d/%m')
    usados = maconha['usados_semana']
    max_dias = maconha['max_permitidos_semana']

    maconha_details = [
        f"Semana ({week_start_str}): {usados}/{max_dias} dias permitidos usados",
        f"Próximo permitido: {maconha['proximo_permitido_str']}",
        f"Hoje: {maconha['hoje_dia']} - {hoje_status} {mark if not maconha['hoje_permitido'] else ''}".strip(),
    ]

    print(format_goal_section(
        f"MACONHA - {maconha['titulo']}",
        maconha['subtitulo'],
        maconha['progresso_fase'],
        maconha_details
    ))


def show_today(as_json: bool = False) -> None:
    """Display only today's focus items."""
    saude = calculate_saude_progress()
    maconha = calculate_maconha_progress()
    focus = get_today_focus(saude, maconha)

    if as_json:
        print(json.dumps({
            'date': date.today().isoformat(),
            'foco_do_dia': focus,
        }, indent=2, ensure_ascii=False))
        return

    hoje = date.today()
    print(f"FOCO DO DIA - {hoje.strftime('%Y-%m-%d')}")
    print('─' * 36)
    for i, item in enumerate(focus, 1):
        print(f"{i}. {item}")


def show_all(as_json: bool = False) -> None:
    """Display full progress report."""
    if as_json:
        from daily_digest import generate_digest_json
        print(json.dumps(generate_digest_json(), indent=2, ensure_ascii=False))
        return

    from daily_digest import generate_digest_ascii
    print(generate_digest_ascii())


def main():
    parser = argparse.ArgumentParser(
        description='Show goals progress',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 scripts/show_goals.py           # Full view
    python3 scripts/show_goals.py --today   # Just today's focus
    python3 scripts/show_goals.py --saude   # Just training
    python3 scripts/show_goals.py --maconha # Just reduction
    python3 scripts/show_goals.py --json    # JSON output
        """
    )
    parser.add_argument('--today', '-t', action='store_true', help="Show only today's focus")
    parser.add_argument('--saude', '-s', action='store_true', help='Show only training progress')
    parser.add_argument('--maconha', '-m', action='store_true', help='Show only reduction progress')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    try:
        if args.today:
            show_today(args.json)
        elif args.saude:
            show_saude(args.json)
        elif args.maconha:
            show_maconha(args.json)
        else:
            show_all(args.json)
    except FileNotFoundError as e:
        print(f"Error: Could not find goals file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
