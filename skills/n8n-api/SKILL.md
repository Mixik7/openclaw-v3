---
name: n8n-api
description: Control n8n workflow automation via REST API. Use when the user asks to trigger workflows, check execution status, list workflows, or manage n8n automations. Requires N8N_API_KEY and N8N_BASE_URL environment variables.
metadata: { "openclaw": { "emoji": "⚙️", "requires": { "env": ["N8N_API_KEY", "N8N_BASE_URL"] }, "primaryEnv": "N8N_API_KEY", "homepage": "https://n8n.io" } }
---

# n8n API Skill

Control the Content Factory n8n instance via REST API. This skill lets you trigger workflows, check statuses, list workflows, and monitor automations.

## Configuration

Environment variables (set in Railway or openclaw.json):
- `N8N_API_KEY` — JWT token for n8n API authentication
- `N8N_BASE_URL` — n8n instance URL (e.g. `https://n8n-production-fc90.up.railway.app`)

## Authentication

All API requests use header:
```
X-N8N-API-KEY: $N8N_API_KEY
```

## Core Operations

### List All Workflows

```bash
curl -s "$N8N_BASE_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '.data[] | {id, name, active}'
```

### Get Workflow Details

```bash
curl -s "$N8N_BASE_URL/api/v1/workflows/WORKFLOW_ID" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '{id, name, active, nodes: [.nodes[].name]}'
```

### Activate/Deactivate Workflow

```bash
# Activate
curl -s -X PATCH "$N8N_BASE_URL/api/v1/workflows/WORKFLOW_ID" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true}'

# Deactivate
curl -s -X PATCH "$N8N_BASE_URL/api/v1/workflows/WORKFLOW_ID" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": false}'
```

### Get Recent Executions

```bash
curl -s "$N8N_BASE_URL/api/v1/executions?limit=10" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '.data[] | {id, workflowId, status, startedAt, stoppedAt}'
```

### Get Execution Details (with errors)

```bash
curl -s "$N8N_BASE_URL/api/v1/executions/EXECUTION_ID" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '{id, status, data: .data.resultData.error}'
```

## Content Factory Workflows

Key workflow names and their purposes:

| Name | Purpose |
|------|---------|
| `1_Router_Core` | Telegram command routing |
| `2_Content_Scheduler` | Cron scheduler for video publishing |
| `2a_Channel_Worker_Acc01/02/03` | YouTube upload workers per account |
| `3_Status_Service` | Channel status monitoring |
| `3a_Status_Worker` | Status query worker |
| `5_AI_Chat` | AI responses (Groq/Claude/Gemini) |
| `6_Suno_Music` | Music generation via Suno |
| `7_Event_Logger` | Event logging to Google Sheet |

The `_v3` suffixed workflows are fixed versions (inactive, awaiting activation).

## Scripts

Use `{baseDir}/scripts/n8n-status.sh` to get a quick overview of all workflows and recent executions.

## Tips

- Always check `active` field before triggering — inactive workflows won't execute
- Use `_v3` workflows for testing, original workflows for production
- The Scheduler runs on cron — don't trigger it manually unless testing
- Event Logger records all actions — check it for audit trail
