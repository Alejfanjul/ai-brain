# Anexo Técnico — Projeto de Independência de TI

**Duke Beach Hotel & SPA**
**Elaborado por:** HiHotel Tecnologia LTDA
**Data:** Abril de 2026

---

## 1. Contexto

Atualmente, toda a operação de tecnologia do Duke Beach Hotel & SPA — desde suporte ao usuário até arquitetura de sistemas — é executada por um único profissional que também acumula funções de desenvolvimento de software e projetos estratégicos.

Essa concentração gera dois riscos para o hotel:
- **Dependência:** qualquer ausência impacta toda a operação de TI
- **Subutilização:** um profissional com competências em arquitetura de sistemas e desenvolvimento de software dedica parte significativa do tempo a atividades de suporte básico

Este projeto tem como objetivo tornar o Duke Beach Hotel & SPA **autossuficiente em suporte operacional de TI**, liberando a HiHotel para focar integralmente em projetos de maior valor estratégico para o hotel.

---

## 2. Diagnóstico Atual

### Infraestrutura sob gestão

| Área | Componentes |
|------|-------------|
| Rede | Firewall pfSense, switches e access points UniFi, VLANs segmentadas por departamento |
| Servidores | Hipervisor Proxmox (VMs e containers), Dokploy, file server, web server |
| CFTV | Câmeras IP, NVR/DVR, monitoramento em dois prédios |
| Telefonia | Sistema VoIP Sothis, ramais por departamento, integração Savant |
| Controle de acesso | Fechaduras Saga Bis Hotel, pulseiras/cartões, cadastro facial |
| Sistemas | 14 sistemas administrados (OcoMon, pfSense, Proxmox, Google Workspace, Zoho Mail, Bis Hotel, entre outros) |

### Departamentos atendidos

Operacional, financeiro, administrativo, manutenção, marketing, governança, RH, reservas, compras/estoque, restaurante/bar/salão.

### Localidades

- Prédio Lago — recepção, administrativo, CPD principal
- Prédio Praia — recepção, restaurante, salão
- Administrativo — financeiro, RH, marketing, reservas
- Estoque — compras, almoxarifado

---

## 3. Entregáveis

### Fase 1 — Documentação completa (meses 1-2)

**Objetivo:** consolidar e completar o registro do conhecimento operacional de TI, ampliando a documentação já iniciada.

| Entregável | Descrição |
|-----------|-----------|
| Manual de procedimentos de suporte | Guia passo a passo para os chamados mais frequentes (impressoras, rede, telefonia, acessos) |
| Mapa de infraestrutura | Diagrama atualizado de rede, servidores, câmeras, telefonia e controle de acesso |
| Inventário completo | Todos os equipamentos catalogados com localização, status e responsável |
| Registro de fornecedores | Contatos, contratos, SLAs e procedimentos de acionamento de cada parceiro |
| Documentação de acessos | Senhas, licenças, certificados e credenciais em registro seguro |
| Processos formalizados | Atualização dos PROs e TPLs existentes + criação dos que faltam |

### Fase 2 — Definição de perfil (mês 2-3)

**Objetivo:** definir exatamente que profissional o hotel precisa contratar.

| Entregável | Descrição |
|-----------|-----------|
| Descrição de cargo | Título, responsabilidades, escopo de atuação |
| Competências técnicas | O que o profissional precisa saber (rede, suporte, sistemas específicos do hotel) |
| Competências comportamentais | Perfil adequado ao ambiente hoteleiro |
| Faixa salarial sugerida | Pesquisa de mercado para o perfil definido |
| Rotina de trabalho | Descrição de um dia/semana típico do profissional |

### Fase 3 — Treinamento (após contratação pelo hotel)

**Objetivo:** capacitar o novo profissional para operar com autonomia.

| Entregável | Descrição |
|-----------|-----------|
| Programa de treinamento | Cronograma estruturado cobrindo todas as áreas |
| Treinamento prático | Período de acompanhamento direto com a equipe HiHotel |
| Avaliação de competência | Verificação de que o profissional está apto a operar de forma independente |
| Handoff de fornecedores | Apresentação formal aos parceiros (Saga, Sothis, entre outros) |

### Fase 4 — Transição supervisionada (1-2 meses após treinamento)

**Objetivo:** garantir que a transição seja segura e sem impacto na operação.

| Entregável | Descrição |
|-----------|-----------|
| Operação assistida | Novo profissional assume gradualmente, HiHotel supervisiona |
| Suporte de segundo nível | HiHotel disponível para questões que excedam o nível do novo profissional |
| Handoff formal | Documento de encerramento da transição, com aceite do hotel |

---

## 4. Cronograma estimado

```
Mês 1-2    ████████████  Fase 1 — Documentação
Mês 2-3    ████████████  Fase 2 — Perfil e contratação
Mês 4-5        ████████  Fase 3 — Treinamento (após contratação)
Mês 5-6          ██████  Fase 4 — Transição supervisionada
```

*O cronograma das fases 3 e 4 depende do tempo de contratação pelo hotel.*

---

## 5. Resultado esperado

Ao final deste projeto, o Duke Beach Hotel & SPA terá:

- **Profissional de TI próprio**, treinado e operando com autonomia
- **Documentação completa** de toda a infraestrutura e procedimentos
- **Processos formalizados** para suporte e manutenção
- **Independência operacional** — sem depender de terceiros para o dia-a-dia de TI

A HiHotel permanece como parceira estratégica de tecnologia, focada em evolução de sistemas, projetos de inovação e migração CMNET — atividades de alto valor que geram resultado para o hotel e para a parceria.

---

## 6. Observações

- Este projeto é parte integrante do contrato de prestação de serviços HiHotel → Duke Beach Hotel & SPA
- A contratação do profissional de TI é responsabilidade e decisão do hotel
- A HiHotel pode apoiar no processo seletivo, se solicitado
- Durante o período de transição, a manutenção de TI continua sob responsabilidade da HiHotel conforme contrato principal

---

*HiHotel Tecnologia LTDA*
