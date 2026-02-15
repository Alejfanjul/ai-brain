# Claude Code Settings Backup

> Atualizado: 2026-02-15
> Para replicar em outra máquina, copie os conteúdos abaixo nos respectivos caminhos.

---

## 1. Global — `~/.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Write(**)",
      "Edit(**)",
      "Glob(**)",
      "Grep(**)",
      "WebSearch",
      "WebFetch(*)",
      "Skill(*)",
      "Task(*)",
      "Bash(*)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(rm -r /*)",
      "Bash(rm -r ~*)",
      "Bash(sudo rm -rf *)",
      "Bash(sudo rm -r *)",
      "Bash(dd if=*)",
      "Bash(mkfs*)",
      "Bash(git push --force*)",
      "Bash(git push -f *)",
      "Bash(git reset --hard*)",
      "Bash(git clean -f*)",
      "Bash(git checkout -- .)",
      "Bash(git restore .)",
      "Bash(git merge * main)",
      "Bash(git merge main*)",
      "Bash(> /dev/sd*)",
      "Bash(chmod 777 *)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/initialize-session.ts"
          },
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/load-core-context.ts"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/security-validator.ts"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/update-tab-titles.ts"
          }
        ]
      }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  },
  "enabledPlugins": {
    "frontend-design@claude-plugins-official": true,
    "supabase@claude-plugins-official": true
  },
  "language": "PT-BR",
  "alwaysThinkingEnabled": true
}
```

### Notas
- `permissions.allow` pode ter paths adicionais específicos da máquina (ex: `/mnt/c/Users/...`)
- `permissions.additionalDirectories` é específico da máquina — ajustar conforme necessário
- Hooks dependem de `~/.bun/bin/bun` e scripts em `~/.claude/hooks/` — copiar também

---

## 2. Projeto (sistema-os) — `sistema-os/.claude/settings.json`

```json
{
  "enabledPlugins": {
    "feature-dev@claude-plugins-official": true,
    "playwright@claude-plugins-official": true,
    "explanatory-output-style@claude-plugins-official": true,
    "hookify@claude-plugins-official": true
  }
}
```

---

## Checklist para nova máquina

1. Instalar Claude Code
2. Copiar `~/.claude/settings.json` (global)
3. Copiar `~/.claude/CLAUDE.md` (instruções globais)
4. Copiar `~/.claude/hooks/` (todos os scripts de hooks)
5. Copiar `~/.claude/skills/` (skills customizadas)
6. Copiar `~/.claude/pai/` (PAI context)
7. Copiar `~/.claude/statusline.sh`
8. Instalar bun: `curl -fsSL https://bun.sh/install | bash`
9. Clonar sistema-os e copiar `.claude/settings.json` do projeto
10. Plugins são instalados automaticamente na primeira sessão