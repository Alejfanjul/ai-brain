# Jornada PAI - Aprendendo com Daniel Miessler

> **Objetivo:** Entender a filosofia, metodologia e arquitetura do PAI (Personal AI Infrastructure) para construir um sistema similar aplicado a gestão de hotel.

## Por que estudar isso?

O Daniel Miessler construiu ao longo de anos um sistema que:
- **Aprende sozinho** - captura feedback de cada interação
- **Se atualiza automaticamente** - monitora fontes e evolui
- **É determinístico** - 80% código, 20% prompts
- **É modular** - skills compostos, UNIX philosophy

Isso é exatamente o que queremos para o Duke Beach Hotel.

## O Ecossistema

```
┌─────────────────────────────────────────────────────────────┐
│                      HUMAN 3.0                              │
│         (Visão: humanos magnificados por IA)                │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │  TELOS  │          │   PAI   │          │  DAEMON │
   │ Contexto│◄────────►│ Sistema │◄────────►│   API   │
   │ Profundo│          │   IA    │          │ Pessoal │
   └─────────┘          └─────────┘          └─────────┘
        │                     │                     │
        │              ┌──────┴──────┐              │
        │              │             │              │
        ▼              ▼             ▼              ▼
   ┌─────────┐    ┌─────────┐  ┌─────────┐   ┌─────────┐
   │ FABRIC  │    │  SKILLS │  │  HOOKS  │   │SUBSTRATE│
   │ Prompts │    │Capacid. │  │ Eventos │   │Argumento│
   │ p/Probs │    │Modulares│  │Automát. │   │Transpar.│
   └─────────┘    └─────────┘  └─────────┘   └─────────┘
```

---

## Status Atual

**Fase 1: TELOS - Em andamento (~70%)**

- [x] Repositórios clonados (PAI, TELOS, Fabric, Daemon, Substrate)
- [x] Guias de patterns criados
- [x] Perfil V5 limpo e estruturado
- [x] Plano de entrevista criado
- [x] Conversas 01-03 realizadas (Propósito, Camada profunda, Pilares)
- [x] **TELOS-ALE.md** consolidado (2026-01-17)
- [ ] Próximas conversas: Metas concretas, Métricas, Estratégias
- [ ] Criar TELOS do Duke Beach Hotel

---

## Estrutura do Projeto

```
pai-study/
├── README.md           ← Este arquivo
├── ROADMAP.md          ← Plano de 4 fases
├── TELOS-ALE.md        ← TELOS pessoal consolidado (documento principal)
├── REFERENCES.md       ← Links e sources capturados
├── guides/
│   ├── FABRIC-ALL-PATTERNS.md      ← Guia dos 234 patterns
│   └── FABRIC-TELOS-PATTERNS.md    ← 16 patterns para TELOS
└── archive/
    ├── ALE-PERFIL-LIMPO.md         ← Perfil V5 (anterior)
    ├── TELOS-CONVERSA-01.md        ← Conversa 01
    ├── TELOS-CONVERSA-02.md        ← Conversa 02
    └── TELOS-INTERVIEW-PLAN.md     ← Plano de entrevista (executado)
```

**Projeto relacionado:** `projects/ai-pms/` - Sistema hoteleiro AI-Native (aplicação prática)

---

## Repositórios Clonados

| Repo | Local | Descrição |
|------|-------|-----------|
| **PAI** | `/home/marketing/pai-reference/` | Sistema completo (skills, hooks, memory) |
| **TELOS** | `/home/marketing/telos-reference/` | Templates de contexto pessoal/corporativo |
| **Fabric** | `/home/marketing/fabric-reference/` | 234 patterns de prompts |
| **Daemon** | `/home/marketing/daemon-reference/` | API pessoal broadcast |
| **Substrate** | `/home/marketing/substrate-reference/` | Argumentos estruturados |

---

## Sources Capturados

| Arquivo | Descrição |
|---------|-----------|
| `sources/2025-12-16-unsupervised-learning-a-deepdive-on-my-personal-ai-infrastructure-pai-v2.md` | Deep dive completo no PAI |
| `sources/2026-01-11-danielmiessler-personal-ai-maturity-model-paimm.md` | Modelo de maturidade (9 níveis) |
| `sources/2024-10-15-unsupervised-learning-how-my-projects-fit-together-substrate-fabric-telo.md` | Como todos os projetos se conectam (66 min) |

---

## Jornada de Aprendizado

Ver `ROADMAP.md` para o plano detalhado.

**Resumo das fases:**

```
Fase 1: TELOS      → Contexto profundo (Ale + Hotel)     ← AQUI
Fase 2: FABRIC     → Resolver problemas com patterns
Fase 3: PAI        → Automatizar com skills/hooks
Fase 4: Expansão   → Daemon, Self-update
```

---

## Aplicação: Duke Beach Hotel

A ideia é aplicar esses conceitos para criar um sistema que:
1. **Conhece o hotel profundamente** (TELOS do hotel)
2. **Resolve problemas específicos** (Skills de hotelaria)
3. **Aprende com cada interação** (Sistema de memória)
4. **Se atualiza automaticamente** (Hooks + self-update)

---

## Próximos Passos

1. ~~Ale responde entrevista~~ ✓
2. ~~Criar TELOS-ALE.md~~ ✓
3. **Criar TELOS do Duke Beach Hotel** usando mesmo processo
4. **Iniciar Fase 2** - Usar patterns do FABRIC para resolver problemas reais
5. **Criar gerador de Metcons** - Primeiro projeto prático (ver `projects/metas-pessoais/`)
