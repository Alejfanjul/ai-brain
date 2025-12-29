# Building an AI-Native Company - Dan Shipper (Every)

## Metadata
- **Fonte:** Palestra "Dispatch from the Future: building an AI-native Company"
- **Palestrante:** Dan Shipper (CEO, Every)
- **Evento:** AI & I Conference
- **URL:** https://www.youtube.com/watch?v=MGzymaYBiss
- **Duração:** ~17 min
- **Data extração:** 2025-12-27

## Resumo

Palestra sobre como construir uma empresa nativa de IA usando agentes de código (Claude Code, Cursor, Codeium). Dan Shipper compartilha a experiência da Every, que opera 4 produtos de software com apenas 15 pessoas, onde 99% do código é escrito por agentes IA e cada app é mantido por um único desenvolvedor. O conceito central é **Compounding Engineering**: um processo de 4 etapas (Plan → Delegate → Assess → Codify) que garante que cada feature torna a próxima mais fácil de construir.

## Dados da Every (Contexto)

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Pessoas** | 15 | Total da empresa |
| **Business Units** | 6 | Incluindo produtos e conteúdo |
| **Produtos de Software** | 4 | Apps complexos em produção |
| **Assinantes Pagos** | 7.000+ | Crescimento duplo-dígito/mês (últimos 6 meses) |
| **Assinantes Free** | 100.000+ | Base total |
| **Capital Levantado** | ~$1M | Operação capital-efficient |
| **Código via IA** | 99% | Ninguém escreve código manualmente |
| **Dev por App** | 1 | Um desenvolvedor principal por produto |

## Conceito Central: 100% AI Adoption

### Diferença 10x: 90% vs 100%

**Tese principal:** Há uma diferença de **10x** entre uma org onde 90% dos engenheiros usam IA vs 100%.

**Por quê?**
- Mesmo que 10% da empresa use métodos tradicionais (digitar em code editor), você precisa "voltar completamente para aquele mundo"
- Isso impede que você faça coisas que só são possíveis quando **ninguém** está editando código manualmente
- É um regime completamente diferente de trabalho

**Evidência na Every:**
- Transformou completamente o que é possível fazer como empresa pequena
- Permite operar como um "laboratório do que é possível"

## Produtos Desenvolvidos (Exemplos)

### 1. Kora - AI Email Management
- **Descrição:** Assistente de email com IA
- **Features:**
  - Painel esquerdo: Resumos de todos os emails recebidos
  - Painel direito: Assistente que responde perguntas sobre o email
- **Time:** 1 engenheiro + 1-2 contractors ocasionais
- **Complexidade:** Milhares de usuários

### 2. Monologue - Speech-to-Text
- **Descrição:** App de transcrição de voz (similar a Super Whisper / Whisper Flow)
- **Time:** 1 desenvolvedor
- **Complexidade:** App "belamente feito", não-trivial

### 3. Spiral
- **Descrição:** [Produto mostrado nos screenshots como exemplo de app complexo]
- **Time:** 1 engenheiro
- **Complexidade:** "É grande" (interface mostrada é substancial)

## Compounding Engineering: O Loop de 4 Etapas

### Definição
> "Em engenharia tradicional, cada feature torna a próxima feature **mais difícil** de construir. Em Compounding Engineering, seu objetivo é garantir que cada feature torne a próxima feature **mais fácil** de construir."

### Loop de 4 Etapas

```
1. PLAN → 2. DELEGATE → 3. ASSESS → 4. CODIFY
     ↑                                      ↓
     └──────────────────────────────────────┘
```

#### 1. PLAN (Planejar)
- Criar planos **extremamente detalhados**
- É crítico quando trabalhando com agentes
- Todos na conferência já sabem da importância disso

#### 2. DELEGATE (Delegar)
- Dizer ao agente para executar o plano
- "Just go tell the agent to do it"
- Processo direto

#### 3. ASSESS (Avaliar)
- **Muitas maneiras** de avaliar se o trabalho do agente é bom:
  - Testes automatizados
  - Testar manualmente
  - Ter o agente avaliar a si mesmo
  - Code review humano
  - Code review por agente
  - Outras técnicas

#### 4. CODIFY (Codificar) ⭐ **ETAPA CHAVE**
- **"The money step"** - onde a composição acontece
- Pegar todo conhecimento tácito adquirido nas etapas 1-3
- Transformar em prompts explícitos que vão para:
  - Arquivos `claude.md`
  - Sub-agentes
  - Slash commands
  - Outros arquivos de configuração
- Criar uma **biblioteca de conhecimento explícito**
- Espalhar esse conhecimento para toda a organização

**Resultado:** Conhecimento tácito individual → Biblioteca explícita compartilhada

## Unlocks de Produtividade (1ª Ordem)

### 1. Trabalho Paralelo em Features/Bugs
- **Meme do "vibe coder":** 4 panes abertas, mas não fazendo trabalho real
- **Realidade na Every:** Engenheiros produtivamente usando **4 panes de agentes simultaneamente**
- Contribui muito para a capacidade de 1 dev construir/manter app de produção

### 2. Prototipagem de Ideias Arriscadas
- **Por quê:** Código é barato agora
- **Benefício:** Permite fazer mais experimentos
- **Como:** Energia inicial para tentar algo é muito menor
  - "Go do some research on this big refactor I might want to do"
  - Enquanto isso, você trabalha em outra coisa
- **Resultado:** Muito mais progresso através de experimentação

### 3. Demo Culture (Cultura de Demonstrações)
- **Antes:** Escrever memo/deck → convencer pessoas que vale a pena investir tempo
- **Agora:** Vibe code algo em **poucas horas** que mostra a ideia
- **Vantagem:** Permite fazer coisas mais estranhas/ousadas que "só funcionam se você sentir"
- **Processo:** Mostrar ao invés de explicar

## Efeitos de 2ª Ordem (Não-Óbvios)

### 1. Compartilhamento Tácito de Código
**Problema tradicional:**
- Para compartilhar código entre produtos, precisa abstrair em biblioteca
- Difícil fazer download e integrar
- Alto custo de coordenação

**Solução com IA:**
- Apontar Claude Code para o **repo do dev ao lado**
- Agente aprende o processo usado para construir a feature
- Reimplementa no seu próprio tech stack/framework
- **Zero custo adicional**

**Benefício:** Quanto mais devs trabalhando em coisas diferentes, mais compartilhamento sem overhead

### 2. Novos Contratados Produtivos no Dia 1
**Como:**
- Todo conhecimento sobre setup, commits, boas práticas já está em:
  - `claude.md`
  - `cursor.rules`
  - Arquivos do Codeium
  - Outros arquivos de configuração
- Agente configura ambiente local automaticamente
- Agente já sabe escrever bons PRs

**Benefício:** Zero ramp-up time

### 3. Expert Freelancers para Tarefas Pontuais
- Contratar especialista em algo específico
- Ele/ela pode entrar **por 1 dia** e fazer aquela coisa
- **Analogia:** Como DJ que entra em alguns compassos de uma música
- **Antes:** Custo de startup muito alto para colaboração curta
- **Agora:** Viável e eficiente

### 4. Devs Commitam em Outros Produtos
**Cenário na Every:**
- 4 produtos internos
- Todo mundo usa todos os produtos
- Se alguém encontra bug ou paper cut (pequeno problema de UX):
  - Baixa o repo do outro produto
  - Tem Claude/Codex descobrir como consertar
  - Submete PR para o GM daquele app

**Benefício:** Colaboração cross-produto muito mais fácil

**Especulação futura:**
- Clientes poderão fazer isso
- Encontrou um bug? Seu agente conserta e submete PR
- "Weird open source thing"

### 5. Sem Necessidade de Padronizar Stack/Linguagem
**Prática tradicional:** Toda empresa padroniza (ex: "somos uma empresa Python")

**Prática na Every:**
- Cada dev de cada produto escolhe stack que prefere
- IA traduz entre diferentes tecnologias
- Mais fácil pular entre linguagens/frameworks e ser produtivo

**Benefício:** Deixar pessoas usarem o que gostam, IA faz a ponte

### 6. Managers Podem Commitar Código ⚠️
**Contexto:**
- Dan (CEO) commita código de produção regularmente
- Não tem tempo (4 produtos, 15 pessoas, crescimento rápido)
- Mas consegue fazer mesmo assim

**Por quê funciona:**
- **Atenção fraturada** agora é possível
- **Antes:** Precisava bloco de 3-4h de foco
- **Agora:**
  - Sai de reunião
  - "Hey, investigue esse bug"
  - Vai fazer outra coisa
  - Volta e tem plano/root cause fix
  - Submete PR

**Observação:** "Não é fácil, não é mágico, mas é possível"

**Impacto:** Nova forma de managers interagirem com produtos que constroem

## Ferramentas Mencionadas

| Ferramenta | Tipo | Uso na Every |
|------------|------|--------------|
| **Claude Code** | Coding agent (terminal UI) | Principal, pioneiro na eliminação do code editor |
| **Cursor** | Code editor com IA | Usado pela equipe |
| **Codeium** | Code assistant | Usado pela equipe |
| **Devin** | Coding agent | Mencionado como opção |

**Nota:** Dan enfatiza "coding agent of your choice" - não há lock-in em ferramenta específica

## Lógica de Negócio

### Modelo de Negócio da Every
- **Tagline:** "The only subscription you need to stay at the edge of AI"
- **Site:** every.to

### 3 Pilares:

1. **IDEAS (Ideias)**
   - Newsletter diário sobre IA
   - Reviews de novos modelos quando lançam
   - Reviews de novos produtos quando lançam

2. **APPS (Aplicativos)**
   - Bundle de todos os apps (Kora, Monologue, Spiral, etc.)
   - Todos incluídos na assinatura

3. **TRAINING (Treinamento)**
   - Consultoria com grandes empresas
   - Ajudar a usar IA

**Modelo de Preço:** Tudo em **uma assinatura única**

## Insights para Implementação

### 1. Adoção 100% é Crítica
- Não é sobre "a maioria usar IA"
- É sobre **eliminar completamente** edição manual de código
- Mudança de regime, não incremento

### 2. Codify é a Etapa que Diferencia
- Planning, Delegation, Assessment = todo mundo faz
- **Codifying** = transformar aprendizado em biblioteca reutilizável
- Este é o passo que cria o efeito composto

### 3. Arquivos de Configuração são Assets Estratégicos
- `claude.md`, `cursor.rules`, etc. não são "só configs"
- São a **memória institucional compilada**
- Quanto mais ricos, mais rápido novos devs/features

### 4. Single-Developer Products são Viáveis
- Não é sobre "toy projects"
- Apps de produção complexos com milhares de usuários
- 1 dev principal + contractors ocasionais

### 5. Capital Efficiency Extrema
- $1M raised para construir 4 produtos + 100k usuários
- IA permite fazer muito mais com muito menos capital

### 6. Demo > Docs
- Prototipar é tão rápido que faz mais sentido mostrar que explicar
- Permite explorar ideias que "só fazem sentido quando você sente"

## Padrões de UX Observados

### Interface dos Apps
- **Kora:** Split-pane (resumos à esquerda, chat à direita)
- **Monologue:** Interface de transcrição (não detalhada no vídeo)
- **Spiral:** Interface complexa multi-seção (mostrada como exemplo de escala)

### Filosofia de Design
- Apps não são "toys" - são produtos polidos e completos
- Foco em UX mesmo sendo construídos rapidamente
- Milhares de usuários reais validam qualidade

## Conexões com Sistema-OS

### Aplicável ao Desenvolvimento do RM Module:

1. **Codifying Best Practices:**
   - Criar `claude.md` para o projeto sistema-os
   - Documentar padrões de RM, estrutura de dados, regras de negócio
   - Cada feature de RM deve enriquecer esse arquivo

2. **Demo Culture para Stakeholders:**
   - Prototipar telas de RM rapidamente para Duke Beach Hotel
   - Mostrar conceitos (Pick Up, Overbooking, etc.) em demos ao invés de specs

3. **Single-Developer Viability:**
   - RM module pode ser construído/mantido por 1 dev principal
   - Usar agentes para paralelizar trabalho

4. **Cross-Repository Learning:**
   - Usar repos do Climber RMS como referência
   - Agentes podem aprender padrões sem copiar código

5. **Expert Freelancers:**
   - Contratar especialista em RM para consultoria de 1 dia
   - Agente absorve conhecimento e implementa

## Timestamps de Referência

- **00:41** — Introdução: "Everyone is moving to San Francisco... but I love New York"
- **01:14** — "I don't have a playbook... the playbook is being invented right now"
- **02:06** — **Tese Principal:** 10x difference entre 90% e 100% AI adoption
- **03:19** — Stats da Every: 15 pessoas, 4 produtos, 7k assinantes
- **03:37** — **99% do código escrito por IA agents**
- **04:28** — Demo: Kora (email AI assistant)
- **04:59** — Demo: Monologue (speech-to-text)
- **05:20** — Demo: Spiral (app complexo)
- **05:52** — Unlock 1: Trabalho paralelo em múltiplas features
- **06:42** — Unlock 2: Prototipagem de ideias arriscadas
- **07:37** — Unlock 3: Demo culture
- **08:39** — **Introdução: Compounding Engineering**
- **09:03** — Loop de 4 etapas: Plan → Delegate → Assess → Codify
- **10:13** — **Codify é o "money step"**
- **11:17** — Efeito 2ª ordem: Compartilhamento tácito de código
- **12:29** — Efeito 2ª ordem: Novos contratados produtivos no dia 1
- **12:55** — Efeito 2ª ordem: Expert freelancers viáveis
- **13:52** — Efeito 2ª ordem: Devs commitam em outros produtos
- **14:24** — Efeito 2ª ordem: Sem padronização de stack
- **15:17** — **Efeito 2ª ordem: Managers podem commitar código**
- **16:06** — Resumo final
- **16:59** — Every.to pitch

## Termos e Conceitos

| Termo | Significado |
|-------|-------------|
| **Compounding Engineering** | Processo onde cada feature torna a próxima mais fácil (vs tradicional onde fica mais difícil) |
| **Codify** | Transformar conhecimento tácito em prompts/configs explícitos e reutilizáveis |
| **Vibe Coder** | Meme sobre devs usando múltiplas janelas de agentes sem ser produtivo (mas Dan mostra que é possível ser produtivo assim) |
| **Demo Culture** | Preferência por prototipar e mostrar ao invés de escrever specs/memos |
| **Paper Cut** | Pequeno problema de UX que irrita mas não é crítico |
| **100% AI Adoption** | Regime onde NINGUÉM edita código manualmente - todos usam agentes |
| **Fractured Attention** | Capacidade de trabalhar em código sem blocos longos de foco (possível com agentes) |
| **Capital Efficient** | Construir muito com pouco investimento |
| **Tacit Code Sharing** | Compartilhar conhecimento de código sem abstrair em biblioteca |

## Citações Memoráveis

> "There's a 10x difference between an org where 90% of engineers are using AI versus an org where 100% of engineers are using AI. It's totally different."

> "In traditional engineering, each feature makes the next feature harder to build. In compounding engineering, your goal is to make sure that each feature makes the next feature easier to build."

> "The last step [Codify] which is I think the most interesting one... is kind of like the money step."

> "We run four software products with just 15 people, which is kind of crazy. And these software products are not toys."

> "99% of our code is written by AI agents. No one is handwriting code. No one is writing code at all."

> "With Claude Code, you can kind of like get out of meeting and say, 'Hey, I want you to investigate this bug,' and then go do something else and then come back and you have like a plan or like a root cause fix."

> "Many people in San Francisco don't know this yet [about New York having this knowledge]. So you're the first to hear it."

## Conclusão e Aplicabilidade

Esta palestra oferece um **framework mental completo** para como operar em um mundo onde código é escrito por agentes. Os conceitos de **Compounding Engineering** e **100% AI Adoption** são aplicáveis ao desenvolvimento do sistema-os, especialmente:

1. **Documentação como Asset:** Transformar este knowledge extraction em parte do processo de Codify
2. **RM Module como Produto Single-Dev:** Viável com agentes
3. **Integração com Duke Beach:** Demo culture para validar features rapidamente
4. **Crescimento Sustentável:** Capital-efficient development permite crescer sem levantar capital massivo

**Próximos Passos Sugeridos:**
- Criar `claude.md` robusto para sistema-os
- Documentar padrões de RM nesse arquivo
- Implementar loop Plan → Delegate → Assess → Codify formalmente
- Considerar 1 dev dedicado ao RM module full-time com suporte de agentes
