# Cosmo - Plataforma de Hotelaria

> "Nem todos os funcionários lidam com reservas, mas todos lidam com hóspedes."

---

## Visão

**Cosmo** é uma plataforma base para hotelaria com o **hóspede no centro** — não reservas.

A hotelaria se industrializou, mas nunca se digitalizou de verdade. Sistemas atuais são versões digitais fragmentadas de processos analógicos, centrados em reservas, usados apenas pela recepção.

**Nossa proposta:** Sistema onde todos os funcionários contribuem, porque todos impactam o hóspede de alguma maneira.

---

## Status

**Fase:** Construção da base técnica

- [x] Filosofia e propósito definidos
- [x] Stack open source pesquisado (QloApps + Channex)
- [x] QloApps instalado e API funcionando
- [x] Conta Channex criada
- [ ] Integração QloApps ↔ Channex
- [ ] Análise de Oceano Azul
- [ ] Primeiro MVP/protótipo

---

## Estrutura do Projeto

```
ai-pms/
├── README.md                    ← Este arquivo
├── COSMO-VISION.md              ← Visão completa do produto
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

## Conexão com PAI

Este projeto é a **aplicação prática** do que está sendo aprendido em `projects/pai-study/`:
- TELOS do hotel (contexto profundo)
- Skills específicos de hotelaria
- Hooks para automação

---

## Próximos Passos

### Imediato
- [ ] Gerar API Key no Channex staging
- [ ] Testar API do Channex
- [ ] Construir middleware de integração

### Estratégico
- [ ] Análise de Oceano Azul dos PMS existentes
- [ ] Protótipo de interface "hóspede no centro"
- [ ] Validação com equipe do Duke Beach

---

## Ambiente de Desenvolvimento

### QloApps (PMS)
- **Local:** `~/QloApps`
- **Servidor:** `cd ~/QloApps && php -S localhost:8080`
- **Admin:** http://localhost:8080/admin/
- **API Key:** `Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9`

### Channex (Channel Manager)
- **Staging:** https://staging.channex.io/
- **Docs:** https://docs.channex.io/

### Sistema existente
- **Local:** `~/sistema-os`
- **Banco:** Supabase (PostgreSQL)
- **Schema:** `~/sistema-os/docs/schemas/supabase_full_schema_20260116.sql`

---

## Referências

- `COSMO-VISION.md` - Visão completa do produto
- `integracao/CHANNEX-INTEGRATION.md` - Plano de integração
- `lab/QLOAPPS-EXPLORATION.md` - Notas técnicas QloApps
- `~/sistema-os/` - Sistema atual (base para camada de IA)
