# Pesquisa de Stack Open Source para Hotelaria

> Pesquisa exploratória para identificar soluções open source e API-first no ecossistema de tecnologia hoteleira, visando construir uma plataforma de orquestração AI-native para operações de hospitalidade.
>
> **Data:** Janeiro 2026

---

## 1. PMS (Property Management System)

### Líder Identificado: QloApps

| Aspecto | Detalhes |
|---------|----------|
| GitHub | 11.4k stars, comunidade ativa |
| Licença | OSL-3.0 (open source) |
| Stack | PHP/MySQL (baseado em PrestaShop) |
| API REST | Completa, com endpoints para reservas, quartos, disponibilidade |

**Principais APIs:**

- `/api/hotel_ari` - Disponibilidade, tarifas e inventário (mais poderosa)
- `/api/bookings` - Ciclo completo de reservas
- `/api/customers`, `/api/room_types`, `/api/hotels`
- Schema discovery nativo (`?schema=blank`, `?schema=synopsis`)
- Filtros avançados (EQUAL, LIKE, GREATER THAN, etc.)

**Alternativas analisadas:**

- **miniCal** - Mais modular, menor comunidade
- **HotelDruid** - Simples, bom para pequenas propriedades

---

## 2. Referência Comercial: Apaleo

### Por que estudar Apaleo?

Apaleo representa o estado da arte em PMS API-first e lançou o **primeiro MCP Server nativo para hotelaria** (setembro 2025).

| Característica | Valor |
|----------------|-------|
| Endpoints | 237 APIs transformadas em MCP tools |
| Formato | JSON nativo |
| MCP Server | Nativo, permite agentes AI interagirem diretamente |
| Agent Hub | Marketplace de agentes AI para hotelaria |

**Insight estratégico:** Apaleo demonstra que o futuro é **agent-native** - sistemas onde AI agents colaboram (reservas + housekeeping + manutenção) e até negociam entre si (A2A - Agent to Agent).

**Citação relevante (citizenM CIO):**
> "Shifts from coding to describing intent, enabling GMs to front desk teams to design guest journeys without developer backlogs"

---

## 3. Channel Manager

### Descoberta Principal

**Não existe channel manager verdadeiramente open source funcional** devido a:

1. **Certificação obrigatória:** OTAs (Airbnb, Booking.com, Expedia) só concedem API a parceiros certificados
2. **Manutenção contínua:** APIs das OTAs mudam constantemente
3. **Modelo de negócio das OTAs:** Preferem poucos intermediários grandes vs. milhares de conexões diretas

### Opções Identificadas

| Solução | Modelo | Preço | Observação |
|---------|--------|-------|------------|
| **Channex.io** | API White-Label | $30-49/mês por propriedade | 50+ OTAs, API completa, MCP Server open source existe |
| **QloApps Channel Manager** | SaaS (do mesmo vendor do PMS) | $30/mês por propriedade | Integração nativa com QloApps PMS |

### Channex MCP Server (Open Source)

**Repositório:** `WebRenew/channex-mcp`

**Funcionalidades:**
- CRUD completo: Properties, Room Types, Rate Plans
- Gestão de ARI (Availability, Rates, Inventory)
- Conexão com canais: Airbnb, Booking.com, Expedia, Agoda, etc.
- Licença MIT

---

## 4. Comparativo: QloApps vs Apaleo

| Aspecto | QloApps | Apaleo |
|---------|---------|--------|
| Agent-Ready | ❌ Requer MCP wrapper | ✅ MCP Server nativo |
| Endpoints | ~20 recursos | 237 endpoints como tools |
| Formato | XML (JSON opcional) | JSON nativo |
| Webhooks | ❌ Não possui | ✅ Event-driven |
| Open Source | ✅ OSL-3.0 | ❌ Comercial |
| Custo | Gratuito | Pago (sandbox free) |
| Controle de Dados | ✅ Total | ⚠️ Nuvem do vendor |
| Multi-property | ✅ Suportado | ✅ Nativo |

---

## 5. Arquitetura Recomendada

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE AGENTES AI                     │
│         (MCP Servers / Orquestração / CrewAI/LangGraph)     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     MCP SERVER LAYER                        │
│  ┌─────────────────┐              ┌──────────────────────┐  │
│  │ QloApps MCP     │              │ Channex MCP          │  │
│  │ (a construir)   │              │ (já existe - MIT)    │  │
│  └────────┬────────┘              └──────────┬───────────┘  │
└───────────┼─────────────────────────────────┼───────────────┘
            │                                 │
            ▼                                 ▼
┌───────────────────────┐       ┌─────────────────────────────┐
│      QloApps PMS      │       │       Channex.io API        │
│    (self-hosted)      │       │        ($30-49/mês)         │
│    - Reservas         │       │    - Airbnb                 │
│    - Quartos          │       │    - Booking.com            │
│    - Tarifas          │       │    - Expedia                │
│    - Clientes         │       │    - 50+ OTAs               │
└───────────────────────┘       └─────────────────────────────┘
```

---

## 6. Próximos Passos Sugeridos

### Curto Prazo

- [ ] Instalar QloApps localmente como ambiente de desenvolvimento
- [ ] Criar conta Channex (staging gratuito para testes)
- [ ] Testar channex-mcp com Claude Code

### Médio Prazo

- [ ] Construir QloApps MCP Server - wrapper Python/TypeScript sobre a REST API
- [ ] Integrar ambos MCP servers em orquestração unificada

### Diferencial Competitivo

- **"Living Infrastructure"**: Documentação + PRDs + Skills + Agents como produto
- **Primitive-native**: Sistemas que expõem fundamentos operacionais (não escondem)
- **Agent-first**: Projetado para AI desde o início, não retrofitted

---

## 7. Insight Estratégico Final

> A indústria hoteleira **industrializou mas nunca digitalizou verdadeiramente** - sistemas atuais são versões digitais fragmentadas de processos analógicos.

Isso cria oportunidade para:

1. **Construir plataformas AI-native** enquanto incumbentes lutam com sistemas legados
2. **Usar channel managers como commodity** ($30/mês) enquanto foca em orquestração inteligente
3. **Capturar contexto operacional rico** para treinar e melhorar agentes AI continuamente

---

## Referências

- QloApps: https://github.com/webkul/hotelcommerce
- Apaleo MCP: https://apaleo.dev/
- Channex MCP: https://github.com/WebRenew/channex-mcp
