# Knowledge Bases for AI Agents - Best Practices

## Metadata
- **Fonte:** Tutorial em vídeo
- **Tema:** Optimizing Knowledge Bases for AI Agents
- **URL:** https://www.youtube.com/watch?v=w7OGw9-ZXQo
- **Duração:** ~10 min
- **Plataformas:** Voiceflow, VectorShift, Vapi
- **Data extração:** 2025-12-27

## Resumo

Tutorial técnico sobre como otimizar knowledge bases para AI agents (chatbots, voice agents, AI tools). Cobre estruturação de documentos, chunking strategies, diferentes tipos de documentos, query optimization, e comparação entre plataformas (Voiceflow vs VectorShift). Apresenta 7 técnicas práticas para melhorar accuracy de respostas baseadas em knowledge bases.

## Tese Central

> "The most integral part of building advanced AI agents is your knowledge base. A poorly created knowledge base will mean inaccurate answers and pretty confused users. Think of it like a stack of playing cards - the knowledge base is the bottom layer, and without one of these cards, everything comes crashing down."

## Plataformas Analisadas

### Voiceflow

| Aspecto | Detalhe |
|---------|---------|
| **Tipo** | No-code chatbot builder |
| **Knowledge Base** | Built-in, mas "very little functionality and features" |
| **Chunk Control** | Limitado (3-10 chunks por query) |
| **Customização** | Baixa |
| **Uso** | AI Response block que targets knowledge base |
| **Limitação** | Não consegue extrair máximo potencial da knowledge base |

### VectorShift (Sponsor)

| Aspecto | Detalhe |
|---------|---------|
| **Tipo** | Advanced knowledge base platform |
| **Analogia** | "Voiceflow mas specifically targeting the knowledge base" |
| **Chunk Control** | Full customization (size, overlap) |
| **Document Types** | PDF, Word, CSV, Excel, images com OCR |
| **Advanced Features** | Transform query, expand query, hybrid search, multiple questions |
| **Deployment** | API call para integrar com qualquer plataforma |
| **Integração** | Pode ser usado com Voiceflow, Vapi, etc via API |

## Técnica 1: Ajustar Chunk Size e Retrieval Count

### Chunk Count (Voiceflow)

**Configuração:**
- **Default:** 3 chunks por query
- **Máximo:** 10 chunks por query

**Trade-off:**

| Chunks | Custo | Accuracy |
|--------|-------|----------|
| 3 | Menor (menos tokens) | Menor (menos contexto) |
| 10 | Maior (mais tokens) | Maior (mais contexto) |

**Observação do autor:**
> "Ultimately the difference is going to be quite negligible"

**Implicação:** Ajustar chunk count sozinho não resolve o problema fundamental

### Chunk Size (VectorShift)

**Configuração:**
- **Máximo:** ~4,000 characters por chunk
- **Impacto:**
  - Maior chunk size = mais custo (mais tokens no prompt)
  - Maior chunk size = maior accuracy (mais contexto por chunk)

## Técnica 2: Estruturação de Documentos ⭐ **MAIS IMPORTANTE**

### Problema: Chunks Sequenciais Sem Estrutura

**Como funciona atualmente:**
```
Document → Split sequencialmente → Chunks 1, 2, 3, ...
Chunk 1: primeiras X palavras
Chunk 2: próximas X palavras (sequencial)
Chunk 3: próximas X palavras (sequencial)
```

**Problema:**
- Se documento não está bem estruturado, um chunk pode ter:
  - Informação sobre Topic A (início do chunk)
  - Informação sobre Topic B (fim do chunk)
- Quando chunk é retrieved, tem informação **diluída** sobre dois tópicos ao invés de **concentrada** sobre um

### Solução: Estruture Documentos por Relevância

**Princípio:**
> "Structure your documents so that information is relevant as it goes down"

**Boas práticas:**

1. **Agrupe informação relacionada fisicamente no documento**
   - Tópico A: todas as informações juntas
   - Tópico B: todas as informações juntas (separado de A)

2. **Ordem hierárquica**
   - Informações mais gerais primeiro
   - Informações específicas depois
   - Evite pular entre níveis de abstração

3. **Evite misturar tópicos**
   - Não intercale Topic A e Topic B
   - Cada seção deve ser self-contained

**Exemplo (ruim):**
```markdown
# Document
Produto X custa $100.
Produto Y tem garantia de 2 anos.
Produto X tem 5 cores disponíveis.
Produto Y custa $150.
```

**Exemplo (bom):**
```markdown
# Document
## Produto X
Produto X custa $100.
Produto X tem 5 cores disponíveis.
Produto X tem garantia de 1 ano.

## Produto Y
Produto Y custa $150.
Produto Y tem garantia de 2 anos.
Produto Y está disponível apenas em preto.
```

**Benefício:** Chunks se alinham com tópicos, aumentando relevância quando retrieved

## Técnica 3: Chunk Overlap

### O Que É

**Definição:** Número de caracteres que devem se sobrepor entre dois chunks consecutivos

**Propósito:** Fornecer mais contexto para cada chunk

### Por Que Usar

**Problema sem overlap:**
```
Chunk 1: "... o produto tem múltiplas características."
Chunk 2: "Ele está disponível em 5 cores e vem com..."
```
- Chunk 2 perde contexto: "Ele" se refere a quê?

**Com overlap:**
```
Chunk 1: "... o produto tem múltiplas características."
Chunk 2: "o produto tem múltiplas características. Ele está disponível..."
```
- Chunk 2 agora tem contexto: "Ele" = "o produto"

### Configuração (VectorShift)

- **Onde:** Advanced Settings → Chunk Overlap
- **Valor:** Ajustável (maior = mais contexto, mais custo)
- **Trade-off:** Overlap maior = mais accurate, mas mais tokens duplicados = maior custo

## Técnica 4: Diferentes Tipos de Documentos

### Limitações de Knowledge Bases Tradicionais

**Aceitos tipicamente:**
- Word documents (.doc, .docx)
- Text files (.txt)
- PDF files (.pdf)

**NÃO aceitos:**
- Excel sheets (.xlsx)
- CSV files (.csv)
- Images/graphs dentro de PDFs
- Scanned PDFs (texto como imagem)

### Solução: Advanced Document Processing (VectorShift)

#### 1. CSV Query Function

**Funcionalidade:**
- Pergunta em natural language → convertida em fórmula
- Fórmula busca na database (Excel/CSV)
- Retorna resultados estruturados

**Exemplo:**
- Pergunta: "Quantos clientes temos em São Paulo?"
- Sistema: Converte para query → busca CSV → retorna número

**Referência:** Vídeo separado do autor sobre CSV querying

#### 2. OCR (Optical Character Recognition)

**Problema:**
- Alguns PDFs são scanned documents
- Texto é na verdade uma **imagem**
- Knowledge base tradicional não consegue ler

**Solução: LlamaParse (VectorShift)**
- **Onde:** File Processing Option → LlamaParse
- **Funcionalidade:**
  - Detecta automaticamente page elements (graphs, images, charts)
  - Extrai texto de imagens via OCR
  - Permite buscar em ALL content, não só texto nativo
  - Faz sentido de gráficos e charts

**Recomendação:**
> "Check your knowledge based documents as you may not realize that some of your documents might be scanned PDF files where the text is actually an image"

## Técnica 5: Hybrid Keyword Search

### O Que É

**Definição:** Combinar semantic search (embeddings) com old-school keyword search

**Histórico:**
- **Antes de knowledge bases:** Search engines usavam keywords
- **Agora:** Knowledge bases usam semantic similarity (embeddings)
- **Hybrid:** Usa ambos simultaneamente

### Por Que Usar

**Semantic search limitação:**
- Pode não pegar exact matches de termos técnicos
- Pode não encontrar códigos de produto específicos

**Keyword search adição:**
- Busca exact matches
- Complementa semantic search
- Fornece informação adicional ao AI

### Configuração (VectorShift)

- **Onde:** Create Knowledge Base → Hybrid toggle
- **Como:** Simplesmente toggle ON
- **Efeito:** Adiciona old-fashioned keyword search aos resultados semânticos

## Técnica 6: Transform Query

### O Que É

**Definição:** Transformar query do usuário em pergunta mais provável de gerar boas respostas

### Problema

**Usuários escrevem mal:**
- Perguntas confusas
- Gramática ruim
- Falta de contexto
- Ambiguidade

**Exemplo:**
- User: "quanto custa aquele negocio"
- Knowledge base: Luta para entender "aquele negócio"

### Solução

**Transform Query:**
1. Pega pergunta original do usuário
2. Usa LLM para reformular em pergunta clara
3. Envia versão melhorada para knowledge base

**Exemplo:**
- Original: "quanto custa aquele negocio"
- Transformed: "Qual é o preço do produto mencionado anteriormente?"

### Configuração (VectorShift)

- **Onde:** Knowledge Base Reader → Settings → Transform Query
- **Como:** Toggle ON
- **Backend:** Usa knowledge interno para melhorar pergunta automaticamente

## Técnica 7: Expand Query

### O Que É

**Definição:** Quebrar pergunta complexa em múltiplas perguntas simples, fazer uma por vez

### Problema

**Perguntas complexas:**
- Usuário faz pergunta técnica que requer múltiplos steps
- Knowledge base tenta responder tudo de uma vez
- Pode não ter contexto suficiente em chunks limitados

**Exemplo:**
- User: "Como configurar integração OAuth2 com refresh tokens e rate limiting?"
- Problema: Requer informação sobre OAuth2 + refresh tokens + rate limiting

### Solução

**Expand Query:**
1. Quebra em step-by-step questions
2. Pergunta knowledge base uma por vez:
   - "O que é OAuth2?"
   - "Como implementar refresh tokens?"
   - "Como configurar rate limiting?"
3. Combina respostas em resposta completa e formada

**Benefício:**
- Cada sub-query pode usar chunks limitados eficientemente
- Resposta final tem **all information required**
- Mais in-depth answer do que single query

### Configuração (VectorShift)

- **Onde:** Knowledge Base Reader → Settings → Expand Query
- **Como:** Toggle ON
- **Efeito:** Automatic breakdown em backend

## Técnica 8: Answer Multiple Questions

### O Que É

**Definição:** Detectar se usuário fez múltiplas perguntas de uma vez e responder cada uma separadamente

### Problema

**Usuário faz várias perguntas:**
- "Qual o preço? E a garantia? Vocês entregam em SP?"
- Knowledge base fica confusa
- Pode responder parcialmente ou misturar respostas

### Solução

**Answer Multiple Questions:**
1. Detecta que há múltiplas perguntas
2. Separa em perguntas individuais
3. Faz query para cada uma
4. Retorna respostas diretas para cada pergunta

**Exemplo:**
- Input: "Qual o preço? E a garantia?"
- Sistema quebra em:
  - Q1: "Qual o preço?" → A1: "$100"
  - Q2: "E a garantia?" → A2: "2 anos"
- Output: "O preço é $100. A garantia é de 2 anos."

### Configuração (VectorShift)

- **Onde:** Knowledge Base Reader → Settings → Answer Multiple Questions
- **Como:** Toggle ON
- **Efeito:** Automatic splitting e answering em backend

## Integração: VectorShift API com Outras Plataformas

### Como Exportar Knowledge Base

**Steps:**
1. Deploy → Chatbot → Give it a name → Save
2. Export → API → Choose API function
3. Copia URL endpoint
4. Settings → Pega API key

**API Call Structure:**
```
POST [URL_endpoint]
Headers:
  - API-Key: [your_api_key]
Body:
  - question: [user_question]
```

### Integração com Voiceflow

**Uso:**
- Fazer API call de dentro do Voiceflow
- Usar VectorShift knowledge base ao invés do nativo
- Benefício: Advanced features do VectorShift com UI do Voiceflow

### Integração com Vapi (Voice Agents)

**Uso:**
- Fazer API call de dentro do Vapi
- Usar knowledge base avançado para voice agents
- Mesmos benefícios

## Resumo das 8 Técnicas

| # | Técnica | Plataforma | Impacto | Complexidade |
|---|---------|------------|---------|--------------|
| 1 | **Chunk Count** | Voiceflow | Baixo | Baixa |
| 2 | **Document Structure** ⭐ | Universal | Alto | Média |
| 3 | **Chunk Overlap** | VectorShift | Médio | Baixa |
| 4 | **CSV/OCR Support** | VectorShift | Alto (se aplicável) | Média |
| 5 | **Hybrid Search** | VectorShift | Médio | Baixa |
| 6 | **Transform Query** | VectorShift | Alto | Baixa |
| 7 | **Expand Query** | VectorShift | Alto | Baixa |
| 8 | **Multiple Questions** | VectorShift | Médio | Baixa |

**Técnica mais importante:** #2 (Document Structure) - aplica a qualquer plataforma

## Exemplo Prático: Book Upload (200 páginas)

**Contexto:**
- Documento: Livro de Alex Hormozi (200 páginas)
- Result: 103 chunks no Voiceflow

**Processo:**

1. **Upload** → Document dividido em 103 chunks sequenciais
2. **Relevance Scoring** → Cada chunk recebe score de relevância
3. **Query** → Busca nos 103 chunks, retorna top 3-10 mais relevantes
4. **Response** → AI usa chunks retrieved para gerar resposta

**Problema identificado:**
- Chunks são sequenciais (página 1 → página 2 → ...)
- Se livro não está bem estruturado, chunks misturam tópicos
- Solução: **Reestruturar documento** antes de upload

## Trade-offs: Accuracy vs Cost

### Fatores que Aumentam Custo

| Fator | Custo ↑ | Accuracy ↑ |
|-------|---------|------------|
| Mais chunks por query (3 → 10) | ✅ | ✅ |
| Maior chunk size (1k → 4k chars) | ✅ | ✅ |
| Maior chunk overlap | ✅ | ✅ |
| Transform query (LLM extra call) | ✅ | ✅ |
| Expand query (múltiplas queries) | ✅ | ✅ |
| Hybrid search | Marginal | ✅ |

**Princípio:**
- Mais contexto = mais tokens = mais custo
- Mas também = respostas melhores

**Recomendação:**
- Comece com document structure (free)
- Adicione features incrementalmente
- Monitore cost/accuracy ratio

## Aplicação ao Sistema-OS

### 1. Knowledge Base para RM Module

**Documentos a estruturar:**
- Curso Intro Climber RMS (aulas extraídas)
- Livros de RM
- Experiência Duke Beach Hotel
- Documentação HITS API

**Aplicação de técnicas:**

| Técnica | Como Aplicar |
|---------|--------------|
| **Document Structure** | Agrupar conceitos de RM juntos (ex: Pick Up, Overbooking, Forecast em seções separadas) |
| **Chunk Overlap** | Para termos técnicos de RM que span múltiplos chunks |
| **CSV Support** | Dados históricos de ocupação, ADR, RevPAR em CSV |
| **Transform Query** | Usuário pergunta "quanto vou faturar?" → "Qual a previsão de receita para o período?" |
| **Expand Query** | "Como calcular forecast?" → quebra em steps (histórico + pick-up + ajustes) |

### 2. Onboarding de Novos Devs

**Knowledge base contém:**
- CLAUDE.md
- TASKS.md
- SCHEMAS.md
- Prompts de features anteriores

**Benefício:**
- Dev novo pergunta: "Como funciona o scheduler?"
- Knowledge base retorna: Documentação do scheduler + código relevante + exemplos

### 3. AI Assistant para Duke Beach Staff

**Use case:**
- Recepcionista pergunta: "Como fazer check-in de grupo?"
- Knowledge base busca em: Manual de procedimentos + edge cases + troubleshooting

**Aplicação:**
- Upload de manuais operacionais (estruturados por procedure)
- OCR para manuais scanned antigos
- Multiple questions para perguntas rápidas no balcão

### 4. Chatbot para Hóspedes

**Use case:**
- Hóspede: "Qual horário café da manhã? E piscina?"
- System: Answer multiple questions

**Documents:**
- Serviços do hotel
- Políticas
- FAQs
- Informações turísticas locais

## Best Practices Resumidas

### Para Estruturação de Documentos

1. ✅ Agrupe informação relacionada fisicamente
2. ✅ Use hierarquia clara (H1 > H2 > H3)
3. ✅ Coloque informações mais gerais primeiro
4. ✅ Evite pular entre tópicos
5. ✅ Teste fazendo queries e vendo chunks retrieved

### Para Configuração de Plataforma

1. ✅ Comece simples (chunk count básico)
2. ✅ Adicione features incrementalmente
3. ✅ Monitore accuracy através de test queries
4. ✅ Balance cost vs accuracy para seu use case
5. ✅ Use hybrid search se tem termos técnicos/códigos

### Para Query Optimization

1. ✅ Sempre ative Transform Query (melhora user input)
2. ✅ Use Expand Query para perguntas complexas/técnicas
3. ✅ Use Multiple Questions se usuários fazem várias perguntas de uma vez
4. ✅ Teste com perguntas reais de usuários

## Ferramentas e Recursos

### Plataformas Mencionadas

| Plataforma | URL | Uso |
|------------|-----|-----|
| **Voiceflow** | voiceflow.com | No-code chatbot builder |
| **VectorShift** | vectorshift.ai | Advanced knowledge base platform |
| **Vapi** | vapi.ai | AI voice callers platform |

### Vídeos Relacionados (do autor)

- "How to create AI chatbots from scratch in 1 hour"
- "How to create AI phone callers from scratch in 2 hours"
- "How to query CSV files on VectorShift"
- "1.5 hour tutorial on Voiceflow"

## Termos e Conceitos

| Termo | Definição |
|-------|-----------|
| **Knowledge Base** | Database de documentos que AI agent pode query para responder perguntas |
| **Chunk** | Pedaço de documento dividido para armazenamento e retrieval |
| **Chunk Size** | Número de caracteres em cada chunk |
| **Chunk Overlap** | Caracteres que se repetem entre chunks consecutivos |
| **Relevance Score** | Score atribuído a cada chunk indicando quão relevante é para uma query |
| **Semantic Search** | Busca baseada em similaridade de significado (embeddings) |
| **Keyword Search** | Busca baseada em exact matches de palavras |
| **Hybrid Search** | Combinação de semantic + keyword search |
| **Transform Query** | Reformular pergunta do usuário para melhorar retrieval |
| **Expand Query** | Quebrar pergunta complexa em sub-perguntas simples |
| **OCR** | Optical Character Recognition - extrair texto de imagens |
| **LlamaParse** | Ferramenta do VectorShift para processar images/graphs/scanned PDFs |

## Citações Memoráveis

> "The most integral part of building advanced AI agents is your knowledge base."

> "Think of it like a stack of playing cards - the knowledge base is the bottom layer, and without one of these cards, everything comes crashing down."

> "The biggest thing that I encourage you to do is just structure your documents better."

> "Unfortunately this Voiceflow knowledge base has very little functionality and features so we can't really get the most out of this knowledge base."

> "The more chunks we use, the more cost is involved... but ultimately the difference is going to be quite negligible." (sobre só ajustar chunk count)

## Timestamps de Referência

- **00:00** — Introdução: Knowledge base como foundation
- **00:39** — Voiceflow: Upload de documentos e limitations
- **01:43** — Exemplo: 200 páginas → 103 chunks
- **02:06** — Chunk count: 3 vs 10 (accuracy vs cost)
- **02:36** — **Técnica #1:** Structure your documents better ⭐
- **03:08** — Problema: Chunks misturam tópicos diferentes
- **03:51** — VectorShift introduction (sponsor)
- **04:08** — **Técnica #2:** Chunk size e chunk overlap
- **04:50** — VectorShift platform walkthrough
- **05:22** — Deploy e API integration
- **05:53** — Advanced settings: chunk size até 4,000
- **06:29** — Chunk overlap configuration
- **06:43** — **Técnica #3:** Different document types (CSV, Excel)
- **07:07** — CSV query function
- **07:16** — **Técnica #4:** OCR para images e scanned PDFs
- **07:49** — LlamaParse file processing
- **08:09** — **Técnica #5:** Hybrid keyword search
- **08:39** — **Técnica #6:** Transform query
- **09:03** — Transform query settings
- **09:17** — **Técnica #7:** Expand query (break into steps)
- **09:48** — Expand query settings
- **09:56** — **Técnica #8:** Answer multiple questions
- **10:09** — Multiple questions settings

## Conclusão e Próximos Passos

Este tutorial oferece um **framework prático** para otimizar knowledge bases de AI agents. A técnica mais importante (document structure) é **universal e gratuita**, enquanto as advanced features (VectorShift) oferecem ganhos incrementais.

**Para Sistema-OS:**

1. **Imediato:** Reestruturar arquivos MD de knowledge extraction
   - Agrupar conceitos relacionados
   - Hierarquia clara
   - Seções self-contained

2. **Curto prazo:** Implementar knowledge base para RM module
   - Curso Climber + Livros + Experiência Duke Beach
   - Usar para AI assistant no desenvolvimento

3. **Médio prazo:** Chatbot para staff Duke Beach
   - Manuais operacionais estruturados
   - OCR para documentos antigos
   - Multiple questions para uso no balcão

4. **Longo prazo:** Guest-facing chatbot
   - FAQs estruturados
   - Informações de serviços
   - Integração com sistema de reservas

**Ferramentas recomendadas:**
- **Grátis/Low-cost:** Começar com document structure optimization
- **Production:** Considerar VectorShift ou similar para advanced features
- **Integração:** Via API com sistema existente
