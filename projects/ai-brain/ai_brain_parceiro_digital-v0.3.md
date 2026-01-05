# AI Brain - Parceiro Digital Pessoal

**Data:** 05/01/2026 (v0.3)
**Status:** Em concepção - arquitetura simplificada
**Changelog v0.3:**
- Arquitetura simplificada: Claude Code CLI + Hooks (em vez de API direta + FastAPI)
- Removido Telegram como interface inicial
- Foco em audit trail como primeira implementação
- Supabase free tier definido como banco
- Features JFDI marcadas
- Integração com repositório sistema-os

---

## Visao Geral

Um parceiro digital que sabe absolutamente tudo da minha vida. Nao e assistente que executa comandos - e parceiro que entende contexto, conecta ideias, distribui informacao e me relembra do que precisa ser relembrado.

### Principio central
> "Ferramenta que cria o cenario ideal pra que voce possa dar vazao a todas as ideias, potencial, vontades e objetivos que voce tem na vida - de forma organizada e estruturada."

O AI Brain e um parceiro que trabalha junto comigo pra otimizar e aproveitar melhor minha energia. Ele entende contexto, propoe, acompanha, aprende.

### Validacao externa: JFDI System (Alex Hillman)

Alex Hillman, fundador do Indie Hall (coworking em Philadelphia), construiu algo muito similar chamado **JFDI System**. Em ~3 semanas de desenvolvimento ativo (Outubro-Dezembro 2025), ele criou um sistema que:

> "Has already had a materially positive impact on my life, my productivity, my happiness. Most importantly, my executive function where open loops really are a challenge for me."

**Por que isso importa:** Hillman tinha exatamente os mesmos problemas que queremos resolver - ferramentas que exigem manutencao manual, multiplos sistemas desconectados, dificuldade em saber o que fazer a seguir. O sistema dele prova que a abordagem funciona.

**Como Hillman construiu:** Ele usa **Claude Code Headless Mode** (CLI), nao API direta:
> "I am not hitting Anthropic's API directly for anything. Everything is going through Claude Code using Claude Code headless mode."

---

## Conexao Estrategica

### Prototipo para o sistema de hospitalidade
Este AI Brain pessoal e prototipo da interface que funcionarios de hotel usarao no futuro. A mesma logica:

- Em vez de navegar menus e preencher campos, a pessoa fala: *"faz o checkin do Joao Mendes, ele chegou com a esposa Priscila, vou fazer tour agora"*
- O sistema entende, executa, avisa quem precisa, registra onde precisa

Aprender construindo pra mim, depois adaptar pro contexto corporativo.

### Estrategia Derek Sivers
1. Construir pra resolver meu problema
2. Documentar a jornada publicamente (marca pessoal)
3. Se funciona pra mim, talvez funcione pra outros
4. Entregar de graca enquanto pode, validar
5. Quando comecar a custar, cobrar

---

## O que o sistema precisa fazer

### Capacidades de entrada
- [ ] Receber texto
- [ ] Receber audio (transcrever)
- [ ] Receber imagem / print de tela
- [ ] Receber de qualquer lugar (interface propria, terminal, futuro: mobile)

### Capacidades de processamento
- [ ] Entender o contexto da mensagem
- [ ] Identificar a qual projeto/area se refere
- [ ] Decidir o que fazer: anotar? criar tarefa? lembrar depois? responder?
- [ ] Conectar com informacoes relacionadas que ja existem - JFDI
- [ ] Busca semantica ("aquela ideia sobre gamificacao" -> encontra mesmo sem a palavra exata) - JFDI

### Comportamento proativo
- [ ] Acompanhar projetos ativamente - perguntar como esta a evolucao
- [ ] Propor atividades baseado no que conhece dos projetos
- [ ] Aprender quanto de atividade consigo executar em determinado periodo
- [ ] Entender contexto emocional/fisico (desanimado, mal de saude)
- [ ] Avaliar junto comigo o que e possivel fazer no momento - JFDI
- [ ] Ajustar expectativas e propostas baseado no meu estado atual - JFDI

### Processamento automatico de conteudo
- [ ] Processar conteudos que chegam automaticamente (ex: posts do Nate, newsletters) - JFDI
- [ ] Gerar resumos breves diarios - leitura de ~3 minutos sem eu pedir - JFDI
- [ ] Identificar conexoes entre conteudos novos e meus projetos/ideias - JFDI
- [ ] Encadear conteudos de diferentes fontes pra formar visao integrada - JFDI
- [ ] Alertar quando algo relevante pro meu contexto aparecer - JFDI
- [ ] Trabalhar em background, nao so quando eu aciono - JFDI

### Capacidades de saida
- [ ] Responder no momento
- [ ] Gravar no projeto/local adequado
- [ ] Criar compromissos/lembretes - JFDI
- [ ] Me procurar na hora certa (nao eu procurando ele) - JFDI
- [ ] Avisar outras pessoas/sistemas quando necessario - JFDI

---

## Abordagem Tecnica: Claude Code CLI + Hooks

### Por que essa abordagem (v0.3)

**Antes (v0.2):** Claude API direto + FastAPI + Telegram + servidor
**Agora (v0.3):** Claude Code CLI + Hooks + Supabase

**Vantagens:**
1. **Simplicidade:** Nao precisa de servidor, roda local
2. **Validada:** Exatamente como Hillman construiu o JFDI
3. **Custo:** ~$0/mes para comecar (Supabase free tier)
4. **Session ID:** Persistencia de conversas nativa
5. **Hooks:** Auditoria automatica de tudo

### Como funciona

```
Eu uso Claude Code no terminal
        |
        v
Hooks interceptam cada acao
        |
        v
PostToolUse -> salva no Supabase
        |
        v
Audit trail automatico
```

### Hooks disponiveis (Python)

| Hook | Quando dispara | Uso |
|------|----------------|-----|
| `PostToolUse` | Apos cada tool executar | Registrar arquivos tocados, comandos |
| `UserPromptSubmit` | Ao enviar prompt | Registrar meus prompts |
| `Stop` | Ao finalizar sessao | Salvar transcript completo |
| `PreToolUse` | Antes de executar tool | Validar/bloquear acoes |

### Session ID para persistencia

```bash
# Iniciar sessao
session_id=$(claude -p "Comecar trabalho no projeto X" --output-format json | jq -r '.session_id')

# Continuar na mesma sessao
claude -p "Continuar de onde paramos" --resume "$session_id"
```

---

## Integracao com sistema-os

O repositorio `sistema-os` (separado do ai-brain) tambem sera integrado ao mesmo sistema de audit trail.

### Organizacao
- Um banco so no Supabase
- Campo `repositorio` distingue origem (`ai-brain` ou `sistema-os`)
- Mesmos hooks, mesma estrutura

### Objetivo do sistema-os
> "Registrar tudo o que e feito para que eu possa automatizar ao longo do tempo."

O audit trail de ambos os repositorios alimenta:
1. Identificacao de padroes repetitivos
2. Sugestoes de automacoes
3. SOPs automaticas

---

## Referencias do JFDI System: Por que cada feature existe

Esta secao documenta os problemas reais que levaram Hillman a construir cada parte do sistema. Util para priorizar e entender o "porque" por tras de cada decisao.

### 1. Dashboard Automatizado (Morning Overview)

**Problema que resolve:**
> "Every project management tool I've ever used had the same problem - what it expects from me. I'm the worst at going in and keeping them current and up-to-date and clean and gardened and organized."

**Como funciona:**
- Gerado automaticamente as 8:30 todo dia util
- Olha todos os sistemas: calendario, inbox, tarefas, projetos, relacionamentos
- Gera prioridades e recomendacoes de ordem
- Mostra blocos de tempo disponiveis entre compromissos

**Insight chave:**
> "The dream of an assistant who you wake up in the morning and your day is prepared for you. That's what this is."

**Aplicacao no AI Brain:** O sistema deve preparar meu dia, nao esperar que eu pergunte. Resumo matinal automatico e essencial.

---

### 2. Sistema de Lembretes Integrado

**Problema que resolve:**
> "I was not already in a reminders tool. I had to go elsewhere to get a reminders tool."

**Como funciona:**
- Sempre a um clique de distancia (vive dentro do sistema principal)
- Snooze inteligente: swipe left para adiar, swipe right para completar
- Diferencia "lembretes anytime" (sem data) de lembretes com prazo

**Insight chave:**
> "It is directly integrated into wherever I already am... I don't have to open a separate tool."

**Aplicacao no AI Brain:** Nao criar sistema de lembretes separado. Integrar na interface principal.

---

### 3. Gestao de Projetos com "Now View"

**Problema que resolve:**
> "None of these tools really help me figure out what to do next. They're great at making me feel overwhelmed, but never great at making me feel like I know what I should be doing next."

**Como funciona:**
- **Life View (30.000 ft):** Espacos/areas da vida
- **Project View (10.000 ft):** Projetos e tarefas
- **Now View (ground level):** O que fazer AGORA

**Now View - a inovacao principal:**
- Mostra tarefas overdue + ate 3 proximas tarefas nao-datadas
- Permite filtrar por tipo de energia: Quick Win, Creative, Deep Work
- Cada tarefa tem um "energy type" classificado automaticamente por Haiku

**Insight chave:**
> "Lets me approach the work that needs doing intentionally... allowing me to be proactive while using my energy as a tool rather than as a constraint."

**Aplicacao no AI Brain:** Adicionar conceito de "tipo de energia" as tarefas. Sistema deve sugerir baseado em como estou me sentindo.

---

### 4. Relationship Manager (CRM Pessoal)

**Problema que resolve:**
> "I've always wanted a CRM that was not about sales but about actual relationship building - more focus on depth than closing."

**Como funciona:**
- Arquivo markdown para cada pessoa
- Tracking automatico de pontos de contato
- Bubble up de relacionamentos que precisam de atencao
- Nao diferencia "trabalho" de "pessoal" - sao pessoas na minha vida

**Insight chave:**
> "A CRM never made sense and a personal CRM never made sense. These are just people in my life."

**Integracao inteligente:**
- Quando salva um link interessante, o sistema sugere: "Isso seria interessante para essas 1-3 pessoas. Quer enviar?"
- Cria lembretes automaticamente (nao envia sem confirmacao)

**Aplicacao no AI Brain:** Pessoas sao entidades centrais. Conectar tudo a pessoas quando relevante.

---

### 5. Sistema de Reunioes

**Problema que resolve:**
> "I've never been much of a notetaker except for when it matters. And the trouble is I don't always know that it matters until after the fact."

**Como funciona:**

**Antes da reuniao (automatico):**
- Olha calendario, identifica participantes
- Cruza com relacionamentos existentes
- Gera prep sheet: ultima vez que conversamos, o que discutimos, conexoes entre participantes

**Depois da reuniao:**
- Botao para processar notas/transcricao
- Extrai: 3 takeaways, decisoes, outputs, compromissos
- Gera tarefas automaticamente para coisas que EU me comprometi
- Gera lembretes para follow-up de coisas que OUTROS se comprometeram

**Insight chave:**
> "Show up fully present knowing what we're there to talk about and not having to draw purely on memory every time I sit down."

**Aplicacao no AI Brain:** Preparacao pre-reuniao e processamento pos-reuniao sao features essenciais.

---

### 6. Knowledge System (Second Brain)

**Problema que resolve:**
> "Your standard second brain type stuff. The difference is it doesn't require all the human labor of figuring out where to put things."

**Como funciona:**
- Dropa link -> sistema extrai, resume, organiza
- Conexoes automaticas entre conteudos
- Cruza com relacionamentos para sugerir compartilhamento

**Exemplo real:**
> "I grabbed a podcast link, dropped it in the system and said 'The guest had a cool decision-making framework. Can you find that?' And it pulled out exactly what it was along with awesome examples - better notes than I would have taken."

**Aplicacao no AI Brain:** Knowledge management deve ser zero-friction. Jogar conteudo e deixar o sistema organizar.

**Status atual:** Ja temos 68 documentos capturados de 15+ autores em `/home/marketing/ai-brain/sources/`

---

### 7. Goal Alignment Tracker

**Problema que resolve:**
Manter foco nas prioridades certas ao longo do tempo.

**Como funciona:**
- Sistema entrevistou Hillman sobre goals para 60-90 dias
- Definiu proporcoes: 40% crescer Indie Hall, 35% parcerias, 25% relacionamentos
- Todo dia analisa todas as atividades e mostra progresso vs. goals
- Ajuda a priorizar: "Esses lembretes atrasados podem esperar pra amanha. Isso e o que voce precisa fazer."

**Aplicacao no AI Brain:** Ter visao de goals de medio prazo e checar alinhamento regularmente.

---

## Sistema de Memoria: Evolucao e Implementacao

Esta e uma das partes mais sofisticadas do sistema do Hillman. Ele evoluiu em tres fases.

### Fase 1: Audit Trail (Semanas 1-2)

**Conceito:** Cada agente/comando documenta o que fez depois de executar.

**Estrutura:**
```
/audits/
  /2025-12-13/
    overview-activity.md
    person-researcher-activity.md
    newsletter-activity.md
```

**O que cada audit contem:**
- O que aconteceu
- Acoes tomadas
- Decisoes feitas dentro do contexto
- Opcoes consideradas (mesmo as nao escolhidas)
- Cross-agent notes (para agentes que rodam em paralelo)
- Arquivos criados/modificados

**Insight chave:**
> "Trust through transparency - I design things to provide me maximum transparency and then as a byproduct that transparency becomes value to both me and the system."

**Resultado:** ~1/3 das features novas vieram de sugestoes do proprio sistema analisando padroes nos audit trails.

---

### Fase 2: Sintese Semanal (Semanas 3-4)

**Conceito:** Semanalmente, analisar todos os audits e extrair padroes.

**Agentes envolvidos:**
- Pattern Miner: encontra repeticoes
- Recommendation Tracker: sugere melhorias
- System Gap Detector: encontra sistemas que deveriam conversar
- Strategic Adviser: identifica oportunidades

**O que a sintese gera:**
- Padroes identificados com confidence score
- Recomendacoes de features/melhorias
- Tracking de recomendacoes implementadas vs. ignoradas

**Insight chave:**
> "Hey, you did this the same way the last three times. Do you want to just make that an SOP so I don't have to guess each time?"

**Aplicacao no AI Brain:** Comecar com audit trails simples. Sintese pode vir depois.

---

### Fase 3: Memory Lane (Semanas 4+)

**Conceito:** Memoria semantica com recall automatico baseado em contexto.

**Arquitetura:**

```
1. Sessoes Claude Code -> Salvas em Supabase (tabela claude_sessions)
2. Job a cada 15min -> "Memory Catcher" extrai memorias
3. Memorias -> Embedding gerado localmente (Ollama)
4. Embeddings -> Armazenados em PG Vector
5. Claude Code Hooks -> Injetam memorias relevantes no contexto
```

**Tipos de memorias extraidas:**
- Decisoes
- Insights
- Padroes
- Compromissos
- Momentos de aprendizado
- Correcoes (em ambas direcoes)
- Workflows
- Gaps (sistemas que deveriam conversar)

**Triggers de "surpresa" (inspirado em paper do Google):**
- Recovery patterns: tentou X, falhou, fez Y e funcionou
- User corrections: "nao assim, assim"
- Enthusiasm signals: "isso e exatamente o que eu queria!"
- Negative reactions: "nunca faca isso"
- Repeat requests: pedindo a mesma coisa multiplas vezes

**Retrieval inteligente:**
1. Quando digito mensagem -> extrai entidades (pessoas, projetos)
2. Busca memorias relacionadas as entidades
3. Busca semantica adicional baseada no significado
4. Filtra por relevancia ao contexto atual
5. Injeta no contexto do Claude

**Feedback loop:**
- Thumbs up/down em cada memoria surfada
- +-5% weight adjustment por feedback
- Sistema melhora com uso

**Insight chave:**
> "This is a way to build relevant context on the fly... gives you in effect the ability to remember something."

---

## Jornada de Construcao: Por Onde Comecar

Baseado na evolucao do JFDI System e nas decisoes desta conversa.

### Fase 1: Audit Trail (Semana 1) - PRIMEIRA VITORIA

**Objetivo:** Deixar de usar Claude Web e usar somente via ai-brain/sistema-os, com todas as conversas persistidas.

```
1. Criar conta Supabase (free tier)
2. Schema basico: sessoes, audits
3. Configurar hooks do Claude Code
4. Hook PostToolUse salva no Supabase
5. Testar em: ai-brain E sistema-os
```

**O que Hillman tinha nessa fase:** Claude Code + arquivos markdown + comandos basicos

**Entregavel:** Toda interacao com Claude Code e registrada automaticamente.

---

### Fase 2: Persistencia de Conversas (Semana 2)

```
1. Session ID para continuar conversas
2. Salvar transcripts completos
3. Busca basica em conversas anteriores
4. Campo 'repositorio' para distinguir origem
```

**Entregavel:** Posso continuar conversas de onde parei e buscar o que ja discuti.

---

### Fase 3: Memoria e Sintese (Semanas 3-4)

```
1. Extracao de memorias dos transcripts
2. Sintese semanal de padroes
3. Sugestoes de automacoes baseadas em padroes
```

**Insight chave:**
> "You can get so much value out of this without vector search. Don't let people tell you that you need fancy databases with vector search to get the power."

**Entregavel:** Sistema comeca a sugerir melhorias baseado em padroes.

---

### Fase 4: Interface e Proatividade (Semanas 5+)

```
1. Interface web propria (se necessario)
2. Morning overview automatico
3. Lembretes e check-ins
4. Embeddings para busca semantica (opcional)
```

**Entregavel:** Sistema me procura, prepara meu dia, lembra de contexto.

---

## Decisoes de Infraestrutura

### Principio fundamental: Conexao direta com modelos de ponta

> **"Nao quero me distanciar de modelos de ponta (Claude Opus, Sonnet, Haiku) pois eles evoluem rapidamente. Quero que meu app se mova rapidamente em termos de incorporar novas funcionalidades advindas de novos modelos."**

Isso significa:
- **Sem frameworks intermediarios** - LangChain, CrewAI, n8n criam rigidez
- **Claude Code CLI** - Acesso direto as features mais recentes
- **Codigo proprio** - Controle total sobre como usar os recursos

### Validacao do Hillman

Hillman usa **Claude Code Headless Mode** para tudo:
> "I am not hitting Anthropic's API directly for anything. Everything is going through Claude Code using Claude Code headless mode."

**Vantagem:** Session ID permite continuar conversas, compactar contexto, etc.

### Por que essa decisao

**Exemplo concreto:** Claude lancou "extended thinking" recentemente. Com framework, teria que esperar atualizacao. Com Claude Code CLI, uso imediatamente.

---

## Stack Tecnologica (v0.3)

| Componente | Tecnologia | Justificativa |
|------------|------------|---------------|
| **Core** | Claude Code CLI + Hooks | Mesma abordagem do JFDI, simplicidade |
| **Interface inicial** | Terminal (`claude -p`) | Zero setup, ja funciona |
| **BD** | Supabase (free tier) | PostgreSQL gratis, facil de usar |
| **BD vetorial** | pgvector (futuro) | Quando precisar de busca semantica |
| **Embeddings** | Ollama (local, futuro) | Sem dependencia de API externa |
| **Hosting** | Local | Sem custo, sem complexidade |

### Comparacao com JFDI System

| Componente | JFDI System | AI Brain (v0.3) |
|------------|-------------|-----------------|
| **Core** | Claude Code (headless mode) | Claude Code CLI + Hooks |
| **UI** | Web app custom (mobile-first) | Terminal (futuro: web) |
| **BD** | Supabase (PostgreSQL) | Supabase (PostgreSQL) |
| **Vetorial** | PG Vector | pgvector (futuro) |
| **Embeddings** | Ollama (local) | Ollama (futuro) |

---

## Modelo de Dados (Simplificado para v0.3)

### Schema inicial (Fase 1)

```sql
-- Sessoes de chat
CREATE TABLE sessoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT UNIQUE, -- ID do Claude Code
    repositorio TEXT NOT NULL, -- 'ai-brain' ou 'sistema-os'
    primeira_mensagem TEXT,
    ultima_mensagem TEXT,
    transcript_completo JSONB,
    arquivos_tocados TEXT[],
    tool_calls JSONB,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

-- Audit trails
CREATE TABLE audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sessao_id UUID REFERENCES sessoes(id),
    repositorio TEXT NOT NULL,
    data DATE DEFAULT CURRENT_DATE,
    agente TEXT, -- qual hook/comando executou
    acoes_tomadas JSONB,
    arquivos_modificados TEXT[],
    criado_em TIMESTAMP DEFAULT NOW()
);
```

### Schema futuro (Fase 2+)

```sql
-- Memorias extraidas
CREATE TABLE memorias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sessao_id UUID REFERENCES sessoes(id),
    tipo TEXT, -- 'decisao', 'insight', 'padrao', 'compromisso'
    resumo TEXT,
    contexto_original TEXT,
    confidence_score FLOAT,
    embedding VECTOR(1536), -- quando implementar busca semantica
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Padroes identificados
CREATE TABLE padroes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    descricao TEXT,
    frequencia INTEGER,
    sugestao_automacao TEXT,
    implementado BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT NOW()
);
```

---

## Estimativa de Custos (v0.3)

| Item | Custo |
|------|-------|
| Claude Code Max | $100/mes (ja uso) |
| Supabase | $0 (free tier) |
| Servidor | $0 (roda local) |
| Ollama | $0 (roda local) |
| **Total adicional** | **$0/mes** |

---

## Framework de Construcao + Captura

### Principio fundamental

> **"Tudo que eu fizer tem que gerar material pra que possa futuramente ser feito por agente."**

Cada hora de trabalho gera valor em tres dimensoes:
1. **O resultado** - o agente, o sistema, a funcionalidade
2. **O conteudo** - material para marca pessoal (YouTube, blog, etc)
3. **A automacao futura** - instrucao para agente replicar o processo

### Validacao do JFDI System

Hillman descobriu que ~1/3 das features novas vieram de sugestoes do proprio sistema:
> "I don't know what the percentage is. I could probably ask it. If I had to ballpark it, it's probably somewhere near a third where it's like, hey, if we built this feature or we updated this feature in this way, this problem would go away."

### Fluxo de captura

```
[Eu faco manualmente]
       |
       v
[Audit trail documenta o processo]
       |
       v
[Sintese semanal identifica padroes]
       |
       v
[Sistema sugere automacoes]
       |
       v
[Material vira conteudo (YouTube, etc)]
       |
       v
[Agente replica o processo]
```

---

## Proximos passos

### Imediato (proxima sessao)
1. **Criar conta Supabase** - free tier
2. **Criar schema basico** - sessoes + audits
3. **Configurar hook PostToolUse** - salvar no Supabase
4. **Testar** - fazer uma tarefa no ai-brain e verificar se salvou

### Curto prazo (Semana 1)
5. **Configurar no sistema-os** - mesmo hook, mesmo banco
6. **Validar persistencia** - session_id funcionando
7. **Primeira vitoria** - parar de usar Claude Web

### Medio prazo (Semanas 2-4)
8. **Busca em conversas** - encontrar o que ja discuti
9. **Extracao de memorias** - decisoes, insights, padroes
10. **Sintese semanal** - identificar padroes repetitivos

### Longo prazo (Semanas 5+)
11. **Morning overview** - dashboard diario automatico
12. **Busca semantica** - pgvector + Ollama
13. **Interface web** - se necessario

---

## Conexao com marca pessoal

Documentar publicamente a construcao deste sistema:
- Os problemas que estou resolvendo
- As descobertas e os erros
- O processo de aprender IA construindo
- Inspiracao: videos de restauracao de caminhao (acompanhar o processo, nao so o resultado)

> "Eu tenho objetivo de construir negocio. Eu acho que inteligencia artificial pode ser o caminho. E eu vou mostrar eu procurando esse caminho."

---

## Apendice: Quotes importantes do JFDI System

### Sobre o problema que resolve
> "Every project management tool I've ever used had the same problem - what it expects from me. I'm the worst at going in and keeping them current."

### Sobre proatividade
> "The dream of an assistant who you wake up in the morning and your day is prepared for you."

### Sobre memoria simples
> "You can get so much value out of this without vector search. Don't let people tell you that you need fancy databases with vector search to get the power."

### Sobre transparencia
> "Trust through transparency - I design things to provide me maximum transparency and then as a byproduct that transparency becomes value to both me and the system."

### Sobre o impacto
> "Has already had a materially positive impact on my life, my productivity, my happiness. Most importantly, my executive function."

### Sobre documentacao gerando SOPs
> "Almost everything of meaning that this system does is basically a giant SOP or collection of SOPs. And I found that it's very very good at writing instructions better than I've ever been."

### Sobre Claude Code Headless
> "I am not hitting Anthropic's API directly for anything. Everything is going through Claude Code using Claude Code headless mode."

---

*Documento vivo - sera atualizado conforme novas ideias surgirem*

*v0.3 - Arquitetura simplificada (CLI + Hooks + Supabase)*
