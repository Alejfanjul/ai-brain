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

### 5. Symlink de arquivos gitignored

Arquivos no `.gitignore` NAO sao copiados para a worktree. Verificar e criar symlinks:

```bash
# .env (credenciais, config de ambiente)
if [ -f {repo_dir}/.env ] && [ ! -f {worktree_dir}/.env ]; then
  ln -s {repo_dir}/.env {worktree_dir}/.env
fi
```

**Arquivos comuns que precisam de symlink:**

| Arquivo | Motivo |
|---------|--------|
| `.env` | Credenciais do banco, API keys, config de ambiente |
| `.env.local` | Overrides locais |
| `venv/` | Virtual environment Python (ou criar novo) |

**Regra:** Sempre verificar se `.env` existe no repo pai. Se sim, criar symlink automaticamente (nao copiar — symlink garante que mudancas no original se propagam).

Para venv Python, PERGUNTAR ao usuario: symlink da venv existente ou criar nova?

### 6. Setup do ambiente (se aplicavel)

Verificar se o projeto precisa de setup adicional:
- **Python**: checar se existe `requirements.txt` ou `pyproject.toml` — sugerir criar venv ou symlink
- **Node**: checar se existe `package.json` — sugerir `npm install`
- **Outros**: checar documentacao do projeto

NAO executar setup automaticamente — apenas informar o usuario o que precisa ser feito.

### 7. Confirmar e instruir

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

### 8. Registrar em additionalDirectories (se na mesma sessao)

Se o usuario quiser acessar a worktree da sessao atual (sem abrir nova sessao), a worktree precisa estar registrada em `additionalDirectories` no settings.local.json do projeto.

Perguntar antes de modificar settings.
