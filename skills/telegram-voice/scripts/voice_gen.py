#!/usr/bin/env python3
"""Generate Telegram-compatible OGG/Opus voice from text via Edge-TTS + ffmpeg."""

import argparse
import asyncio
import os
import re
import subprocess
import sys
import uuid


def clean_markdown(text: str) -> str:
    """Strip markdown formatting for natural speech."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # [link](url) → link
    text = re.sub(r"```[\s\S]*?```", "", text)  # code blocks
    text = re.sub(r"`([^`]+)`", r"\1", text)  # inline code
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*([^*]+)\*", r"\1", text)  # italic
    text = re.sub(r"~~([^~]+)~~", r"\1", text)  # strikethrough
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)  # headings
    text = re.sub(r"^[>\-*]\s+", "", text, flags=re.MULTILINE)  # blockquote/list
    text = re.sub(r"\n{3,}", "\n\n", text)  # extra newlines
    return text.strip()


async def generate(text: str, voice: str, rate: str, outdir: str) -> str:
    """Edge-TTS → MP3 → ffmpeg → OGG/Opus."""
    try:
        import edge_tts
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "edge-tts", "-q"],
            stdout=subprocess.DEVNULL,
        )
        import edge_tts

    uid = uuid.uuid4().hex[:8]
    mp3_path = os.path.join(outdir, f"voice_{uid}.mp3")
    ogg_path = os.path.join(outdir, f"voice_{uid}.ogg")

    # Edge-TTS → MP3 (always works)
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(mp3_path)

    # ffmpeg: MP3 → OGG/Opus (Telegram voice compatible)
    result = subprocess.run(
        [
            "ffmpeg", "-y", "-i", mp3_path,
            "-c:a", "libopus",
            "-b:a", "48k",
            "-vbr", "on",
            "-application", "voip",
            "-ar", "48000",
            "-ac", "1",
            ogg_path,
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr.decode()}", file=sys.stderr)
        # Fallback: return MP3 if ffmpeg fails
        print(mp3_path)
        return mp3_path

    # Cleanup MP3
    try:
        os.remove(mp3_path)
    except OSError:
        pass

    print(ogg_path)
    return ogg_path


def main():
    parser = argparse.ArgumentParser(description="Edge-TTS + ffmpeg voice generator")
    parser.add_argument("-t", "--text", required=True, help="Text to convert to speech")
    parser.add_argument("--voice", default="ru-RU-SvetlanaNeural", help="Edge TTS voice")
    parser.add_argument("--rate", default="+0%", help="Speech rate (e.g. +10%, -5%)")
    parser.add_argument("--outdir", default="/tmp", help="Output directory")
    parser.add_argument("--no-clean", action="store_true", help="Skip markdown cleaning")
    args = parser.parse_args()

    text = args.text if args.no_clean else clean_markdown(args.text)

    if not text:
        print("Error: empty text after cleaning", file=sys.stderr)
        sys.exit(1)

    asyncio.run(generate(text, args.voice, args.rate, args.outdir))


if __name__ == "__main__":
    main()
