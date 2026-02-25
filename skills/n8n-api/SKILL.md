---
name: n8n-api
description: Control the Content Factory via N8N REST API. Use when the user asks to publish video, generate music, check status, manage articles, list workflows, or monitor automations. This is the primary skill for content operations. Requires N8N_API_KEY and N8N_BASE_URL environment variables.
metadata:
  {
    "openclaw":
      {
        "emoji": "⚙️",
        "requires": { "env": ["N8N_API_KEY", "N8N_BASE_URL"] },
        "primaryEnv": "N8N_API_KEY",
        "homepage": "https://n8n.io",
      },
  }
---

# N8N API Skill — Content Factory Operations

Control the Content Factory N8N instance. This is the **primary skill for content commands**: publishing, music generation, article management, and workflow monitoring.

## When to Use This Skill

| User says...                     | Action                                             |
| -------------------------------- | -------------------------------------------------- |
| "publish video" / "выложи видео" | Trigger WF 01 Router via knowledge of WF structure |
| "music" / "музыка"               | Music generation pipeline                          |
| "status" / "статус"              | Channel status via WF 05                           |
| "article" / "статья"             | SEO article pipeline (WF 16→17→18)                 |
| "list workflows"                 | List all N8N workflows                             |
| "check executions"               | Recent execution history                           |

**Do NOT use agent-delegate (WF 26) for these operations.** This skill calls N8N directly.

## Authentication

All API requests use header:

```bash
curl -s "$N8N_BASE_URL/api/v1/<endpoint>" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
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

### Activate Workflow

```bash
curl -s -X POST "$N8N_BASE_URL/api/v1/workflows/WORKFLOW_ID/activate" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

### Deactivate Workflow

```bash
curl -s -X POST "$N8N_BASE_URL/api/v1/workflows/WORKFLOW_ID/deactivate" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
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

## Content Factory Workflows (31 total)

### Core Content (WF 01-07)

| #   | Name               | ID                      | Trigger                            |
| --- | ------------------ | ----------------------- | ---------------------------------- |
| 01  | Telegram Router    | `7h11iwrBtElelwwpiPHbb` | Telegram webhook (@My_Asst_c2)     |
| 02  | YouTube Publishing | `IQA0eAMXkyBWSrFR`      | Cron 9/13/19 + Router              |
| 03  | TikTok Publishing  | `OlVizpU4pV7WGrK2`      | Cron 12:00 + Router                |
| 04  | VK Publishing      | `9nQEUNj6xc07hKdN`      | Cron 10/14/20 + Router             |
| 05  | AI Mozgi           | `5QtaHWA8QUyC1TqE`      | Execute Workflow (Claude Sonnet 4) |
| 06  | Music Generation   | `wn4VgYjBHgTHFNbRmCSko` | Execute Workflow (Kie.ai)          |
| 07  | Event Logger       | `KZwQpHP6qrNkVvzHB94Un` | Execute Workflow                   |

### Content Factory (WF 16-18, 33-34)

| #   | Name              | ID                 | Trigger                                         |
| --- | ----------------- | ------------------ | ----------------------------------------------- |
| 16  | News Collector    | `yq0Tlm0ukRzOw9IP` | Cron 6h (10 channels, RSS+AI)                   |
| 17  | Content Processor | `uMXIqx8Ty6PthUCN` | Execute Workflow (SEO + images via ElectronHub) |
| 18  | Text Publisher    | `MsNRDjTffBC0hi29` | Execute Workflow (Telegram + VK + Telegraph)    |
| 33  | Channel Analysts  | `HuFkfwJR5Dqy6zCF` | Cron 4h (per-channel AI brain, ChannelMemory)   |
| 34  | Content Executor  | `tX52Wmlk50esNd8t` | Cron 30min (auto-publish + inline moderation)   |

### TG-Kombain Automation (WF 14-15, 19-25)

| #   | Name                 | ID                 | Purpose               |
| --- | -------------------- | ------------------ | --------------------- |
| 14  | Warmup Scheduler     | `HEo7VCJNBQ4l5EOJ` | Account warmup cron   |
| 15  | TG Control           | `fTw1h8nqG5nA4Fd3` | Account management    |
| 19  | Audience Acquisition | `aBncMREQTKX2kB85` | Automated parsing     |
| 20  | Smart Invite         | `I8ijUejvMxIckcqG` | Invite campaigns      |
| 21  | Content Feedback     | `073Y5hNjIrIjLtbO` | Quality feedback loop |
| 22  | Engagement Booster   | `FhFNghBmFAvQ2dNL` | Engagement automation |
| 23  | Ad Pipeline          | `Z6RbfJblESOP5Kar` | Ad orchestration      |
| 24  | Mutual PR            | `kIxHVulFXYeH3zJo` | Cross-promotion       |
| 25  | Viral Campaign       | `pjl9GXSeOMSihMRd` | Viral campaigns       |

### Monitoring (WF 31)

| #   | Name                    | ID                 | Purpose                         |
| --- | ----------------------- | ------------------ | ------------------------------- |
| 31  | Video Inventory Monitor | `EGE8kChflVR0Hq47` | Cron 6h, Drive inventory alerts |

### Agent Ecosystem (WF 09, 26-30)

| #   | Name             | ID                 | Purpose             |
| --- | ---------------- | ------------------ | ------------------- |
| 09  | OpenClaw Bridge  | `mXnfHX25m0eEcixc` | N8N → OpenClaw      |
| 26  | Agent Dispatcher | `uNUbgpRcXbvToZcF` | Inter-agent routing |
| 27  | Result Collector | `fWiswnHYt2w3vq2E` | Agent results       |
| 28  | Analytics        | `A0hwGzeStnN0lUi8` | Cross-agent KPI     |
| 29  | Strategy         | `FQhWmhWvpRdKbuFn` | Content strategy    |
| 30  | Feedback Loop    | `dkn2xB9ZQtgWFYH3` | Pipeline feedback   |

### Inactive

| #      | Name           | ID                     | Reason             |
| ------ | -------------- | ---------------------- | ------------------ |
| ~~13~~ | ~~Jarvis Bot~~ | ~~`pvQMTF9etkC4qTxd`~~ | DELETED 2026-02-24 |

## Tips

- Always check `active` field before assuming a workflow runs
- WF 02/03/04 run on cron AND can be triggered manually via WF 01
- WF 05 (AI Mozgi) is called by WF 01 Router — not independently triggered
- WF 16→17→34→18 is the Content Factory pipeline: collect → process → moderate → publish
- WF 33 (Channel Analysts) builds per-channel memory — runs every 4h, updates ChannelMemory tab
- WF 34 (Content Executor) auto-publishes high-score articles, sends low-score for operator review
- Use `editorial-review` skill for article moderation, not this skill
- WF 19-25 are TG-Kombain automation crons — they run autonomously
- WF 26-30 are agent ecosystem support — don't trigger manually unless debugging
