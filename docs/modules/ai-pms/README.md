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
| `sistema-os` | Plataforma principal (produção Duke Beach) + **Middleware Channex** (`middleware/`). FastAPI + PostgreSQL. |
| `ai-brain/projects/ai-pms` | Docs de visão, planejamento, integração. **Código migrou para sistema-os.** |

> **QloApps descartado.** Serviu como POC (Marco 1, Fases 1.1-1.3). Substituído pelo sistema-os.

---

## Status

**Fase atual:** Marco 2 — Migrar PMS de QloApps para sistema-os

**Marco 1 (POC QloApps + Channex):** Concluído (Fases 1.1-1.3)
- [x] Filosofia e propósito definidos
- [x] Stack pesquisado (QloApps + Channex)
- [x] Middleware Python criado (FastAPI)
- [x] Sync ARI real com Channex (disponibilidade + tarifas + restricoes)
- [x] Booking new/modification/cancellation end-to-end
- [x] Booking store (mapeamento Channex ↔ PMS)

**Marco 2 (sistema-os + Channex):** Em progresso
- [x] Middleware migrado para sistema-os/middleware/
- [x] Categorias atualizadas (GOVP/GOV → OVP)
- [ ] Tabela tarifas (preco fixo por categoria)
- [ ] Endpoints Channex (ARI + booking CRUD com auto-assign)
- [ ] sistemeos_client.py (substitui qloapps_client.py)
- [ ] Swap middleware para sistema-os
- [ ] Room types Duke no Channex

**Roadmap macro:**
1. ~~Provar conceito com QloApps + Channex~~ ← **Concluído**
2. Migrar PMS pro sistema-os ← **Em progresso**
3. Construir Booking Engine próprio
4. Revenue Management ativo

---

## Estrutura do Projeto

```
ai-pms/
├── README.md                    ← Este arquivo
├── ECOSYSTEM.md                 ← Visão completa do ecossistema
├── COSMO-VISION.md              ← Visão de produto, Blue Ocean
├── ROADMAP.md                   ← Roadmap detalhado
├── visao/
│   ├── ai-pms-filosofia.md      ← 5 Stakeholders, propósito
│   └── ideia-sistema-social-hospitalidade.md
├── arquitetura/
│   └── STACK-RESEARCH.md        ← Pesquisa de stack
├── integracao/
│   └── CHANNEX-INTEGRATION.md   ← Integração com Channel Manager
└── lab/
    ├── HOTEL-LAB.md             ← Duke Beach como laboratório
    └── archive/                 ← Docs arquivados (QloApps-specific)
```

> **Código do middleware:** `~/sistema-os/middleware/`

---

## Como Rodar

### Middleware (Integração Channex)

```bash
cd ~/sistema-os/middleware
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

- **API:** http://localhost:8001
- **Docs:** http://localhost:8001/docs

### sistema-os (PMS)

```bash
cd ~/sistema-os
uvicorn app.main:app --reload --port 8000
```

---

## Credenciais (Staging)

| Serviço | Credencial |
|---------|------------|
| Channex API Key | `uTdTdIa1S+kXozFtM8wGtESiMtrzb7aRSZI50Io7rYEsS+EKApvdHjvvx+mqP09v` |
| Channex Property ID | `7c504651-9b33-48bc-9896-892c351f3736` |

---

## Referências

| Doc | Quando consultar |
|-----|------------------|
| `ECOSYSTEM.md` | Visão geral, glossário, roadmap, modelo de negócio |
| `COSMO-VISION.md` | Decisões estratégicas, Blue Ocean |
| `ROADMAP.md` | Roadmap detalhado com todos os marcos |
| `visao/ai-pms-filosofia.md` | Propósito, 5 Stakeholders |
| `integracao/CHANNEX-INTEGRATION.md` | Detalhes técnicos da integração |
| `lab/HOTEL-LAB.md` | Tarefas por área, framework de observação |
| `~/sistema-os/` | Plataforma principal + middleware (produção) |
