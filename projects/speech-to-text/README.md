# Speech-to-Text — Projeto estratégico

> Iniciado: 2026-02-07
> Status: Fase 1 em andamento
> Frente: AI-Brain (Capacidade) + Duke (futuro)

## Visão

```
Whisper API (voz→texto) + Claude (inteligência) + ElevenLabs (texto→voz)
├── Fase 1: Dictation pessoal ← AGORA
├── Fase 2: sistema-os POPs (funcionários falam com o sistema)
└── Fase 3: App mobile (falar com Claude pelo celular)
```

## Decisões tomadas

| Decisão | Escolha | Por quê |
|---------|---------|---------|
| API vs local | **OpenAI Whisper API** | Custo irrisório (~R$0.03/min), sem GPU requerida, portável |
| Linguagem | **Python** | sistema-os é FastAPI/Python — core reusável |
| Desktop tools | **Descartadas** | OpenWhispr, Buzz, WhisperTyping são becos sem saída pro plano maior |
| Hotkey | **F9** toggle (press/press) | Mais confortável que hold-to-release, tecla única |
| Distribuição | **ai-brain/tools/** + git | Versionado, sincroniza em todas as máquinas |

## Opções avaliadas e descartadas

| Ferramenta | Tipo | Por que descartada |
|-----------|------|-------------------|
| Win+H | Built-in Windows | Péssimo em pt-BR (testado) |
| Buzz | Open source desktop | Não faz dictation system-wide |
| OpenWhispr | Open source desktop | Precisa Visual Studio Build Tools; beco sem saída |
| whisper-key-local | Open source desktop | 100% local, não integra com nada |
| WhisperTyping | Comercial ($5/mês) | Caixa preta, sem reusabilidade |
| Wispr Flow | Comercial ($15/mês) | 2.8/5 Trustpilot, buggy no Windows |

## Arquitetura

### Código: `ai-brain/tools/whisper-dictation/`

```
tools/whisper-dictation/
├── transcribe.py      ← Core reusável (Whisper API)
├── dictation.py       ← Wrapper desktop (hotkey + mic + paste)
├── config.json        ← Configurações
├── requirements.txt   ← Deps Python
├── setup-windows.bat  ← Setup automático
└── README.md
```

### Separação core vs wrapper

- `transcribe.py` → migra pro sistema-os (async + repo pattern)
- `dictation.py` → roda em qualquer PC Windows com Python

### Alinhamento com sistema-os

Confirmado: Python/FastAPI, mesmo config pattern (BaseSettings + env vars), já tem ANTHROPIC_API_KEY.

Caminho de migração:
```
ai-brain/tools/whisper-dictation/transcribe.py
    ↓
sistema-os/app/services/transcribe/transcribe_service.py
sistema-os/app/api/v1/endpoints/transcribe.py
sistema-os/app/models/transcription.py
sistema-os/app/schemas/transcription.py
```

## Setup por máquina

### Pré-requisitos (1 vez no Windows)
1. Python 3.11 (python.org, "Add to PATH")
2. OPENAI_API_KEY nas variáveis de ambiente

### Instalação guiada

```bash
# No WSL (faz a parte automática e mostra os comandos do Windows):
bash ~/ai-brain/tools/whisper-dictation/install.sh
```

### Instalação manual detalhada

Ver `tools/whisper-dictation/SETUP.md` — inclui todas as lições aprendidas.

> **Lições do primeiro setup:**
> - Usar Python 3.11 (não 3.14 alpha — incompatibilidades com libs)
> - `pip` pode não estar no PATH → usar `py -3.11 -m pip`
> - Caminhos `\\wsl.localhost\` falham com Python → copiar via `/mnt/c/` do WSL
> - Nome da distro WSL pode variar (ex: `Ubuntu-22.04`, não `Ubuntu`)

## Progresso

### Fase 1: Dictation pessoal
- [x] Pesquisa de ferramentas (7 opções avaliadas)
- [x] Decisão arquitetural (Whisper API + Python)
- [x] Validação com sistema-os (patterns confirmados)
- [x] Código criado (transcribe.py + dictation.py)
- [x] Python instalado no Windows (3.11 — 3.14 alpha removido)
- [x] API key OpenAI criada e configurada
- [x] Deps instaladas (py -3.11 -m pip install)
- [x] Teste funcional (hotkey + mic + transcrição pt-BR)
- [x] Autostart configurado (setup-startup.bat → VBS na pasta Startup)
- [ ] Teste em VSCode terminal, browser, notepad

### Fase 2: sistema-os POPs (futuro)
- [ ] Endpoint FastAPI para upload de áudio
- [ ] TranscribeService (async, repo pattern)
- [ ] Frontend: botão "gravar" nas telas de POP
- [ ] Modelo Transcription no banco

### Fase 3: App mobile (futuro)
- [ ] PWA com MediaRecorder API
- [ ] Interface conversacional
- [ ] ElevenLabs para text-to-speech

## Custo

- Whisper API: ~$0.006/min (~R$0.03/min)
- 30 min/dia ≈ R$27/mês
- Irrisório comparado com alternativas comerciais ($5-15/mês)
