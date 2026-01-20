# AI Brain - Parceiro Digital Pessoal

**Status:** Operacional (modelo file-based PAI-style)

## O que é

Um parceiro digital que sabe tudo da minha vida. Não é assistente que executa comandos - é parceiro que entende contexto, conecta ideias e me relembra do que precisa ser relembrado.

> "Ferramenta que cria o cenário ideal pra que você possa dar vazão a todas as ideias, potencial, vontades e objetivos que você tem na vida - de forma organizada e estruturada."

## Por que construir isso

### Problema
Toda ferramenta de produtividade que usei morreu da mesma forma: exige manutenção manual, fica desatualizada, paro de confiar, paro de usar.

### Solução
Sistema que trabalha **junto** comigo:
- Captura acontece naturalmente (conversas com Claude)
- Hooks gravam sessões automaticamente
- Claude lê arquivos nativamente (sem scripts intermediários)

### Conexão estratégica
Este AI Brain pessoal é protótipo da interface que funcionários de hotel usarão no futuro. Mesma lógica: falar naturalmente em vez de navegar menus e preencher campos.

---

## Arquitetura (File-Based)

```
┌────────────────────────────────────────────────────────────┐
│  AI BRAIN - MODELO FILE-BASED (PAI-style)                  │
│                                                            │
│   VOCÊ CONVERSA                                            │
│        │                                                   │
│        ▼                                                   │
│   ┌─────────────┐                                          │
│   │ Claude Code │  ← Você trabalha aqui                    │
│   │  (terminal) │                                          │
│   └──────┬──────┘                                          │
│          │                                                 │
│          │ Stop hook → session-capture.ts                  │
│          ▼                                                 │
│   ┌─────────────────────────────────────────┐              │
│   │         MEMORY/ (file system)           │              │
│   │                                         │              │
│   │   sessions/   → logs de sessão (auto)   │              │
│   │   decisions/  → decisões importantes    │              │
│   │   learnings/  → aprendizados por fase   │              │
│   │   State/      → estado ativo            │              │
│   │   Signals/    → padrões e falhas        │              │
│   │                                         │              │
│   └─────────────────────────────────────────┘              │
│                                                            │
│   sources/ → PDFs, artigos, vídeos capturados              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Por que file-based?

| Antes (Supabase/Embeddings) | Agora (File-based) |
|-----------------------------|---------------------|
| Scripts externos para busca | Claude lê direto |
| Processamento de embeddings | Zero processamento |
| Cron jobs cada 15 min | Hooks no momento certo |
| Infraestrutura externa | Apenas arquivos |

---

## Quick Start

### Comandos principais

| Comando | Descrição |
|---------|-----------|
| `/goals` ou `/metas` | Ver progresso das metas pessoais |
| `/pdf` | Capturar PDF para sources |
| `ls MEMORY/sessions/` | Ver sessões recentes |

### Captura de conteúdo

```bash
# YouTube
python3 scripts/capture_youtube.py <url>

# Artigo web
python3 scripts/capture_article.py <url>

# PDF
python3 scripts/capture_pdf.py /path/to/file.pdf --author "Autor" --title "Título"
```

### Consultar memória

```bash
# Sessões recentes
ls -la ~/ai-brain/MEMORY/sessions/

# Buscar termo
grep -r "termo" ~/ai-brain/MEMORY/

# Estado ativo
cat ~/ai-brain/MEMORY/State/active-work.json
```

---

## Estrutura MEMORY/

```
MEMORY/
├── sessions/          # Auto-capturado pelo hook Stop
│   └── YYYY-MM-DD-{session_id}.md
├── decisions/         # Decisões importantes
├── learnings/         # Aprendizados por fase do ciclo PAI
│   ├── OBSERVE/       # Observações e descobertas
│   ├── THINK/         # Análises e reflexões
│   ├── PLAN/          # Planos e estratégias
│   ├── BUILD/         # O que aprendi construindo
│   ├── EXECUTE/       # O que aprendi executando
│   └── VERIFY/        # Validações
├── State/
│   └── active-work.json   # Trabalho atual
└── Signals/
    ├── failures.jsonl     # Erros para análise
    └── patterns.jsonl     # Padrões detectados
```

---

## Stack

| Componente | Tecnologia | Por quê |
|------------|------------|---------|
| Core | Claude Code CLI + Hooks | Acesso direto a features novas |
| Interface | Terminal | Zero setup |
| Memória | File system (MEMORY/) | Claude lê nativamente |
| Conhecimento | sources/ (markdown) | Busca via Grep/Read |
| Hooks | TypeScript + Bun | Performance + tipagem |

---

## Arquivos do projeto

```
projects/ai-brain/
├── README.md      ← Você está aqui
├── ROADMAP.md     ← Marcos e fases
├── SETUP.md       ← Configs técnicas
├── REFERENCES.md  ← Material de estudo
├── CHANGELOG.md   ← Histórico de decisões
├── telos/
│   └── TELOS-ALE.md       ← Contexto profundo pessoal
├── metas/
│   ├── README.md          ← Visão geral
│   ├── MACONHA.md         ← Tracking: redução
│   └── SAUDE.md           ← Tracking: 5/3/1 + cardio
├── guides/
│   ├── FABRIC-ALL-PATTERNS.md      ← 234 patterns
│   └── FABRIC-TELOS-PATTERNS.md    ← 16 patterns TELOS
└── archive/
    └── (rascunhos anteriores)
```

---

## Migração (2026-01-20)

Sistema anterior (Supabase + embeddings + pgvector) foi substituído por modelo file-based.

**Backup disponível em:** `~/ai-brain-backup-20260120/`

Contém:
- Scripts de embeddings removidos
- Schemas SQL
- Configuração do cron

---

## Links úteis

- [ROADMAP.md](./ROADMAP.md) - Próximos passos
- [SETUP.md](./SETUP.md) - Configurar ambiente
- [REFERENCES.md](./REFERENCES.md) - Material de estudo (Hillman, Nate, Miessler)
- [MEMORY/README.md](../../MEMORY/README.md) - Documentação do sistema de memória
