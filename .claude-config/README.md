# .claude-config

Configuracao centralizada do Claude Code. Sincroniza via git — `setup-pai.sh` cria symlinks de `~/.claude/` para ca.

## Estrutura

```
.claude-config/
├── settings.json   ← Permissoes, hooks, model, language
├── hooks/          ← Hooks de sessao e seguranca
├── skills/         ← Skills invocaveis (/fim, /goals, etc.)
├── CLAUDE.md       ← Instrucoes globais pro Claude
└── README.md       ← Este arquivo
```

## Permissoes

Logica: **permitir tudo, bloquear o perigoso.**

### Allow (tudo liberado)

`Bash(*)`, `Read(**)`, `Write(**)`, `Edit(**)`, `WebFetch(*)`, `WebSearch`, `Skill(*)`, `Task(*)`.

Nenhum prompt de aprovacao para operacoes normais.

### Deny (bloqueado, sem excecao)

| Categoria | Patterns |
|-----------|----------|
| Delecao destrutiva | `rm -rf`, `rm -r /`, `rm -r ~`, `sudo rm` |
| Git destrutivo | `push --force`, `push -f`, `reset --hard`, `clean -f`, `checkout -- .`, `restore .` |
| Merge em main | `merge main`, `merge * main` |
| Sistema | `dd if=`, `mkfs`, `chmod 777`, fork bomb |

### Segunda camada: security-validator.ts

Hook `PreToolUse` que roda antes de todo comando Bash. Cobre padroes avancados que deny rules nao pegam:

- Reverse shells (bash, netcat, python, ruby, php, socat)
- Execucao remota (curl|sh, wget|sh, base64 decode)
- Prompt injection
- Exfiltracao de dados (tar|curl, zip|nc)
- Manipulacao de credenciais/env
- Protecao de arquivos PAI/Claude

## Setup em novo PC

```bash
git clone <repo> ~/ai-brain
cd ~/ai-brain
./scripts/setup-pai.sh
```

O script cria symlinks:
- `~/.claude/settings.json` → `.claude-config/settings.json`
- `~/.claude/hooks/` → `.claude-config/hooks/`
- `~/.claude/skills/` → `.claude-config/skills/`
- `~/.claude/CLAUDE.md` → `.claude-config/CLAUDE.md`

Depois disso, `git pull` atualiza tudo automaticamente.
