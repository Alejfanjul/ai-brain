#!/usr/bin/env python3
"""
RSS Capture Script
Checa feeds RSS e captura posts novos para o ai-brain.
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime, timedelta
from pathlib import Path
import re
import json

# Configuração dos feeds
FEEDS = [
    {
        "name": "Nate",
        "url": "https://natesnewsletter.substack.com/feed",
        "type": "newsletter",
        "author": "Nate"
    },
    {
        "name": "Seth Godin",
        "url": "https://seths.blog/feed/",
        "type": "blog",
        "author": "Seth Godin"
    }
]

SOURCES_DIR = Path("sources")
STATE_FILE = Path(".github/captured_urls.json")


def load_captured_urls():
    """Carrega URLs já capturadas."""
    if STATE_FILE.exists():
        return set(json.loads(STATE_FILE.read_text()))
    return set()


def save_captured_urls(urls):
    """Salva URLs capturadas."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(list(urls), indent=2))


def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def extract_content(url):
    """Extrai conteúdo principal de uma URL."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tenta diferentes seletores para o conteúdo principal
        content = None
        
        # Substack
        if 'substack.com' in url:
            content = soup.select_one('.body.markup, .post-content, article')
        
        # Seth's blog
        elif 'seths.blog' in url:
            content = soup.select_one('.post-content, article, .entry-content')
        
        # Fallback genérico
        if not content:
            content = soup.select_one('article, .post-content, .entry-content, main')
        
        if content:
            # Remove scripts, styles, nav
            for tag in content.select('script, style, nav, footer, .comments'):
                tag.decompose()
            
            # Converte para markdown
            return md(str(content), heading_style="ATX")
        
        return None
    except Exception as e:
        print(f"Erro ao extrair {url}: {e}")
        return None


def create_capture_file(entry, feed_config, content):
    """Cria arquivo de captura."""
    # Parse da data
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        date = datetime(*entry.published_parsed[:6])
    else:
        date = datetime.now()
    
    date_str = date.strftime('%Y-%m-%d')
    title = entry.get('title', 'Sem título')
    slug = slugify(title)
    
    filename = f"{date_str}-{slug}.md"
    filepath = SOURCES_DIR / filename
    
    # Evita sobrescrever
    if filepath.exists():
        return None
    
    template = f"""# {title}

## Fonte
- **Tipo:** {feed_config['type']}
- **Autor:** {feed_config['author']}
- **URL:** {entry.get('link', 'N/A')}
- **Data original:** {date_str}
- **Data captura:** {datetime.now().strftime('%Y-%m-%d')}

## Conteúdo

{content}

## Minhas Anotações

"""
    
    filepath.write_text(template, encoding='utf-8')
    print(f"Criado: {filename}")
    return filepath


def process_feed(feed_config, captured_urls):
    """Processa um feed RSS."""
    print(f"\nProcessando: {feed_config['name']}")
    
    feed = feedparser.parse(feed_config['url'])
    new_captures = []
    
    # Pega posts das últimas 48 horas (margem de segurança)
    cutoff = datetime.now() - timedelta(hours=48)
    
    for entry in feed.entries[:10]:  # Limita a 10 mais recentes
        url = entry.get('link', '')
        
        if not url or url in captured_urls:
            continue
        
        # Checa data do post
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            entry_date = datetime(*entry.published_parsed[:6])
            if entry_date < cutoff:
                continue
        
        print(f"  Novo post: {entry.get('title', 'Sem título')[:50]}...")
        
        content = extract_content(url)
        if content:
            filepath = create_capture_file(entry, feed_config, content)
            if filepath:
                captured_urls.add(url)
                new_captures.append(filepath)
    
    return new_captures


def main():
    """Função principal."""
    print("=== RSS Capture ===")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    SOURCES_DIR.mkdir(exist_ok=True)
    captured_urls = load_captured_urls()
    
    all_captures = []
    for feed_config in FEEDS:
        captures = process_feed(feed_config, captured_urls)
        all_captures.extend(captures)
    
    save_captured_urls(captured_urls)
    
    print(f"\n=== Resumo ===")
    print(f"Total de novos posts capturados: {len(all_captures)}")
    
    return len(all_captures)


if __name__ == "__main__":
    main()
