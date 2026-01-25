# Integração QloApps ↔ Channex

> Plano de integração entre PMS (QloApps) e Channel Manager (Channex).
>
> **Atualizado:** 2026-01-25
> **Status:** Middleware funcionando, sync com Channex pendente

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

### Pendente

| Item | Prioridade | Descrição |
|------|------------|-----------|
| Sync ARI real | Alta | Enviar disponibilidade para Channex quando reserva é criada |
| Expor middleware | Alta | ngrok ou cloudflare tunnel para receber webhooks externos |
| Webhook Channex | Alta | Configurar Channex para enviar reservas para middleware |
| Fluxo Channex → QloApps | Média | Criar reserva no QloApps quando OTA reserva |
| Cancelamentos | Média | Sincronizar cancelamentos nos dois sentidos |

---

## Componentes Implementados

### 1. Middleware Python (`middleware/`)

**Localização:** `projects/ai-pms/middleware/`

```
middleware/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app (webhooks)
│   ├── config.py            # Configurações e mapeamentos
│   ├── channex_client.py    # Cliente API Channex (async)
│   └── qloapps_client.py    # Cliente API QloApps (async)
├── requirements.txt
└── README.md
```

**Endpoints:**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/webhook/qloapps` | POST | Recebe webhooks do módulo PHP |
| `/webhook/channex` | POST | Recebe webhooks do Channex |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |
| `/sync/ari` | POST | Sync manual de ARI |
| `/bookings/channex` | GET | Lista reservas do Channex |
| `/bookings/qloapps` | GET | Lista reservas do QloApps |

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

### Fluxo 1: Reserva Direta (QloApps → Channex) ✅ PARCIAL

```
1. Hóspede reserva no motor do QloApps
2. QloApps valida reserva (hook actionValidateOrder)
3. Módulo PHP envia webhook para middleware     ✅ FUNCIONANDO
4. Middleware recebe em /webhook/qloapps        ✅ FUNCIONANDO
5. Middleware extrai room_type, datas           ✅ FUNCIONANDO
6. Middleware mapeia para IDs Channex           ✅ FUNCIONANDO
7. Middleware envia ARI para Channex            ⏳ TODO
8. Channex distribui para OTAs                  ⏳ TODO
```

**Request para atualizar ARI no Channex:**
```json
POST /api/v1/restrictions
{
  "values": [
    {
      "property_id": "7c504651-9b33-48bc-9896-892c351f3736",
      "room_type_id": "329d23da-9238-4b58-b0a0-a7a294e7e024",
      "rate_plan_id": "c4cada39-dae3-4813-9d3c-d4f02eda9b0f",
      "date": "2026-01-28",
      "availability": 4,
      "rate": "350.00"
    }
  ]
}
```

### Fluxo 2: Reserva OTA (Channex → QloApps) ⏳ TODO

```
1. Hóspede reserva no Booking.com/Airbnb
2. Channex recebe reserva
3. Channex envia webhook para middleware        ⏳ Precisa configurar
4. Middleware recebe em /webhook/channex        ✅ Endpoint pronto
5. Middleware busca detalhes: GET /bookings/{id}
6. Middleware transforma JSON → formato QloApps
7. Middleware cria reserva no QloApps
8. Middleware confirma: POST /bookings/{id}/ack
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

## Próximos Passos Detalhados

### 1. Implementar sync ARI real

No arquivo `middleware/app/main.py`, função `handle_qloapps_booking_created`:

```python
# Atual: apenas loga
logger.info(f"SUCCESS: Would sync {len(dates_to_update)} dates to Channex")

# Implementar:
# 1. Buscar disponibilidade atual do QloApps
availability = await qloapps.get_availability(hotel_id=1, date_from=checkin, date_to=checkout)

# 2. Montar payload para Channex
values = []
for date in dates_to_update:
    values.append({
        "property_id": settings.channex_property_id,
        "room_type_id": channex_room_type,
        "rate_plan_id": channex_rate_plan,
        "date": date,
        "availability": calcular_disponibilidade(availability, date),
        "rate": str(obter_tarifa(availability, date)),
    })

# 3. Enviar para Channex
result = await channex.update_restrictions(values)
```

### 2. Expor middleware na internet

**Opção A - ngrok:**
```bash
ngrok http 8001
# Copiar URL: https://abc123.ngrok.io
```

**Opção B - Cloudflare Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8001
```

### 3. Configurar webhook no Channex

Após ter URL pública, criar webhook via API ou UI:
- URL: `https://SEU_DOMINIO/webhook/channex`
- Evento: `booking` (ou `*` para todos)
- `is_active: true`
- `send_data: true`

### 4. Testar fluxo bidirecional

1. Criar reserva no QloApps → verificar se Channex recebeu ARI
2. Criar reserva no Channex (simular OTA) → verificar se QloApps recebeu

---

## Recursos

- Channex API Docs: https://docs.channex.io/
- Channex Webhooks: https://docs.channex.io/api-v.1-documentation/webhook-collection
- Channex PMS Guide: https://docs.channex.io/guides/pms-integration-guide
- QloApps API: http://localhost:8080/webservice/dispatcher.php
