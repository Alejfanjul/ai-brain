#!/usr/bin/env python3
"""
Captura playlist inteira do YouTube.
Uso: python3 scripts/capture_playlist.py <URL_DA_PLAYLIST>
"""

import sys
import subprocess
import re
import json
import glob
import tempfile
import os
from datetime import datetime
from pathlib import Path

SOURCES_DIR = Path("sources")


def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def get_playlist_info(url):
    """Extrai informações da playlist."""
    cmd = [
        'yt-dlp',
        '--dump-json',
        '--flat-playlist',
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    videos = []
    playlist_title = None
    playlist_author = None

    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        try:
            data = json.loads(line)
            if not playlist_title and data.get('playlist_title'):
                playlist_title = data.get('playlist_title')
            if not playlist_author and data.get('playlist_uploader'):
                playlist_author = data.get('playlist_uploader')

            videos.append({
                'id': data.get('id'),
                'title': data.get('title'),
                'url': f"https://www.youtube.com/watch?v={data.get('id')}"
            })
        except json.JSONDecodeError:
            continue

    return {
        'title': playlist_title or 'Playlist',
        'author': playlist_author or 'Desconhecido',
        'videos': videos
    }


def get_transcript(video_id):
    """Extrai transcript de um vídeo."""
    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = os.path.join(tmpdir, '%(id)s')

        # Detecta idioma disponível
        cmd_info = [
            'yt-dlp',
            '--dump-json',
            '--skip-download',
            url
        ]

        result = subprocess.run(cmd_info, capture_output=True, text=True)

        sub_lang = 'en'
        try:
            video_info = json.loads(result.stdout)
            auto_captions = video_info.get('automatic_captions', {})

            if auto_captions:
                available_langs = list(auto_captions.keys())
                orig_langs = [l for l in available_langs if '-orig' in l]
                if orig_langs:
                    sub_lang = orig_langs[0]
                elif 'en' in available_langs:
                    sub_lang = 'en'
                elif available_langs:
                    sub_lang = available_langs[0]
        except:
            pass

        # Baixa legendas
        cmd = [
            'yt-dlp',
            '--write-auto-sub',
            '--sub-lang', sub_lang,
            '--skip-download',
            '-o', output_template,
            url
        ]

        subprocess.run(cmd, capture_output=True, text=True)

        vtt_files = glob.glob(os.path.join(tmpdir, '*.vtt'))
        if vtt_files:
            return parse_vtt(vtt_files[0])

        srt_files = glob.glob(os.path.join(tmpdir, '*.srt'))
        if srt_files:
            return parse_vtt(srt_files[0])

    return None


def parse_vtt(filepath):
    """Parse arquivo VTT e extrai texto."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = []
    for line in content.split('\n'):
        line = line.strip()
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
        line = re.sub(r'<[^>]+>', '', line)
        if line:
            lines.append(line)

    cleaned = []
    prev = None
    for line in lines:
        if line != prev:
            cleaned.append(line)
            prev = line

    return ' '.join(cleaned)


def create_playlist_file(playlist_info, video_transcripts):
    """Cria arquivo único com toda a playlist."""
    date_str = datetime.now().strftime('%Y-%m-%d')

    author_slug = slugify(playlist_info['author'])
    title_slug = slugify(playlist_info['title'])
    filename = f"{date_str}-{author_slug}-playlist-{title_slug}.md"
    filepath = SOURCES_DIR / filename

    counter = 1
    while filepath.exists():
        filename = f"{date_str}-{author_slug}-playlist-{title_slug}-{counter}.md"
        filepath = SOURCES_DIR / filename
        counter += 1

    # Monta conteúdo
    videos_content = ""
    for i, (video, transcript) in enumerate(video_transcripts, 1):
        videos_content += f"""
### Vídeo {i}: {video['title']}

{transcript if transcript else '[Transcript não disponível]'}

---
"""

    template = f"""# {playlist_info['title']}

## Fonte
- **Tipo:** playlist
- **Autor:** {playlist_info['author']}
- **Plataforma:** YouTube
- **Total de vídeos:** {len(video_transcripts)}
- **Data captura:** {date_str}

## Conteúdo
{videos_content}

## Minhas Anotações

"""

    filepath.write_text(template, encoding='utf-8')
    return filepath


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 scripts/capture_playlist.py <URL_DA_PLAYLIST>")
        sys.exit(1)

    url = sys.argv[1]
    print("=" * 50)
    print("CAPTURA DE PLAYLIST")
    print("=" * 50)
    print(f"URL: {url}")
    print()

    SOURCES_DIR.mkdir(exist_ok=True)

    print("Obtendo informações da playlist...")
    playlist_info = get_playlist_info(url)

    print(f"Playlist: {playlist_info['title']}")
    print(f"Autor: {playlist_info['author']}")
    print(f"Vídeos: {len(playlist_info['videos'])}")
    print()

    # Confirma antes de continuar
    confirm = input(f"Extrair transcript de {len(playlist_info['videos'])} vídeos? (s/n): ").strip().lower()
    if confirm != 's':
        print("Cancelado.")
        return

    print()
    video_transcripts = []

    for i, video in enumerate(playlist_info['videos'], 1):
        print(f"[{i}/{len(playlist_info['videos'])}] {video['title'][:50]}...")
        transcript = get_transcript(video['id'])
        video_transcripts.append((video, transcript))

        if transcript:
            print(f"    ✅ {len(transcript)} caracteres")
        else:
            print(f"    ⚠️ Sem transcript")

    print()
    filepath = create_playlist_file(playlist_info, video_transcripts)

    print(f"✅ Arquivo criado: {filepath}")

    subprocess.run(['git', 'add', str(filepath)])
    commit_msg = f"capture: playlist - {playlist_info['title'][:40]}"
    subprocess.run(['git', 'commit', '-m', commit_msg])
    print(f"✅ Commit: {commit_msg}")


if __name__ == "__main__":
    main()
