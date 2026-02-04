# AI Brain - Setup Técnico

## Variáveis de ambiente

```bash
# ~/ai-brain/.env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

## Dependências

- Python 3.x
- Ollama (opcional, para embeddings locais futuros)
- Bun (para hooks TypeScript)

---

## Ollama (Opcional)

### Comandos básicos

```bash
# Gerenciar serviço
sudo systemctl start ollama
sudo systemctl stop ollama
sudo systemctl status ollama

# Verificar se está rodando
curl localhost:11434/api/tags

# Ver modelos instalados
ollama list

# Instalar modelo de embeddings
ollama pull nomic-embed-text
```

### Verificar uso de GPU

```bash
# Ver se CUDA está disponível
nvidia-smi

# Verificar logs do Ollama (deve mostrar "using CUDA")
journalctl -u ollama -f
```

---

## Daily Digest / Goals System

Sistema para visualizar progresso das metas pessoais (treino e hábitos).

### Arquitetura

```
scripts/
├── goals/                    # Módulo de metas
│   ├── __init__.py
│   ├── parser.py             # Parse SAUDE.md e MACONHA.md
│   ├── progress.py           # Calcula métricas
│   └── ascii_charts.py       # Gráficos ASCII
├── daily_digest.py           # Gerador principal
└── show_goals.py             # Comando CLI

~/.claude/skills/DailyGoals/  # Skill para /goals
```

### Comandos

```bash
# Visão completa com ASCII art
python3 scripts/show_goals.py

# Só o foco do dia
python3 scripts/show_goals.py --today

# Só treino
python3 scripts/show_goals.py --saude

# Só redução de maconha
python3 scripts/show_goals.py --maconha

# Saída JSON
python3 scripts/show_goals.py --json

# Resumo em uma linha
python3 scripts/daily_digest.py --short
```

### Skill PAI

O skill `/goals` ou `/metas` está em `~/.claude/skills/DailyGoals/SKILL.md`.

### Dados fonte

- `projects/ai-brain/metas/SAUDE.md` - Dados de treino (ciclos, semanas, log)
- `projects/ai-brain/metas/MACONHA.md` - Dados de redução (fases, streak, log)

---

## MEMORY/ System

Sistema file-based para memória persistente (PAI-style) com captura inteligente via Haiku.

### Estrutura

```
MEMORY/
├── sessions/          # Sessões produtivas (filtradas, sem vazias)
│   └── YYYY-MM-DD_HH-mm-ss_{session_id}.md
├── decisions/         # Decisões importantes
├── learnings/         # Aprendizados AUTO-EXTRAÍDOS por fase
│   ├── OBSERVE/       # Descobertas sobre sistemas/domínios
│   ├── THINK/         # Conclusões de análises
│   ├── PLAN/          # Decisões estratégicas
│   ├── BUILD/         # Padrões de implementação
│   ├── EXECUTE/       # Learnings operacionais
│   └── VERIFY/        # Insights de validação
│   └── YYYY-MM-DD_HH-mm-ss_{hash}.md
├── State/             # Estado ativo (JSON)
│   └── active-work.json
└── Signals/           # Padrões e falhas (JSONL)
    ├── failures.jsonl
    └── patterns.jsonl
```

**Formato de nomes:** Timestamp completo garante ordem cronológica e evita sobrescrita.

### Hooks de captura

**1. `stop-hook.ts`** (evento `Stop` - cada resposta do Claude)
- Usa Haiku para classificar: `learning` / `work` / `empty`
- Se `learning`, extrai insight e salva em `MEMORY/learnings/{PHASE}/`
- Custo: ~$0.001 por chamada

**2. `session-capture.ts`** (evento `SessionEnd` - fim da sessão)
- **Filtro:** `interactions < 2` sem arquivos → não salva
- **Resumo inteligente:** Se não tem summary, Haiku gera
- Salva em `MEMORY/sessions/`

### Configuração

A `ANTHROPIC_API_KEY` deve estar em `~/.claude/.env`:

```bash
# ~/.claude/.env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Consulta

```bash
# Ver sessões recentes
ls -la ~/ai-brain/MEMORY/sessions/

# Ver learnings por fase
ls -la ~/ai-brain/MEMORY/learnings/BUILD/

# Buscar em toda memória
grep -r "termo" ~/ai-brain/MEMORY/
```

### Multi-máquina

Em nova máquina, após `git clone`:

```bash
cd ~/ai-brain
bash scripts/setup-pai.sh
```

Os symlinks propagam automaticamente todos os hooks e configurações.
