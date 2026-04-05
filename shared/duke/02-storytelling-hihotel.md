# HiHotel — A história até aqui

**Data:** 2026-03-31
**Objetivo:** Alinhar a evolução estratégica da HiHotel e a descoberta que muda como pensamos o produto.

---

## Como começou

A gente tinha dois produtos: o SID (sistema interno do hotel, orquestração) e o Concierge (face pro hóspede, TV, app). Duas coisas separadas. O SID era do Duke porque foi construído lá dentro. O Concierge era nosso — IP da HiHotel.

A primeira grande conversa estratégica (17 de março) girou em torno de um dilema: como transformar isso num negócio? Código hoje é barato de produzir com IA — então propriedade intelectual sobre código não vale tanto quanto parece. O valor real está em saber **o que** construir, não em ter construído.

A decisão foi: o SID do Duke fica com o Duke. A gente leva o conhecimento. O Concierge é nosso. E a HiHotel vende resultado, não tecnologia — porque hotéis não compram tecnologia, compram operação melhor.

---

## A virada: o funcionário trabalha pra gente

Na conversa de 21 de março, algo mudou. Inspiração no Pokémon GO: a Niantic usou o jogo pra capturar dados 3D de cidades inteiras, sem ninguém perceber. O jogo era o cavalo de Tróia. Os dados eram o produto real.

A pergunta foi: **e se o SID fosse o Pokémon GO dos hotéis?**

A IA pode estar em muitos lugares, mas não pode estar fisicamente dentro de um hotel. Funcionários — garçons, camareiras, recepcionistas — têm o domínio da interação real com o hóspede. E ninguém hoje "é dono" da comunicação com o funcionário de hotel. Nenhuma big tech vai buscar pequenos hotéis. Esse espaço está aberto.

Aí veio a frase que define tudo:

> **"O funcionário trabalha para o meu sistema e indiretamente atinge os resultados do hotel."**

A ideia: o SID não é um ERP. É uma plataforma onde o funcionário **aprende**, é **avaliado**, é **reconhecido** e se **desenvolve**. Gamificação, quizzes de onboarding, pontos por bom atendimento, benefícios dados pela HiHotel — não pelo hotel. O funcionário é leal à plataforma. Muda de hotel, continua no SID. Um LinkedIn da hotelaria operacional.

Do lado do hóspede, o Concierge faz o mesmo: um perfil portável de preferências que viaja entre hotéis. O João Almeida é alérgico a glúten e gosta de pacotes românticos? Todo hotel com Concierge já sabe disso.

E quando SID e Concierge se conectam, surge um ciclo:

1. Hóspede compartilha preferências (Concierge)
2. SID traduz em ação pro funcionário
3. Funcionário executa sem perguntar nada
4. Hóspede avalia positivamente (Concierge)
5. Funcionário ganha pontos (SID)
6. Hotel vê resultado
7. Ciclo se fortalece

O exemplo do Matheus encapsulou perfeitamente: "o hóspede avalia a limpeza com 5 estrelas e a camareira ganha 5 estrelas no nosso app." Ninguém faz trabalho extra. O hóspede já avalia, a camareira já limpa. O que muda é que agora isso alimenta um sistema que gera valor pros dois lados.

A identidade que emergiu: **a HiHotel não é uma empresa de software. É a camada de inteligência da hotelaria.**

---

## A decisão de sair

O Duke não havia respondido em mais de duas semanas com informações básicas pra proposta. Convergência independente — os dois chegando no mesmo ponto por caminhos diferentes.

Cartas entregues em 30 de março.

O Duke não é cliente — é laboratório. E o laboratório cumpriu sua função: deu o conhecimento de domínio que é o verdadeiro ativo.

---

## Hoje: como ir pro mercado?

Com a saída do Duke definida, a pergunta mudou: como a HiHotel chega no primeiro hotel de verdade?

Duas abordagens foram discutidas:

1. **Consultiva** — reuniões, diagnóstico, proposta sob medida. Escala devagar.
2. **Produto como porta de entrada** — chegar com algo tangível. "Aqui, um app de pedidos pro restaurante. Melhor que o que você usa. Dois meses grátis." Risco zero pro hotel. Uma vez dentro, expande.

A abordagem preferida é a segunda. Porque além de criar algo pra vender, o processo de construção já é processo de construção da empresa — praticar produto, praticar conversa com cliente, ter algo tangível.

Matheus levantou um ponto crucial: **o receio de virar um apanhado de módulos que não conversam.** Software da década passada, peças remendadas. Receio legítimo.

---

## A peça que faltava: ontologia

Pesquisando sobre a Palantir, surgiu o conceito de ontologia — uma camada de significado que fica entre os dados e as interfaces.

A Palantir não construiu "módulos". Ela construiu uma representação unificada do mundo real — objetos (equipamentos, pessoas, transações), relações entre eles, e ações possíveis. Qualquer app que roda em cima da Palantir está falando com o mesmo modelo da realidade.

Traduzindo pra HiHotel: a gente não precisa de módulos. Precisa de uma **ontologia hoteleira** — um modelo unificado do que é um hotel.

```
Objetos: Hóspede, Funcionário, Quarto, Pedido, Turno, Evento, Treinamento...
Relações: Hóspede ←está_em→ Quarto, Funcionário ←atende→ Hóspede...
Ações: Check-in atualiza Quarto + notifica Funcionários + ativa perfil Concierge
```

Quando isso existe como fundação, o "app do restaurante" não é um módulo separado — é uma **janela** sobre a ontologia. O Concierge é outra janela. O Claude Vault é outra. Cada hotel pode ter interfaces diferentes, integrações diferentes, mas a ontologia é a mesma. É isso que mantém tudo coerente.

A arquitetura fica assim:

```
         PESSOAS (hóspedes, funcionários, gestores)
              ↕
     VERBOS DA HIHOTEL
     aprender · ensinar · coordenar · elevar
     reconhecer · conectar · traduzir · lembrar
              ↕
         INTERFACES
     Concierge · App Restaurante · Claude Vault · Dashboard Gestor
              ↕
      ONTOLOGIA HOTELEIRA
     (modelo unificado — objetos, relações, ações)
              ↕
      DADOS E INTEGRAÇÕES
     PMS · Bancos · APIs · Modelos de IA
```

---

## Os verbos da HiHotel

A HiHotel é feita pra humanos. O objetivo: atingir o ápice do potencial de cada pessoa no hotel — garçom, camareira, supervisor, gestor. Um sistema otimizado pra que todos possam brilhar.

Os verbos que definem o que a HiHotel faz no mundo:

- **APRENDER** — o funcionário aprende continuamente
- **ENSINAR** — o sistema ensina, funcionários ensinam uns aos outros
- **COORDENAR** — informação certa, pessoa certa, hora certa
- **ELEVAR** — levar cada pessoa ao seu potencial máximo
- **RECONHECER** — tornar visível o trabalho bem feito
- **CONECTAR** — hóspede↔funcionário, gestor↔equipe, hotel↔hotel
- **TRADUZIR** — gestor pede → sistema traduz pra equipe
- **LEMBRAR** — preferências, competências, o que funcionou antes

Nenhum desses é verbo de software. Não tem "automatizar", "otimizar", "digitalizar". São verbos de gente. Verbos de liderança e educação. A tecnologia é invisível.

Juntos, esses verbos descrevem um líder. A HiHotel é um líder digital — não substituindo liderança humana, mas fazendo o que nenhum gestor consegue sozinho: estar em todos os lugares, lembrar de tudo, reconhecer cada pessoa.
