---
name: editorial-review
description: Review and moderate pending articles in the Content Factory pipeline. Use when the user asks to check articles, approve/reject content, review what's ready to publish, or manage the editorial queue. Works with SQLite Content Pipeline API via TG-Kombain. Requires N8N_BASE_URL and TG_KOMBAIN_API_URL environment variables.
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

Review, approve, reject, and manage articles in the Content Factory pipeline. Articles flow through: WF 33 (analyst recommendations) → WF 16 (news collection) → WF 17 (content processing) → **SQLite Content Pipeline** → WF 34 (executor/moderation) → WF 18 (publisher).

## When to Use This Skill

| User says...                                    | Action                                                |
| ----------------------------------------------- | ----------------------------------------------------- |
| "what articles are pending?" / "что в очереди?" | GET /api/content/articles, filter by status           |
| "approve article" / "одобри статью"             | PATCH status to `approved`                            |
| "reject article" / "отклони"                    | PATCH status to `rejected`                            |
| "review queue" / "покажи на модерацию"          | List articles with `status=approved` awaiting publish |
| "publish now" / "опубликуй сейчас"              | Trigger WF 18 for specific article                    |
| "what's been published?" / "что опубликовано?"  | List articles with `status=published`                 |
| "channel performance" / "аналитика канала"      | Read channel memory for insights                      |

## Architecture

```
SQLite Content Pipeline (TG-Kombain /api/content/*)
  ├── status: draft → approved → publishing → published
  │                  └→ rejected
  ├── Fields: title, content, fullContent, channelKey, source, aiScore, imageUrl, ...
  └── Per-channel auto-approve threshold in NewsChannels GS tab (config only)

WF 34 Content Executor (cron 30min)
  ├── aiScore >= autoApproveThreshold → auto-publish via WF 18
  └── aiScore < threshold → sends preview to operator for inline review (✅/❌)
```

## API Endpoints

All requests go through TG-Kombain API (`TG_KOMBAIN_API_URL`).
Auth: `Authorization: Bearer $TG_KOMBAIN_API_KEY` header.

### 1. List Articles (with filters)

```bash
curl -s "$TG_KOMBAIN_API_URL/api/content/articles?status=approved&limit=20" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

Query params: `status` (draft|approved|publishing|published|rejected), `channelKey`, `limit`, `offset`.

### 2. Get Single Article

```bash
curl -s "$TG_KOMBAIN_API_URL/api/content/articles/{article_id}" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

### 3. Update Article Status

```bash
curl -s -X PATCH "$TG_KOMBAIN_API_URL/api/content/articles/{article_id}" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

Allowed status transitions: draft→approved, draft→rejected, approved→rejected, approved→publishing.

### 4. Claim Article for Publishing (atomic)

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/content/articles/claim?channelKey=crypto_news&limit=1" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

Query params: `channelKey` (optional), `limit` (default 5, max 50).
Atomically transitions approved→publishing (prevents TOCTOU race conditions).

### 5. Read Channel Memory

```bash
curl -s "$TG_KOMBAIN_API_URL/api/content/memory/{channel_key}" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

Returns: `lastTopics`, `painPoints`, `bestPerforming`, `worstPerforming`, `updatedAt`.

### 6. Read NewsChannels Config (still in Google Sheets)

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/google/sheets/read" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1lFwmozG-ci94UFV_kmzVVyHKz_y4FUfCAj4p1KnBSkw",
    "tab": "NewsChannels",
    "range": "A:L"
  }'
```

Key fields: `channelKey`, `channelName`, `autoApproveThreshold`, `systemPrompt`, `tone`, `enabled`.

### 7. Pipeline Stats

```bash
curl -s "$TG_KOMBAIN_API_URL/api/content/stats" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY"
```

Returns: articles by status, plan counts, generation costs, published_today.

### 8. Quality Check (5-point gate)

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/content/check-quality" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Article text here...", "channelKey": "crypto_news"}'
```

Returns: `passed` (bool), per-check results: `contentSafe`, `hookScore`, `aiScore`, `varietyOk`, `lengthOk`.

### 9. Humanize AI Text

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/content/humanize" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "AI-sounding text...", "maxRetries": 3}'
```

Returns: `text` (humanized), `aiScoreBefore`, `aiScoreAfter`.

### 10. Record Format Variety

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/content/record-variety" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Published text...", "channelKey": "crypto_news"}'
```

Records format type for anti-monotony tracking. Returns: `format` (question|listicle|stat_hook|story|opinion|how_to|announcement|generic).

### 11. Trigger Immediate Publish (via WF 18)

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
        "publishToTelegram": true
      }
    }
  }'
```

### 12. Delegate Research to Moltis

When an article needs fact-checking or deeper analysis before approval:

```bash
curl -s -X POST "$TG_KOMBAIN_API_URL/api/agent/dispatch" \
  -H "Authorization: Bearer $TG_KOMBAIN_API_KEY" \
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
draft  →  approved  →  publishing  →  published  →  archived
  │           │
  └→ rejected └→ failed (publish error, recovered back to approved after 60min)
```

- `draft`: WF 33 created article recommendation, WF 16 gathered from RSS
- `approved`: WF 17 processed content (AI rewrite + image), score meets threshold OR operator approved
- `publishing`: WF 34 claimed before calling WF 18 (prevents re-pickup)
- `published`: WF 18 successfully posted to channel(s)
- `rejected`: Operator or WF 34 callback rejected
- `archived`: Background worker archives published/rejected articles after 7 days

## Editorial Workflow

1. **Quick review**: `GET /api/content/articles?status=approved` → summarize for user
2. **Approve**: `PATCH /api/content/articles/{id}` with `{"status": "approved"}`
3. **Reject**: `PATCH /api/content/articles/{id}` with `{"status": "rejected"}`
4. **Immediate publish**: Approve + trigger WF 18 directly
5. **Research first**: Delegate to Moltis for fact-checking → approve/reject based on result

## 10 Active Channels (per-channel thresholds, S76/ADR-005)

| Key           | Niche                      | Threshold |
| ------------- | -------------------------- | --------- |
| general_news  | Breaking news              | 8         |
| crypto_news   | Cryptocurrency news        | 8         |
| ai_news       | AI & ML technology         | 7         |
| wb_products   | Wildberries marketplace    | 7         |
| crypto_games  | Crypto games & P2E         | 7         |
| kids_gifts    | Обучалки (kids education)  | 7         |
| horoscope     | Гороскоп с ИИ (horoscopes) | 6         |
| astrology     | Астрология с ИИ (transits) | 6         |
| food_taganrog | Recipes & cooking          | 6         |
| life_hacks    | Life hacks & tips          | 6         |

## Tips

- Articles with `aiScore >= autoApproveThreshold` are auto-published by WF 34 — no operator action needed
- Articles below threshold get inline keyboard preview in @My_Asst_c2 chat for manual review
- Channel memory is updated by WF 33 (Channel Analysts) with topic trends and pain points
- Always check `fullContent` (not just `content`) — Telegraph needs full text
- WF 34 runs every 30 minutes — approved articles publish within one cron cycle
- For urgent publish, trigger WF 18 directly instead of waiting for WF 34
- Stuck articles in `publishing` status for >60 min are auto-recovered back to `approved` by background worker
