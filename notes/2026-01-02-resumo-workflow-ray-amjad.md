# Resumo: Workflow de Coding com IA - Ray Amjad (2026)

**Data:** 2026-01-02
**Fonte:** [My AI Coding Workflow Going Into 2026](https://www.youtube.com/watch?v=sy65ARFI9Bg)
**Autor:** Ray Amjad

---

## Fluxo Principal de Trabalho

### 1. Criação de Especificação (Spec)
- **Screen Recording**: Grava tela de produto/feature similar que já existe
- **Gemini 2.0 Pro**: Processa o vídeo e gera PRD (Product Requirements Document)
- **Claude Code**: Refina spec usando Ask User Question tool
- **ChatGPT (heavy thinking)**: Pesquisa packages/bibliotecas relevantes no GitHub
- **Resultado**: Spec detalhada com bibliotecas modernas e bem mantidas

### 2. Desenvolvimento em Fases
- Claude Code quebra spec em fases
- Testa entre cada fase antes de avançar
- Usa Planning Mode para manter padrões consistentes no codebase

### 3. Papel do Desenvolvedor
Não é mais escrever código, mas sim:
- **Orquestrador**: desenhar feedback loops para o agente
- **Monitor**: observar reasoning do agente e identificar padrões de erro
- **Arquiteto**: decisões de alto nível (database, MCP servers, skills)
- **Curator**: manter CLAUDE.md atualizado com learnings

---

## Modelos e Ferramentas Utilizados

### Modelos por Uso (% de uso estimado)

| Modelo | Uso Principal | % Tempo |
|--------|---------------|---------|
| **Opus 4.5** | Features grandes, refactors, código limpo | 70-80% |
| **Sonnet 4.5** | Fixes pequenos, UI tweaks, code reviews | 15-20% |
| **Haiku 4.5** | Respostas rápidas, edits precisos | 5-10% |
| **GPT o1** | Arquitetura, planning, debugging complexo | Situacional |
| **Gemini 2.0 Pro** | Design, criatividade, screen→spec | Inicial |
| **ChatGPT** | Pesquisa de packages | Inicial |

### Claude Code vs Codex CLI

**Claude Code (80% do tempo)**:
- Mais interativo e "chatty"
- Ciclos curtos de feedback
- Start time mais rápido
- Melhor para iteração ativa

**Codex CLI (20% do tempo)**:
- Tarefas que precisam muito contexto
- Lê codebase inteiro antes de agir (10-15 min)
- Melhor para erros fundamentais de arquitetura
- Background tasks longas (ex: analisar erros do Sentry)

### Ferramentas Complementares

- **Hypisper**: Dictation tool (próprio do Ray) - prompts por voz
- **Cursor**: Code review visual (olhar "shape" do diff)
- **Warp**: Terminal (fork sessions)
- **MCP Servers**: Para contexto adicional (ex: Stripe docs)

---

## Técnicas Avançadas

### Planning Mode (Crítico!)
- Evita "architectural drift" (padrões inconsistentes)
- Sub-agents exploram codebase para encontrar padrões existentes
- Usa descobertas para manter consistência
- **Regra**: usar para qualquer mudança >10-15 linhas

### Sub-Agents (Evolução do Uso)

**❌ O que NÃO fazer** (tentou e falhou):
- Múltiplos sub-agents editando mesmo projeto em paralelo
- Roles diferentes (frontend/backend) no mesmo codebase
- Problemas: coordenação, merge conflicts, outputs incompatíveis

**✅ O que FUNCIONA**:
- **Research & Thinking**: 3-4 sub-agents pesquisando em paralelo
- **Diferentes ângulos**: Opus + Sonnet + Haiku analisando mesmo bug
- **Busca online**: Sub-agent com MCP para docs atualizadas
- **Multi-projeto**: 1 sub-agent por projeto (fixes em templates similares)
- **Tarefas bem definidas**: Ex: extrair i18n strings (edits pequenos)

### Fork Sessions
- Duplicar sessão atual para aprender/explorar
- Perguntar "por que escolheu essa abordagem?"
- Não interrompe sessão principal
- Pode usar modelo mais barato (Sonnet) para aprendizado

### Code Review Moderno
- **Antes (2025)**: linha por linha
- **Agora (2026)**: olha "shape" do diff
  - Quantos arquivos mudaram?
  - Quantas linhas?
  - Shape parece correto?
- Se shape está certo + plan era bom = commit direto
- Só investiga quando shape parece errado

### CLAUDE.md Dinâmico
- Atualiza fim de cada sessão
- Adiciona patterns que agente perdeu
- Correções arquiteturais
- Usa arquivos hierárquicos (por subpasta)

---

## Análise de Complexidade

### ⚠️ Complexidade de Setup

**Assinaturas Necessárias**:
1. ✅ **Claude Pro/API** (essencial) - 70-80% do trabalho
2. ⚠️ **OpenAI o1** (opcional mas recomendado) - arquitetura complexa
3. ⚠️ **Google Gemini 2.0 Pro** (opcional) - screen→spec workflow
4. ⚠️ **ChatGPT Plus** (opcional) - pesquisa de packages
5. ⚠️ **Codex CLI/Cursor Pro** (opcional) - debugging profundo

**Custo Estimado Mensal**:
- Mínimo viável: ~$20-40 (só Claude)
- Setup completo: ~$100-150 (todas ferramentas)

### 🎯 Simplificação Possível

**Workflow Simplificado (1 assinatura)**:
```
Claude Code apenas:
1. Spec manual ou com Claude
2. Planning Mode
3. Desenvolvimento iterativo
4. Fork session para aprender
```

**Adições Incrementais**:
- **+ChatGPT**: Só quando precisar descobrir packages
- **+Gemini**: Só para specs visuais complexas
- **+o1**: Só quando arquitetura é crítica

### 🚦 Sinais de Quando Adicionar Mais Modelos

| Situação | Solução |
|----------|---------|
| Specs ficam ambíguas | + Gemini (screen recording) |
| Usa bibliotecas desatualizadas | + ChatGPT (package search) |
| Arquitetura fica bagunçada | + o1 (planning) |
| Bugs fundamentais não resolvem | + Codex CLI |

---

## Workflow Paralelo (Multi-tasking)

- Ray usa 3-4 sessões em paralelo
- 1 projeto principal + projetos satélites
- **Limite cognitivo**: context switching cansa (silêncio necessário)
- **Ceticismo**: claims de 10+ sessões paralelas

---

## Key Takeaways para Ale

### ✅ Aplicável Imediatamente (Low Complexity)
1. **Planning Mode sempre** para features >10 linhas
2. **CLAUDE.md dinâmico** - atualizar fim de sessão
3. **Shape-based review** ao invés de linha por linha
4. **Fork sessions** para aprender sem poluir contexto

### ⚠️ Avaliar Custo/Benefício
1. **Múltiplos modelos**: começar só com Claude, adicionar conforme dor
2. **Sub-agents**: usar para research, não para edits paralelos
3. **Sessões paralelas**: máximo 2-3 (cognitive load alto)

### 🎓 Mindset Shift
- Código é **throwaway** (experimentar sem medo)
- Dev é **orchestrator** não writer
- **Feedback loops** > escrever código perfeito
- **Planning** > speed (evita refactor futuro)

---

## Limitações e Cautelas

1. **Vendor Lock-in**: Workflow depende fortemente de Claude Code
2. **Custos Escaláveis**: Múltiplas APIs podem ficar caras
3. **Curva de Aprendizado**: Dominar sub-agents, MCP, planning mode
4. **Over-engineering Risk**: Fácil adicionar complexidade desnecessária
5. **Cognitive Load**: Multi-tasking com agents cansa

---

## Conclusão

**É complexo demais?**
Depende:
- **Setup mínimo** (só Claude): ✅ Acessível e poderoso
- **Setup completo** (4-5 LLMs): ⚠️ Para power users / empresas

**Recomendação**:
Começar simples (Claude + Planning Mode) e adicionar ferramentas conforme dores específicas aparecem. O core do workflow (Planning Mode + CLAUDE.md + Shape Review) não precisa de múltiplas assinaturas.
