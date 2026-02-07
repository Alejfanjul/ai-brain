# Setup manual — Whisper Dictation

Passo a passo detalhado para instalação em uma nova máquina.
Todas as lições aprendidas no primeiro setup estão documentadas aqui.

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
- Settings > System > Advanced > Environment Variables > New
- Nome: `OPENAI_API_KEY`
- Valor: `sk-...`
- Criar chave em: https://platform.openai.com/api-keys

## 3. Copiar arquivos do WSL para Windows

No terminal WSL:

```bash
cp -r ~/ai-brain/tools/whisper-dictation /mnt/c/Users/$USER/whisper-dictation
```

> **Lição:** Acessar WSL via `\\wsl.localhost\` no PowerShell falha com Python.
> Copiar via `/mnt/c/` do lado WSL é o caminho confiável.

> **Lição:** O nome da distro WSL pode variar (`Ubuntu-22.04` vs `Ubuntu`).
> Por isso copiar pelo `/mnt/c/` evita esse problema.

## 4. Instalar dependências Python

No PowerShell:

```powershell
py -3.11 -m pip install openai sounddevice keyboard pyperclip numpy scipy
```

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
```

Aperta F9, fala algo, aperta F9 de novo. O texto deve aparecer colado.

## 6. Configurar autostart

No PowerShell, dentro da pasta:

```powershell
cd C:\Users\Alejandro\whisper-dictation
.\setup-startup.bat
```

Cria um VBScript na pasta Startup do Windows que roda o dictation.py minimizado no boot.

Para remover: deletar `WhisperDictation.vbs` de:
`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

## Verificação final

- [ ] `F9` grava e transcreve
- [ ] Texto é colado no Notepad
- [ ] Texto é colado no browser
- [ ] Texto é colado no VSCode
- [ ] Funciona após reiniciar o PC (autostart)
