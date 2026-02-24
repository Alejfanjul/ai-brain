# Setup PAI (Kai) no Windows

> Guia para Claude Code executar no Windows.
> O usuário clona este repo e pede: "leia scripts/SETUP-WINDOWS.md e me ajude a configurar"

---

## Pré-requisitos

O usuário precisa ter:
- Git instalado
- Claude Code funcionando (VSCode ou CLI)
- Este repo clonado em `%USERPROFILE%\ai-brain`

---

## Passos (execute em ordem)

### 1. Verificar localização do repo

```powershell
# Verificar que o repo está no lugar certo
ls $HOME\ai-brain\pai\DAIDENTITY.md
```

Se não existir, o repo não está em `%USERPROFILE%\ai-brain`. Orientar o usuário a mover ou re-clonar:
```powershell
git clone git@github.com:Alejfanjul/ai-brain.git $HOME\ai-brain
```

**IMPORTANTE:** No PowerShell, NUNCA usar `~` em argumentos para programas externos (git, bun, etc). Sempre usar `$HOME` ou path completo. O `~` não expande corretamente e cria pastas literais chamadas `~`.

---

### 2. Verificar/Instalar Bun

```powershell
bun --version
```

Se não encontrar:
```powershell
powershell -c "irm bun.sh/install.ps1 | iex"
```

Depois de instalar, o usuário PRECISA fechar e reabrir o terminal (ou o VSCode inteiro) para o bun estar no PATH. Avise isso.

Verificar de novo após reabrir:
```powershell
bun --version
```

---

### 3. Verificar SSH (se clonou via SSH)

```powershell
ssh -T git@github.com
```

Se falhar com "Permission denied":

```powershell
# Verificar se já tem chave
ls $HOME\.ssh\id_ed25519.pub
```

Se não tiver chave:
```powershell
ssh-keygen -t ed25519 -C "alejfanjul@github.com"
# Aceitar todos os defaults (Enter 3x)
```

Depois, mostrar a chave pública:
```powershell
cat $HOME\.ssh\id_ed25519.pub
```

Instruir o usuário:
> "Copie essa chave e adicione em github.com → Settings → SSH and GPG keys → New SSH key. Cole a chave, dê um nome (ex: 'PC Trabalho') e salve."

Isso é uma ação no browser que o Claude Code NÃO consegue fazer. Esperar o usuário confirmar.

Testar novamente:
```powershell
ssh -T git@github.com
```

---

### 4. Rodar o setup script

```powershell
powershell -ExecutionPolicy Bypass -File $HOME\ai-brain\scripts\setup-pai.ps1
```

O script cria junctions (links de diretório) de `%USERPROFILE%\.claude\` apontando para o repo:
- `hooks/` → `.claude-config/hooks/`
- `skills/` → `.claude-config/skills/`
- `pai/` → `pai/`
- `settings.json` → `.claude-config/settings.json`
- `CLAUDE.md` → `.claude-config/CLAUDE.md`

Verificar que funcionou:
```powershell
ls $HOME\.claude\hooks\
ls $HOME\.claude\pai\
cat $HOME\.claude\pai\DAIDENTITY.md | Select-Object -First 5
```

Deve mostrar os arquivos de hooks e o início do DAIDENTITY.md.

---

### 5. Configurar .env (API key para session capture)

O hook session-capture.ts precisa da ANTHROPIC_API_KEY para gerar resumos com Haiku.

```powershell
# Verificar se já existe
cat $HOME\.claude\.env
```

Se não existir ou estiver vazio:
```powershell
# O usuário precisa fornecer a key
# Pergunte: "Qual é a sua ANTHROPIC_API_KEY?"
```

Criar o arquivo:
```powershell
echo "ANTHROPIC_API_KEY=<key-fornecida>" > $HOME\.claude\.env
```

---

### 6. Verificação final

Instruir o usuário:
> "Feche esta sessão do Claude Code e abra uma nova. Na nova sessão, pergunte: 'Kai, é você?'"

Se Kai responder com personalidade (nome, fala em primeira pessoa, reconhece Ale), o setup está completo.

---

## Troubleshooting

### Hooks não executam
- Verificar que bun está no PATH: `bun --version`
- Verificar que os junctions existem: `ls $HOME\.claude\hooks\`
- Testar hook manualmente: `echo '{}' | bun run $HOME\.claude\hooks\load-core-context.ts`

### Kai não carrega mas hooks existem
- Verificar que os arquivos de identidade existem: `ls $HOME\.claude\pai\`
- Se `pai/` está vazio, o junction pode ter quebrado. Re-rodar o setup.

### "Permission denied" no setup
- Fechar todos os VSCode/terminais que possam estar usando `~/.claude/`
- Re-rodar como admin se necessário

### settings.json conflita com config local
- O setup faz backup da config anterior (`.bak-YYYYMMDD`)
- Se precisar recuperar: `ls $HOME\.claude\*.bak*`
