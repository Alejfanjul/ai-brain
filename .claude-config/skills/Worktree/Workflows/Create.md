# Create Workflow

Cria uma nova git worktree seguindo as convencoes do projeto.

## Steps

### 1. Identificar parametros

A partir do pedido do usuario, extrair:
- **repo**: repositorio de origem (detectar automaticamente pelo diretorio atual)
- **feature**: nome da feature em kebab-case
- **branch-type**: `feature/` (padrao), `fix/`, ou outra convencao do projeto

Se o usuario nao especificar o nome da feature, perguntar.

### 2. Montar nomes

```
repo_name = basename do diretorio do repo (ex: "sistema-os")
worktree_dir = ../{repo_name}-wt-{feature}
branch_name = {branch-type}/{feature}
```

Exemplo:
- repo: `/home/alejandro/sistema-os`
- feature: `catalogo`
- worktree_dir: `../sistema-os-wt-catalogo`
- branch: `feature/catalogo`

### 3. Verificar pre-condicoes

```bash
# Verificar se worktree ja existe
git worktree list

# Verificar se branch ja existe
git branch --list "feature/{feature}"
git branch -r --list "origin/feature/{feature}"
```

Se a branch ja existir no remote, usar ela:
```bash
git worktree add {worktree_dir} feature/{feature}
```

Se nao existir, criar nova:
```bash
git worktree add {worktree_dir} -b feature/{feature}
```

### 4. Criar worktree

Executar o comando git worktree add com os parametros montados.

### 5. Setup do ambiente (se aplicavel)

Verificar se o projeto precisa de setup:
- **Python**: checar se existe `requirements.txt` ou `pyproject.toml` — sugerir criar venv
- **Node**: checar se existe `package.json` — sugerir `npm install`
- **Outros**: checar documentacao do projeto

NAO executar automaticamente — apenas informar o usuario o que precisa ser feito.

### 6. Confirmar e instruir

Informar o usuario:

```
Worktree criada:
- Diretorio: /home/alejandro/{worktree_dir}
- Branch: feature/{feature}

Para abrir no VS Code:
  code /home/alejandro/{worktree_dir}

Para iniciar uma sessao Claude na worktree:
  cd /home/alejandro/{worktree_dir} && claude
```

### 7. Registrar em additionalDirectories (se na mesma sessao)

Se o usuario quiser acessar a worktree da sessao atual (sem abrir nova sessao), a worktree precisa estar registrada em `additionalDirectories` no settings.local.json do projeto.

Perguntar antes de modificar settings.
