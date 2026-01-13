# PAI Study - Roadmap

> Jornada guiada para aprender o ecossistema Daniel Miessler

## Visão Geral

| Fase | Foco | Status |
|------|------|--------|
| 1 | Fundamentos - Filosofia e Conceitos | 🔄 Em progresso |
| 2 | Fabric - Prompts como Soluções | 📋 Pendente |
| 3 | TELOS - Contexto Profundo | 📋 Pendente |
| 4 | PAI - Arquitetura e Skills | 📋 Pendente |
| 5 | Aplicação - Duke Beach Hotel | 📋 Pendente |

---

## Fase 1: Fundamentos

**Objetivo:** Entender a filosofia por trás de tudo

### 1.1 Os 3 Problemas Mundiais (WP1-3)

Daniel trabalha para resolver:
1. **WP1:** Humanos sofrem com falta de propósito e significado
2. **WP2:** IA vai exacerbar isso (disrupção de trabalho)
3. **WP3:** Somos treinados para ser úteis economicamente, não humanos completos

### 1.2 Princípios Fundamentais

| # | Princípio | O que significa |
|---|-----------|-----------------|
| 1 | **Clear Thinking First** | Bons prompts vêm de pensamento claro |
| 2 | **Scaffolding > Model** | Estrutura importa mais que o modelo |
| 3 | **Code Before Prompts** | Se pode resolver com código, não use IA |
| 4 | **Spec / Test / Evals First** | Defina sucesso antes de construir |
| 5 | **UNIX Philosophy** | Uma coisa bem feita, componentes compostos |

### 1.3 O Algoritmo (THE CENTERPIECE)

```
Current State → Ideal State (via iteração verificável)

7 Fases:
1. OBSERVE - Coletar contexto
2. THINK - Gerar hipóteses
3. PLAN - Desenhar abordagem
4. BUILD - Definir critérios de sucesso
5. EXECUTE - Fazer o trabalho
6. VERIFY - Testar contra critérios
7. LEARN - Extrair insights, iterar
```

**Key insight:** A maioria pula o VERIFY. O poder vem de definir critérios ANTES e medir DEPOIS.

### Leitura Fase 1
- [ ] Ler: `sources/2024-10-15-unsupervised-learning-how-my-projects-fit-together-*.md`
- [ ] Ler: Seção "The PAI Principles" em `/home/marketing/pai-reference/README.md`

---

## Fase 2: Fabric

**Objetivo:** Entender prompts como soluções para problemas específicos

### 2.1 Conceito

- Cada "pattern" é uma solução para um problema humano específico
- Exemplos: `extract_wisdom`, `analyze_personality`, `create_aphorisms`
- Crowdsourced - comunidade contribui soluções

### 2.2 Estrutura de um Pattern

```
fabric/patterns/
└── extract_wisdom/
    └── system.md    ← O prompt completo
```

### 2.3 Aplicação Hotel

Patterns que poderíamos criar:
- `analyze_guest_feedback`
- `create_welcome_message`
- `summarize_daily_operations`

### Ações Fase 2
- [ ] Clonar: `github.com/danielmiessler/fabric`
- [ ] Explorar: 5 patterns relevantes
- [ ] Criar: 1 pattern para o hotel

---

## Fase 3: TELOS

**Objetivo:** Criar contexto profundo sobre o hotel

### 3.1 Conceito

TELOS = Estrutura para capturar TUDO sobre uma entidade
- Missão, Metas, KPIs
- Desafios, Estratégias
- Histórico, Decisões

### 3.2 Estrutura

```
telos/
├── mission.md
├── goals.md
├── kpis.md
├── challenges.md
├── strategies.md
├── risk_register.md
└── ...
```

### 3.3 Aplicação Hotel

Criar TELOS do Duke Beach Hotel:
- Missão do hotel
- Metas (ocupação, satisfação, receita)
- KPIs operacionais
- Desafios sazonais
- Estratégias de diferenciação

### Ações Fase 3
- [ ] Clonar: `github.com/danielmiessler/Telos`
- [ ] Estudar: Template corporativo
- [ ] Criar: TELOS do Duke Beach Hotel

---

## Fase 4: PAI - Arquitetura

**Objetivo:** Entender como montar o sistema completo

### 4.1 Componentes

| Componente | Função |
|------------|--------|
| Skills | Capacidades modulares |
| Hooks | Eventos automáticos |
| Memory | Sistema de memória (hot/warm/cold) |
| Tools | Código determinístico |

### 4.2 Estrutura de um Skill

```
skills/
└── Art/
    ├── SKILL.md      ← Routing e descrição
    ├── workflows/    ← Procedimentos específicos
    └── tools/        ← Código (.ts)
```

### 4.3 Sistema de Hooks

```
~/.claude/hooks/
├── PreToolUse     → Antes de usar ferramenta
├── PostToolUse    → Depois de usar ferramenta
├── SessionEnd     → Fim de sessão (captura)
└── ...
```

### Ações Fase 4
- [ ] Explorar: `/home/marketing/pai-reference/Packs/pai-core-install/`
- [ ] Entender: Sistema de memória
- [ ] Mapear: Skills que precisamos para hotel

---

## Fase 5: Aplicação - Duke Beach Hotel

**Objetivo:** Construir o sistema para o hotel

### 5.1 Skills do Hotel

| Skill | Função |
|-------|--------|
| `GuestService` | Atendimento ao hóspede |
| `Operations` | Operações diárias |
| `Revenue` | Gestão de receita |
| `Maintenance` | Manutenção preventiva |

### 5.2 TELOS do Hotel

- Missão, visão, valores
- Metas de ocupação, ADR, RevPAR
- Processos operacionais
- Perfil de hóspedes

### 5.3 Integração

- Hooks para capturar interações
- Memória de decisões e aprendizados
- Self-update baseado em fontes do setor

### Ações Fase 5
- [ ] Criar estrutura base
- [ ] Implementar primeiro skill
- [ ] Testar ciclo completo

---

## Decisões de Design

### Princípio #1: Começar simples
> "Não construa o que não precisa ainda"

### Princípio #2: Aprender fazendo
> "Cada fase deve ter uma entrega prática"

### Princípio #3: Texto é rei
> "Tudo em markdown, versionado, legível"
