# Cosmo - Plataforma de Hotelaria

> "Nem todos os funcionários lidam com reservas, mas todos lidam com hóspedes."

---

## Visão

**Cosmo** é uma plataforma base para hotelaria com o **hóspede no centro** — não reservas.

**Modelo de negócio:** "Contrata só eu, cuido de toda a tua infraestrutura de software." Valor justo, baixo e variável.

**Dependências externas aceitas:** Channex (channel manager) + Stripe (pagamentos). Tudo mais é nosso.

> **Para visão completa do ecossistema, leia:** `ECOSYSTEM.md`

---

## Repositórios

| Repo | Papel |
|------|-------|
| `sistema-os` | Plataforma principal (produção Duke Beach). 47 tabelas, 50+ endpoints, FastAPI + PostgreSQL. **Futuro PMS.** |
| `ai-brain/projects/ai-pms` | Laboratório de integração (middleware, docs, visão Cosmo) |
| `~/QloApps` | PMS **temporário** para provar conceito. Será descartado após migração pro sistema-os. |

---

## Status

**Fase atual:** Provar conceito (QloApps + Channex)

- [x] Filosofia e propósito definidos
- [x] Stack pesquisado (QloApps + Channex)
- [x] QloApps instalado e API funcionando
- [x] Conta Channex criada (staging)
- [x] Room types e rate plans mapeados
- [x] Middleware Python criado (FastAPI)
- [x] Módulo PHP webhook no QloApps
- [x] Fluxo QloApps → Middleware testado e funcionando
- [x] Ecossistema documentado (`ECOSYSTEM.md`)
- [x] Sync ARI real com Channex (disponibilidade + tarifas + restricoes)
- [x] ngrok configurado, webhook Channex → Middleware funcionando
- [x] Booking new/modification/cancellation end-to-end
- [x] Booking store (mapeamento Channex ↔ QloApps)
- [ ] Configurar Duke Beach no QloApps (demo)

**Roadmap macro:**
1. Provar conceito com QloApps + Channex ← **Fases 1.1-1.3 completas, falta 1.4 (dados reais)**
2. Migrar PMS pro sistema-os
3. Construir Booking Engine próprio
4. Revenue Management ativo

---

## Estrutura do Projeto

```
ai-pms/
├── README.md                    ← Este arquivo
├── ECOSYSTEM.md                 ← Visão completa do ecossistema (referência principal)
├── COSMO-VISION.md              ← Visão de produto, Blue Ocean, modelo de dados
├── middleware/                   ← Middleware de integração (FastAPI)
│   ├── app/
│   │   ├── main.py              # Webhooks, handlers, sync, debug endpoints
│   │   ├── config.py            # Configurações e mapeamentos
│   │   ├── channex_client.py    # Cliente API Channex
│   │   ├── qloapps_client.py    # Cliente API QloApps (temporário)
│   │   └── booking_store.py     # Mapeamento Channex ↔ QloApps (JSON)
│   ├── data/                    # Dados runtime (gitignored)
│   ├── requirements.txt
│   └── README.md
├── visao/
│   ├── ai-pms-filosofia.md      ← 5 Stakeholders, propósito
│   └── ideia-sistema-social-hospitalidade.md  ← Comunidade de prática (futuro)
├── arquitetura/
│   └── STACK-RESEARCH.md        ← Pesquisa de stack
├── integracao/
│   └── CHANNEX-INTEGRATION.md   ← Integração com Channel Manager
└── lab/
    ├── HOTEL-LAB.md             ← Duke Beach como laboratório, tarefas por área
    └── archive/                 ← Docs arquivados (QloApps-specific)
```

---

## Como Rodar

### 1. QloApps (PMS temporário)

```bash
cd ~/QloApps && php -S localhost:8080
```

- **Front:** http://localhost:8080
- **Admin:** http://localhost:8080/admin964cmnm2w/

### 2. Middleware (Integração)

```bash
cd ~/ai-brain/projects/ai-pms/middleware
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

- **API:** http://localhost:8001
- **Docs:** http://localhost:8001/docs

### 3. Módulo QloApps

O módulo `channexwebhook` já está instalado em:
- `~/QloApps/modules/channexwebhook/`
- Configurado para enviar webhooks para `http://localhost:8001/webhook/qloapps`

---

## Credenciais (Staging)

| Serviço | Credencial |
|---------|------------|
| QloApps API Key | `Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9` |
| Channex API Key | `uTdTdIa1S+kXozFtM8wGtESiMtrzb7aRSZI50Io7rYEsS+EKApvdHjvvx+mqP09v` |
| Channex Property ID | `7c504651-9b33-48bc-9896-892c351f3736` |

---

## Referências

| Doc | Quando consultar |
|-----|------------------|
| `ECOSYSTEM.md` | Visão geral, glossário, roadmap, modelo de negócio |
| `COSMO-VISION.md` | Decisões estratégicas, Blue Ocean |
| `visao/ai-pms-filosofia.md` | Propósito, 5 Stakeholders |
| `integracao/CHANNEX-INTEGRATION.md` | Detalhes técnicos da integração |
| `lab/HOTEL-LAB.md` | Tarefas por área, framework de observação |
| `/home/alejandro/sistema-os/` | Plataforma principal (produção) |
