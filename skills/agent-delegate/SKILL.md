---
name: agent-delegate
description: Delegate tasks to other AI agents in the ecosystem (Moltis for deep research/analysis, TG-Kombain for Telegram automation). Use when the user's request needs capabilities beyond your own — complex analysis, research tasks, or Telegram data operations. Requires N8N_BASE_URL environment variable.
metadata: { "openclaw": { "emoji": "🤝", "requires": { "env": ["N8N_BASE_URL"] }, "primaryEnv": "N8N_BASE_URL" } }
---

# Agent Delegation

Delegate tasks to other AI agents in the Content Factory ecosystem via the N8N Agent Dispatcher (WF 26).

## Architecture

```
You (IDEA/OpenClaw) ──► N8N Agent Dispatcher ──► Target Agent
                                                   ├── Moltis (deep research)
                                                   ├── TG-Kombain (TG automation)
                                                   └── N8N (workflow triggers)
```

## When to Delegate

| Agent | Delegate When... |
|-------|-----------------|
| **Moltis** | User needs deep research, competitive analysis, complex reasoning, monitoring alerts |
| **TG-Kombain** | User needs Telegram data (stats, parsed users, channels), automation (parsing, warmup), ad pipeline |
| **N8N** | User needs to trigger a specific workflow, check execution status |

## Delegation via N8N Webhook

**Endpoint:** `POST $N8N_BASE_URL/webhook/agent-dispatch`

**Body (AgentMessage):**
```json
{
  "from_agent": "openclaw",
  "to_agent": "moltis",
  "action": "delegate",
  "task_id": "unique-task-id",
  "payload": {
    "message": "Describe the task clearly..."
  },
  "metadata": {
    "priority": "normal",
    "timeout_seconds": 300,
    "callback_url": "https://openclaw-v3-production.up.railway.app/hooks/agent"
  }
}
```

### Valid Agents
- `openclaw` (this agent)
- `moltis` (deep research, Rust sandbox)
- `tg-kombain` (Telegram automation, 55K LOC)
- `n8n` (workflow orchestration)

### Valid Actions
- `delegate` — ask another agent to perform a task
- `query` — ask for data without side effects
- `notify` — send a notification (no response expected)
- `result` — return a completed task result

## Examples

### Delegate deep analysis to Moltis
```bash
curl -s -X POST "$N8N_BASE_URL/webhook/agent-dispatch" \
  -H "Content-Type: application/json" \
  -d '{
    "from_agent": "openclaw",
    "to_agent": "moltis",
    "action": "delegate",
    "payload": {
      "message": "Analyze competitive landscape for Telegram channels in crypto niche. Compare top 10 channels by engagement, growth, and content strategy."
    },
    "metadata": {
      "priority": "normal",
      "timeout_seconds": 600,
      "callback_url": "https://openclaw-v3-production.up.railway.app/hooks/agent"
    }
  }'
```

### Query TG-Kombain for stats
```bash
curl -s -X POST "$N8N_BASE_URL/webhook/agent-dispatch" \
  -H "Content-Type: application/json" \
  -d '{
    "from_agent": "openclaw",
    "to_agent": "tg-kombain",
    "action": "query",
    "payload": {
      "action": "stats"
    }
  }'
```

### Trigger N8N workflow
```bash
curl -s -X POST "$N8N_BASE_URL/webhook/agent-dispatch" \
  -H "Content-Type: application/json" \
  -d '{
    "from_agent": "openclaw",
    "to_agent": "n8n",
    "action": "delegate",
    "payload": {
      "workflow": "content-strategy",
      "message": "Run weekly content strategy analysis"
    }
  }'
```

## Result Callback

When a delegated task completes, the result is sent to your hooks endpoint:
`POST /hooks/agent` with body:
```json
{
  "task_id": "...",
  "from_agent": "moltis",
  "status": "completed",
  "result": {
    "summary": "Analysis complete...",
    "data": {...}
  }
}
```

The result is automatically delivered to the active conversation session.

## Anti-Loop Protection

Each message carries a `hop_count` in metadata. The system rejects messages with `hop_count >= 3` to prevent infinite delegation loops.
