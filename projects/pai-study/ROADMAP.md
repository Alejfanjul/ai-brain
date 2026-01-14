# PAI Study - Roadmap

> Jornada para construir infraestrutura de IA pessoal

## Filosofia Central

> "Start with the human side of things. Then think about the tasks. Then break that into skills, workflows, and tools." - Daniel Miessler

**A progressão natural:**
1. **TELOS** → Entender quem você é e o que quer
2. **FABRIC** → Resolver problemas específicos (validar o que funciona)
3. **PAI** → Automatizar o que já funciona

**Princípio chave:** Só automatize o que já validou manualmente.

---

## Visão Geral

| Fase | Foco | Entrega Concreta | Status |
|------|------|------------------|--------|
| 1 | TELOS - Contexto | TELOS pessoal + hotel | 🔄 Em andamento |
| 2 | FABRIC - Problemas | 3-5 patterns úteis | 📋 Pendente |
| 3 | PAI - Automação | Skills estruturados | 📋 Pendente |
| 4 | Expansão | Daemon, Self-update | 📋 Futuro |

---

## Repositórios Disponíveis

| Repo | Local | O que contém |
|------|-------|--------------|
| PAI | `/home/marketing/pai-reference/` | Sistema completo (skills, hooks, memory) |
| TELOS | `/home/marketing/telos-reference/` | Templates de contexto |
| Fabric | `/home/marketing/fabric-reference/` | 234 patterns de prompts |
| Daemon | `/home/marketing/daemon-reference/` | API pessoal broadcast |
| Substrate | `/home/marketing/substrate-reference/` | Argumentos estruturados |

---

## Fase 1: TELOS - Contexto Profundo

**Objetivo:** Criar contexto que a IA possa usar para te ajudar melhor.

### Por que primeiro?

> "Once the AI sees everything—purpose, goals, challenges, strategies, KPIs—now we can start asking questions." - Daniel

Sem TELOS, a IA não sabe:
- Quem você é
- O que você quer alcançar
- Quais são seus desafios
- Como medir sucesso

### Estrutura do TELOS

```
TELOS/
├── PROBLEMS        ← Problemas que quer resolver
├── MISSION         ← Por que você faz o que faz
├── GOALS           ← Metas com prazo
├── CHALLENGES      ← Obstáculos atuais
├── STRATEGIES      ← Como vai superar
├── METRICS/KPIs    ← Como mede sucesso
├── IDEAS           ← Ideias originais
├── WISDOM          ← Sabedoria acumulada
└── LOG             ← Diário de progresso
```

### Progresso Fase 1

**Concluído:**
- [x] Repositórios clonados (PAI, TELOS, Fabric, Daemon, Substrate)
- [x] Guias de patterns criados (`FABRIC-ALL-PATTERNS.md`, `FABRIC-TELOS-PATTERNS.md`)
- [x] Perfil V5 limpo e estruturado (`ALE-PERFIL-LIMPO.md`)
- [x] Plano de entrevista criado (`TELOS-INTERVIEW-PLAN.md`)
- [x] Templates TELOS lidos e analisados

**Em andamento:**
- [x] **Conversa 01** (2026-01-13) - Problemas, Missão, Desafios → `TELOS-CONVERSA-01.md`
- [x] **Conversa 02** (2026-01-14) - Camada profunda: traumas, autocobrança, sabedoria, identidade, como quer ser tratado → `TELOS-CONVERSA-02.md`
- [ ] **Próximas conversas** - Metas concretas, Métricas de capacidade, Estratégias (após explorar mundo técnico)
- [ ] Criar `TELOS-ALE.md` consolidando todas as conversas

**Pendente:**
- [ ] Explorar mundo técnico dos agentes (pré-requisito para definir metas/métricas)
- [ ] Criar `TELOS-HOTEL.md` (Duke Beach)
- [ ] Criar pattern `create_telos_interview` para reutilização

### Entregas Fase 1

- [ ] **TELOS Pessoal (Ale)** → `TELOS-ALE.md`
  - Problemas que quer resolver
  - Missão pessoal
  - Metas para 2026
  - Desafios atuais

- [ ] **TELOS Hotel (Duke Beach)** → `TELOS-HOTEL.md`
  - Missão do hotel
  - Metas (ocupação, ADR, satisfação)
  - KPIs operacionais
  - Desafios sazonais
  - Perfil de hóspedes

### Leitura Fase 1
- [x] `/home/marketing/telos-reference/personal_telos.md`
- [x] `/home/marketing/telos-reference/corporate_telos.md`

### Patterns do Fabric para Criar TELOS

Usar esses patterns como apoio na construção:

| Pattern | Uso para TELOS |
|---------|----------------|
| `extract_primary_problem` | Definir PROBLEMS |
| `create_better_frame` | Reformular crenças limitantes |
| `analyze_personality` | Entender perfil para ABOUT ME |
| `extract_wisdom` | Processar conteúdos para WISDOM |
| `create_hormozi_offer` | Definir proposta de valor (empresa) |

### Patterns do Fabric para Revisar TELOS

Após ter o TELOS criado, usar para manutenção:

```
Semanal:
├── t_check_metrics         → KPIs estão melhorando?
├── t_find_neglected_goals  → Algo foi esquecido?
└── t_give_encouragement    → Manter motivação

Mensal:
├── t_analyze_challenge_handling → Estou trabalhando nos desafios?
├── t_find_blindspots            → Pontos cegos?
└── t_find_negative_thinking     → Pensamentos limitantes?

Trimestral:
├── t_red_team_thinking               → Atacar meu próprio plano
├── t_threat_model_plans              → O que pode dar errado?
└── t_visualize_mission_goals_projects → Está tudo alinhado?

Anual:
├── t_year_in_review      → O que realizei?
├── t_create_h3_career    → Estou preparado para o futuro?
└── t_describe_life_outlook → Minha perspectiva mudou?
```

> Ver guia completo: `projects/pai-study/FABRIC-TELOS-PATTERNS.md`

---

## Fase 2: FABRIC - Resolver Problemas

**Objetivo:** Usar prompts estruturados para resolver problemas específicos do dia a dia.

### Por que segundo?

Antes de automatizar, você precisa:
1. Identificar problemas recorrentes
2. Testar soluções manualmente
3. Validar o que funciona
4. Só então pensar em automação

### O que é um Pattern?

```
fabric/data/patterns/
└── analyze_personality/
    └── system.md    ← Prompt completo e testado
```

Cada pattern resolve **um problema específico**.

### Patterns Relevantes para Explorar

| Pattern | Uso potencial |
|---------|---------------|
| `extract_wisdom` | Extrair insights de conteúdos |
| `summarize` | Resumir documentos |
| `analyze_personality` | Entender perfis de hóspedes |
| `create_aphorisms` | Criar frases de impacto |
| `improve_writing` | Melhorar comunicação |

### Patterns para Criar (Hotel)

| Pattern | Problema que resolve |
|---------|---------------------|
| `analyze_guest_feedback` | Extrair insights de reviews |
| `summarize_daily_operations` | Resumo diário para gestão |
| `create_welcome_message` | Mensagens personalizadas |
| `analyze_occupancy_trends` | Padrões de ocupação |

### Entregas Fase 2

- [ ] Explorar 5 patterns existentes do Fabric
- [ ] Testar patterns manualmente no dia a dia
- [ ] Criar 1 pattern customizado para o hotel
- [ ] Documentar o que funciona vs. não funciona

### Leitura Fase 2
- [ ] `/home/marketing/fabric-reference/README.md`
- [ ] Explorar `/home/marketing/fabric-reference/data/patterns/`

---

## Fase 3: PAI - Automatizar

**Objetivo:** Transformar o que funciona em automação estruturada.

### Por que terceiro?

> "Code Before Prompts" - Só automatize o que já validou.

Neste ponto você já tem:
- ✅ TELOS definido (contexto)
- ✅ Patterns testados (soluções)
- ✅ Entendimento do que funciona

Agora é hora de estruturar.

### Componentes do PAI

| Componente | O que faz |
|------------|-----------|
| **Skills** | Capacidades modulares com routing |
| **Workflows** | Procedimentos dentro de cada skill |
| **Tools** | Código determinístico (TypeScript) |
| **Hooks** | Eventos automáticos |
| **Memory** | Sistema de memória (hot/warm/cold) |

### Estrutura de um Skill

```
skills/HotelOperations/
├── SKILL.md              ← Descrição + routing (USE WHEN...)
├── Workflows/
│   ├── DailyChecklist.md
│   ├── GuestCheckIn.md
│   └── OccupancyReport.md
└── Tools/
    └── generate-report.ts
```

### Skills para o Hotel

| Skill | Função |
|-------|--------|
| `HotelOperations` | Operações diárias |
| `GuestService` | Atendimento ao hóspede |
| `Revenue` | Gestão de receita |
| `Maintenance` | Manutenção preventiva |

### Entregas Fase 3

- [ ] Estudar estrutura de skills do PAI
- [ ] Criar primeiro skill (HotelOperations)
- [ ] Implementar 1 workflow funcional
- [ ] Criar 1 tool em TypeScript

### Leitura Fase 3
- [ ] `/home/marketing/pai-reference/Packs/pai-core-install/src/skills/`
- [ ] `/home/marketing/pai-reference/Packs/pai-core-install/src/skills/CORE/SYSTEM/SKILLSYSTEM.md`

---

## Fase 4: Expansão (Futuro)

**Quando:** Após ter Fases 1-3 funcionando.

### 4.1 Self-Update

Sistema que monitora fontes e se atualiza:
- Novos patterns do Fabric
- Atualizações do setor hoteleiro
- Melhores práticas

### 4.2 Daemon (API do Hotel)

Broadcast do hotel para integrações:
- Disponibilidade em tempo real
- Integração com OTAs
- Dados para parceiros

### 4.3 Substrate

Para decisões complexas:
- Análise de investimentos
- Debates internos estruturados

---

## Princípios de Design

### 1. Começar simples
> "Não construa o que não precisa ainda"

### 2. Validar antes de automatizar
> "Só automatize o que já funciona manualmente"

### 3. Texto é rei
> "Tudo em markdown, versionado, legível"

### 4. Iterar
> "Fase 1 imperfeita > Fase 3 nunca começada"

---

## O Algoritmo (Referência)

Para qualquer tarefa, a progressão:

```
Current State → Ideal State

1. OBSERVE  - Coletar contexto
2. THINK    - Gerar hipóteses
3. PLAN     - Desenhar abordagem
4. BUILD    - Definir critérios de sucesso
5. EXECUTE  - Fazer o trabalho
6. VERIFY   - Testar contra critérios
7. LEARN    - Extrair insights, iterar
```

**Key insight:** A maioria pula VERIFY. O poder vem de definir critérios ANTES e medir DEPOIS.

---

## Próximo Passo

**Fase 1 (continuação):**
1. Explorar mundo técnico dos agentes (possibilidades de negócio)
2. Definir metas concretas e métricas de capacidade
3. Consolidar conversas em `TELOS-ALE.md`
4. Criar `TELOS-HOTEL.md` (Duke Beach)
