# PAI - Visão Macro (Referência)

> Conceitos extraídos dos documentos do Daniel Miessler (Unsupervised Learning).
> Fonte: `sources/2025-12-16-unsupervised-learning-a-deepdive-on-my-personal-ai-infrastructure-pai-v2.md`
> Capturado: 2026-01-27

---

## O Que É o PAI

PAI (Personal AI Infrastructure) é um **sistema unificado de augmentação humana**. Não é sobre tecnologia - é tech a serviço de humanos.

```
┌─────────────────────────────────────────────────────────────────┐
│                         PAI - VISÃO MACRO                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   HUMANO ──────► TECH/AI ──────► HUMANO                        │
│   (input)        (meio)          (outcome)                      │
│                                                                 │
│   "Tech should disappear. Focus on human connection."           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Problema que Resolve (World Problems)

```
WP1: Falta de propósito/significado → mental health, societal problems
         │
         ▼
WP2: IA vai exacerbar isso → disruption de trabalho de conhecimento
         │
         ▼
WP3: Humanos treinados para serem úteis economicamente, não "full spectrum"
```

---

## Princípios Fundamentais

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRINCÍPIOS FUNDAMENTAIS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Clear Thinking → Clear Writing → Clear Prompting → Good AI │
│                                                                 │
│  2. SCAFFOLDING > MODEL (estrutura > inteligência)             │
│                                                                 │
│  3. CODE BEFORE PROMPTS (80% code / 20% prompts)               │
│                                                                 │
│  4. UNIX PHILOSOPHY (pequeno, modular, composável)             │
│                                                                 │
│  5. SOLVE ONCE, REUSE FOREVER                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Algoritmo Fundamental: Two Loops

```
┌─────────────────────────────────────────────────────────────────┐
│                       THE TWO LOOPS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  OUTER LOOP:                                                    │
│  ┌──────────────┐                    ┌──────────────┐          │
│  │ CURRENT STATE │ ──────────────►  │ DESIRED STATE │          │
│  └──────────────┘                    └──────────────┘          │
│                                                                 │
│  INNER LOOP (7 fases):                                         │
│                                                                 │
│    OBSERVE ──► THINK ──► PLAN ──► BUILD                        │
│       ▲                              │                          │
│       │                              ▼                          │
│    LEARN ◄── VERIFY ◄── EXECUTE                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estrutura do Sistema (como Daniel organiza o Kai)

```
~/.claude/
├── context/              ← CORAÇÃO DO SISTEMA (UFC)
│   ├── active/           ← Projetos ativos
│   ├── identity/         ← TELOS (quem sou)
│   ├── tools/            ← Ferramentas disponíveis
│   │   ├── mcps/
│   │   ├── commands/
│   │   └── fobs/
│   └── history/          ← Sessions, learnings, decisions
├── agents/               ← Developer, Researcher, etc
├── skills/               ← 65+ skills (Art, Content, etc)
├── hooks/                ← Automações (load context, etc)
└── commands/             ← Slash commands
```

---

## Os 5 Projetos do Daniel e Como se Encaixam

```
┌─────────────────────────────────────────────────────────────────┐
│                   ECOSSISTEMA DANIEL MIESSLER                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     HUMAN 3.0                            │   │
│  │         (framework + plataforma para upgrade)            │   │
│  └─────────────────────────────────────────────────────────┘   │
│           ▲           ▲           ▲           ▲                 │
│           │           │           │           │                 │
│  ┌────────┴──┐ ┌──────┴────┐ ┌────┴────┐ ┌────┴────┐           │
│  │ SUBSTRATE │ │  FABRIC   │ │  TELOS  │ │  DAMON  │           │
│  │           │ │           │ │         │ │         │           │
│  │ biblioteca│ │ prompts   │ │ contexto│ │ API     │           │
│  │ de compo- │ │ para      │ │ profundo│ │ pessoal │           │
│  │ nentes    │ │ problemas │ │ sobre   │ │ para o  │           │
│  │ transpa-  │ │ humanos   │ │ o que   │ │ mundo   │           │
│  │ rentes    │ │           │ │ importa │ │         │           │
│  └───────────┘ └───────────┘ └─────────┘ └─────────┘           │
│                                                                 │
│  TODOS baseados em: TEXTO + MARKDOWN + FILE SYSTEM             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Níveis de Maturidade AI (AIMM)

```
┌─────────────────────────────────────────────────────────────────┐
│                        AIMM MODEL                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Level 0: NATURAL (pré-2022)                                   │
│           Humano faz tudo sozinho                               │
│                                                                 │
│  Level 1: CHATBOTS (2023-2025)                                 │
│           Perguntas → Respostas → Trabalho manual              │
│                                                                 │
│  Level 2: AGENTIC (2025-2027) ◄── ESTAMOS AQUI                 │
│           Plataformas que magnificam efetividade               │
│           Learning tasks, context, tooling                     │
│                                                                 │
│  ─────────────── TRANSIÇÃO HUMAN→AI CENTERED ──────────────    │
│                                                                 │
│  Level 3: WORKFLOWS (2027?)                                    │
│           Trabalho decomposto em pipelines AI                  │
│                                                                 │
│  Level 4: MANAGED (2030?)                                      │
│           AI captura estado e faz ajustes contínuos            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Decisão: Goal → Implementation

```
┌─────────────────────────────────────────────────────────────────┐
│              GOAL → CODE → CLI → PROMPTS → AGENTS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. GOAL         O que quero fazer?                            │
│       │                                                         │
│       ▼                                                         │
│  2. CODE?        Posso fazer em código determinístico?         │
│       │          (SIM = mais confiável, mais barato)           │
│       ▼                                                         │
│  3. CLI TOOL     Código vira ferramenta de linha de comando    │
│       │          (documentada, flags, help)                    │
│       ▼                                                         │
│  4. PROMPTS      Prompts chamam as CLI tools                   │
│       │                                                         │
│       ▼                                                         │
│  5. AGENTS       Skills/Agents orquestram tudo                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Roadmap PAI (aplicado ao ai-brain)

```
┌─────────────────────────────────────────────────────────────────┐
│                        ROADMAP PAI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 0: CLAREZA ✅                                            │
│  → 2 repos, 3 frentes bem definidas                            │
│                                                                 │
│  FASE 1: PAI PORTÁVEL ✅                                       │
│  → pai/IDENTITY.md + pai/PROJECTS.md                           │
│  → symlinks em ~/.claude/pai/                                  │
│  → Contexto pessoal em QUALQUER repo                           │
│                                                                 │
│  FASE 2: SESSION CAPTURE GLOBAL ⏳                             │
│  → Melhorar session-capture.ts                                 │
│  → Toda sessão gera resumo útil                                │
│                                                                 │
│  FASE 3: AFINAR ⏳                                             │
│  → Melhorar formato das sessions                               │
│  → Edita em ai-brain → impacta TODOS os repos                  │
│                                                                 │
│  FASE 4: WORKFLOWS AVANÇADOS ⏳                                │
│  → Daily review (consolidar sessões)                           │
│  → Contexto de projeto (estado atual ao abrir)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fontes

- `sources/2025-12-16-unsupervised-learning-a-deepdive-on-my-personal-ai-infrastructure-pai-v2.md`
- `sources/2026-01-26-unsupervised-learning-how-and-why-i-built-pai-with-nathan-labenz.md`
- `sources/2024-10-15-unsupervised-learning-how-my-projects-fit-together-substrate-fabric-telo.md`
- `sources/2025-09-04-unsupervised-learning-building-your-own-unified-ai-assistant-using-claud.md`
