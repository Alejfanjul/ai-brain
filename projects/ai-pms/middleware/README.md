# AI-PMS Middleware

Middleware FastAPI que sincroniza QloApps (PMS) com Channex (Channel Manager).

## Arquitetura

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   QloApps   │         │  Middleware │         │   Channex   │
│    (PMS)    │ ◄─────► │  (FastAPI)  │ ◄─────► │    (CM)     │
└─────────────┘         └─────────────┘         └─────────────┘
      │                       │                       │
      │  POST /webhook/       │  POST /webhook/       │
      │  qloapps              │  channex              │
      └───────────────────────┴───────────────────────┘
```

## Setup

```bash
cd ~/ai-brain/projects/ai-pms/middleware

# Criar virtualenv (opcional)
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Rodar

```bash
# Desenvolvimento
uvicorn app.main:app --reload --port 8001

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Acesso:
- API: http://localhost:8001
- Docs: http://localhost:8001/docs

## Endpoints

### Webhooks (recebem eventos)

| Endpoint | Origem | Eventos |
|----------|--------|---------|
| `POST /webhook/channex` | Channex | booking_new, booking_modification, booking_cancellation |
| `POST /webhook/qloapps` | QloApps | booking.created, booking.updated, booking.cancelled |

### Utilitários

| Endpoint | Descrição |
|----------|-----------|
| `GET /health` | Health check |
| `GET /docs` | Swagger UI |
| `POST /sync/ari` | Push manual de disponibilidade para Channex |
| `GET /bookings/channex` | Listar reservas do Channex |
| `GET /bookings/qloapps` | Listar reservas do QloApps |

## Configuração

Variáveis de ambiente (ou arquivo `.env`):

```env
QLOAPPS_URL=http://localhost:8080
QLOAPPS_API_KEY=Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9

CHANNEX_URL=https://staging.channex.io/api/v1
CHANNEX_API_KEY=uTdTdIa1S+kXozFtM8wGtESiMtrzb7aRSZI50Io7rYEsS+EKApvdHjvvx+mqP09v
CHANNEX_PROPERTY_ID=7c504651-9b33-48bc-9896-892c351f3736

WEBHOOK_SECRET=
```

## Fluxos

### Reserva OTA → QloApps

1. Hóspede reserva no Booking.com/Airbnb
2. Channex recebe a reserva
3. Channex envia webhook para `/webhook/channex`
4. Middleware busca detalhes completos da reserva
5. Middleware cria reserva no QloApps
6. Middleware confirma (ack) no Channex

### Reserva Direta → Channex

1. Hóspede reserva no motor do QloApps
2. Módulo PHP envia webhook para `/webhook/qloapps`
3. Middleware busca disponibilidade atualizada
4. Middleware envia ARI para Channex
5. Channex atualiza OTAs (menos quartos disponíveis)

## Módulo QloApps

O módulo PHP `channexwebhook` deve estar instalado no QloApps:
- Localização: `~/QloApps/modules/channexwebhook/`
- Configurar URL: `http://localhost:8001/webhook/qloapps`

## Configurar Webhook no Channex

Via API ou UI (https://staging.channex.io/webhooks):

```bash
curl -X POST "https://staging.channex.io/api/v1/webhooks" \
  -H "user-api-key: SUA_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "7c504651-9b33-48bc-9896-892c351f3736",
    "callback_url": "http://SEU_IP:8001/webhook/channex",
    "event_mask": "booking",
    "is_active": true,
    "send_data": true
  }'
```

**Nota:** Para receber webhooks do Channex em desenvolvimento local, você precisa expor o middleware na internet (ex: ngrok, cloudflare tunnel).
