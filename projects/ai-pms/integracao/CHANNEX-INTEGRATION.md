# Integração QloApps ↔ Channex

> Plano de integração entre PMS (QloApps) e Channel Manager (Channex).
>
> **Data:** 2026-01-24
> **Status:** Em planejamento

---

## Objetivo

Criar middleware que sincroniza:
1. **QloApps → Channex:** Disponibilidade, tarifas, restrições
2. **Channex → QloApps:** Reservas das OTAs

---

## Arquitetura

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   QloApps   │         │  Middleware │         │   Channex   │
│    (PMS)    │ ◄─────► │   (Python)  │ ◄─────► │    (CM)     │
└─────────────┘   API   └─────────────┘   API   └─────────────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │  Booking.com  │
                                              │  Airbnb       │
                                              │  Expedia      │
                                              │  50+ OTAs     │
                                              └───────────────┘
```

---

## APIs Envolvidas

### QloApps API

- **Base URL:** `http://localhost:8080/webservice/dispatcher.php`
- **Auth:** HTTP Basic com API Key
- **Formato:** XML
- **Key:** `Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9`

**Endpoints relevantes:**

| Endpoint | Uso na integração |
|----------|-------------------|
| `/hotel_ari` | Ler/escrever disponibilidade e tarifas |
| `/bookings` | Criar reservas vindas das OTAs |
| `/room_types` | Mapear tipos de quarto |
| `/hotels` | Identificar propriedade |
| `/customers` | Criar/atualizar hóspedes |

### Channex API

- **Base URL:** `https://staging.channex.io/api/v1/` (staging)
- **Auth:** API Key no header
- **Formato:** JSON
- **Docs:** https://docs.channex.io/

**Endpoints relevantes:**

| Endpoint | Uso na integração |
|----------|-------------------|
| `/properties` | Configurar propriedade |
| `/room_types` | Mapear tipos de quarto |
| `/rate_plans` | Planos de tarifa |
| `/ari` | Atualizar disponibilidade/tarifas |
| `/bookings` | Receber reservas |

---

## Fluxos de Dados

### Fluxo 1: Push de Disponibilidade (QloApps → Channex)

```
Trigger: Mudança de disponibilidade/tarifa no QloApps

1. Detectar mudança (webhook ou polling)
2. Ler dados do QloApps:
   GET /hotel_ari?id_hotel=1&date_from=X&date_to=Y
3. Transformar XML → JSON
4. Mapear room_type_id QloApps → Channex
5. Enviar para Channex:
   POST /api/v1/restrictions    ← ENDPOINT CORRETO!
6. Channex distribui para OTAs conectadas
```

**Estrutura do request para `/restrictions`:**
```json
{
  "values": [
    {
      "property_id": "uuid",
      "room_type_id": "uuid",
      "rate_plan_id": "uuid",
      "date": "2026-01-25",
      "availability": 5,
      "rate": "1000.00",        // DEVE ser string!
      "min_stay_arrival": 1
    }
  ]
}
```

### Fluxo 2: Receber Reservas (Channex → QloApps)

```
Trigger: Nova reserva via OTA

1. Channex recebe reserva (Booking.com, Airbnb, etc.)
2. Middleware consulta feed de reservas:
   GET /bookings?filter[status]=new
3. Para cada reserva nova:
   a. Transformar JSON → XML
   b. Verificar/criar cliente no QloApps
   c. Criar reserva:
      POST /bookings
   d. Confirmar recebimento no Channex:
      POST /bookings/{id}/ack
4. Atualizar disponibilidade no QloApps
```

---

## Mapeamento de Dados

### IDs Mapeados (Ambiente de Teste)

**Property:** `7c504651-9b33-48bc-9896-892c351f3736` (The Hotel Prime)

| QloApps ID | Nome | Channex Room Type | Channex Rate Plan |
|------------|------|-------------------|-------------------|
| 1 | General Rooms | `3e19102f-29fd-4597-8ef1-6037703056eb` | `69d0f921-5ec5-4712-a50c-69f1853705a9` |
| 2 | Delux Rooms | `329d23da-9238-4b58-b0a0-a7a294e7e024` | `c4cada39-dae3-4813-9d3c-d4f02eda9b0f` |
| 3 | Executive Rooms | `0dd44d4a-38f4-49db-baa9-b837a6d37afe` | `abb98eec-b4e5-469f-a9ae-b630c8546e72` |
| 4 | Luxury Rooms | `54887bb9-aecb-4970-9011-c5e00106bc88` | `ef4da7e1-9555-4ef5-9b8f-ac0bce3d7179` |
| 11 | Upper Laker | `2d655afd-60fd-42ac-9d05-4cddce65bc88` | `e22e0f20-fe38-4ebd-8bd8-519f9dcfab8b` |

### Campos Room Types

| QloApps | Channex | Notas |
|---------|---------|-------|
| `id_room_type` | `room_type_id` | Usar tabela acima |
| `name` | `title` | |
| `max_adults` | `occ_adults` | |
| `max_children` | `occ_children` | |
| - | `occ_infants` | Obrigatório no Channex (pode ser 0) |

### Reservas

| Channex | QloApps | Transformação |
|---------|---------|---------------|
| `arrival_date` | `checkin_date` | Formato de data |
| `departure_date` | `checkout_date` | Formato de data |
| `customer.name` | `firstname + lastname` | Split do nome |
| `customer.email` | `email` | Direto |
| `total_amount` | `total_price_with_tax` | Verificar moeda |
| `status` | `booking_status` | Mapear códigos |

### Status de Reserva

| Channex | QloApps | Código |
|---------|---------|--------|
| `new` | `API_BOOKING_STATUS_NEW` | 1 |
| `modified` | `API_BOOKING_STATUS_NEW` | 1 |
| `cancelled` | `API_BOOKING_STATUS_CANCELLED` | 3 |

---

## Configuração Inicial

### 1. Criar conta staging no Channex

- [x] URL: https://staging.channex.io/
- [x] Conta criada
- [ ] Gerar API Key

### 2. Configurar propriedade no Channex

```bash
# Criar propriedade
POST /properties
{
  "title": "Duke Beach Hotel (Test)",
  "currency": "BRL",
  "timezone": "America/Sao_Paulo"
}
```

### 3. Mapear room types

```bash
# Listar room types do QloApps
curl -u "KEY:" "http://localhost:8080/webservice/dispatcher.php?url=room_types"

# Criar correspondentes no Channex
POST /room_types
{
  "property_id": "xxx",
  "title": "General Rooms",
  "occ_adults": 2,
  "occ_children": 0
}
```

### 4. Criar rate plans

```bash
POST /rate_plans
{
  "room_type_id": "xxx",
  "title": "Standard Rate",
  "currency": "BRL"
}
```

---

## Implementação do Middleware

### Stack sugerido

- **Linguagem:** Python 3.11+
- **Framework:** FastAPI (async, bom para webhooks)
- **Bibliotecas:**
  - `httpx` - Cliente HTTP async
  - `xmltodict` - Conversão XML ↔ dict
  - `pydantic` - Validação de dados
  - `apscheduler` - Jobs agendados (sync periódico)

### Estrutura do projeto

```
channex-middleware/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configurações
│   ├── qloapps/
│   │   ├── client.py        # Cliente API QloApps
│   │   └── models.py        # Modelos de dados
│   ├── channex/
│   │   ├── client.py        # Cliente API Channex
│   │   └── models.py        # Modelos de dados
│   ├── sync/
│   │   ├── availability.py  # Sync de disponibilidade
│   │   └── bookings.py      # Sync de reservas
│   └── mappings/
│       └── room_types.py    # Mapeamento de IDs
├── tests/
├── requirements.txt
└── README.md
```

---

## Próximos Passos

### Concluído ✅
1. [x] Gerar API Key no Channex staging
2. [x] Testar API do Channex via curl
3. [x] Propriedade já existe: "The Hotel Prime"
4. [x] Mapear room types (QloApps ↔ Channex)
5. [x] Criar rate plans para cada room type
6. [x] Testar envio de ARI (disponibilidade + tarifas)

### Pendente
7. [ ] Implementar cliente Python para QloApps
8. [ ] Implementar cliente Python para Channex
9. [ ] Criar sync automático de disponibilidade
10. [ ] Criar sync de reservas (Channex → QloApps)
11. [ ] Testar fluxo completo com OTA real

---

## Recursos

- Channex API Docs: https://docs.channex.io/
- Channex Postman Collection: https://documenter.getpostman.com/view/681982/RztkPpne
- Channex PMS Guide: https://docs.channex.io/guides/pms-integration-guide
- QloApps API: http://localhost:8080/webservice/dispatcher.php
