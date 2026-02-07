@echo off
echo ============================================
echo   Whisper Dictation - Configurar Autostart
echo ============================================
echo.

set "DICTATION_DIR=C:\Users\%USERNAME%\whisper-dictation"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_DIR%\WhisperDictation.vbs"

REM Verifica se dictation.py existe
if not exist "%DICTATION_DIR%\dictation.py" (
    echo [ERRO] dictation.py nao encontrado em %DICTATION_DIR%
    echo        Copie a pasta whisper-dictation para C:\Users\%USERNAME%\
    exit /b 1
)

REM Cria VBScript que roda minimizado (sem janela preta)
echo Creating startup script...
(
    echo Set WshShell = CreateObject("WScript.Shell"^)
    echo WshShell.Run "py -3.11 ""%DICTATION_DIR%\dictation.py""", 0, False
) > "%SHORTCUT%"

if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar atalho de startup.
    exit /b 1
)

echo.
echo [OK] Autostart configurado!
echo     Arquivo: %SHORTCUT%
echo     O dictation.py vai iniciar automaticamente com o Windows.
echo     Para remover: delete o arquivo acima.
echo.
pause
