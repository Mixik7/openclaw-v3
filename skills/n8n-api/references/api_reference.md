# n8n REST API Reference

Base URL: `$N8N_BASE_URL/api/v1`
Auth header: `X-N8N-API-KEY: $N8N_API_KEY`

## Workflows

### GET /workflows
List all workflows. Returns `{ data: Workflow[] }`.

### GET /workflows/:id
Get single workflow with all nodes and connections.

### POST /workflows
Create new workflow. Body: `{ name, nodes, connections, settings?, active? }`.

### PATCH /workflows/:id
Update workflow. Body: partial workflow object.
Use `{ "active": true/false }` to activate/deactivate.

### DELETE /workflows/:id
Delete workflow permanently. **Use with caution.**

## Executions

### GET /executions
List executions. Query params: `limit`, `cursor`, `status`, `workflowId`.
Status values: `success`, `error`, `waiting`, `running`.

### GET /executions/:id
Get execution details including node results and errors.

### DELETE /executions/:id
Delete an execution record.

## Credentials

### GET /credentials
List all credentials (no secrets). Returns `{ data: Credential[] }`.

### GET /credentials/:id
Get credential details (type, name, no secrets).

## Webhook Endpoints

Workflows with Webhook nodes expose endpoints at:
- Production: `$N8N_BASE_URL/webhook/PATH`
- Test: `$N8N_BASE_URL/webhook-test/PATH`

## Rate Limits

n8n self-hosted has no built-in rate limits, but Railway containers have CPU/memory limits.
Recommended: max 10 requests/second.

## Error Responses

```json
{
  "code": 404,
  "message": "Workflow not found"
}
```

Common codes: 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error).
