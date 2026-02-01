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

### Sync Manual (para testar)

| Endpoint | Descrição |
|----------|-----------|
| `POST /sync/full` | Consulta QloApps e envia ARI completo (disponibilidade + tarifa) pro Channex |
| `POST /sync/availability` | Push manual de disponibilidade |
| `POST /sync/rate` | Push manual de tarifa |
| `POST /sync/restrictions` | Push manual de restricoes (min_stay, stop_sell, etc.) |

### Debug

| Endpoint | Descrição |
|----------|-----------|
| `POST /webhook/channex/debug` | Captura webhook Channex raw (loga JSON completo) |
| `GET /bookings/mapping` | Mapeamentos Channex ↔ QloApps (booking_store) |
| `GET /bookings/channex/feed` | Revisions nao-confirmadas no Channex |

### Consultas e Status

| Endpoint | Descrição |
|----------|-----------|
| `GET /health` | Health check |
| `GET /docs` | Swagger UI |
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

### Reserva OTA → QloApps (Fase 1.3 ✅)

1. Hospede reserva no Booking.com/Airbnb
2. Channex recebe a reserva
3. Channex envia webhook para `/webhook/channex` (event: `booking_new`)
4. Middleware checa idempotencia (booking_store)
5. Middleware busca detalhes via `GET /booking_revisions/{revision_id}`
6. Middleware transforma formato Channex → QloApps
7. Middleware cria reserva no QloApps (`POST /bookings`)
8. Middleware salva mapeamento em `data/bookings.json`
9. Middleware confirma (ack) no Channex (`POST /booking_revisions/{id}/ack`)
10. Middleware re-sync ARI (disponibilidade atualizada)

### Modificacao OTA → QloApps (Fase 1.3 ✅)

1. Channex envia webhook `booking_modification`
2. Middleware busca revision + lookup no booking_store
3. GET booking atual do QloApps → merge guest changes → PUT
4. Atualiza status no booking_store → ack → re-sync ARI

### Cancelamento OTA → QloApps (Fase 1.3 ✅)

1. Channex envia webhook `booking_cancellation`
2. Middleware busca revision + lookup no booking_store
3. Cancel attempt no QloApps (best-effort)
4. Atualiza status → `cancelled` no booking_store → ack → re-sync ARI

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

Ver secao **ngrok** abaixo para setup completo. O webhook precisa de URL publica.

Tambem pode configurar via UI: https://staging.channex.io/ → Webhooks

## ngrok (URL publica para desenvolvimento)

O Channex precisa de uma URL publica pra enviar webhooks. Como o middleware roda em localhost, usamos ngrok pra criar um tunel.

### Instalacao

Ja instalado: `~/.local/bin/ngrok` (v3.35.0)

Se precisar reinstalar:
```bash
# Linux
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok-v3-stable-linux-amd64.tgz | tar xz -C ~/.local/bin/

# Autenticar (conta gratuita em https://dashboard.ngrok.com)
ngrok config add-authtoken SEU_TOKEN
```

### Como usar

**1. Subir o middleware (terminal 1):**
```bash
cd ~/ai-brain/projects/ai-pms/middleware
uvicorn app.main:app --reload --port 8001
```

**2. Subir o ngrok (terminal 2):**
```bash
ngrok http 8001
```

Vai aparecer algo assim:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8001
```

**3. Configurar webhook no Channex** com a URL do ngrok:
```bash
curl -X POST "https://staging.channex.io/api/v1/webhooks" \
  -H "user-api-key: SUA_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "7c504651-9b33-48bc-9896-892c351f3736",
    "callback_url": "https://abc123.ngrok-free.app/webhook/channex",
    "event_mask": "booking",
    "is_active": true,
    "send_data": true
  }'
```

### Cuidados

- **URL muda** toda vez que reinicia o ngrok (plano gratuito). Precisa atualizar o webhook no Channex.
- **Plano pago** ($8/mes) da URL fixa (ex: `https://cosmo.ngrok.io`). Vale a pena se usar por bastante tempo.
- **Dashboard ngrok**: https://dashboard.ngrok.com — mostra requests recebidos em tempo real (util pra debug).
- **Testar se funciona**: acesse `https://SUA_URL.ngrok-free.app/docs` no navegador — deve abrir o Swagger.

### Rotina diaria de desenvolvimento

```bash
# Terminal 1: QloApps (se nao estiver rodando)
# (verificar se Docker do QloApps esta up)

# Terminal 2: Middleware
cd ~/ai-brain/projects/ai-pms/middleware && uvicorn app.main:app --reload --port 8001

# Terminal 3: ngrok
ngrok http 8001
```

Os 3 terminais precisam ficar abertos durante o desenvolvimento.
