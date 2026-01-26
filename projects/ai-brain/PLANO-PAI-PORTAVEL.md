# Plano: PAI Portável - Contexto Pessoal em Qualquer Repo

## Problema
Ale trabalha em 2 máquinas (casa/trabalho) com 3 repositórios independentes:
- `ai-brain` - Infraestrutura pessoal (PAI/TELOS)
- `ai-pms` - Produto hoteleiro (futuro negócio)
- `ai-pms-duke` - Aplicação no Duke Beach Hotel

Hoje o contexto pessoal (TELOS, skills, identidade) só está disponível no ai-brain.
**Objetivo**: Ter o assistente pessoal carregando em QUALQUER sessão Claude Code.

---

## Arquitetura (com Symlinks)

```
ai-brain/                           ← SOURCE OF TRUTH
├── pai/                            ← Arquivos fonte do PAI
│   ├── IDENTITY.md                 ← Quem sou (extraído do TELOS)
│   └── PROJECTS.md                 ← 3 frentes ativas + critérios
├── .claude-config/skills/CORE/     ← CORE skill
├── MEMORY/                         ← Memória de sessões
└── projects/ai-brain/telos/        ← TELOS completo

~/.claude/                          ← GLOBAL (symlinks)
├── pai/
│   ├── IDENTITY.md → ~/ai-brain/pai/IDENTITY.md
│   └── PROJECTS.md → ~/ai-brain/pai/PROJECTS.md
├── hooks/
│   └── load-pai-context.ts         ← Hook que injeta contexto
└── settings.json

ai-pms/                             ← Herda contexto global
├── CLAUDE.md                       ← Instruções específicas
└── MEMORY/sessions/                ← Memória isolada

ai-pms-duke/                        ← Herda contexto global
├── CLAUDE.md                       ← Instruções específicas
└── MEMORY/sessions/                ← Memória isolada
```

**Vantagem dos symlinks**: Edita em ai-brain → reflete automaticamente em ~/.claude/pai/

---

## Implementação (3 Fases)

### Fase 1: Criar Arquivos Fonte no ai-brain

**1.1 Criar `ai-brain/pai/IDENTITY.md`**

Extrair do TELOS as seções essenciais (~60 linhas):
- IDENTITY (quem sou, padrão recorrente)
- HOW TO WORK WITH ME (o que funciona/irrita)
- WISDOM (6 lições)
- Princípio central: "Verdade acima de conforto"

**1.2 Criar `ai-brain/pai/PROJECTS.md`**

```markdown
# Projetos Ativos

## 3 Frentes de Trabalho

### 1. AI-PMS-Duke (Obrigação)
- **O que**: Aplicação prática no Duke Beach Hotel
- **Status**: [em andamento]
- **Relevância**: Alta - trabalho atual
- **Critério**: Contribui se resolve problema real do hotel

### 2. AI-PMS (Visão)
- **O que**: PMS AI-native como produto (futura empresa)
- **Status**: [exploração]
- **Relevância**: Média - longo prazo
- **Critério**: Contribui se é padrão reusável do Duke

### 3. AI-Brain (Capacidade)
- **O que**: PAI/TELOS, assistente pessoal, exploração de agentes
- **Status**: [ativo]
- **Relevância**: Alta - habilita os outros dois
- **Critério**: Contribui se melhora produtividade ou organização

## Filtro de Relevância

Quando surge conhecimento/tarefa nova, perguntar:
1. Qual das 3 frentes isso serve?
2. Serve a frente prioritária (Duke) ou pode esperar?
3. Se não serve nenhuma → arquivar ou descartar
```

---

### Fase 2: Criar Symlinks e Hook

**2.1 Criar estrutura de diretórios**
```bash
mkdir -p ~/.claude/pai
```

**2.2 Criar symlinks**
```bash
ln -s ~/ai-brain/pai/IDENTITY.md ~/.claude/pai/IDENTITY.md
ln -s ~/ai-brain/pai/PROJECTS.md ~/.claude/pai/PROJECTS.md
```

**2.3 Criar/Modificar hook `~/.claude/hooks/load-pai-context.ts`**

O hook deve:
- Ler ~/.claude/pai/IDENTITY.md
- Ler ~/.claude/pai/PROJECTS.md
- Injetar como contexto no início da sessão
- Funcionar em qualquer diretório (não só ai-brain)

**2.4 Registrar hook em `~/.claude/settings.json`**

Adicionar em `hooks.SessionStart`:
```json
{
  "type": "command",
  "command": "~/.bun/bin/bun run ~/.claude/hooks/load-pai-context.ts"
}
```

---

### Fase 3: Configurar Repos ai-pms e ai-pms-duke

**Para cada repo:**

**3.1 Criar `CLAUDE.md`** com instruções específicas do projeto

**3.2 Criar `MEMORY/sessions/`** para captura isolada

**3.3 (Opcional) Criar `.claude-config/skills/`** para skills específicas do projeto

---

## Arquivos a Criar/Modificar

| Arquivo | Ação | Local |
|---------|------|-------|
| `pai/IDENTITY.md` | Criar | ai-brain |
| `pai/PROJECTS.md` | Criar | ai-brain |
| `pai/IDENTITY.md` | Symlink | ~/.claude |
| `pai/PROJECTS.md` | Symlink | ~/.claude |
| `hooks/load-pai-context.ts` | Criar/Modificar | ~/.claude |
| `settings.json` | Modificar | ~/.claude |
| `CLAUDE.md` | Criar | ai-pms |
| `MEMORY/sessions/` | Criar dir | ai-pms |
| `CLAUDE.md` | Criar | ai-pms-duke |
| `MEMORY/sessions/` | Criar dir | ai-pms-duke |

---

## Setup em Nova Máquina

Quando clonar em máquina nova:

```bash
# 1. Clonar repos
git clone <ai-brain>
git clone <ai-pms>
git clone <ai-pms-duke>

# 2. Criar symlinks (uma vez)
mkdir -p ~/.claude/pai
ln -s ~/ai-brain/pai/IDENTITY.md ~/.claude/pai/IDENTITY.md
ln -s ~/ai-brain/pai/PROJECTS.md ~/.claude/pai/PROJECTS.md

# 3. Hooks já estão em ~/.claude/hooks/ (versionados ou copiados)
```

**Nota**: Se ~/ai-brain estiver em path diferente, ajustar symlinks.

---

## Verificação

1. **Teste básico:**
   ```bash
   cd ~/ai-pms && claude
   # Perguntar: "quais são minhas 3 frentes de trabalho?"
   # Deve responder corretamente sobre AI-PMS, AI-PMS-Duke, AI-Brain
   ```

2. **Teste de atualização:**
   - Editar `ai-brain/pai/PROJECTS.md`
   - Abrir nova sessão em qualquer repo
   - Verificar que mudança refletiu

3. **Teste em máquina 2:**
   - Push do ai-brain
   - Pull na máquina 2
   - Verificar que symlinks funcionam

---

## Evolução Futura

Após esta base funcionar, próximos passos possíveis:
1. **Workflow de visibilidade**: Dashboard de status dos 3 projetos
2. **Classificação de conteúdo**: Sistema que avalia relevância de conhecimento novo
3. **Sync de MEMORY**: Consolidar aprendizados entre projetos
