# Capture Manual

Fluxo guiado para capturar conteúdo copiado manualmente.

## Usage

```
/capture manual
```

## What it does

1. Pergunta título, tipo, autor e URL
2. Pede para colar o conteúdo
3. Cria arquivo em `sources/` usando o template padrão
4. Faz git commit e push automaticamente com mensagem "capture: [título]"

## Implementation

```python
import sys
from datetime import datetime
from pathlib import Path
import subprocess
import re

def slugify(text):
    """Converte texto para slug (lowercase, hífens)"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def get_multiline_input(prompt):
    """Pede input multilinha (termina com linha vazia ou Ctrl+D)"""
    print(prompt)
    print("(Cole o conteúdo abaixo. Termine com uma linha vazia e pressione Enter)")
    print("-" * 60)
    
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "":
                # Se já temos conteúdo e recebemos linha vazia, terminar
                if lines:
                    break
            else:
                lines.append(line)
    except EOFError:
        pass
    
    return '\n'.join(lines)

def create_manual_capture():
    """Fluxo interativo para captura manual"""
    print("\n=== Captura Manual de Conteúdo ===\n")
    
    # Coletar informações
    title = input("Título: ").strip()
    if not title:
        print("Erro: Título é obrigatório")
        return None
    
    print("\nTipos disponíveis: newsletter | video | artigo | blog | curso | livro | podcast")
    content_type = input("Tipo: ").strip() or "artigo"
    
    author = input("Autor: ").strip() or "Unknown"
    
    url = input("URL (opcional): ").strip() or "N/A"
    
    pub_date = input("Data original (YYYY-MM-DD, opcional): ").strip() or "N/A"
    
    # Coletar conteúdo
    print()
    content = get_multiline_input("Cole o conteúdo abaixo:")
    
    if not content.strip():
        print("Erro: Conteúdo não pode estar vazio")
        return None
    
    # Criar nome do arquivo
    today = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(title)
    filename = f"{today}-{slug}.md"
    
    # Criar conteúdo do arquivo
    file_content = f"""# {title}

## Fonte
- **Tipo:** {content_type}
- **Autor:** {author}
- **URL:** {url}
- **Data original:** {pub_date}
- **Data captura:** {today}

## Conteúdo

{content}

## Minhas Anotações

[Adicionar anotações aqui]
"""
    
    # Salvar arquivo
    sources_dir = Path('/home/alejandro/ai-brain/sources')
    sources_dir.mkdir(exist_ok=True)
    
    filepath = sources_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print(f"\n✓ Arquivo criado: {filepath}")
    
    # Fazer git commit
    subprocess.run(['git', 'add', str(filepath)], cwd='/home/alejandro/ai-brain')
    commit_msg = f"capture: {title}"
    subprocess.run(['git', 'commit', '-m', commit_msg], cwd='/home/alejandro/ai-brain')

    print(f"✓ Commit criado: {commit_msg}")

    # Fazer git push
    subprocess.run(['git', 'push'], cwd='/home/alejandro/ai-brain')
    print(f"✓ Push feito")
    
    return str(filepath)

# Executar
if __name__ == '__main__':
    try:
        filepath = create_manual_capture()
        if filepath:
            print(f"\n=== Captura completa! ===")
            print(f"Arquivo: {filepath}")
        else:
            print("\nCaptura cancelada.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCaptura cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

## Notes

- Modo interativo: faz perguntas ao usuário
- Suporta input multilinha para conteúdo (termina com linha vazia)
- Campos opcionais: URL, data original
- Cria commit automaticamente após captura
- Pode ser cancelado com Ctrl+C
