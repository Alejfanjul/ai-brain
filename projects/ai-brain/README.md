# AI Brain - Parceiro Digital Pessoal

**Status:** Migração para modelo file-based (PAI-style)

## O que é

Um parceiro digital que sabe tudo da minha vida. Não é assistente que executa comandos - é parceiro que entende contexto, conecta ideias e me relembra do que precisa ser relembrado.

> "Ferramenta que cria o cenário ideal pra que você possa dar vazão a todas as ideias, potencial, vontades e objetivos que você tem na vida - de forma organizada e estruturada."

## Por que construir isso

### Problema
Toda ferramenta de produtividade que usei morreu da mesma forma: exige manutenção manual, fica desatualizada, paro de confiar, paro de usar.

### Solução
Sistema que trabalha **junto** comigo:
- Captura acontece naturalmente (conversas com Claude)
- IA classifica e organiza automaticamente
- Sistema me procura com o que importa (não eu procurando nele)

### Conexão estratégica
Este AI Brain pessoal é protótipo da interface que funcionários de hotel usarão no futuro. Mesma lógica: falar naturalmente em vez de navegar menus e preencher campos.

## Arquitetura Atual (File-Based)

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
│          │ (hooks capturam automaticamente)                │
│          ▼                                                 │
│   ┌─────────────────────────────────────────┐              │
│   │         MEMORY/ (file system)           │              │
│   │                                         │              │
│   │   sessions/   → logs de sessão          │              │
│   │   decisions/  → decisões importantes    │              │
│   │   learnings/  → aprendizados por fase   │              │
│   │   State/      → estado ativo            │              │
│   │   Signals/    → padrões e falhas        │              │
│   │                                         │              │
│   └─────────────────────────────────────────┘              │
│                                                            │
│   VANTAGEM: Claude Code lê nativamente                     │
│   (sem scripts de busca, sem embeddings externos)          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Stack

| Componente | Tecnologia | Por quê |
|------------|------------|---------|
| Core | Claude Code CLI + Hooks | Acesso direto a features novas |
| Interface | Terminal | Zero setup |
| Memória | File system (MEMORY/) | Claude lê nativamente |
| Conhecimento | sources/ (markdown) | Busca via Grep/Read |

## Arquivos do projeto

```
projects/ai-brain/
├── README.md      ← Você está aqui (visão + estado atual)
├── ROADMAP.md     ← Marcos e fases de implementação
├── SETUP.md       ← Configs técnicas
├── REFERENCES.md  ← Quotes e material de consulta
├── CHANGELOG.md   ← Histórico de decisões
├── telos/
│   └── TELOS-ALE.md       ← Contexto profundo pessoal
├── metas/
│   ├── README.md          ← Visão geral das metas
│   ├── MACONHA.md         ← Tracking: redução de maconha
│   └── SAUDE.md           ← Tracking: 5/3/1 + cardio
├── guides/
│   ├── FABRIC-ALL-PATTERNS.md      ← 234 patterns disponíveis
│   └── FABRIC-TELOS-PATTERNS.md    ← 16 patterns para TELOS
└── archive/
    └── (conversas e rascunhos anteriores)
```

## Links úteis

- [ROADMAP.md](./ROADMAP.md) - Ver próximos passos
- [SETUP.md](./SETUP.md) - Configurar ambiente
- [REFERENCES.md](./REFERENCES.md) - Material de estudo (Hillman, Nate)
