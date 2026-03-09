"""Transcribe audio files using OpenAI Whisper API.
Converts to mp3 first (for API compatibility), splits files >25MB.
"""
import os
import subprocess
import tempfile
from pathlib import Path
from openai import OpenAI

AUDIO_DIR = Path(r"C:\Users\aleja\OneDrive\Desktop\voz")
MAX_SIZE = 24 * 1024 * 1024  # 24MB safe limit
FFMPEG_BIN = Path(r"C:\Users\aleja\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin")
FFMPEG = str(FFMPEG_BIN / "ffmpeg.exe")
FFPROBE = str(FFMPEG_BIN / "ffprobe.exe")

client = OpenAI()


def convert_to_mp3(filepath: Path, output: Path) -> Path:
    """Convert any audio to mp3."""
    subprocess.run(
        [FFMPEG, "-y", "-i", str(filepath), "-vn", "-ar", "16000",
         "-ac", "1", "-b:a", "64k", str(output)],
        capture_output=True, check=True
    )
    return output


def get_duration(filepath: Path) -> float:
    """Get audio duration in seconds."""
    result = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(filepath)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def split_mp3(filepath: Path, chunk_duration: int = 600) -> list[Path]:
    """Split mp3 into chunks of chunk_duration seconds."""
    duration = get_duration(filepath)
    chunks = []
    tmpdir = Path(tempfile.mkdtemp())

    start = 0
    i = 0
    while start < duration:
        chunk_path = tmpdir / f"chunk_{i:03d}.mp3"
        subprocess.run([
            FFMPEG, "-y", "-i", str(filepath),
            "-ss", str(start), "-t", str(chunk_duration),
            "-c", "copy", str(chunk_path)
        ], capture_output=True, check=True)
        if chunk_path.exists() and chunk_path.stat().st_size > 0:
            chunks.append(chunk_path)
        start += chunk_duration
        i += 1

    return chunks


def transcribe_file(filepath: Path) -> str:
    """Transcribe a single file (must be under 25MB)."""
    size_mb = filepath.stat().st_size / 1024 / 1024
    print(f"  Transcrevendo: {filepath.name} ({size_mb:.1f} MB)")
    with open(filepath, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="pt",
        )
    return response.text


def process_file(filepath: Path) -> str:
    """Convert to mp3, split if needed, transcribe."""
    tmpdir = Path(tempfile.mkdtemp())
    mp3_path = tmpdir / (filepath.stem + ".mp3")

    print(f"  Convertendo para mp3...")
    convert_to_mp3(filepath, mp3_path)
    mp3_size = mp3_path.stat().st_size
    print(f"  MP3: {mp3_size / 1024 / 1024:.1f} MB")

    if mp3_size <= MAX_SIZE:
        text = transcribe_file(mp3_path)
        os.unlink(mp3_path)
        return text

    # Split and transcribe each chunk
    print(f"  Ainda grande, dividindo...")
    chunks = split_mp3(mp3_path)
    os.unlink(mp3_path)
    print(f"  {len(chunks)} partes")

    texts = []
    for chunk in chunks:
        text = transcribe_file(chunk)
        texts.append(text)
        os.unlink(chunk)

    return "\n\n".join(texts)


def main():
    audio_files = sorted(AUDIO_DIR.glob("*.m4a"))
    print(f"Encontrados {len(audio_files)} arquivos de audio\n")

    for filepath in audio_files:
        print(f"Processando: {filepath.name}")
        try:
            text = process_file(filepath)
            output = filepath.with_suffix(".txt")
            output.write_text(text, encoding="utf-8")
            print(f"  Salvo em: {output.name}")
            print(f"  Preview: {text[:120]}...\n")
        except Exception as e:
            print(f"  ERRO: {e}\n")


if __name__ == "__main__":
    main()
