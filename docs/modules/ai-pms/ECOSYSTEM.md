# Cosmo - Ecossistema Hoteleiro

> Documento de referência permanente. Explica todas as peças, como se conectam, e onde estamos.
>
> **Atualizado:** 2026-01-31

---

## Modelo de Negócio

**Proposta:** "Contrata só eu, cuido de toda a tua infraestrutura de software."

Valor justo, baixo e variável. O hotel não precisa contratar 5 fornecedores diferentes.

**Dependências externas aceitas (apenas 2):**
- **Channex** ($30-49/mês) — Channel Manager. Não existe alternativa open source viável (certificação com 50+ OTAs é inviável de replicar).
- **Stripe** (~2.5% por transação) — Pagamentos. Segurança PCI, gateway global. Não faz sentido construir.

**Tudo mais é nosso.** PMS, Booking Engine, Revenue Management, Ordens de Serviço, Inteligência — código próprio, controle total.

---

## As 4 Peças do Ecossistema

Todo hotel digital precisa de 4 sistemas que se comunicam:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│     PMS      │    │   CHANNEL    │    │   BOOKING    │    │   REVENUE    │
│              │    │   MANAGER    │    │   ENGINE     │    │  MANAGEMENT  │
│ "O caderno"  │    │ "O distri-   │    │ "O site do   │    │ "O estrateg- │
│              │    │  buidor"     │    │  hotel"      │    │  ista de     │
│ Reservas,    │    │              │    │              │    │  preços"     │
│ quartos,     │    │ Sincroniza   │    │ Venda direta │    │              │
│ hóspedes,    │    │ com OTAs     │    │ pelo site    │    │ Define preço │
│ tarifas      │    │ (Booking,    │    │ do hotel     │    │ ótimo por    │
│              │    │  Expedia,    │    │              │    │ data/quarto  │
│              │    │  Airbnb)     │    │              │    │              │
├──────────────┤    ├──────────────┤    ├──────────────┤    ├──────────────┤
│ Nosso:       │    │ Channex      │    │ Nosso:       │    │ Nosso:       │
│ sistema-os   │    │ (SaaS)       │    │ custom       │    │ evolução RM  │
│              │    │              │    │ (Next.js +   │    │ do sistema-os│
│ (QloApps     │    │ Única dep.   │    │  Stripe)     │    │              │
│  temporário) │    │ externa      │    │              │    │ (Climber é   │
│              │    │              │    │              │    │  referência) │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │                   │
       └─────────┬─────────┘                   │                   │
                 │                             │                   │
                 ▼                             ▼                   ▼
          ┌────────────┐               ┌────────────┐      ┌────────────┐
          │ Middleware  │               │  Site do   │      │ Ajuste de  │
          │ (FastAPI)   │               │  hotel     │      │ preços nos │
          │             │               │  (frontend)│      │ canais     │
          │ Traduz PMS  │               │            │      │            │
          │ ↔ Channex   │               │ Consulta   │      │ Baseado em │
          │             │               │ PMS via API│      │ demanda +  │
          └──────┬──────┘               └────────────┘      │ concorrência│
                 │                                          └────────────┘
                 ▼
          Booking.com
          Expedia
          Airbnb
          50+ OTAs
```

### O que cada peça faz

| Peça | Função | Exemplos de mercado | Nós |
|------|--------|--------------------|----|
| **PMS** | Gerencia reservas, quartos, hóspedes, tarifas. O "banco de dados central" do hotel. | HITS, Opera, Cloudbeds, Mews, QloApps | sistema-os (QloApps temporário) |
| **Channel Manager** | Distribui disponibilidade/preços para OTAs. Recebe reservas de OTAs. Evita overbooking. | Channex, SiteMinder, RateGain | Channex ($30-49/mês) |
| **Booking Engine** | Site do hotel onde hóspedes reservam direto (sem comissão de OTA). | Omnibees, Motor de reservas SiteMinder | Custom (futuro) |
| **Revenue Management** | Define preços inteligentes baseado em demanda, concorrência, ocupação, eventos. | Climber, IDeaS, Duetto | Evolução do RM já existente |

### Como se comunicam

```
PMS ←──webhook/API──→ Middleware ←──API──→ Channel Manager ←──→ OTAs

Booking Engine ──API──→ PMS (verifica disponibilidade, cria reserva)

Revenue Mgmt ──API──→ PMS (lê ocupação) + Channel Manager (publica preços)
```

**Padrão:** Webhook (aviso automático quando algo acontece), não polling (ficar perguntando a cada 5 segundos).

---

## Glossário

| Termo | Significado |
|-------|-------------|
| **ARI** | Availability, Rates, Inventory. As 3 informações que os canais de venda precisam: quantos quartos disponíveis, qual o preço, qual o inventário. |
| **Webhook** | "Me avisa quando acontecer algo." Aviso automático via HTTP quando um evento ocorre (reserva criada, cancelada, etc). |
| **OTA** | Online Travel Agency. Booking.com, Expedia, Airbnb, etc. Cobram comissão (15-25%). |
| **Channel Manager** | Sistema que sincroniza ARI entre o PMS e todas as OTAs. Evita overbooking. |
| **Booking Engine** | Motor de reservas no site próprio do hotel. Venda direta = sem comissão de OTA. |
| **PMS** | Property Management System. O sistema central do hotel (reservas, quartos, hóspedes). |
| **RMS** | Revenue Management System. Otimiza preços baseado em dados (demanda, concorrência, ocupação). |
| **Middleware** | Programa que traduz entre dois sistemas que falam "línguas diferentes". No nosso caso: FastAPI (Python) entre PMS e Channex. |
| **ngrok** | Ferramenta que cria URL pública temporária apontando para um servidor local. Necessário pra Channex enviar webhooks pro nosso middleware. |
| **MCP** | Model Context Protocol. Padrão da Anthropic para agentes de IA interagirem com sistemas externos via "tools". |
| **REVPAR** | Revenue Per Available Room. Métrica principal de hotelaria (receita total / quartos disponíveis). |
| **ADR** | Average Daily Rate. Tarifa média diária. |

---

## Duke Beach: Hoje vs Cosmo

### O que o Duke Beach usa hoje

| Função | Ferramenta atual | Custo | Problemas |
|--------|-----------------|-------|-----------|
| PMS | HITS | ? | Sem API, dados extraídos por scraping |
| Channel Manager | Omnibees (?) | ? | Dependência, custo repassado |
| Booking Engine | Omnibees (?) | ? | Não é nosso, modelo de cobrança deles |
| Revenue Management | Climber | ? | Custo externo, artigo de luxo |
| Ordens de Serviço | **sistema-os** ✅ | Nosso | Funcionando em produção |
| Inteligência de Preços | **sistema-os** ✅ | Nosso | 6 concorrentes monitorados diariamente |
| Propostas de Eventos | **sistema-os** ✅ | Nosso | PDFs profissionais, versionamento |

### O que o Cosmo entrega

| Função | Ferramenta Cosmo | Custo | Diferencial |
|--------|-----------------|-------|-------------|
| PMS | sistema-os (evoluído) | Nosso | Guest-centric, IA nativa |
| Channel Manager | Channex | $30-49/mês | Única dependência externa |
| Booking Engine | Custom (Next.js + Stripe) | Nosso | Sem comissão de OTA |
| Revenue Management | Evolução do RM atual | Nosso | Já coleta dados de concorrentes |
| OS + Tudo mais | sistema-os | Nosso | Já existe e funciona |

---

## O que já existe no sistema-os

O sistema-os é a plataforma principal. 47 tabelas, 50+ endpoints API, FastAPI + PostgreSQL (Supabase).

### Já temos (base pra PMS)

| Funcionalidade | Tabelas | Status |
|---|---|---|
| Gestão de hóspedes (40 colunas, IA-ready) | `hospedes` | ✅ Produção |
| Reservas com N-N (multi-quarto, multi-hóspede) | `reservas`, `reserva_hospedes`, `reserva_apartamentos` | ✅ Produção |
| Inventário de quartos (7 categorias Duke Beach) | `apartamentos` | ✅ Produção |
| Ocupação em tempo real | `ocupacao_atual`, `movimentacao_eventos` | ✅ Produção |
| Financeiro básico | `contas` | ✅ Produção |
| Ordens de Serviço + tarefas | `ordens_servico`, `tarefas`, `tarefas_templates` | ✅ Produção |
| Monitoramento de preços (6 concorrentes) | `competitors`, `price_snapshots` | ✅ Produção |
| Propostas de eventos | `event_proposals` + 11 tabelas | ✅ Produção |
| Auth multi-departamento | `usuarios` | ✅ Produção |

### Falta construir (pra virar PMS completo)

| Funcionalidade | O que precisa | Complexidade |
|---|---|---|
| **Tarifas diárias** | Tabela de preço por quarto/data/temporada | Média |
| **Calendário de disponibilidade** | Bloqueios, min/max noites, restrições | Média |
| **Serviços extras padronizados** | Late checkout, cama extra, estacionamento | Baixa |
| **Políticas de cancelamento** | Regras e prazos | Baixa |
| **REVPAR/ADR tracking** | Métricas de revenue | Baixa |

A distância é menor do que parece. Fundação está pronta.

### Categorias de quarto do Duke Beach (já mapeadas)

```
LVU  — Lateral Vista Urbana
DLVU — De Luxe Vista Urbana
DLVL — De Luxe Vista Lateral
LVL  — Lateral Vista Lateral
OV   — Ocean View
GOVP — Grand Ocean View Premium
GOV  — Grand Ocean View
```

---

## Roadmap (4 Fases)

### Fase 1: Provar Conceito (agora)

```
QloApps (PMS tmp) ←→ Middleware (FastAPI) ←→ Channex → OTAs
```

- QloApps como PMS temporário
- Middleware traduz entre os dois
- Provar: reserva no PMS → atualiza OTAs. Reserva na OTA → aparece no PMS.
- **Resultado:** "Sei fazer channel management funcionar."

### Fase 2: Migrar PMS pro sistema-os (semanas)

```
sistema-os (PMS real) ←→ Middleware ←→ Channex → OTAs
```

- Adicionar tabelas: tarifas, disponibilidade, extras
- Adicionar endpoints: ARI, booking CRUD
- Middleware aponta pro sistema-os em vez do QloApps
- QloApps descartado
- **Resultado:** "PMS é nosso, 100% controle."

### Fase 3: Booking Engine próprio (meses)

```
Booking Engine (Next.js) → sistema-os (API) → Stripe (pgto)
```

- Site bonito com busca de quartos e datas
- Consulta disponibilidade e preços via API do sistema-os
- Pagamento via Stripe (checkout seguro)
- Cria reserva via API
- **Resultado:** "Hotel não precisa de Omnibees."

### Fase 4: Revenue Management ativo (futuro)

```
RM ativo → Sugere preços → Publica via Channex
```

- Evolução do RM que já coleta preços de concorrentes
- Adicionar: sugestão de preço ótimo baseado em demanda + concorrência + ocupação
- Publicar preços automaticamente nos canais
- **Resultado:** "Hotel não precisa de Climber."

---

## Onde cada coisa vive

| Repo | Conteúdo | Papel |
|------|----------|-------|
| `sistema-os` | OS, RM, Eventos, Hóspedes, Reservas, Quartos, Auth | Plataforma principal (produção) |
| `ai-brain/projects/ai-pms` | Middleware, documentação, visão Cosmo, laboratório | Laboratório de integração |
| `~/QloApps` | PMS temporário | Descartável após Fase 2 |

---

## Princípios Estratégicos

### 1. Foco em Tarefas, não em Sistemas

> "O hotel não precisa do PMS. Precisa das tarefas que o PMS realiza."
> — HOTEL-LAB.md

Sistemas são meios. O que importa são as tarefas executadas. Cada tarefa é um job que um agente de IA pode eventualmente executar.

### 2. Middleware persiste, PMS muda

O middleware (FastAPI que traduz entre PMS e Channex) é a peça que sobrevive a qualquer mudança de PMS. Hoje traduz QloApps ↔ Channex. Amanhã traduz sistema-os ↔ Channex. O Channex nem percebe.

### 3. Guest-centric, não booking-centric

> "Nem todos os funcionários lidam com reservas, mas todos lidam com hóspedes."
> — COSMO-VISION.md

O hóspede é a entidade central, não a reserva. O sistema-os já implementa isso (hospedes tem 40 colunas incluindo `contexto_ia`, `padroes_identificados`, `logs_preferencias`).

### 4. Eliminar desperdício sistêmico

> "Eliminar o desperdício sistêmico que impede cada pessoa de fazer seu melhor trabalho na hospitalidade."
> — ai-pms-filosofia.md

Cada feature responde: "Qual desperdício isso elimina e para quem?"

### 5. Framework dos 5 Stakeholders

Toda decisão de produto passa pelo filtro: atende a pelo menos 3 dos 5?

| # | Stakeholder | O que precisa |
|---|---|---|
| 1 | **Dono** | Paz de espírito, controle, métricas reais |
| 2 | **Gestor** | Coordenação fluida, sem apagar incêndios |
| 3 | **Funcionário** | Menos sistema, mais hóspede, trabalho digno |
| 4 | **Negócio** | ROI mensurável, redução de desperdício |
| 5 | **Hóspede** | Personalização genuína, coordenação invisível |

---

## Tarefas por Área do Hotel

Base para design de agentes. Cada tarefa é um potencial "agent job".

### Reservas & Distribuição
- Verificar disponibilidade por data/tipo
- Criar/modificar/cancelar reserva
- Sincronizar ARI com OTAs (via Channex)
- Receber reserva de OTA
- Processar pagamento (Stripe)
- Enviar confirmação

### Recepção / Front Office
- Check-in / Check-out
- Atribuição de quartos
- Comunicação pré-chegada
- Upselling no check-in
- Resolução de reclamações

### Governança / Housekeeping
- Status dos quartos (limpo/sujo/inspecionado)
- Atribuição de camareiras
- Controle de enxoval e amenities
- Manutenção preventiva

### Revenue Management
- Monitorar concorrência (✅ já funciona)
- Definir tarifas por data/quarto/temporada
- Previsão de demanda
- Gestão de overbooking
- Performance por canal

### Experiência do Hóspede
- Personalização da estadia
- Recomendações locais
- Coleta de feedback em tempo real
- Resolução proativa de problemas

---

## Diferenciadores de Longo Prazo

### Blue Ocean (Eliminar/Reduzir/Aumentar/Criar)

| Ação | O quê |
|------|-------|
| **Eliminar** | Complexidade de módulos que ninguém usa, relatórios que ninguém lê |
| **Reduzir** | Configurações infinitas, tempo em treinamento, dependências externas |
| **Aumentar** | Contexto por hóspede, autonomia do funcionário, velocidade de valor |
| **Criar** | IA nativa, interface conversacional, comunidade de prática, todos como usuários |

### Comunidade de Prática (Fase futura)

Conectar funcionários de hotéis diferentes para compartilhar conhecimento e boas práticas. O funcionário que muda de emprego leva o sistema — e se torna evangelista.

> Ver: `visao/ideia-sistema-social-hospitalidade.md`

### Documentador de Processos (Pattern pronto)

Bot Telegram que entrevista funcionários por áudio para documentar processos operacionais. Gera: SOP, Checklist, FAQ, Ficha Resumo.

> Ver: `lab/HOTEL-LAB.md` (seção "Documentador de Processos")

---

## Referências

| Documento | O que contém | Quando consultar |
|---|---|---|
| `COSMO-VISION.md` | Visão de produto, Blue Ocean, modelo de dados | Decisões estratégicas |
| `visao/ai-pms-filosofia.md` | 5 Stakeholders, propósito, diferenciação | Alinhar propósito |
| `visao/ideia-sistema-social-hospitalidade.md` | Comunidade de prática | Fase futura |
| `lab/HOTEL-LAB.md` | Tarefas por área, framework de observação | Design de agentes |
| `integracao/CHANNEX-INTEGRATION.md` | Detalhes técnicos da integração | Implementação Fase 1-2 |
| `middleware/` | Código do middleware FastAPI | Implementação |
| `/home/alejandro/sistema-os/` | Plataforma principal (produção) | Sempre |
