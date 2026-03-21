---
name: tg-kombain
description: Access TG-Kombain Telegram automation platform — parse channels, manage accounts, check stats, audience insights, warmup status, ad pipeline, content pipeline, engagement metrics, AI memory, syntx.ai proxy, and more. Use when the user asks about Telegram data, audience, channel metrics, account management, content operations, engagement, or wants to trigger parsing/automation tasks. Requires TG_KOMBAIN_API_KEY and TG_KOMBAIN_API_URL environment variables.
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "env": ["TG_KOMBAIN_API_KEY", "TG_KOMBAIN_API_URL"] },
        "primaryEnv": "TG_KOMBAIN_API_KEY",
      },
  }
---

# TG-Kombain Integration

Access the TG-Kombain Telegram automation platform (~112K LOC, 16 MCP modules, 76 tools, 291 endpoints, 33 routers).

## Auth

All requests require Bearer token:

```bash
curl -s "$TG_KOMBAIN_API_URL/api/<endpoint>" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

## Quick Reference

### System

| Action         | Endpoint                 | Method |
| -------------- | ------------------------ | ------ |
| Health check   | `/api/n8n/health`        | GET    |
| Platform stats | `/api/n8n/stats`         | GET    |
| Stats by days  | `/api/n8n/stats?days=30` | GET    |
| System status  | `/api/health`            | GET    |

### Parsing

| Action          | Endpoint                              | Method |
| --------------- | ------------------------------------- | ------ |
| Parse channel   | `/api/n8n/parse`                      | POST   |
| Task status     | `/api/n8n/task/{id}`                  | GET    |
| Parsed users    | `/api/n8n/data/users?source=@channel` | GET    |
| Parsed channels | `/api/n8n/data/channels`              | GET    |

**Parse request body:**

```json
{
  "target": "@channel_name",
  "mode": "channel_members",
  "limit": 500
}
```

Modes: `channel_members`, `channel_posts`, `search_channels`, `search_users`

### Accounts

| Action          | Endpoint                | Method |
| --------------- | ----------------------- | ------ |
| List accounts   | `/api/accounts`         | GET    |
| Account details | `/api/accounts/{phone}` | GET    |
| Warmup status   | `/api/warmup/status`    | GET    |

### Audience & Analytics

| Action            | Endpoint                 | Method |
| ----------------- | ------------------------ | ------ |
| Audience insights | `/api/audience/insights` | GET    |
| Overlap analysis  | `/api/n8n/data/overlap`  | GET    |
| KPI snapshots     | `/api/n8n/kpi`           | GET    |

### Ad Pipeline

| Action          | Endpoint                      | Method |
| --------------- | ----------------------------- | ------ |
| Candidates list | `/api/ad-pipeline/candidates` | GET    |
| Scoring results | `/api/ad-pipeline/scoring`    | GET    |
| Deals           | `/api/ad-pipeline/deals`      | GET    |

### Content Pipeline (SQLite API)

| Action              | Endpoint                            | Method   |
| ------------------- | ----------------------------------- | -------- |
| List articles       | `/api/content/articles`             | GET      |
| Create article      | `/api/content/articles`             | POST     |
| Batch create        | `/api/content/articles/batch`       | POST     |
| Get article         | `/api/content/articles/{id}`        | GET      |
| Update article      | `/api/content/articles/{id}`        | PATCH    |
| Claim for publish   | `/api/content/articles/claim`       | POST     |
| Dedup check         | `/api/content/articles/dedup`       | GET      |
| Archive old         | `/api/content/articles/archive`     | POST     |
| Recover stuck       | `/api/content/articles/recover`     | POST     |
| List/create plans   | `/api/content/plans`                | GET/POST |
| Update plan         | `/api/content/plans/{id}`           | PATCH    |
| Pipeline stats      | `/api/content/stats`                | GET      |
| SEO publish log     | `/api/content/seo-log`              | GET/POST |
| Persona publish log | `/api/content/persona-log`          | GET/POST |
| Generation log      | `/api/content/generation-log`       | GET/POST |
| Channel memory      | `/api/content/memory/{channel_key}` | GET/POST |

Query params for articles: `status` (draft|approved|publishing|published|rejected), `channelKey`, `limit`, `offset`.

### Quality Gate

| Action                | Endpoint                      | Method |
| --------------------- | ----------------------------- | ------ |
| 5-point quality check | `/api/content/check-quality`  | POST   |
| Humanize AI text      | `/api/content/humanize`       | POST   |
| Record format variety | `/api/content/record-variety` | POST   |

### Engagement

| Action                    | Endpoint                          | Method |
| ------------------------- | --------------------------------- | ------ |
| Collect (Telethon, WF 41) | `/api/content/collect-engagement` | POST   |
| Write post metrics        | `/api/content/engagement`         | POST   |
| ERR stats per channel     | `/api/content/engagement/stats`   | GET    |
| Top/bottom posts by ERR   | `/api/content/engagement/top`     | GET    |

### syntx.ai Proxy

| Action                 | Endpoint                    | Method |
| ---------------------- | --------------------------- | ------ |
| Generate text          | `/api/n8n/syntx-text`       | POST   |
| Generate image         | `/api/n8n/syntx-image`      | POST   |
| JWT status             | `/api/n8n/syntx-jwt-status` | GET    |
| Circuit breaker status | `/api/n8n/syntx-cb-status`  | GET    |
| Circuit breaker reset  | `/api/n8n/syntx-cb-reset`   | POST   |

Text model aliases: claude-opus, claude-sonnet, claude-haiku, sonar, sonar-pro, sonar-deep, gpt-5, gpt-4.1.

### Engram Memory (AI Persistence)

| Action           | Endpoint                  | Method |
| ---------------- | ------------------------- | ------ |
| Store memory     | `/api/memory/store`       | POST   |
| Search memories  | `/api/memory/search`      | GET    |
| Recall by ID     | `/api/memory/recall`      | GET    |
| Evolve memory    | `/api/memory/evolve`      | POST   |
| Forget memory    | `/api/memory/forget`      | POST   |
| Consolidate      | `/api/memory/consolidate` | POST   |
| Decay old        | `/api/memory/decay`       | POST   |
| Stats            | `/api/memory/stats`       | GET    |
| Generate context | `/api/memory/context`     | GET    |

Based on A-MEM (NeurIPS 2025). FTS5 BM25 search, Ebbinghaus forgetting curve, bigram Jaccard dedup.

### Persona Pipeline

| Action          | Endpoint                           | Method |
| --------------- | ---------------------------------- | ------ |
| Train LoRA      | `/api/n8n/persona/train-lora`      | POST   |
| Training status | `/api/n8n/persona/training-status` | GET    |
| Generate batch  | `/api/n8n/persona/generate-batch`  | POST   |
| Face validate   | `/api/n8n/persona/face-validate`   | POST   |

### RSS Feeds

| Action      | Endpoint              | Method |
| ----------- | --------------------- | ------ |
| List feeds  | `/api/rss-feeds`      | GET    |
| Add feed    | `/api/rss-feeds`      | POST   |
| Update feed | `/api/rss-feeds/{id}` | PATCH  |
| Delete feed | `/api/rss-feeds/{id}` | DELETE |

### Agent Bridge (Symbiosis)

| Action        | Endpoint                | Method |
| ------------- | ----------------------- | ------ |
| Dispatch task | `/api/agent/dispatch`   | POST   |
| Task status   | `/api/agent/tasks/{id}` | GET    |
| Active tasks  | `/api/agent/tasks`      | GET    |
| Submit result | `/api/agent/result`     | POST   |

**Agent dispatch body:**

```json
{
  "from_agent": "openclaw",
  "to_agent": "moltis",
  "action": "delegate",
  "payload": { "message": "Analyze this..." },
  "metadata": { "priority": "normal", "timeout_seconds": 300 }
}
```

### MCP

| Action     | Endpoint          | Method |
| ---------- | ----------------- | ------ |
| MCP status | `/api/mcp-status` | GET    |
| MCP proxy  | `/api/mcp-proxy`  | POST   |

## MCP Modules (76 tools, 16 modules)

| Module           | Tools | Purpose                                          |
| ---------------- | ----- | ------------------------------------------------ |
| system           | 4     | Health, stats, task management                   |
| parsing          | 7     | Channel/user parsing, search, audience           |
| content          | 5     | Post to channel, scheduled posts, strategy       |
| engagement       | 4     | Reactions, AI comments, invites, DMs             |
| analytics        | 6     | KPI, quality, ad pipeline stats                  |
| accounts         | 4     | Account listing, trust scores, warmup            |
| automation       | 5     | Mutual PR, viral campaigns                       |
| syntx            | 2     | syntx.ai generate + balance                      |
| google_workspace | 9     | Sheets CRUD, Drive operations                    |
| image_gen        | 2     | Image generation, model listing                  |
| fal              | 8     | fal.ai: generate, edit, video, lipsync, etc.     |
| persona          | 4     | LoRA training, batch generation, face validation |
| comfyui          | 6     | ComfyUI on RunPod: generate, portrait, skin      |
| tglite           | 2     | Read channel messages, list dialogs              |
| memory           | 8     | Engram: store, search, recall, evolve, etc.      |

MCP endpoint: `POST /mcp/` (trailing slash required). Auth: `Bearer MCP_ACCESS_TOKEN`.

### Image Generation (Phase 8.1)

| Action      | Endpoint                  | Method |
| ----------- | ------------------------- | ------ |
| Generate    | `/api/n8n/image-generate` | POST   |
| List models | `/api/n8n/image-models`   | GET    |

**11 models with aliases:** dall-e-3 (dalle3) ✅, flux-pro (flux) ✅, gpt-image-1 (gpt-image) ✅, midjourney-v7 (mj), midjourney-v6.1 (mj6), niji-v6 (niji), dall-e-2 (dalle2), google/nano-banana (banana)

**Generate image:**

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/n8n/image-generate" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"sunset over ocean","model":"midjourney-v7","size":"1024x1024"}'
```

**With auto-upload to Drive:**

```json
{ "prompt": "crypto cover", "model": "mj", "upload_to_drive": true, "channel_key": "ch_001" }
```

### Post with Media

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/n8n/post" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"channel":"@my_channel","text":"Post text","media_url":"https://..."}'
```

Fields: `media_url` (auto-download) OR `media_path` (local file in data/).

### Google Workspace

| Action             | Endpoint                             | Method |
| ------------------ | ------------------------------------ | ------ |
| Read sheet         | `/api/google/sheets/read`            | POST   |
| Write sheet        | `/api/google/sheets/write`           | POST   |
| Append rows        | `/api/google/sheets/append`          | POST   |
| Create spreadsheet | `/api/google/sheets/create`          | POST   |
| List Drive files   | `/api/google/drive/list?folder_id=X` | GET    |
| Upload to Drive    | `/api/google/drive/upload`           | POST   |
| Create folder      | `/api/google/drive/create-folder`    | POST   |
| Ensure path        | `/api/google/drive/ensure-path`      | POST   |
| Download file      | `/api/google/drive/download/{id}`    | GET    |
| Video inventory    | `/api/google/drive/video-inventory`  | GET    |
| Google health      | `/api/google/health`                 | GET    |

**Upload file from URL to Drive:**

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/drive/upload" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"folder_id":"abc123","url":"https://example.com/image.png","filename":"cover.png"}'
```

**Create folder path (mkdir -p):**

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/drive/ensure-path" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"root_id":"abc123","path":"Изображения/midjourney-v7/крипто"}'
```

> **Note:** If `root_id` is empty or omitted, the server uses `DRIVE_CONTENT_HUB_ROOT` env var as fallback.

### Image → Drive → Post Flow

1. Generate: `POST /api/n8n/image-generate {"prompt":"...","model":"mj"}`
2. Ensure path: `POST /api/google/drive/ensure-path {"root_id":"ch_folder","path":"Изображения/midjourney-v7/тема"}`
3. Upload: `POST /api/google/drive/upload {"folder_id":"<from step 2>","url":"<image_url from step 1>"}`
4. Show preview to user, wait for approval
5. Post: `POST /api/n8n/post {"channel":"@ch","text":"...","media_url":"<image_url>"}`
6. **ONLY if user explicitly says "нагони трафик":** `POST /api/agent/dispatch {"to_agent":"moltis",...}`

### Video → Drive Flow

1. Generate: use `syntx` skill
2. User says "save to Drive": `POST /api/google/drive/ensure-path {"path":"Видео/kling/тема"}`
3. Upload: `POST /api/google/drive/upload {"folder_id":"...","url":"<video_url>"}`

**Read sheet:**

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/sheets/read" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tab":"Channels"}'
```

**Video inventory (all channels):**

```bash
curl -s "$TG_KOMBAIN_API_URL/api/google/drive/video-inventory" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

**Create new spreadsheet:**

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/sheets/create" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Parser Analytics","tabs":["Data","Metrics"],"share_with":["user@gmail.com"]}'
```

## Examples

**Get platform stats:**

```bash
curl -s "$TG_KOMBAIN_API_URL/api/n8n/stats" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

**Parse a channel:**

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/n8n/parse" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target":"@example_channel","mode":"channel_members","limit":100}'
```

**Delegate task to Moltis via Agent Bridge:**

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/agent/dispatch" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"from_agent":"openclaw","to_agent":"moltis","action":"delegate","payload":{"message":"Deep analysis of..."}}'
```
