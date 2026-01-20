#!/usr/bin/env python3
"""
Fitness Coach - Personal fitness tracking dashboard.

Usage:
    python3 coach.py                    # Show dashboard
    python3 coach.py log-weight 81.5    # Log weight
    python3 coach.py log-weight 81.5 22 # Log weight + body fat %
    python3 coach.py log-cardio "5km 31min corrida"
    python3 coach.py log-metcon "AMRAP 15min burpees"
    python3 coach.py --json             # JSON output
"""

import argparse
import csv
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
WEIGHT_FILE = DATA_DIR / "weight.csv"
CARDIO_FILE = DATA_DIR / "cardio.csv"
WENDLER_FILE = DATA_DIR / "wendler.csv"


def parse_weight_data() -> list[dict]:
    """Parse weight.csv and return list of entries."""
    entries = []
    if not WEIGHT_FILE.exists():
        return entries

    with open(WEIGHT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('date', '').startswith('#'):
                continue
            try:
                entry = {
                    'date': datetime.strptime(row['date'], '%Y-%m-%d').date(),
                    'weight': float(row['weight_kg']) if row.get('weight_kg') else None,
                    'body_fat': float(row['body_fat_pct']) if row.get('body_fat_pct') else None,
                }
                if entry['weight']:
                    entries.append(entry)
            except (ValueError, KeyError):
                continue

    return sorted(entries, key=lambda x: x['date'])


def parse_cardio_data() -> list[dict]:
    """Parse cardio.csv and return list of entries."""
    entries = []
    if not CARDIO_FILE.exists():
        return entries

    with open(CARDIO_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('date', '').startswith('#'):
                continue
            try:
                entry = {
                    'date': datetime.strptime(row['date'], '%Y-%m-%d').date(),
                    'type': row.get('type', 'cardio'),
                    'duration': int(row['duration_min']) if row.get('duration_min') else 0,
                    'distance': float(row['distance_km']) if row.get('distance_km') else None,
                    'description': row.get('description', ''),
                }
                entries.append(entry)
            except (ValueError, KeyError):
                continue

    return sorted(entries, key=lambda x: x['date'])


def parse_wendler_data() -> list[dict]:
    """Parse wendler.csv (Five3One export) and return list of entries."""
    entries = []
    if not WENDLER_FILE.exists():
        return entries

    with open(WENDLER_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Find header row (starts with "Ciclo#")
    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0] == 'Ciclo#':
            header_idx = i
            break

    if header_idx is None:
        return entries

    # Parse data rows
    for row in rows[header_idx + 1:]:
        if len(row) < 6:
            continue
        try:
            date_str = row[5]
            if not date_str or date_str == ' ':
                continue
            entry = {
                'cycle': int(row[0]) if row[0] else 0,
                'week': int(row[1]) if row[1] else 0,
                'lift': row[2],
                'tm': float(row[3]) if row[3] else 0,
                'real': float(row[4]) if row[4] else 0,
                'date': datetime.strptime(date_str, '%Y-%m-%d').date(),
            }
            entries.append(entry)
        except (ValueError, IndexError):
            continue

    return sorted(entries, key=lambda x: x['date'])


def calculate_weight_stats(entries: list[dict]) -> dict:
    """Calculate weight statistics."""
    if not entries:
        return {'current': None, 'avg_7d': None, 'trend': None}

    hoje = date.today()
    last_7_days = [e for e in entries if (hoje - e['date']).days <= 7]
    last_14_days = [e for e in entries if 7 < (hoje - e['date']).days <= 14]

    current = entries[-1]['weight'] if entries else None
    avg_7d = sum(e['weight'] for e in last_7_days) / len(last_7_days) if last_7_days else None
    avg_prev = sum(e['weight'] for e in last_14_days) / len(last_14_days) if last_14_days else None

    trend = None
    if avg_7d and avg_prev:
        diff = avg_7d - avg_prev
        if diff > 0.3:
            trend = 'subindo'
        elif diff < -0.3:
            trend = 'descendo'
        else:
            trend = 'estável'

    return {
        'current': current,
        'current_date': entries[-1]['date'] if entries else None,
        'avg_7d': avg_7d,
        'avg_prev_7d': avg_prev,
        'trend': trend,
    }


def get_week_start(d: date) -> date:
    """Get the Sunday that starts the week containing date d."""
    # weekday(): Monday=0, Sunday=6
    # We want Sunday as start, so we go back (weekday + 1) % 7 days
    days_since_sunday = (d.weekday() + 1) % 7
    return d - timedelta(days=days_since_sunday)


def calculate_cardio_stats(entries: list[dict]) -> dict:
    """Calculate cardio statistics."""
    hoje = date.today()
    week_start = get_week_start(hoje)

    this_week = [e for e in entries if e['date'] >= week_start]
    last_30_days = [e for e in entries if (hoje - e['date']).days <= 30]

    runs_week = [e for e in this_week if e['type'] == 'corrida']
    metcons_week = [e for e in this_week if e['type'] == 'metcon']

    total_km_week = sum(e['distance'] or 0 for e in runs_week)
    total_min_week = sum(e['duration'] for e in this_week)

    # Frequency last 30 days
    runs_30d = len([e for e in last_30_days if e['type'] == 'corrida'])
    metcons_30d = len([e for e in last_30_days if e['type'] == 'metcon'])

    return {
        'runs_week': len(runs_week),
        'metcons_week': len(metcons_week),
        'total_km_week': total_km_week,
        'total_min_week': total_min_week,
        'runs_30d': runs_30d,
        'metcons_30d': metcons_30d,
        'last_cardio': entries[-1] if entries else None,
        'week_start': week_start,
    }


def calculate_wendler_stats(entries: list[dict]) -> dict:
    """Calculate Wendler training statistics."""
    hoje = date.today()
    week_start = get_week_start(hoje)

    this_week = [e for e in entries if e['date'] >= week_start]
    last_30_days = [e for e in entries if (hoje - e['date']).days <= 30]

    # Current cycle/week (from most recent entry)
    current = entries[-1] if entries else None

    # Lifts this week
    lifts_week = list(set(e['lift'] for e in this_week))
    lifts_30d = len(last_30_days)

    # Last lift
    last_lift = entries[-1] if entries else None

    return {
        'current_cycle': current['cycle'] if current else None,
        'current_week': current['week'] if current else None,
        'lifts_week': lifts_week,
        'lifts_30d': lifts_30d,
        'last_lift': last_lift,
        'week_start': week_start,
    }


def progress_bar(value: float, max_value: float, width: int = 20) -> str:
    """Generate ASCII progress bar."""
    if max_value == 0:
        return '[' + '░' * width + ']'

    ratio = min(1.0, value / max_value)
    filled = int(ratio * width)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}]"


def format_dashboard() -> str:
    """Generate ASCII dashboard."""
    weight_data = parse_weight_data()
    cardio_data = parse_cardio_data()
    wendler_data = parse_wendler_data()

    weight = calculate_weight_stats(weight_data)
    cardio = calculate_cardio_stats(cardio_data)
    wendler = calculate_wendler_stats(wendler_data)

    hoje = date.today()
    lines = []

    # Header
    lines.append('═' * 44)
    lines.append('FITNESS COACH'.center(44))
    lines.append(hoje.strftime('%Y-%m-%d').center(44))
    lines.append('═' * 44)

    # Weight section
    lines.append('')
    lines.append('PESO')
    lines.append('─' * 36)

    if weight['current']:
        lines.append(f"Atual: {weight['current']:.1f}kg ({weight['current_date']})")
        if weight['avg_7d']:
            lines.append(f"Média 7 dias: {weight['avg_7d']:.1f}kg")
        if weight['trend']:
            trend_icon = {'subindo': '↑', 'descendo': '↓', 'estável': '→'}.get(weight['trend'], '?')
            lines.append(f"Tendência: {trend_icon} {weight['trend']}")
    else:
        lines.append("Sem dados de peso")
        lines.append("→ python3 coach.py log-weight 81.5")

    # Cardio section
    week_start_str = cardio['week_start'].strftime('%d/%m') if cardio.get('week_start') else ''
    lines.append('')
    lines.append(f'CARDIO (semana de {week_start_str})')
    lines.append('─' * 36)

    lines.append(f"Corridas: {cardio['runs_week']}x | Metcons: {cardio['metcons_week']}x")
    if cardio['total_km_week']:
        lines.append(f"Total: {cardio['total_km_week']:.1f}km em {cardio['total_min_week']}min")

    # Progress bar: target 2-3 cardio sessions per week
    cardio_total = cardio['runs_week'] + cardio['metcons_week']
    lines.append(f"Meta semanal: {progress_bar(cardio_total, 2)} {cardio_total}/2-3")

    if cardio['last_cardio']:
        last = cardio['last_cardio']
        lines.append(f"Último: {last['date']} - {last['description']}")

    # Wendler section
    lines.append('')
    lines.append(f'WENDLER (semana de {week_start_str})')
    lines.append('─' * 36)

    if wendler['lifts_week']:
        lifts_str = ', '.join(wendler['lifts_week'])
        lines.append(f"Lifts: {lifts_str}")
        lines.append(f"Meta semanal: {progress_bar(len(wendler['lifts_week']), 3)} {len(wendler['lifts_week'])}/3")
    else:
        lines.append("Nenhum lift esta semana")

    if wendler['last_lift']:
        last = wendler['last_lift']
        lines.append(f"Último: {last['date']} - {last['lift']} ({last['real']:.0f}kg)")

    # Footer
    lines.append('')
    lines.append('═' * 44)

    return '\n'.join(lines)


def log_weight(weight: float, body_fat: float = None):
    """Log weight entry to CSV."""
    hoje = date.today().isoformat()

    # Read existing entries
    existing = []
    if WEIGHT_FILE.exists():
        with open(WEIGHT_FILE, 'r') as f:
            existing = f.readlines()

    # Check if header exists
    has_header = any('date,weight' in line for line in existing)

    with open(WEIGHT_FILE, 'a') as f:
        if not has_header:
            f.write('date,weight_kg,body_fat_pct,notes\n')

        bf_str = f'{body_fat}' if body_fat else ''
        f.write(f'{hoje},{weight},{bf_str},\n')

    print(f"Registrado: {hoje} | Peso: {weight}kg" + (f" | Gordura: {body_fat}%" if body_fat else ""))


def log_cardio(description: str, cardio_type: str = 'corrida'):
    """Log cardio entry to CSV."""
    hoje = date.today().isoformat()

    # Try to parse duration and distance from description
    duration = 0
    distance = None

    # Match patterns like "5km 31min" or "31min 5km"
    km_match = re.search(r'(\d+(?:\.\d+)?)\s*km', description, re.IGNORECASE)
    min_match = re.search(r'(\d+)\s*min', description, re.IGNORECASE)

    if km_match:
        distance = float(km_match.group(1))
    if min_match:
        duration = int(min_match.group(1))

    with open(CARDIO_FILE, 'a') as f:
        dist_str = f'{distance}' if distance else ''
        f.write(f'{hoje},{cardio_type},{duration},{dist_str},{description},\n')

    print(f"Registrado: {hoje} | {cardio_type.title()}: {description}")


def main():
    parser = argparse.ArgumentParser(
        description='Fitness Coach - Personal tracking dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('command', nargs='?', default='dashboard',
                        help='Command: dashboard, log-weight, log-cardio, log-metcon')
    parser.add_argument('args', nargs='*', help='Command arguments')
    parser.add_argument('--json', action='store_true', help='JSON output')

    args = parser.parse_args()

    if args.command == 'dashboard' or args.command is None:
        print(format_dashboard())

    elif args.command == 'log-weight':
        if not args.args:
            print("Uso: python3 coach.py log-weight <peso> [gordura%]")
            sys.exit(1)
        weight = float(args.args[0])
        body_fat = float(args.args[1]) if len(args.args) > 1 else None
        log_weight(weight, body_fat)

    elif args.command == 'log-cardio':
        if not args.args:
            print("Uso: python3 coach.py log-cardio \"5km 31min corrida\"")
            sys.exit(1)
        log_cardio(' '.join(args.args), 'corrida')

    elif args.command == 'log-metcon':
        if not args.args:
            print("Uso: python3 coach.py log-metcon \"AMRAP 15min burpees\"")
            sys.exit(1)
        log_cardio(' '.join(args.args), 'metcon')

    else:
        print(f"Comando desconhecido: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
