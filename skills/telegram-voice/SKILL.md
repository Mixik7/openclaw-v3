---
name: telegram-voice
description: Generate Telegram voice bubbles from text using Edge-TTS + ffmpeg. Produces OGG/Opus files guaranteed to show as round voice bubbles in Telegram. Use when responding to voice messages or when user requests voice output. Requires ffmpeg in PATH.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "os": ["linux"],
        "requires": { "bins": ["ffmpeg", "python3"] },
        "primaryBin": "ffmpeg",
      },
  }
---

# Telegram Voice Generator

Generate **guaranteed Telegram voice bubbles** 🔵 from text using Edge-TTS + ffmpeg.

## Why this skill exists

The built-in Edge TTS `auto` mode may produce MP3 files that Telegram displays as audio files (📎) instead of voice bubbles (🔵). This skill converts the audio through ffmpeg to OGG/Opus format, which Telegram **always** displays as a round voice bubble.

## When to use

- User sent a **voice message** and you want to reply with voice
- User explicitly asks for a **voice reply** or **audio response**
- You want to send a **voice note** in Telegram

## Usage

```bash
python3 {baseDir}/scripts/voice_gen.py -t "Привет! Это голосовое сообщение от IDEA."
```

The script outputs the path to the generated `.ogg` file. Use it with `MEDIA:` prefix to send:

```
MEDIA:/tmp/voice_abc123.ogg
[[audio_as_voice]]
```

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `-t`, `--text` | (required) | Text to convert to speech |
| `--voice` | `ru-RU-SvetlanaNeural` | Edge TTS voice name |
| `--rate` | `+0%` | Speech rate: `+10%` faster, `-5%` slower |
| `--outdir` | `/tmp` | Output directory for OGG files |
| `--no-clean` | false | Skip markdown stripping |

## Available voices

| Voice | Language | Gender |
|-------|----------|--------|
| `ru-RU-SvetlanaNeural` | Russian | Female (default) |
| `ru-RU-DmitryNeural` | Russian | Male |
| `en-US-JennyNeural` | English | Female |
| `en-US-GuyNeural` | English | Male |

## Example: Reply to voice message

When user sends a voice message, generate your response as voice:

```bash
# Generate voice reply
OGG_PATH=$(python3 {baseDir}/scripts/voice_gen.py -t "Вот результат анализа: канал вырос на 15% за неделю.")

# The script prints the OGG path to stdout
# Use it in your response with MEDIA: prefix
```

Then include in your response:
```
MEDIA:/tmp/voice_abc123.ogg
[[audio_as_voice]]
```

## Dependencies

- **ffmpeg** — installed via `OPENCLAW_DOCKER_APT_PACKAGES` in railway.toml
- **python3** — included in node:22-bookworm base image
- **edge-tts** — auto-installed on first run via pip

## Pipeline

```
Text → clean markdown → Edge-TTS → MP3 → ffmpeg (libopus) → OGG/Opus → 🔵 voice bubble
```
