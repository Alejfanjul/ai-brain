# Resumo Estrutural: PAI do Daniel Miessler

> Síntese de 4 fontes: transcript do vídeo (Unsupervised Learning), repositório PAI local,
> GitHub Discussion #500, paper Stanford "Generative Agents".
>
> Objetivo: entender a arquitetura completa para construir a mesma CAPACIDADE adaptada ao nosso cenário.
> Este documento é referência para a próxima conversa onde tomaremos decisões.

---

## 1. Visão Geral: O que é o PAI

PAI não é uma aplicação. É uma **camada de configuração e automação** sobre o Claude Code.

Três camadas:
1. **Engine** = Claude Code (o motor)
2. **Middleware** = Hooks (interceptam eventos, validam segurança, capturam dados)
3. **Content** = Skills + Identity + MEMORY (markdown + scripts)

O que o Daniel construiu é um sistema que **aprende sobre si mesmo** e **melhora recursivamente**. Não é só organização - é um loop de feedback contínuo.

---

## 2. A Estrutura Completa (`~/.claude/`)

```
$PAI_DIR/ (~/.claude/)
│
├── settings.json              ← Config central (hooks, env vars, permissões)
├── .env                       ← API keys (único lugar)
├── .current-session           ← Marker da sessão ativa (JSON)
│
├── hooks/                     ← 12 hooks ativos (TypeScript/bun)
│   ├── initialize-session.ts  ← SessionStart: cria marker, dirs, tab title
│   ├── load-core-context.ts   ← SessionStart: carrega CORE skill
│   ├── security-validator.ts  ← PreToolUse: bloqueia comandos perigosos
│   ├── update-tab-titles.ts   ← UserPromptSubmit: atualiza terminal
│   ├── capture-all-events.ts  ← TODOS eventos: grava em JSONL
│   ├── stop-hook.ts           ← Stop: processa fim de resposta
│   ├── subagent-stop-hook.ts  ← SubagentStop: captura output de subagentes
│   ├── capture-session-summary.ts ← SessionEnd: gera resumo da sessão
│   └── [+4 hooks de sentiment/routing]
│
├── skills/                    ← Capabilities organizadas
│   ├── CORE/                  ← Tier 0: auto-load no SessionStart (~10K tokens)
│   │   ├── SKILL.md           ← Bootstrap: identidade + routing + formato
│   │   ├── USER/              ← Contexto pessoal (14 arquivos)
│   │   │   ├── DAIDENTITY.md  ← Nome/voz/personalidade do AI (Kai)
│   │   │   ├── BASICINFO.md   ← Nome, email, handles
│   │   │   ├── TELOS.md       ← Sistema operacional pessoal
│   │   │   ├── CONTACTS.md    ← Diretório de contatos
│   │   │   ├── TECHSTACKPREFERENCES.md
│   │   │   ├── ASSETMANAGEMENT.md
│   │   │   ├── RESUME.md
│   │   │   ├── ABOUTME.md
│   │   │   ├── CORECONTENT.md
│   │   │   ├── DEFINITIONS.md
│   │   │   ├── REMINDERS.md
│   │   │   ├── ALGOPREFS.md
│   │   │   ├── ART.md
│   │   │   └── PAISECURITYSYSTEM/ (8 arquivos de segurança)
│   │   └── SYSTEM/            ← Arquitetura do sistema (17 arquivos)
│   │       ├── PAISYSTEMARCHITECTURE.md  ← 15 Princípios Fundadores
│   │       ├── MEMORYSYSTEM.md
│   │       ├── SKILLSYSTEM.md
│   │       ├── THEHOOKSYSTEM.md
│   │       ├── THEDELEGATIONSYSTEM.md
│   │       └── [+12 docs de sistema]
│   ├── THEALGORITHM/         ← O Algorithm skill
│   │   ├── SKILL.md
│   │   ├── Phases/ (7 .md)
│   │   ├── Tools/ (7 .ts)
│   │   └── Data/Capabilities.yaml
│   ├── CreateSkill/
│   └── [outras skills...]
│
├── MEMORY/                    ← TODA memória persistente (3 tiers)
│   │
│   │  ── TIER 1: CAPTURE (Hot) ──
│   ├── Work/                  ← Memória por task ativa
│   │   └── [Task-Name_TIMESTAMP]/
│   │       ├── Work.md        ← Goal, resultado, sinais
│   │       ├── IdealState.jsonl ← Critérios de sucesso (append-only)
│   │       ├── TRACE.jsonl    ← Trace de decisões
│   │       ├── Output/        ← Entregas produzidas
│   │       └── Learning/      ← Aprendizados por fase
│   │
│   │  ── TIER 2: SYNTHESIS (Warm) ──
│   ├── Learning/              ← Aprendizados curados por fase do Algorithm
│   │   ├── OBSERVE/
│   │   ├── THINK/
│   │   ├── PLAN/
│   │   ├── BUILD/
│   │   ├── EXECUTE/
│   │   ├── VERIFY/
│   │   └── ALGORITHM/         ← Meta-learnings sobre o próprio sistema
│   │
│   │  ── TIER 3: APPLICATION (Cold) ──
│   ├── sessions/YYYY-MM/      ← Resumos de sessão (rolling 90 dias)
│   ├── learnings/YYYY-MM/     ← Insights extraídos (permanente)
│   ├── decisions/YYYY-MM/     ← Decisões arquiteturais (permanente)
│   ├── research/YYYY-MM/      ← Pesquisas (permanente)
│   ├── execution/             ← Logs de execução (rolling 30 dias)
│   ├── raw-outputs/YYYY-MM/   ← JSONL brutos (rolling 7 dias)
│   ├── security/              ← Eventos de segurança (permanente)
│   ├── recovery/              ← Snapshots de recovery (rolling 7 dias)
│   ├── backups/               ← Backups pre-change
│   ├── archive/               ← Meses antigos compactados
│   │
│   │  ── REAL-TIME STATE ──
│   ├── State/
│   │   ├── active-work.json   ← Task ativa no momento
│   │   ├── algorithm-stats.json ← Total de tasks/compliance
│   │   ├── algorithm-streak.json ← Streak de tasks corretas
│   │   ├── format-streak.json  ← Streak de formato correto
│   │   └── last-judge-rating.json ← Rating mais recente
│   │
│   │  ── SIGNAL DETECTION ──
│   ├── Signals/
│   │   ├── failures.jsonl     ← Falhas no VERIFY com root cause
│   │   ├── loopbacks.jsonl    ← Regressões de fase
│   │   ├── patterns.jsonl     ← Padrões agregados semanalmente
│   │   └── ratings.jsonl      ← Satisfação do usuário
│   │
│   └── session-events.jsonl   ← Log principal de todos os eventos
│
└── tools/                     ← Utilitários globais
    ├── GenerateSkillIndex.ts
    ├── PaiArchitecture.ts
    └── SkillSearch.ts
```

---

## 3. O Modelo Mental: Por que MEMORY dentro de ~/.claude/

Do transcript do Daniel:

> "Underneath the dotclaude directory in all caps is MEMORY, and under memory I have learning, signals, and all these different things."

> "I am taking [every prompt, every tool use, every output] and putting it inside of this memory structure and I'm overlaying on top of it sentiment analysis. This is all being done dynamically. I'm not seeing anything. It's all just handled automatically due to hooks."

A razão não é convenção - é **fluxo de dados**. O Claude Code já grava tudo em `~/.claude/` (history.jsonl, session-env/, etc.). MEMORY é uma **camada de processamento** em cima desses dados brutos. Faz sentido colocar onde os dados já estão.

---

## 4. O Sistema de Hooks (Middleware)

### 8 Eventos do Claude Code

| Evento | Quando | O que o Daniel faz |
|--------|--------|---------------------|
| `SessionStart` | Sessão inicia | Inicializa, carrega CORE skill, loga |
| `UserPromptSubmit` | Usuário envia mensagem | Security check, sentiment analysis, routing, atualiza tab |
| `PreToolUse` | Antes de executar tool | Valida segurança (10 tiers de ataque) |
| `PostToolUse` | Depois de executar tool | Loga resultado |
| `Stop` | AI termina resposta | Captura output, extrai voz |
| `SubagentStop` | Subagente termina | Captura output de agentes spawned |
| `SessionEnd` | Sessão fecha | Gera resumo da sessão para MEMORY |
| `PreCompact` | Antes de comprimir contexto | Salva informação importante |

### O que torna isso poderoso (do transcript)

> "I have 12 hooks that are active. I've got a whole bunch for user prompt submit. There's security checks. There's sentiment analysis checks. It's actually routing throughout the PI system according to what I'm trying to do based on this sentiment analysis which uses Haiku."

O Daniel usa hooks não só para capturar, mas para **routing inteligente** em tempo real:
- Haiku analisa o sentimento de cada interação
- O sistema ajusta comportamento baseado em satisfação
- Histogramas de felicidade com resultados
- Auto-upgrade: "we tried this, that didn't work, we went in another direction"

### Custom Inference Tool

3 níveis de inference embutidos no sistema:
- **Fast** = Haiku (sentiment analysis, routing, classificação)
- **Standard** = Sonnet (tasks normais)
- **Smart** = Opus (tasks complexas)

O sistema self-routes entre esses níveis baseado na complexidade da task.

---

## 5. O Algorithm (Peça Central)

```
CURRENT STATE ──────────────────────────────► IDEAL STATE
                    │
                    ▼
    ┌─────────────────────────────────┐
    │         THE ALGORITHM           │
    │                                 │
    │  OBSERVE → THINK → PLAN →      │
    │  BUILD → EXECUTE → VERIFY →    │
    │  LEARN                          │
    │                                 │
    │  (loop até VERIFY passar)       │
    └─────────────────────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────┐
    │      SIGNAL FEEDBACK            │
    │                                 │
    │  ratings → patterns → upgrades  │
    │  failures → learnings → skills  │
    └─────────────────────────────────┘
```

### As 7 Fases

1. **OBSERVE** - Coletar contexto, entender estado atual
2. **THINK** - Gerar hipóteses, analisar possibilidades
3. **PLAN** - Criar plano de execução, sequenciar trabalho
4. **BUILD** - Definir ISC (Ideal State Criteria) - o que "ideal" parece
5. **EXECUTE** - Implementar
6. **VERIFY** - Testar contra critérios do ISC
7. **LEARN** - Extrair learnings, atualizar MEMORY

**Conexão com MEMORY**: `Learning/` é organizado por essas fases. Learnings de uma task melhoram performance futura em cada fase específica.

### Effort Classification

| Nível | Modelos | Agentes paralelos |
|-------|---------|-------------------|
| TRIVIAL | nenhum | 0 |
| QUICK | haiku | 1 |
| STANDARD | haiku, sonnet | 1-3 |
| THOROUGH | haiku, sonnet | 3-5 |
| DETERMINED | todos + opus | 10 |

---

## 6. Stanford "Generative Agents" - A Inspiração

Paper: [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) (Stanford + Google, 2023)

O Daniel cita como inspiração para o sistema de memória. O conceito central é **Reflections**:

### Arquitetura de Memória do Paper

1. **Memory Stream** - Registro completo de experiências em linguagem natural
2. **Retrieval** - Busca por 3 critérios: recência, relevância (cosine similarity), importância (1-10)
3. **Reflections** - A cada ~100 memórias, o agente:
   - Propõe 3 perguntas de alto nível
   - Busca memórias relevantes para cada pergunta
   - Gera 5 insights de alto nível
   - Armazena esses insights de volta na memória

### Como o Daniel aplica isso

> "Sort of stealing from a Stanford idea called reflections where you get a whole bunch of context and you summarize it, maybe in one line or one paragraph."

> "Summarizations into indexes which can be parsed, and of course they could always go look at the raw log if they want to, but they should be able to go off of the index."

**Tradução para o PAI:**
- Raw data → `MEMORY/raw-outputs/` (JSONL bruto)
- Summarization → `MEMORY/sessions/` (resumos por sessão)
- Reflections → `MEMORY/Learning/` (insights curados por fase)
- Indexes → `MEMORY/session-events.jsonl` (index parseável rápido)
- Signals → `MEMORY/Signals/` (padrões detectados)

O fluxo é: **Captura bruta → Sumarização → Reflexão → Aplicação**

---

## 7. Skill System (4 Tiers de Loading)

### Tier 0: CORE (sempre carregado)
- Auto-load via hook no SessionStart
- ~10K tokens
- Contém: identidade, routing table, formato de resposta, referências para USER/ e SYSTEM/

### Tier 1: Frontmatter (routing table)
- YAML de cada SKILL.md carrega como "índice"
- Cláusula `USE WHEN` para matching de intenção
- Mínimo de tokens - só para o Claude saber que skills existem

### Tier 2: Full Skill (sob demanda)
- Corpo completo do SKILL.md carrega quando a skill é invocada
- 30-50 linhas por design

### Tier 3: Workflow (específico)
- Arquivo .md de workflow específico carrega quando roteado
- Execução passo-a-passo

### Formato de um SKILL.md

```yaml
---
name: SkillName
description: Personal AI Infrastructure core. AUTO-LOADS at session start.
  USE WHEN any session begins OR user asks about identity...
---

[Corpo com Workflow Routing table + Examples]
```

### Organização

```
skills/SkillName/
├── SKILL.md              ← Obrigatório
├── [Context].md           ← Arquivos de contexto (na raiz, NÃO em subdirs)
├── Tools/                 ← TypeScript tools
│   ├── ToolName.ts
│   └── ToolName.help.md
└── Workflows/             ← Procedimentos
    └── WorkflowName.md
```

**Regras**: TitleCase para tudo. Flat structure (max 2 níveis). Skills pessoais: `_BLOGGING`, `_METRICS`.

---

## 8. PAI 3.x - O que vem pela frente

Da [GitHub Discussion #500](https://github.com/danielmiessler/Personal_AI_Infrastructure/discussions/500):

### Mudanças planejadas
1. **Wizard/Install melhorado** - Pede API key upfront, Agent Installer como chat interface
2. **Update process** - Git-based release management, staging repo com CI/CD
3. **Config standardizada** - Movendo para `~/.config/PAI/` (novo padrão)
4. **Proteção de customizações** - Updates não destroem mais configurações do usuário
5. **Kayvan Sylvan** como novo MVP do projeto (profissionalizando com CI/CD, como fez no Fabric)

### Implicação para nós
O Daniel está movendo de `~/.claude/` para `~/.config/PAI/`. Isso separa ainda mais o PAI do Claude Code específico (portabilidade para outros engines como Open Code).

---

## 9. O que nós temos vs. O que o Daniel tem

### Capacidades que o Daniel tem e nós NÃO

| Capacidade | Daniel | Nós |
|------------|--------|-----|
| Session capture com conteúdo | ✅ Hook gera resumo ativo | ❌ Hook grava metadata vazia |
| Sentiment analysis | ✅ Haiku analisa cada interação | ❌ Não existe |
| Self-routing por complexidade | ✅ 3 níveis (haiku/sonnet/opus) | ❌ Não existe |
| Signal detection | ✅ failures, loopbacks, patterns, ratings | ❌ Estrutura existe mas vazia |
| Learning por fase do Algorithm | ✅ OBSERVE→LEARN com curadoria | ❌ Diretórios existem mas vazios |
| JSONL event stream | ✅ capture-all-events.ts | ❌ Não temos esse hook |
| Work/ por task | ✅ ISC, TRACE, Output | ❌ Não existe |
| Algorithm como skill | ✅ 7 fases + tools + capabilities | ❌ Não existe |
| 65+ skills | ✅ Blogging, Research, Art, Browser... | ⚡ 4 skills (CORE, CapturePdf, CreateSkill, DailyGoals) |
| Voice integration | ✅ 11Labs TTS | ❌ Não existe |
| Observability dashboard | ✅ localhost:4000 | ❌ Não existe |

### O que nós temos de CERTO

| O que fizemos | Status |
|---------------|--------|
| CORE skill auto-load via hook | ✅ Funcionando |
| Security validator | ✅ Funcionando |
| Tab titles | ✅ Funcionando |
| Identidade pessoal (IDENTITY/PROJECTS) | ✅ Funcionando |
| Portabilidade via symlinks | ✅ Funcionando em 2 máquinas |
| Skills versionadas no git | ✅ .claude-config/skills/ |
| Hooks versionados no git | ✅ .claude-config/hooks/ |

### Problemas estruturais atuais

1. **MEMORY duplicado**: `~/.claude/MEMORY/` (vazio/template) + `ai-brain/MEMORY/` (dados reais)
2. **Skills duplicadas**: `~/.claude/skills/` (cópia real) + `.claude-config/skills/` (fonte)
3. **`pai/` como conceito separado**: Deveria ser `skills/CORE/USER/` como no Daniel
4. **Session capture vazia**: Hook grava metadata, não conteúdo
5. **Sem JSONL event stream**: Não capturamos os dados brutos que alimentam tudo

---

## 10. Decisões a tomar (próxima conversa)

Estas são as decisões que precisamos discutir:

### A. Estrutura de diretórios
- Onde MEMORY vive? (ai-brain git vs ~/.claude/ runtime)
- Unificar skills (symlink único)?
- Migrar pai/ para skills/CORE/USER/?
- Seguir ou não a mudança para ~/.config/PAI/ (PAI 3.x)?

### B. Prioridade de capacidades
- O que construir primeiro? Session capture? Signal system? Algorithm?
- Precisamos de sentiment analysis agora ou é premature optimization?
- O JSONL event stream é pré-requisito para tudo?

### C. Modelo de portabilidade
- ai-brain como source of truth para código/config (current model)?
- MEMORY compartilhado entre repos ou por-máquina?
- Como funciona em sistema-os (Duke)?

### D. Escopo
- Quanta complexidade do Daniel queremos replicar agora?
- O que é essencial vs. nice-to-have para o nosso cenário?

---

## Fontes

- Transcript: `sources/2026-01-26-unsupervised-learning-how-and-why-i-built-pai-with-nathan-labenz.md`
- PAI Repo: `/home/alejandro/Personal_AI_Infrastructure/`
- [GitHub Discussion #500 - PAI 3.x](https://github.com/danielmiessler/Personal_AI_Infrastructure/discussions/500)
- [Stanford Generative Agents Paper](https://arxiv.org/abs/2304.03442)
- Nossos docs: `projects/ai-brain/PAI-PORTAVEL.md`, `projects/ai-brain/PAI-VISAO-MACRO.md`
