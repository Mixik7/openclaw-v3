---
summary: "Local infrastructure notes"
---
# TOOLS.md - Content Factory Infrastructure

## n8n (Workflow Automation)

- **URL:** https://n8n-production-fc90.up.railway.app
- **API Auth:** Header `X-N8N-API-KEY` with JWT token from `$N8N_API_KEY`
- **Workflows:** 30 total (13 active production + 8 inactive _v3 fixes + others)

### Key Workflows
| Name | Purpose | Status |
|------|---------|--------|
| 1_Router_Core | Telegram command routing | Active |
| 2_Content_Scheduler | Cron video publishing | Active |
| 2a_Channel_Worker_Acc01 | YouTube upload (Karinaranevskay) | Active |
| 2a_Channel_Worker_Acc02 | YouTube upload (singularity.shift.help) | Active |
| 3_Status_Service | Channel monitoring | Active |
| 5_AI_Chat | AI responses | Active |
| 6_Suno_Music | Music generation | Active |
| 7_Event_Logger | Logging to Google Sheet | Active |

### v3 Workflows (fixed, inactive — testing)
All have `_v3` suffix. Same as above but with bug fixes applied.

## Google Sheets (Source of Truth)

- **Sheet ID:** 1lFwmozG-ci94UFV_kmzVVyHKz_y4FUfCAj4p1KnBSkw
- **Content:** Channel config (ch_001, ch_002, ch_003), credentials mapping

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
