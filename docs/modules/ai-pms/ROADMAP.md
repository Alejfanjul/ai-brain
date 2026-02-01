# AI-PMS (Cosmo) - Roadmap

> Ultima atualizacao: 2026-02-01 (Marco 2 em progresso: middleware migrado para sistema-os)

## Visao geral dos Marcos

| Marco | Descricao | Status |
|-------|-----------|--------|
| 1 | Proof of Concept: QloApps <-> Channex | ✅ Completo |
| 2 | Migrar PMS para sistema-os | 🔄 Em progresso |
| 3 | Booking Engine proprio | 📋 Futuro |
| 4 | Revenue Management ativo | 📋 Futuro |

---

## Marco 1: Proof of Concept <-> Channex ✅

**Objetivo:** Provar que o middleware consegue sincronizar PMS <-> Channel Manager bidirecionalmente.

**Stack temporaria:** QloApps (PMS) <-> Middleware (FastAPI) <-> Channex (CM)

**Conclusao:** 2026-02-01

### Fase 1.1: Infraestrutura ✅

- QloApps instalado e API funcionando
- Channex staging configurado (property + room types + rate plans)
- Middleware FastAPI criado
- Modulo PHP webhook instalado no QloApps
- Room type mappings completos (5 tipos)

### Fase 1.2: QloApps -> Channex (ARI completo) ✅

**Concluido 2026-01-31**

- Webhook QloApps -> Middleware funcionando
- Middleware consulta ARI real no QloApps
- Push de disponibilidade + tarifas + restricoes para Channex
- Retry com backoff para lidar com DB locks do PHP
- Sync manual via Swagger

### Fase 1.3: Channex -> QloApps (OTA Bookings) ✅

**Concluido 2026-02-01**

- ngrok configurado para URL publica
- Webhook Channex criado via API
- Booking CRS App instalado no Channex
- booking_store.py: mapeamento Channex <-> QloApps
- Handlers: booking_new, booking_modification, booking_cancellation
- Idempotencia, ack, ARI re-sync

**Resultado:** Ciclo completo new -> modified -> cancelled testado end-to-end.

### Fase 1.4: Eliminada

Validacao com dados reais do Duke foi incorporada ao Marco 2 (direto no sistema-os, sem passar pelo QloApps).

### Criterio de conclusao ✅

- [x] QloApps booking -> Channex ARI atualizado (Fase 1.2)
- [x] Channex booking -> QloApps booking criado (Fase 1.3)
- [x] Booking modification e cancellation funcionando (Fase 1.3)
- [x] Fluxo bidirecional testado end-to-end (Fase 1.3)

---

## Marco 2: Migrar PMS para sistema-os 🔄

**Objetivo:** Substituir QloApps pelo sistema-os (plataforma propria). Middleware aponta para sistema-os em vez de QloApps.

**Decisao:** Fase 1.4 eliminada. Migrar direto para sistema-os com categorias Duke reais.

### O que foi feito

- [x] **Enum CategoriaApartamento atualizado** — GOVP/GOV removidos, OVP adicionado (6 categorias)
- [x] **Middleware movido** para `sistema-os/middleware/` (era `ai-brain/projects/ai-pms/middleware/`)
- [x] **Tabela `tarifas` criada** — preco fixo por categoria (6 categorias, seed com valores placeholder)
- [x] **Endpoints Channex no sistema-os** — ARI query + booking CRUD com auto-assign de quarto
- [x] **`sistemeos_client.py`** — HTTP client async chamando sistema-os API
- [x] **Middleware reescrito** — main.py agora usa sistema-os em vez de QloApps
- [x] **booking_store migrado** — `qloapps_order_id` -> `pms_reserva_id` (com backward compat)
- [x] **Script setup Channex** — cria room types Duke no Channex staging

### O que falta

- [ ] **Rodar setup Channex** — executar `scripts/setup_channex_duke.py` e atualizar UUIDs no config.py
- [ ] **Testar end-to-end** — criar booking via Channex CRS -> verificar reserva no sistema-os
- [ ] **Rodar migrations** — `alembic upgrade head` (enum OVP + tabela tarifas)

### Endpoints sistema-os criados

| Endpoint | Descricao |
|----------|-----------|
| `GET /api/v1/channex/ari` | ARI (disponibilidade + tarifa por categoria para range de datas) |
| `POST /api/v1/channex/booking` | Criar booking OTA (find-or-create hospede + auto-assign quarto) |
| `PATCH /api/v1/channex/booking/{id}` | Atualizar booking (nome, telefone, ocupacao) |
| `POST /api/v1/channex/booking/{id}/cancel` | Cancelar booking |
| `GET /api/v1/tarifas/` | Listar tarifas |
| `GET /api/v1/tarifas/{categoria}` | Tarifa por categoria |

### Categorias Duke Beach (6)

| Categoria | Nome | Unidades |
|-----------|------|----------|
| lvu | Lateral Vista Urbana | 11 |
| dlvu | De Luxe Vista Urbana | 2 |
| dlvl | De Luxe Vista Lateral | 2 |
| lvl | Lateral Vista Lateral | 11 |
| ov | Ocean View | 5 |
| ovp | Ocean View Premier | 2 |

### Criterio de conclusao

- [x] Middleware apontando para sistema-os (nao QloApps)
- [ ] Fluxo bidirecional testado end-to-end com sistema-os
- [ ] Channex configurado com room types Duke (6 categorias)
- [ ] Zero cenarios de overbooking

---

## Marco 3: Booking Engine Proprio 📋

**Objetivo:** Canal de venda direta sem comissao de OTA.

**Stack:** Next.js + Stripe + sistema-os API

**Capacidades:**
- [ ] Busca de quartos por data/tipo/ocupacao
- [ ] Fluxo de reserva com pagamento seguro
- [ ] Branding customizavel por hotel
- [ ] Disponibilidade em tempo real (via sistema-os)

---

## Marco 4: Revenue Management Ativo 📋

**Objetivo:** Precificacao inteligente baseada em demanda, concorrencia e ocupacao.

**Base existente:** sistema-os ja monitora 6 concorrentes diariamente.

**Capacidades:**
- [ ] Tarifas por data/temporada (substituir preco fixo)
- [ ] Sugestoes de preco por IA
- [ ] Publicacao automatica de precos no Channex
- [ ] Metricas REVPAR/ADR em tempo real

---

## Decisoes tecnicas

### Principio: middleware e o centro estavel

```
Marco 1:  QloApps    <->  Middleware  <->  Channex  ->  OTAs
Marco 2:  sistema-os <->  Middleware  <->  Channex  ->  OTAs
                          (nao muda)
```

O middleware e a ponte. O PMS muda, o CM nao. O middleware traduz.

### Dependencias externas (intencionais)

| Servico | Custo | Motivo |
|---------|-------|--------|
| Channex | $30-49/mes | Certificacao OTA (barreira intransponivel) |
| Stripe | ~2.5% | Seguranca de pagamento + cobertura global |
| **Todo o resto** | **Nosso** | Codigo, dados, controle |

---

## Repositorios

| Repo | Conteudo |
|------|----------|
| `sistema-os` | PMS + middleware (producao) |
| `ai-brain/projects/ai-pms` | Docs de visao, roadmap, planejamento |

---

## Arquivos de referencia

| Arquivo | Conteudo |
|---------|----------|
| `ECOSYSTEM.md` | Visao completa do ecossistema |
| `COSMO-VISION.md` | Filosofia do produto + Blue Ocean |
| `integracao/CHANNEX-INTEGRATION.md` | Detalhes tecnicos da integracao |
