# PAI Portável - Documentação

> Contexto pessoal disponível em qualquer repositório.
> Status: **Fase 1.5 concluída** (2026-01-28)

---

## Resumo

O PAI Portável permite que seu contexto pessoal (identidade, projetos, preferências) seja carregado automaticamente em **qualquer** sessão Claude Code, não apenas no ai-brain.

---

## Arquitetura Atual

```
ai-brain/                              ← SOURCE OF TRUTH (versionado)
├── pai/                               ← Contexto pessoal
│   ├── IDENTITY.md                    ← Quem sou (extraído do TELOS)
│   └── PROJECTS.md                    ← 3 frentes de trabalho
├── .claude-config/                    ← Configuração Claude
│   ├── hooks/                         ← Hooks (5 arquivos + lib/)
│   │   └── load-core-context.ts       ← Hook principal (auto-setup de pai/)
│   └── settings.json                  ← Configurações + registro de hooks
├── MEMORY/                            ← Memória de sessões
├── scripts/setup-pai.sh               ← Script de setup (uma vez por máquina)
└── SETUP-WORK-PC.md                   ← Instruções para máquina do trabalho

~/.claude/                             ← GLOBAL (symlinks)
├── pai/                               ← → ai-brain/pai/
│   ├── IDENTITY.md
│   └── PROJECTS.md
├── hooks/                             ← → ai-brain/.claude-config/hooks/
│   └── *.ts
└── settings.json                      ← → ai-brain/.claude-config/settings.json
```

**Fluxo de setup (uma vez por máquina):**
```
git clone ai-brain → ./scripts/setup-pai.sh → Symlinks criados
```

**Fluxo de atualização (sempre):**
```
git pull → Symlinks já apontam para arquivos atualizados → Pronto
```

---

## Status das Fases

### Fase 0: Clareza ✅
- [x] Definir 2 repos (ai-brain, sistema-os)
- [x] Definir 3 frentes (Duke, AI-PMS, AI-Brain)

### Fase 1: PAI Portável ✅
- [x] Criar `ai-brain/pai/IDENTITY.md`
- [x] Criar `ai-brain/pai/PROJECTS.md`
- [x] Criar symlinks em `~/.claude/pai/`
- [x] Corrigir `~/.claude/hooks/load-core-context.ts`
- [x] Limpar arquivos obsoletos

### Fase 1.5: Setup Portátil ✅
- [x] Hook com auto-setup de symlinks pai/
- [x] Hooks versionados em `.claude-config/hooks/`
- [x] Settings versionado em `.claude-config/settings.json`
- [x] Script `setup-pai.sh` atualizado (usa symlinks)
- [x] Instruções `SETUP-WORK-PC.md` para máquina do trabalho

### Fase 2: Session Capture Global ⏳
- [ ] Melhorar `session-capture.ts` para capturar resumo útil
- [ ] Testar captura em múltiplos repos

### Fase 3: Configurar sistema-os ⏳
- [ ] Criar `CLAUDE.md` no sistema-os
- [ ] Criar `MEMORY/sessions/` no sistema-os
- [ ] Testar herança de contexto

### Fase 4: Afinar ⏳
- [ ] Melhorar formato das sessions
- [ ] Adicionar mais contexto ao IDENTITY/PROJECTS
- [ ] Daily review workflow

---

## Setup em Nova Máquina

```bash
# 1. Clonar repo
git clone https://github.com/alejandrofjl/ai-brain.git ~/ai-brain

# 2. Rodar setup (cria todos os symlinks)
cd ~/ai-brain && ./scripts/setup-pai.sh

# 3. Reiniciar Claude Code
```

**Alternativa:** Abrir `SETUP-WORK-PC.md` e colar no Claude Code - ele executa automaticamente.

**Se path diferente de ~/ai-brain:**
```bash
export AI_BRAIN_PATH=/seu/path/ai-brain
```

---

## Verificação

1. **Teste básico:**
   ```bash
   cd ~/sistema-os && claude
   # Perguntar: "quais são minhas 3 frentes de trabalho?"
   # Deve responder: Duke, AI-PMS, AI-Brain
   ```

2. **Teste de atualização:**
   - Editar `ai-brain/pai/PROJECTS.md`
   - Abrir nova sessão em qualquer repo
   - Verificar que mudança refletiu

---

## Atualização do TELOS

```
TELOS-ALE.md (documento mestre, completo)
      │
      │ (extração manual - quando mudar)
      ▼
pai/IDENTITY.md (subset para sessões)
      │
      │ (symlink automático)
      ▼
~/.claude/pai/IDENTITY.md → carrega em qualquer repo
```

Quando o TELOS mudar significativamente, atualizar `pai/IDENTITY.md` manualmente.

---

## Arquivos de Referência

| Arquivo | Descrição |
|---------|-----------|
| `pai/IDENTITY.md` | Quem sou, como trabalhar comigo |
| `pai/PROJECTS.md` | 3 frentes de trabalho |
| `projects/ai-brain/telos/TELOS-ALE.md` | TELOS completo |
| `.claude-config/hooks/load-core-context.ts` | Hook que carrega contexto (com auto-setup) |
| `.claude-config/settings.json` | Configurações do Claude |
| `scripts/setup-pai.sh` | Script de setup (symlinks) |
| `SETUP-WORK-PC.md` | Instruções para máquina do trabalho |

---

## Log de Implementação

### 2026-01-28 - Fase 1.5 concluída
- Hook `load-core-context.ts` agora faz auto-setup de `~/.claude/pai/`
  - Se symlinks não existem, procura ai-brain e cria automaticamente
  - Mensagens de feedback para cada cenário
- Hooks movidos para `.claude-config/hooks/` (versionados)
- Settings movido para `.claude-config/settings.json` (versionado)
- Script `setup-pai.sh` reescrito para usar symlinks (não cópias)
- Criado `SETUP-WORK-PC.md` com instruções para Claude executar setup

**Limitações documentadas:**
- Setup inicial necessário uma vez por máquina
- Arquivos novos exigem novo symlink (rodar setup de novo)
- Symlinks são absolutos (se mudar path do repo, recriar)

### 2026-01-27 - Fase 1 concluída
- Criados `pai/IDENTITY.md` e `pai/PROJECTS.md`
- Criados symlinks em `~/.claude/pai/`
- Corrigido `load-core-context.ts` (buscava path errado)
- Eliminados ~25 arquivos obsoletos:
  - Hooks duplicados em `.claude-config/hooks/`
  - Templates vazios em `.claude-config/skills/CORE/USER/`
  - Sessions vazias em `MEMORY/sessions/`
