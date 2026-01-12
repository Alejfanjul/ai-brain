# AI Brain - Changelog

Histórico de decisões e mudanças importantes do projeto.

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
