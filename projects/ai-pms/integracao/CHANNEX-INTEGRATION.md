# Integração QloApps ↔ Channex

> Plano de integração entre PMS (QloApps) e Channel Manager (Channex).
>
> **Atualizado:** 2026-02-01
> **Status:** Fase 1.3 completa — fluxo bidirecional QloApps ↔ Channex funcionando

---

## Objetivo

Criar middleware que sincroniza:
1. **QloApps → Channex:** Disponibilidade, tarifas, restrições (ARI)
2. **Channex → QloApps:** Reservas das OTAs

---

## Arquitetura

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   QloApps   │         │  Middleware │         │   Channex   │
│    (PMS)    │ ──────► │  (FastAPI)  │ ──────► │    (CM)     │
└─────────────┘ webhook └─────────────┘   API   └─────────────┘
                              ▲                       │
                              │      webhook          │
                              └───────────────────────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │  Booking.com  │
                                              │  Airbnb       │
                                              │  Expedia      │
                                              │  50+ OTAs     │
                                              └───────────────┘
```

**Comunicação via Webhooks (não polling):**
- QloApps → Middleware: Módulo PHP `channexwebhook`
- Channex → Middleware: Webhook nativo do Channex

---

## Progresso

### Concluído ✅

| Item | Data | Detalhes |
|------|------|----------|
| API Key Channex staging | 2026-01-24 | Gerada e testada |
| Propriedade configurada | 2026-01-24 | "The Hotel Prime" |
| Room types mapeados | 2026-01-24 | 5 tipos (ver tabela abaixo) |
| Rate plans criados | 2026-01-24 | 1 por room type |
| Teste manual ARI | 2026-01-24 | QloApps → Channex funcionou |
| Teste manual booking | 2026-01-24 | Channex → QloApps funcionou |
| **Middleware criado** | 2026-01-25 | FastAPI em `middleware/` |
| **Módulo PHP criado** | 2026-01-25 | `channexwebhook` instalado |
| **Webhook QloApps → Middleware** | 2026-01-25 | Testado e funcionando |

| **ARI sync real** | 2026-01-31 | Disponibilidade + tarifas + restricoes (Fase 1.2) |
| **ngrok configurado** | 2026-02-01 | URL publica para receber webhooks Channex |
| **Webhook Channex** | 2026-02-01 | `send_data: true`, `event_mask: booking` |
| **Booking CRS App** | 2026-02-01 | Instalado para simular bookings OTA |
| **booking_store.py** | 2026-02-01 | Mapeamento Channex ↔ QloApps (file-based) |
| **Booking new** | 2026-02-01 | Channex → QloApps com idempotencia + ack + ARI re-sync |
| **Booking modification** | 2026-02-01 | GET→merge→PUT + ack + ARI re-sync |
| **Booking cancellation** | 2026-02-01 | Cancel attempt + status tracking + ack + ARI re-sync |

### Proximo

| Item | Prioridade | Descrição |
|------|------------|-----------|
| Validacao Duke Beach | Alta | Dados reais do hotel no QloApps (Fase 1.4) |
| Migrar para sistema-os | Media | Substituir QloApps pelo PMS proprio (Marco 2) |

---

## Componentes Implementados

### 1. Middleware Python (`middleware/`)

**Localização:** `projects/ai-pms/middleware/`

```
middleware/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app (webhooks, handlers, sync)
│   ├── config.py            # Configurações e mapeamentos
│   ├── channex_client.py    # Cliente API Channex (async)
│   ├── qloapps_client.py    # Cliente API QloApps (async, temporario)
│   └── booking_store.py     # Mapeamento Channex ↔ QloApps (JSON file)
├── data/
│   └── bookings.json        # Booking mappings (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

**Endpoints principais:**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/webhook/qloapps` | POST | Recebe webhooks do módulo PHP |
| `/webhook/channex` | POST | Recebe webhooks do Channex |
| `/webhook/channex/debug` | POST | Debug: loga webhook raw |
| `/bookings/mapping` | GET | Mapeamentos Channex ↔ QloApps |
| `/bookings/channex/feed` | GET | Revisions nao-ack'd no Channex |
| `/sync/full` | POST | Sync ARI completo (disponibilidade + tarifa) |
| `/sync/availability` | POST | Push manual de disponibilidade |
| `/sync/rate` | POST | Push manual de tarifa |
| `/sync/restrictions` | POST | Push manual de restricoes |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |

**Rodar:**
```bash
cd ~/ai-brain/projects/ai-pms/middleware
uvicorn app.main:app --reload --port 8001
```

### 2. Módulo QloApps (`channexwebhook`)

**Localização:** `~/QloApps/modules/channexwebhook/`

**Hooks registrados:**
- `actionValidateOrder` - Nova reserva criada
- `actionOrderStatusPostUpdate` - Status alterado

**Payload enviado:**
```json
{
  "event": "booking.created",
  "timestamp": "2026-01-25T10:00:00-03:00",
  "source": "qloapps",
  "data": {
    "order_id": 10,
    "reference": "ABCDEF",
    "total": 500.00,
    "currency": "BRL",
    "customer_id": 2,
    "customer_email": "guest@email.com",
    "customer_firstname": "Nome",
    "customer_lastname": "Sobrenome",
    "date": "2026-01-25 10:00:00",
    "rooms": [
      {
        "id_room_type": 2,
        "checkin_date": "2026-01-28",
        "checkout_date": "2026-01-30",
        "id_room": 5,
        "adults": 2,
        "children": 0
      }
    ]
  }
}
```

**Configurar:** Admin QloApps → Modules → Channex Webhook → Configure

---

## APIs Envolvidas

### QloApps API

- **Base URL:** `http://localhost:8080/webservice/dispatcher.php`
- **Auth:** HTTP Basic com API Key
- **Formato:** XML (suporta JSON via `output_format=JSON`)
- **Key:** `Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9`

### Channex API

- **Base URL:** `https://staging.channex.io/api/v1/`
- **Auth:** Header `user-api-key`
- **Formato:** JSON
- **Key:** `uTdTdIa1S+kXozFtM8wGtESiMtrzb7aRSZI50Io7rYEsS+EKApvdHjvvx+mqP09v`
- **Docs:** https://docs.channex.io/

---

## Mapeamento de Dados

### Property

**Channex Property ID:** `7c504651-9b33-48bc-9896-892c351f3736` (The Hotel Prime)

### Room Types e Rate Plans

| QloApps ID | Nome | Channex Room Type | Channex Rate Plan |
|------------|------|-------------------|-------------------|
| 1 | General Rooms | `3e19102f-29fd-4597-8ef1-6037703056eb` | `69d0f921-5ec5-4712-a50c-69f1853705a9` |
| 2 | Delux Rooms | `329d23da-9238-4b58-b0a0-a7a294e7e024` | `c4cada39-dae3-4813-9d3c-d4f02eda9b0f` |
| 3 | Executive Rooms | `0dd44d4a-38f4-49db-baa9-b837a6d37afe` | `abb98eec-b4e5-469f-a9ae-b630c8546e72` |
| 4 | Luxury Rooms | `54887bb9-aecb-4970-9011-c5e00106bc88` | `ef4da7e1-9555-4ef5-9b8f-ac0bce3d7179` |
| 11 | Upper Laker | `2d655afd-60fd-42ac-9d05-4cddce65bc88` | `e22e0f20-fe38-4ebd-8bd8-519f9dcfab8b` |

---

## Fluxos de Dados

### Fluxo 1: Reserva Direta (QloApps → Channex) ✅

```
1. Hospede reserva no motor do QloApps
2. QloApps valida reserva (hook actionValidateOrder)
3. Modulo PHP envia webhook para middleware         ✅
4. Middleware recebe em /webhook/qloapps             ✅
5. Middleware consulta ARI real no QloApps           ✅
6. Middleware envia disponibilidade (POST /availability)  ✅
7. Middleware envia tarifas (POST /restrictions)     ✅
8. Channex distribui para OTAs                       ✅
```

### Fluxo 2: Reserva OTA — Nova (Channex → QloApps) ✅

```
1. Hospede reserva no Booking.com/Airbnb
2. Channex recebe reserva
3. Channex envia webhook booking_new + booking       ✅
4. Middleware checa idempotencia (booking_store)      ✅
5. Middleware busca revision: GET /booking_revisions/{id}  ✅
6. Middleware transforma Channex → QloApps           ✅
7. Middleware cria reserva no QloApps                ✅
8. Middleware salva mapeamento (bookings.json)        ✅
9. Middleware ack: POST /booking_revisions/{id}/ack  ✅
10. Middleware re-sync ARI                           ✅
```

### Fluxo 3: Reserva OTA — Modificacao ✅

```
1. Channex envia webhook booking_modification        ✅
2. Middleware busca revision + lookup no booking_store ✅
3. GET booking QloApps → merge guest changes → PUT   ✅
4. Atualiza status → ack → re-sync ARI              ✅
```

### Fluxo 4: Reserva OTA — Cancelamento ✅

```
1. Channex envia webhook booking_cancellation        ✅
2. Middleware busca revision + lookup no booking_store ✅
3. Cancel attempt no QloApps (best-effort)           ✅
4. Status → cancelled no booking_store → ack → ARI  ✅
```

---

## Webhooks do Channex

### Eventos disponíveis

| Evento | Descrição |
|--------|-----------|
| `booking` | Qualquer mudança de reserva |
| `booking_new` | Nova reserva |
| `booking_modification` | Reserva modificada |
| `booking_cancellation` | Reserva cancelada |
| `ari` | Mudança de disponibilidade |
| `non_acked_booking` | Reserva não confirmada (30min) |

### Configurar webhook

```bash
curl -X POST "https://staging.channex.io/api/v1/webhooks" \
  -H "user-api-key: SUA_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "7c504651-9b33-48bc-9896-892c351f3736",
    "callback_url": "https://SEU_IP_PUBLICO/webhook/channex",
    "event_mask": "booking",
    "is_active": true,
    "send_data": true
  }'
```

**Importante:** Para desenvolvimento local, precisa expor o middleware na internet (ngrok, cloudflare tunnel, etc).

---

## Proximos Passos

### Fase 1.4: Validacao com Duke Beach

1. Criar property no QloApps com room types reais do Duke (LVU, DLVU, DLVL, LVL, OV, GOVP, GOV)
2. Configurar tarifas reais
3. Testar fluxo completo com dados reais
4. Validar zero overbooking

### Marco 2: Migrar para sistema-os

1. Criar endpoints ARI e booking CRUD no sistema-os
2. Criar `sistemeos_client.py` no middleware (substitui `qloapps_client.py`)
3. Testar fluxo bidirecional com sistema-os
4. Descomissionar QloApps

---

## Recursos

- Channex API Docs: https://docs.channex.io/
- Channex Webhooks: https://docs.channex.io/api-v.1-documentation/webhook-collection
- Channex PMS Guide: https://docs.channex.io/guides/pms-integration-guide
- QloApps API: http://localhost:8080/webservice/dispatcher.php
