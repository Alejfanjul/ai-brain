# QloApps Exploration - Lab Notes

> Documentação da exploração do QloApps como base PMS para o projeto Cosmo.
>
> **Data:** 2026-01-24

---

## Visão do Projeto

### O que estamos construindo

**"Cosmo da Hotelaria"** - Uma plataforma base robusta que contém todos os jobs/tarefas que um hotel precisa realizar.

```
┌─────────────────────────────────────────────────────────────┐
│                    "COSMO" DA HOTELARIA                     │
│         Plataforma base com TODOS os jobs/tarefas           │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐          ┌──────────┐         ┌──────────┐
   │   PMS   │          │ Channel  │         │  Outros  │
   │(QloApps)│          │ Manager  │         │ Módulos  │
   └─────────┘          └──────────┘         └──────────┘
```

### Diferencial: Hóspede no Centro

> "Nem todos os funcionários lidam com reservas, mas todos lidam com hóspedes."

| Aspecto | PMS Tradicional | Nosso sistema |
|---------|-----------------|---------------|
| **Centro** | Reserva | Hóspede |
| **Pergunta base** | "Qual o status da reserva?" | "Quem é esse hóspede?" |
| **Funcionários** | Só recepção usa o sistema | Todos contribuem |
| **Dados** | Fragmentados por módulo | Unificados em torno da pessoa |
| **Valor** | Controle operacional | Experiência do hóspede |

**Exemplo prático:**
- **Hoje:** Camareira limpa quarto 302. Ela não sabe nada sobre quem está lá.
- **Com nosso sistema:** Camareira vê que o hóspede do 302 é Sr. João, habitué, prefere travesseiro extra, está comemorando aniversário de casamento. Ela pode agir.

---

## QloApps - Estado Atual

### Instalação

- **Local:** `~/QloApps`
- **Servidor:** PHP 8.1.2 built-in server
- **Banco:** MySQL 8.0.44, database `qloapps`, user `qloapps`
- **Acesso:** http://localhost:8080
- **Admin:** http://localhost:8080/admin/

### Iniciar o servidor

```bash
cd ~/QloApps && php -S localhost:8080
```

### API Webservice

- **Endpoint:** `http://localhost:8080/webservice/dispatcher.php`
- **Autenticação:** HTTP Basic com API Key
- **Formato:** XML (padrão)
- **Key:** `Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9`

**Teste:**
```bash
curl -s -u "Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9:" \
  "http://localhost:8080/webservice/dispatcher.php?url=bookings"
```

---

## API do QloApps - Endpoints Relevantes

### Hotelaria (específicos)

| Endpoint | Métodos | Descrição |
|----------|---------|-----------|
| `/hotels` | CRUD | Propriedades/hotéis |
| `/hotel_rooms` | CRUD | Quartos individuais |
| `/hotel_room_types` | CRUD | Tipos de quarto |
| `/room_types` | CRUD | Categorias de quarto |
| `/bookings` | GET/POST/PUT | Reservas completas |
| `/room_bookings` | CRUD | Reservas por quarto |
| `/hotel_ari` | CRUD | Disponibilidade, Tarifas, Inventário |
| `/feature_prices` | CRUD | Preços dinâmicos/sazonais |
| `/services` | CRUD | Serviços extras |
| `/advance_payments` | CRUD | Pagamentos antecipados |
| `/hotel_features` | CRUD | Amenidades do hotel |
| `/hotel_refund_rules` | CRUD | Políticas de cancelamento |

### Clientes/Hóspedes

| Endpoint | Métodos | Descrição |
|----------|---------|-----------|
| `/customers` | CRUD | Cadastro de clientes |
| `/guests` | CRUD | Hóspedes (checkout rápido) |
| `/addresses` | CRUD | Endereços |
| `/customer_messages` | CRUD | Mensagens |
| `/customer_threads` | CRUD | Conversas |

### Pedidos/Financeiro

| Endpoint | Métodos | Descrição |
|----------|---------|-----------|
| `/orders` | CRUD | Pedidos |
| `/order_details` | CRUD | Itens do pedido |
| `/order_payments` | CRUD | Pagamentos |
| `/order_histories` | CRUD | Histórico de status |
| `/cart_rules` | CRUD | Cupons/descontos |

### Estrutura de uma Reserva (exemplo)

```xml
<booking>
  <id>1</id>
  <id_property>1</id_property>
  <currency>BRL</currency>
  <booking_date>2026-01-24 14:36:59</booking_date>
  <associations>
    <customer_detail>
      <firstname>Alejandro</firstname>
      <lastname>Fanjul</lastname>
      <email>alejandro.fjl@gmail.com</email>
      <phone>11952994179</phone>
    </customer_detail>
    <price_details>
      <total_price_without_tax>1500</total_price_without_tax>
      <total_tax>375</total_tax>
    </price_details>
    <room_types>
      <room_type>
        <checkin_date>2026-01-24</checkin_date>
        <checkout_date>2026-01-25</checkout_date>
        <rooms>
          <room>
            <id_room>1</id_room>
            <adults>2</adults>
            <child>0</child>
            <services>...</services>
          </room>
        </rooms>
      </room_type>
    </room_types>
  </associations>
</booking>
```

---

## Banco de Dados QloApps

### Tabelas principais de hotelaria (prefixo `qlo_htl_`)

| Tabela | Descrição |
|--------|-----------|
| `qlo_htl_branch_info` | Informações do hotel |
| `qlo_htl_room_type` | Tipos de quarto |
| `qlo_htl_room_information` | Quartos individuais |
| `qlo_htl_booking_detail` | Detalhes das reservas (37 campos) |
| `qlo_htl_cart_booking_data` | Dados do carrinho |
| `qlo_htl_room_type_feature_pricing` | Preços dinâmicos |

### Acesso ao banco

```bash
mysql -u qloapps -pqloapps123 qloapps
```

---

## Observações da Exploração

### Frontend
- Design datado (tecnologia ~2015, herdada do PrestaShop)
- Stack: Smarty templates + SASS/CSS + JavaScript + Bootstrap antigo
- **Precisará ser refeito completamente** para o produto final

### Modelo de dados
- **Centrado em reserva**, não em hóspede
- Cliente é apenas um cadastro básico (sem contexto, preferências, histórico rico)
- Isso é exatamente o **gap** que nosso sistema preenche

### API
- Funcional e completa para operações básicas
- Formato XML (pode ser convertido para JSON)
- Endpoints específicos de hotelaria são robustos
- Base suficiente para integração com Channel Manager

---

## Comparativo: QloApps vs sistema-os

| Aspecto | QloApps | sistema-os (seu) |
|---------|---------|------------------|
| **Tabelas** | 301 | 35 |
| **Foco** | PMS completo | Operações + IA |
| **Hóspede** | Cadastro básico | 40 campos + contexto_ia |
| **IA** | Nenhum campo | contexto_ia, padroes_identificados |
| **Pricing** | Básico | Scraping de concorrentes |
| **Integração** | Standalone | Sync com HITS |

---

## Próximos Passos

### Imediato: Integração com Channex
- [x] Conta criada no Channex
- [ ] Explorar API do Channex (staging)
- [ ] Mapear fluxos de sincronização
- [ ] Construir middleware QloApps ↔ Channex

### Estratégico: Análise de Oceano Azul
- [ ] Listar principais PMS do mercado
- [ ] Identificar fatores competitivos atuais
- [ ] Mapear onde cada um compete
- [ ] Encontrar espaços vazios (oceano azul)

---

## Referências

- QloApps Docs: https://docs.qloapps.com/
- QloApps DevDocs: https://devdocs.qloapps.com/
- Channex Docs: https://docs.channex.io/
- Channex PMS Guide: https://docs.channex.io/guides/pms-integration-guide
