---
name: syntx
description: "Access syntx.ai — 148 AI models for text, image, video, and audio generation. Text (51 models, free): Claude Opus/Sonnet, GPT-5, Gemini 3 Pro, Grok 4, Perplexity Sonar, DeepSeek, Qwen. Image (35 models): Nano Banana PRO, MidJourney v7, Flux, Seedream, Imagen 4. Video (50+ models): Kling, Runway, Veo 3.1, SORA 2, Luma, Seedance. Audio (9 models): SUNO v4, ElevenLabs Voice. Use when the user asks to generate video, image, text via syntx, or check syntx balance/status. Requires SYNTX_AUTH_TOKEN environment variable."
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

# syntx.ai — Unified AI Generation (148 models)

Access syntx.ai aggregator: text, image, video, and audio generation across 148 models.

## Platform

- **Base URL:** `https://api.syntx.ai/api/v1/`
- **Auth:** `Authorization: Bearer $SYNTX_AUTH_TOKEN`
- **CDN:** `https://r2.syntx.ai/`
- **Subscription:** VIP. Text models free (∞). Image/video/audio by included limits + purchasable tokens.

## Route by Request Type

| Request               | API Pattern      | Endpoint                                           |
| --------------------- | ---------------- | -------------------------------------------------- |
| Generate video        | Direct REST      | `POST /video/generate`                             |
| Generate image        | Direct REST      | `POST /design/generate`                            |
| Generate text         | TG-Kombain proxy | `POST $TG_KOMBAIN_API_URL/api/n8n/syntx-text`      |
| Generate music/audio  | Direct REST      | (same as video pattern)                            |
| Check balance         | Direct REST      | `GET /user/balance`                                |
| Check JWT status      | TG-Kombain       | `GET $TG_KOMBAIN_API_URL/api/n8n/syntx-jwt-status` |
| Reset circuit breaker | TG-Kombain       | `POST $TG_KOMBAIN_API_URL/api/n8n/syntx-cb-reset`  |

---

## Pattern A: Video Generation (direct REST)

### Step 1. Create Video Chat

```bash
curl -s -X POST "https://api.syntx.ai/api/v1/chats" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Video Gen", "scope": "video"}'
```

Returns `{"uuid": "<CHAT_UUID>", ...}`.

### Step 2. Start Generation

```bash
curl -s -X POST "https://api.syntx.ai/api/v1/video/generate?ai_name=<AI_NAME>" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "<CHAT_UUID>",
    "model": "<MODEL_TYPE>",
    "prompt": "description of the video",
    "settings": { "model_type": "<MODEL_TYPE>" }
  }'
```

`model` and `settings.model_type` MUST match.

### Step 3. Poll for Result

Wait 30s, then poll every 15s (max 40 polls):

```bash
curl -s "https://api.syntx.ai/api/v1/chats/<CHAT_UUID>/messages?page_size=5" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN"
```

Look for `author_id: -1`, `completed: true`, extract `object_url` from `message_object`.

Deliver to user: `MEDIA:<object_url>`

### Video Models

| User says            | model_type          | ai_name            |
| -------------------- | ------------------- | ------------------ |
| Kling                | `kling_text2video`  | `kling`            |
| Kling image-to-video | `kling_image2video` | `kling`            |
| Kling video-to-video | `kling_video2video` | `kling`            |
| Kling o1             | `kling_o1`          | `kling`            |
| Kling Elements v3    | `kling_elements_3`  | `kling`            |
| Kling v3             | `kling_3`           | `kling`            |
| Veo 3.1              | `veo3`              | `veo3`             |
| Veo 3.1 Fast         | `veo3fast`          | `veo3`             |
| Veo 3.1 Fast Relax   | `veo3fast_r`        | `veo3`             |
| VEO Editor           | `veo_editor`        | `veo3`             |
| SORA 1               | `sora_1`            | `sora`             |
| SORA 2               | `sora_2`            | `sora`             |
| Runway text2video    | `text2video`        | `runway`           |
| Runway Gen 4         | `gen4`              | `runway`           |
| Runway Gen 4.5       | `gen4_5`            | `runway`           |
| Runway Aleph         | `runway_aleph`      | `runway`           |
| Runway Frames        | `runway_frames`     | `runway-frames`    |
| Luma Ray v2          | `ray-v2`            | `luma`             |
| Luma Ray v2 Flash    | `ray-v2-flash`      | `luma`             |
| Luma Ray v3          | `ray-v3`            | `luma`             |
| Seedance Lite        | `seedance_lite`     | `seedance`         |
| Seedance Pro         | `seedance_pro`      | `seedance`         |
| Seedance Pro Fast    | `seedance_pro-fast` | `seedance`         |
| Seedance 1.5 Pro     | `seedance_1.5-pro`  | `seedance`         |
| Wan 2.6 text2video   | `wan_26_t2v`        | `wan_video`        |
| Wan 2.6 image2video  | `wan_26_i2v`        | `wan_video`        |
| Wan 2.5              | `wan_25_t2v`        | `wan_video`        |
| Grok Video text      | `grok_t2v`          | `grok_video`       |
| Grok Video image     | `grok_i2v`          | `grok_video`       |
| MidJourney Video     | `midjourney-video`  | `midjourney-video` |
| Hailuo MiniMax       | `minimax`           | `minimax`          |
| Hailuo MiniMax v2.3  | `minimax_v2.3`      | `minimax`          |
| Higgsfield           | `dop-lite`          | `higgsfield`       |
| Higgsfield Speak     | `higgsfield-speak`  | `higgsfield-soul`  |
| HeyGen v4.1          | `heygen4`           | `heygen`           |
| Pika v2.0            | `pika_v2`           | `pika`             |
| Topaz AI             | `topaz_enhance`     | `topaz_ai`         |
| Hedra                | `hedra`             | `hedra`            |
| Lip Sync (Kling)     | `kling_lipsync`     | `kling`            |
| Lip Sync (RunWay)    | `runway_lipsync`    | `runway`           |
| Kling Motion Control | `kling_motion`      | `kling`            |

Default model: **kling** (best quality/speed balance).

---

## Pattern B: Image Generation (direct REST)

### Step 1. Create Image Chat

```bash
curl -s -X POST "https://api.syntx.ai/api/v1/chats" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Image Gen", "scope": "image"}'
```

### Step 2. Generate Image

```bash
curl -s -X POST "https://api.syntx.ai/api/v1/design/generate?ai_name=<AI_NAME>" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_uuid": "<CHAT_UUID>",
    "prompt": "image description",
    "settings": {
      "n": 1,
      "image_url": [],
      "model_type": "<MODEL_TYPE>",
      "aspect_ratio": "1:1",
      "image_size": "2K"
    }
  }'
```

**Important:** Use `POST /design/generate` (NOT `/chats/{uuid}/messages` — that returns 402 for images).

### Step 3. Poll for Result

```bash
# Wait until not generating:
curl -s "https://api.syntx.ai/api/v1/chats/<CHAT_UUID>/inprogress" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN"
# When empty [] -> fetch result:
curl -s "https://api.syntx.ai/api/v1/chats/<CHAT_UUID>/messages?page_size=5" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN"
```

Look for `author_id: -1`, `completed: true`, extract `object_url`. Deliver: `MEDIA:<object_url>`

### Settings Fields

| Field          | Required    | Values                                                   |
| -------------- | ----------- | -------------------------------------------------------- |
| `n`            | Yes         | Always `1`                                               |
| `image_url`    | Yes         | `[]` for text-to-image, or array of reference image URLs |
| `model_type`   | Yes         | Exact model type (e.g., `banana2`, `flux-pro-1.1`)       |
| `aspect_ratio` | Yes         | `1:1`, `3:4`, `9:16`, `16:9`, `4:3`                      |
| `image_size`   | banana only | `1K`, `2K`, `4K`                                         |

### Model-Specific Required Params

| ai_name    | Required param    | Values                                                           |
| ---------- | ----------------- | ---------------------------------------------------------------- |
| banana     | `image_size`      | 1K, 2K, 4K                                                       |
| midjourney | `rendering_speed` | normal, turbo                                                    |
| flux       | —                 | —                                                                |
| imagen4    | —                 | —                                                                |
| seedream   | —                 | model_type must be `seedream-4`, `seedream-4.5`, or `seedream-5` |

### Image Models

| User says             | model_type                | ai_name             |
| --------------------- | ------------------------- | ------------------- |
| Nano Banana           | `banana`                  | `banana`            |
| Nano Banana Pro       | `banana2`                 | `banana`            |
| Nano Banana 2         | `banana3`                 | `banana`            |
| MidJourney v7         | `imagine`                 | `midjourney`        |
| MidJourney Editor     | `midjourney-editor`       | `midjourney_editor` |
| Flux 1.1 Pro          | `flux-pro-1.1`            | `flux`              |
| Flux 1.1 Pro Ultra    | `flux-pro-1.1-ultra`      | `flux`              |
| Flux Kontext Pro      | `flux-kontext-pro`        | `flux`              |
| Flux Kontext Max      | `flux-kontext-max`        | `flux`              |
| Flux Kontext Multi    | `flux-kontext-multi`      | `flux`              |
| Seedream 4            | `seedream-4`              | `seedream`          |
| Seedream 4.5          | `seedream-4.5`            | `seedream`          |
| Seedream 5            | `seedream-5`              | `seedream`          |
| Google Imagen 4       | `google-imagen-4-preview` | `imagen4`           |
| Google Imagen 4 Ultra | `google-imagen-4-ultra`   | `imagen4`           |
| Sora GPT Image        | `gpt-image-1`             | `sora-images`       |
| Sora GPT Image 1.5    | `gpt-image-1.5`           | `sora-images`       |
| Ideogram v3           | `ideogram`                | `ideogram`          |
| Recraft v3            | `recraft-v3`              | `recraft`           |
| Clarity Upscale       | `clarity`                 | `clarity`           |
| Dall-e 3 Turbo        | `dall-e-3-turbo`          | `dalle`             |
| Kling Kolors          | `kling-kolors`            | `kling_kolors`      |
| Wan Image             | `wan_26_t2i`              | `wan_image`         |
| Stable Diffusion      | `stable-diffusion`        | `stable_diffusion`  |

Default model: **banana2** (Nano Banana Pro, 2K — best for Russian text on images).

---

## Pattern C: Text Generation (via TG-Kombain proxy)

Text requires WebSocket (curl can't do WS streaming). Use TG-Kombain proxy:

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/n8n/syntx-text" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "opus",
    "prompt": "your prompt here",
    "system_prompt": "optional system prompt"
  }'
```

Returns: `{"ok": true, "text": "AI response...", "model": "claude-opus-4-6", "token_cost": 0}`.

All text models are **free** (0 tokens).

### Text Model Aliases

| Alias        | model_type                  | ai_name      |
| ------------ | --------------------------- | ------------ |
| opus         | `claude-opus-4-6`           | `claude`     |
| sonnet       | `claude-sonnet-4-6`         | `claude`     |
| haiku        | `claude-3-5-haiku-20241022` | `claude`     |
| sonar        | `sonar`                     | `perplexity` |
| sonar-pro    | `sonar-pro`                 | `perplexity` |
| sonar-deep   | `sonar-deep-research`       | `perplexity` |
| gpt-5        | `gpt-5`                     | `chatgpt`    |
| gpt-5.4      | `gpt-5.4`                   | `chatgpt`    |
| gpt-4.1      | `gpt-4.1-2025-04-14`        | `chatgpt`    |
| gemini       | `gemini-3-pro-preview`      | `gemini`     |
| gemini-flash | `gemini-2.5-flash`          | `gemini`     |
| grok         | `grok-4`                    | `grok`       |
| grok-3       | `grok-3`                    | `grok`       |
| deepseek     | `deepseek-r1`               | `deepseek`   |
| deepseek-v3  | `deepseek-v3`               | `deepseek`   |
| qwen         | `qwen3-235b-a22b`           | `qwen`       |

### All 51 Text Models

Claude (Opus 4.6, Sonnet 4.6, Opus 4.5, Sonnet 4.5, Opus 4.1, Sonnet 4, Haiku 3.5), ChatGPT (5.4, 5.4 Pro, 5.3, 5.2, 5.1, 5, 5 Mini, 5 Nano, 4.1, 4.1 Mini, 4.1 Nano, GPT Web), Gemini (3.1 Pro Preview, 3 Pro, 2.5 Pro, 2.5 Flash), Grok (4, 3, 3 Reasoner, 3 Deep Search), Perplexity (Sonar Pro, Sonar Deep Research, Sonar), DeepSeek (R1, V3), Qwen (3, 3 Thinking, 3 Max Thinking).

---

## Audio Generation

Audio uses Pattern A (video) workflow with `scope: "video"` and audio ai_name.

| Model             | ai_name       | Type           |
| ----------------- | ------------- | -------------- |
| SUNO v3.5 (music) | `suno`        | Music creation |
| SUNO v4 (music)   | `suno`        | Music creation |
| SUNO V4.5         | `suno`        | Music creation |
| ElevenLabs Voice  | `elevenlabs`  | Text-to-speech |
| Video to Audio    | `video2audio` | Sound effects  |

---

## Balance & Status

### Check Token Balance

```bash
curl -s "https://api.syntx.ai/api/v1/user/balance" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN"
```

### Check JWT Status

```bash
curl -s "$TG_KOMBAIN_API_URL/api/n8n/syntx-jwt-status" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

### Reset Circuit Breaker

If syntx.ai returns 402 (token exhaustion), the circuit breaker trips:

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/n8n/syntx-cb-reset" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

### Check Model Cost

```bash
curl -s "https://api.syntx.ai/api/v2/get_model_info?ai_name=banana&model_type=banana2&image_size=2K" \
  -H "Authorization: Bearer $SYNTX_AUTH_TOKEN"
```

Returns: `{"access": true, "cost": 2.0, "discount_cost": null, "limit": 3}`.

---

## Rules

1. **Route by type:** video -> Pattern A, image -> Pattern B, text -> Pattern C, audio -> Pattern A
2. **NEVER use browser** for any syntx.ai generation — always use REST API or TG-Kombain proxy
3. **Image `image_size`** is REQUIRED for banana models. Without it -> 402 error
4. **Video `model`** and `settings.model_type` MUST be identical
5. **Text is free** (0 tokens). Image/video cost tokens. Check balance before large batches
6. **Image endpoint:** Use `POST /design/generate` (NOT `/chats/{uuid}/messages` — deprecated for images)
7. **Deliver media:** Use `MEDIA:<object_url>` syntax to send generated content
8. **Three Banana paths exist:** syntx.ai (this skill), Polza API (tg-kombain), Gemini API — this skill uses syntx.ai
9. **JWT renewal:** Token expires periodically. If 401 -> tell user JWT needs renewal via Browserless
10. **Poll timing:** Video: wait 30s then every 15s (max 40 polls). Image: poll /inprogress until empty

## Examples

**User:** "Make a video of sunset over the ocean with Kling"

1. Create chat (scope: video) -> get uuid
2. Generate: ai_name=`kling`, model_type=`kling_text2video`
3. Poll -> deliver `MEDIA:<url>`

**User:** "Generate a cover image with Nano Banana Pro, 16:9"

1. Create chat (scope: image) -> get uuid
2. Generate: ai_name=`banana`, model_type=`banana2`, aspect_ratio=`16:9`, image_size=`2K`
3. Poll /inprogress -> fetch /messages -> deliver `MEDIA:<url>`

**User:** "Ask Claude Opus via syntx about quantum computing"

1. POST to TG-Kombain: model=`opus`, prompt="explain quantum computing"
2. Return text response
