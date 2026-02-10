# Setup manual — Whisper Dictation

Passo a passo para instalação em uma nova máquina Windows.
Todas as lições aprendidas de setups anteriores estão documentadas aqui.

## Pré-requisitos

- Windows 10/11
- Microfone funcionando
- Conta na OpenAI com crédito (API key)

## 1. Python 3.11 no Windows

- Baixar de https://python.org (versão 3.11.x, **não** alpha/beta)
- **IMPORTANTE:** Marcar "Add to PATH" durante instalação
- Verificar no PowerShell: `py -3.11 --version`

> **Lição:** Python 3.14 alpha causa incompatibilidades com libs (numpy, scipy).
> Usar 3.11 que é o mesmo do sistema-os.

> **Lição:** `pip` pode não estar no PATH mesmo com Python instalado.
> Sempre usar `py -3.11 -m pip` em vez de `pip` direto.

## 2. API key da OpenAI

Configurar variável de ambiente no Windows:
- Settings > System > Advanced > Environment Variables > New (em System variables)
- Nome: `OPENAI_API_KEY`
- Valor: `sk-...`
- Criar chave em: https://platform.openai.com/api-keys
- **Fechar e reabrir o PowerShell** após configurar (env vars só carregam em novas janelas)

## 3. Copiar arquivos para Windows

**Do WSL** (caminho confiável):

```bash
# Se a pasta destino NÃO existe ainda:
cp -r ~/ai-brain/tools/whisper-dictation /mnt/c/Users/$USER/whisper-dictation

# Se a pasta destino JÁ existe (atualizar arquivos):
cp -f ~/ai-brain/tools/whisper-dictation/*.py ~/ai-brain/tools/whisper-dictation/*.bat ~/ai-brain/tools/whisper-dictation/*.md ~/ai-brain/tools/whisper-dictation/*.json ~/ai-brain/tools/whisper-dictation/*.txt /mnt/c/Users/$USER/whisper-dictation/
```

> **Lição:** `cp -r source dest` quando `dest` já existe cria `dest/source/` (pasta aninhada).
> Para atualizar, usar `cp -f` com globs explícitos (`*.py`, `*.bat`, etc.).

> **Lição:** Acessar WSL via `\\wsl.localhost\` no PowerShell falha com Python.
> Copiar via `/mnt/c/` do lado WSL é o caminho confiável.

## 4. Instalar dependências Python

No PowerShell:

```powershell
py -3.11 -m pip install openai sounddevice keyboard pyperclip numpy scipy pystray pillow
```

Todas as deps estão em `requirements.txt`. Libs de feedback sonoro (`winsound`, `io`, `wave`) são stdlib do Python — não precisam instalar.

> **Nota:** `pystray` e `pillow` são para o ícone na system tray (opcional). Se não estiverem instalados, o dictation funciona normalmente sem ícone.

## 5. Testar

No PowerShell:

```powershell
py -3.11 "C:\Users\Alejandro\whisper-dictation\dictation.py"
```

Deve mostrar:
```
Whisper Dictation ativo.
  Hotkey: F9
  Idioma: pt
  Log: C:\Users\Alejandro\whisper-dictation\whisper_dictation.log
  Aperte F9 para gravar. Aperte de novo para transcrever.
```

Aperta F9 → beep grave (gravando) → fala → aperta F9 → beep agudo (transcrevendo) → beep mais agudo (texto colado).

> **Lição:** Se não ouvir beeps, verificar se o áudio do sistema funciona (testar com YouTube).
> Os beeps usam `winsound.PlaySound` (mesma saída de áudio do sistema).
> Fones Bluetooth têm latency de wake-up — por isso os sons têm fade-in de 350ms embutido.

## 6. Configurar autostart (via watchdog)

No PowerShell, dentro da pasta:

```powershell
cd C:\Users\Alejandro\whisper-dictation
.\setup-startup.bat
```

Isso cria um VBScript na pasta Startup do Windows que roda `watchdog.py` minimizado no boot.
O watchdog mantém `dictation.py` sempre rodando e reinicia automaticamente se o processo morrer.

Para remover: deletar `WhisperDictation.vbs` de:
`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

## Arquitetura

```
[Windows Boot]
  └→ VBScript (Startup folder)
       └→ watchdog.py (monitora e reinicia se morrer)
            └→ dictation.py (hotkey F9 + mic + Whisper API + paste)
                 └→ transcribe.py (Whisper API — core reusável para sistema-os)
```

**Proteções:**

| Proteção | Como funciona |
|----------|---------------|
| **Singleton** | Lock file com PID — nova instância mata a anterior automaticamente |
| **F9 sempre responsivo** | Transcrição roda em thread separada, hotkey nunca trava |
| **Timeout API** | 30 segundos max, 1 retry automático |
| **Auto-restart** | Watchdog reinicia se processo morrer (max 5x em 5 min) |
| **Feedback sonoro** | Tons distintos via winsound.PlaySound (compatível com Bluetooth) |
| **System tray icon** | Bolinha colorida na barra — cinza/vermelho/amarelo/verde por estado |
| **Logs** | `whisper_dictation.log` e `whisper_watchdog.log` com rotação automática |

## Feedback sonoro

| Evento | Tom | Frequência |
|--------|-----|------------|
| Início gravação (F9) | Grave | 400Hz |
| Fim gravação (F9 de novo) | Médio-agudo | 800Hz |
| Texto colado com sucesso | Agudo | 1200Hz |
| Erro (API, mic, etc.) | Grave longo | 300Hz |
| Ocupado (F9 durante transcrição) | Médio | 600Hz |

Cada tom tem fade-in de 350ms embutido para compatibilidade com fones Bluetooth (que entram em sleep e precisam de tempo para acordar).

## System tray icon

Quando `pystray` e `pillow` estão instalados, aparece um ícone circular na system tray do Windows:

| Estado | Cor | Tooltip |
|--------|-----|---------|
| Pronto | Cinza | "Whisper — Pronto (F9)" |
| Gravando | Vermelho | "Whisper — Gravando..." |
| Transcrevendo | Amarelo | "Whisper — Transcrevendo..." |
| Sucesso (flash 1.5s) | Verde | — |

- Clique direito no ícone → "Sair" para encerrar o processo
- Se o ícone não aparece, as libs não estão instaladas — funciona normalmente sem ele

### Fixar ícone na barra de tarefas

Por padrão o Windows esconde ícones novos na área de overflow (seta `^`). Para fixar:

1. Abrir **Settings > Personalization > Taskbar**
2. Expandir **Other system tray icons**
3. Ativar o toggle do **Python** (ou **Whisper Dictation**)

Alternativa rápida: arrastar o ícone da área de overflow para a barra de tarefas.

## Troubleshooting

### F9 não faz nada

1. **Verificar se o processo está rodando:**
   - Task Manager → procurar `python` ou `py`
   - Se não está: rodar manualmente para ver erros:
     ```powershell
     py -3.11 "C:\Users\Alejandro\whisper-dictation\dictation.py"
     ```

2. **Verificar logs:**
   ```powershell
   type "C:\Users\Alejandro\whisper-dictation\whisper_dictation.log"
   type "C:\Users\Alejandro\whisper-dictation\whisper_watchdog.log"
   ```

3. **Múltiplas instâncias:**
   - O singleton resolve isso automaticamente (mata instância anterior)
   - Se persistir: `taskkill /f /im python.exe` e reiniciar

### Não ouve beeps

1. Testar áudio do sistema (YouTube, etc.)
2. Testar `winsound` isolado:
   ```powershell
   py -3.11 -c "import winsound; winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)"
   ```
3. Fone Bluetooth: os sons já têm fade-in de 350ms para compatibilidade
4. Verificar log — erros de beep aparecem com `Beep falhou:`

### Texto não cola

1. Verificar API key: `echo %OPENAI_API_KEY%` no PowerShell (deve mostrar `sk-...`)
2. Verificar log para erros de API
3. Verificar microfone: Settings > Sound > Input

### Watchdog reiniciando em loop

- Circuit breaker para após 5 restarts em 5 minutos
- Verificar `whisper_watchdog.log` para o exit code
- Causa comum: dependência faltando ou API key não configurada

## Verificação final

- [ ] `py -3.11 --version` retorna 3.11.x
- [ ] `echo %OPENAI_API_KEY%` retorna a key
- [ ] `F9` emite beep grave ao pressionar (confirma processo ativo)
- [ ] Falar algo → texto aparece colado
- [ ] Funciona em Notepad, browser e VSCode
- [ ] Funciona com fone Bluetooth conectado
- [ ] Funciona após reiniciar o PC (autostart via watchdog)
- [ ] Logs existem em `whisper_dictation.log`
- [ ] Ícone aparece na system tray (cinza = pronto)
- [ ] Ícone muda de cor: vermelho (gravando) → amarelo (transcrevendo) → verde (sucesso)
- [ ] Abrir duas instâncias → segunda assume, primeira morre
