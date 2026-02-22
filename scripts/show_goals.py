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

    saude_details = [
        f"Próximo: {saude['proximo_treino']}",
        f"Lifts restantes: {lifts_restantes_str}",
    ]

    print(format_goal_section(
        f"TREINO - {saude['titulo']}",
        saude['subtitulo'],
        saude['progresso_ciclo'],
        saude_details
    ))


def show_maconha(as_json: bool = False) -> None:
    """Display usage reflection (Reflexivo model)."""
    maconha = calculate_maconha_progress()

    if as_json:
        print(json.dumps({
            'modelo': maconha['modelo'],
            'padrao_natural': maconha['padrao_natural'],
            'criterio': maconha['criterio'],
            'ultima_semana': maconha['ultima_semana'],
        }, indent=2, ensure_ascii=False))
        return

    ultima = maconha.get('ultima_semana', {})

    print(f"MACONHA - Reflexivo ({maconha['padrao_natural']})")
    print('─' * 36)
    if ultima:
        print(f"  {ultima.get('header', '')}")
        if ultima.get('uso'):
            print(f"  Uso: {ultima['uso']}")
        if ultima.get('impacto'):
            print(f"  Impacto: {ultima['impacto']}")
        if ultima.get('sentimento'):
            print(f"  Reflexão: {ultima['sentimento']}")
    else:
        print("  Sem registros recentes.")
    if maconha.get('criterio'):
        print(f"\n  Critério: {maconha['criterio']}")
    print()


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
