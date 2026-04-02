# HiHotel — Ontologia, Verbos e Arquitetura

**Data:** 2026-03-31
**Objetivo:** Documentar a arquitetura conceitual da HiHotel — ontologia hoteleira como peça unificadora e os verbos que definem a identidade da empresa.

---

## DNA da HiHotel

Empresa de tecnologia com DNA ligado à inteligência artificial. IA não é apenas ferramenta — é como enxergamos soluções e onde queremos nos posicionar.

Hotelaria não é adepta a novas tecnologias de forma geral. Isso é tanto desafio (vender é difícil) quanto oportunidade (quem entrar primeiro domina).

---

## A descoberta da ontologia

### O gatilho: Palantir

A Palantir não construiu "módulos". Construiu uma representação unificada do mundo real — objetos, relações entre eles, e ações possíveis. Qualquer app que roda em cima da Palantir fala com o mesmo modelo da realidade.

Ontologia da Palantir:
- Mapeia dados para objetos do mundo real
- Cria elementos semânticos (objetos, propriedades, links) e cinéticos (ações, funções)
- Forma um "gêmeo digital" da organização
- Permite que LLMs e agentes raciocinem com contexto completo
- Une humanos e IA em fluxos de decisão

### Conexão com a HiHotel

A HiHotel tem a mesma estrutura:
- **Topo:** interfaces onde usuários interagem (Concierge TV, app funcionário, Claude Vault)
- **Meio:** a operação, onde as coisas acontecem
- **Base:** dados, bancos, sistemas, integrações

### Ontologia como peça unificadora

Em vez de construir módulos independentes, construir uma **camada de significado unificada** — a ontologia hoteleira — sobre a qual qualquer interface é apenas uma "janela".

```
INTERFACES (faces)
  Concierge TV | App Restaurante | Claude Vault | App Funcionário
─────────────────────────────────────────────────
ONTOLOGIA HOTELEIRA
  (modelo unificado: hóspedes, funcionários, quartos, pedidos, turnos, avaliações, treinamentos...)
  + Agentes de IA (orquestrador, recepção, etc.)
─────────────────────────────────────────────────
DADOS E INTEGRAÇÕES
  PMS (CMNET/Hits) | PostgreSQL | Redis | APIs externas
```

O app de restaurante não é um módulo separado — é uma interface sobre a ontologia. Quando o hotel quer governança, não se constrói módulo novo — abre-se uma nova janela sobre o mesmo modelo. Rápido, escalável, coerente.

### Claude Vault

Interface alimentada por IA que Matheus está desenvolvendo. Exemplo: recepcionista loga no computador, tela se abre com todas as informações necessárias, microfone disponível pra falar com IA que é "responsável pela recepção" mas conectada a um agente orquestrador. Todo o sistema se comunica.

---

## Os verbos da HiHotel

### Premissa
"A HiHotel é feita para humanos. O que buscamos é atingir o ápice do potencial humano."

Cada pessoa dentro do hotel pode brilhar na sua função — garçom, camareira, supervisor. O sistema é otimizado pra que todos possam aproveitar seu potencial ao máximo.

### Os 8 verbos

- **APRENDER** — o funcionário aprende continuamente
- **ENSINAR** — o sistema ensina, funcionários ensinam uns aos outros
- **COORDENAR** — informação certa, pessoa certa, hora certa
- **ELEVAR** — levar cada pessoa ao seu potencial máximo
- **RECONHECER** — tornar visível o trabalho bem feito (a camareira das 5 estrelas)
- **CONECTAR** — hóspede↔funcionário, gestor↔equipe, hotel↔hotel
- **TRADUZIR** — gestor pede → SID traduz pra equipe. Hóspede tem preferência → SID traduz em ação
- **LEMBRAR** — o sistema lembra o que o hóspede gosta, o que o funcionário sabe, o que funcionou

Nenhum dos verbos é verbo de software. São verbos de gente — de educação e liderança. Tecnologia invisível, humanos no centro.

### Síntese: HiHotel como líder digital

Os verbos juntos descrevem um líder. A HiHotel é um líder digital — não substituindo liderança humana, mas fazendo o que nenhum gestor consegue sozinho: estar em todos os lugares ao mesmo tempo, lembrar de tudo, reconhecer cada pessoa.

### Estrutura completa com verbos

```
         PESSOAS (hóspedes, funcionários, gestores)
              ↕
     VERBOS DA HIHOTEL
     aprender · ensinar · coordenar · elevar
     reconhecer · conectar · traduzir · lembrar
              ↕
         INTERFACES
     Concierge · App Funcionário · Claude Vault · Dashboard Gestor
              ↕
      ONTOLOGIA HOTELEIRA
     (modelo unificado — objetos, relações, ações)
              ↕
      DADOS E INTEGRAÇÕES
     PMS · Bancos · APIs · Modelos de IA
```

Os verbos ficam entre as pessoas e as interfaces — definem COMO cada interface se comporta. O app do restaurante não é só formulário de pedidos — ele coordena (encaminha pra cozinha), reconhece (dá pontos ao garçom), lembra (preferências do hóspede), ensina (sugere upsell).

---

## Próximo passo técnico

Extrair a ontologia do que já existe. O SID e o Concierge já foram construídos. O modelo está implícito no código — entidades, relações, ações. Ler os repositórios e gerar um primeiro rascunho da ontologia hoteleira como ponto de partida pra refinamento conjunto.

---

## Referências

- **Palantir Ontology** — camada semântica entre dados e interfaces. Gêmeo digital da organização.
- **Alex Osterwalder — The Invincible Company** — explore vs. exploit. HiHotel está no modo explore.
- **Seth Godin (3a geração de IA)** — criar valor conectando pessoas.
- **Nate (Jevons Paradox)** — quando custo de execução cai 10x, o valor migra do artefato pro insight.
