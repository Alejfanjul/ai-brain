# Plano de Estudo — Fundamentos Técnicos para Fundador

> **Contexto:** Ale é fundador não-técnico (administração) da HiHotel, construindo com IA.
> Matheus (sócio técnico) precisa que Ale tenha base para comunicar ideias de produto com precisão.
> O objetivo NÃO é virar engenheiro — é ser um fundador que fala a língua técnica o suficiente para especificar, decidir e colaborar.

> **Método:** Aprendizado orientado a artefato — cada módulo produz algo concreto e útil para a HiHotel.
> Sessões práticas com Claude, aplicando conceitos ao domínio real.

> **Criado em:** 2026-04-05

---

## Como usar este plano (em qualquer máquina)

Para iniciar um módulo em uma sessão nova do Claude, use este prompt:

```
Estou seguindo meu plano de estudo de fundamentos técnicos.
Leia o plano em projects/hihotel/plano-estudo-fundamentos.md
e os artefatos já completados em projects/hihotel/artefatos/.

Vamos fazer o módulo [X.X].

Regras da sessão:
- Ensina o conceito aplicando ao domínio real da HiHotel (Duke Beach Hotel)
- Cada módulo produz um artefato concreto que fica no repo
- Tom: direto e técnico, mas explicando como se eu fosse fundador não-técnico
- Usa os artefatos anteriores como base (cada módulo constrói sobre o anterior)
- No final, lista o vocabulário novo e atualiza o status no plano
```

> **Importante:** Os artefatos anteriores são a memória do progresso.
> O Claude vai ler os artefatos completados pra saber o que você já aprendeu
> e construir em cima. Não precisa reexplicar o histórico.

---

## Estrutura

Três blocos, em sequência. Cada módulo é uma sessão de ~1h.

```
BLOCO 1: Modelagem de Domínio     ← "O que existe no mundo do hotel?"
BLOCO 2: Arquitetura de Software  ← "Como os sistemas se organizam?"
BLOCO 3: Ecossistema Agêntico     ← "Como agentes e automação funcionam?"
```

Cada módulo segue o formato:
- **Conceito** — explicação direta (~10 min)
- **Aplicação** — modelar algo real da HiHotel (~30 min)
- **Artefato** — diagrama, documento ou modelo que fica no repo
- **Vocabulário** — termos novos para usar com Matheus

---

## BLOCO 1 — Modelagem de Domínio

> **Por que isso primeiro:** É a base de tudo que vocês discutiram sobre ontologia.
> Modelagem de domínio é literalmente o que você faz quando lista "hóspede, reserva, quarto, serviço"
> e define como se relacionam. Você já faz isso intuitivamente — aqui a gente formaliza.

### Módulo 1.1 — Entidades, Atributos e Relacionamentos

**O que você vai aprender:**
- O que é uma entidade (algo que tem identidade própria: Hóspede, Reserva, Quarto)
- O que é um atributo (características: nome, data_checkin, número)
- O que é um relacionamento (Hóspede FAZ Reserva, Reserva OCUPA Quarto)
- Cardinalidade (um hóspede pode ter MUITAS reservas, um quarto tem UMA reserva por vez)

**Aplicação prática:**
Modelar as entidades centrais do app de restaurante:
Mesa, Pedido, Item do Cardápio, Conta, Cliente, Garçom

**Artefato:**
`projects/hihotel/artefatos/1.1-entidades-restaurante.md` — Modelo de entidades do app de restaurante

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Entidade | Algo com identidade única | Hóspede, Reserva |
| Atributo | Propriedade de uma entidade | nome, data_checkin |
| Relacionamento | Conexão entre entidades | Hóspede FAZ Reserva |
| Cardinalidade | Quantos de cada lado | 1:N = um para muitos |

**Status:** [x] Completo — 2026-04-05

---

### Módulo 1.2 — Diagrama de Classes (UML)

**O que você vai aprender:**
- Como representar entidades visualmente em UML
- Notação de classes: nome, atributos, métodos
- Tipos de relacionamento visual: associação, composição, herança
- Como ler e desenhar um diagrama de classes

**Aplicação prática:**
Transformar o modelo de entidades do módulo 1.1 em um diagrama de classes UML.
Primeiro diagrama visual que você pode mostrar pro Matheus.

**Artefato:**
`projects/hihotel/artefatos/1.2-diagrama-classes-restaurante.md` — Diagrama UML do app de restaurante

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Classe | Representação de uma entidade em UML | caixa com nome/atributos/métodos |
| Associação | Linha conectando duas classes | Pedido → Mesa |
| Composição | "Faz parte de" (não existe sozinho) | ItemPedido ◆→ Pedido |
| Herança | "É um tipo de" | PedidoDelivery herda de Pedido |
| Multiplicidade | Cardinalidade no diagrama | 1..* = um ou mais |

**Status:** [x] Completo — 2026-04-05

---

### Módulo 1.3 — Domain-Driven Design (DDD): Linguagem e Contextos

**O que você vai aprender:**
- Ubiquitous Language: por que fundador e dev PRECISAM usar as mesmas palavras
- Bounded Context: onde termina um domínio e começa outro
- Entity vs Value Object: o que tem identidade vs o que é só um valor
- Aggregate: grupo de entidades que formam uma unidade

**Aplicação prática:**
- Criar o glossário da HiHotel (Ubiquitous Language)
- Mapear os Bounded Contexts: SID, Concierge, App Restaurante
- Conectar com os Verbos da HiHotel (aprender, ensinar, coordenar, etc.)

**Artefato:**
`projects/hihotel/artefatos/1.3-glossario-hihotel.md` — Glossário + mapa de contextos

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Ubiquitous Language | Vocabulário único compartilhado | "Reserva" = mesma coisa pra todos |
| Bounded Context | Fronteira de um domínio | SID ≠ Concierge (mesmo dado, uso diferente) |
| Entity | Objeto com identidade | Hóspede (tem ID único) |
| Value Object | Objeto sem identidade própria | Endereço (descreve, não identifica) |
| Aggregate | Cluster de objetos tratado como unidade | Pedido + Itens do Pedido |

**Status:** [x] Completo — 2026-04-05

---

### Módulo 1.4 — Ontologia na Prática

**O que você vai aprender:**
- Diferença entre modelo de dados, modelo de domínio e ontologia
- Como a Palantir usa ontologia (e o que adaptar pra HiHotel)
- Objetos, relações e ações — formalizar o rascunho de ontologia que vocês já começaram
- Como a ontologia se conecta com os Verbos da HiHotel

**Aplicação prática:**
Formalizar a ontologia hoteleira:
Pessoas ↔ Verbos ↔ Interfaces ↔ Ontologia ↔ Dados

**Artefato:**
`projects/hihotel/artefatos/1.4-ontologia-hoteleira-v1.md` — Ontologia formalizada (primeiro draft)

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Ontologia | Modelo formal de um domínio (conceitos + relações + regras) | "Hóspede OCUPA Quarto DURANTE Estadia" |
| Taxonomia | Classificação hierárquica | Bebida > Alcoólica > Cerveja |
| Modelo canônico | Representação interna padronizada | Reserva da HiHotel (independe do PMS) |
| Gêmeo digital | Representação digital do mundo real | Hotel no sistema = espelho do hotel físico |

**Status:** [ ] Não iniciado

---

## BLOCO 2 — Arquitetura de Software

> **Por que agora:** Com o domínio modelado, você precisa entender como as peças técnicas se organizam.
> Isso é o que permite entender por que o Matheus toma certas decisões e participar delas.

### Módulo 2.1 — Camadas e Responsabilidades

**O que você vai aprender:**
- Frontend (o que o usuário vê) vs Backend (lógica e dados) vs Banco de Dados
- Por que se separa em camadas (cada uma muda por razões diferentes)
- Onde cada coisa roda (browser, servidor, banco)
- Como o Sistema OS está organizado hoje (FastAPI + React + PostgreSQL)

**Aplicação prática:**
Desenhar a arquitetura em camadas do app de restaurante.
Comparar com a arquitetura do Sistema OS pra ver o padrão.

**Artefato:**
`projects/hihotel/artefatos/2.1-camadas-restaurante.md` — Diagrama de camadas

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Frontend | Interface visual (roda no browser/app) | Tela do garçom no tablet |
| Backend | Lógica de negócio (roda no servidor) | "Pedido foi pago? Pode fechar conta" |
| Banco de Dados | Armazenamento persistente | PostgreSQL com tabelas de pedidos |
| Request/Response | Pergunta e resposta entre front e back | Front pede lista de pedidos, back responde |

**Status:** [ ] Não iniciado

---

### Módulo 2.2 — APIs e Contratos

**O que você vai aprender:**
- O que é uma API (interface entre sistemas)
- REST: o padrão mais comum (GET, POST, PUT, DELETE)
- Contrato: o acordo sobre formato de dados entre sistemas
- Por que contratos são cruciais para interoperabilidade (o "conectar com qualquer sistema")

**Aplicação prática:**
- Especificar a API do app de restaurante (quais endpoints, quais dados)
- Entender como o Sistema OS se conectaria com um PMS novo via API

**Artefato:**
`projects/hihotel/artefatos/2.2-api-restaurante.md` — Especificação de API

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| API | Interface entre sistemas | PMS expõe API → SID consulta reservas |
| Endpoint | URL que aceita requisições | GET /api/pedidos → lista pedidos |
| Contrato | Formato acordado de dados | "Reserva sempre tem: id, hospede_id, data_checkin" |
| REST | Padrão de design de APIs web | Verbos HTTP (GET, POST, PUT, DELETE) |
| Payload | Dados enviados na requisição | JSON com dados do pedido |

**Status:** [ ] Não iniciado

---

### Módulo 2.3 — Padrões de Integração e Interoperabilidade

**O que você vai aprender:**
- Adapter Pattern: traduzir dados de um formato pra outro
- Anti-Corruption Layer: proteger seu sistema de sistemas externos sujos
- Eventos e Mensageria: pub/sub, webhooks
- Como construir o "conecta com qualquer PMS" na prática

**Aplicação prática:**
Desenhar como o Sistema OS se conectaria com o PMS novo E com o antigo ao mesmo tempo.
Isso é exatamente o cenário real da mudança de PMS no Duke.

**Artefato:**
`projects/hihotel/artefatos/2.3-integracao-pms.md` — Arquitetura de integração com PMS

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Adapter | Tradutor entre formatos | AdapterCMNET traduz dados do CMNET → modelo HiHotel |
| Anti-Corruption Layer | Camada protetora contra sistemas externos | SID nunca usa estrutura do PMS internamente |
| Webhook | Notificação automática de um sistema pra outro | PMS avisa SID: "novo check-in" |
| Pub/Sub | Padrão de eventos (publicar/assinar) | SID publica "pedido criado", Concierge escuta |
| SDK | Kit de ferramentas pra integrar com um sistema | "HiHotel SDK" = como outros sistemas se conectam |

**Status:** [ ] Não iniciado

---

### Módulo 2.4 — Diagramas de Sequência e Componentes (UML)

**O que você vai aprender:**
- Diagrama de Sequência: "quando X acontece, o que acontece passo a passo?"
- Diagrama de Componentes: "quais sistemas existem e como se conectam?"
- Diagrama de Casos de Uso: "o que o sistema faz, do ponto de vista do usuário?"
- Quando usar cada um (dica: sequência é o mais útil no dia a dia)

**Aplicação prática:**
- Diagrama de sequência: fluxo de pedido no restaurante (hóspede → garçom → cozinha → conta)
- Diagrama de componentes: SID ↔ Concierge ↔ App Restaurante ↔ PMS

**Artefato:**
`projects/hihotel/artefatos/2.4-diagramas-uml-hihotel.md` — Diagramas de sequência e componentes

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Diagrama de Sequência | Fluxo temporal entre atores/sistemas | Hóspede → App → Backend → Cozinha |
| Diagrama de Componentes | Visão de alto nível dos sistemas | SID ↔ PMS ↔ Concierge |
| Caso de Uso | O que o usuário consegue fazer | "Garçom registra pedido" |
| Ator | Quem interage com o sistema | Hóspede, Garçom, Cozinheiro |
| Lifeline | Linha de vida de um participante na sequência | Barra vertical = "está ativo" |

**Status:** [ ] Não iniciado

---

## BLOCO 3 — Ecossistema Agêntico

> **Por que por último:** Agentes são poderosos, mas sem entender domínio e arquitetura,
> você não sabe O QUE o agente deveria fazer nem COMO ele se encaixa no sistema.
> Com os blocos 1 e 2, você chega aqui sabendo modelar e especificar.

### Módulo 3.1 — O que é um Agente de IA

**O que você vai aprender:**
- Agente vs Chatbot vs Automação: as diferenças
- Componentes de um agente: modelo, contexto, tools, memória
- Context Engineering: como dar contexto suficiente pro agente funcionar
- Intent Engineering (framework do Nate): capturar intenção antes de automatizar

**Aplicação prática:**
Especificar o agente "Garçom Virtual" do app de restaurante.
Qual o contexto dele? Quais tools ele tem? O que ele sabe e não sabe?

**Artefato:**
`projects/hihotel/artefatos/3.1-agente-garcom-virtual.md` — Especificação do agente

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Agent | Sistema que decide e age autonomamente | Claude com tools fazendo reserva |
| Tool | Capacidade que o agente pode usar | consultar_cardapio(), registrar_pedido() |
| Context | Informação disponível pro agente | "Este é o hotel Duke, cardápio atual é..." |
| Memory | Informação que persiste entre interações | "Este hóspede prefere sem lactose" |
| Orchestrator | Agente que coordena outros agentes | SID como orquestrador central |

**Status:** [ ] Não iniciado

---

### Módulo 3.2 — Claude Code: Skills, Hooks e MCP

**O que você vai aprender:**
- Skills: comandos reutilizáveis (você já usa! /fim, /goals, /pdf)
- Hooks: automações que rodam em eventos (session start, tool call, etc.)
- MCP (Model Context Protocol): como conectar Claude a sistemas externos
- CLAUDE.md: como dar contexto persistente ao Claude

**Aplicação prática:**
- Entender a infraestrutura que você já tem no ai-brain
- Criar uma skill nova para a HiHotel (ex: /ontologia pra consultar o modelo de domínio)

**Artefato:**
`projects/hihotel/artefatos/3.2-ecossistema-claude-code.md` — Mapa do ecossistema

**Vocabulário:**
| Termo | Significado | Exemplo |
|-------|-------------|---------|
| Skill | Comando reutilizável com prompt estruturado | /fim salva resumo da sessão |
| Hook | Script que roda automaticamente em eventos | session-capture.ts no SessionEnd |
| MCP | Protocolo de conexão Claude ↔ sistemas | MCP server Supabase → Claude consulta banco |
| CLAUDE.md | Contexto persistente para o Claude | Regras do projeto, estrutura, convenções |

**Status:** [ ] Não iniciado

---

### Módulo 3.3 — Orquestração Multi-Agente

**O que você vai aprender:**
- Padrões de orquestração: central vs distribuído
- Como o SID funciona como orquestrador
- Claude Vault (projeto do Matheus): agente de recepção
- Como múltiplos agentes colaboram sem conflito

**Aplicação prática:**
Desenhar a arquitetura agêntica da HiHotel:
SID (orquestrador) → Claude Vault (recepção) → App Restaurante (garçom) → Concierge (hóspede)

**Artefato:**
`projects/hihotel/artefatos/3.3-arquitetura-agentica-hihotel.md` — Arquitetura multi-agente

**Status:** [ ] Não iniciado

---

### Módulo 3.4 — Cloud, Deploy e Infraestrutura

**O que você vai aprender:**
- O que é cloud (AWS, GCP, Supabase, Railway — onde as coisas rodam)
- Containers e Docker: como empacotar sistemas
- CI/CD: como código vai do repo pra produção
- Monitoramento: como saber se o sistema está funcionando

**Aplicação prática:**
Entender onde o Sistema OS roda hoje (Railway + Supabase + Upstash)
e como o app de restaurante seria deployado.

**Artefato:**
`projects/hihotel/artefatos/3.4-infraestrutura-hihotel.md` — Mapa de infraestrutura

**Status:** [ ] Não iniciado

---

## Como usar este plano

1. **Uma sessão = um módulo.** Comece uma conversa com Claude dizendo: "Vamos fazer o módulo X.X do plano de estudo."
2. **Cada módulo produz um artefato.** O artefato fica no repo e pode ser compartilhado com Matheus.
3. **Marque o status** conforme avança: `[ ]` → `[x]`
4. **Leve artefatos pro Matheus.** Especialmente os diagramas — pede feedback dele. Isso calibra o vocabulário compartilhado.
5. **Não pule módulos** sem motivo. A sequência existe porque cada módulo usa conceitos do anterior.

## Progresso

| Bloco | Módulo | Status |
|-------|--------|--------|
| 1 | 1.1 Entidades e Relacionamentos | [x] 2026-04-05 |
| 1 | 1.2 Diagrama de Classes (UML) | [x] 2026-04-05 |
| 1 | 1.3 DDD: Linguagem e Contextos | [x] 2026-04-05 |
| 1 | 1.4 Ontologia na Prática | [ ] |
| 2 | 2.1 Camadas e Responsabilidades | [ ] |
| 2 | 2.2 APIs e Contratos | [ ] |
| 2 | 2.3 Padrões de Integração | [ ] |
| 2 | 2.4 Diagramas UML (Sequência/Componentes) | [ ] |
| 3 | 3.1 Agentes de IA | [ ] |
| 3 | 3.2 Claude Code: Skills, Hooks, MCP | [ ] |
| 3 | 3.3 Orquestração Multi-Agente | [ ] |
| 3 | 3.4 Cloud, Deploy e Infraestrutura | [ ] |
