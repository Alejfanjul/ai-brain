# Decisão: Sistema de MEMORY para Sessões

**Data:** 2026-01-22
**Atualizado:** 2026-02-02
**Status:** Implementado (abordagem híbrida)
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

## Solução Implementada (2026-02-02)

Abordagem **híbrida simples**:

### Camada 1: Hook automático (sempre roda)
- `session-capture.ts` reescrito para ler JSONL do Claude Code
- Extrai: summaries, primeira mensagem do usuário, arquivos modificados, tools usados
- **Centralizado:** sempre salva em `~/ai-brain/MEMORY/sessions/` independente do projeto
- MEMORY removido do sistema-os (`.gitignore` adicionado)

### Camada 2: Skill `/fim` (opcional, melhor qualidade)
- Skill `SessionEnd` criado em `.claude-config/skills/SessionEnd/SKILL.md`
- Claude gera resumo rico antes de encerrar sessão
- Se `/fim` já criou o arquivo, o hook append metadata automática

### Decisões tomadas
1. **MEMORY centralizado no ai-brain** — sessões de qualquer projeto vão pra cá
2. **Mecanismo híbrido** — automático + manual (`/fim`)
3. **42 session files vazios deletados** — limpeza do lixo acumulado

## Próximos Passos

1. Validar captura em sessões reais (ai-brain e sistema-os)
2. Implementar extração de learnings das sessões capturadas
3. Implementar skill de extração de conhecimento (tipo extract_knowledge)

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
