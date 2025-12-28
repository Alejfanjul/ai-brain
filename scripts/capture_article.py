#!/usr/bin/env python3
"""
Captura artigo de qualquer URL.
Uso: python3 scripts/capture_article.py <URL>
"""

import sys
import re
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urlparse

SOURCES_DIR = Path("sources")


def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def extract_content(url):
    """Extrai conteúdo principal de uma URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, timeout=30, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrai título
    title = None
    if soup.find('h1'):
        title = soup.find('h1').get_text().strip()
    elif soup.find('title'):
        title = soup.find('title').get_text().strip()

    # Extrai autor (tenta várias formas)
    author = None
    author_meta = soup.find('meta', {'name': 'author'})
    if author_meta:
        author = author_meta.get('content')

    # Tenta extrair do domínio se não encontrou
    if not author:
        domain = urlparse(url).netloc.replace('www.', '')
        author = domain

    # Extrai conteúdo principal
    content = None

    # Seletores comuns para conteúdo principal
    selectors = [
        'article',
        '.post-content',
        '.entry-content',
        '.article-content',
        '.content',
        'main',
        '.post-body',
        '#content'
    ]

    for selector in selectors:
        content = soup.select_one(selector)
        if content:
            break

    # Fallback: pega o body inteiro
    if not content:
        content = soup.find('body')

    if content:
        # Remove elementos indesejados
        for tag in content.select('script, style, nav, footer, header, aside, .comments, .sidebar, .advertisement'):
            tag.decompose()

        # Converte para markdown
        markdown = md(str(content), heading_style="ATX")

        # Limpa linhas em branco excessivas
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        return {
            'title': title or 'Sem título',
            'author': author,
            'content': markdown.strip()
        }

    return None


def create_capture_file(data, url):
    """Cria arquivo de captura."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(data['title'])
    filename = f"{date_str}-{slug}.md"
    filepath = SOURCES_DIR / filename

    # Evita sobrescrever
    counter = 1
    while filepath.exists():
        filename = f"{date_str}-{slug}-{counter}.md"
        filepath = SOURCES_DIR / filename
        counter += 1

    template = f"""# {data['title']}

## Fonte
- **Tipo:** artigo
- **Autor:** {data['author']}
- **URL:** {url}
- **Data original:** {date_str}
- **Data captura:** {date_str}

## Conteúdo

{data['content']}

## Minhas Anotações

"""

    filepath.write_text(template, encoding='utf-8')
    return filepath


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 scripts/capture_article.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"=== Captura Artigo ===")
    print(f"URL: {url}")

    SOURCES_DIR.mkdir(exist_ok=True)

    print("Extraindo conteúdo...")
    data = extract_content(url)

    if not data:
        print("❌ Erro: não foi possível extrair conteúdo")
        sys.exit(1)

    print(f"Título: {data['title']}")
    print(f"Autor: {data['author']}")
    print(f"Conteúdo: {len(data['content'])} caracteres")

    filepath = create_capture_file(data, url)
    print(f"✅ Criado: {filepath}")

    # Git commit
    import subprocess
    subprocess.run(['git', 'add', str(filepath)])
    subprocess.run(['git', 'commit', '-m', f'capture: {data["title"][:50]}'])
    print("✅ Commit feito")

    # Git push
    subprocess.run(['git', 'push'])
    print("✅ Push feito")


if __name__ == "__main__":
    main()
