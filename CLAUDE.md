# AI Brain - Contexto para Claude

Este é um hub central de conhecimento e projetos pessoais.

## Estrutura

```
ai-brain/
├── sources/           ← Conhecimento capturado
├── projects/          ← Projetos em andamento
├── templates/         ← Templates
├── scripts/           ← Scripts de captura
└── CONTEXT.md         ← Guia de autores
```

## Como trabalhar

Ao iniciar uma conversa:
1. Ler `CONTEXT.md` para entender os autores e seus domínios
2. Se for sobre um projeto, ler o `README.md` do projeto
3. Identificar o estágio (Exploração, Definição, Execução)
4. Adaptar abordagem conforme o estágio

Ao finalizar uma conversa produtiva:
1. Atualizar o `README.md` do projeto se houve decisões
2. Adicionar entrada no Histórico com data e mudança

## Comandos de Captura

| Tipo | Comando |
|------|---------|
| YouTube | `python3 scripts/capture_youtube.py <url>` |
| Playlist | `python3 scripts/capture_playlist.py <url>` |
| Artigo | `python3 scripts/capture_article.py <url>` |
| EPUB | `python3 scripts/capture_epub.py <arquivo>` |
| Curso | `python3 scripts/capture_course.py` |
| Manual | Usar template `templates/CAPTURE-MANUAL.md` |

## Memory Lane (Sistema de Memória)

| Comando | Descrição |
|---------|-----------|
| python3 scripts/extract_memories.py | Extrair memórias das conversas |
| python3 scripts/generate_embeddings.py | Gerar embeddings das memórias |
| python3 scripts/embed_sources.py | Gerar embeddings dos sources (transcripts) |
| python3 scripts/embed_sources.py --dry-run | Ver quantos chunks seriam processados |

### Status atual (2026-01-08)

- **218/910 chunks** processados dos sources
- Continuar processamento na máquina com GPU (muito mais rápido)

### Ollama (Embeddings locais)

| Comando | Descrição |
|---------|-----------|
| sudo systemctl start ollama | Iniciar Ollama |
| sudo systemctl stop ollama | Parar Ollama |
| sudo systemctl status ollama | Ver status |
| curl localhost:11434/api/tags | Verificar se está rodando |
| ollama list | Ver modelos instalados |

### Continuar processamento na máquina com RTX

**1. Verificar se Ollama está usando GPU:**
```bash
# Ver se CUDA está disponível
nvidia-smi

# Iniciar Ollama e verificar logs
sudo systemctl start ollama
journalctl -u ollama -f
# Deve mostrar "using CUDA" ou "GPU detected"
```

**2. Verificar modelo instalado:**
```bash
ollama list
# Se não tiver nomic-embed-text:
ollama pull nomic-embed-text
```

**3. Atualizar repo e rodar:**
```bash
cd ~/ai-brain
git pull
python3 scripts/embed_sources.py
```

**Tempo estimado com GPU:** ~2-5 minutos para os ~700 chunks restantes

**4. Após terminar, criar script de busca (Fase 3):**
```bash
# Verificar total de chunks
python3 -c "
from scripts.embed_sources import supabase_request
result = supabase_request('source_chunks?select=id&limit=10000')
print(f'Total chunks: {len(result)}')
"
```

## Criar novo projeto

```bash
cp templates/PROJECT-EXPLORATION.md projects/nome-do-projeto/README.md
```

## Guia rápido de autores

- **Direção/Marketing** → Seth Godin
- **Filosofia/Clareza** → Derek Sivers
- **IA/Execução** → Nate
- **Emocional/Bloqueios** → Joe Hudson
- **Marca pessoal** → Bruno Perini

## Usuário

- **Nome:** Ale
- **Contexto:** Construindo empresa de uma pessoa só, baseada em IA
- **Trabalha em:** Duke Beach Hotel (liberdade para criar soluções)
- **Objetivo:** Sistemas que mostrem que "trabalho pode ser bacana"
