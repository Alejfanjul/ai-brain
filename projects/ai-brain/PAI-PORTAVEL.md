# PAI Portável - Documentação

> Contexto pessoal disponível em qualquer repositório.
> Status: **Fase 1 concluída** (2026-01-27)

---

## Resumo

O PAI Portável permite que seu contexto pessoal (identidade, projetos, preferências) seja carregado automaticamente em **qualquer** sessão Claude Code, não apenas no ai-brain.

---

## Arquitetura Atual

```
ai-brain/                           ← SOURCE OF TRUTH
├── pai/                            ← Arquivos de contexto
│   ├── IDENTITY.md                 ← Quem sou (extraído do TELOS)
│   └── PROJECTS.md                 ← 3 frentes + critérios de relevância
├── MEMORY/                         ← Memória de sessões
└── projects/ai-brain/telos/        ← TELOS completo

~/.claude/                          ← GLOBAL
├── pai/                            ← Symlinks
│   ├── IDENTITY.md → ~/ai-brain/pai/IDENTITY.md
│   └── PROJECTS.md → ~/ai-brain/pai/PROJECTS.md
├── hooks/
│   └── load-core-context.ts        ← Hook que injeta contexto
└── settings.json                   ← Hooks registrados

sistema-os/                         ← Herda contexto global
├── CLAUDE.md                       ← (a criar) Instruções específicas
└── MEMORY/sessions/                ← (a criar) Memória isolada
```

**Fluxo:**
```
ai-brain/pai/*.md → ~/.claude/pai/ (symlinks) → load-core-context.ts → Qualquer sessão
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
# 1. Clonar repos
git clone <ai-brain>
git clone <sistema-os>

# 2. Criar symlinks (uma vez)
mkdir -p ~/.claude/pai
ln -s ~/ai-brain/pai/IDENTITY.md ~/.claude/pai/IDENTITY.md
ln -s ~/ai-brain/pai/PROJECTS.md ~/.claude/pai/PROJECTS.md

# 3. Copiar hooks (se não existirem)
cp -r ~/ai-brain/.claude-config/hooks/* ~/.claude/hooks/ 2>/dev/null || true
```

**Nota:** Se `~/ai-brain` estiver em path diferente, ajustar symlinks.

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
| `~/.claude/hooks/load-core-context.ts` | Hook que carrega contexto |

---

## Log de Implementação

### 2026-01-27 - Fase 1 concluída
- Criados `pai/IDENTITY.md` e `pai/PROJECTS.md`
- Criados symlinks em `~/.claude/pai/`
- Corrigido `load-core-context.ts` (buscava path errado)
- Eliminados ~25 arquivos obsoletos:
  - Hooks duplicados em `.claude-config/hooks/`
  - Templates vazios em `.claude-config/skills/CORE/USER/`
  - Sessions vazias em `MEMORY/sessions/`
