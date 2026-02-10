"""
Watchdog — Mantém o dictation.py sempre rodando.

Reinicia automaticamente se o processo morrer.
Circuit breaker: para se crashar mais de 5 vezes em 5 minutos.

Uso:
    python watchdog.py
"""

import logging
import subprocess
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

DICTATION_SCRIPT = Path(__file__).parent / "dictation.py"
LOG_FILE = Path(__file__).parent / "whisper_watchdog.log"

# Circuit breaker: max 5 restarts em 300 segundos
MAX_RESTARTS = 5
WINDOW_SECONDS = 300
RESTART_DELAY = 2

# Logging
logger = logging.getLogger("watchdog")
logger.setLevel(logging.INFO)

_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=500_000, backupCount=1, encoding="utf-8"
)
_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
)
logger.addHandler(_handler)
logger.addHandler(logging.StreamHandler(sys.stdout))


def main():
    python = sys.executable
    restart_times = []

    logger.info(f"Watchdog iniciado. Monitorando: {DICTATION_SCRIPT}")
    logger.info(f"Python: {python}")

    while True:
        # Circuit breaker: limpa restarts fora da janela
        now = time.time()
        restart_times = [t for t in restart_times if now - t < WINDOW_SECONDS]

        if len(restart_times) >= MAX_RESTARTS:
            logger.error(
                f"Circuit breaker: {MAX_RESTARTS} restarts em {WINDOW_SECONDS}s. "
                "Parando watchdog."
            )
            break

        logger.info("Iniciando dictation.py...")
        try:
            proc = subprocess.run(
                [python, str(DICTATION_SCRIPT)],
                cwd=str(DICTATION_SCRIPT.parent),
            )
            exit_code = proc.returncode
        except Exception as e:
            logger.error(f"Erro ao iniciar dictation.py: {e}")
            exit_code = -1

        restart_times.append(time.time())
        logger.warning(f"dictation.py encerrou (exit code: {exit_code}). "
                       f"Reiniciando em {RESTART_DELAY}s...")
        time.sleep(RESTART_DELAY)


if __name__ == "__main__":
    main()
