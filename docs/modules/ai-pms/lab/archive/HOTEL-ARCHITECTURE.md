# Plataforma AI-Native para Orquestração Hoteleira

> Visão macro e arquitetura completa do projeto HOTEL-LAB

---

## Quick Start: Explorando o QloApps PMS

### 3 Caminhos para Começar

#### Opção 1: Demo Online (mais rápido - zero setup)

```
URL: https://demo.qloapps.com
Login: demo@demo.com
Senha: demodemo
```

**Ideal para:** Ver a interface, entender fluxos, testar funcionalidades antes de instalar

#### Opção 2: Docker (recomendado para dev)

```bash
docker pull webkul/qloapps_docker
docker run -d -p 80:80 webkul/qloapps_docker
```

**Ideal para:** Ambiente isolado, fácil de resetar, não polui o sistema

#### Opção 3: Instalação Local (XAMPP/WAMP)

**Requisitos:**
- PHP 8.1+ (extensões: PDO_MySQL, cURL, OpenSSL, SOAP, GD, SimpleXML, DOM, Zip, Phar)
- MySQL 5.7+
- Apache/Nginx

Código clonado em: `/home/alejandro/QloApps`

### Roteiro de Exploração

| Passo | Ação | Objetivo |
|-------|------|----------|
| 1 | Acessar demo online | Conhecer interface sem setup |
| 2 | Criar hotel fictício | Entender estrutura de propriedade |
| 3 | Criar tipos de quarto | Entender room types + pricing |
| 4 | Fazer reserva manual | Entender booking flow |
| 5 | Explorar Back Office | Ver relatórios, KPIs, configurações |
| 6 | Habilitar API (Webservice) | Preparar para integração |
| 7 | Testar endpoints com curl | Validar API REST |

### API do QloApps (para o MCP)

Endpoints principais:
- **Bookings management** - CRUD de reservas
- **Availability & Rates** - Consulta/atualização de ARI
- **Date-wise breakdown** - Disponibilidade por data

Para habilitar a API:
1. Back Office → Advanced Parameters → Webservice
2. Criar chave de API com permissões granulares
3. Testar: `curl -u SUA_CHAVE: https://seu-qloapps.com/api/`

---

## Resumo Executivo

Pesquisa exploratória para identificar e arquitetar uma stack tecnológica open source + API-first para construir uma plataforma de orquestração AI-native para operações de hospitalidade.

**Decisões principais:**

- **PMS:** QloApps (open source, self-hosted)
- **Channel Manager:** Channex.io (API-first, $30-49/mês)
- **Interface AI:** MCP Servers (protocolo padrão Anthropic)
- **Abordagem:** Sem frameworks intermediários (CrewAI, LangGraph) - Claude direto + MCP

---

## 1. Contexto e Visão

### O Problema da Indústria

A hotelaria industrializou mas nunca digitalizou verdadeiramente. Sistemas atuais são versões digitais fragmentadas de processos analógicos, não soluções nativas digitais.

### A Oportunidade

Construir plataformas AI-native enquanto incumbentes lutam com sistemas legados. A explosão de agentes AI na hotelaria vai piorar a fragmentação - a menos que exista uma camada de orquestração unificada.

### Filosofia do Projeto

- **Primitive-native:** Sistemas que expõem fundamentos operacionais, não escondem
- **Living Infrastructure:** Documentação + PRDs + Skills + Agents como produto vendável
- **Agent-first:** Projetado para AI desde o início, não retrofitted
- **Sem frameworks:** Controle total, acesso direto às APIs dos modelos

---

## 2. Stack Tecnológica

### 2.1 PMS: QloApps

| Aspecto | Detalhe |
|---------|---------|
| Tipo | Open source (OSL-3.0) |
| GitHub | 11.4k stars, comunidade ativa |
| Stack | PHP/MySQL (baseado em PrestaShop) |
| Custo | Gratuito (self-hosted) |
| API | REST completa |

**Principais endpoints da API:**

| Endpoint | Função |
|----------|--------|
| `/api/hotel_ari` | Disponibilidade, tarifas, inventário (mais poderosa) |
| `/api/bookings` | Ciclo completo de reservas |
| `/api/customers` | Gestão de hóspedes |
| `/api/room_types` | Tipos de quarto |
| `/api/hotels` | Propriedades |

**Características da API:**

- Formato: XML por padrão, JSON via `output_format=JSON`
- Autenticação: Webservice keys com permissões granulares
- Schema discovery: `?schema=blank` (template), `?schema=synopsis` (requisitos)
- Filtros avançados: EQUAL, LIKE, GREATER THAN, LOWER THAN, OR, NOT EQUAL

**Alternativas analisadas:**

- miniCal - Mais modular, menor comunidade
- HotelDruid - Simples, bom para pequenas propriedades
- Apaleo - Comercial, API-first, referência arquitetural

### 2.2 Channel Manager: Channex.io

| Aspecto | Detalhe |
|---------|---------|
| Tipo | SaaS com API completa |
| Custo | $30-49/mês por propriedade |
| OTAs | 50+ (Booking.com, Airbnb, Expedia, Agoda, Google Hotels...) |
| Staging | Gratuito para desenvolvimento/testes |
| MCP Server | Já existe (open source, MIT) |

**Por que Channex e não QloApps Channel Manager?**

| Aspecto | QloApps CM | Channex |
|---------|------------|---------|
| Integração com QloApps PMS | Nativa | Via API |
| API para desenvolvedores | Limitada | Completa |
| MCP Server | Não existe | Já existe |
| Webhooks | Não | Completo |
| Documentação | Básica | Extensa |

**Decisão:** Channex oferece mais controle programático, essencial para construir camada de orquestração AI.

**Recursos do Channex:**

- API REST completa (Properties, Room Types, Rate Plans, ARI, Bookings)
- Webhooks para eventos (reservas, mudanças de ARI, mensagens)
- Contas de teste para Booking.com e Airbnb
- White-label disponível
- Staging gratuito: https://staging.channex.io

### 2.3 Realidade sobre Channel Managers Open Source

**Não existe channel manager verdadeiramente open source funcional.**

Razões estruturais:

1. **Certificação obrigatória:** OTAs só concedem API a parceiros certificados
2. **Manutenção contínua:** APIs das OTAs mudam constantemente
3. **Modelo de negócio das OTAs:** Preferem poucos intermediários grandes

**Conclusão:** Channel management é um dos poucos componentes onde SaaS faz sentido. $30/mês é custo aceitável pelo valor entregue.

### 2.4 Interface AI: MCP (Model Context Protocol)

**O que é MCP?**

Protocolo padrão (criado pela Anthropic) que permite LLMs chamarem funções externas de forma padronizada. É um "tradutor universal" entre AI e sistemas externos.

**Componentes:**

| MCP Server | Status | Função |
|------------|--------|--------|
| QloApps MCP | A construir | Interface AI para o PMS |
| Channex MCP | Já existe | Interface AI para Channel Manager |

Repositório channex-mcp: https://github.com/webrenew/channex-mcp

**Características do channex-mcp:**

- Licença MIT (open source)
- CRUD completo: Properties, Room Types, Rate Plans
- Gestão de ARI (Availability, Rates, Inventory)
- Conexão com canais OTA
- Pronto para uso com Claude Code/Desktop

---

## 3. Arquitetura Completa

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLAUDE                                  │
│              (comandos em linguagem natural)                    │
│                                                                 │
│  "Reserve um quarto para João dia 15/01"                        │
│  "Aumenta a tarifa em 20% para o Carnaval"                      │
│  "Qual a ocupação da próxima semana?"                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ MCP Protocol
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
   ┌───────────────┐               ┌───────────────┐
   │ QloApps MCP   │               │ Channex MCP   │
   │ (a construir) │               │ (já existe)   │
   │ ~200 linhas   │               │ MIT license   │
   │ Python        │               │ TypeScript    │
   └───────┬───────┘               └───────┬───────┘
           │ REST API                      │ REST API
           ▼                               ▼
   ┌───────────────┐               ┌───────────────┐
   │               │◄─────────────►│               │
   │  QloApps PMS  │   API REST    │  Channex.io   │
   │  (self-hosted)│   Webhooks    │  (staging:    │
   │               │   (24/7 sync) │   gratuito)   │
   └───────────────┘               └───────┬───────┘
                                           │ APIs certificadas
                                           ▼
                                   ┌───────────────┐
                                   │     OTAs      │
                                   │ • Booking.com │
                                   │ • Airbnb      │
                                   │ • Expedia     │
                                   │ • Agoda       │
                                   │ • Google      │
                                   │ • 50+ outros  │
                                   └───────────────┘
```

---

## 4. Duas Camadas Distintas

### Camada Operacional (funciona sem AI)

```
QloApps PMS ◄──────────► Channex.io ◄──────────► OTAs
              API REST                APIs certificadas
              Webhooks
```

**Fluxo exemplo:**

1. Hóspede reserva pelo Airbnb
2. Channex recebe a reserva
3. Channex envia para QloApps via API
4. QloApps registra no calendário
5. Channex atualiza disponibilidade no Booking.com

Automático, 24/7, sem intervenção humana, sem AI.

### Camada de Inteligência (diferencial)

```
Você/Agente ──► Claude ──► MCP Servers ──► Sistemas
```

**Fluxo exemplo:**

1. Você: "Aumenta a tarifa do Standard em 20% para o Carnaval"
2. Claude chama `qloapps_mcp.update_rates`
3. Claude chama `channex_mcp.sync_rates`
4. Tarifas atualizadas em todos os canais

Comandos em linguagem natural, AI executa.

---

## 5. Referência Arquitetural: Apaleo

Apaleo representa o estado da arte em PMS API-first e serve como referência:

| Característica | Apaleo | Nossa Stack |
|----------------|--------|-------------|
| MCP Server | Nativo (set/2025) | Channex (existe) + QloApps (construir) |
| Endpoints | 237 como MCP tools | ~30-50 tools combinados |
| Formato | JSON nativo | JSON |
| Webhooks | Sim | Sim (via Channex) |
| Open Source | Não | Parcialmente (QloApps) |
| Custo | Alto | Baixo (~$30/mês) |

**Insight do Apaleo:** O futuro é agent-native - sistemas onde AI agents colaboram e até negociam entre si (A2A - Agent to Agent).

---

## 6. Plano de Implementação

### Fase 1: Fundação (1-2 semanas)

**Objetivo:** Conhecer o PMS por dentro

- [ ] Instalar QloApps localmente ou em servidor de teste
- [ ] Explorar interface administrativa
- [ ] Criar tipos de quarto, tarifas
- [ ] Fazer reservas manuais
- [ ] Testar API REST (Postman/curl)
- [ ] Documentar endpoints úteis

**Resultado:** Entendimento prático do PMS

### Fase 2: Channel Manager (1-2 semanas)

**Objetivo:** Camada operacional funcionando

- [ ] Criar conta no Channex Staging (gratuito): https://staging.channex.io
- [ ] Explorar interface do Channex
- [ ] Gerar API key
- [ ] Conectar QloApps ↔ Channex via API
- [ ] Testar sincronização bidirecional
- [ ] Testar webhooks
- [ ] Usar contas de teste Booking.com/Airbnb

**Resultado:** Sincronização automática funcionando

### Fase 3: Explorar MCP (1 semana)

**Objetivo:** Entender MCP na prática

- [ ] Instalar channex-mcp
- [ ] Configurar no Claude Code/Desktop
- [ ] Testar comandos: "liste propriedades", "qual disponibilidade"
- [ ] Entender estrutura de um MCP Server
- [ ] Documentar aprendizados

**Resultado:** Experiência prática com MCP

### Fase 4: Construir QloApps MCP (2-3 semanas)

**Objetivo:** Interface AI completa

- [ ] Definir tools necessárias (começar com 3-5)
- [ ] Construir MCP Server em Python (com ajuda do Claude Code)
- [ ] Tools iniciais sugeridas:
  - `check_availability`
  - `list_bookings`
  - `create_booking`
  - `get_booking`
  - `update_rates`
- [ ] Testar integrado com channex-mcp
- [ ] Expandir conforme necessidade

**Resultado:** Camada de inteligência completa

---

## 7. Custos Estimados

| Item | Custo Mensal | Notas |
|------|--------------|-------|
| QloApps PMS | $0 | Self-hosted |
| Servidor (VPS) | $5-20 | DigitalOcean, Hetzner |
| Channex Staging | $0 | Para desenvolvimento |
| Channex Produção | $30-49 | Por propriedade |
| **Total Desenvolvimento** | **$5-20** | |
| **Total Produção** | **$35-70** | Por propriedade |

---

## 8. Diferenciais Competitivos

1. **AI-native desde o início:** Não é retrofit de sistema legado
2. **Controle total:** Open source + APIs, sem vendor lock-in no PMS
3. **Custo baixo:** ~$50/mês vs milhares em soluções enterprise
4. **Extensível:** Adicionar novos MCP Servers conforme necessidade
5. **Vendável:** Cada componente é produto potencial
   - QloApps MCP Server como produto open source
   - Consultoria de implementação
   - "Living Infrastructure" como serviço

---

## 9. Riscos e Mitigações

| Risco | Probabilidade | Mitigação |
|-------|---------------|-----------|
| QloApps descontinuado | Baixa | Código open source, pode ser mantido |
| Channex aumenta preços | Média | Arquitetura permite trocar CM |
| Complexidade técnica | Média | Começar simples, expandir gradualmente |
| OTAs mudam APIs | Alta | Channex absorve essa complexidade |

---

## 10. Próximos Passos Imediatos

1. **Hoje:** Criar conta no Channex Staging
2. **Esta semana:** Instalar QloApps localmente
3. **Próxima semana:** Conectar os dois sistemas
4. **Em 2 semanas:** Testar channex-mcp com Claude

---

## 11. Links e Recursos

### QloApps

- Site: https://qloapps.com
- GitHub: https://github.com/Qloapps/QloApps (11.4k stars)
- Documentação API: https://devdocs.qloapps.com/webservice/
- Download: https://qloapps.com/download/

### Channex

- Site: https://channex.io
- Staging (gratuito): https://staging.channex.io
- Documentação API: https://docs.channex.io
- Guia de integração PMS: https://docs.channex.io/guides/pms-integration-guide
- Teste Booking.com: https://docs.channex.io/guides/test-account-for-booking.com
- Teste Airbnb: https://docs.channex.io/guides/test-accounts-for-airbnb

### MCP

- Channex MCP Server: https://github.com/webrenew/channex-mcp
- MCP Protocol (Anthropic): https://github.com/modelcontextprotocol
- Lista de MCP Servers: https://github.com/punkpeye/awesome-mcp-servers

### Referência

- Apaleo (referência arquitetural): https://apaleo.com
- Apaleo MCP Server: https://store.apaleo.com

---

## 12. Exemplo de MCP Server (QloApps)

Estrutura básica de como seria o QloApps MCP Server:

```python
from mcp.server import Server
from mcp.types import Tool
import httpx

server = Server("qloapps-mcp")

# Configuração da API QloApps
QLOAPPS_URL = "https://seu-hotel.com/api"
QLOAPPS_KEY = "sua-chave-api"

@server.tool()
async def check_availability(
    date_from: str,
    date_to: str,
    adults: int = 2
) -> dict:
    """Verifica disponibilidade de quartos no hotel"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{QLOAPPS_URL}/hotel_ari",
            auth=(QLOAPPS_KEY, ""),
            json={
                "date_from": date_from,
                "date_to": date_to,
                "get_available_rooms": 1,
                "room_occupancies": [{"adults": adults}]
            }
        )
        return response.json()

@server.tool()
async def create_booking(
    customer_name: str,
    email: str,
    room_type_id: int,
    checkin: str,
    checkout: str
) -> dict:
    """Cria uma nova reserva"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{QLOAPPS_URL}/bookings",
            auth=(QLOAPPS_KEY, ""),
            json={
                "firstname": customer_name.split()[0],
                "lastname": customer_name.split()[-1],
                "email": email,
                "room_types": [{
                    "id_room_type": room_type_id,
                    "checkin_date": checkin,
                    "checkout_date": checkout
                }]
            }
        )
        return response.json()

# Adicionar mais tools conforme necessidade:
# - list_bookings
# - cancel_booking
# - update_rates
# - get_customer
# - etc.
```

---

## 13. Configuração MCP para Claude Code/Desktop

```json
{
  "mcpServers": {
    "qloapps": {
      "command": "python",
      "args": ["/caminho/para/qloapps_mcp.py"],
      "env": {
        "QLOAPPS_URL": "https://seu-hotel.com/api",
        "QLOAPPS_KEY": "sua-chave"
      }
    },
    "channex": {
      "command": "npx",
      "args": ["--prefix", "/caminho/para/channex-mcp", "channex-mcp"],
      "env": {
        "CHANNEX_API_KEY": "sua-chave-channex",
        "CHANNEX_BASE_URL": "https://staging.channex.io/api/v1/"
      }
    }
  }
}
```

---

*Documento gerado em janeiro/2026*
*Baseado em pesquisa colaborativa Claude + Alejandro*
