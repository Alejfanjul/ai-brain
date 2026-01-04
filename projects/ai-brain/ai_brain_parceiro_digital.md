# AI Brain - Parceiro Digital Pessoal

**Data:** 03/01/2026 (atualizado)  
**Status:** Em concepção - arquitetura definida

---

## Visão Geral

Um parceiro digital que sabe absolutamente tudo da minha vida. Não é assistente que executa comandos - é parceiro que entende contexto, conecta ideias, distribui informação e me relembra do que precisa ser relembrado.

### Princípio central
> "Ferramenta que cria o cenário ideal pra que você possa dar vazão a todas as ideias, potencial, vontades e objetivos que você tem na vida - de forma organizada e estruturada."

O AI Brain é um parceiro que trabalha junto comigo pra otimizar e aproveitar melhor minha energia. Ele entende contexto, propõe, acompanha, aprende.

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

## Modelagem Conceitual

### Entidades principais

```
[A definir com mais contribuições do Ale]

Candidatas iniciais:
- Projeto
- Nota / Registro
- Tarefa / Compromisso
- Lembrete
- Pessoa / Contato
- Conversa / Interação
- Área da vida (trabalho, saúde, pessoal, etc.)
```

### Relações entre entidades

```
[A definir]

Perguntas a responder:
- Um registro pode pertencer a múltiplos projetos?
- Como categorizar áreas da vida vs projetos?
- Como conectar pessoas a projetos/tarefas?
- Como o sistema sabe quando me lembrar de algo?
```

### Ações que o sistema executa

```
[A definir com exemplos concretos do Ale]

Candidatas:
- Anotar informação em projeto
- Criar tarefa com prazo
- Criar lembrete contextual
- Buscar informação relacionada
- Resumir estado de um projeto
- Conectar ideias de projetos diferentes
```

---

## Casos de uso concretos

### Caso 1: Treino físico
**Hoje:** Ale precisa procurar a conversa certa entre centenas, informar performance, receber próximo treino baseado no plano.

**Com AI Brain:** Ale fala "fiz o treino de hoje, consegui 3 séries de 10 no supino com 40kg, senti o ombro um pouco". O sistema já sabe qual é o plano, registra a performance, ajusta o próximo treino, e se o ombro continuar incomodando, lembra de mencionar isso.

### Caso 2: Ideias durante o dia
**Hoje:** Ale tem uma ideia, anota em algum lugar (ou esquece), depois precisa lembrar onde anotou e conectar com o projeto certo.

**Com AI Brain:** Ale fala a ideia. O sistema identifica que se relaciona com o projeto X, anota lá, e ainda conecta: "isso me lembra daquela outra ideia que você teve em novembro sobre Y".

### Caso 3: Preparação para reunião
**Hoje:** Ale precisa lembrar o que foi discutido da última vez, o que ficou pendente, quem são as pessoas envolvidas.

**Com AI Brain:** Ale fala "vou ter reunião com o Denis amanhã sobre o sistema de OS". O sistema puxa: últimas decisões, pendências, contexto relevante, e prepara um resumo.

### Caso 4: Digestão diária de conteúdo
**Hoje:** Ale tem conteúdos salvos de várias fontes (Nate, Seth Godin, Bruno Fajão, etc). Precisa ler cada um, lembrar de ler, conectar manualmente com seus projetos.

**Com AI Brain:** Todo dia, o sistema já processou os novos conteúdos. Apresenta resumo de 3 minutos: "Hoje o Nate falou sobre X - isso conecta com sua ideia de sistema social. O Seth publicou sobre Y - relevante pro posicionamento do AI Brain." Tudo encadeado, sem eu pedir.

### Caso 5: Visão integrada do negócio
**Hoje:** Ale tem várias ideias, projetos, referências espalhadas. Difícil ver como tudo se conecta.

**Com AI Brain:** O sistema conhece todos os conteúdos, todas as ideias, todos os projetos. Consegue mostrar: "Olha como essas três coisas se conectam", dando segurança pra entender como a ideia de negócio está se formando e como as partes estão se amarrando.

---

## Funcionalidades desejadas

*[Espaço para Ale adicionar mais ideias]*

- 
- 
- 

---

## Questões em aberto

### Conceituais
- Como o sistema decide a qual projeto uma mensagem pertence?
- O que acontece quando uma informação é relevante pra múltiplos projetos?
- Como lidar com informação que não se encaixa em nenhum projeto existente?
- Como o sistema aprende minhas preferências de organização?

### Técnicas (para depois)
- Interface: app próprio vs Telegram vs WhatsApp vs múltiplos
- Armazenamento: SQL para estruturado + Vector DB para busca semântica
- Processamento: Claude como cérebro central
- Velocidade de resposta vs profundidade de análise

---

## Análise de Mercado

### Categoria emergente: AI Personal Assistants com memória

Existem três categorias de produtos convergindo:

| Categoria | Exemplos | Limitação |
|-----------|----------|-----------|
| **Second Brain / PKM** | Notion, Obsidian, Logseq | Organização manual, não proativo |
| **AI Assistants** | Lindy, Notion AI, Copilot | Tarefas pontuais, sem memória longa |
| **Memory Assistants** | Limitless, Personal.ai, Second-Me | Digital twin OU memória, não parceiro |

### Produtos analisados

**Limitless (ex-Rewind):** Pendant que grava conversas, transcreve, busca ($99-399). Pivotou de app pra wearable. Indica que captura passiva + AI é o futuro.

**Personal.ai:** Digital twin que fala na sua voz. Foco em replicar você, não em ser parceiro.

**Second-Me:** Open source para criar digital twin local. Usa modelos pequenos (Qwen 1B), memória hierárquica L0/L1/L2. Conceito interessante, execução limitada por capacidade dos modelos.

**Logseq:** Ferramenta de PKM com outliner + grafo. Excelente para organização manual, mas não é proativo. Plugins de AI são add-ons, não core.

### Gap identificado - O que ninguém faz bem

| O que o mercado faz | O que eu quero |
|---------------------|----------------|
| Gravam e transcrevem | Processam proativamente |
| Organizam o que você põe | Encadeiam automaticamente |
| Respondem quando pergunta | Me procuram na hora certa |
| Focam memória OU tarefas | Integram vida + projetos + conteúdos |
| São ferramentas | Parceiro que entende contexto emocional |

### Por que construir do zero

| Fator | Usar produto existente | Construir do zero |
|-------|------------------------|-------------------|
| Velocidade inicial | Mais rápido | Mais lento |
| Flexibilidade longo prazo | Limitada | **Total** |
| Dependência externa | Alta | **Nenhuma** |
| Aproveitamento evolução AI | Depende do produto | **Máximo** |
| Alinhamento com filosofia | Compromissos | **Perfeito** |

---

## Decisões de Infraestrutura

### Princípio fundamental: Conexão direta com modelos de ponta

> **"Não quero me distanciar de modelos de ponta (Claude Opus, Sonnet, Haiku) pois eles evoluem rapidamente. Quero que meu app se mova rapidamente em termos de incorporar novas funcionalidades advindas de novos modelos."**

Isso significa:
- **Sem frameworks intermediários** - LangChain, CrewAI, n8n criam rigidez
- **API direta** - Quando Anthropic lançar algo novo, uso no dia seguinte
- **Código próprio** - Controle total sobre como usar os recursos

### Por que essa decisão

**Exemplo concreto:** Claude lançou "extended thinking" recentemente. Com framework, teria que esperar atualização. Com API direta, uso imediatamente.

**O mercado está fazendo errado:**
- Second-Me usa modelo local pequeno (1B params) → perde capacidade cognitiva
- Produtos que abstraem a AI → ficam presos na versão do dia do lançamento
- Frameworks que "facilitam" → criam dependência e limitação

### Conceitos úteis extraídos da pesquisa

Mesmo construindo do zero, esses conceitos são valiosos:

| Conceito | Origem | Como usar |
|----------|--------|-----------|
| **Memória hierárquica L0/L1/L2** | Second-Me | Camadas de contexto para Claude |
| **Bidirectional links** | Logseq | Relações que vão nos dois sentidos no BD |
| **Daily capture** | Logseq | Interface de entrada rápida por dia |
| **Proatividade via scheduler** | Limitless | Sistema que me procura |
| **Processamento background** | Ideia original | Digestão automática de conteúdos |

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
│  │                         │                                   │   │
│  │   ┌─────────────────────▼─────────────────────────────┐     │   │
│  │   │           MOTOR DE DECISÃO                        │     │   │
│  │   │                                                   │     │   │
│  │   │   • Entender intenção da mensagem                 │     │   │
│  │   │   • Identificar projeto/área relacionada          │     │   │
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
│  │   └─────────────────┘    └─────────────────────────────┘   │   │
│  │                                                             │   │
│  │   ┌─────────────────────────────────────────────────────┐   │   │
│  │   │           MEMÓRIA HIERÁRQUICA                       │   │   │
│  │   │                                                     │   │   │
│  │   │   L0 - Curto prazo: últimas interações, contexto    │   │   │
│  │   │   L1 - Médio prazo: padrões, preferências recentes  │   │   │
│  │   │   L2 - Longo prazo: identidade, valores, história   │   │   │
│  │   │                                                     │   │   │
│  │   │   Injetado no contexto do Claude conforme relevante │   │   │
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
│  │   │ • Check-ins     │    │ • Buscar posts do Nate      │   │   │
│  │   │ • Lembretes     │    │ • Processar newsletters     │   │   │
│  │   │ • Follow-ups    │    │ • Gerar resumo diário       │   │   │
│  │   │ • Revisões      │    │ • Identificar conexões      │   │   │
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
| **Interface inicial** | Telegram Bot | Rápido de implementar, mobile-ready |
| **Scheduler** | Celery + Redis | Jobs em background, confiável |
| **Hosting** | Render ou Railway | Deploy simples, escala fácil |
| **Transcrição** | Whisper API ou Deepgram | Áudio → texto |

### Por que PostgreSQL + pgvector (não Baserow)

| Aspecto | Baserow | PostgreSQL direto |
|---------|---------|-------------------|
| Controle | Interface limita | **Total** |
| Performance | OK para pouco dado | **Escala** |
| Queries complexas | Limitado | **SQL completo** |
| Vector search | Não tem | **pgvector nativo** |
| Relações | Básico | **Completo** |
| Migrations | Manual | **Automático** |

Baserow é bom pra protótipos rápidos, mas para o AI Brain que vai crescer e ter queries complexas, PostgreSQL direto dá mais poder.

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

### Relações bidirecionais (conceito do Logseq)

O modelo permite descobrir conexões nos dois sentidos:

```sql
-- Dado um projeto, encontrar todos os registros
SELECT r.* FROM registros r
JOIN registro_projeto rp ON r.id = rp.registro_id
WHERE rp.projeto_id = 'uuid-do-projeto';

-- Dado um registro, encontrar todos os projetos relacionados
SELECT p.* FROM projetos p
JOIN registro_projeto rp ON p.id = rp.projeto_id
WHERE rp.registro_id = 'uuid-do-registro';

-- Encontrar conexões não óbvias: projetos que compartilham registros
SELECT p1.nome as projeto1, p2.nome as projeto2, COUNT(*) as registros_em_comum
FROM registro_projeto rp1
JOIN registro_projeto rp2 ON rp1.registro_id = rp2.registro_id AND rp1.projeto_id != rp2.projeto_id
JOIN projetos p1 ON rp1.projeto_id = p1.id
JOIN projetos p2 ON rp2.projeto_id = p2.id
GROUP BY p1.nome, p2.nome
ORDER BY registros_em_comum DESC;
```

### Busca semântica (conceito importante)

```sql
-- Buscar registros similares a uma query
-- "aquela ideia sobre gamificação no hotel"

-- 1. Gerar embedding da query via Claude/OpenAI
-- 2. Buscar por similaridade de cosseno

SELECT r.*, 1 - (r.embedding <=> query_embedding) as similaridade
FROM registros r
ORDER BY r.embedding <=> query_embedding
LIMIT 10;
```

---

## Memória Hierárquica (L0/L1/L2)

### Conceito adaptado do Second-Me

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
│  - Analisamos Logseq, Second-Me, mercado                   │
│  - Definindo arquitetura técnica                           │
│  - Próximo: começar implementação                          │
│  </memoria_l0_sessao_atual>                                 │
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

### Vantagem dessa abordagem

- **Não precisa fine-tuning** → usa modelo de ponta sempre
- **Contexto dinâmico** → relevante pra cada conversa
- **Controle total** → você decide o que o Claude "lembra"
- **Evoluível** → quando contexto do Claude aumentar, usa mais

---

## Fluxo de Processamento

### Fluxo 1: Mensagem do usuário

```
[Ale manda mensagem no Telegram]
         │
         ▼
[API recebe mensagem]
         │
         ▼
[Classificação rápida (Haiku)]
    "Que tipo de mensagem é essa?"
    - Pergunta sobre projeto existente?
    - Nova ideia?
    - Tarefa pra criar?
    - Conversa casual?
         │
         ▼
[Busca contexto relevante]
    - Query semântica no Vector DB
    - Últimas interações (L0)
    - Contexto recente (L1)
    - Perfil (L2)
         │
         ▼
[Monta prompt com contexto]
         │
         ▼
[Claude (Sonnet) processa]
    - Entende intenção
    - Decide ações
    - Gera resposta
         │
         ▼
[Executa ações]
    - Salva registro no BD
    - Cria tarefa se necessário
    - Agenda lembrete se necessário
    - Conecta com projetos relevantes
         │
         ▼
[Responde ao usuário]
         │
         ▼
[Registra interação no histórico]
```

### Fluxo 2: Processamento de conteúdo externo (background)

```
[Scheduler dispara: "hora de buscar conteúdo"]
         │
         ▼
[Worker busca novas publicações]
    - RSS do Nate
    - Blog do Seth
    - Newsletters configuradas
         │
         ▼
[Para cada conteúdo novo]
         │
         ▼
[Claude (Sonnet) processa]
    - Resume o conteúdo
    - Identifica temas principais
    - Busca conexões com projetos do Ale
         │
         ▼
[Salva no BD]
    - Conteúdo original
    - Resumo
    - Embedding
    - Conexões identificadas
         │
         ▼
[Se conexão forte com projeto ativo]
         │
         ▼
[Agenda notificação pro Ale]
    "O Nate publicou algo relevante pro AI Brain"
```

### Fluxo 3: Proatividade - Check-in de projeto

```
[Scheduler dispara: "check-in do projeto X"]
         │
         ▼
[Busca estado do projeto]
    - Última atualização
    - Tarefas pendentes
    - Registros recentes
         │
         ▼
[Claude (Sonnet) analisa]
    - Projeto está parado há muito tempo?
    - Tem tarefa atrasada?
    - Houve progresso?
         │
         ▼
[Gera mensagem de check-in]
    Contextual, não genérica
         │
         ▼
[Envia pro Ale no Telegram]
    "Faz 5 dias que não falamos do AI Brain.
     Última coisa foi definir arquitetura.
     Quer continuar de onde paramos?"
```

---

## Componentes a Implementar

### Fase 1: MVP funcional

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **Bot Telegram** | Receber mensagens, responder | Alta |
| **API básica** | FastAPI com endpoints essenciais | Alta |
| **BD PostgreSQL** | Schema inicial, conexão | Alta |
| **Integração Claude** | Chamadas à API, prompts | Alta |
| **Registro de notas** | Salvar o que Ale manda | Alta |

**Entregável:** Posso mandar mensagem, Claude entende, salva no banco, responde.

### Fase 2: Memória e contexto

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **pgvector** | Embeddings e busca semântica | Alta |
| **Sistema de contexto** | Montar L0/L1/L2 pro Claude | Alta |
| **Projetos** | CRUD de projetos, relações | Média |
| **Busca semântica** | "aquela ideia sobre X" | Média |

**Entregável:** Claude "lembra" de conversas anteriores e encontra informações relacionadas.

### Fase 3: Proatividade

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **Celery + Redis** | Jobs em background | Média |
| **Check-ins** | Sistema me procura | Média |
| **Processamento conteúdo** | RSS, newsletters | Média |
| **Lembretes** | Baseado em contexto | Média |

**Entregável:** Sistema me procura, processa conteúdos automaticamente.

### Fase 4: Refinamento

| Componente | Descrição | Prioridade |
|------------|-----------|------------|
| **Tarefas** | Sistema completo de tasks | Baixa |
| **Pessoas** | Relacionar pessoas a projetos | Baixa |
| **Web dashboard** | Visualizar tudo | Baixa |
| **Multi-interface** | WhatsApp, app próprio | Baixa |

---

## O que vai precisar (atualizado)

### Infraestrutura
- [ ] Conta API Claude (plano Teams ou superior)
- [ ] Servidor: Render ou Railway (starter ~$7/mês)
- [ ] PostgreSQL: Render managed ($7/mês) ou Supabase (free tier)
- [ ] Redis: Render ou Upstash (free tier pra começar)

### Desenvolvimento
- [ ] Repositório GitHub
- [ ] Ambiente Python com FastAPI
- [ ] Bot Telegram criado (@BotFather)
- [ ] Variáveis de ambiente configuradas

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

### Fluxo de captura

```
[Eu faço manualmente]
       │
       ▼
[Documento o processo enquanto faço]
       │
       ▼
[Material vira conteúdo (YouTube, etc)]
       │
       ▼
[Material vira instrução pro agente]
       │
       ▼
[Agente replica o processo]
```

### Método para qualquer tarefa

#### 1. INVESTIGAÇÃO
- O que precisa ser feito?
- Por que isso é necessário?
- Como outros fazem?
- Que alternativas existem?

**Documenta:** Perguntas feitas, respostas encontradas, fontes consultadas

#### 2. DESIGN
- Como vou fazer?
- Que decisões estou tomando?
- Por que essas decisões e não outras?
- Que trade-offs estou aceitando?

**Documenta:** Decisões tomadas e suas razões (o "porquê" é mais importante que o "o quê")

#### 3. EXECUÇÃO
- Passos concretos realizados
- O que funcionou
- O que não funcionou
- Ajustes feitos no caminho
- Comandos, código, configurações

**Documenta:** Processo real, não idealizado. Incluir erros e correções.

#### 4. REFLEXÃO
- O que aprendi?
- O que faria diferente da próxima vez?
- Como automatizar isso?
- Que partes podem virar agente?

**Documenta:** Aprendizados e insights para futuro

### Output de cada tarefa

| Output | Pra quê serve |
|--------|---------------|
| **Resultado** | O trabalho em si (código, sistema, etc) |
| **Conteúdo** | Post, vídeo, thread - marca pessoal |
| **Instrução** | Prompt/spec pra agente replicar |
| **Conhecimento** | Alimenta o próprio AI Brain |

### Por que isso funciona

**Compound effect:** Trabalho uma vez, colho três vezes.

**Documentação natural:** Documenta durante, não depois (que ninguém faz).

**AI Brain se auto-constrói:** Material gerado alimenta o sistema.

**Prova pública:** Conteúdo mostra processo real, não teoria.

**Automação progressiva:** Cada tarefa documentada é candidata a virar agente.

### Aplicação prática

Exemplo: Construir o bot Telegram do AI Brain

| Fase | O que fazer | O que documentar |
|------|-------------|------------------|
| **Investigação** | Pesquisar API Telegram, libs Python | Comparação de opções, prós/contras |
| **Design** | Decidir estrutura, fluxo de mensagens | Diagrama, decisões arquiteturais |
| **Execução** | Codar, testar, debugar | Código comentado, erros encontrados |
| **Reflexão** | O que aprendi, o que automatizar | Insights, prompt pro agente |

**Resultado:** Bot funcionando
**Conteúdo:** "Como construí um bot Telegram com IA em X horas"
**Instrução:** Spec pra agente criar bots similares
**Conhecimento:** Registro no AI Brain sobre Telegram bots

---

## Próximos passos

### Imediato (próximas sessões)
1. **Validar arquitetura** - Ale revisar se faz sentido, ajustar
2. **Criar repositório** - GitHub, estrutura de pastas
3. **Setup inicial** - FastAPI rodando, conexão com Claude funcionando
4. **Bot Telegram** - Receber mensagem, responder com Claude

### Curto prazo (Fase 1 - MVP)
5. **PostgreSQL** - Schema básico funcionando
6. **Fluxo completo** - Mensagem → Claude → Salva → Responde
7. **Primeiro deploy** - Render rodando 24/7

### Médio prazo (Fase 2 - Memória)
8. **pgvector** - Busca semântica funcionando
9. **Sistema de contexto L0/L1/L2** - Claude com memória
10. **Projetos** - CRUD básico, relações com registros

### Longo prazo (Fase 3 - Proatividade)
11. **Background jobs** - Celery + Redis
12. **Check-ins** - Sistema me procura
13. **Processamento de conteúdo** - RSS, newsletters automáticos

---

## Conexão com marca pessoal

Documentar publicamente a construção deste sistema:
- Os problemas que estou resolvendo
- As descobertas e os erros
- O processo de aprender IA construindo
- Inspiração: vídeos de restauração de caminhão (acompanhar o processo, não só o resultado)

> "Eu tenho objetivo de construir negócio. Eu acho que inteligência artificial pode ser o caminho. E eu vou mostrar eu procurando esse caminho."

---

*Documento vivo - será atualizado conforme novas ideias surgirem*