#!/usr/bin/env python3
"""
Daily Digest - Goals progress visualization.
Generates ASCII formatted progress report for personal goals.

Usage:
    python3 scripts/daily_digest.py           # Full ASCII output
    python3 scripts/daily_digest.py --json    # JSON output
    python3 scripts/daily_digest.py --short   # Compact output
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
from goals.ascii_charts import header_box, format_goal_section, checkmark


def generate_digest_json() -> dict:
    """Generate digest data as JSON-serializable dict."""
    saude_data = parse_saude()
    maconha_data = parse_maconha()

    saude_progress = calculate_saude_progress(saude_data)
    maconha_progress = calculate_maconha_progress(maconha_data)
    focus = get_today_focus(saude_progress, maconha_progress)

    return {
        'date': date.today().isoformat(),
        'saude': {
            'ciclo': saude_progress['ciclo'],
            'semana': saude_progress['semana'],
            'semana_tipo': saude_progress['semana_tipo'],
            'progresso': round(saude_progress['progresso_ciclo'], 2),
            'proximo_treino': saude_progress['proximo_treino'],
            'lifts_completados': saude_progress['lifts_completados'],
            'lifts_restantes': saude_progress['lifts_restantes'],
        },
        'maconha': {
            'fase': maconha_progress['fase'],
            'fase_padrao': maconha_progress['fase_padrao'],
            'progresso': round(maconha_progress['progresso_fase'], 2),
            'dias_na_fase': maconha_progress['dias_na_fase'],
            'dias_total_fase': maconha_progress['dias_total_fase'],
            'streak': maconha_progress['streak'],
            'hoje_permitido': maconha_progress['hoje_permitido'],
            'proximo_permitido': maconha_progress['proximo_permitido_str'],
        },
        'foco_do_dia': focus,
    }


def generate_digest_ascii() -> str:
    """Generate full ASCII formatted digest."""
    saude_data = parse_saude()
    maconha_data = parse_maconha()

    saude = calculate_saude_progress(saude_data)
    maconha = calculate_maconha_progress(maconha_data)
    focus = get_today_focus(saude, maconha)

    hoje = date.today()
    lines = []

    # Header
    lines.append(header_box("METAS DO DIA", hoje.strftime("%Y-%m-%d")))

    # Saude section
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

    lines.append(format_goal_section(
        f"TREINO - {saude['titulo']}",
        saude['subtitulo'],
        saude['progresso_ciclo'],
        saude_details
    ))

    # Maconha section
    hoje_status = "dia de resistir" if not maconha['hoje_permitido'] else "dia permitido"
    mark = checkmark(not maconha['hoje_permitido'])  # Checkmark for resistance days

    maconha_details = [
        f"Próximo permitido: {maconha['proximo_permitido_str']}",
        f"Hoje: {maconha['hoje_dia']} - {hoje_status} {mark if not maconha['hoje_permitido'] else ''}".strip(),
    ]

    lines.append(format_goal_section(
        f"MACONHA - {maconha['titulo']}",
        maconha['subtitulo'],
        maconha['progresso_fase'],
        maconha_details
    ))

    # Footer
    lines.append('')
    lines.append('═' * 44)

    return '\n'.join(lines)


def generate_digest_short() -> str:
    """Generate compact one-line summary."""
    saude = calculate_saude_progress()
    maconha = calculate_maconha_progress()

    treino_pct = int(saude['progresso_ciclo'] * 100)
    maconha_pct = int(maconha['progresso_fase'] * 100)

    return (
        f"Treino: C{saude['ciclo']}S{saude['semana']} ({treino_pct}%) | "
        f"Maconha: F{maconha['fase']} ({maconha_pct}%) streak:{maconha['streak']}d | "
        f"Próximo: {saude['proximo_treino']}"
    )


def main():
    parser = argparse.ArgumentParser(
        description='Generate daily goals digest',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 scripts/daily_digest.py           # Full ASCII output
    python3 scripts/daily_digest.py --json    # JSON for programmatic use
    python3 scripts/daily_digest.py --short   # One-line summary
        """
    )
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--short', action='store_true', help='Compact one-line output')

    args = parser.parse_args()

    try:
        if args.json:
            data = generate_digest_json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif args.short:
            print(generate_digest_short())
        else:
            print(generate_digest_ascii())
    except FileNotFoundError as e:
        print(f"Error: Could not find goals file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error generating digest: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
