# Plano de Entrevista para TELOS

> Perguntas curtas e diretas para construir TELOS pessoal
> Responda em 1-3 frases. Pode ser por texto ou voz.

---

## Sessão 1: Problemas e Missão (5-10 min)

### PROBLEMS - O que te incomoda no mundo?

**P1.** Qual injustiça no mundo te irrita de verdade?

**P2.** O que as pessoas fazem que você pensa "isso é desperdício"?

**P3.** Se pudesse resolver UM problema no mundo, qual seria?

### MISSION - Por que você existe?

**P4.** Quando você se sente mais útil?

**P5.** O que você faria de graça pelo resto da vida?

**P6.** Complete: "Eu existo para _______"

---

## Sessão 2: Metas e Métricas (5-10 min)

### GOALS - O que você quer?

**P7.** Daqui 1 ano, o que precisa ter acontecido para você considerar sucesso?

**P8.** Daqui 5 anos, como é um dia típico seu?

**P9.** O que você quer ter construído antes de morrer?

### METRICS - Como mede progresso?

**P10.** Como você sabe se está no caminho certo? (sinais concretos)

**P11.** Que número você olharia toda semana para saber se está progredindo?

**P12.** O que significa "liberdade" em termos concretos? (ex: R$ X/mês, X horas livres)

---

## Sessão 3: Desafios e Estratégias (5-10 min)

### CHALLENGES - O que te trava?

**P13.** O que te impede de avançar mais rápido agora?

**P14.** Qual hábito seu te sabota?

**P15.** O que você evita fazer mesmo sabendo que deveria?

### STRATEGIES - Como vai superar?

**P16.** Qual sua estratégia atual para o ai-brain/hotel?

**P17.** O que você precisa aprender nos próximos 6 meses?

**P18.** Quem poderia te ajudar? (pessoa ou tipo de pessoa)

---

## Sessão 4: Autoconhecimento (5-10 min)

### THINGS I'VE BEEN WRONG ABOUT

**P19.** Cite algo que você acreditava fortemente e descobriu estar errado.

**P20.** Que conselho você dava que hoje discorda?

**P21.** Que previsão sua não se concretizou?

### PREDICTIONS

**P22.** O que você acha que vai acontecer com IA nos próximos 2 anos?

**P23.** Que tendência as pessoas ainda não perceberam?

**P24.** Onde você estará em 3 anos? (% de confiança)

---

## Sessão 5: Sabedoria e Identidade (5-10 min)

### WISDOM - O que você aprendeu?

**P25.** Qual a lição mais importante que a vida te ensinou?

**P26.** Que frase você repetiria para si mesmo todo dia?

**P27.** O que você diria para o Ale de 10 anos atrás?

### IDENTITY - Quem você é?

**P28.** Como você se apresentaria em 1 frase para um estranho?

**P29.** O que te diferencia de outras pessoas com perfil similar?

**P30.** O que você quer que falem de você no seu funeral?

---

## Sessão 6: Contexto Pessoal (opcional, 5 min)

### HISTORY

**P31.** 3 momentos que te moldaram (positivos ou negativos)?

### TRAUMAS (se quiser compartilhar)

**P32.** Algo difícil que ainda afeta suas decisões hoje?

### FAVORITES

**P33.** 3 livros que mais te influenciaram?

**P34.** 3 filmes que te marcaram?

---

## Sessão 7: Atualização (5 min)

### O QUE MUDOU NOS ÚLTIMOS 6 MESES

**P35.** O que mudou na sua situação desde o Perfil V5?

**P36.** Alguma crença que mudou?

**P37.** O ai-brain virou o projeto principal?

**P38.** Alguma meta nova?

---

## Como usar

**Opção A:** Responde todas de uma vez (30-40 min total)

**Opção B:** Uma sessão por dia (5-10 min cada)

**Opção C:** Responde só as que considerar importantes

Após as respostas, eu estruturo tudo no formato TELOS.

---

## Output esperado

Após a entrevista, teremos:

```
TELOS-ALE.md
├── PROBLEMS (P1-P3)
├── MISSION (P4-P6)
├── GOALS (P7-P9)
├── METRICS (P10-P12)
├── CHALLENGES (P13-P15)
├── STRATEGIES (P16-P18)
├── WRONG ABOUT (P19-P21)
├── PREDICTIONS (P22-P24)
├── WISDOM (P25-P27)
├── NARRATIVES (P28-P30)
├── HISTORY (P31)
├── TRAUMAS (P32)
├── FAVORITES (P33-P34)
└── LOG (data de criação)
```

---

## Meta: criar pattern

Após validar esse processo contigo, transformamos em:

```
fabric/patterns/create_telos_interview/
└── system.md
```

Assim qualquer pessoa pode usar para criar seu próprio TELOS.

---

## Progresso

| Data | O que aconteceu | Arquivo gerado |
|------|-----------------|----------------|
| 2026-01-13 | Entrevista gravada (38 perguntas) | Pendente processamento |
| 2026-01-13 | Conversa exploratória com Claude | `TELOS-CONVERSA-01.md` |

### Insights da conversa (não estava no roteiro)

A conversa exploratória revelou coisas que as 38 perguntas talvez não capturassem:
- Definição pessoal de propósito
- Visão de produto/sistema emergiu organicamente
- Barreira identificada (episódio do café da manhã)
- Padrão de comportamento (transformar caos em sistema)

### Próximos passos

- [ ] Processar áudio da entrevista gravada
- [ ] Consolidar respostas + insights da conversa em `TELOS-ALE.md`
