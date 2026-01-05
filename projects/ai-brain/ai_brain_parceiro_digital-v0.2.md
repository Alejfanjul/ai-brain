# AI Brain - Parceiro Digital Pessoal

**Data:** 04/01/2026 (v0.2)
**Status:** Em concepção - arquitetura definida
**Changelog v0.2:** Enriquecido com insights do JFDI System (Alex Hillman) - sistema similar em produção desde Dezembro 2025

---

## Visão Geral

Um parceiro digital que sabe absolutamente tudo da minha vida. Não é assistente que executa comandos - é parceiro que entende contexto, conecta ideias, distribui informação e me relembra do que precisa ser relembrado.

### Princípio central
> "Ferramenta que cria o cenário ideal pra que você possa dar vazão a todas as ideias, potencial, vontades e objetivos que você tem na vida - de forma organizada e estruturada."

O AI Brain é um parceiro que trabalha junto comigo pra otimizar e aproveitar melhor minha energia. Ele entende contexto, propõe, acompanha, aprende.

### Validação externa: JFDI System (Alex Hillman)

Alex Hillman, fundador do Indie Hall (coworking em Philadelphia), construiu algo muito similar chamado **JFDI System**. Em ~3 semanas de desenvolvimento ativo (Outubro-Dezembro 2025), ele criou um sistema que:

> "Has already had a materially positive impact on my life, my productivity, my happiness. Most importantly, my executive function where open loops really are a challenge for me."

**Por que isso importa:** Hillman tinha exatamente os mesmos problemas que queremos resolver - ferramentas que exigem manutenção manual, múltiplos sistemas desconectados, dificuldade em saber o que fazer a seguir. O sistema dele prova que a abordagem funciona.

---

## Conexão Estratégica

### Protótipo para o sistema de hospitalidade
Este AI Brain pessoal é protótipo da interface que funcionários de hotel usarão no futuro. A mesma lógica:

- Em vez de navegar menus e preencher campos, a pessoa fala: *"faz o checkin do João Mendes, ele chegou com a esposa Priscila, vou fazer tour agora"*
- O sistema entende, executa, avisa quem precisa, registra onde precisa

Aprender construindo pra mim, depois adaptar pro contexto corporativo.

### Estratégia Derek Sivers
1. Construir pra resolver meu problema
2. Documentar a jornada publicamente (marca pessoal)
3. Se funciona pra mim, talvez funcione pra outros
4. Entregar de graça enquanto pode, validar
5. Quando começar a custar, cobrar

---

## O que o sistema precisa fazer

### Capacidades de entrada
- [ ] Receber texto
- [ ] Receber áudio (transcrever)
- [ ] Receber imagem / print de tela
- [ ] Receber de qualquer lugar (interface própria, Telegram, WhatsApp)

### Capacidades de processamento
- [ ] Entender o contexto da mensagem
- [ ] Identificar a qual projeto/área se refere
- [ ] Decidir o que fazer: anotar? criar tarefa? lembrar depois? responder?
- [ ] Conectar com informações relacionadas que já existem
- [ ] Busca semântica ("aquela ideia sobre gamificação" → encontra mesmo sem a palavra exata)

### Comportamento proativo
- [ ] Acompanhar projetos ativamente - perguntar como está a evolução
- [ ] Propor atividades baseado no que conhece dos projetos
- [ ] Aprender quanto de atividade consigo executar em determinado período
- [ ] Entender contexto emocional/físico (desanimado, mal de saúde)
- [ ] Avaliar junto comigo o que é possível fazer no momento
- [ ] Ajustar expectativas e propostas baseado no meu estado atual

### Processamento automático de conteúdo
- [ ] Processar conteúdos que chegam automaticamente (ex: posts do Nate, newsletters)
- [ ] Gerar resumos breves diários - leitura de ~3 minutos sem eu pedir
- [ ] Identificar conexões entre conteúdos novos e meus projetos/ideias
- [ ] Encadear conteúdos de diferentes fontes pra formar visão integrada
- [ ] Alertar quando algo relevante pro meu contexto aparecer
- [ ] Trabalhar em background, não só quando eu aciono

### Capacidades de saída
- [ ] Responder no momento
- [ ] Gravar no projeto/local adequado
- [ ] Criar compromissos/lembretes
- [ ] Me procurar na hora certa (não eu procurando ele)
- [ ] Avisar outras pessoas/sistemas quando necessário

---

## Referências do JFDI System: Por que cada feature existe

Esta seção documenta os problemas reais que levaram Hillman a construir cada parte do sistema. Útil para priorizar e entender o "porquê" por trás de cada decisão.

### 1. Dashboard Automatizado (Morning Overview)

**Problema que resolve:**
> "Every project management tool I've ever used had the same problem - what it expects from me. I'm the worst at going in and keeping them current and up-to-date and clean and gardened and organized."

**Como funciona:**
- Gerado automaticamente às 8:30 todo dia útil
- Olha todos os sistemas: calendário, inbox, tarefas, projetos, relacionamentos
- Gera prioridades e recomendações de ordem
- Mostra blocos de tempo disponíveis entre compromissos

**Insight chave:**
> "The dream of an assistant who you wake up in the morning and your day is prepared for you. That's what this is."

**Aplicação no AI Brain:** O sistema deve preparar meu dia, não esperar que eu pergunte. Resumo matinal automático é essencial.

---

### 2. Sistema de Lembretes Integrado

**Problema que resolve:**
> "I was not already in a reminders tool. I had to go elsewhere to get a reminders tool."

**Como funciona:**
- Sempre a um clique de distância (vive dentro do sistema principal)
- Snooze inteligente: swipe left para adiar, swipe right para completar
- Diferencia "lembretes anytime" (sem data) de lembretes com prazo

**Insight chave:**
> "It is directly integrated into wherever I already am... I don't have to open a separate tool."

**Aplicação no AI Brain:** Não criar sistema de lembretes separado. Integrar na interface principal.

---

### 3. Gestão de Projetos com "Now View"

**Problema que resolve:**
> "None of these tools really help me figure out what to do next. They're great at making me feel overwhelmed, but never great at making me feel like I know what I should be doing next."

**Como funciona:**
- **Life View (30.000 ft):** Espaços/áreas da vida
- **Project View (10.000 ft):** Projetos e tarefas
- **Now View (ground level):** O que fazer AGORA

**Now View - a inovação principal:**
- Mostra tarefas overdue + até 3 próximas tarefas não-datadas
- Permite filtrar por tipo de energia: Quick Win, Creative, Deep Work
- Cada tarefa tem um "energy type" classificado automaticamente por Haiku

**Insight chave:**
> "Lets me approach the work that needs doing intentionally... allowing me to be proactive while using my energy as a tool rather than as a constraint."

**Aplicação no AI Brain:** Adicionar conceito de "tipo de energia" às tarefas. Sistema deve sugerir baseado em como estou me sentindo.

---

### 4. Relationship Manager (CRM Pessoal)

**Problema que resolve:**
> "I've always wanted a CRM that was not about sales but about actual relationship building - more focus on depth than closing."

**Como funciona:**
- Arquivo markdown para cada pessoa
- Tracking automático de pontos de contato
- Bubble up de relacionamentos que precisam de atenção
- Não diferencia "trabalho" de "pessoal" - são pessoas na minha vida

**Insight chave:**
> "A CRM never made sense and a personal CRM never made sense. These are just people in my life."

**Integração inteligente:**
- Quando salva um link interessante, o sistema sugere: "Isso seria interessante para essas 1-3 pessoas. Quer enviar?"
- Cria lembretes automaticamente (não envia sem confirmação)

**Aplicação no AI Brain:** Pessoas são entidades centrais. Conectar tudo a pessoas quando relevante.

---

### 5. Sistema de Reuniões

**Problema que resolve:**
> "I've never been much of a notetaker except for when it matters. And the trouble is I don't always know that it matters until after the fact."

**Como funciona:**

**Antes da reunião (automático):**
- Olha calendário, identifica participantes
- Cruza com relacionamentos existentes
- Gera prep sheet: última vez que conversamos, o que discutimos, conexões entre participantes

**Depois da reunião:**
- Botão para processar notas/transcrição
- Extrai: 3 takeaways, decisões, outputs, compromissos
- Gera tarefas automaticamente para coisas que EU me comprometi
- Gera lembretes para follow-up de coisas que OUTROS se comprometeram

**Insight chave:**
> "Show up fully present knowing what we're there to talk about and not having to draw purely on memory every time I sit down."

**Aplicação no AI Brain:** Preparação pré-reunião e processamento pós-reunião são features essenciais.

---

### 6. Knowledge System (Second Brain)

**Problema que resolve:**
> "Your standard second brain type stuff. The difference is it doesn't require all the human labor of figuring out where to put things."

**Como funciona:**
- Dropa link → sistema extrai, resume, organiza
- Conexões automáticas entre conteúdos
- Cruza com relacionamentos para sugerir compartilhamento

**Exemplo real:**
> "I grabbed a podcast link, dropped it in the system and said 'The guest had a cool decision-making framework. Can you find that?' And it pulled out exactly what it was along with awesome examples - better notes than I would have taken."

**Aplicação no AI Brain:** Knowledge management deve ser zero-friction. Jogar conteúdo e deixar o sistema organizar.

---

### 7. Goal Alignment Tracker

**Problema que resolve:**
Manter foco nas prioridades certas ao longo do tempo.

**Como funciona:**
- Sistema entrevistou Hillman sobre goals para 60-90 dias
- Definiu proporções: 40% crescer Indie Hall, 35% parcerias, 25% relacionamentos
- Todo dia analisa todas as atividades e mostra progresso vs. goals
- Ajuda a priorizar: "Esses lembretes atrasados podem esperar pra amanhã. Isso é o que você precisa fazer."

**Aplicação no AI Brain:** Ter visão de goals de médio prazo e checar alinhamento regularmente.

---

## Sistema de Memória: Evolução e Implementação

Esta é uma das partes mais sofisticadas do sistema do Hillman. Ele evoluiu em três fases.

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

**O que cada audit contém:**
- O que aconteceu
- Ações tomadas
- Decisões feitas dentro do contexto
- Opções consideradas (mesmo as não escolhidas)
- Cross-agent notes (para agentes que rodam em paralelo)
- Arquivos criados/modificados

**Insight chave:**
> "Trust through transparency - I design things to provide me maximum transparency and then as a byproduct that transparency becomes value to both me and the system."

**Resultado:** ~1/3 das features novas vieram de sugestões do próprio sistema analisando padrões nos audit trails.

---

### Fase 2: Síntese Semanal (Semanas 3-4)

**Conceito:** Semanalmente, analisar todos os audits e extrair padrões.

**Agentes envolvidos:**
- Pattern Miner: encontra repetições
- Recommendation Tracker: sugere melhorias
- System Gap Detector: encontra sistemas que deveriam conversar
- Strategic Adviser: identifica oportunidades

**O que a síntese gera:**
- Padrões identificados com confidence score
- Recomendações de features/melhorias
- Tracking de recomendações implementadas vs. ignoradas

**Insight chave:**
> "Hey, you did this the same way the last three times. Do you want to just make that an SOP so I don't have to guess each time?"

**Aplicação no AI Brain:** Começar com audit trails simples. Síntese pode vir depois.

---

### Fase 3: Memory Lane (Semanas 4+)

**Conceito:** Memória semântica com recall automático baseado em contexto.

**Arquitetura:**

```
1. Sessões Claude Code → Salvas em Supabase (tabela claude_sessions)
2. Job a cada 15min → "Memory Catcher" extrai memórias
3. Memórias → Embedding gerado localmente (Ollama)
4. Embeddings → Armazenados em PG Vector
5. Claude Code Hooks → Injetam memórias relevantes no contexto
```

**Tipos de memórias extraídas:**
- Decisões
- Insights
- Padrões
- Compromissos
- Momentos de aprendizado
- Correções (em ambas direções)
- Workflows
- Gaps (sistemas que deveriam conversar)

**Triggers de "surpresa" (inspirado em paper do Google):**
- Recovery patterns: tentou X, falhou, fez Y e funcionou
- User corrections: "não assim, assim"
- Enthusiasm signals: "isso é exatamente o que eu queria!"
- Negative reactions: "nunca faça isso"
- Repeat requests: pedindo a mesma coisa múltiplas vezes

**Retrieval inteligente:**
1. Quando digito mensagem → extrai entidades (pessoas, projetos)
2. Busca memórias relacionadas às entidades
3. Busca semântica adicional baseada no significado
4. Filtra por relevância ao contexto atual
5. Injeta no contexto do Claude

**Feedback loop:**
- Thumbs up/down em cada memória surfada
- ±5% weight adjustment por feedback
- Sistema melhora com uso

**Insight chave:**
> "This is a way to build relevant context on the fly... gives you in effect the ability to remember something."

---

## Jornada de Construção: Por Onde Começar

Baseado na evolução do JFDI System, uma ordem recomendada:

### Semana 1-2: Fundação
```
1. Chat funcionando (Claude Code ou API direta)
2. Persistência básica (salvar conversas)
3. Primeiros slash commands simples
```

**O que Hillman tinha:** Claude Code + arquivos markdown + comandos básicos

### Semana 3-4: Audit Trail + Dashboard
```
1. Cada comando gera arquivo de auditoria
2. Morning overview automático
3. Integração com calendário
```

**Insight:** O audit trail começa a gerar valor quase imediatamente. Não precisa de nada sofisticado.

### Semana 5-6: Relacionamentos + Projetos
```
1. Arquivos markdown para pessoas
2. Sistema básico de projetos
3. Conexões entre entidades
```

### Semana 7-8: Memória Avançada
```
1. Sessões salvas em banco
2. Extração de memórias
3. Embeddings e busca semântica
4. Hooks para injeção de contexto
```

**Insight chave:**
> "You can get so much value out of this without vector search. Don't let people tell you that you need fancy databases with vector search to get the power."

---

## Decisões de Infraestrutura

### Princípio fundamental: Conexão direta com modelos de ponta

> **"Não quero me distanciar de modelos de ponta (Claude Opus, Sonnet, Haiku) pois eles evoluem rapidamente. Quero que meu app se mova rapidamente em termos de incorporar novas funcionalidades advindas de novos modelos."**

Isso significa:
- **Sem frameworks intermediários** - LangChain, CrewAI, n8n criam rigidez
- **API direta** - Quando Anthropic lançar algo novo, uso no dia seguinte
- **Código próprio** - Controle total sobre como usar os recursos

### Validação do Hillman

Hillman usa **Claude Code Headless Mode** para tudo:
> "I am not hitting Anthropic's API directly for anything. Everything is going through Claude Code using Claude Code headless mode."

**Vantagem:** Session ID permite continuar conversas, compactar contexto, etc.

### Por que essa decisão

**Exemplo concreto:** Claude lançou "extended thinking" recentemente. Com framework, teria que esperar atualização. Com API direta, uso imediatamente.

### Conceitos úteis extraídos da pesquisa

| Conceito | Origem | Como usar |
|----------|--------|-----------|
| **Memória hierárquica L0/L1/L2** | Second-Me | Camadas de contexto para Claude |
| **Bidirectional links** | Logseq | Relações que vão nos dois sentidos no BD |
| **Daily capture** | Logseq | Interface de entrada rápida por dia |
| **Proatividade via scheduler** | Limitless | Sistema que me procura |
| **Processamento background** | Ideia original | Digestão automática de conteúdos |
| **Audit trails** | JFDI System | Cada ação documentada = aprendizado |
| **Energy types** | JFDI System | Classificar tarefas por tipo de energia |
| **Entity resolution** | JFDI System | Detectar pessoas/projetos mencionados |

---

## Arquitetura Técnica

### Visão geral do sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI BRAIN                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    CAMADA DE ENTRADA                        │   │
│  │                                                             │   │
│  │   [Telegram]  [WhatsApp]  [Web App]  [Áudio]  [Imagem]     │   │
│  │        │          │           │         │         │         │   │
│  │        └──────────┴─────┬─────┴─────────┴─────────┘         │   │
│  │                         │                                   │   │
│  │                         ▼                                   │   │
│  │              [API Gateway / FastAPI]                        │   │
│  │                                                             │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            │                                       │
│  ┌─────────────────────────▼───────────────────────────────────┐   │
│  │                 CAMADA DE INTELIGÊNCIA                      │   │
│  │                                                             │   │
│  │   ┌─────────────────────────────────────────────────────┐   │   │
│  │   │              CLAUDE API (DIRETO)                    │   │   │
│  │   │                                                     │   │   │
│  │   │   • Opus para raciocínio complexo                   │   │   │
│  │   │   • Sonnet para tarefas do dia-a-dia                │   │   │
│  │   │   • Haiku para classificação rápida                 │   │   │
│  │   │                                                     │   │   │
│  │   │   Sem framework. Sem abstração. Direto na API.      │   │   │
│  │   └─────────────────────────────────────────────────────┘   │   │
│  │                         │                                   │   │
│  │   ┌─────────────────────▼─────────────────────────────┐     │   │
│  │   │           MOTOR DE DECISÃO                        │     │   │
│  │   │                                                   │     │   │
│  │   │   • Entender intenção da mensagem                 │     │   │
│  │   │   • Identificar projeto/área relacionada          │     │   │
│  │   │   • Identificar entidades (pessoas, projetos)     │     │   │
│  │   │   • Decidir ação: anotar? tarefa? lembrar?        │     │   │
│  │   │   • Conectar com contexto existente               │     │   │
│  │   │                                                   │     │   │
│  │   └───────────────────────────────────────────────────┘     │   │
│  │                                                             │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            │                                       │
│  ┌─────────────────────────▼───────────────────────────────────┐   │
│  │                   CAMADA DE MEMÓRIA                         │   │
│  │                                                             │   │
│  │   ┌─────────────────┐    ┌─────────────────────────────┐   │   │
│  │   │   PostgreSQL    │    │      Vector DB              │   │   │
│  │   │  (estruturado)  │    │   (busca semântica)         │   │   │
│  │   │                 │    │                             │   │   │
│  │   │ • Projetos      │    │ • Embeddings de conteúdo    │   │   │
│  │   │ • Tarefas       │    │ • Busca por similaridade    │   │   │
│  │   │ • Pessoas       │    │ • "aquela ideia sobre X"    │   │   │
│  │   │ • Relações      │    │                             │   │   │
│  │   │ • Histórico     │    │                             │   │   │
│  │   │ • Sessões       │    │                             │   │   │
│  │   │ • Memórias      │    │                             │   │   │
│  │   └─────────────────┘    └─────────────────────────────┘   │   │
│  │                                                             │   │
│  │   ┌─────────────────────────────────────────────────────┐   │   │
│  │   │           MEMÓRIA HIERÁRQUICA                       │   │   │
│  │   │                                                     │   │   │
│  │   │   L0 - Curto prazo: últimas interações, contexto    │   │   │
│  │   │   L1 - Médio prazo: padrões, preferências recentes  │   │   │
│  │   │   L2 - Longo prazo: identidade, valores, história   │   │   │
│  │   │                                                     │   │   │
│  │   │   + Memory Lane: memórias extraídas de sessões      │   │   │
│  │   │   Injetado no contexto do Claude conforme relevante │   │   │
│  │   └─────────────────────────────────────────────────────┘   │   │
│  │                                                             │   │
│  │   ┌─────────────────────────────────────────────────────┐   │   │
│  │   │           AUDIT TRAIL                               │   │   │
│  │   │                                                     │   │   │
│  │   │   • Cada ação gera documentação                     │   │   │
│  │   │   • Decisões e alternativas consideradas            │   │   │
│  │   │   • Base para síntese semanal de padrões            │   │   │
│  │   │   • Alimenta recomendações de melhorias             │   │   │
│  │   └─────────────────────────────────────────────────────┘   │   │
│  │                                                             │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            │                                       │
│  ┌─────────────────────────▼───────────────────────────────────┐   │
│  │                 CAMADA DE PROATIVIDADE                      │   │
│  │                                                             │   │
│  │   ┌─────────────────┐    ┌─────────────────────────────┐   │   │
│  │   │   Scheduler     │    │   Processador de Conteúdo   │   │   │
│  │   │   (Cron jobs)   │    │   (Background workers)      │   │   │
│  │   │                 │    │                             │   │   │
│  │   │ • Morning brief │    │ • Buscar posts do Nate      │   │   │
│  │   │ • Check-ins     │    │ • Processar newsletters     │   │   │
│  │   │ • Lembretes     │    │ • Gerar resumo diário       │   │   │
│  │   │ • Follow-ups    │    │ • Identificar conexões      │   │   │
│  │   │ • Síntese       │    │ • Extrair memórias          │   │   │
│  │   └─────────────────┘    └─────────────────────────────┘   │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Stack tecnológica definida

| Componente | Tecnologia | Justificativa |
|------------|------------|---------------|
| **Backend** | Python + FastAPI | Simples, rápido, boa integração com AI |
| **AI** | Claude API direto | Modelos de ponta, sem intermediários |
| **BD estruturado** | PostgreSQL | Robusto, relações complexas, JSON nativo |
| **BD vetorial** | pgvector (extensão PostgreSQL) | Mesmo banco, menos complexidade |
| **Embeddings** | Ollama (local) | Sem dependência de API externa |
| **Interface inicial** | Telegram Bot | Rápido de implementar, mobile-ready |
| **Scheduler** | Celery + Redis | Jobs em background, confiável |
| **Hosting** | Render ou Railway | Deploy simples, escala fácil |
| **Transcrição** | Whisper API ou Deepgram | Áudio → texto |

### Referência: Stack do JFDI System

| Componente | Tecnologia usada |
|------------|------------------|
| **Core** | Claude Code (headless mode) |
| **UI** | Web app custom (mobile-first) |
| **BD** | Supabase (PostgreSQL) |
| **Vetorial** | PG Vector |
| **Embeddings** | Ollama (local) |
| **Hooks** | Claude Code hooks (user_prompt_submit, tool_use) |

---

## Modelo de Dados

### Entidades principais

```sql
-- Projetos e áreas da vida
CREATE TABLE projetos (
    id UUID PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT,
    area TEXT, -- 'trabalho', 'saude', 'pessoal', 'negocios'
    status TEXT DEFAULT 'ativo',
    pai_id UUID REFERENCES projetos(id), -- hierarquia
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

-- Registros (notas, ideias, informações)
CREATE TABLE registros (
    id UUID PRIMARY KEY,
    conteudo TEXT NOT NULL,
    tipo TEXT, -- 'ideia', 'nota', 'decisao', 'aprendizado'
    fonte TEXT, -- 'telegram', 'web', 'audio', 'processamento'
    embedding VECTOR(1536), -- para busca semântica
    criado_em TIMESTAMP DEFAULT NOW(),
    metadata JSONB -- dados extras flexíveis
);

-- Relação muitos-para-muitos: registro <-> projeto
CREATE TABLE registro_projeto (
    registro_id UUID REFERENCES registros(id),
    projeto_id UUID REFERENCES projetos(id),
    relevancia FLOAT DEFAULT 1.0, -- quão relevante é essa conexão
    PRIMARY KEY (registro_id, projeto_id)
);

-- Tarefas e compromissos
CREATE TABLE tarefas (
    id UUID PRIMARY KEY,
    titulo TEXT NOT NULL,
    descricao TEXT,
    projeto_id UUID REFERENCES projetos(id),
    status TEXT DEFAULT 'pendente', -- 'pendente', 'em_progresso', 'concluida'
    prioridade INTEGER DEFAULT 2, -- 1=alta, 2=media, 3=baixa
    energy_type TEXT, -- 'quick_win', 'creative', 'deep_work', 'admin'
    data_limite TIMESTAMP,
    lembrar_em TIMESTAMP, -- quando o sistema deve me lembrar
    criado_em TIMESTAMP DEFAULT NOW(),
    concluido_em TIMESTAMP
);

-- Pessoas/contatos relevantes
CREATE TABLE pessoas (
    id UUID PRIMARY KEY,
    nome TEXT NOT NULL,
    contexto TEXT, -- 'colega', 'mentor', 'cliente', 'amigo'
    notas TEXT,
    ultimo_contato TIMESTAMP,
    metadata JSONB -- email, telefone, etc
);

-- Relação pessoa <-> projeto
CREATE TABLE pessoa_projeto (
    pessoa_id UUID REFERENCES pessoas(id),
    projeto_id UUID REFERENCES projetos(id),
    papel TEXT, -- 'responsavel', 'colaborador', 'stakeholder'
    PRIMARY KEY (pessoa_id, projeto_id)
);

-- Conteúdos externos processados
CREATE TABLE conteudos_externos (
    id UUID PRIMARY KEY,
    fonte TEXT NOT NULL, -- 'nate_substack', 'seth_blog', etc
    titulo TEXT,
    url TEXT,
    conteudo_original TEXT,
    resumo TEXT, -- gerado pelo Claude
    conexoes_identificadas JSONB, -- projetos relacionados
    embedding VECTOR(1536),
    processado_em TIMESTAMP DEFAULT NOW()
);

-- Sessões de chat (Memory Lane)
CREATE TABLE sessoes (
    id UUID PRIMARY KEY,
    transcript_completo JSONB,
    primeira_mensagem TEXT,
    ultima_mensagem TEXT,
    mensagens_usuario TEXT[], -- array de mensagens do usuário
    mensagens_agente TEXT[], -- array de respostas do agente
    arquivos_tocados TEXT[],
    tool_calls JSONB,
    tipo_trabalho TEXT, -- 'tecnico', 'criativo', 'comunicacao', etc
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

-- Memórias extraídas (Memory Lane)
CREATE TABLE memorias (
    id UUID PRIMARY KEY,
    sessao_id UUID REFERENCES sessoes(id),
    tipo TEXT, -- 'decisao', 'insight', 'padrao', 'compromisso', 'aprendizado', 'correcao', 'workflow', 'gap'
    resumo TEXT,
    reasoning TEXT, -- por que essa memória foi capturada
    contexto_original TEXT, -- chunk do transcript
    confidence_score FLOAT,
    entidades_relacionadas TEXT[], -- pessoas, projetos, arquivos
    embedding VECTOR(1536),
    formada_em TIMESTAMP, -- quando aconteceu originalmente
    salva_em TIMESTAMP DEFAULT NOW()
);

-- Feedback de memórias
CREATE TABLE memoria_feedback (
    id UUID PRIMARY KEY,
    memoria_id UUID REFERENCES memorias(id),
    sessao_id UUID REFERENCES sessoes(id), -- em qual sessão foi surfada
    query_que_surfou TEXT,
    util BOOLEAN, -- thumbs up/down
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Audit trails
CREATE TABLE audits (
    id UUID PRIMARY KEY,
    data DATE,
    agente TEXT, -- qual agente/comando executou
    acoes_tomadas JSONB,
    decisoes JSONB,
    opcoes_consideradas JSONB,
    arquivos_criados TEXT[],
    cross_agent_notes TEXT,
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Interações (histórico de conversas)
CREATE TABLE interacoes (
    id UUID PRIMARY KEY,
    mensagem_usuario TEXT,
    resposta_sistema TEXT,
    contexto_usado JSONB, -- que memórias foram usadas
    acao_executada TEXT, -- que ação o sistema tomou
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Lembretes proativos
CREATE TABLE lembretes (
    id UUID PRIMARY KEY,
    tipo TEXT, -- 'checkin_projeto', 'followup_tarefa', 'lembrete_custom'
    referencia_id UUID, -- id do projeto/tarefa relacionado
    referencia_tipo TEXT, -- 'projeto', 'tarefa', 'pessoa'
    mensagem TEXT,
    disparar_em TIMESTAMP,
    disparado BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT NOW()
);
```

---

## Memória Hierárquica (L0/L1/L2) + Memory Lane

### Conceito adaptado do Second-Me + JFDI System

Em vez de fine-tuning (que limitaria ao modelo pequeno), implementamos como **camadas de contexto** injetadas no prompt do Claude.

```
┌─────────────────────────────────────────────────────────────┐
│                    PROMPT PARA CLAUDE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  <system>                                                   │
│  Você é o AI Brain do Ale, um parceiro digital que...      │
│  </system>                                                  │
│                                                             │
│  <memoria_l2_identidade>                                    │
│  # Quem é o Ale                                             │
│  - Trabalhador de hotel buscando criar negócio próprio     │
│  - Filosofia: eliminar desperdício sistêmico               │
│  - Valores: fazer os outros brilharem, autonomia           │
│  - Projetos principais: AI Brain, Sistema Hospitalidade    │
│  - Mentores/influências: Seth Godin, Nate, Derek Sivers    │
│  </memoria_l2_identidade>                                   │
│                                                             │
│  <memoria_l1_contexto_recente>                              │
│  # Últimas semanas                                          │
│  - Pesquisando mercado de AI assistants                    │
│  - Decidiu construir do zero (sem frameworks)              │
│  - Começando a documentar jornada publicamente             │
│  - Estado emocional: motivado, fase de clareza             │
│  </memoria_l1_contexto_recente>                             │
│                                                             │
│  <memoria_l0_sessao_atual>                                  │
│  # Hoje                                                     │
│  - Analisamos Logseq, Second-Me, JFDI System               │
│  - Definindo arquitetura técnica                           │
│  - Próximo: começar implementação                          │
│  </memoria_l0_sessao_atual>                                 │
│                                                             │
│  <memorias_relevantes>                                      │
│  # Memórias recuperadas (Memory Lane)                       │
│  [Decisão 2025-12-28] Preferência por Haiku para...        │
│  [Correção 2025-12-30] Não usar framework X porque...      │
│  [Padrão identificado] Ale trabalha melhor de manhã...     │
│  </memorias_relevantes>                                     │
│                                                             │
│  <contexto_relevante>                                       │
│  [Resultados de busca semântica relacionados à mensagem]   │
│  </contexto_relevante>                                      │
│                                                             │
│  <mensagem_usuario>                                         │
│  [Mensagem atual do Ale]                                    │
│  </mensagem_usuario>                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Como cada camada é alimentada

| Camada | Fonte | Atualização |
|--------|-------|-------------|
| **L0** | Últimas mensagens da sessão | Em tempo real |
| **L1** | Síntese das últimas semanas | Diária ou semanal |
| **L2** | Perfil consolidado | Manual ou mensal |
| **Memory Lane** | Extração automática de sessões | A cada 15 min |

---

## Componentes a Implementar

### Fase 1: MVP funcional (Semanas 1-2)

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **Bot Telegram** | Receber mensagens, responder | Alta |
| **API básica** | FastAPI com endpoints essenciais | Alta |
| **BD PostgreSQL** | Schema inicial, conexão | Alta |
| **Integração Claude** | Chamadas à API, prompts | Alta |
| **Registro de notas** | Salvar o que Ale manda | Alta |
| **Audit trail básico** | Cada ação gera documentação | Alta |

**Entregável:** Posso mandar mensagem, Claude entende, salva no banco, gera audit, responde.

### Fase 2: Memória e contexto (Semanas 3-4)

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **pgvector** | Embeddings e busca semântica | Alta |
| **Sistema de contexto** | Montar L0/L1/L2 pro Claude | Alta |
| **Projetos** | CRUD de projetos, relações | Média |
| **Busca semântica** | "aquela ideia sobre X" | Média |
| **Morning overview** | Dashboard diário automático | Média |

**Entregável:** Claude "lembra" de conversas anteriores e encontra informações relacionadas.

### Fase 3: Relacionamentos e Síntese (Semanas 5-6)

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **Pessoas** | Arquivos/registros por pessoa | Média |
| **Síntese semanal** | Análise de padrões dos audits | Média |
| **Entity resolution** | Detectar pessoas/projetos mencionados | Média |
| **Conexões automáticas** | Ligar registros a entidades | Média |

**Entregável:** Sistema entende quem são as pessoas na minha vida e sugere conexões.

### Fase 4: Proatividade (Semanas 7-8)

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **Celery + Redis** | Jobs em background | Média |
| **Check-ins** | Sistema me procura | Média |
| **Processamento conteúdo** | RSS, newsletters | Média |
| **Lembretes** | Baseado em contexto | Média |
| **Memory Lane** | Extração automática de memórias | Média |

**Entregável:** Sistema me procura, processa conteúdos automaticamente, lembra de contexto.

### Fase 5: Refinamento (Semanas 9+)

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **Tarefas com energy type** | Sistema de tasks com classificação | Baixa |
| **Now View** | O que fazer agora baseado em energia | Baixa |
| **Web dashboard** | Visualizar tudo | Baixa |
| **Multi-interface** | WhatsApp, app próprio | Baixa |
| **Prep de reuniões** | Automático baseado em calendário | Baixa |

---

## O que vai precisar (atualizado)

### Infraestrutura
- [ ] Conta API Claude (plano Teams ou superior)
- [ ] Servidor: Render ou Railway (starter ~$7/mês)
- [ ] PostgreSQL: Render managed ($7/mês) ou Supabase (free tier)
- [ ] Redis: Render ou Upstash (free tier pra começar)
- [ ] Ollama (local) para embeddings

### Desenvolvimento
- [ ] Repositório GitHub
- [ ] Ambiente Python com FastAPI
- [ ] Bot Telegram criado (@BotFather)
- [ ] Variáveis de ambiente configuradas
- [ ] Claude Code instalado (para hooks e headless mode)

### Estimativa de custo mensal inicial
| Item | Custo |
|------|-------|
| Claude API | ~$20-50 (dependendo do uso) |
| Servidor | ~$7 |
| Banco de dados | $0-7 |
| Redis | $0 |
| **Total** | **~$30-65/mês** |

---

## Framework de Construção + Captura

### Princípio fundamental

> **"Tudo que eu fizer tem que gerar material pra que possa futuramente ser feito por agente."**

Cada hora de trabalho gera valor em três dimensões:
1. **O resultado** - o agente, o sistema, a funcionalidade
2. **O conteúdo** - material para marca pessoal (YouTube, blog, etc)
3. **A automação futura** - instrução para agente replicar o processo

### Validação do JFDI System

Hillman descobriu que ~1/3 das features novas vieram de sugestões do próprio sistema:
> "I don't know what the percentage is. I could probably ask it. If I had to ballpark it, it's probably somewhere near a third where it's like, hey, if we built this feature or we updated this feature in this way, this problem would go away."

### Fluxo de captura

```
[Eu faço manualmente]
       │
       ▼
[Audit trail documenta o processo]
       │
       ▼
[Síntese semanal identifica padrões]
       │
       ▼
[Sistema sugere automações]
       │
       ▼
[Material vira conteúdo (YouTube, etc)]
       │
       ▼
[Agente replica o processo]
```

---

## Próximos passos

### Imediato (próximas sessões)
1. **Validar arquitetura** - Revisar se faz sentido, ajustar
2. **Criar repositório** - GitHub, estrutura de pastas
3. **Setup inicial** - FastAPI rodando, conexão com Claude funcionando
4. **Bot Telegram** - Receber mensagem, responder com Claude
5. **Audit trail** - Cada interação gera documentação

### Curto prazo (Fase 1 - MVP)
6. **PostgreSQL** - Schema básico funcionando
7. **Fluxo completo** - Mensagem → Claude → Salva → Audit → Responde
8. **Primeiro deploy** - Render rodando 24/7

### Médio prazo (Fase 2 - Memória)
9. **pgvector** - Busca semântica funcionando
10. **Sistema de contexto L0/L1/L2** - Claude com memória
11. **Morning overview** - Dashboard diário automático
12. **Projetos** - CRUD básico, relações com registros

### Longo prazo (Fase 3+ - Proatividade)
13. **Background jobs** - Celery + Redis
14. **Síntese semanal** - Padrões nos audit trails
15. **Memory Lane** - Extração automática de memórias
16. **Check-ins** - Sistema me procura
17. **Processamento de conteúdo** - RSS, newsletters automáticos

---

## Conexão com marca pessoal

Documentar publicamente a construção deste sistema:
- Os problemas que estou resolvendo
- As descobertas e os erros
- O processo de aprender IA construindo
- Inspiração: vídeos de restauração de caminhão (acompanhar o processo, não só o resultado)

> "Eu tenho objetivo de construir negócio. Eu acho que inteligência artificial pode ser o caminho. E eu vou mostrar eu procurando esse caminho."

---

## Apêndice: Quotes importantes do JFDI System

### Sobre o problema que resolve
> "Every project management tool I've ever used had the same problem - what it expects from me. I'm the worst at going in and keeping them current."

### Sobre proatividade
> "The dream of an assistant who you wake up in the morning and your day is prepared for you."

### Sobre memória simples
> "You can get so much value out of this without vector search. Don't let people tell you that you need fancy databases with vector search to get the power."

### Sobre transparência
> "Trust through transparency - I design things to provide me maximum transparency and then as a byproduct that transparency becomes value to both me and the system."

### Sobre o impacto
> "Has already had a materially positive impact on my life, my productivity, my happiness. Most importantly, my executive function."

### Sobre documentação gerando SOPs
> "Almost everything of meaning that this system does is basically a giant SOP or collection of SOPs. And I found that it's very very good at writing instructions better than I've ever been."

---

*Documento vivo - será atualizado conforme novas ideias surgirem*

*v0.2 - Enriquecido com insights do JFDI System (Alex Hillman)*
