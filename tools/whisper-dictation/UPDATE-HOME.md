# Atualizar Whisper Dictation no PC de casa

## Contexto

O PC do trabalho tem a versão mais recente (RegisterHotKey).
O PC de casa tem mudanças locais NÃO PUSHADAS da noite de 11/02.

## Passos

### 1. Matar o processo atual
```
taskkill /IM pythonw.exe /F
```

### 2. No WSL, sincronizar o repositório
```bash
cd ~/ai-brain
git stash          # salva mudanças locais
git pull           # puxa versão nova (RegisterHotKey)
git stash pop      # tenta reaplicar mudanças locais
```

Se der conflito em `tools/whisper-dictation/dictation.py`:
- A versão do **remote** é a correta (tem RegisterHotKey)
- Resolver conflito aceitando a versão remote
- As mudanças locais (tray inline, logging, singleton, watchdog) já foram incorporadas

### 3. Copiar para Windows
```bash
SRC=~/ai-brain/tools/whisper-dictation
DEST=/mnt/c/Users/USUARIO/whisper-dictation   # ajustar username
cp "$SRC/dictation.py" "$SRC/watchdog.py" "$SRC/setup-startup.bat" "$SRC/requirements.txt" "$DEST/"
```

### 4. Instalar dependências (se necessário)
No PowerShell:
```
py -3.11 -m pip install pystray Pillow
```

### 5. Recriar o autostart
No PowerShell:
```
cd C:\Users\USUARIO\whisper-dictation
.\setup-startup.bat
```
Isso cria o VBScript usando `pyw -3.11` (sem janela de console).

### 6. Testar
```
py -3.11 "C:\Users\USUARIO\whisper-dictation\dictation.py"
```
Deve aparecer: `Hotkey registrada via RegisterHotKey (thread XXXX)`
Testar F9 várias vezes. Se funcionar, fechar e subir via watchdog:
```
pyw -3.11 "C:\Users\USUARIO\whisper-dictation\watchdog.py"
```

### 7. Commit e push (se houver mudanças locais resolvidas)
```bash
cd ~/ai-brain
git add tools/whisper-dictation/
git commit -m "chore: sync whisper-dictation com PC trabalho"
git push
```

## O que mudou (resumo para Claude)

- **RegisterHotKey** substituiu `keyboard.add_hotkey()` — hotkey não morre mais
- **pyw (pythonw.exe)** no startup — sem janela de console
- **State machine** com 5 estados + tray icon colorido
- **Watchdog** reinicia automaticamente se crashar
