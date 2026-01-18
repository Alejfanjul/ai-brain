# AI Brain - Contexto para Claude

Este é um hub central de conhecimento e projetos pessoais.

## Estrutura do Repositório

```
ai-brain/
├── sources/           ← Conhecimento capturado (transcripts, artigos)
├── projects/          ← Projetos em andamento
├── templates/         ← Templates
├── scripts/           ← Scripts de captura e processamento
├── CONTEXT.md         ← Guia de autores
└── CLAUDE.md          ← Este arquivo
```

## Como trabalhar

Ao iniciar uma conversa:
1. Ler `CONTEXT.md` para entender os autores e seus domínios
2. Se for sobre um projeto, ler o `README.md` do projeto
3. Identificar o estágio (Exploração, Definição, Execução)
4. Adaptar abordagem conforme o estágio

Ao finalizar uma conversa produtiva:
1. Atualizar os documentos do projeto conforme a seção "Como atualizar documentação"
2. Se houve decisão importante, adicionar entrada no CHANGELOG.md

---

## Estrutura Padrão de Projetos

Todo projeto deve seguir esta estrutura:

```
projeto/
├── README.md      ← Visão + estado atual (o que é, por que existe)
├── ROADMAP.md     ← Marcos e fases (onde estamos, para onde vamos)
├── SETUP.md       ← Configs técnicas, SQLs, comandos
├── REFERENCES.md  ← Material de consulta e inspiração
└── CHANGELOG.md   ← Histórico de decisões importantes
```

### Propósito de cada arquivo

| Arquivo | Analogia | Atualização |
|---------|----------|-------------|
| **README.md** | Estrela Polar - "por que estamos fazendo isso?" | Manual |
| **ROADMAP.md** | Mapa da Viagem - "você está aqui" | Semi-auto |
| **SETUP.md** | Manual de Instruções | Quando configs mudam |
| **REFERENCES.md** | Biblioteca | Quando há novo material |
| **CHANGELOG.md** | Diário de Bordo | A cada decisão importante |

### Como atualizar documentação

**Após conversa com decisões importantes:**
1. Adicionar entrada no `CHANGELOG.md` com data, contexto e decisões
2. Atualizar status no `ROADMAP.md` se fase mudou
3. Atualizar `README.md` se visão/capacidades mudaram

**Após mudança técnica:**
1. Atualizar `SETUP.md` com novos comandos/configs
2. Adicionar entrada no `CHANGELOG.md`

**Após descobrir material útil:**
1. Adicionar em `REFERENCES.md` com quotes relevantes
2. Linkar para source local se disponível

**Princípio:** Documentação deve refletir realidade. Se algo mudou no código/sistema, os docs precisam acompanhar.

## Comandos de Captura

| Tipo | Comando |
|------|---------|
| YouTube | `python3 scripts/capture_youtube.py <url>` |
| Playlist | `python3 scripts/capture_playlist.py <url>` |
| Artigo | `python3 scripts/capture_article.py <url>` |
| EPUB | `python3 scripts/capture_epub.py <arquivo>` |
| PDF | `python3 scripts/capture_pdf.py <arquivo>` ou `/pdf` |
| Curso | `python3 scripts/capture_course.py` |
| Manual | Usar template `templates/CAPTURE-MANUAL.md` |

## Memory Lane (Sistema de Memória)

**Automático (cron a cada 15 min):**
- `extract_memories.py` → extrai memórias de conversas novas
- `generate_embeddings.py` → gera embeddings das memórias

**Manual:**

| Comando | Descrição |
|---------|-----------|
| python3 scripts/search.py "query" | Busca semântica em memórias e sources |
| python3 scripts/embed_sources.py | Gerar embeddings dos sources |
| python3 scripts/embed_sources.py --dry-run | Ver quantos chunks faltam |

**Verificar logs:**
```bash
tail -f /tmp/ml_extract.log      # Extração
tail -f /tmp/ml_embeddings.log   # Embeddings
```

### Status atual (2026-01-12)

- **969 chunks** processados dos sources (100% ✅)
- **80 memórias** com embeddings
- **Busca semântica** funcionando (Fase 3.4 ✅)
- Próximo: Daily Digest (Fase 3.5)

### Ollama (comandos rápidos)

```bash
sudo systemctl start ollama    # Iniciar
sudo systemctl status ollama   # Ver status
ollama list                    # Ver modelos
```

> **Mais detalhes:** Ver `projects/ai-brain/SETUP.md`

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
