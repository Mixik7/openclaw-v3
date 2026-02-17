---
name: tg-kombain
description: Access TG-Kombain Telegram automation platform — parse channels, manage accounts, check stats, audience insights, warmup status, ad pipeline, and more. Use when the user asks about Telegram data, audience, channel metrics, account management, or wants to trigger parsing/automation tasks. Requires TG_KOMBAIN_API_KEY and TG_KOMBAIN_API_URL environment variables.
metadata: { "openclaw": { "emoji": "📡", "requires": { "env": ["TG_KOMBAIN_API_KEY", "TG_KOMBAIN_API_URL"] }, "primaryEnv": "TG_KOMBAIN_API_KEY" } }
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
| Action | Endpoint | Method |
|--------|----------|--------|
| Health check | `/api/n8n/health` | GET |
| Platform stats | `/api/n8n/stats` | GET |
| Stats by days | `/api/n8n/stats?days=30` | GET |
| System status | `/api/health` | GET |

### Parsing
| Action | Endpoint | Method |
|--------|----------|--------|
| Parse channel | `/api/n8n/parse` | POST |
| Task status | `/api/n8n/task/{id}` | GET |
| Parsed users | `/api/n8n/data/users?source=@channel` | GET |
| Parsed channels | `/api/n8n/data/channels` | GET |

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
| Action | Endpoint | Method |
|--------|----------|--------|
| List accounts | `/api/accounts` | GET |
| Account details | `/api/accounts/{phone}` | GET |
| Warmup status | `/api/warmup/status` | GET |

### Audience & Analytics
| Action | Endpoint | Method |
|--------|----------|--------|
| Audience insights | `/api/audience/insights` | GET |
| Overlap analysis | `/api/n8n/data/overlap` | GET |
| KPI snapshots | `/api/n8n/kpi` | GET |

### Ad Pipeline
| Action | Endpoint | Method |
|--------|----------|--------|
| Candidates list | `/api/ad-pipeline/candidates` | GET |
| Scoring results | `/api/ad-pipeline/scoring` | GET |
| Deals | `/api/ad-pipeline/deals` | GET |

### Agent Bridge (Symbiosis)
| Action | Endpoint | Method |
|--------|----------|--------|
| Dispatch task | `/api/agent/dispatch` | POST |
| Task status | `/api/agent/tasks/{id}` | GET |
| Active tasks | `/api/agent/tasks` | GET |
| Submit result | `/api/agent/result` | POST |

**Agent dispatch body:**
```json
{
  "from_agent": "openclaw",
  "to_agent": "moltis",
  "action": "delegate",
  "payload": {"message": "Analyze this..."},
  "metadata": {"priority": "normal", "timeout_seconds": 300}
}
```

### MCP
| Action | Endpoint | Method |
|--------|----------|--------|
| MCP status | `/api/mcp-status` | GET |
| MCP proxy | `/api/mcp-proxy` | POST |

## Available Modules

| Module | Purpose |
|--------|---------|
| parser | Channel/user parsing, search |
| warmup | Account warmup automation |
| trust | Trust score tracking |
| neurochat | AI chatting in groups |
| poster | Scheduled posting |
| ad_pipeline | Ad buying pipeline (7 stages) |
| rss | RSS feed aggregation |
| viral | Viral campaigns (giveaway, quiz) |
| mutual_pr | Cross-promotion finder |
| strategy | AI strategy advisor |

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
