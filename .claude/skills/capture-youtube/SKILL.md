# Capture YouTube

Extrai transcript e metadata de vídeos do YouTube e salva em sources/.

## Usage

```
/capture youtube <url>
```

## What it does

1. Extrai transcript/legendas usando yt-dlp
2. Extrai metadata (título, canal, data de publicação, duração)
3. Cria arquivo em `sources/` usando o template padrão
4. Faz git commit automaticamente com mensagem "capture: [título]"

## Implementation

```python
import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

def slugify(text):
    """Converte texto para slug (lowercase, hífens)"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def extract_video_info(url):
    """Extrai metadata do vídeo usando yt-dlp"""
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-lang', 'en,pt',
        '--write-subs',
        '--sub-format', 'vtt',
        '--print', '%(title)s|||%(uploader)s|||%(upload_date)s|||%(duration)s',
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro ao extrair metadata: {result.stderr}")
    
    parts = result.stdout.strip().split('|||')
    title = parts[0] if len(parts) > 0 else "Unknown"
    uploader = parts[1] if len(parts) > 1 else "Unknown"
    upload_date = parts[2] if len(parts) > 2 else ""
    duration = parts[3] if len(parts) > 3 else ""
    
    # Formatar data de upload
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[0:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    
    return {
        'title': title,
        'uploader': uploader,
        'upload_date': upload_date,
        'duration': duration
    }

def extract_transcript(url):
    """Extrai transcript do vídeo"""
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-lang', 'en,pt',
        '--write-subs',
        '--sub-format', 'vtt',
        '--convert-subs', 'txt',
        '--output', '/tmp/%(id)s.%(ext)s',
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro ao extrair transcript: {result.stderr}")
    
    # Procurar arquivo de legenda gerado
    import glob
    subtitle_files = glob.glob('/tmp/*.txt')
    if not subtitle_files:
        return "Transcript não disponível para este vídeo."
    
    # Ler o primeiro arquivo encontrado
    with open(subtitle_files[0], 'r', encoding='utf-8') as f:
        transcript = f.read()
    
    # Limpar arquivo temporário
    os.remove(subtitle_files[0])
    
    return transcript

def create_capture_file(url):
    """Cria arquivo de captura em sources/"""
    print("Extraindo informações do vídeo...")
    info = extract_video_info(url)
    
    print("Extraindo transcript...")
    transcript = extract_transcript(url)
    
    # Criar nome do arquivo
    today = datetime.now().strftime('%Y-%m-%d')
    author_slug = slugify(info['uploader'])
    title_slug = slugify(info['title'])
    filename = f"{today}-{author_slug}-{title_slug}.md"
    
    # Criar conteúdo
    content = f"""# {info['title']}

## Fonte
- **Tipo:** video
- **Autor:** {info['uploader']}
- **URL:** {url}
- **Data original:** {info['upload_date']}
- **Data captura:** {today}
- **Duração:** {info['duration']}s

## Conteúdo

{transcript}

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
    commit_msg = f"capture: {info['title']}"
    subprocess.run(['git', 'commit', '-m', commit_msg], cwd='/home/alejandro/ai-brain')
    
    print(f"Commit criado: {commit_msg}")
    return str(filepath)

# Executar
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: /capture youtube <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        filepath = create_capture_file(url)
        print(f"\nCaptura completa! Arquivo: {filepath}")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
```

## Notes

- Requer `yt-dlp` instalado (ver requirements.txt)
- Tenta extrair legendas em inglês ou português
- Se não houver legendas, retorna mensagem informando
- Cria commit automaticamente após captura
