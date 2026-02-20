---
name: syntx-video
description: Generate AI videos via syntx.ai REST API. Supports 50+ models including Kling, Veo3, Sora, Runway, Luma, Seedance, Grok Video. Use when the user asks to create, generate, or make a video using AI. Requires SYNTX_AUTH_TOKEN for REST API access.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "env": ["SYNTX_AUTH_TOKEN"] },
        "primaryEnv": "SYNTX_AUTH_TOKEN",
      },
  }
---

# syntx-video — AI Video Generation via REST API

Generate AI videos through syntx.ai REST API (50+ models). Three-step process: create chat → generate → poll for result.

## Available Models

| User says    | model_type          | ai_name          | Quality   | Speed   | Cost       |
| ------------ | ------------------- | ---------------- | --------- | ------- | ---------- |
| kling        | kling_text2video    | kling            | High      | 2-5 min | ~21 tokens |
| kling o1     | kling_o1_text2video | kling            | High      | 2-5 min | ~10 tokens |
| veo3         | veo3                | veo3             | Very high | 3-8 min | ~30 tokens |
| veo3 fast    | veo3fast            | veo3             | High      | 1-3 min | ~15 tokens |
| sora         | sora_1              | sora             | High      | 3-6 min | ~15 tokens |
| sora 2       | sora_2              | sora             | High      | 3-6 min | ~20 tokens |
| runway       | text2video          | runway           | Good      | 2-4 min | ~10 tokens |
| runway gen4  | 4genfirstframeimage | runway           | Good      | 2-4 min | ~15 tokens |
| luma         | ray-v2              | luma             | Good      | 1-3 min | ~5 tokens  |
| luma v3      | ray-v3              | luma             | Good      | 2-4 min | ~10 tokens |
| seedance     | seedance_lite       | seedance         | Good      | 2-5 min | ~10 tokens |
| seedance pro | seedance_pro        | seedance         | High      | 3-6 min | ~15 tokens |
| midjourney   | midjourney-video    | midjourney-video | High      | 3-6 min | ~15 tokens |
| grok video   | grok_t2v            | grok             | Good      | 2-4 min | ~10 tokens |

Default model: **kling** (best quality/speed balance). Budget option: **kling o1** (~10 tokens).

## Step 1: Create Video Chat

```bash
exec: curl -s -X POST "https://api.syntx.ai/api/v1/chats" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"scope": "video", "ai_name": "<AI_NAME>", "title": "Video Generation"}'
```

**Response:** `{"id": 123, "uuid": "176b76a9-...", ...}`

Save the `uuid` value — you need it for Steps 2 and 3.

## Step 2: Start Generation

```bash
exec: curl -s --max-time 30 -X POST "https://api.syntx.ai/api/v1/video/generate?ai_name=<AI_NAME>" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "<CHAT_UUID>", "model": "<MODEL_TYPE>", "prompt": "<PROMPT>", "settings": {"model_type": "<MODEL_TYPE>"}}'
```

**Response:** `{"id": 80361596, "message_object": [{"token_cost": 21.0, "task_id": "89a337f2-..."}]}`

## Step 3: Poll for Result

Wait 30 seconds, then poll every 15 seconds until `completed: true`:

```bash
exec: curl -s "https://api.syntx.ai/api/v1/chats/<CHAT_UUID>/messages" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN"
```

**Look for:** In the `messages` array, find the message with `author_id: -1` (bot response). Check its `message_object[0]`:

- `completed: false` → still generating, poll again in 15 seconds
- `completed: true` → done! Get `object_url` — this is the video URL

**Response when done:**

```json
{
  "message_object": [
    {
      "object_type": "video",
      "object_url": "https://r2.syntx.ai/user_.../generated/....mp4",
      "completed": true,
      "metadata": {
        "duration": 5.04,
        "preview_url": "https://r2.syntx.ai/user_.../thumbnails/video_thumb_....jpg"
      }
    }
  ]
}
```

## Deliver Video to User

After getting `object_url` from Step 3:

```
MEDIA:<object_url>
```

Example: `MEDIA:https://r2.syntx.ai/user_5160049188/generated/02ef663b55dff65c2ce1dddb85080cd4.mp4`

## Check Balance

```bash
exec: curl -s "https://api.syntx.ai/api/v1/user/balance" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN"
```

Response: `{"balance": 189.854, "user_id": "5160049188"}`

## Important Rules

1. **ALWAYS check balance** before generating if the user hasn't generated recently
2. **Tell the user** generation takes 1-8 minutes — set expectations
3. **Poll every 15 seconds** after initial 30s wait. Max 40 polls (10 min timeout).
4. **One generation at a time** — don't send multiple requests simultaneously
5. **Prompt language**: works in both Russian and English. Be descriptive for better results.
6. **If generation fails** or polls timeout, tell the user and suggest a different model
7. **Reuse chat_id** — you can generate multiple videos in the same chat
8. **model_type in settings MUST match the model field** — they are always the same value

## Example Interaction

**User:** "Сгенерируй видео: кот играет с мячом в парке"

**You should:**

1. Check balance: `curl ... /api/v1/user/balance` → "189 токенов, достаточно"
2. Acknowledge: "Генерирую видео через Kling (kling_text2video). Это займёт 2-5 минут..."
3. Create chat: `curl ... /api/v1/chats` → get uuid
4. Generate: `curl ... /api/v1/video/generate?ai_name=kling` with prompt
5. Poll: `curl ... /chats/<uuid>/messages` every 15s
6. On success: "Готово! Видео сгенерировано. 21 токен.\nMEDIA:https://r2.syntx.ai/..."
7. On failure: "Не удалось сгенерировать видео. Попробовать другую модель?"

**User:** "Сделай видео через Sora: закат над океаном"

**You should:**

1. Use ai_name="sora", model_type="sora_1"
2. "Генерирую через Sora. Обычно занимает 3-6 минут..."
