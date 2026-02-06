#!/usr/bin/env bash
# n8n-status.sh — Quick overview of all workflows and recent executions
# Usage: bash {baseDir}/scripts/n8n-status.sh

set -euo pipefail

API_KEY="${N8N_API_KEY:?N8N_API_KEY not set}"
BASE_URL="${N8N_BASE_URL:?N8N_BASE_URL not set}"

echo "=== n8n Workflows ==="
curl -s "$BASE_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $API_KEY" | \
  jq -r '.data[] | "\(.active | if . then "✅" else "⏸ " end) \(.name) (id: \(.id))"' | sort

echo ""
echo "=== Last 5 Executions ==="
curl -s "$BASE_URL/api/v1/executions?limit=5" \
  -H "X-N8N-API-KEY: $API_KEY" | \
  jq -r '.data[] | "\(.status | if . == "success" then "✅" elif . == "running" then "🔄" else "❌" end) \(.workflowId) — \(.startedAt // "unknown") [\(.status)]"'
