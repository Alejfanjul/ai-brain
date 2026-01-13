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

## Materiais Disponíveis

### Capturados no ai-brain

| Arquivo | Descrição |
|---------|-----------|
| `sources/2025-12-16-unsupervised-learning-a-deepdive-on-my-personal-ai-infrastructure-pai-v2.md` | Deep dive completo no PAI |
| `sources/2026-01-11-danielmiessler-personal-ai-maturity-model-paimm.md` | Modelo de maturidade (9 níveis) |
| `sources/2024-10-15-unsupervised-learning-how-my-projects-fit-together-substrate-fabric-telo.md` | Como todos os projetos se conectam |

### Repositórios Clonados

| Local | Descrição |
|-------|-----------|
| `/home/marketing/pai-reference/` | PAI - Personal AI Infrastructure |

### Repositórios para Explorar

| Repo | Descrição | Prioridade |
|------|-----------|------------|
| [Fabric](https://github.com/danielmiessler/fabric) | Prompts crowdsourced para problemas específicos | Alta |
| [Telos](https://github.com/danielmiessler/Telos) | Deep context sobre entidades (pessoas, empresas) | Alta |
| [Daemon](https://github.com/danielmiessler/Daemon) | API pessoal broadcast | Média |
| [Substrate](https://github.com/danielmiessler/Substrate) | Argumentos transparentes | Baixa |

## Jornada de Aprendizado

Ver `ROADMAP.md` para o plano detalhado.

## Aplicação: Duke Beach Hotel

A ideia é aplicar esses conceitos para criar um sistema que:
1. **Conhece o hotel profundamente** (TELOS do hotel)
2. **Resolve problemas específicos** (Skills de hotelaria)
3. **Aprende com cada interação** (Sistema de memória)
4. **Se atualiza automaticamente** (Hooks + self-update)

---

**Status:** Fase 1 - Fundamentos
