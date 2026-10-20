# Developer setup

The RagLab NHL power-ranking server exposes a **read-only** MCP server over
Streamable HTTP. The same catalog drives the interactive developer page at
https://sports.raglab.services/developers.

## Requirements

1. An API key created at https://sports.raglab.services/developers. Keys are shown once at
   creation and look like `pr_live_…`.
2. An active (or past-due) Pro entitlement carrying the `mcp_server` feature.
3. Any MCP client that supports Streamable HTTP, or plain `curl`.

## Endpoint and authentication

- **Endpoint:** `https://sports.raglab.services/mcp` (POST, Streamable HTTP)
- **Authorization:** `Authorization: Bearer pr_live_…`
- **Transport:** stateless — a fresh server instance is built per request, so
  no session initialization handshake is required before `tools/list` or
  `tools/call`.

## Client setup

### Cursor / VS Code (`.cursor/mcp.json` or `.vscode/mcp.json`)

```json
{
  "mcpServers": {
    "nhl-power-ranking": {
      "url": "https://sports.raglab.services/mcp",
      "headers": { "Authorization": "Bearer <YOUR_API_KEY>" }
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http nhl-power-ranking https://sports.raglab.services/mcp \
  --header "Authorization: Bearer <YOUR_API_KEY>"
```

### Claude Desktop (via `mcp-remote`)

```json
{
  "mcpServers": {
    "nhl-power-ranking": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "https://sports.raglab.services/mcp",
        "--header", "Authorization: Bearer <YOUR_API_KEY>"
      ]
    }
  }
}
```

### Smoke test with curl

```bash
curl -s https://sports.raglab.services/mcp \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

The server may answer with `application/json` or `text/event-stream`
(SSE). For SSE, parse the first `data: ` line as JSON. Runnable clients are in
[`../examples/`](../examples).

## Keys, plans, and limits

- Keys are created on the developer page, shown **once**, and should be stored
  in a secret manager. Revoke a key from the same page when it is no longer
  needed; revoked keys stop working immediately.
- The MCP server requires an active Pro entitlement carrying the `mcp_server`
  feature. A key on an account without it returns `403` until the plan is
  active again; past-due accounts keep access during the grace period.
- Per-key rate limit: **120 requests per minute** by default. Exceeding it
  returns `429` (`code: "rate_limited"`) with a `Retry-After` header; back off
  for that many seconds before retrying.

## Result contract

Server contract `2.1.0` returns a versioned object envelope from
every successful tool:

```json
{
  "schemaVersion": "1.0.0",
  "data": {},
  "meta": {
    "serverVersion": "2.1.0",
    "generatedAt": "2026-09-24T12:00:00.000Z",
    "season": 20262027,
    "asOf": "2026-09-24",
    "source": "postgres:power_history",
    "completeness": "complete",
    "modelVersion": null,
    "warnings": []
  },
  "evidence": []
}
```

- Successful output is identical in `content[0].text` (JSON string) and
  `structuredContent`.
- List tools expose `meta.pagination` with `total`, `returned`, `hasMore`, and
  an opaque `nextCursor`. Pass `cursor` back unchanged.
- Inspect `meta.asOf`, `meta.completeness`, and `meta.warnings` before relying
  on a result.

## Errors

| Status | Code | Meaning |
|---|---|---|
| 401 | `invalid_token` | Missing or invalid API key |
| 403 | — | Key valid but the account lacks an active `mcp_server` entitlement |
| 429 | `rate_limited` | Per-key request limit exceeded; honor `Retry-After` |

## Data notes

- Seasons are 8-digit ids (`20252026` = the 2025-26 season); omit the season
  argument for the current one.
- Team codes are official NHL tri-codes (TOR, MTL, NYR); call `list_teams` to
  resolve or verify them.
- Power scores, normalized metric scores, and PAA are snapshot-relative and
  descriptive, not calibrated win probabilities.
- Metric definitions are available at runtime through `get_metric_definitions`
  and the `power-ranking://docs/metrics` resource. See
  [`metrics.md`](metrics.md) for the public definitions summary.
