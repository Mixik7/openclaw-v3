---
name: tg-kombain
description: Access TG-Kombain Telegram automation platform — parse channels, manage accounts, check stats, audience insights, warmup status, ad pipeline, and more. Use when the user asks about Telegram data, audience, channel metrics, account management, or wants to trigger parsing/automation tasks. Requires TG_KOMBAIN_API_KEY and TG_KOMBAIN_API_URL environment variables.
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

Access the TG-Kombain Telegram automation platform (55K LOC, 9 modules, 100+ API endpoints).

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

## Available Modules

| Module      | Purpose                          |
| ----------- | -------------------------------- |
| parser      | Channel/user parsing, search     |
| warmup      | Account warmup automation        |
| trust       | Trust score tracking             |
| neurochat   | AI chatting in groups            |
| poster      | Scheduled posting                |
| ad_pipeline | Ad buying pipeline (7 stages)    |
| rss         | RSS feed aggregation             |
| viral       | Viral campaigns (giveaway, quiz) |
| mutual_pr   | Cross-promotion finder           |
| strategy    | AI strategy advisor              |

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

1. Generate: use `syntx-video` skill
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
