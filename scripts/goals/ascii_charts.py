#!/usr/bin/env python3
"""
ASCII charts and formatting for goals display.
"""


def progress_bar(progress: float, width: int = 20, filled: str = '█', empty: str = '░') -> str:
    """
    Generate an ASCII progress bar.

    Args:
        progress: Float from 0.0 to 1.0
        width: Total width of the bar (excluding brackets)
        filled: Character for filled portion
        empty: Character for empty portion

    Returns:
        String like "[██████░░░░░░░░░░░░░░] 33%"
    """
    progress = max(0.0, min(1.0, progress))
    filled_width = int(progress * width)
    empty_width = width - filled_width

    bar = f"[{filled * filled_width}{empty * empty_width}]"
    percent = f"{int(progress * 100)}%"

    return f"{bar} {percent}"


def header_box(title: str, subtitle: str = '', width: int = 44) -> str:
    """
    Generate a header box with double-line borders.

    Args:
        title: Main title text
        subtitle: Optional subtitle (e.g., date)
        width: Total width of the box

    Returns:
        Multi-line string with box borders
    """
    top_border = '═' * width
    bottom_border = '═' * width

    lines = [top_border]

    # Center title
    title_line = title.center(width)
    lines.append(title_line)

    # Add subtitle if provided
    if subtitle:
        subtitle_line = subtitle.center(width)
        lines.append(subtitle_line)

    lines.append(bottom_border)

    return '\n'.join(lines)


def section_header(title: str, width: int = 36) -> str:
    """
    Generate a section header with single-line border.

    Args:
        title: Section title (e.g., "TREINO")
        width: Width of the separator line

    Returns:
        Multi-line string with title and separator
    """
    separator = '─' * width
    return f"{title}\n{separator}"


def format_goal_section(
    title: str,
    subtitle: str,
    progress: float,
    details: list[str],
    width: int = 36
) -> str:
    """
    Format a complete goal section.

    Args:
        title: Section title (e.g., "TREINO - 5/3/1 Prep & Fat Loss")
        subtitle: Status line (e.g., "Ciclo 1 | Semana 2 (3s)")
        progress: Progress value 0.0-1.0
        details: List of detail lines to display
        width: Width of separator line

    Returns:
        Multi-line formatted section
    """
    lines = [
        '',  # Empty line before section
        section_header(title, width),
        subtitle,
        progress_bar(progress),
        '',  # Empty line after progress bar
    ]

    for detail in details:
        lines.append(detail)

    return '\n'.join(lines)


def checkmark(condition: bool) -> str:
    """Return checkmark or X based on condition."""
    return '✓' if condition else '✗'


def format_list_items(items: list[str], prefix: str = '• ') -> str:
    """Format a list of items with bullet points."""
    return '\n'.join(f"{prefix}{item}" for item in items)


if __name__ == "__main__":
    from datetime import date

    # Demo output
    print(header_box("METAS DO DIA", date.today().strftime("%Y-%m-%d")))
    print()

    # Saude section
    saude_details = [
        "Próximo: Cardio (colete) - Qua 21/01",
        "Lifts restantes: Bench → Squat → OHP",
    ]
    print(format_goal_section(
        "TREINO - 5/3/1 Prep & Fat Loss",
        "Ciclo 1 | Semana 2 (3s)",
        0.33,
        saude_details
    ))
    print()

    # Maconha section
    maconha_details = [
        "Próximo permitido: Sex 23/01",
        f"Hoje: Segunda - dia de resistir {checkmark(True)}",
    ]
    print(format_goal_section(
        "MACONHA - Fase 1 (Sex-Sáb-Dom)",
        "Dia 2 de 14 | Streak: 3 dias sem fumar",
        0.14,
        maconha_details
    ))

    print()
    print(header_box("", ""))  # Just the borders
