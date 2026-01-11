#!/usr/bin/env python3
"""
EPUB Capture Script
Extrai conteúdo de livros EPUB e salva no ai-brain.
"""

import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Importa módulo de limpeza
sys.path.insert(0, str(Path(__file__).parent))
from content_cleaner import clean_content

SOURCES_DIR = Path("sources")

def slugify(text):
    """Converte texto para slug (padrão do projeto)."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]

def extract_metadata(book):
    """Extrai metadados do EPUB."""
    metadata = {
        'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Sem título',
        'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Autor desconhecido',
        'publisher': book.get_metadata('DC', 'publisher')[0][0] if book.get_metadata('DC', 'publisher') else 'N/A',
        'date': book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else 'N/A',
        'language': book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else 'N/A',
        'isbn': book.get_metadata('DC', 'identifier')[0][0] if book.get_metadata('DC', 'identifier') else 'N/A',
    }
    return metadata

def extract_chapters(book):
    """Extrai capítulos do EPUB."""
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')

            # Remove elementos indesejados
            for tag in soup.select('script, style, nav, header, footer'):
                tag.decompose()

            # Converte para markdown
            markdown_content = md(str(soup), heading_style="ATX", strip=['script', 'style'])

            # Limpa excesso de quebras de linha
            markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)

            # Limpa links internos de EPUB e outros elementos sem valor semântico
            markdown_content = clean_content(markdown_content)

            if markdown_content.strip():
                chapters.append({
                    'filename': item.get_name(),
                    'content': markdown_content.strip()
                })

    return chapters

def create_book_file(metadata, content, mode='full'):
    """Cria arquivo markdown do livro."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    author_slug = slugify(metadata['author'])
    title_slug = slugify(metadata['title'])

    # Base filename
    filename = f"{date_str}-{author_slug}-{title_slug}.md"
    filepath = SOURCES_DIR / filename

    # Evita sobrescrever
    counter = 1
    while filepath.exists():
        filename = f"{date_str}-{author_slug}-{title_slug}-{counter}.md"
        filepath = SOURCES_DIR / filename
        counter += 1

    # Template do projeto
    template = f"""# {metadata['title']}

## Fonte
- **Tipo:** livro
- **Autor:** {metadata['author']}
- **Editora:** {metadata['publisher']}
- **Data publicação:** {metadata['date']}
- **ISBN:** {metadata['isbn']}
- **Idioma:** {metadata['language']}
- **Data captura:** {date_str}

## Conteúdo

{content}

## Minhas Anotações

"""

    filepath.write_text(template, encoding='utf-8')
    print(f"✅ Criado: {filename}")
    return filepath

def main():
    """Função principal."""
    if len(sys.argv) < 2:
        print("Uso: python3 capture_epub.py <caminho-para-arquivo.epub>")
        sys.exit(1)

    epub_path = Path(sys.argv[1])

    if not epub_path.exists():
        print(f"❌ Arquivo não encontrado: {epub_path}")
        sys.exit(1)

    if epub_path.suffix.lower() != '.epub':
        print("❌ Arquivo deve ter extensão .epub")
        sys.exit(1)

    print(f"📖 Processando: {epub_path.name}")

    # Lê EPUB
    try:
        book = epub.read_epub(str(epub_path))
    except Exception as e:
        print(f"❌ Erro ao ler EPUB: {e}")
        sys.exit(1)

    # Extrai metadata
    metadata = extract_metadata(book)
    print(f"\nLivro: {metadata['title']}")
    print(f"Autor: {metadata['author']}")

    # Extrai capítulos
    print("\n📄 Extraindo conteúdo...")
    chapters = extract_chapters(book)
    print(f"✅ {len(chapters)} seções encontradas")

    # Combina todo o conteúdo
    full_content = "\n\n---\n\n".join([ch['content'] for ch in chapters])

    # Cria arquivo
    SOURCES_DIR.mkdir(exist_ok=True)
    filepath = create_book_file(metadata, full_content)

    # Git automation
    print("\n📝 Fazendo commit...")
    subprocess.run(['git', 'add', str(filepath)])
    subprocess.run(['git', 'commit', '-m', f'capture: {metadata["title"]}'])

    print(f"\n✅ Captura concluída: {filepath}")
    print(f"\n💡 Para fazer push: git push")

if __name__ == "__main__":
    main()
