# AI Brain - Changelog

Histórico de decisões e mudanças importantes do projeto.

---

## 2026-02-02: Symlinks de diretório + CLAUDE.md global versionado

**Contexto:** Hooks e PAI context usavam symlinks individuais por arquivo, exigindo re-run do `setup-pai.sh` sempre que um novo hook ou arquivo PAI fosse criado. O `CLAUDE.md` global (`~/.claude/CLAUDE.md`) não era versionado no repo.

**Mudanças:**
1. `hooks/` e `pai/` agora usam symlinks de **diretório inteiro** (mesmo padrão de `skills/`)
2. `CLAUDE.md` global criado em `.claude-config/CLAUDE.md` e linkado via setup
3. `setup-pai.sh` atualizado com novo padrão

**Resultado:** Qualquer novo hook, skill ou arquivo PAI é visível automaticamente via `git pull`. Nenhum re-run necessário após setup inicial.

**Arquitetura final:**
```
ai-brain/ (versionado)              ~/.claude/ (symlinks de diretório)
├── .claude-config/hooks/    →      ├── hooks/
├── .claude-config/skills/   →      ├── skills/
├── .claude-config/CLAUDE.md →      ├── CLAUDE.md
├── .claude-config/settings.json →  ├── settings.json
└── pai/                     →      └── pai/
```

---

## 2026-01-29: Análise estrutural PAI - Daniel Miessler

**Contexto:** Assistimos o vídeo "How and Why I Built PAI" (Unsupervised Learning, Daniel Miessler + Nathan Labenz) e analisamos o repositório PAI baixado localmente para entender a arquitetura de referência.

**Fontes analisadas:**
- Transcript do vídeo (`sources/2026-01-26-unsupervised-learning-how-and-why-i-built-pai-with-nathan-labenz.md`)
- Repositório PAI (`~/Personal_AI_Infrastructure/`)
- GitHub Discussion #500 (PAI 3.x improvements)
- Paper Stanford "Generative Agents" (inspiração do sistema de memória)

**Entregável:** `PAI-ESTRUTURA-DANIEL.md` - resumo estrutural completo cobrindo:
- Estrutura de `~/.claude/` (hooks, skills, MEMORY 3-tier, State, Signals)
- Sistema de Hooks (8 eventos, 12 hooks ativos, sentiment analysis)
- The Algorithm (7 fases: OBSERVE→LEARN)
- Skill System (4 tiers de loading)
- Gap analysis: 11 capacidades que o Daniel tem e nós não

**Problemas estruturais identificados:**
1. MEMORY duplicado em dois locais com dados separados
2. Skills duplicadas (cópia real vs fonte versionada)
3. `pai/` como conceito separado do CORE skill
4. Session capture sem conteúdo útil
5. Sem JSONL event stream

**Decisões pendentes:** Estrutura de diretórios, prioridade de capacidades, modelo de portabilidade, escopo de implementação. Documentado em `PAI-ESTRUTURA-DANIEL.md` seção 10.

**Roadmap atualizado:** Adicionados Marco 6 (PAI Portável) e Marco 7 (MEMORY System).

---

## 2026-01-28: Fix hook initialize-session.ts

**Problema:** Hook `initialize-session.ts` falhava ao iniciar sessão com erro:
```
Cannot find module './lib/observability'
```

**Causa:** O hook foi versionado com dependência de um módulo de observability que nunca foi implementado. O código tentava enviar eventos para um dashboard inexistente.

**Solução:** Removida dependência de `./lib/observability` do hook. O código de observability era opcional e não afeta a funcionalidade principal (título da aba, arquivos de sessão).

---

## 2026-01-28: PAI Portável - Setup único por máquina

**Contexto:** PAI Portável funcionava na máquina pessoal mas falhava na máquina do trabalho. Symlinks não são versionados pelo git, e hooks estavam apenas localmente em `~/.claude/`.

**Problema identificado:**
- Symlinks de `pai/` precisavam ser criados manualmente em cada máquina
- Hooks não estavam no repo, então atualizações não propagavam

**Solução implementada:**
1. Hook `load-core-context.ts` agora faz **auto-setup** de symlinks para `pai/`
2. Hooks e settings movidos para `.claude-config/` (versionados)
3. Script `setup-pai.sh` atualizado para criar **symlinks** (não cópias)
4. Criado `SETUP-WORK-PC.md` com instruções para o Claude executar

**Arquitetura final:**
```
ai-brain/ (versionado)          ~/.claude/ (symlinks)
├── pai/*.md            →       ├── pai/*.md
├── .claude-config/hooks/ →     ├── hooks/*.ts
└── .claude-config/settings.json → └── settings.json
```

**Fluxo de uso:**
- Setup inicial: `./scripts/setup-pai.sh` (uma vez por máquina)
- Atualizações: `git pull` (symlinks propagam mudanças automaticamente)

---

## 2026-01-20: Migração para modelo file-based (PAI-style)

**Contexto:** Sistema de embeddings/Supabase adicionava infraestrutura externa que o Claude Code não acessa nativamente. Decisão de substituir por modelo file-based inspirado no PAI do Daniel Miessler.

**O que foi removido:**
- Cron job de extração de memórias (*/15 min)
- Scripts: `embed_sources.py`, `generate_embeddings.py`, `extract_memories.py`, `cleanup_orphan_chunks.py`, `extract_supabase_schema.py`, `search.py`
- Schemas SQL do Supabase
- Dependência `supabase` do requirements.txt
- Variáveis `SUPABASE_URL` e `SUPABASE_ANON_KEY` do .env

**O que foi criado:**
- Estrutura `MEMORY/` com sessions, decisions, learnings (6 fases), State, Signals
- Hook `session-capture.ts` que dispara no evento Stop
- Documentação completa do novo sistema

**Backup:** `~/ai-brain-backup-20260120/`

**Motivação:**
| Antes (Supabase) | Depois (File-based) |
|------------------|---------------------|
| Scripts externos para busca | Claude lê nativamente |
| Embeddings exigem processamento | Zero processamento |
| Infraestrutura externa | Apenas arquivos |
| Cron jobs | Hooks simples |

---

## 2026-01-12: Fase 3.4 concluída - Busca semântica unificada (OBSOLETO)

**Contexto:** Próximo passo do Memory Lane era criar script de busca que cruza memórias com sources.

**Entregáveis:**
1. `scripts/search.py` - busca semântica via linha de comando
2. Funções RPC no Supabase (`search_sources`, `search_memories`)
3. Documentação atualizada (SETUP.md, ROADMAP.md, CLAUDE.md)

**Como usar:**
```bash
python3 scripts/search.py "como implementar agentes ia"
python3 scripts/search.py "building agents" --autor nate
python3 scripts/search.py "decisões" --memories-only
```

**Flags disponíveis:**
- `--autor <nome>` - Filtrar sources por autor
- `--limit <n>` - Limitar resultados (default: 5)
- `--sources-only` - Buscar apenas em source_chunks
- `--memories-only` - Buscar apenas em memórias

**Próximo passo:** Fase 3.5 - Daily Digest

---

## 2026-01-12: Cron jobs configurados

**Contexto:** O cron para automação do Memory Lane estava documentado mas nunca foi configurado.

**Ações:**
1. Configurado crontab com job a cada 15 minutos
2. Encadeado `extract_memories.py` + `generate_embeddings.py`
3. Removido referência ao `sync_sessions.py` (nunca existiu)
4. Atualizada documentação (SETUP.md, README.md)

**Testar:**
```bash
# Ver logs após 15 minutos
tail -f /tmp/ml_extract.log
tail -f /tmp/ml_embeddings.log
```

---

## 2026-01-10: Fase 3.3 concluída - Embeddings dos sources

**Resultado:**
- 969 chunks processados (100%)
- Ollama rodando com GPU (RTX 5060)
- Todos os 61 arquivos em `sources/` indexados

**Próximo passo:** Fase 3.4 - Script de busca unificada (`search.py`)

---

## 2026-01-09: Reestruturação da documentação

**Contexto:** Documentação estava fragmentada em dois arquivos (`ai_brain_parceiro_digital-v0.5.md` e `memory_lane_plan.md`) com informações redundantes.

**Decisões:**
1. Adotar a própria "Estrutura Padrão de Projetos" que havíamos definido
2. Criar 5 arquivos com propósitos claros: README, ROADMAP, SETUP, REFERENCES, CHANGELOG
3. Mover estrutura padrão para CLAUDE.md (disponível para todos os projetos)
4. Adicionar instruções de como atualizar documentação

**Inspiração:** Newsletter do Nate sobre Second Brain 2026 - validou a arquitetura e sugeriu novos componentes (Bouncer, Daily Digest, Fix Button).

---

## 2026-01-08: Embeddings dos Sources + Simplificação

**Contexto:** Reflexão sobre o propósito original do projeto.

**Insight do Ale:**
> "Estou complicando demais as coisas para o começo. Este projeto nasceu com o objetivo de criar planos de projetos pessoais/trabalho e que a IA conseguisse relacionar com os transcripts e conteúdos deste repo."

**Decisões:**
1. Priorizar embeddings dos sources (não só das memórias)
   - Permite cruzar planos com ideias de Nate, Hillman, etc.
2. Scripts manuais primeiro, automatização depois
   - Validar busca semântica antes de criar hooks
3. Configurações técnicas definidas:
   - Chunks de ~600 palavras
   - 15% overlap entre chunks
   - Extração automática de autor/data do nome do arquivo

**Progresso:** Iniciado com 218 chunks. Concluído em 2026-01-10 com 969 chunks.

---

## 2026-01-06: Context Engineering do Manus

**Contexto:** Discussão sobre artigo "Context Engineering for AI Agents" do Manus e newsletter do Nate sobre aquisição pela Meta ($2B).

**Decisões:**
- AI Brain é **fundação** (memória + contexto) para futuros sistemas agentic
- Modelo atual: parceria conversacional (eu + sistema trabalhando juntos)

**Insight principal:**
> "O que o Manus construiu que vale $2B não é o modelo, é o 'harness' - toda a engenharia de contexto ao redor."

**Referências:**
- `sources/2026-01-06-manus-context-engineering-for-ai-agents-lessons-from-bui.md`
- `sources/2026-01-06-nate-meta-bought-manus-for-2b-to-acquire-an-agentic-har.md`

---

## 2026-01-05: Fase 1 Memory Lane concluída

**Resultado:**
- 22 memórias extraídas das conversas existentes
- Tipos: 8 workflows, 6 decisões, 6 insights, 1 correção, 1 padrão
- Cron jobs configurados e funcionando

---

## 2026-01-06: Fase 2 Memory Lane concluída

**Resultado:**
- 40 memórias com embeddings (768 dimensões via nomic-embed-text)
- Script `generate_embeddings.py` criado
- Ollama instalado e configurado localmente

---

## Dezembro 2025: Marcos 1 e 2 concluídos

**Marco 1 - Audit Trail:**
- Conta Supabase criada (free tier)
- Schema básico: sessões, audits
- Hooks do Claude Code configurados

**Marco 2 - Persistência:**
- 81+ sessões e 1000+ mensagens salvas
- Session ID para continuar conversas
- Campo `repositorio` distingue origem

---

## Origem do projeto

**Inspiração:** JFDI System do Alex Hillman + estratégia Derek Sivers (construir para si, documentar publicamente).

**Princípio central:**
> "Ferramenta que cria o cenário ideal pra que você possa dar vazão a todas as ideias, potencial, vontades e objetivos que você tem na vida."
