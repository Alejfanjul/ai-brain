# AI Brain - Parceiro Digital Pessoal

**Status:** Em desenvolvimento (Marco 3 em progresso)

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

## O que o sistema precisa fazer

### Entrada
- [x] Receber texto (Claude Code terminal)
- [ ] Receber áudio (transcrever)
- [ ] Receber imagem / print de tela

### Processamento
- [x] Entender contexto da mensagem
- [x] Identificar tipo (decisão, insight, padrão, etc.)
- [x] Salvar com embeddings para busca semântica
- [ ] Conectar com informações relacionadas automaticamente
- [ ] Cruzar conversas com conteúdos capturados (sources)

### Proatividade
- [ ] Daily digest - o que importa hoje
- [ ] Acompanhar projetos - perguntar como está a evolução
- [ ] Detectar padrões - sugerir automações
- [ ] Me procurar na hora certa (não eu procurando ele)

### Saída
- [x] Responder no momento
- [x] Gravar no local adequado (Supabase)
- [ ] Criar lembretes
- [ ] Avisar outras pessoas/sistemas quando necessário

## Como funciona hoje

```
┌────────────────────────────────────────────────────────────┐
│  AI BRAIN - ARQUITETURA ATUAL                              │
│                                                            │
│   VOCÊ CONVERSA                                            │
│        │                                                   │
│        ▼                                                   │
│   ┌─────────────┐                                          │
│   │ Claude Code │  ← Você trabalha aqui                    │
│   │  (terminal) │                                          │
│   └──────┬──────┘                                          │
│          │                                                 │
│          │ (hooks gravam automaticamente)                  │
│          ▼                                                 │
│   ┌─────────────────────────────────────────┐              │
│   │         SUPABASE (banco de dados)       │              │
│   │                                         │              │
│   │   conversas    → 109+ sessões           │              │
│   │   mensagens    → 1000+ mensagens        │              │
│   │   memorias     → 40 memórias            │              │
│   │   source_chunks→ 218/910 processados    │              │
│   │                                         │              │
│   └─────────────────────────────────────────┘              │
│                                                            │
│   CRON JOBS (automático):                                  │
│   ┌──────────────────────────────────────┐                 │
│   │ */5 min  → sync_sessions.py          │                 │
│   │ */15 min → extract_memories.py       │                 │
│   │            (Claude Haiku extrai      │                 │
│   │             decisões, insights...)   │                 │
│   └──────────────────────────────────────┘                 │
│                                                            │
│   EMBEDDINGS (busca semântica):                            │
│   ┌──────────────────────────────────────┐                 │
│   │ Ollama (local) → nomic-embed-text    │                 │
│   │ 768 dimensões por chunk              │                 │
│   │ pgvector no Supabase                 │                 │
│   └──────────────────────────────────────┘                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Stack

| Componente | Tecnologia | Por quê |
|------------|------------|---------|
| Core | Claude Code CLI + Hooks | Acesso direto a features novas |
| Interface | Terminal | Zero setup |
| Banco | Supabase (free tier) | PostgreSQL grátis |
| Vetorial | pgvector | Busca semântica |
| Embeddings | Ollama (local) | Sem custo de API |

## Arquivos do projeto

```
projects/ai-brain/
├── README.md      ← Você está aqui (visão + estado atual)
├── ROADMAP.md     ← Marcos e fases de implementação
├── SETUP.md       ← Configs técnicas, SQLs, cron
├── REFERENCES.md  ← Quotes e material de consulta
└── CHANGELOG.md   ← Histórico de decisões
```

## Links úteis

- [ROADMAP.md](./ROADMAP.md) - Ver próximos passos
- [SETUP.md](./SETUP.md) - Configurar ambiente
- [REFERENCES.md](./REFERENCES.md) - Material de estudo (Hillman, Nate)
