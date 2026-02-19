---
name: agent-delegate
description: Delegate tasks to other AI agents — Moltis for deep research/analysis, TG-Kombain for complex multi-step automation. Use ONLY for inter-agent delegation where another agent's reasoning is needed. Do NOT use for system commands (publish, music, status) — use n8n-api skill instead. Do NOT use for data queries — use tg-kombain skill instead. Requires N8N_BASE_URL environment variable.
metadata: { "openclaw": { "emoji": "🤝", "requires": { "env": ["N8N_BASE_URL"] }, "primaryEnv": "N8N_BASE_URL" } }
---

# Agent Delegation (Inter-Agent ONLY)

Delegate tasks to other AI agents in the Content Factory ecosystem via N8N WF 26 Agent Dispatcher.

## CRITICAL: When to Use vs When NOT to Use

### USE this skill when:
- User asks you to **delegate reasoning** to another agent
- "Ask Moltis to analyze competitive landscape"
- "Have TG-Kombain run a full parsing strategy for channel X"
- Task requires **another agent's judgment**, not just data retrieval

### DO NOT use this skill when:
- User wants to **publish content** → use `n8n-api` skill
- User wants **data or stats** → use `tg-kombain` skill
- User wants to **trigger a workflow** → use `n8n-api` skill
- User wants **system health check** → use `tg-kombain` skill

**Rule of thumb:** If the request can be fulfilled by a single API call, don't delegate. Only delegate when the task needs multi-step reasoning from another agent.

## Architecture

```
You (IDEA/Secretary) ──► N8N WF 26 ──► Target Agent
                                         ├── Moltis Atlas (deep research, analysis)
                                         ├── TG-Kombain (complex multi-step automation)
                                         └── N8N (workflow orchestration)
```

## When to Delegate to Each Agent

| Agent | Delegate for... | NOT for... |
|-------|----------------|-----------|
| **Moltis** | Deep research, competitive analysis, complex reasoning, monitoring strategy | Simple data queries (use tg-kombain) |
| **TG-Kombain** | Complex multi-step automation requiring planning | Single API calls (use tg-kombain) |
| **N8N** | Complex workflow orchestration requiring judgment | Simple workflow triggers (use n8n-api) |

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
- `openclaw` (this agent — you)
- `moltis` (deep research, Rust sandbox, 33 MCP tools)
- `tg-kombain` (Telegram automation platform)
- `n8n` (workflow orchestration)

### Valid Actions
- `delegate` — ask another agent to perform a reasoning task
- `query` — ask for synthesized analysis (not raw data)
- `notify` — send a notification (no response expected)

## Example: Delegate Research to Moltis

```bash
curl -s -X POST "$N8N_BASE_URL/webhook/agent-dispatch" \
  -H "Content-Type: application/json" \
  -d '{
    "from_agent": "openclaw",
    "to_agent": "moltis",
    "action": "delegate",
    "payload": {
      "message": "Analyze competitive landscape for Telegram channels in crypto niche. Compare top 10 channels by engagement, growth, and content strategy. Use get_audience_insights and get_parsed_channels tools."
    },
    "metadata": {
      "priority": "normal",
      "timeout_seconds": 600,
      "callback_url": "https://openclaw-v3-production.up.railway.app/hooks/agent"
    }
  }'
```

## Result Callback

When a delegated task completes, the result arrives at your hooks endpoint:
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
