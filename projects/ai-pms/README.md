# Cosmo - Plataforma de Hotelaria

> "Nem todos os funcionários lidam com reservas, mas todos lidam com hóspedes."

---

## Visão

**Cosmo** é uma plataforma base para hotelaria com o **hóspede no centro** — não reservas.

A hotelaria se industrializou, mas nunca se digitalizou de verdade. Sistemas atuais são versões digitais fragmentadas de processos analógicos, centrados em reservas, usados apenas pela recepção.

**Nossa proposta:** Sistema onde todos os funcionários contribuem, porque todos impactam o hóspede de alguma maneira.

---

## Status

**Fase:** Integração QloApps ↔ Channex (em progresso)

- [x] Filosofia e propósito definidos
- [x] Stack open source pesquisado (QloApps + Channex)
- [x] QloApps instalado e API funcionando
- [x] Conta Channex criada (staging)
- [x] Room types e rate plans mapeados
- [x] **Middleware Python criado** (FastAPI)
- [x] **Módulo PHP webhook no QloApps**
- [x] **Fluxo QloApps → Middleware testado e funcionando**
- [ ] Implementar sync real com Channex (ARI)
- [ ] Configurar webhook Channex → Middleware
- [ ] Análise de Oceano Azul
- [ ] Primeiro MVP/protótipo

---

## Estrutura do Projeto

```
ai-pms/
├── README.md                    ← Este arquivo
├── COSMO-VISION.md              ← Visão completa do produto
├── middleware/                  ← 🆕 Middleware de integração
│   ├── app/
│   │   ├── main.py              # FastAPI app (webhooks)
│   │   ├── config.py            # Configurações e mapeamentos
│   │   ├── channex_client.py    # Cliente API Channex
│   │   └── qloapps_client.py    # Cliente API QloApps
│   ├── requirements.txt
│   └── README.md
├── visao/
│   ├── ai-pms-filosofia.md      ← Propósito e filosofia
│   └── ideia-sistema-social-hospitalidade.md
├── arquitetura/
│   ├── HOTEL-ARCHITECTURE.md    ← Arquitetura técnica
│   └── STACK-RESEARCH.md        ← Pesquisa de stack
├── integracao/
│   └── CHANNEX-INTEGRATION.md   ← Plano de integração com Channel Manager
└── lab/
    ├── HOTEL-LAB.md             ← Duke Beach como laboratório
    └── QLOAPPS-EXPLORATION.md   ← Notas técnicas do QloApps
```

---

## Como Rodar

### 1. QloApps (PMS)

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

## Fluxo Atual (Funcionando)

```
┌─────────────────────────────────────────────────────────────────┐
│  RESERVA NO MOTOR QLOAPPS                                       │
│  ─────────────────────────                                      │
│                                                                 │
│  1. Hóspede faz reserva no site                                │
│  2. QloApps cria a reserva                                      │
│  3. Módulo PHP dispara webhook com dados da reserva            │
│  4. Middleware recebe em /webhook/qloapps                       │
│  5. Middleware extrai: room_type, datas, cliente               │
│  6. Middleware mapeia para IDs do Channex                       │
│  7. [TODO] Middleware envia ARI para Channex                    │
│  8. [TODO] Channex atualiza OTAs                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Conceitos Chave

### Framework dos 5 Stakeholders

Para gerar impacto real, a solução deve atender simultaneamente:
1. Dono do hotel
2. Gerente
3. Funcionários
4. Hóspedes
5. Comunidade local

### Diferencial: Comunidade de Prática

Conectar pessoas que fazem trabalhos similares em hotéis diferentes, permitindo:
- Troca de conhecimento
- Reconhecimento entre pares
- Liderança emergente

---

## Próximos Passos

### Imediato (próxima sessão)
1. [ ] Implementar envio real de ARI para Channex
2. [ ] Expor middleware na internet (ngrok/cloudflare tunnel)
3. [ ] Configurar webhook do Channex para receber reservas de OTAs
4. [ ] Testar fluxo completo bidirecional

### Estratégico
- [ ] Análise de Oceano Azul dos PMS existentes
- [ ] Protótipo de interface "hóspede no centro"
- [ ] Validação com equipe do Duke Beach

---

## Credenciais (Staging)

| Serviço | Credencial |
|---------|------------|
| QloApps API Key | `Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9` |
| Channex API Key | `uTdTdIa1S+kXozFtM8wGtESiMtrzb7aRSZI50Io7rYEsS+EKApvdHjvvx+mqP09v` |
| Channex Property ID | `7c504651-9b33-48bc-9896-892c351f3736` |

---

## Referências

- `COSMO-VISION.md` - Visão completa do produto
- `integracao/CHANNEX-INTEGRATION.md` - Plano de integração
- `middleware/README.md` - Documentação do middleware
- `lab/QLOAPPS-EXPLORATION.md` - Notas técnicas QloApps
