#!/usr/bin/env python3
"""
Captura transcript de vídeo do YouTube.
Uso: python3 scripts/capture_youtube.py <URL>
"""

import sys
import subprocess
import re
import json
from datetime import datetime
from pathlib import Path

SOURCES_DIR = Path("sources")


def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def get_video_info(url):
    """Extrai metadata do vídeo."""
    cmd = [
        'yt-dlp',
        '--print', '%(title)s',
        '--print', '%(channel)s',
        '--print', '%(upload_date)s',
        '--print', '%(duration)s',
        '--print', '%(id)s',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro ao obter info: {result.stderr}")

    lines = result.stdout.strip().split('\n')
    return {
        'title': lines[0] if len(lines) > 0 else 'Sem título',
        'channel': lines[1] if len(lines) > 1 else 'Desconhecido',
        'upload_date': lines[2] if len(lines) > 2 else '',
        'duration': int(lines[3]) if len(lines) > 3 and lines[3].isdigit() else 0,
        'video_id': lines[4] if len(lines) > 4 else ''
    }


def get_transcript(url):
    """Extrai transcript/legendas do vídeo."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        # Tenta legendas automáticas primeiro
        cmd = [
            'yt-dlp',
            '--write-auto-sub',
            '--sub-lang', 'pt,en',
            '--skip-download',
            '--sub-format', 'vtt',
            '-o', f'{tmpdir}/%(id)s',
            url
        ]
        subprocess.run(cmd, capture_output=True, text=True)

        # Procura arquivo de legenda
        for f in os.listdir(tmpdir):
            if f.endswith('.vtt'):
                vtt_path = os.path.join(tmpdir, f)
                return parse_vtt(vtt_path)

        # Se não encontrou, tenta legendas manuais
        cmd = [
            'yt-dlp',
            '--write-sub',
            '--sub-lang', 'pt,en',
            '--skip-download',
            '--sub-format', 'vtt',
            '-o', f'{tmpdir}/%(id)s',
            url
        ]
        subprocess.run(cmd, capture_output=True, text=True)

        for f in os.listdir(tmpdir):
            if f.endswith('.vtt'):
                vtt_path = os.path.join(tmpdir, f)
                return parse_vtt(vtt_path)

    return None


def parse_vtt(filepath):
    """Parse arquivo VTT e extrai texto."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove timestamps e metadata
    lines = []
    for line in content.split('\n'):
        line = line.strip()
        # Ignora linhas de timestamp, WEBVTT header, etc
        if not line:
            continue
        if line.startswith('WEBVTT'):
            continue
        if '-->' in line:
            continue
        if re.match(r'^\d+$', line):
            continue
        if re.match(r'^NOTE', line):
            continue
        # Remove tags HTML
        line = re.sub(r'<[^>]+>', '', line)
        if line:
            lines.append(line)

    # Remove duplicatas consecutivas (comum em auto-captions)
    cleaned = []
    prev = None
    for line in lines:
        if line != prev:
            cleaned.append(line)
            prev = line

    return ' '.join(cleaned)


def format_duration(seconds):
    """Formata duração em minutos."""
    if not seconds:
        return "N/A"
    minutes = seconds // 60
    return f"{minutes} min"


def create_capture_file(info, transcript, url):
    """Cria arquivo de captura."""
    # Parse da data
    if info['upload_date']:
        try:
            date_obj = datetime.strptime(info['upload_date'], '%Y%m%d')
            date_str = date_obj.strftime('%Y-%m-%d')
        except:
            date_str = datetime.now().strftime('%Y-%m-%d')
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')

    slug = slugify(info['title'])
    filename = f"{date_str}-{slug}.md"
    filepath = SOURCES_DIR / filename

    # Evita sobrescrever
    counter = 1
    while filepath.exists():
        filename = f"{date_str}-{slug}-{counter}.md"
        filepath = SOURCES_DIR / filename
        counter += 1

    template = f"""# {info['title']}

## Fonte
- **Tipo:** video
- **Autor:** {info['channel']}
- **URL:** {url}
- **Duração:** {format_duration(info['duration'])}
- **Data original:** {date_str}
- **Data captura:** {datetime.now().strftime('%Y-%m-%d')}

## Conteúdo

{transcript if transcript else '[Transcript não disponível]'}

## Minhas Anotações

"""

    filepath.write_text(template, encoding='utf-8')
    return filepath


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 scripts/capture_youtube.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"=== Captura YouTube ===")
    print(f"URL: {url}")

    SOURCES_DIR.mkdir(exist_ok=True)

    print("Obtendo informações do vídeo...")
    info = get_video_info(url)
    print(f"Título: {info['title']}")
    print(f"Canal: {info['channel']}")

    print("Extraindo transcript...")
    transcript = get_transcript(url)

    if transcript:
        print(f"Transcript extraído: {len(transcript)} caracteres")
    else:
        print("⚠️ Transcript não disponível")

    filepath = create_capture_file(info, transcript, url)
    print(f"✅ Criado: {filepath}")

    # Git commit
    subprocess.run(['git', 'add', str(filepath)])
    subprocess.run(['git', 'commit', '-m', f'capture: {info["title"][:50]}'])
    print("✅ Commit feito")


if __name__ == "__main__":
    main()
