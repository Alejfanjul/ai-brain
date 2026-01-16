# Exemplo de Conversa: Documentando Check-in

Simulação de como o bot conduziria uma entrevista.

---

## FASE 1: ABERTURA

**Bot:**
> Oi! Sou o assistente de documentação do hotel.
>
> Vou te ajudar a registrar como funciona um processo do seu dia a dia. É simples: você explica como faz, eu anoto tudo e faço algumas perguntas para não faltar nada.
>
> No final, gero uma documentação organizada que pode ajudar a treinar pessoas novas.
>
> **Qual processo você quer documentar hoje?**

**Funcionário (áudio):**
> "Quero explicar o check-in"

---

## FASE 2: ESCUTA ATIVA

**Bot:**
> Ótimo! Check-in é fundamental. Me conta como você faz do início ao fim - pode falar à vontade que eu vou anotando tudo.

**Funcionário (áudio):**
> "Então, quando o hóspede chega, primeiro eu cumprimento, pergunto o nome e procuro a reserva no sistema. Aí confiro os dados, peço documento e cartão de crédito pra garantia. Passo o cartão na maquininha, se der certo, dou as informações do quarto - número, andar, horário do café - e entrego a chave. Pronto, basicamente é isso."

**Bot:**
> Entendi bem a estrutura geral! Deixa eu fazer algumas perguntas para completar os detalhes.

---

## FASE 3: PREENCHIMENTO DE GAPS

**Bot:**
> Você mencionou que procura a reserva no sistema. Qual sistema vocês usam? E se o hóspede não tiver reserva, o que acontece?

**Funcionário:**
> "O sistema é o Hospedin. Se não tiver reserva, a gente pode fazer walk-in ali na hora mesmo, se tiver quarto disponível. Aí eu mostro as opções de quarto e preço."

**Bot:**
> E quando você passa o cartão pra garantia - o que acontece se for recusado?

**Funcionário:**
> "Aí complica um pouco. Primeiro peço outro cartão. Se não tiver, pode pagar em dinheiro adiantado ou Pix. Se o hóspede não aceitar nenhuma opção, aí tenho que chamar o gerente."

**Bot:**
> Faz sentido. E antes do hóspede chegar - tem algo que você prepara? Ou é tudo na hora?

**Funcionário:**
> "Ah sim, no começo do turno a gente olha as chegadas previstas do dia. Se tiver VIP ou alguém com pedido especial, já deixa anotado. E confere se os quartos tão liberados pela governança."

**Bot:**
> Quanto tempo leva um check-in normal, sem problemas?

**Funcionário:**
> "Uns 3 a 5 minutos. Mas se for grupo ou tiver problema no cartão, pode levar 15, 20 minutos."

**Bot:**
> Último ponto: depois que você entrega a chave, precisa fazer mais alguma coisa? Registrar em algum lugar?

**Funcionário:**
> "Sim, marco no sistema que o check-in foi feito. E se o hóspede pediu algo específico - tipo travesseiro extra - passo pra governança pelo rádio ou WhatsApp do setor."

---

## FASE 4: VALIDAÇÃO

**Bot:**
> Deixa eu ver se entendi tudo certo:
>
> **Check-in começa** quando o hóspede chega na recepção.
>
> **Antes**, você verifica as chegadas do dia e se os quartos estão liberados.
>
> **O processo é:** cumprimentar → buscar reserva no Hospedin → conferir dados → pedir documento e cartão → passar garantia → informar sobre o quarto → entregar chave → registrar no sistema.
>
> **Se o cartão for recusado:** pede outro, ou aceita dinheiro/Pix, ou chama gerente.
>
> **Se não tiver reserva:** faz walk-in se tiver disponibilidade.
>
> **Depois:** marca check-in no sistema e avisa governança se tiver pedido especial.
>
> **Tempo:** 3-5 min normal, até 20 min com problemas.
>
> Tá certo isso? Faltou alguma coisa importante?

**Funcionário:**
> "Isso! Só faltou: a gente também pede pra assinar a FNRH - aquela ficha de registro de hóspede. É obrigatório."

**Bot:**
> Anotado! E última pergunta: se você fosse treinar alguém novo, qual o erro mais comum que a pessoa cometeria?

**Funcionário:**
> "Esquecer de verificar se o quarto tá liberado antes de entregar a chave. Já aconteceu de mandar hóspede pra quarto que ainda tava sendo limpo. Constrangedor demais."

---

## FASE 5: ENCERRAMENTO

**Bot:**
> Perfeito! Tenho tudo que preciso. Muito obrigado pelo tempo - seu conhecimento vai ajudar muito no treinamento de pessoas novas.
>
> Vou gerar a documentação agora. Se precisar tirar alguma dúvida depois, posso voltar a perguntar?

**Funcionário:**
> "Pode sim, sem problema."

**Bot:**
> Ótimo! Aqui está a documentação:
>
> 📄 **[Gera os 4 outputs: SOP, Checklist, FAQ, Ficha Resumo]**

---

## OUTPUT GERADO

### SOP: Check-in de Hóspedes

**Responsável:** Recepcionista
**Frequência:** A cada chegada de hóspede
**Tempo médio:** 3-5 minutos (até 20 min com exceções)

#### Objetivo
Registrar a entrada do hóspede, coletar garantia de pagamento e entregar acesso ao quarto.

#### Pré-requisitos
- Sistema Hospedin acessível
- Lista de chegadas do dia verificada
- Confirmação da governança de quartos liberados
- Maquininha de cartão funcionando
- Chaves/cartões dos quartos disponíveis
- Fichas FNRH impressas

#### Procedimento

**1. Preparação (início do turno)**
- Verificar chegadas previstas do dia no Hospedin
- Identificar VIPs ou pedidos especiais
- Confirmar com governança quais quartos estão liberados

**2. Recepção do hóspede**
- Cumprimentar o hóspede
- Perguntar nome completo
- Localizar reserva no Hospedin

> ⚠️ **Atenção:** Se não houver reserva, verificar disponibilidade para walk-in

**3. Conferência de dados**
- Confirmar datas de entrada e saída
- Confirmar tipo de quarto
- Solicitar documento de identificação
- Solicitar cartão de crédito para garantia

**4. Garantia de pagamento**
- Passar cartão na maquininha (pré-autorização)
- Se recusado: solicitar outro cartão
- Se não tiver: aceitar dinheiro ou Pix adiantado
- Se recusar todas opções: chamar gerente

**5. Registro**
- Pedir assinatura na FNRH (obrigatório)
- Registrar check-in no sistema

**6. Entrega do quarto**
- Informar: número do quarto, andar, horário do café
- Entregar chave/cartão
- Verificar se há pedidos especiais

> ⚠️ **Atenção:** SEMPRE verificar se o quarto está liberado pela governança antes de entregar a chave

**7. Finalização**
- Se houver pedido especial: comunicar governança (rádio/WhatsApp)

#### Exceções

| Situação | Ação | Escalar se |
|----------|------|------------|
| Cartão recusado | Pedir outro cartão, dinheiro ou Pix | Hóspede recusar todas opções |
| Sem reserva | Oferecer walk-in se houver disponibilidade | Não houver quartos |
| Quarto não liberado | Pedir para aguardar, oferecer guardar bagagem | Demora > 30 min |

#### Checklist de Qualidade
- [ ] Reserva localizada e confirmada
- [ ] Documento verificado
- [ ] Garantia processada
- [ ] FNRH assinada
- [ ] Quarto confirmado como liberado
- [ ] Informações do hotel passadas
- [ ] Check-in registrado no sistema

---

### Checklist: Check-in

- [ ] Verificar se quarto está liberado (governança)
- [ ] Localizar reserva no Hospedin
- [ ] Conferir documento do hóspede
- [ ] Passar garantia no cartão
- [ ] Coletar assinatura na FNRH
- [ ] Informar quarto, andar e café
- [ ] Entregar chave
- [ ] Registrar check-in no sistema
- [ ] Avisar governança se pedido especial

---

### FAQ: Check-in

**P: E se o hóspede não tiver reserva?**
R: Verificar disponibilidade no Hospedin e oferecer walk-in com as opções de quarto e preço.

**P: O cartão foi recusado, o que fazer?**
R: Pedir outro cartão. Se não tiver, aceitar dinheiro ou Pix adiantado. Se recusar, chamar gerente.

**P: O quarto ainda está sendo limpo, e agora?**
R: Pedir desculpas, oferecer para guardar bagagem, avisar que será chamado quando liberado.

**P: O que é FNRH?**
R: Ficha Nacional de Registro de Hóspede. É obrigatório por lei. O hóspede precisa assinar.

**P: Preciso avisar alguém depois do check-in?**
R: Só se houver pedido especial (travesseiro extra, berço, etc). Nesse caso, avisa governança por rádio ou WhatsApp.

---

### Check-in - Resumo

**O que é:** Processo de entrada do hóspede no hotel
**Quando:** Hóspede chega na recepção
**Tempo:** 3-5 min (normal) / até 20 min (com problemas)
**Resultado:** Hóspede com chave do quarto liberado, garantia coletada, registro no sistema

**Os 3 erros mais comuns:**
1. Entregar chave sem confirmar com governança → Sempre verificar se quarto está liberado
2. Esquecer FNRH → Pedir assinatura ANTES de entregar a chave
3. Não registrar no sistema → Marcar check-in imediatamente após entregar chave

**Se der problema:** Chamar gerente de plantão
