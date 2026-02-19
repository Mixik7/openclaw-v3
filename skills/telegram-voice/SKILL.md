---
name: telegram-voice
description: Generate Telegram voice bubbles from text using Node edge-tts + ffmpeg. Produces OGG/Opus files that show as round voice bubbles in Telegram. MUST use when responding to voice messages. Requires ffmpeg in PATH.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "os": ["linux"],
        "requires": { "bins": ["ffmpeg"] },
        "primaryBin": "ffmpeg",
      },
  }
---

# Telegram Voice Generator

Generate **guaranteed Telegram voice bubbles** from text using the built-in Node `edge-tts` module + ffmpeg.

## WHEN TO USE — MANDATORY

**ALWAYS use this method when the user sends a voice message.** This is not optional.

## How it works

You already have access to `edge-tts` (Node module bundled with OpenClaw) and `ffmpeg` (installed via apt). Use them together:

### Step 1: Generate MP3 via Edge TTS (Node)

Use the built-in TTS tool or edge-tts Node API to generate audio. The default voice is `ru-RU-SvetlanaNeural`.

### Step 2: Convert MP3 → OGG/Opus via ffmpeg

```bash
ffmpeg -y -i /tmp/voice_input.mp3 -c:a libopus -b:a 48k -vbr on -application voip -ar 48000 -ac 1 /tmp/voice_output.ogg
```

### Step 3: Send as voice bubble

Include in your response:
```
MEDIA:/tmp/voice_output.ogg
[[audio_as_voice]]
```

## Settings

| Setting | Value |
|---------|-------|
| Voice | `ru-RU-SvetlanaNeural` (Russian female) |
| Format | OGG/Opus via ffmpeg |
| Bitrate | 48kbps |
| Sample rate | 48kHz mono |

## Available voices

| Voice | Language | Gender |
|-------|----------|--------|
| `ru-RU-SvetlanaNeural` | Russian | Female (default) |
| `ru-RU-DmitryNeural` | Russian | Male |

## Rules

- Voice message in → voice bubble out (ALWAYS)
- Text message in → text out (NEVER send unsolicited voice)
- Keep voice responses concise (under 60 seconds)
- Clean markdown from text before TTS (remove `**`, `#`, links, code blocks)

## Pipeline

```
Text → clean markdown → Edge TTS (Node) → MP3 → ffmpeg (libopus) → OGG/Opus → 🔵
```
