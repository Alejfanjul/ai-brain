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

### Status atual (2026-01-20)

- **969 chunks** processados dos sources (100% ✅)
- **80 memórias** com embeddings
- **Busca semântica** funcionando (Fase 3.4 ✅)
- **Daily Digest** funcionando (Fase 3.5 ✅)

## Metas Pessoais

| Comando | Descrição |
|---------|-----------|
| `/goals` ou `/metas` | Mostrar progresso das metas (treino + hábitos) |
| `python3 scripts/show_goals.py` | Visão completa com ASCII art |
| `python3 scripts/show_goals.py --today` | Só o foco do dia |
| `python3 scripts/show_goals.py --json` | Saída JSON |

**Dados fonte:**
- `projects/ai-brain/metas/SAUDE.md` - Treino (5/3/1)
- `projects/ai-brain/metas/MACONHA.md` - Redução

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

---

## Ecossistema Daniel Miessler

O **ai-brain** é construído sobre três repositórios de referência do Daniel Miessler:

| Repo | O que é | Local | Quando usar |
|------|---------|-------|-------------|
| **PAI** | Arquitetura de IA pessoal | `~/Personal_AI_Infrastructure` | Criar skills, hooks, estrutura |
| **Fabric** | 234 prompts prontos | `~/Fabric` | Tarefas específicas (análise, criação, extração) |
| **Substrate** | Organização de conhecimento | `~/Substrate` | Estruturar dados, claims, ideias |

### PAI (Personal AI Infrastructure)

Framework de arquitetura. O ai-brain incorporou:
- Sistema de Skills (`.claude-config/skills/`)
- Sistema de Hooks (`.claude-config/hooks/`)
- 15 Princípios Fundadores
- Arquitetura CLI-first

**Usar para:** criar novos skills, hooks, estruturar features.

### Fabric

Coleção de 234 patterns (prompts) testados pela comunidade.

**Guias locais:**
- `projects/ai-brain/guides/FABRIC-ALL-PATTERNS.md` — catálogo completo
- `projects/ai-brain/guides/FABRIC-TELOS-PATTERNS.md` — patterns para TELOS

**Categorias principais:**
| Categoria | Qtd | Exemplos |
|-----------|-----|----------|
| Análise | 35 | `analyze_claims`, `analyze_personality`, `analyze_risk` |
| Criação | 55 | `create_summary`, `create_keynote`, `create_report` |
| Extração | 42 | `extract_wisdom`, `extract_insights`, `extract_ideas` |
| TELOS | 16 | `t_find_blindspots`, `t_check_dunning_kruger` |

**Usar para:** buscar prompts prontos antes de criar do zero.

```bash
# Listar patterns disponíveis
ls ~/Fabric/patterns/

# Usar um pattern
cat input.txt | fabric -p extract_wisdom
```

### Substrate

Sistema de organização do mundo em categorias estruturadas.

**Estrutura:**
```
~/Substrate/
├── Arguments/      ← Argumentos e debates
├── Claims/         ← Afirmações verificáveis
├── Data/           ← Dados e estatísticas
├── Experiments/    ← Experimentos e testes
├── Frames/         ← Modelos mentais
├── Ideas/          ← Ideias e conceitos
├── Models/         ← Modelos de pensamento
├── Organizations/  ← Organizações relevantes
├── Outcomes/       ← Resultados e consequências
└── People/         ← Pessoas importantes
```

**Usar para:** estruturar conhecimento, criar taxonomias.

### 15 Princípios Fundadores (resumo)

1. **Clear Thinking + Prompting is King** — qualidade do output depende do input
2. **Scaffolding > Model** — estrutura importa mais que o modelo
3. **As Deterministic as Possible** — mesmo input = mesmo output
4. **Code Before Prompts** — código é mais confiável que prompts
5. **Spec / Test / Evals First** — definir antes de implementar
6. **UNIX Philosophy** — ferramentas pequenas, composáveis
7. **ENG / SRE Principles** — tratar IA como infra de produção
8. **CLI as Interface** — tudo acessível via linha de comando
9. **Goal → Code → CLI → Prompts → Agents** — pipeline de desenvolvimento
10. **Meta / Self Update System** — sistema que evolui sozinho
11. **Custom Skill Management** — skills como unidade organizacional
12. **Custom History System** — captura automática de histórico
13. **Custom Agent Personalities** — agentes com vozes distintas
14. **Science as Cognitive Loop** — método científico como padrão
15. **Permission to Fail** — permissão explícita para dizer "não sei"

> **Referência completa:** `.claude-config/skills/CORE/SYSTEM/PAISYSTEMARCHITECTURE.md`

### Sincronização entre PCs

```bash
# Em novo PC (após clonar ai-brain):
cd ~/ai-brain
./scripts/setup-pai.sh

# Em PC existente (após mudanças):
cd ~/ai-brain
git pull
./scripts/setup-pai.sh
```

O script copia `.claude-config/` para `~/.claude/` (local da máquina).

**Regra:** Skills e hooks devem sempre estar em `.claude-config/` (repo), nunca só em `~/.claude/` (local).
