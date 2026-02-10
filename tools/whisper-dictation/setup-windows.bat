@echo off
echo ============================================
echo   Whisper Dictation - Setup Windows
echo ============================================
echo.

REM Verifica Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado.
    echo        Instale de https://python.org
    echo        IMPORTANTE: Marque "Add to PATH" durante instalacao.
    exit /b 1
)

echo [OK] Python encontrado:
python --version

REM Detecta o caminho do script (funciona tanto via WSL quanto Windows)
set "SCRIPT_DIR=%~dp0"

echo.
echo Instalando dependencias...
pip install -r "%SCRIPT_DIR%requirements.txt"

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao instalar dependencias.
    exit /b 1
)

echo.
echo [OK] Dependencias instaladas.

REM Verifica API key
if "%OPENAI_API_KEY%"=="" (
    echo.
    echo [AVISO] OPENAI_API_KEY nao configurada.
    echo         Configure nas variaveis de ambiente do Windows:
    echo         System ^> Advanced ^> Environment Variables ^> New
    echo         Nome: OPENAI_API_KEY
    echo         Valor: sk-...
    echo.
    echo         Ou crie em: https://platform.openai.com/api-keys
) else (
    echo [OK] OPENAI_API_KEY configurada.
)

echo.
echo ============================================
echo   Setup completo!
echo.
echo   Para usar manualmente:
echo     py -3.11 "%SCRIPT_DIR%dictation.py"
echo.
echo   Para iniciar automaticamente com o Windows:
echo     setup-startup.bat
echo.
echo   Hotkey: veja config.json (padrao F9)
echo ============================================
pause
