# Worktree Rules

Criterios de decisao e convencoes para git worktrees.

---

## Quando Criar uma Worktree

Sugerir worktree quando **2 ou mais** criterios forem verdadeiros:

| Criterio | Sinal |
|----------|-------|
| **Tarefa grande** | Multi-arquivo, multi-step, estimativa de 30+ minutos de trabalho |
| **Branch propria** | Feature ou fix que precisa de branch isolada (feature/*, fix/*) |
| **Paralelismo** | Usuario quer trabalhar em outra coisa ao mesmo tempo |
| **Risco de conflito** | Mudancas que podem conflitar com trabalho em andamento no repo principal |
| **Modulo independente** | Trabalho em modulo com pouca dependencia do resto (ex: booking-engine) |

### Quando NAO criar

- Bug fix simples (1-3 arquivos, branch development)
- Consulta ou exploracao de codigo
- Mudanca de docs ou config
- Tarefa que sera concluida na mesma sessao em menos de 15 minutos

---

## Naming Convention

### Pattern

```
{repo-name}-wt-{feature-name}
```

### Regras

1. **repo-name**: nome exato do diretorio do repositorio (ex: `sistema-os`, `ai-brain`)
2. **-wt-**: separador fixo (worktree). Usado pelo hook de auto-approve para pattern matching
3. **feature-name**: descricao curta em kebab-case (ex: `catalogo`, `auth-guard`, `booking-engine`)

### Localizacao

Worktrees sao SEMPRE criadas como irmas do repo pai:

```
/home/alejandro/
├── sistema-os/                    # repo principal
├── sistema-os-wt-catalogo/        # worktree
├── sistema-os-wt-auth-guard/      # worktree
├── ai-brain/                      # outro repo
└── ai-brain-wt-voice-system/      # worktree do ai-brain
```

### Branch Mapping

A branch dentro da worktree segue a convencao do projeto:

| Worktree | Branch |
|----------|--------|
| `sistema-os-wt-catalogo` | `feature/catalogo` |
| `sistema-os-wt-auth-guard` | `feature/auth-guard` |
| `sistema-os-wt-hotfix-login` | `fix/hotfix-login` |

---

## Hook de Auto-Approve

O hook `worktree-auto-approve.ts` em `~/.claude/hooks/` intercepta Read/Write/Edit/Glob/Grep e auto-aprova paths que casam com `/home/alejandro/sistema-os-wt-*`.

**Para adicionar suporte a novos repos:**
Editar o WORKTREE_PATTERN no hook para incluir o novo repo, ou generalizar para `*-wt-*`.
