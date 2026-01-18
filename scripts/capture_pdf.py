#!/usr/bin/env python3
"""
PDF Capture Script
Extrai conteúdo de livros PDF e salva no ai-brain.

Uso:
    python3 scripts/capture_pdf.py <arquivo.pdf>
    python3 scripts/capture_pdf.py <arquivo.pdf> --author "Jim Wendler" --title "5/3/1 Forever"
"""

import sys
import re
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

try:
    import pypdf
except ImportError:
    print("❌ Biblioteca pypdf não encontrada.")
    print("   Instale com: pip install pypdf")
    sys.exit(1)

# Importa módulo de limpeza
sys.path.insert(0, str(Path(__file__).parent))
from content_cleaner import clean_content

SOURCES_DIR = Path(__file__).parent.parent / "sources"


def slugify(text):
    """Converte texto para slug (padrão do projeto)."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def extract_metadata(reader):
    """Extrai metadados do PDF."""
    metadata = reader.metadata or {}

    return {
        'title': metadata.get('/Title', '').strip() if metadata.get('/Title') else None,
        'author': metadata.get('/Author', '').strip() if metadata.get('/Author') else None,
        'subject': metadata.get('/Subject', '').strip() if metadata.get('/Subject') else None,
        'creator': metadata.get('/Creator', '').strip() if metadata.get('/Creator') else None,
        'pages': len(reader.pages),
    }


def extract_text(reader, verbose=True):
    """Extrai texto de todas as páginas do PDF."""
    pages_content = []
    total_pages = len(reader.pages)

    for i, page in enumerate(reader.pages):
        if verbose and (i + 1) % 50 == 0:
            print(f"   Processando página {i + 1}/{total_pages}...")

        text = page.extract_text() or ""

        # Limpa quebras de linha excessivas dentro de parágrafos
        # mas mantém quebras duplas (parágrafos)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        text = re.sub(r' +', ' ', text)

        if text.strip():
            pages_content.append(text.strip())

    return pages_content


def create_book_file(metadata, content):
    """Cria arquivo markdown do livro."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    author_slug = slugify(metadata['author'])
    title_slug = slugify(metadata['title'])

    filename = f"{date_str}-{author_slug}-{title_slug}.md"
    filepath = SOURCES_DIR / filename

    # Evita sobrescrever
    counter = 1
    while filepath.exists():
        filename = f"{date_str}-{author_slug}-{title_slug}-{counter}.md"
        filepath = SOURCES_DIR / filename
        counter += 1

    template = f"""# {metadata['title']}

## Fonte
- **Tipo:** livro
- **Autor:** {metadata['author']}
- **Páginas:** {metadata['pages']}
- **Data captura:** {date_str}

## Conteúdo

{content}

## Minhas Anotações

"""

    filepath.write_text(template, encoding='utf-8')
    print(f"✅ Criado: {filename}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description='Captura conteúdo de PDF para ai-brain')
    parser.add_argument('pdf_path', help='Caminho para o arquivo PDF')
    parser.add_argument('--author', '-a', help='Nome do autor (se não detectado automaticamente)')
    parser.add_argument('--title', '-t', help='Título do livro (se não detectado automaticamente)')
    parser.add_argument('--no-commit', action='store_true', help='Não fazer commit automático')
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)

    if not pdf_path.exists():
        print(f"❌ Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    if pdf_path.suffix.lower() != '.pdf':
        print("❌ Arquivo deve ter extensão .pdf")
        sys.exit(1)

    print(f"📖 Processando: {pdf_path.name}")

    # Lê PDF
    try:
        reader = pypdf.PdfReader(str(pdf_path))
    except Exception as e:
        print(f"❌ Erro ao ler PDF: {e}")
        sys.exit(1)

    # Extrai metadados
    metadata = extract_metadata(reader)

    # Usa argumentos se fornecidos, senão usa metadados do PDF
    if args.author:
        metadata['author'] = args.author
    if args.title:
        metadata['title'] = args.title

    # Se ainda não tiver autor/título, pergunta
    if not metadata['author']:
        metadata['author'] = input("Autor não detectado. Digite o nome do autor: ").strip()
    if not metadata['title']:
        metadata['title'] = input("Título não detectado. Digite o título: ").strip()

    print(f"\nLivro: {metadata['title']}")
    print(f"Autor: {metadata['author']}")
    print(f"Páginas: {metadata['pages']}")

    # Extrai texto
    print("\n📄 Extraindo conteúdo...")
    pages = extract_text(reader)
    print(f"✅ {len(pages)} páginas com conteúdo extraído")

    # Combina e limpa
    full_content = "\n\n".join(pages)
    full_content = clean_content(full_content)

    word_count = len(full_content.split())
    print(f"📊 ~{word_count:,} palavras")

    # Cria arquivo
    SOURCES_DIR.mkdir(exist_ok=True)
    filepath = create_book_file(metadata, full_content)

    # Git automation
    if not args.no_commit:
        print("\n📝 Fazendo commit...")
        subprocess.run(['git', 'add', str(filepath)], cwd=filepath.parent.parent)
        subprocess.run(['git', 'commit', '-m', f'capture: {metadata["title"]}'], cwd=filepath.parent.parent)
        print(f"\n💡 Para fazer push: git push")

    print(f"\n✅ Captura concluída!")
    print(f"   Arquivo: {filepath}")
    print(f"   Próximo passo: python3 scripts/embed_sources.py")


if __name__ == "__main__":
    main()
