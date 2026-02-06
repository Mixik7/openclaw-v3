---
summary: "Local infrastructure notes"
---
# TOOLS.md - Content Factory Infrastructure

## n8n (Workflow Automation)

- **URL:** https://n8n-production-fc90.up.railway.app
- **API Auth:** Header `X-N8N-API-KEY` with JWT token from `$N8N_API_KEY`
- **Workflows:** 35+ total (18 active production + 8 inactive _v3 fixes + others)

### Key Workflows
| Name | ID | Purpose | Status |
|------|----|---------|--------|
| 1_Router_Core | 7h11iwrB... | Telegram command routing | Active |
| 2_Content_Scheduler_v2 | y4gGFSeA... | Cron video publishing (multi-platform) | Active |
| 2a_Channel_Worker_Acc01 | By9t27uH... | YouTube upload (Karinaranevskay) | Active |
| 2a_Channel_Worker_Acc02 | OATVTrrq... | YouTube upload (singularity.shift.help) | Active |
| 2a_Channel_Worker_Acc03 | 14S6Qdk1... | YouTube upload (mi.xi.million) | Active |
| 3_Status_Service | 07HBejiv... | Channel monitoring | Active |
| 5_AI_Chat | xSvhQX0k... | AI responses | Active |
| 6_Suno_Music | wn4VgYjB... | Music generation | Active |
| 7_Event_Logger | KZwQpHP6... | Logging to Google Sheet | Active |
| 12_OpenClaw_Bridge | mXnfHX25... | n8n→OpenClaw AI notifications | Active |
| **8_Platform_Router** | sFRx11bM... | Multi-platform routing (YT/TT/VK) | **Active** |
| **9a_TikTok_Worker** | XgE9q857... | TikTok video publishing | **Active** |
| **9b_VK_Worker** | jn2xPkYw... | VK video publishing | **Active** |
| **10_TikTok_Token_Refresh** | 4xfXnDMi... | Auto-refresh TikTok OAuth tokens (cron 20h) | **Active** |

### Multi-Platform Architecture (Phase 2)
```
Scheduler → [Multi-Platform?]
  ├─ No (youtube only) → Роутинг по credGroup → Worker Acc01/02/03
  └─ Yes (has platforms field) → 8_Platform_Router
       ├─ youtube → Route to Acc01/02/03 by credGroup
       ├─ tiktok → 9a_TikTok_Worker
       ├─ vk → 9b_VK_Worker
       └─ unknown → Log
```

### v3 Workflows (fixed, inactive — backup)
All have `_v3` suffix. Same as above but with bug fixes applied.

## Google Sheets (Source of Truth)

- **Sheet ID:** 1lFwmozG-ci94UFV_kmzVVyHKz_y4FUfCAj4p1KnBSkw
- **Tabs:**
  - **Channels** — Channel config (ch_001-003), folderId, archiveId, credGroup, platform, `platforms` (comma-separated for multi-platform)
  - **PlatformCredentials** — Per-platform credentials (credGroup + platform → accessToken, refreshToken, tokenExpiry, groupId, status)
  - **EventLog** — Publication events log
  - **Metrics** — Performance metrics

## Google Drive

- Videos stored in channel folders
- After publishing, videos moved to archive subfolder

## Railway Projects

| Project | Service | Purpose |
|---------|---------|---------|
| N8N | n8n | Workflow automation (DON'T TOUCH) |
| openclaw-v3 | openclaw-v3 | This bot (IDEA) |
| OPENCLAW-2 | openclaw | Old bot (backup, don't touch) |

## Telegram Bots

| Bot | Purpose |
|-----|---------|
| @IDEA_TOP_BOT | This bot (Content Factory AI) |
| @Open_Claw_7BOT | Old bot (backup) |
| @My_Assistant_content2_bot | n8n Router (fallback commands) |
