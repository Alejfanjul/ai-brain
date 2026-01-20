# AI Brain - Roadmap

> Última atualização: 2026-01-20 (PAI Study unificado ao ai-brain)

## Visão geral dos Marcos

| Marco | Descrição | Status |
|-------|-----------|--------|
| 1 | Audit Trail | ✅ Concluído |
| 2 | Persistência de Conversas | ✅ Concluído |
| 3 | Memória Semântica | 🔄 Em progresso |
| 4 | Proatividade | 📋 Futuro |
| 5 | Contexto Profundo (TELOS) | 🔄 Em progresso |

---

## Marco 1: Audit Trail ✅

**Objetivo:** Registrar tudo automaticamente via hooks.

**Resultado:**
- Hooks do Claude Code configurados
- Toda interação salva no Supabase
- Campo `repositorio` distingue origem (ai-brain / sistema-os)

---

## Marco 2: Persistência de Conversas ✅

**Objetivo:** Manter histórico completo de conversas.

**Resultado:**
- 109+ sessões salvas
- 1000+ mensagens registradas
- Session ID para continuar conversas

---

## Marco 3: Memória Semântica 🔄

**Objetivo:** Sistema que cruza memórias (conversas) com conteúdos (sources), permitindo perguntas como "como nosso plano se relaciona com as ideias do Nate?"

### Fases

| Fase | Descrição | Status |
|------|-----------|--------|
| 3.1 | Sync + Extração de memórias | ✅ Concluído |
| 3.2 | Embeddings das memórias | ✅ Concluído |
| 3.3 | Embeddings dos sources | ✅ Concluído |
| 3.4 | Script de busca unificada | ✅ Concluído |
| 3.5 | Daily Digest | 📋 Pendente |
| 3.6 | Hooks de retrieval | 📋 Pendente |
| 3.7 | Bouncer + Fix Button | 📋 Pendente |

### Fase 3.1: Sync + Extração ✅

**Resultado:**
- 40 memórias extraídas das conversas
- Tipos: workflow (13), decisão (11), insight (10), correção (5), padrão (1)
- Cron job a cada 15 min (extract_memories + generate_embeddings)

### Fase 3.2: Embeddings das memórias ✅

**Resultado:**
- 40 memórias com embeddings (768 dimensões)
- Ollama + nomic-embed-text configurado
- pgvector habilitado no Supabase

### Fase 3.3: Embeddings dos sources ✅

**Objetivo:** Processar todos os arquivos em `sources/` para busca semântica.

**Resultado:**
- ✅ Tabela `source_chunks` criada
- ✅ Script `embed_sources.py` funcionando
- ✅ **969 chunks processados** (100%)
- ✅ Ollama com GPU (RTX 5060) - processamento rápido

**Configs:**
- Chunks de ~600 palavras
- 15% overlap entre chunks
- Autor extraído automaticamente do nome do arquivo

### Fase 3.4: Script de busca unificada ✅

**Objetivo:** Busca manual que cruza memórias + sources.

**Resultado:**
- ✅ `scripts/search.py` funcionando
- ✅ Funções RPC `search_sources` e `search_memories` no Supabase
- ✅ Filtros: `--autor`, `--limit`, `--sources-only`, `--memories-only`

```bash
# Exemplos de uso
python3 scripts/search.py "como implementar agentes ia"
python3 scripts/search.py "building agents" --autor nate --limit 10
python3 scripts/search.py "decisões importantes" --memories-only
```

### Fase 3.5: Daily Digest 📋

**Objetivo:** Sistema me procurar de manhã com o que importa.

> Inspirado no Nate: "Humans don't retrieve consistently. But we do respond to what shows up in front of us."

**Entregável:**
- Cron às 7h
- Query projetos ativos + memórias recentes
- Gera resumo via Claude
- Envia para Slack/Telegram/email

**Conteúdo do digest:**
- Top 3 ações do dia
- Um projeto que pode estar parado
- Uma conexão interessante (memória ↔ source)

### Fase 3.6: Hooks de retrieval 📋

**Objetivo:** Injetar contexto relevante automaticamente nas conversas.

**Entregável:**
- `~/.claude/hooks/memory_retrieval_hook.py`
- Hook `user_prompt_submit` → busca memórias/sources → injeta contexto

### Fase 3.7: Bouncer + Fix Button 📋

**Objetivo:** Qualidade e correção fácil.

> Inspirado no Nate: "The fastest way to kill a system is to fill it with garbage."

**Bouncer:**
- Haiku retorna `confidence_score` ao extrair memória
- Se < 0.6, não salva automaticamente - pede confirmação

**Fix Button:**
- Comando simples para corrigir classificação errada
- Ex: `fix: essa memória é decisao, não insight`

---

## Marco 4: Proatividade 📋

**Objetivo:** Sistema que trabalha proativamente, não só quando acionado.

**Features planejadas:**
- Morning overview automático
- Acompanhamento de projetos (perguntar evolução)
- Detecção de padrões → sugestão de automações
- Weekly review automática

**Pré-requisito:** Marco 3 concluído.

---

## Decisões técnicas

### Princípio fundamental
> "Não quero me distanciar de modelos de ponta. Quero que meu app incorpore novas funcionalidades rapidamente."

**Implicações:**
- Sem frameworks intermediários (LangChain, CrewAI)
- Claude Code CLI direto
- Código próprio para controle total

### Validação externa
Alex Hillman (JFDI System) e Nate (Second Brain 2026) construíram sistemas muito similares. Ver [REFERENCES.md](./REFERENCES.md).

---

## Marco 5: Contexto Profundo (TELOS) 🔄

**Objetivo:** Dar contexto profundo para a IA sobre quem sou e o que quero.

> "Once the AI sees everything—purpose, goals, challenges, strategies, KPIs—now we can start asking questions." - Daniel Miessler

### Fases

| Fase | Descrição | Status |
|------|-----------|--------|
| 5.1 | TELOS pessoal (Ale) | ✅ Concluído |
| 5.2 | TELOS hotel (Duke Beach) | 📋 Pendente |
| 5.3 | Patterns FABRIC validados | 📋 Pendente |
| 5.4 | Skills estruturados | 📋 Pendente |

### Fase 5.1: TELOS Pessoal ✅

**Resultado:**
- ✅ Conversas 01-03 realizadas (Propósito, Camada profunda, Pilares)
- ✅ `telos/TELOS-ALE.md` consolidado (2026-01-17)
- ✅ Guias de patterns criados (`guides/`)

**Documentos:**
- `telos/TELOS-ALE.md` - TELOS pessoal consolidado
- `guides/FABRIC-ALL-PATTERNS.md` - 234 patterns disponíveis
- `guides/FABRIC-TELOS-PATTERNS.md` - 16 patterns para manutenção do TELOS
- `archive/` - Conversas e rascunhos anteriores

### Fase 5.2: TELOS Hotel 📋

**Objetivo:** Criar contexto profundo do Duke Beach Hotel.

**Entregável:**
- [ ] `telos/TELOS-HOTEL.md`
- [ ] Missão, metas, KPIs, desafios sazonais, perfil de hóspedes

### Fase 5.3: Patterns FABRIC 📋

**Objetivo:** Validar patterns resolvendo problemas reais.

> "Só automatize o que já validou manualmente"

**Entregável:**
- [ ] 3-5 patterns testados no dia a dia
- [ ] 1 pattern customizado para o hotel

### Fase 5.4: Skills Estruturados 📋

**Objetivo:** Transformar patterns validados em skills do PAI.

**Entregável:**
- [ ] Primeiro skill (ex: HotelOperations)
- [ ] 1 workflow funcional
- [ ] 1 tool em TypeScript

---

## Repositórios de Referência

| Repo | Local | Uso |
|------|-------|-----|
| PAI | `/home/marketing/pai-reference/` | Arquitetura de skills/hooks |
| TELOS | `/home/marketing/telos-reference/` | Templates de contexto |
| Fabric | `/home/marketing/fabric-reference/` | 234 patterns de prompts |
| Daemon | `/home/marketing/daemon-reference/` | API broadcast (futuro) |
| Substrate | `/home/marketing/substrate-reference/` | Argumentos estruturados (futuro) |
