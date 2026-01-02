#!/usr/bin/env python3
"""
Email Capture Script
Captura emails do Nate's Newsletter e salva no ai-brain.
"""

import os
import json
import base64
import re
from datetime import datetime, timedelta
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Configuração
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SOURCES_DIR = Path("sources")
STATE_FILE = Path(".github/captured_emails.json")

# Remetentes para capturar
SENDERS = [
    {
        "email": "natesnewsletter.substack.com",
        "author": "Nate",
        "type": "newsletter"
    },
    {
        "email": "simonw.substack.com",
        "author": "Simon Willison",
        "type": "newsletter"
    },
    {
        "email": "joe@artofaccomplishment.com",
        "author": "Joe Hudson",
        "type": "newsletter"
    }
]


def get_gmail_service():
    """Autentica e retorna serviço Gmail."""
    creds = None

    # Tenta carregar token existente
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se não existe ou expirou
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Salva token atualizado
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        else:
            raise Exception("Token inválido. Execute gmail_auth.py primeiro.")

    return build('gmail', 'v1', credentials=creds)


def load_captured_emails():
    """Carrega IDs de emails já capturados."""
    if STATE_FILE.exists():
        return set(json.loads(STATE_FILE.read_text()))
    return set()


def save_captured_emails(email_ids):
    """Salva IDs de emails capturados."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(list(email_ids), indent=2))


def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def extract_email_content(payload):
    """Extrai conteúdo HTML/texto do payload do email."""

    def get_body(payload):
        """Recursivamente busca o corpo do email."""
        if 'body' in payload and payload['body'].get('data'):
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        if 'parts' in payload:
            for part in payload['parts']:
                mime_type = part.get('mimeType', '')

                # Prefere HTML
                if mime_type == 'text/html':
                    if part['body'].get('data'):
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

                # Recursivo para multipart
                if mime_type.startswith('multipart/'):
                    result = get_body(part)
                    if result:
                        return result

            # Fallback para text/plain
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    if part['body'].get('data'):
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

        return None

    return get_body(payload)


def html_to_markdown(html_content):
    """Converte HTML para Markdown limpo."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove elementos indesejados
    for tag in soup.select('script, style, meta, link, header, footer, nav'):
        tag.decompose()

    # Remove imagens de tracking (1x1 pixels, etc)
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if 'track' in src.lower() or 'pixel' in src.lower() or 'beacon' in src.lower():
            img.decompose()

    # Converte para markdown
    markdown = md(str(soup), heading_style="ATX", strip=['script', 'style'])

    # Limpa linhas em branco excessivas
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    return markdown.strip()


def extract_notion_links(content):
    """Extrai links do Notion do conteúdo."""
    notion_pattern = r'https://(?:www\.)?notion\.so/[^\s\)\]\"<>]+'
    links = re.findall(notion_pattern, content)
    return list(set(links))  # Remove duplicatas


def get_header(headers, name):
    """Extrai header específico."""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return None


def extract_author_from_content(html_content, subject):
    """Tenta extrair autor do conteúdo HTML/subject quando header falha."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()

    # Combina subject + body para buscar
    combined_text = f"{subject} {text}"

    # Patterns específicos baseados em análise dos emails capturados
    patterns = [
        ("Simon Willison", r"Simon Willison'?s? Newsletter|simonw\.substack\.com"),
        ("Nate", r"Nate'?s? Newsletter|natesnewsletter\.substack\.com"),
        ("Joe Hudson", r"Joe Hudson|artofaccomplishment\.com"),
    ]

    for author, pattern in patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            return author

    return None


def create_capture_file(subject, author, content, date_str, email_type, notion_links=None):
    """Cria arquivo de captura."""
    author_slug = slugify(author)
    title_slug = slugify(subject)
    filename = f"{date_str}-{author_slug}-{title_slug}.md"
    filepath = SOURCES_DIR / filename

    # Evita sobrescrever
    if filepath.exists():
        return None

    # Seção de links do Notion se houver
    notion_section = ""
    if notion_links:
        notion_section = "\n## Links do Notion (Prompts/Templates)\n\n"
        for link in notion_links:
            notion_section += f"- {link}\n"
        notion_section += "\n"

    template = f"""# {subject}

## Fonte
- **Tipo:** {email_type}
- **Autor:** {author}
- **URL:** email
- **Data original:** {date_str}
- **Data captura:** {datetime.now().strftime('%Y-%m-%d')}
{notion_section}
## Conteúdo

{content}

## Minhas Anotações

"""

    filepath.write_text(template, encoding='utf-8')
    print(f"✅ Criado: {filename}")
    return filepath


def process_emails(service, days_back=2):
    """Busca e processa emails recentes."""
    captured_ids = load_captured_emails()
    new_captures = []

    # Data de corte
    after_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')

    # Busca emails de todas as fontes configuradas
    query = f'from:(natesnewsletter.substack.com OR simonw.substack.com OR joe@artofaccomplishment.com) after:{after_date}'

    print(f"Buscando emails: {query}")

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=100
    ).execute()

    messages = results.get('messages', [])
    print(f"Encontrados: {len(messages)} emails")

    for msg in messages:
        msg_id = msg['id']

        if msg_id in captured_ids:
            print(f"  Já capturado: {msg_id[:8]}...")
            continue

        # Busca conteúdo completo
        full_msg = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        headers = full_msg['payload'].get('headers', [])
        subject = get_header(headers, 'Subject') or 'Sem título'
        date_raw = get_header(headers, 'Date') or ''
        from_header = get_header(headers, 'From') or ''

        # Extrai conteúdo HTML PRIMEIRO (necessário para fallback de autor)
        html_content = extract_email_content(full_msg['payload'])

        if not html_content:
            print(f"    ⚠️ Sem conteúdo HTML")
            continue

        # Detecta autor baseado no remetente (com fallback para conteúdo)
        author = "Unknown"
        email_type = "newsletter"

        # Tenta match direto com SENDERS
        for sender in SENDERS:
            if sender['email'].lower() in from_header.lower():
                author = sender['author']
                email_type = sender['type']
                break

        # Fallback: extrai do conteúdo se falhou
        if author == "Unknown":
            extracted_author = extract_author_from_content(html_content, subject)
            if extracted_author:
                author = extracted_author
                # Busca o type correspondente em SENDERS
                for sender in SENDERS:
                    if sender['author'] == author:
                        email_type = sender['type']
                        break

        print(f"  Processando: {subject[:50]}... [autor: {author}]")

        # Parse da data
        try:
            # Tenta diferentes formatos
            for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%d %b %Y %H:%M:%S %z']:
                try:
                    date_obj = datetime.strptime(date_raw.split(' (')[0].strip(), fmt)
                    break
                except:
                    continue
            else:
                date_obj = datetime.now()
            date_str = date_obj.strftime('%Y-%m-%d')
        except:
            date_str = datetime.now().strftime('%Y-%m-%d')

        # Converte para markdown
        markdown_content = html_to_markdown(html_content)

        # Extrai links do Notion
        notion_links = extract_notion_links(html_content)
        if notion_links:
            print(f"    🔗 Links Notion encontrados: {len(notion_links)}")

        # Cria arquivo
        filepath = create_capture_file(
            subject=subject,
            author=author,
            content=markdown_content,
            date_str=date_str,
            email_type=email_type,
            notion_links=notion_links
        )

        if filepath:
            captured_ids.add(msg_id)
            new_captures.append(filepath)

    save_captured_emails(captured_ids)
    return new_captures


def main():
    """Função principal."""
    print("=== Email Capture ===")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    SOURCES_DIR.mkdir(exist_ok=True)

    try:
        service = get_gmail_service()
        captures = process_emails(service, days_back=30)  # Últimos 30 dias

        print(f"\n=== Resumo ===")
        print(f"Novos emails capturados: {len(captures)}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        raise


if __name__ == "__main__":
    main()
