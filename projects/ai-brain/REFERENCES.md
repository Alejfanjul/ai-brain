# AI Brain - Referências

Material de estudo e inspiração para o projeto.

---

## Alex Hillman - JFDI System

Alex Hillman, fundador do Indie Hall (coworking em Philadelphia), construiu um sistema similar chamado **JFDI System** em ~3 semanas de desenvolvimento ativo.

### Por que importa

> "Has already had a materially positive impact on my life, my productivity, my happiness. Most importantly, my executive function where open loops really are a challenge for me."

### Quotes importantes

**Sobre o problema:**
> "Every project management tool I've ever used had the same problem - what it expects from me. I'm the worst at going in and keeping them current."

**Sobre proatividade:**
> "The dream of an assistant who you wake up in the morning and your day is prepared for you."

**Sobre memória simples:**
> "You can get so much value out of this without vector search. Don't let people tell you that you need fancy databases with vector search to get the power."

**Sobre transparência:**
> "Trust through transparency - I design things to provide me maximum transparency and then as a byproduct that transparency becomes value to both me and the system."

**Sobre documentação:**
> "Almost everything of meaning that this system does is basically a giant SOP or collection of SOPs. And I found that it's very very good at writing instructions better than I've ever been."

**Sobre Claude Code:**
> "I am not hitting Anthropic's API directly for anything. Everything is going through Claude Code using Claude Code headless mode."

### Links

- [YouTube: JFDI System Demo](https://www.youtube.com/watch?v=Wpz7LNI737Q)
- Source local: `sources/2025-12-13-alex-hillman-jfdi-system-my-ai-executive-assistant-full-life-co.md`

---

## Nate - Second Brain 2026

Newsletter de 2026-01-09 sobre por que sistemas de segundo cérebro falham e como construir um que funciona.

### Por que importa

Nate identifica os mesmos problemas que estamos resolvendo e propõe uma arquitetura com 8 building blocks e 12 princípios.

### Os 8 Building Blocks

| Block | Descrição | Tradução |
|-------|-----------|----------|
| Drop Box | Lugar único de captura zero-fricção | Inbox |
| Sorter | IA classifica automaticamente | Classificador |
| Form | Schema consistente | Estrutura |
| Filing Cabinet | Onde vive a verdade | Banco de dados |
| Receipt | Audit trail do que foi feito | Log |
| Bouncer | Filtro de confiança | Guardião |
| Tap on the Shoulder | Digests diários/semanais | Proatividade |
| Fix Button | Correção trivial de erros | Ajuste fácil |

### Quotes importantes

**Sobre o problema:**
> "Most second brain systems die the same death. You find a tool, set it up with real enthusiasm, capture notes for a few weeks. Then the pile gets messy. You stop trusting it. You stop using it."

**Sobre a mudança em 2026:**
> "What changed in 2026 is the shift from AI inside your notes to AI running a loop. That difference is enormous."

**Sobre proatividade:**
> "Humans don't retrieve consistently. We don't wake up and think 'I should search my databases.' But we do respond to what shows up in front of us."

**Sobre qualidade:**
> "The fastest way to kill a system is to fill it with garbage."

**Sobre correções:**
> "Corrections must be trivial or people won't make them."

**Sobre simplicidade:**
> "Reduce the human's job to one reliable behavior. If your system requires three behaviors, you don't have a system—you have a self-improvement program."

**Sobre leverage:**
> "AI is a multiplier, and multipliers are only as powerful as what they multiply. A 10x boost to shallow knowledge produces shallow output faster. A 10x boost to someone who genuinely understands the domain produces something qualitatively different."

### 12 Princípios

1. Reduce the human's job to one reliable behavior
2. Separate memory from compute from interface
3. Treat prompts like APIs, not creative writing
4. Build trust mechanisms, not just capabilities
5. Default to safe behavior when uncertain
6. Make outputs small, frequent, and actionable
7. Use "next action" as the unit of execution
8. Prefer routing over organizing
9. Keep categories and fields painfully small
10. Design for restart, not perfection
11. Build one workflow, then attach modules
12. Optimize for maintainability over cleverness

### Link

- Source local: `sources/2026-01-09-nate-why-every-system-youve-tried-has-failed-grab-the-9.md`

---

## Analogias Lúdicas

Explicação dos arquivos de projeto usando analogias do mundo real.

| Arquivo | Analogia | Descrição |
|---------|----------|-----------|
| **README.md** | Estrela Polar | Quando você está perdido às 2h da manhã, olha pra cima e lembra por que está fazendo isso |
| **ROADMAP.md** | Mapa da Viagem | As cidades pelas quais você precisa passar. "Você está aqui" |
| **SETUP.md** | Manual de Instruções | Como montar e configurar a máquina |
| **REFERENCES.md** | Biblioteca | Material de consulta e inspiração |
| **CHANGELOG.md** | Diário de Bordo | "12/Jan - Tempestade! Perdemos uma vela, mas sobrevivemos" |

### Visualização: ROADMAP como Trilha

```
┌─────────────────────────────────────────────────────────┐
│  JORNADA DO PROJETO                                     │
│                                                         │
│     ✅ Marco 1       ✅ Marco 2       ⚡ Marco 3        │
│     Audit Trail      Persistência     File-based        │
│                                                         │
│  ───●━━━━━━━━━━━━━●━━━━━━━━━━━━━●━━━━━━━━━━●════○───   │
│                                             │    │      │
│                                           VOCÊ Marco 4  │
│                                           ESTÁ Futuro   │
│                                           AQUI          │
└─────────────────────────────────────────────────────────┘
```

### Visualização: Componentes do Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    AI BRAIN                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   📥 DROP BOX      🤖 SORTER        📋 FORM            │
│   "Joga aqui"      "IA organiza"    "Estrutura fixa"   │
│                                                         │
│   🗄️ CABINET       📜 RECEIPT       🚪 BOUNCER         │
│   "Onde guarda"    "O que fez"      "Filtro qualidade" │
│                                                         │
│   👋 TAP           🔧 FIX                               │
│   "Te procura"     "Corrige fácil"                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Manus - Context Engineering

Artigo sobre engenharia de contexto para agentes IA (referência do Ale em 2026-01-06).

### Por que importa

> "O que o Manus construiu que vale $2B não é o modelo, é o 'harness' - toda a engenharia de contexto ao redor."

### Princípios aplicáveis ao AI Brain

- File system como memória (já fazemos com `sources/` e `projects/`)
- Recitação de objetivos (hooks de retrieval vão implementar)
- Manter erros visíveis (memórias tipo "correção" e "aprendizado")

### Link

- Source local: `sources/2026-01-06-manus-context-engineering-for-ai-agents-lessons-from-bui.md`

---

## Daniel Miessler - PAI Ecosystem

Daniel Miessler construiu um ecossistema completo de projetos open source para IA pessoal.

### Repositórios Principais (clonados localmente)

| Repo | Propósito | Local |
|------|-----------|-------|
| **PAI** | Arquitetura de IA pessoal | `~/Personal_AI_Infrastructure` |
| **Fabric** | 234 prompts prontos | `~/Fabric` |
| **Substrate** | Organização de conhecimento | `~/Substrate` |

### Outros Repos (referência)

| Repo | URL | Descrição |
|------|-----|-----------|
| TELOS | github.com/danielmiessler/Telos | Template de contexto pessoal |
| Daemon | github.com/danielmiessler/Daemon | Agente autônomo |

### Relação ai-brain ↔ Ecossistema Miessler

```
┌─────────────────────────────────────────────────────────────┐
│                      ai-brain                                │
│                (implementação pessoal)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│   │     PAI     │  │   Fabric    │  │  Substrate  │        │
│   │ (estrutura) │  │  (prompts)  │  │   (dados)   │        │
│   └─────────────┘  └─────────────┘  └─────────────┘        │
│         ↓                ↓                ↓                 │
│   Skills/Hooks    Patterns prontos   Taxonomias            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Quando usar cada repo

| Situação | Usar |
|----------|------|
| Criar novo skill | PAI → ver estrutura de skills |
| Analisar conteúdo | Fabric → buscar pattern existente |
| Criar hook | PAI → ver exemplos de hooks |
| Estruturar conhecimento | Substrate → ver categorias |
| Extrair insights | Fabric → `extract_wisdom`, `extract_ideas` |
| Criar resumo | Fabric → `create_summary`, `summarize` |

### Guias Locais

| Arquivo | Conteúdo |
|---------|----------|
| `guides/FABRIC-ALL-PATTERNS.md` | Catálogo dos 234 patterns do Fabric |
| `guides/FABRIC-TELOS-PATTERNS.md` | 16 patterns específicos para TELOS |

### Sources Capturados

| Arquivo | Conteúdo |
|---------|----------|
| `sources/2025-12-16-unsupervised-learning-a-deepdive-on-my-personal-ai-infrastructure-pai-v2.md` | Vídeo 48min + blog completo sobre PAI v2 |
| `sources/2026-01-11-danielmiessler-personal-ai-maturity-model-paimm.md` | PAIMM - 9 níveis de maturidade |
| `sources/2024-10-15-unsupervised-learning-how-my-projects-fit-together-substrate-fabric-telo.md` | Vídeo 66min explicando como projetos se conectam |

### Quotes Importantes

**Sobre Scaffolding:**
> "If I had to choose between the latest model with not very good scaffolding or excellent scaffolding with a model from 6 months ago, I would definitely pick the latter."

**Sobre Code Before Prompts:**
> "Prompts wrap code, not replace it. 80% deterministic code, 20% prompts for orchestration."

**Sobre Clareza:**
> "Clear Thinking → Clear Writing → Clear Prompting → High AI Efficacy"

**Sobre TELOS:**
> "Once the AI sees everything—purpose, goals, challenges, strategies, KPIs—now we can start asking questions. We can start taking actions. It's absolutely insane what you can do."

### Links Externos

- [How My Projects Fit Together](https://danielmiessler.com/blog/how-my-projects-fit-together)
- [Personal AI Infrastructure](https://danielmiessler.com/blog/personal-ai-infrastructure)
- [Personal AI Maturity Model](https://danielmiessler.com/blog/personal-ai-maturity-model)
