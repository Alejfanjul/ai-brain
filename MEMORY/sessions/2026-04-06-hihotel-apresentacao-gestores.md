# Sessão: HiHotel — Preparação da Apresentação para Gestores

**Data:** 2026-04-06
**Participantes:** Ale + Claude (modo conversa)
**Contexto:** Após entrega das cartas de demissão (30/03), proposta formal (02/04), e evolução conceitual (ontologia, bounded contexts, entidades do restaurante), Ale quer preparar uma nova apresentação para todos os gestores do Duke.

---

## Objetivo da sessão

Alinhar contexto político, definir público, tom e estrutura de uma nova apresentação da HiHotel para os gestores do Duke Beach Hotel. A estrutura foi criada e está pronta para validação antes de virar HTML.

---

## Contexto político atualizado

### Cronologia recente
- **30/03:** Cartas de demissão entregues. Richard não estava (esposa doente). Carta ficou com assistente.
- **01/04 (terça):** Diego ainda não sabia. Ale contou. Diego ficou desconfortável por não ter sido avisado primeiro.
- **03/04 (quinta):** Richard veio conversar. Chamou atenção pelo formato da saída. Não sabia que já tinha 3 semanas desde a apresentação. Achava que queriam só pejotização (risco trabalhista). Ale esclareceu: estão abrindo empresa. Richard mostrou mais empatia. Informou custos reais (Ale R$6.6k + Matheus R$8k). Richard deu a entender falta de alinhamento entre ele e Diego.
- **02/04 (quarta, final da tarde):** Diego veio à sala, reclamou que foi colocado em posição delicada. Questionou confiança. Disse que a gestão não está convencida do SID. Pediu que preparassem apresentação pra toda a gestão. Usou estratégia do medo — tentou fazer Ale e Matheus sentirem que o apoio não existe.

### Dinâmica entre gestores
- Comunicação entre gestores é fragmentada e ruim
- Diego funcionava como intermediário entre Ale/Matheus e o restante da gestão
- Diego usava o SID como bandeira pessoal — aceitava pedidos sem questionar e repassava pra Ale
- Resultado: módulos construídos a pedido do Diego são pouco utilizados. Os mais usados (OS, personalização) foram criados por iniciativa do Ale sem interferência do Diego
- Richard e Diego parecem ter falta de alinhamento entre si
- Heiko pode estar menos amigável por se sentir pressionado pela carta de demissão

### Postura da HiHotel
- Evitar atrito direto com o Diego
- Deixar claro que a HiHotel se relaciona com o hotel inteiro, não abaixo de nenhum departamento
- O SID não é bandeira do Diego — é ferramenta do hotel, construída pela HiHotel
- A HiHotel tem visão própria, propõe mudanças, não fica aguardando pedidos

---

## Os gestores (público da apresentação)

### Heiko (Diretor/CEO)
- Visionário, já conhece o SID, fez pitch deck de 18 páginas
- Pode estar menos amigável por causa da pressão da carta de demissão
- Não é garantido como apoiador. Pode estar neutro ou desconfortável
- Se estiver na apresentação, o mais poderoso é ele ver os outros gestores reconhecendo valor

### Diego (Marketing)
- Estará presente. Desconfortável com a situação
- Usava o SID como bandeira pessoal, sem ser bom gestor do produto
- Não atacar, mas a apresentação comunica a mudança implicitamente: "cada gestor tem voz direta"
- Já tem módulos pra ele: dashboards de concorrentes, vendas, hóspede 360°

### Fábio Reis (Gerente Operacional — Hospedagem)
- Cuida de: concierge, recepção, governança, manutenção
- Hoje é neutro / não vê muito valor no SID
- Dor concreta: descontente com a Nonius (TV dos quartos)
- Oportunidade: Concierge Platform substitui Nonius, já funcional, inclusa nos R$18k
- Ale e Matheus querem apresentar o Concierge pra ele (pode ser antes da apresentação geral)
- Também: governança (status de quartos, OS), manutenção (chamados, histórico)

### Fabrício (Chefe de Cozinha / Gerente de A&B)
- Cuida de: restaurante, bares, cozinha, (possivelmente estoque)
- Cenário parecido com o do Diego — provavelmente neutro ou cético
- Contratou assistente pra realizar controles que o SID poderia ajudar
- Dores concretas: fichas técnicas, cálculo de custo de pratos, menu → lista de compras, controle de estoque
- Oportunidade: app de restaurante (entidades já modeladas em detalhe — artefatos 1.1, 1.2, 1.3)

### Richard (RH)
- Já conversou com Ale e Matheus, tem mais contexto que os outros
- Pediu lista de atividades (provavelmente a pedido do Heiko)
- Dores: muito retrabalho na área dele
- Oportunidade: automação de processos repetitivos, onboarding com quiz, comunicação interna estruturada

---

## Decisões sobre a apresentação

### Tom escolhido
"A gente quer ouvir vocês e construir o que faz sentido" — mas sem ser consultoria passiva. A HiHotel tem visão própria, é parceira com direção. Não replica módulos que replicam problemas da hotelaria tradicional.

Tom B com assertividade: escuta ativa + posicionamento claro de que a HiHotel transita pelo hotel inteiro e propõe mudanças, não aguarda pedidos.

### O que NÃO entra na apresentação (decisão consciente)
- Valores financeiros (já estão na proposta formal)
- IP / propriedade intelectual (já na proposta)
- Visão de futuro / ontologia / IA (público não se importa agora)
- Currículo detalhado (eles já conhecem Ale e Matheus)
- Comparação com sistemas do mercado
- Qualquer menção a atrito com Diego ou modelo anterior

### Formato
- HTML (mesmo estilo da apresentação-v7)
- Prática, exemplos reais do Duke, sem jargão técnico

---

## Estrutura dos slides (criada e salva)

Arquivo: `projects/hihotel/proposta/estrutura-apresentacao-gestores.md`

1. **Abertura** — "A gente conhece o Duke por dentro. E quer construir as ferramentas que vocês realmente precisam."
2. **O que a HiHotel é** — breve, credibilidade rápida, não currículo
3. **O que já existe e funciona** — OS, personalização, concorrentes, dashboard, acessos, Concierge. Não é promessa — já roda.
4. **O problema que a gente quer resolver** — falta de conexão entre sistemas, pessoas e informação (neutro, sem culpar ninguém)
5. **Como a HiHotel pode ajudar cada área** — slide central:
   - Fábio: Concierge + governança + manutenção
   - Fabrício: fichas técnicas + restaurante + estoque
   - Richard: retrabalho + onboarding + comunicação
   - Diego: dashboards + hóspede 360°
6. **Como a gente trabalha** — HiHotel no centro, conectada a todos, não abaixo de nenhum. Reunião quinzenal com gestores. Cada um tem voz direta.
7. **O que a gente precisa de vocês** — acesso, liberdade pra propor, feedback honesto, tempo
8. **Fechamento com escuta** — "O que mais incomoda no dia-a-dia de vocês?"

---

## Próximos passos

- [ ] Ale e Matheus validam a estrutura dos slides
- [ ] Conversar individualmente com gestores antes da apresentação (se possível)
   - Fábio: apresentar Concierge Platform
   - Fabrício: entender dores de A&B em detalhe
   - Richard: entender retrabalho específico
- [ ] Após validação, produzir HTML da apresentação
- [ ] Definir data da apresentação com o hotel

---

## Referências para produção do HTML

- Estilo visual: mesmo da `2026-03-17-apresentacao-inicial-heiko-diego.html`
- Conteúdo do slide 5 (cada área): enriquecer com dados das conversas individuais quando acontecerem
- Entidades do restaurante já modeladas em `artefatos/1.1-entidades-restaurante.md` — usar como base pra exemplos concretos do Fabrício
- Proposta formal em `2026-04-02-proposta-hihotel-duke.md` — não repetir conteúdo, mas manter coerência

---

## Nota sobre continuidade

Ale vai continuar esta conversa provavelmente do computador amanhã. O próximo passo é ele validar a estrutura (possivelmente com Matheus) e então pedir a produção do HTML. Se houver conversas individuais com gestores antes, o conteúdo do slide 5 pode ser enriquecido.
