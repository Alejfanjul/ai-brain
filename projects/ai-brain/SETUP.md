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

Sistema file-based para memória persistente (PAI-style).

### Estrutura

```
MEMORY/
├── sessions/          # Logs de sessão (criados automaticamente)
├── decisions/         # Decisões importantes
├── learnings/         # Aprendizados por fase do ciclo
│   ├── OBSERVE/
│   ├── THINK/
│   ├── PLAN/
│   ├── BUILD/
│   ├── EXECUTE/
│   └── VERIFY/
├── State/             # Estado ativo (JSON)
│   └── active-work.json
└── Signals/           # Padrões e falhas (JSONL)
    ├── failures.jsonl
    └── patterns.jsonl
```

### Hook de captura

O hook `session-capture.ts` dispara no evento Stop e cria um arquivo em `MEMORY/sessions/` com:
- YAML frontmatter (session_id, timestamp, cwd)
- Conteúdo da sessão

### Consulta

```bash
# Ver sessões recentes
ls -la ~/ai-brain/MEMORY/sessions/

# Buscar em sessões
grep -r "termo" ~/ai-brain/MEMORY/sessions/
```
