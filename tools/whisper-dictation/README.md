# Whisper Dictation

Speech-to-text com hotkey global usando OpenAI Whisper API.

Aperta **F9** → grava → aperta **F9** de novo → transcreve → cola onde o cursor está.

## Setup rápido (nova máquina)

### Pré-requisitos

- Windows com WSL2
- Python 3.11 no Windows (python.org, marcar "Add to PATH")
- API key da OpenAI configurada como variável de ambiente (`OPENAI_API_KEY`)

### Instalação guiada

No WSL, rodar:

```bash
bash ~/ai-brain/tools/whisper-dictation/install.sh
```

O script faz automaticamente:
1. Copia os arquivos para `C:\Users\$USER\whisper-dictation`
2. Mostra os comandos que você precisa rodar no PowerShell

### Instalação manual

Se preferir fazer passo a passo, veja [SETUP.md](SETUP.md).

## Uso

| Ação | Tecla |
|------|-------|
| Toggle gravação | **F9** |
| Sair | Ctrl+C |

1. Aperta `F9` → começa a gravar
2. Fala em português
3. Aperta `F9` de novo → transcreve e cola no cursor

### Trocar hotkey

Editar `config.json`:
```json
{
  "hotkey": "F9",
  "language": "pt",
  "sample_rate": 16000,
  "channels": 1
}
```

### Opções via linha de comando

```powershell
py -3.11 dictation.py --hotkey "ctrl+alt+space" --language en
```

## Arquitetura

```
transcribe.py      ← Core reusável (Whisper API call)
dictation.py       ← Wrapper desktop (hotkey + mic + paste)
config.json        ← Configurações
install.sh         ← Instalação guiada (roda no WSL)
setup-startup.bat  ← Configura autostart com Windows
setup-windows.bat  ← Instala dependências Python
```

O `transcribe.py` é o core que migra pro sistema-os (FastAPI endpoint).
O `dictation.py` é o wrapper desktop que conecta mic + hotkey + clipboard.

## Custo

- Whisper API: ~$0.006/min (~R$0.03/min)
- 30 min/dia ≈ R$27/mês
