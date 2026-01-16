# Capture Article

Extrai conteúdo de artigos web e salva em sources/.

## Usage

```
/capture article <url>
```

## What it does

1. Faz fetch da URL fornecida
2. Extrai conteúdo principal do artigo
3. Detecta autor e tipo baseado no domínio
4. Cria arquivo em `sources/` usando o template padrão
5. Faz git commit automaticamente com mensagem "capture: [título]"

## Supported Sources

- seths.blog (Seth Godin)
- *.substack.com (newsletters como Nate's Newsletter)
- Artigos gerais (tenta extrair conteúdo principal)

## Implementation

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

def slugify(text):
    """Converte texto para slug (lowercase, hífens)"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def detect_source_info(url):
    """Detecta autor e tipo baseado no domínio"""
    domain = urlparse(url).netloc
    
    # Mapeamento de domínios conhecidos
    sources = {
        'seths.blog': {'author': 'Seth Godin', 'type': 'blog'},
        'natesnewsletter.substack.com': {'author': 'Nate', 'type': 'newsletter'},
        'every.to': {'author': 'Dan Shipper', 'type': 'newsletter'},
    }
    
    # Verificar match exato
    if domain in sources:
        return sources[domain]
    
    # Verificar substack genérico
    if 'substack.com' in domain:
        author = domain.split('.')[0].capitalize()
        return {'author': author, 'type': 'newsletter'}
    
    # Padrão para artigos desconhecidos
    return {'author': 'Unknown', 'type': 'artigo'}

def extract_article_content(url):
    """Extrai conteúdo do artigo"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Tentar extrair título
    title = None
    if soup.find('h1'):
        title = soup.find('h1').get_text().strip()
    elif soup.find('title'):
        title = soup.find('title').get_text().strip()
    else:
        title = "Untitled Article"
    
    # Tentar extrair data de publicação
    pub_date = None
    date_meta = soup.find('meta', property='article:published_time')
    if date_meta:
        pub_date = date_meta.get('content', '')[:10]  # YYYY-MM-DD
    
    # Tentar extrair conteúdo principal
    content = None
    
    # Para Substack
    article_div = soup.find('div', class_='available-content')
    if article_div:
        content = article_div.get_text(separator='\n\n').strip()
    
    # Para Seth's Blog
    if not content:
        entry_div = soup.find('div', class_='entry')
        if entry_div:
            content = entry_div.get_text(separator='\n\n').strip()
    
    # Fallback: tentar extrair do article tag
    if not content:
        article_tag = soup.find('article')
        if article_tag:
            content = article_tag.get_text(separator='\n\n').strip()
    
    # Fallback final: todo o body
    if not content:
        body = soup.find('body')
        if body:
            # Remover scripts e styles
            for tag in body(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            content = body.get_text(separator='\n\n').strip()
    
    if not content:
        content = "Não foi possível extrair o conteúdo automaticamente."
    
    return {
        'title': title,
        'content': content,
        'pub_date': pub_date
    }

def create_capture_file(url):
    """Cria arquivo de captura em sources/"""
    print("Detectando fonte...")
    source_info = detect_source_info(url)
    
    print("Extraindo conteúdo do artigo...")
    article = extract_article_content(url)
    
    # Criar nome do arquivo
    today = datetime.now().strftime('%Y-%m-%d')
    author_slug = slugify(source_info['author'])
    title_slug = slugify(article['title'])
    filename = f"{today}-{author_slug}-{title_slug}.md"
    
    # Criar conteúdo
    content = f"""# {article['title']}

## Fonte
- **Tipo:** {source_info['type']}
- **Autor:** {source_info['author']}
- **URL:** {url}
- **Data original:** {article['pub_date'] or 'N/A'}
- **Data captura:** {today}

## Conteúdo

{article['content']}

## Minhas Anotações

[Adicionar anotações aqui]
"""
    
    # Salvar arquivo
    sources_dir = Path('/home/alejandro/ai-brain/sources')
    sources_dir.mkdir(exist_ok=True)
    
    filepath = sources_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Arquivo criado: {filepath}")
    
    # Fazer git commit
    subprocess.run(['git', 'add', str(filepath)], cwd='/home/alejandro/ai-brain')
    commit_msg = f"capture: {article['title']}"
    subprocess.run(['git', 'commit', '-m', commit_msg], cwd='/home/alejandro/ai-brain')
    
    print(f"Commit criado: {commit_msg}")
    return str(filepath)

# Executar
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: /capture article <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        filepath = create_capture_file(url)
        print(f"\nCaptura completa! Arquivo: {filepath}")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

## Notes

- Usa BeautifulSoup para parsing HTML
- Detecta automaticamente autor e tipo para domínios conhecidos
- Suporta Substack, Seth's Blog e artigos genéricos
- Cria commit automaticamente após captura
- Requer `requests` e `beautifulsoup4` (adicionar ao requirements.txt se necessário)
