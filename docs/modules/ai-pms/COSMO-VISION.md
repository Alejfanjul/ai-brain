# Cosmo - Visão do Produto

> Plataforma base para hotelaria com hóspede no centro.
>
> **Data:** 2026-01-24

---

## Manifesto

A hotelaria se industrializou, mas nunca se digitalizou de verdade. Sistemas atuais são versões digitais fragmentadas de processos analógicos.

**Nossa proposta:** Retornar à essência original da hospitalidade — tratamento individualizado em escala — usando IA como habilitador.

---

## Diferencial Central

### Hóspede no Centro, não Reservas

> "Nem todos os funcionários lidam com reservas, mas todos lidam com hóspedes."

**O problema:** Sistemas de PMS são construídos em torno de reservas. Funcionários que não trabalham na recepção (camareiras, manutenção, cozinha, concierge) ficam "de fora" do sistema.

**Nossa solução:** Sistema construído em torno do hóspede. Todos os funcionários podem contribuir e acessar contexto relevante.

### Exemplo concreto

| Cenário | PMS Tradicional | Cosmo |
|---------|-----------------|-------|
| Camareira limpa quarto 302 | Vê: "Quarto 302 - Limpar" | Vê: "Sr. João, habitué, prefere travesseiro extra, aniversário de casamento" |
| Recepção faz check-in | Processa reserva #12345 | Recebe João, sabe que ele pediu vista mar na última vez |
| Manutenção recebe chamado | OS #789 - Ar condicionado | Contexto: hóspede VIP, estadia longa, histórico de reclamações |

---

## Arquitetura de Produto

```
┌─────────────────────────────────────────────────────────────┐
│                         COSMO                               │
│            "O hóspede no centro de tudo"                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              CAMADA DE INTELIGÊNCIA                  │   │
│  │  - Contexto do hóspede (preferências, histórico)    │   │
│  │  - Padrões identificados por IA                     │   │
│  │  - Sugestões proativas                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│  ┌─────────────────────────┼─────────────────────────┐     │
│  │                         │                         │     │
│  ▼                         ▼                         ▼     │
│ ┌───────────┐        ┌───────────┐           ┌───────────┐ │
│ │    PMS    │        │  Channel  │           │  Outros   │ │
│ │ (QloApps) │        │  Manager  │           │  Módulos  │ │
│ │           │        │ (Channex) │           │           │ │
│ │ - Reservas│        │ - OTAs    │           │ - OS      │ │
│ │ - Quartos │        │ - Sync    │           │ - Pricing │ │
│ │ - Tarifas │        │ - Booking │           │ - etc     │ │
│ └───────────┘        └───────────┘           └───────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Componentes Base

### 1. PMS (QloApps)
- **Função:** Operações core - reservas, quartos, tarifas
- **Status:** Instalado, API funcionando
- **Gap:** Centrado em reserva, hóspede é cadastro básico

### 2. Channel Manager (Channex)
- **Função:** Distribuição - sincroniza com OTAs (Booking, Airbnb, Expedia)
- **Status:** Conta criada, integração pendente
- **Valor:** Commodity ($30-49/mês), não precisa reinventar

### 3. Camada de Inteligência (sistema-os evoluído)
- **Função:** Contexto do hóspede, IA, orquestração
- **Status:** Já existe parcialmente no sistema-os
- **Diferencial:** É aqui que mora o valor único

---

## Estratégia de Validação

### Duke Beach Hotel = Laboratório

O Duke Beach não é o cliente final. É o ambiente de teste.

**Ciclo:**
```
Resolver problema real → Entregar valor → Provar que funciona → Ganhar credibilidade
```

**Vantagem:** Acesso irrestrito a dados, processos e feedback real.

---

## Análise de Oceano Azul (a fazer)

### Framework

| Ação | Pergunta |
|------|----------|
| **Eliminar** | O que a indústria considera padrão mas não agrega valor? |
| **Reduzir** | O que pode ser reduzido bem abaixo do padrão? |
| **Aumentar** | O que deve ser elevado bem acima do padrão? |
| **Criar** | O que nunca foi oferecido e deve ser criado? |

### Hipóteses iniciais

**Criar (potencial oceano azul):**
- Sistema centrado em hóspede, não em reservas
- IA nativa desde o início (não retrofitted)
- Todos os funcionários como usuários, não só recepção
- Interface conversacional (não menus complexos)
- Comunidade de prática entre hotéis

**Eliminar/Reduzir:**
- Complexidade de módulos que ninguém usa
- Relatórios que ninguém lê
- Configurações infinitas

---

## Modelo de Dados Central

### Hóspede (entidade central)

```
hospede
├── Identificação
│   ├── nome_completo
│   ├── como_quer_ser_chamado  ← personalização
│   └── documentos
├── Contexto
│   ├── contexto_ia            ← insights da IA
│   ├── padroes_identificados  ← comportamentos detectados
│   └── logs_preferencias      ← histórico de preferências
├── Histórico
│   ├── primeira_visita
│   ├── ultima_visita
│   ├── total_reservas
│   └── total_gasto_historico
├── Perfil
│   ├── vip
│   ├── habitue
│   └── acessibilidade
└── Interações
    ├── reservas[]
    ├── ordens_servico[]
    └── feedbacks[]
```

### Reserva (uma das interações)

```
reserva
├── hospede_principal_id  ← referencia o hóspede
├── datas
├── apartamentos[]
└── contexto_reserva
```

---

## Próximos Passos

1. **Integração QloApps ↔ Channex** - Sincronizar disponibilidade e reservas
2. **Análise de Oceano Azul** - Mapear competidores e encontrar espaços
3. **Protótipo de interface** - Testar conceito "hóspede no centro"
4. **Validação no Duke Beach** - Usar com equipe real

---

## Referências

- `projects/ai-pms/visao/ai-pms-filosofia.md` - Filosofia original
- `projects/ai-pms/lab/HOTEL-LAB.md` - Framework de observação
- `projects/ai-pms/lab/QLOAPPS-EXPLORATION.md` - Notas técnicas QloApps
- `/home/alejandro/sistema-os/` - Sistema atual
