---
name: DailyGoals
description: Show personal goals progress (training and habits). USE WHEN user asks about goals, progress, metas, treino, maconha, streak, workout, fitness OR /goals OR /metas.
---

# DailyGoals

Displays progress on personal goals with ASCII visualizations.

## Goals Tracked

1. **TREINO** - Wendler 5/3/1 strength program (cycles, weeks, lifts)
2. **MACONHA** - Reduction plan by phases (streak, allowed days)

## Usage

**Full progress report:**
```bash
python3 ~/ai-brain/scripts/show_goals.py
```

**Today's focus only:**
```bash
python3 ~/ai-brain/scripts/show_goals.py --today
```

**Just training:**
```bash
python3 ~/ai-brain/scripts/show_goals.py --saude
```

**Just reduction:**
```bash
python3 ~/ai-brain/scripts/show_goals.py --maconha
```

**JSON output (for programmatic use):**
```bash
python3 ~/ai-brain/scripts/show_goals.py --json
```

## What to Show

When user asks about goals/progress, run the appropriate command and present the output.

**Example interactions:**

- "Como estão minhas metas?" → Run `show_goals.py` (full report)
- "Qual é o foco de hoje?" → Run `show_goals.py --today`
- "Quantos dias de streak?" → Run `show_goals.py --maconha`
- "Próximo treino?" → Run `show_goals.py --saude`
- "/goals" → Run `show_goals.py` (full report)
- "/metas" → Run `show_goals.py` (full report)

## Output Example

```
════════════════════════════════════════════
                METAS DO DIA
                 2026-01-20
════════════════════════════════════════════

TREINO - 5/3/1 Prep & Fat Loss
────────────────────────────────────
Ciclo 1 | Semana 2 (3s)
[██████░░░░░░░░░░░░░░] 31%

Próximo: Cardio (colete) - Qua 21/01
Lifts restantes: Bench → Squat → OHP

MACONHA - Fase 1 (Sex-Sáb-Dom)
────────────────────────────────────
Dia 1 de 14 | Streak: 3 dias sem fumar
[█░░░░░░░░░░░░░░░░░░░] 7%

Próximo permitido: Sex 23/01
Hoje: Terça - dia de resistir ✓

════════════════════════════════════════════
```

## Data Sources

- `projects/ai-brain/metas/SAUDE.md` - Training data
- `projects/ai-brain/metas/MACONHA.md` - Reduction data

## Related Commands

- `python3 scripts/daily_digest.py` - Alternative entry point (same output)
- `python3 scripts/daily_digest.py --short` - One-line summary
