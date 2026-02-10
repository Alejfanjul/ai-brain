#!/bin/bash
# Whisper Dictation — Instalação guiada
# Roda no WSL. Faz a parte automática e guia os comandos do Windows.

set -e

DEST="/mnt/c/Users/$USER/whisper-dictation"
SRC="$(dirname "$(realpath "$0")")"

echo "============================================"
echo "  Whisper Dictation — Instalação guiada"
echo "============================================"
echo ""

# --- Passo 1: Verificar pré-requisitos ---
echo "[1/4] Verificando pré-requisitos..."
echo ""

if [ ! -f "$SRC/dictation.py" ]; then
    echo "ERRO: dictation.py não encontrado em $SRC"
    exit 1
fi
echo "  OK: Código fonte encontrado"

if [ ! -d "/mnt/c/Users/$USER" ]; then
    echo "ERRO: Pasta do usuário Windows não encontrada em /mnt/c/Users/$USER"
    echo "      Se seu usuário Windows é diferente, rode:"
    echo "      DEST=/mnt/c/Users/SEU_USUARIO/whisper-dictation bash $0"
    exit 1
fi
echo "  OK: Pasta do usuário Windows encontrada"
echo ""

# --- Passo 2: Copiar arquivos ---
echo "[2/4] Copiando arquivos para Windows..."

if [ -d "$DEST" ]; then
    echo "  Pasta já existe. Atualizando arquivos..."
    cp "$SRC/transcribe.py" "$DEST/"
    cp "$SRC/dictation.py" "$DEST/"
    cp "$SRC/tray.py" "$DEST/"
    cp "$SRC/run.py" "$DEST/"
    cp "$SRC/config.json" "$DEST/"
    cp "$SRC/requirements.txt" "$DEST/"
    cp "$SRC/setup-windows.bat" "$DEST/"
    cp "$SRC/setup-startup.bat" "$DEST/"
else
    cp -r "$SRC" "$DEST"
fi

echo "  OK: Arquivos copiados para $DEST"
echo ""

# --- Passo 3: Comandos do Windows ---
echo "[3/4] Agora rode estes comandos no PowerShell do Windows:"
echo ""
echo "  # Instalar dependências Python:"
echo "  py -3.11 -m pip install -r C:\\Users\\$USER\\whisper-dictation\\requirements.txt"
echo ""
echo "  # Testar:"
echo "  py -3.11 \"C:\\Users\\$USER\\whisper-dictation\\run.py\""
echo ""
echo "  # Configurar autostart (após testar):"
echo "  cd C:\\Users\\$USER\\whisper-dictation"
echo "  .\\setup-startup.bat"
echo ""

# --- Passo 4: Lembrete da API key ---
echo "[4/4] Checklist:"
echo ""
echo "  [ ] OPENAI_API_KEY configurada nas variáveis de ambiente do Windows?"
echo "      Se não: Settings > System > Advanced > Environment Variables > New"
echo "      Nome: OPENAI_API_KEY | Valor: sk-..."
echo ""
echo "  [ ] Python 3.11 instalado no Windows?"
echo "      Se não: https://python.org (marcar 'Add to PATH')"
echo ""
echo "============================================"
echo "  Parte WSL concluída!"
echo "  Siga os comandos acima no PowerShell."
echo "============================================"
