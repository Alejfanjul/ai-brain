---
name: Worktree
description: Git worktree management with naming conventions. USE WHEN user asks to create worktree, work in parallel, isolate feature, spin up parallel session OR when task is large enough to benefit from isolation OR /worktree.
---

# Worktree

Gerencia worktrees git com naming convention padronizada. Inclui criterios de decisao (quando criar) e execucao (como criar).

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Create** | "cria worktree", "quero trabalhar em paralelo", "isola essa feature", "/worktree" | `Workflows/Create.md` |

## Proactive Suggestion

Este skill pode ser sugerido proativamente. Quando o usuario pede uma tarefa que atende aos criterios em `Rules.md`, sugira criar uma worktree ANTES de comecar a implementacao.

Formato da sugestao:
```
Essa tarefa parece se beneficiar de uma worktree isolada:
- [motivo 1]
- [motivo 2]

Quer que eu crie uma worktree para isso? (ex: `sistema-os-wt-catalogo`)
```

Se o usuario aceitar, invocar o workflow Create.

## Examples

**Example 1: Criacao explicita**
```
User: "Cria uma worktree para o modulo de catalogo"
-> Invokes Create workflow
-> Executa: git worktree add ../sistema-os-wt-catalogo -b feature/catalogo
-> Confirma criacao e instrui como abrir no VS Code
```

**Example 2: Sugestao proativa**
```
User: "Quero implementar o sistema de autenticacao completo"
-> Detecta: tarefa grande, multi-arquivo, branch propria
-> Sugere: "Essa tarefa se beneficia de uma worktree. Quer que eu crie sistema-os-wt-auth-guard?"
-> Se aceito, invokes Create workflow
```

**Example 3: Trabalho paralelo**
```
User: "Preciso trabalhar no booking engine em paralelo com o que estou fazendo"
-> Detecta: usuario quer paralelismo
-> Invokes Create workflow
-> Cria: sistema-os-wt-booking-engine
-> Instrui: "Abra a pasta no VS Code e inicie uma nova sessao Claude la"
```

## Naming Convention

**Pattern:** `{repo-name}-wt-{feature-name}`

| Repo | Worktree |
|------|----------|
| `sistema-os` | `sistema-os-wt-catalogo` |
| `sistema-os` | `sistema-os-wt-auth-guard` |
| `ai-brain` | `ai-brain-wt-voice-system` |

**Regras:**
- Sempre irmao do repo pai (mesmo diretorio pai)
- Feature name em kebab-case
- Prefixo `-wt-` identifica worktrees (usado pelo hook de auto-approve)

## Hook Integration

O hook `worktree-auto-approve.ts` auto-aprova operacoes Read/Write/Edit/Glob/Grep em paths matching `/home/alejandro/sistema-os-wt-*`. Para novos repos, o pattern do hook precisa ser atualizado.
