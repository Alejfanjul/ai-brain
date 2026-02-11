@echo off
echo ============================================
echo   Whisper Dictation - Configurar Autostart
echo ============================================
echo.

set "DICTATION_DIR=C:\Users\%USERNAME%\whisper-dictation"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_DIR%\WhisperDictation.vbs"

REM Verifica se watchdog.py existe
if not exist "%DICTATION_DIR%\watchdog.py" (
    echo [ERRO] watchdog.py nao encontrado em %DICTATION_DIR%
    echo        Copie a pasta whisper-dictation para C:\Users\%USERNAME%\
    exit /b 1
)

REM Cria VBScript que roda watchdog minimizado (7 = SW_SHOWMINNOACTIVE)
REM IMPORTANTE: usar 7 em vez de 0 (SW_HIDE) — janela oculta quebra hooks de teclado
echo Creating startup script...
(
    echo Set WshShell = CreateObject("WScript.Shell"^)
    echo WshShell.Run "py -3.11 ""%DICTATION_DIR%\watchdog.py""", 7, False
) > "%SHORTCUT%"

if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar atalho de startup.
    exit /b 1
)

echo.
echo [OK] Autostart configurado!
echo     Arquivo: %SHORTCUT%
echo     O watchdog.py vai iniciar automaticamente com o Windows.
echo     Ele mantem o dictation.py rodando e reinicia se necessario.
echo     Para remover: delete o arquivo acima.
echo.
echo     Logs em:
echo       %DICTATION_DIR%\whisper_dictation.log
echo       %DICTATION_DIR%\whisper_watchdog.log
echo.
pause
