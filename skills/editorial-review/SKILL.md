---
name: editorial-review
description: Review and moderate pending articles in the Content Factory pipeline. Use when the user asks to check articles, approve/reject content, review what's ready to publish, or manage the editorial queue. Works with ArticleQueue in Google Sheets via TG-Kombain API. Requires N8N_BASE_URL and TG_KOMBAIN_API_URL environment variables.
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "env": ["N8N_BASE_URL", "TG_KOMBAIN_API_URL"] },
        "primaryEnv": "TG_KOMBAIN_API_URL",
        "homepage": "https://tg-kombain-production-a5d5.up.railway.app",
      },
  }
---

# Editorial Review — Content Moderation Skill

Review, approve, reject, and manage articles in the Content Factory pipeline. Articles flow through: WF 33 (analyst recommendations) → WF 16 (news collection) → WF 17 (content processing) → **ArticleQueue** → WF 34 (executor/moderation) → WF 18 (publisher).

## When to Use This Skill

| User says...                                    | Action                                                |
| ----------------------------------------------- | ----------------------------------------------------- |
| "what articles are pending?" / "что в очереди?" | Read ArticleQueue, filter by status                   |
| "approve article" / "одобри статью"             | Update status to `approved`                           |
| "reject article" / "отклони"                    | Update status to `rejected`                           |
| "review queue" / "покажи на модерацию"          | List articles with `status=approved` awaiting publish |
| "publish now" / "опубликуй сейчас"              | Trigger WF 18 for specific article                    |
| "what's been published?" / "что опубликовано?"  | List articles with `status=published`                 |
| "channel performance" / "аналитика канала"      | Read ChannelMemory for insights                       |

## Architecture

```
ArticleQueue (Google Sheets)
  ├── status: draft → approved → publishing → published
  │                  └→ rejected
  ├── Fields: title, content, fullContent, channelKey, source, score, imageUrl, ...
  └── Per-channel auto-approve threshold in NewsChannels tab

WF 34 Content Executor (cron 30min)
  ├── score >= autoApproveThreshold → auto-publish via WF 18
  └── score < threshold → sends preview to operator for inline review (✅/❌)
```

## API Endpoints

All requests go through TG-Kombain API (`TG_KOMBAIN_API_URL`).
Auth: `Authorization: Bearer $API_SECRET_KEY` header.

### 1. Read ArticleQueue

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/sheets/read" \
  -H "Authorization: Bearer $API_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1lFwmozG-ci94UFV_kmzVVyHKz_y4FUfCAj4p1KnBSkw",
    "tab": "ArticleQueue",
    "range": "A:Z"
  }'
```

Response: array of rows with headers as keys.

### 2. Update Article Status

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/sheets/write" \
  -H "Authorization: Bearer $API_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1lFwmozG-ci94UFV_kmzVVyHKz_y4FUfCAj4p1KnBSkw",
    "tab": "ArticleQueue",
    "range": "A{ROW}:Z{ROW}",
    "values": [["...updated row data..."]]
  }'
```

Find the row number by matching `title` + `channelKey`, then update the `status` column.

### 3. Read NewsChannels (thresholds, config)

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/sheets/read" \
  -H "Authorization: Bearer $API_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1lFwmozG-ci94UFV_kmzVVyHKz_y4FUfCAj4p1KnBSkw",
    "tab": "NewsChannels",
    "range": "A:Z"
  }'
```

Key fields: `channelKey`, `channelName`, `autoApproveThreshold`, `contentTypes`, `language`.

### 4. Read ChannelMemory (AI analyst insights)

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/sheets/read" \
  -H "Authorization: Bearer $API_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1lFwmozG-ci94UFV_kmzVVyHKz_y4FUfCAj4p1KnBSkw",
    "tab": "ChannelMemory",
    "range": "A:Z"
  }'
```

Key fields: `channelKey`, `lastTopics`, `painPoints`, `updatedAt`.

### 5. Trigger Immediate Publish (via WF 18)

```bash
curl -s -X POST "$N8N_BASE_URL/api/v1/workflows/MsNRDjTffBC0hi29/execute" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "articles": [{
        "title": "...",
        "content": "...",
        "fullContent": "...",
        "channelKey": "...",
        "imageUrl": "...",
        "source": "..."
      }],
      "channelConfig": {
        "channelId": "...",
        "channelName": "...",
        "publishToTelegram": true,
        "publishToVK": false
      }
    }
  }'
```

### 6. Delegate Research to Moltis

When an article needs fact-checking or deeper analysis before approval:

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/agent/dispatch" \
  -H "Authorization: Bearer $API_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from_agent": "openclaw",
    "to_agent": "moltis",
    "action": "query",
    "payload": {
      "message": "Fact-check this article: [title]. Verify key claims and sources."
    },
    "metadata": {
      "priority": "normal",
      "timeout_seconds": 300
    }
  }'
```

## Article Status Flow

```
draft  →  approved  →  publishing  →  published
  │           │
  └→ rejected └→ failed (publish error)
```

- `draft`: WF 33 created article recommendation, WF 16 gathered from RSS
- `approved`: WF 17 auto-approved (score >= threshold) OR operator manually approved
- `publishing`: WF 34 set before calling WF 18 (prevents re-pickup)
- `published`: WF 18 successfully posted to channel(s)
- `rejected`: Operator or WF 34 callback rejected
- `failed`: WF 18 publish error (retry manually)

## Editorial Workflow

1. **Quick review**: Read ArticleQueue → filter `status=approved` → summarize for user
2. **Approve**: Change status from `collected` to `approved`
3. **Reject**: Change status to `rejected` (with optional reason in notes column)
4. **Immediate publish**: Approve + trigger WF 18 directly
5. **Research first**: Delegate to Moltis for fact-checking → approve/reject based on result

## 10 Active Channels

| Key              | Niche                   | Threshold |
| ---------------- | ----------------------- | --------- |
| crypto_games     | Crypto games & P2E      | 7         |
| wb_products      | Wildberries marketplace | 7         |
| cooking          | Recipes & cooking       | 6         |
| crypto_news      | Cryptocurrency news     | 8         |
| ai_news          | AI & ML technology      | 7         |
| life_hacks       | Life hacks & tips       | 6         |
| general_news     | Breaking news           | 7         |
| kids_gifts       | Children's gifts & toys | 6         |
| business_ideas   | Startups & business     | 7         |
| tech_singularity | Tech & future trends    | 8         |

## Tips

- Articles with `score >= autoApproveThreshold` are auto-published by WF 34 — no operator action needed
- Articles below threshold get inline keyboard preview in @My_Asst_c2 chat for manual review
- ChannelMemory is updated by WF 33 (Channel Analysts) with topic trends, pain points, audience profile
- Always check `fullContent` (not just `content`) — VK and Telegraph need full text
- WF 34 runs every 30 minutes — approved articles publish within one cron cycle
- For urgent publish, trigger WF 18 directly instead of waiting for WF 34
