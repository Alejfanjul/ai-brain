#!/usr/bin/env python3
"""
Captura playlist inteira do YouTube.
Cria uma pasta com um arquivo por vídeo + índice.

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

PLAYLISTS_DIR = Path("sources/playlists")


def slugify(text):
    """Converte texto para slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def format_transcript(text):
    """Formata transcript adicionando parágrafos."""
    if not text:
        return ""

    # Remove prefixo de metadados se existir
    text = re.sub(r'^Kind:\s*\w+\s*Language:\s*\w+\s*', '', text)

    # Adiciona quebras após pontuação final seguida de letra maiúscula
    text = re.sub(r'([.!?])\s+([A-ZÁÉÍÓÚÀÂÊÔÃÕÇ])', r'\1\n\n\2', text)

    # Limpa espaços extras
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


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
    playlist_id = None

    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        try:
            data = json.loads(line)
            if not playlist_title and data.get('playlist_title'):
                playlist_title = data.get('playlist_title')
            if not playlist_author and data.get('playlist_uploader'):
                playlist_author = data.get('playlist_uploader')
            if not playlist_id and data.get('playlist_id'):
                playlist_id = data.get('playlist_id')

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
        'playlist_id': playlist_id,
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
                elif 'pt' in available_langs:
                    sub_lang = 'pt'
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


def create_playlist_folder(playlist_info, url):
    """Cria pasta da playlist e retorna o caminho."""
    author_slug = slugify(playlist_info['author'])
    title_slug = slugify(playlist_info['title'])
    folder_name = f"{author_slug}-{title_slug}"

    folder_path = PLAYLISTS_DIR / folder_name

    # Se já existe, adiciona sufixo
    counter = 1
    while folder_path.exists():
        folder_name = f"{author_slug}-{title_slug}-{counter}"
        folder_path = PLAYLISTS_DIR / folder_name
        counter += 1

    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def create_video_file(folder_path, index, video, transcript, playlist_info):
    """Cria arquivo individual para um vídeo."""
    title_slug = slugify(video['title'])
    filename = f"{index:02d}-{title_slug}.md"
    filepath = folder_path / filename

    formatted_transcript = format_transcript(transcript) if transcript else '[Transcript não disponível]'

    content = f"""# {video['title']}

## Fonte
- **Playlist:** {playlist_info['title']}
- **Autor:** {playlist_info['author']}
- **URL:** {video['url']}

## Transcript

{formatted_transcript}

## Minhas Anotações

"""

    filepath.write_text(content, encoding='utf-8')
    return filename


def create_index_file(folder_path, playlist_info, video_files, url):
    """Cria arquivo _index.md com metadata e lista de vídeos."""
    date_str = datetime.now().strftime('%Y-%m-%d')

    videos_list = ""
    for i, (video, filename) in enumerate(video_files, 1):
        # Link relativo para o arquivo
        link_name = filename.replace('.md', '')
        videos_list += f"{i}. [[{link_name}]] - {video['title']}\n"

    content = f"""# {playlist_info['title']}

## Fonte
- **Tipo:** playlist
- **Autor:** {playlist_info['author']}
- **Plataforma:** YouTube
- **URL:** {url}
- **Total de vídeos:** {len(video_files)}
- **Data captura:** {date_str}

## Vídeos

{videos_list}
## Minhas Anotações

"""

    filepath = folder_path / "_index.md"
    filepath.write_text(content, encoding='utf-8')
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

    PLAYLISTS_DIR.mkdir(parents=True, exist_ok=True)

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

    # Cria pasta da playlist
    folder_path = create_playlist_folder(playlist_info, url)
    print(f"\nPasta criada: {folder_path}")
    print()

    video_files = []

    for i, video in enumerate(playlist_info['videos'], 1):
        print(f"[{i}/{len(playlist_info['videos'])}] {video['title'][:50]}...")
        transcript = get_transcript(video['id'])

        # Cria arquivo do vídeo
        filename = create_video_file(folder_path, i, video, transcript, playlist_info)
        video_files.append((video, filename))

        if transcript:
            print(f"    ✅ {len(transcript)} caracteres")
        else:
            print(f"    ⚠️ Sem transcript")

    # Cria índice
    print()
    index_path = create_index_file(folder_path, playlist_info, video_files, url)
    print(f"✅ Índice criado: {index_path}")

    # Git commit
    print()
    subprocess.run(['git', 'add', str(folder_path)])
    commit_msg = f"capture: playlist - {playlist_info['title'][:40]}"
    subprocess.run(['git', 'commit', '-m', commit_msg])
    print(f"✅ Commit: {commit_msg}")

    print()
    print(f"📁 {len(video_files)} arquivos criados em: {folder_path}")


if __name__ == "__main__":
    main()
