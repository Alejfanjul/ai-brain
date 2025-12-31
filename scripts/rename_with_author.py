#!/usr/bin/env python3
"""
Script para renomear arquivos em sources/ adicionando o nome do autor.
Formato: YYYY-MM-DD-titulo.md → YYYY-MM-DD-autor-titulo.md
"""

import re
from pathlib import Path
import subprocess

def slugify(text):
    """Converte texto para slug (minúsculo, hífens)."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def extract_author(content):
    """Extrai o autor da seção de metadata."""
    match = re.search(r'\*\*Autor:\*\*\s*(.+)', content)
    if match:
        return match.group(1).strip()
    return None

def rename_files():
    """Renomeia todos os arquivos em sources/ adicionando o autor."""
    sources = Path("sources")

    if not sources.exists():
        print("❌ Diretório sources/ não encontrado")
        return

    renamed_count = 0
    skipped_count = 0
    error_count = 0

    for filepath in sorted(sources.glob("*.md")):
        try:
            content = filepath.read_text(encoding='utf-8')
            author = extract_author(content)

            if not author:
                print(f"⚠️  Sem autor: {filepath.name}")
                error_count += 1
                continue

            author_slug = slugify(author)

            # Verifica se já tem autor no nome
            if author_slug in filepath.name.lower():
                print(f"✓ Já tem autor: {filepath.name}")
                skipped_count += 1
                continue

            # Extrai data e resto do nome
            name = filepath.stem

            # Tenta match com data YYYY-MM-DD
            match = re.match(r'^(\d{4}-\d{2}-\d{2})-(.+)$', name)
            if match:
                date_part = match.group(1)
                title_part = match.group(2)
            else:
                # Tenta match com data YYYYMMDD
                match = re.match(r'^(\d{8})-(.+)$', name)
                if match:
                    date_part = match.group(1)
                    title_part = match.group(2)
                else:
                    print(f"⚠️  Formato não reconhecido: {filepath.name}")
                    error_count += 1
                    continue

            new_name = f"{date_part}-{author_slug}-{title_part}.md"
            new_path = sources / new_name

            print(f"📝 Renomeando: {filepath.name}")
            print(f"   → {new_name}")

            # Usa git mv para manter histórico
            result = subprocess.run(
                ['git', 'mv', str(filepath), str(new_path)],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"   ❌ Erro: {result.stderr}")
                error_count += 1
            else:
                renamed_count += 1

        except Exception as e:
            print(f"❌ Erro ao processar {filepath.name}: {e}")
            error_count += 1

    print("\n" + "="*60)
    print(f"✅ Renomeados: {renamed_count}")
    print(f"⏭️  Já tinham autor: {skipped_count}")
    print(f"❌ Erros/Sem autor: {error_count}")
    print("="*60)

    return renamed_count

if __name__ == "__main__":
    renamed = rename_files()

    if renamed > 0:
        print("\n📝 Fazendo commit das alterações...")
        subprocess.run(['git', 'status', '--short'])
    else:
        print("\n✓ Nenhum arquivo foi renomeado")
