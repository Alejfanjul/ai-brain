# AI-PMS (Cosmo) - Roadmap

> Ultima atualizacao: 2026-01-31 (Fase 1.2 completa: ARI sync QloApps → Channex)

## Visao geral dos Marcos

| Marco | Descricao | Status |
|-------|-----------|--------|
| 1 | Proof of Concept: QloApps ↔ Channex | 🔄 Em progresso |
| 2 | Migrar PMS para sistema-os | 📋 Futuro |
| 3 | Booking Engine proprio | 📋 Futuro |
| 4 | Revenue Management ativo | 📋 Futuro |

---

## Marco 1: Proof of Concept ↔ Channex 🔄

**Objetivo:** Provar que o middleware consegue sincronizar PMS ↔ Channel Manager bidirecionalmente.

**Stack temporaria:** QloApps (PMS) ↔ Middleware (FastAPI) ↔ Channex (CM)

### Fase 1.1: Infraestrutura ✅

- QloApps instalado e API funcionando (localhost:8080)
- Channex staging configurado (property + room types + rate plans)
- Middleware FastAPI criado (localhost:8001)
- Modulo PHP webhook instalado no QloApps (`channexwebhook`)
- Room type mappings completos (5 tipos)

### Fase 1.2: QloApps → Channex (ARI completo) ✅

**Concluido 2026-01-31**

- Webhook QloApps → Middleware funcionando (booking.created, booking.updated, booking.cancelled)
- Middleware consulta ARI real no QloApps (hotel_ari) — uma chamada retorna disponibilidade E preco
- Push de **disponibilidade** para Channex (POST /availability)
- Push de **tarifas + restricoes** para Channex (POST /restrictions)
- Retry com backoff (5s, 10s, 20s) para lidar com DB locks do PHP
- Sync manual via Swagger: /sync/full, /sync/availability, /sync/rate, /sync/restrictions

**Resultado:** Reserva no QloApps → disponibilidade E tarifa atualizadas automaticamente no Channex.

### Fase 1.3: Channex → QloApps 📋

**Objetivo:** OTA booking chega via Channex → middleware cria no QloApps.

**Pendente:**
- [ ] Expor middleware na internet (ngrok ou cloudflare tunnel)
- [ ] Configurar webhook no Channex (event: booking)
- [ ] Testar fluxo: booking simulado → middleware → QloApps
- [ ] Implementar booking modification/cancellation no QloApps

**Pre-requisito:** URL publica para o middleware.

### Fase 1.4: Validacao com Duke Beach 📋

**Objetivo:** Configurar dados reais do Duke Beach no QloApps como demo.

**Pendente:**
- [ ] Criar property com room types reais (LVU, DLVU, DLVL, LVL, OV, GOVP, GOV)
- [ ] Configurar tarifas reais
- [ ] Testar fluxo completo com dados reais
- [ ] Validar zero overbooking

### Criterio de conclusao do Marco 1

- [x] QloApps booking → Channex ARI atualizado
- [ ] Channex booking → QloApps booking criado
- [ ] Fluxo bidirecional testado com dados reais
- [ ] Zero cenarios de overbooking

---

## Marco 2: Migrar PMS para sistema-os 📋

**Objetivo:** Substituir QloApps pelo sistema-os (plataforma propria, ja em producao no Duke).

**Principio:** O middleware nao muda — so troca o client de QloApps para sistema-os. Channex nem percebe.

### O que o sistema-os ja tem

- 47 tabelas, 50+ endpoints (FastAPI + PostgreSQL/Supabase)
- Gestao de hospedes (40 colunas, campos AI-ready)
- Reservas com relacoes N-N (multi-quarto, multi-hospede)
- Inventario de quartos (7 categorias Duke Beach)
- Monitoramento de precos (6 concorrentes diarios)
- Auth multi-departamento

### O que precisa construir

- [ ] Tabela `tarifas` (diarias por tipo/data/temporada)
- [ ] Tabela `disponibilidade` (bloqueios, min/max noites)
- [ ] Tabela `extras` (late checkout, cama extra, estacionamento)
- [ ] Endpoints ARI (consulta disponibilidade/tarifas)
- [ ] Endpoints booking CRUD

### Criterio de conclusao

- [ ] Middleware apontando para sistema-os (nao QloApps)
- [ ] Fluxo bidirecional funcionando igual ao Marco 1
- [ ] QloApps descomissionado
- [ ] Zero perda de dados na migracao

---

## Marco 3: Booking Engine Proprio 📋

**Objetivo:** Canal de venda direta sem comissao de OTA.

**Stack:** Next.js + Stripe + sistema-os API

**Capacidades:**
- [ ] Busca de quartos por data/tipo/ocupacao
- [ ] Fluxo de reserva com pagamento seguro
- [ ] Branding customizavel por hotel
- [ ] Disponibilidade em tempo real (via sistema-os)

**Resultado:** "Hotel nao precisa de Omnibees." Vendas diretas sem intermediario.

---

## Marco 4: Revenue Management Ativo 📋

**Objetivo:** Precificacao inteligente baseada em demanda, concorrencia e ocupacao.

**Base existente:** sistema-os ja monitora 6 concorrentes diariamente.

**Capacidades:**
- [ ] Sugestoes de preco por IA (por data/tipo/segmento)
- [ ] Publicacao automatica de precos no Channex
- [ ] Metricas REVPAR/ADR em tempo real

**Diferencial:** Interno + AI-native (vs. Climber que e servico externo pago).

---

## Decisoes tecnicas

### Principio: middleware e o centro estavel

```
Fase 1:  QloApps  ↔  Middleware  ↔  Channex  →  OTAs
Fase 2:  sistema-os  ↔  Middleware  ↔  Channex  →  OTAs
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

## Mapa de dados: o que sincroniza entre PMS e Channex

Referencia completa pra saber o que esta implementado e o que falta.

### PMS → Channex (pra OTAs mostrarem listagens)

| Dado | Endpoint Channex | Status | Limitacao atual |
|------|-----------------|--------|-----------------|
| Disponibilidade (qtd quartos) | POST /availability | ✅ Automatico | Conta total no range, nao por dia |
| Tarifa (preco/noite) | POST /restrictions | ✅ Automatico | Preco unico por tipo (sem variacao por data/temporada) |
| Min stay | POST /restrictions | ⚠️ Default fixo (1) | QloApps nao expoe via API; usar /sync/restrictions manual |
| Stop sell | POST /restrictions | ⚠️ Default fixo (false) | Idem |
| Closed to arrival/departure | POST /restrictions | ❌ So manual | Endpoint /sync/restrictions existe pra override |
| Detalhes do quarto (fotos, amenities) | N/A | ❌ Nao sincronizado | Configurar direto no Channex |

### Channex → PMS (quando chega reserva de OTA)

| Dado | Status | Limitacao atual |
|------|--------|-----------------|
| Reserva nova (criar no PMS) | ✅ Codigo pronto | Falta webhook Channex configurado (precisa ngrok) |
| Modificacao de reserva | ❌ TODO no codigo | Nao encontra booking existente pra atualizar |
| Cancelamento de reserva | ❌ TODO no codigo | Nao encontra booking existente pra cancelar |
| Dados do hospede | ⚠️ Parcial | Nome, email, phone. Falta: nacionalidade, idioma, requests |
| Numero de confirmacao OTA | ❌ Nao extraido | Util pra reconciliacao |

### Limitacoes conhecidas (Fase 1)

1. **Preco unico por tipo de quarto** — QloApps retorna `base_price_with_tax` fixo, sem variacao por data ou temporada. Precificacao dinamica vem no Marco 4.
2. **Restricoes sao defaults** — QloApps nao expoe min_stay/stop_sell via API. Usar endpoint manual `/sync/restrictions` pra override. Campos reais vem no Marco 2 (sistema-os).
3. **Sem sync automatico quando hotel muda tarifa** — Webhook so dispara em eventos de booking. Se mudar preco no QloApps sem criar reserva, usar `/sync/full` manual.
4. **Webhook Channex → Middleware precisa de URL publica** — Middleware roda em localhost. Precisa ngrok ou tunnel pra receber bookings de OTAs.
5. **Booking modification/cancellation vindos de OTA** — Codigo recebe o evento mas nao implementa update/cancel no QloApps ainda.

---

## Arquivos de referencia

| Arquivo | Conteudo |
|---------|----------|
| `ECOSYSTEM.md` | Visao completa do ecossistema (ler primeiro) |
| `COSMO-VISION.md` | Filosofia do produto + Blue Ocean |
| `middleware/README.md` | Como rodar o middleware |
| `integracao/CHANNEX-INTEGRATION.md` | Detalhes tecnicos da integracao |
| `visao/ai-pms-filosofia.md` | 5 Stakeholders + proposito |
