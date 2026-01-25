# Sessão 2026-01-25: Middleware QloApps ↔ Channex

**Projeto:** ai-pms
**Duração:** ~2 horas
**Resultado:** Middleware funcionando, fluxo QloApps → Middleware testado com sucesso

---

## O que foi feito

### 1. Criado Middleware FastAPI

**Localização:** `projects/ai-pms/middleware/`

Arquivos criados:
- `app/main.py` - FastAPI com endpoints de webhook
- `app/config.py` - Configurações e mapeamentos de IDs
- `app/channex_client.py` - Cliente async para API Channex
- `app/qloapps_client.py` - Cliente async para API QloApps
- `requirements.txt` - Dependências Python
- `README.md` - Documentação

### 2. Criado Módulo PHP para QloApps

**Localização:** `~/QloApps/modules/channexwebhook/`

O módulo:
- Escuta hooks `actionValidateOrder` e `actionOrderStatusPostUpdate`
- Envia webhook HTTP POST para o middleware
- Inclui dados completos da reserva (room type, datas, cliente)
- Configurável via admin do QloApps

### 3. Testado fluxo QloApps → Middleware

Resultado do teste:
```
INFO:app.main:QloApps webhook received: booking.created
INFO:app.main:QloApps booking created: order 10
INFO:app.main:Booking data: customer=Alejandro Fanjul, rooms=1
INFO:app.main:Room booked: type=2, 2026-01-28 to 2026-01-30
INFO:app.main:Dates affected: ['2026-01-28', '2026-01-29']
INFO:app.main:Channex mapping: room_type=329d23da-..., rate_plan=c4cada39-...
INFO:app.main:SUCCESS: Would sync 2 dates to Channex for room type 2
```

---

## Decisões técnicas

### Webhook vs Polling

**Decisão:** Usar webhooks nos dois sentidos (não polling)

**Motivo:**
- Tempo real
- Menor carga nos servidores
- Arquitetura mais limpa

**Implementação:**
- QloApps → Middleware: Módulo PHP customizado (hooks internos do QloApps não fazem HTTP)
- Channex → Middleware: Webhook nativo do Channex

### Problema do PHP single-threaded

**Problema:** Timeout quando middleware tentava chamar QloApps de volta durante o webhook

**Solução:** Módulo PHP envia todos os dados necessários no payload do webhook, eliminando necessidade de callback

---

## Comandos para rodar

```bash
# Terminal 1 - QloApps
cd ~/QloApps && php -S localhost:8080

# Terminal 2 - Middleware
cd ~/ai-brain/projects/ai-pms/middleware
uvicorn app.main:app --reload --port 8001
```

---

## Próximos passos

1. **Implementar sync ARI real** - Enviar disponibilidade para Channex quando reserva é criada
2. **Expor middleware na internet** - ngrok ou cloudflare tunnel
3. **Configurar webhook Channex** - Para receber reservas de OTAs
4. **Testar fluxo bidirecional** - Reserva em ambas direções

---

## Arquivos modificados/criados

### Criados
- `projects/ai-pms/middleware/` (toda a pasta)
- `~/QloApps/modules/channexwebhook/` (módulo PHP)

### Atualizados
- `projects/ai-pms/README.md`
- `projects/ai-pms/integracao/CHANNEX-INTEGRATION.md`

---

## Aprendizados

1. QloApps usa hooks internos (estilo PrestaShop), não webhooks HTTP nativos
2. PHP built-in server é single-threaded - cuidado com callbacks síncronos
3. Channex webhooks podem chegar fora de ordem - usar como trigger, não como fonte de verdade
4. A classe `HotelCartBookingData` tem método `getCartCurrentDataByCartId` para pegar dados da reserva
