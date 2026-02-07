"""
Core de transcrição via OpenAI Whisper API.

Módulo reusável — vai pro sistema-os depois.
Sem dependências de desktop (hotkey, mic, clipboard).
"""

from pathlib import Path
from openai import OpenAI


def transcribe_audio(
    audio_file_path: str,
    language: str = "pt",
    model: str = "whisper-1",
) -> str:
    """Transcreve um arquivo de áudio usando a Whisper API da OpenAI.

    Args:
        audio_file_path: Caminho do arquivo de áudio (wav, mp3, m4a, webm, etc.)
        language: Código do idioma (padrão: "pt" para português)
        model: Modelo Whisper a usar

    Returns:
        Texto transcrito

    Raises:
        FileNotFoundError: Se o arquivo não existe
        openai.APIError: Se a API falhar
    """
    path = Path(audio_file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {audio_file_path}")

    client = OpenAI()  # usa OPENAI_API_KEY do ambiente

    with open(path, "rb") as f:
        result = client.audio.transcriptions.create(
            model=model,
            file=f,
            language=language,
        )

    return result.text


def transcribe_bytes(
    audio_bytes: bytes,
    filename: str = "audio.wav",
    language: str = "pt",
    model: str = "whisper-1",
) -> str:
    """Transcreve bytes de áudio diretamente (sem salvar em disco).

    Útil para integração com sistema-os (recebe bytes do upload).

    Args:
        audio_bytes: Dados de áudio em bytes
        filename: Nome do arquivo (para a API inferir formato)
        language: Código do idioma
        model: Modelo Whisper

    Returns:
        Texto transcrito
    """
    client = OpenAI()

    result = client.audio.transcriptions.create(
        model=model,
        file=(filename, audio_bytes),
        language=language,
    )

    return result.text
