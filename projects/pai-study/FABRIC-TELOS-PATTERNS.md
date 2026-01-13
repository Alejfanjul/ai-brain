# Fabric TELOS Patterns - Guia Completo

> Análise de todos os 16 patterns do Fabric que trabalham com TELOS

## O que são os patterns `t_*`?

Todos os patterns que começam com `t_` são projetados para trabalhar **com um TELOS já existente**. Eles:

1. Leem o arquivo TELOS completo
2. Entendem profundamente o contexto da pessoa/entidade
3. Aplicam uma análise específica
4. Geram insights acionáveis

**Pré-requisito:** Você precisa ter um TELOS criado para usar esses patterns.

**Uso típico:**
```bash
cat TELOS.md | fabric -p t_find_blindspots
```

---

## Categorias dos Patterns

| Categoria | Patterns | Uso |
|-----------|----------|-----|
| **Auto-conhecimento** | 4 patterns | Entender quem você é |
| **Análise de Progresso** | 3 patterns | Verificar andamento |
| **Identificar Problemas** | 4 patterns | Encontrar falhas |
| **Planejamento** | 3 patterns | Pensar o futuro |
| **Comunicação** | 2 patterns | Apresentar-se |

---

## Auto-conhecimento

### `t_describe_life_outlook`

**O que faz:** Descreve sua perspectiva de vida em 5 bullets de 16 palavras.

**Quando usar:** Para entender como você vê o mundo.

**Output:** 5 frases descrevendo seu outlook de vida.

**Útil para TELOS:** Preencher seção de PHILOSOPHY ou VALUES.

---

### `t_check_dunning_kruger`

**O que faz:** Avalia onde você superestima ou subestima suas competências.

**Quando usar:** Para calibrar auto-percepção vs. realidade.

**Output:**
- OVERESTIMATION OF COMPETENCE (10 bullets)
- UNDERESTIMATION OF COMPETENCE (10 bullets)
- METACOGNITIVE SKILLS (gaps de percepção)
- IMPACT ON DECISION MAKING (como afeta decisões)
- Resumo com 5 gaps principais e como resolver

**Útil para TELOS:** Preencher CHALLENGES com vieses reais, não percebidos.

---

### `t_analyze_challenge_handling`

**O que faz:** Avalia se você está realmente enfrentando seus desafios declarados.

**Quando usar:** Para verificar se CHALLENGES do TELOS estão sendo trabalhados.

**Output:** 8 bullets de 16 palavras avaliando seu progresso (com tough love).

**Útil para TELOS:** Validar se CHALLENGES são reais ou só declarados.

---

### `t_create_h3_career`

**O que faz:** Analisa o que você pode contribuir quando skills técnicos forem automatizados.

**Quando usar:** Para pensar carreira pós-automação (Human 3.0).

**Output:** Lista de contribuições baseadas em interação humana.

**Útil para TELOS:** Preencher MISSION com propósito duradouro.

---

## Análise de Progresso

### `t_check_metrics`

**O que faz:** Verifica estado atual dos KPIs/Métricas e se melhoraram recentemente.

**Quando usar:** Review periódico (semanal/mensal).

**Output:** Lista do estado de cada métrica.

**Útil para TELOS:** Atualizar seção METRICS com progresso real.

---

### `t_find_neglected_goals`

**O que faz:** Identifica metas e projetos que não foram trabalhados recentemente.

**Quando usar:** Review semanal para refocar prioridades.

**Output:** 5 bullets de 16 palavras sobre metas negligenciadas.

**Útil para TELOS:** Decidir o que remover ou reativar em GOALS/PROJECTS.

---

### `t_year_in_review`

**O que faz:** Resume o que você realizou no ano.

**Quando usar:** Review anual (dezembro/janeiro).

**Output:**
- 8 bullets sobre realizações
- ASCII art: trabalhado vs. não trabalhado

**Útil para TELOS:** Atualizar HISTORY e calibrar GOALS para próximo ano.

---

## Identificar Problemas

### `t_find_blindspots`

**O que faz:** Encontra falhas em seus modelos mentais e frames que podem causar erros.

**Quando usar:** Antes de decisões importantes ou periodicamente.

**Output:** 8 bullets de 16 palavras sobre pontos cegos.

**Útil para TELOS:** Adicionar em CHALLENGES ou criar seção BLINDSPOTS.

---

### `t_find_negative_thinking`

**O que faz:** Identifica pensamentos negativos no TELOS ou journal.

**Quando usar:** Quando se sentir travado ou desmotivado.

**Output:**
- 4 bullets identificando pensamento negativo
- Tough love para sair do mindset

**Útil para TELOS:** Limpar CHALLENGES de vitimismo, focar no acionável.

---

### `t_red_team_thinking`

**O que faz:** Ataca seu próprio pensamento, modelos e frames.

**Quando usar:** Antes de decisões estratégicas.

**Output:**
- 4 bullets red-teaming seu pensamento
- Recomendações para corrigir

**Útil para TELOS:** Validar STRATEGIES antes de executar.

---

### `t_threat_model_plans`

**O que faz:** Modela ameaças ao seu plano de vida.

**Quando usar:** Planejamento anual ou mudanças grandes.

**Output:**
- 8 bullets sobre o que pode dar errado
- Recomendações para mitigar

**Útil para TELOS:** Criar seção RISKS ou enriquecer CHALLENGES.

---

## Planejamento

### `t_visualize_mission_goals_projects`

**O que faz:** Cria diagrama ASCII mostrando relação entre missão, metas e projetos.

**Quando usar:** Para visualizar alinhamento estratégico.

**Output:** ASCII art do relacionamento Mission → Goals → Projects.

**Útil para TELOS:** Verificar se projetos estão alinhados com missão.

---

### `t_give_encouragement`

**O que faz:** Dá encorajamento baseado no progresso real.

**Quando usar:** Quando precisar de motivação genuína (não fluff).

**Output:** 8 bullets reconhecendo progresso e recomendando continuar.

**Útil para TELOS:** Não é para criar, mas para manter momentum.

---

## Comunicação

### `t_create_opening_sentences`

**O que faz:** Cria 4 frases de apresentação não-arrogantes.

**Template:** "Sou [quem], vejo [problema no mundo], então [o que faço sobre isso]."

**Quando usar:** Bio, apresentações, networking.

**Output:** 4 bullets de 32 palavras cada.

**Útil para TELOS:** Criar seção NARRATIVE ou ELEVATOR PITCH.

---

### `t_extract_intro_sentences`

**O que faz:** Extrai quem você é, o que faz, no que está trabalhando.

**Quando usar:** Criar bio ou apresentação.

**Output:** 5 bullets de 16 palavras, confiante mas humilde.

**Útil para TELOS:** Criar seção ABOUT ME resumida.

---

### `t_extract_panel_topics`

**O que faz:** Sugere painéis/talks que você poderia participar.

**Quando usar:** Planejamento de marca pessoal.

**Output:** 5 bullets com título (3-5 palavras) + descrição (48 palavras).

**Útil para TELOS:** Identificar áreas de expertise para STRENGTHS.

---

## Fluxo Recomendado

### Para CRIAR um TELOS (usar Fabric como apoio)

```
1. extract_primary_problem  → Clarificar problema central
2. create_better_frame      → Reformular crenças limitantes
3. create_idea_compass      → Estruturar ideias principais
4. analyze_personality      → Entender seu perfil
5. extract_wisdom           → Processar conteúdos que te influenciam
```

### Para REVISAR um TELOS (usar patterns t_*)

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

---

## Patterns Auxiliares (não t_*, mas úteis para TELOS)

| Pattern | Uso para TELOS |
|---------|----------------|
| `extract_primary_problem` | Definir PROBLEMS |
| `create_better_frame` | Reformular CHALLENGES |
| `create_idea_compass` | Explorar IDEAS |
| `analyze_personality` | Entender perfil para ABOUT ME |
| `extract_wisdom` | Processar conteúdos para WISDOM |
| `create_hormozi_offer` | Definir proposta de valor (empresa) |
| `analyze_product_feedback` | Processar feedback (empresa) |
| `analyze_risk` | Criar RISK REGISTER (empresa) |

---

## Referência Rápida

| Pattern | Input | Output | Frequência |
|---------|-------|--------|------------|
| `t_analyze_challenge_handling` | TELOS | 8 bullets avaliando progresso | Mensal |
| `t_check_dunning_kruger` | TELOS | Análise de vieses cognitivos | Trimestral |
| `t_check_metrics` | TELOS | Estado dos KPIs | Semanal |
| `t_create_h3_career` | TELOS | Carreira pós-automação | Anual |
| `t_create_opening_sentences` | TELOS | 4 frases de apresentação | Quando precisar |
| `t_describe_life_outlook` | TELOS | 5 bullets de perspectiva | Anual |
| `t_extract_intro_sentences` | TELOS | 5 bullets de intro | Quando precisar |
| `t_extract_panel_topics` | TELOS | 5 sugestões de painéis | Quando precisar |
| `t_find_blindspots` | TELOS | 8 pontos cegos | Mensal |
| `t_find_negative_thinking` | TELOS | 4 pensamentos negativos | Quando travado |
| `t_find_neglected_goals` | TELOS | 5 metas negligenciadas | Semanal |
| `t_give_encouragement` | TELOS | 8 bullets de encorajamento | Quando precisar |
| `t_red_team_thinking` | TELOS | 4 ataques + recomendações | Trimestral |
| `t_threat_model_plans` | TELOS | 8 ameaças + mitigações | Trimestral |
| `t_visualize_mission_goals_projects` | TELOS | ASCII art de alinhamento | Trimestral |
| `t_year_in_review` | TELOS | Realizações + ASCII | Anual |

---

## Localização

```
/home/marketing/fabric-reference/data/patterns/
├── t_analyze_challenge_handling/system.md
├── t_check_dunning_kruger/system.md
├── t_check_metrics/system.md
├── t_create_h3_career/system.md
├── t_create_opening_sentences/system.md
├── t_describe_life_outlook/system.md
├── t_extract_intro_sentences/system.md
├── t_extract_panel_topics/system.md
├── t_find_blindspots/system.md
├── t_find_negative_thinking/system.md
├── t_find_neglected_goals/system.md
├── t_give_encouragement/system.md
├── t_red_team_thinking/system.md
├── t_threat_model_plans/system.md
├── t_visualize_mission_goals_projects/system.md
└── t_year_in_review/system.md
```
