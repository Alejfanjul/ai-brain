# Sessão: HiHotel — Ontologia, Verbos e Identidade Profunda

**Data:** 2026-03-31
**Participantes:** Ale + Claude (modo conversa / brainstorm)
**Contexto:** Continuação das sessões de 17/03, 21/03 e 26/03. Ale retomou após entregar carta de demissão (30/03). Está pensando em go-to-market, mas na prática a conversa evoluiu pra algo mais profundo: a arquitetura conceitual da HiHotel e sua identidade como empresa.

---

## Ponto de partida

Ale disse que estava lendo "The Invincible Company" do Alex Osterwalder e vendo diferentes modelos de negócio. Queria conversar sobre go-to-market, mas avisou que estava "pensando em voz alta" e se contradizendo. Pediu para revisitar sessões anteriores antes de começar.

Após revisão das 3 sessões anteriores, a conversa se desenvolveu em três blocos: abordagem de mercado, ontologia como peça unificadora, e os verbos da HiHotel.

---

## Bloco 1: DNA e abordagem de mercado

### DNA da HiHotel
Ale definiu: "Somos uma empresa de tecnologia com DNA muito ligado à inteligência artificial." Não é apenas uma ferramenta — é como eles enxergam soluções, como constroem, e onde querem se posicionar como profissionais. IA é a direção que estão apontando.

### Hotelaria como setor
Ale reconhece que hotelaria não é adepta a novas tecnologias de forma geral. Isso é tanto desafio (vender é difícil) quanto oportunidade (quem entrar primeiro domina).

### Duas abordagens discutidas

**Abordagem 1 — Consultiva:** Marcar reuniões, apresentar a empresa, ouvir problemas do hotel, propor soluções. Vantagem: entende a dor real. Risco: escala na velocidade de reuniões, e hotéis tradicionais podem não converter.

**Abordagem 2 — Produto como porta de entrada (preferida pelo Ale):** Chegar com algo tangível e funcional. Exemplo: app de pedidos pro restaurante. "Melhor que o que você usa, mesmo preço, dois meses grátis, a gente ajuda na migração." Risco zero pro hotel. Uma vez dentro, abre canal com funcionários e expande pra outros módulos.

Ale escolheu a abordagem 2 porque:
- Cria algo tangível pra vender
- Pratica criação de produto
- Pratica conversar com pessoas pra desenvolver
- O processo de construção do app já é processo de construção da empresa

### O receio do Matheus
Quando Ale falou sobre o app de restaurante, Matheus ficou com receio de virarem "um apanhado de módulos que não conversam" — tipo empresa de software da década passada, com peças remendadas. Ale entende o receio, mas acredita que a arquitetura pode ser pensada como um todo, com partes que se conectam e desconectam sem parecer remendado.

---

## Bloco 2: A descoberta da ontologia

### O gatilho: Palantir
Ale pesquisou sobre a Palantir e viu um diagrama (compartilhou imagem) que mostra a Palantir Ontology como camada entre interfaces de usuário e bases de dados. A palavra "ontologia" chamou atenção e ele pesquisou mais.

A pesquisa de Ale sobre ontologia da Palantir:
- Ontologia mapeia dados para objetos do mundo real (plantas, produtos, transações)
- Cria elementos semânticos (objetos, propriedades, links) e cinéticos (ações, funções)
- Forma um "gêmeo digital" da organização
- Permite que LLMs e agentes raciocinem com contexto completo, não só dados brutos
- Une humanos e IA em fluxos de decisão

### A conexão com a HiHotel
Ale percebeu que a HiHotel tem a mesma estrutura:
- **Topo:** interfaces onde usuários interagem (Concierge TV, app funcionário, Claude Vault)
- **Meio:** a operação, onde as coisas acontecem
- **Base:** dados, bancos, sistemas, integrações

### O que é o Claude Vault
Matheus está desenvolvendo uma interface alimentada por IA. Exemplo: recepcionista loga no computador, tela se abre com todas as informações necessárias, microfone disponível pra falar com IA que é "responsável pela recepção" mas conectada a um agente orquestrador. Todo o sistema se comunica. (Nome provisório "Claude Vault" — Ale reconhece que o nome está datado.)

### Ontologia como peça unificadora
A ontologia resolve o receio do Matheus sobre módulos desconectados. Em vez de construir módulos independentes, construir uma **camada de significado unificada** — a ontologia hoteleira — sobre a qual qualquer interface é apenas uma "janela".

Estrutura proposta:
```
INTERFACES (faces)
  Concierge TV │ App Restaurante │ Claude Vault │ App Funcionário
─────────────────────────────────────────────────
ONTOLOGIA HOTELEIRA
  (modelo unificado: hóspedes, funcionários, quartos, pedidos, turnos, avaliações, treinamentos...)
  + Agentes de IA (orquestrador, recepção, etc.)
─────────────────────────────────────────────────
DADOS E INTEGRAÇÕES
  PMS (CMNET/Hits) │ PostgreSQL │ Redis │ APIs externas
```

O app de restaurante não é um módulo separado — é uma interface sobre a ontologia. Quando o hotel quer governança, não se constrói módulo novo — abre-se uma nova janela sobre o mesmo modelo. Rápido, escalável, coerente.

### Construir a ontologia a partir do que já existe
Ale quer submeter os repos SID e Concierge a uma "abstração ontológica" — olhar o que já foi construído e extrair: que entidades existem? Como se relacionam? Que ações acontecem entre elas? O modelo já está implícito no código — só precisa ser nomeado e tornado explícito.

Ale se identificou pessoalmente com o conceito: "Eu sempre fui a pessoa que entende o todo e explica para outros." Ontologia é uma externalização dessa habilidade natural dele.

---

## Bloco 3: Os verbos da HiHotel

### A premissa
"A HiHotel é feita para humanos. O que buscamos é atingir o ápice do potencial humano."

Ale enxerga cada pessoa dentro do hotel como alguém que pode brilhar na sua função — garçom, camareira, supervisor. O sistema é otimizado pra que todos possam aproveitar seu potencial ao máximo.

### Verbos definidos por Ale
- **APRENDER** — o funcionário aprende continuamente
- **ENSINAR** — o sistema ensina, funcionários ensinam uns aos outros
- **COORDENAR** — informação certa, pessoa certa, hora certa
- **ELEVAR** — levar cada pessoa ao seu potencial máximo

### Verbos expandidos na conversa (implícitos nas sessões anteriores)
- **RECONHECER** — tornar visível o trabalho bem feito (a camareira das 5 estrelas)
- **CONECTAR** — hóspede↔funcionário, gestor↔equipe, hotel↔hotel (Seth Godin, 3ª geração)
- **TRADUZIR** — gestor pede → SID traduz pra equipe. Hóspede tem preferência → SID traduz em ação
- **LEMBRAR** — o sistema lembra o que o hóspede gosta, o que o funcionário sabe, o que funcionou

### Observação importante
Nenhum dos verbos é verbo de software. Não tem "automatizar", "otimizar", "digitalizar". São verbos de gente — de educação e liderança. Coerente com a identidade: tecnologia invisível, humanos no centro.

### A síntese: HiHotel como líder digital
Os verbos juntos descrevem um líder. Um líder aprende, ensina, coordena, eleva, reconhece, conecta, traduz e lembra. A HiHotel é um líder digital — não substituindo liderança humana, mas fazendo o que nenhum gestor consegue sozinho: estar em todos os lugares ao mesmo tempo, lembrar de tudo, reconhecer cada pessoa.

Conecta com a frase da sessão 21/03: "eu quero ser gestor de milhares de funcionários sem ser gestor direto de nenhum." A HiHotel é como Ale escalaria a si mesmo.

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

## Referências desta sessão

- **Alex Osterwalder — The Invincible Company:** explore vs. exploit. HiHotel está 100% no modo explore, onde o mais importante é reduzir o ciclo de aprendizado.
- **Palantir Ontology:** camada semântica entre dados e interfaces. Gêmeo digital da organização. Modelo que permite IA e humanos raciocinarem juntos com contexto completo.
- **Claude Vault (Matheus):** interface de IA pra recepcionista, com agentes conectados (recepção + orquestrador). Nome provisório.

---

## Dinâmica com Matheus

- Ale já tocou no assunto ontologia com Matheus hoje. Mostrou o diagrama da Palantir e uma frase sobre o Claude Vault.
- Matheus respondeu sobre outro tópico — assunto ainda não foi aprofundado.
- Ale reconhece que precisa comunicar o conceito de forma acessível. Matheus é esperto e entende ideias abstratas, mas a palavra "ontologia" pode precisar de contextualização.
- Próximo passo: Ale vai ler o storytelling junto com Matheus pra ficarem na mesma página.

---

## Decisões e próximos passos

### Decidido
- Abordagem de mercado preferida: produto como porta de entrada (app tangível, risco zero pro hotel, expande depois)
- Ontologia hoteleira é a peça unificadora que resolve o receio de módulos desconectados
- Verbos da HiHotel: aprender, ensinar, coordenar, elevar, reconhecer, conectar, traduzir, lembrar
- HiHotel é feita pra humanos — busca atingir ápice do potencial humano

### Próxima atividade sugerida
- **Extrair ontologia dos repos SID e Concierge:** Claude lê os repositórios e entrega primeiro rascunho da ontologia hoteleira (objetos, relações, ações) como ponto de partida pra Ale e Matheus refinarem juntos.

### Storytelling criado
- Documento separado: `MEMORY/sessions/2026-03-31-hihotel-storytelling-matheus.md`
- Objetivo: Ale ler com Matheus pra ficarem alinhados sobre a evolução estratégica e a descoberta da ontologia

---

## Estado emocional

Ale entrou pensando em go-to-market ("estou confuso"), descobriu a ontologia como peça que faltava, definiu os verbos da empresa, e saiu com uma direção sólida. Pediu registro com "muita riqueza de detalhes" porque "essa conversa é muito preciosa" e quer reler. Sente que deu um passo numa direção sólida.
