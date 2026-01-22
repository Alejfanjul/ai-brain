# Decisão: Sistema de MEMORY para Sessões

**Data:** 2026-01-22
**Status:** Planejamento pendente
**Contexto:** Conversa sobre implementação de sistema de memória híbrido

---

## Situação Atual

### O que foi implementado
- Hook `session-capture.ts` que captura sessões automaticamente no `SessionEnd`
- Estrutura `MEMORY/sessions/` criada no ai-brain e sistema-os
- Hook funciona em modo isolado (cada projeto salva no seu MEMORY/)

### O problema
O hook só captura **metadados** (session_id, timestamp, cwd). O conteúdo fica vazio:

```markdown
## Summary
Session captured automatically by stop hook.
```

Isso não tem utilidade prática - não registra O QUE foi feito.

---

## Solução Correta (baseada no PAI de Daniel Miessler)

### Como Daniel faz
> "When we get done doing anything, Kai thinks about what we did, turns that into a summary and writes it into this history system."

- **Não é hook automático** capturando metadados
- **É o agente (Kai)** que gera resumo ativo antes de salvar
- O agente **pensa** sobre o que foi feito

### Estrutura do History no PAI
```
history/
├── sessions/      # Sessões com resumos
├── learnings/     # Aprendizados extraídos
├── research/      # Pesquisas feitas
├── decisions/     # Decisões tomadas
└── bugs/          # Bugs encontrados e resolvidos
```

### Diferença fundamental

| Nosso sistema atual | PAI do Daniel |
|---------------------|---------------|
| Hook automático captura metadados | Agente gera resumo ativo |
| Vazio - só timestamp/cwd | Rico - resumo do que foi feito |
| Passivo | Ativo |

---

## Próximos Passos (a planejar)

1. **Definir comportamento do Claude** (via CLAUDE.md ou skill) para:
   - Antes de encerrar, gerar resumo da sessão
   - Escrever no `MEMORY/sessions/` com conteúdo útil
   - Categorizar em learnings/decisions/bugs conforme apropriado

2. **Decidir mecanismo de trigger:**
   - Skill `/fim` que usuário invoca manualmente?
   - Instrução no CLAUDE.md para fazer automaticamente?
   - Combinação dos dois?

3. **Revisar estrutura MEMORY/**
   - Manter sessions/decisions/learnings?
   - Adicionar research/bugs?

---

## Referências

### Projeto PAI (Personal AI Infrastructure) - Daniel Miessler
- **Repo:** https://github.com/danielmiessler/pai
- **Video Deep Dive:** https://www.youtube.com/watch?v=Le0DLrn7ta0
- **Blog:** https://danielmiessler.com/blog/personal-ai-infrastructure
- **Fonte capturada:** `sources/2025-12-16-unsupervised-learning-a-deepdive-on-my-personal-ai-infrastructure-pai-v2.md`

### Princípios relevantes do PAI
1. **Scaffolding > Model** - Estrutura importa mais que o modelo
2. **Code Before Prompts** - 80% código determinístico, 20% prompts
3. **Custom History System** - Sessions, learnings, research, decisions, bugs
4. **Meta/Self-Update** - Sistema que melhora a si mesmo

### Outros recursos
- **Impacto no sistema-os:** Mínimo (pasta vazia, pode ficar até implementar direito)
- **Repo ai-brain:** Onde este arquivo está salvo

---

## Notas da Sessão (2026-01-22)

- Houve queda de energia durante sessão anterior, causando confusão no git
- Resolvido conflito de rebase no sistema-os (branch development)
- Force push feito para sincronizar development
- Hook atualizado para modo isolado (não polui ai-brain com sessões de outros projetos)
