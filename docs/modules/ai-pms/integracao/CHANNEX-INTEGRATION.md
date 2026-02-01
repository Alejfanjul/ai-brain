# Integracao sistema-os <-> Channex

> Detalhes tecnicos da integracao entre PMS (sistema-os) e Channel Manager (Channex).
>
> **Atualizado:** 2026-02-01
> **Status:** Marco 2 — middleware migrado para sistema-os, endpoints Channex criados

---

## Objetivo

Middleware que sincroniza:
1. **sistema-os -> Channex:** Disponibilidade, tarifas, restricoes (ARI)
2. **Channex -> sistema-os:** Reservas das OTAs (create, modify, cancel)

---

## Arquitetura

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ sistema-os  │         │  Middleware  │         │   Channex   │
│    (PMS)    │ ◄─────► │  (FastAPI)   │ ◄─────► │    (CM)     │
└─────────────┘   API   └─────────────┘   API   └─────────────┘
  localhost:8000     localhost:8001              ▲         │
                                                │ webhook  │
                                                └──────────┘
                                                           │
                                                           ▼
                                                   ┌───────────────┐
                                                   │  Booking.com  │
                                                   │  Airbnb       │
                                                   │  Expedia      │
                                                   │  50+ OTAs     │
                                                   └───────────────┘
```

**Comunicacao:**
- Channex -> Middleware: Webhook nativo do Channex (URL publica via ngrok)
- Middleware -> sistema-os: HTTP requests (JSON, async)
- Middleware -> Channex: HTTP requests (JSON, async)

---

## Historico

### Marco 1 (QloApps) — Completo ✅

| Fase | Data | Descricao |
|------|------|-----------|
| 1.1 | 2026-01-24 | Infraestrutura: QloApps + Channex + middleware |
| 1.2 | 2026-01-31 | QloApps -> Channex (ARI sync) |
| 1.3 | 2026-02-01 | Channex -> QloApps (booking lifecycle) |
| 1.4 | Eliminada | Incorporada ao Marco 2 |

### Marco 2 (sistema-os) — Em Progresso 🔄

| Item | Data | Status |
|------|------|--------|
| Enum CategoriaApartamento atualizado | 2026-02-01 | ✅ |
| Middleware movido para sistema-os | 2026-02-01 | ✅ |
| Tabela tarifas criada | 2026-02-01 | ✅ |
| Endpoints Channex no sistema-os | 2026-02-01 | ✅ |
| sistemeos_client.py | 2026-02-01 | ✅ |
| Middleware reescrito para sistema-os | 2026-02-01 | ✅ |
| Setup script Channex (room types Duke) | 2026-02-01 | ✅ |
| Executar setup + atualizar UUIDs | - | Pendente |
| Teste end-to-end | - | Pendente |

---

## Componentes

### 1. Middleware (`sistema-os/middleware/`)

```
middleware/
├── app/
│   ├── main.py              # FastAPI app (webhooks, handlers, sync)
│   ├── config.py            # Configuracoes e mapeamentos categoria -> UUID
│   ├── channex_client.py    # Cliente API Channex (async)
│   ├── sistemeos_client.py  # Cliente API sistema-os (async)
│   ├── booking_store.py     # Mapeamento Channex <-> sistema-os (JSON file)
│   └── qloapps_client.py    # [LEGADO] referencia
├── scripts/
│   └── setup_channex_duke.py
├── data/
│   └── bookings.json
└── requirements.txt
```

**Rodar:**
```bash
cd ~/sistema-os/middleware
uvicorn app.main:app --reload --port 8001
```

### 2. Endpoints sistema-os (`sistema-os/app/api/v1/endpoints/channex.py`)

| Endpoint | Descricao |
|----------|-----------|
| `GET /api/v1/channex/ari` | Disponibilidade + tarifa por categoria para range de datas |
| `POST /api/v1/channex/booking` | Criar booking (find-or-create hospede + auto-assign quarto) |
| `PATCH /api/v1/channex/booking/{id}` | Atualizar booking |
| `POST /api/v1/channex/booking/{id}/cancel` | Cancelar booking |

### 3. Channex API

- **Base URL:** `https://staging.channex.io/api/v1/`
- **Auth:** Header `user-api-key`
- **Formato:** JSON
- **Docs:** https://docs.channex.io/

---

## Mapeamento de Dados

### Property

**Channex Property ID:** `7c504651-9b33-48bc-9896-892c351f3736`

### Categorias Duke Beach -> Channex

| Categoria | Nome | Unidades | Channex Room Type | Channex Rate Plan |
|-----------|------|----------|-------------------|-------------------|
| lvu | Lateral Vista Urbana | 11 | TODO: setup_channex_duke.py | TODO |
| dlvu | De Luxe Vista Urbana | 2 | TODO | TODO |
| dlvl | De Luxe Vista Lateral | 2 | TODO | TODO |
| lvl | Lateral Vista Lateral | 11 | TODO | TODO |
| ov | Ocean View | 5 | TODO | TODO |
| ovp | Ocean View Premier | 2 | TODO | TODO |

> UUIDs serao preenchidos apos rodar `scripts/setup_channex_duke.py`

### Mapeamento legado (QloApps) — Referencia

| QloApps ID | Nome | Channex Room Type |
|------------|------|-------------------|
| 1 | General Rooms | `3e19102f-...` |
| 2 | Delux Rooms | `329d23da-...` |
| 3 | Executive Rooms | `0dd44d4a-...` |
| 4 | Luxury Rooms | `54887bb9-...` |
| 11 | Upper Laker | `2d655afd-...` |

---

## Fluxos de Dados

### Fluxo 1: Sync ARI (sistema-os -> Channex)

```
1. Middleware chama GET /api/v1/channex/ari?date_from=X&date_to=Y
2. sistema-os calcula disponibilidade por categoria (total - ocupado)
3. sistema-os busca tarifa por categoria na tabela tarifas
4. Retorna JSON: {room_types: [{categoria, total, available, rate, currency}]}
5. Middleware envia disponibilidade para Channex (POST /availability)
6. Middleware envia tarifas + restricoes para Channex (POST /restrictions)
7. Channex distribui para OTAs
```

**Trigger:** Manual via `/sync/full` ou automatico apos booking create/modify/cancel.

### Fluxo 2: Booking OTA -> sistema-os (Nova)

```
1. Hospede reserva no Booking.com/Airbnb
2. Channex recebe reserva
3. Channex envia webhook booking_new
4. Middleware checa idempotencia (booking_store)
5. Middleware busca revision: GET /booking_revisions/{id}
6. Middleware transforma Channex -> sistema-os (extract guest + room info)
7. Middleware chama POST /api/v1/channex/booking
8. sistema-os: find-or-create hospede (por email -> telefone -> criar novo)
9. sistema-os: auto-assign quarto da categoria solicitada
10. sistema-os: cria reserva + reserva_apartamento
11. Middleware salva mapeamento (bookings.json)
12. Middleware ack: POST /booking_revisions/{id}/ack
13. Middleware re-sync ARI (disponibilidade diminuiu)
```

### Fluxo 3: Booking OTA -> sistema-os (Modificacao)

```
1. Channex envia webhook booking_modification
2. Middleware busca revision + lookup no booking_store
3. Middleware chama PATCH /api/v1/channex/booking/{id}
   (hospede_nome, hospede_telefone, adultos, criancas)
4. Atualiza status no booking_store -> ack -> re-sync ARI
```

### Fluxo 4: Booking OTA -> sistema-os (Cancelamento)

```
1. Channex envia webhook booking_cancellation
2. Middleware busca revision + lookup no booking_store
3. Middleware chama POST /api/v1/channex/booking/{id}/cancel
4. sistema-os seta status=CANCELADA, motivo, cancelado_em
5. Status -> cancelled no booking_store -> ack -> re-sync ARI
```

---

## Webhooks Channex

### Eventos usados

| Evento | Descricao |
|--------|-----------|
| `booking_new` | Nova reserva de OTA |
| `booking_modification` | Reserva modificada |
| `booking_cancellation` | Reserva cancelada |

### Configurar webhook

```bash
curl -X POST "https://staging.channex.io/api/v1/webhooks" \
  -H "user-api-key: SUA_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "7c504651-9b33-48bc-9896-892c351f3736",
    "callback_url": "https://SUA_URL/webhook/channex",
    "event_mask": "booking",
    "is_active": true,
    "send_data": true
  }'
```

### Aprendizados

- Webhooks enviam `booking_revision_id` (nao `revision_id`) em modification/cancellation
- Channex envia 2 webhooks simultaneos: generico `booking` + especifico
- Ack funciona por revision: `POST /booking_revisions/{revision_id}/ack`
- Para development local: ngrok necessario (URL publica)

---

## Diferencas Marco 1 (QloApps) vs Marco 2 (sistema-os)

| Aspecto | QloApps | sistema-os |
|---------|---------|------------|
| Formato API | XML (com JSON hack) | JSON nativo |
| ARI query | hotel_ari (parse complexo) | GET /channex/ari (JSON limpo) |
| Criar booking | POST com payload XML-like | POST com JSON simples |
| Auto-assign quarto | Manual (middleware escolhia) | Automatico (sistema-os) |
| Find-or-create hospede | Nao existia | Automatico (sistema-os) |
| Modificar booking | GET -> merge -> PUT (fragil) | PATCH (simples) |
| Cancelar booking | Best-effort (PHP limitado) | POST /cancel (funciona) |
| Retry backoff | Necessario (PHP DB locks) | Nao necessario |
| Room types | IDs numericos (1, 2, 3...) | Categorias string (lvu, ov...) |
| Tax split | Estimado 80/20 | Sem tax split (preco unico) |

---

## Recursos

- Channex API Docs: https://docs.channex.io/
- Channex Webhooks: https://docs.channex.io/api-v.1-documentation/webhook-collection
- Channex PMS Guide: https://docs.channex.io/guides/pms-integration-guide
