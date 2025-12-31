#!/usr/bin/env python3
"""
Captura conteúdo de curso (transcript colado).
Uso: python3 scripts/capture_course.py
"""

import subprocess
import re
from datetime import datetime
from pathlib import Path

SOURCES_DIR = Path("sources")


def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def get_input(prompt, required=True):
    """Pega input do usuário."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("Este campo é obrigatório.")


def get_multiline_input(prompt):
    """Pega input de múltiplas linhas."""
    print(prompt)
    print("(Cole o conteúdo e pressione Enter duas vezes para finalizar)")
    print("-" * 40)

    lines = []
    empty_count = 0

    while True:
        try:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append("")
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break

    return "\n".join(lines).strip()


def create_capture_file(course_name, author, platform, section_num, section_title, content):
    """Cria arquivo de captura."""
    date_str = datetime.now().strftime('%Y-%m-%d')

    author_slug = slugify(author)
    course_slug = slugify(course_name)
    section_slug = slugify(section_title)

    filename = f"{date_str}-{author_slug}-{course_slug}-s{section_num}-{section_slug}.md"
    filepath = SOURCES_DIR / filename

    counter = 1
    while filepath.exists():
        filename = f"{date_str}-{author_slug}-{course_slug}-s{section_num}-{section_slug}-{counter}.md"
        filepath = SOURCES_DIR / filename
        counter += 1

    template = f"""# {course_name} - Seção {section_num}: {section_title}

## Fonte
- **Tipo:** curso
- **Autor:** {author}
- **Plataforma:** {platform}
- **Seção:** {section_num}
- **Data captura:** {date_str}

## Conteúdo

{content}

## Minhas Anotações

"""

    filepath.write_text(template, encoding='utf-8')
    return filepath


def main():
    print("=" * 50)
    print("CAPTURA DE CURSO")
    print("=" * 50)
    print()

    SOURCES_DIR.mkdir(exist_ok=True)

    course_name = get_input("Nome do curso: ")
    author = get_input("Autor/Instrutor: ")
    platform = get_input("Plataforma (Udemy, Coursera, etc): ")
    section_num = get_input("Número da seção: ")
    section_title = get_input("Título da seção: ")

    print()
    content = get_multiline_input("Transcript/Conteúdo da seção:")

    if not content:
        print("❌ Nenhum conteúdo fornecido")
        return

    filepath = create_capture_file(
        course_name=course_name,
        author=author,
        platform=platform,
        section_num=section_num,
        section_title=section_title,
        content=content
    )

    print()
    print(f"✅ Arquivo criado: {filepath}")
    print(f"   Tamanho: {len(content)} caracteres")

    subprocess.run(['git', 'add', str(filepath)])
    commit_msg = f"capture: {course_name} - S{section_num}"
    subprocess.run(['git', 'commit', '-m', commit_msg])
    print(f"✅ Commit: {commit_msg}")

    print()
    again = input("Capturar outra seção? (s/n): ").strip().lower()
    if again == 's':
        main()


if __name__ == "__main__":
    main()
