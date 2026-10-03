# Quickstart

From zero to your first tool call in six steps. The MCP server is read-only
and requires a Pro entitlement with the `mcp_server` feature; keys are created
from the developer page at https://sports.raglab.services/developers.

## 1. Sign in and get a key

Open https://sports.raglab.services/developers, sign in, and create an API key. Keys look like
`pr_live_…` and are shown **once** at creation — copy it immediately. If a key
leaks or is no longer needed, revoke it on the same page; revoked keys stop
working immediately.

## 2. Connect a client

Paste this into `.cursor/mcp.json` or `.vscode/mcp.json`:

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

Claude Code, Claude Desktop, and a `curl` smoke test are in
[`developers.md`](developers.md).

## 3. Verify the connection

Ask the client to list tools, or:

```bash
curl -s https://sports.raglab.services/mcp \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

A healthy response lists 47 tools. A `401`
(`code: "unauthenticated"`) means the key is missing or wrong; a `403` means
the account has no active Pro entitlement.

## 4. Make a first call

Recommended first tools:

1. `list_teams` — resolve official tri-codes (TOR, MTL, NYR).
2. `get_power_rankings` — all 32 teams with score and 1/7/30-day movement.
3. `get_games` — today's cards, with model win probabilities when stored.
4. `get_game_analysis` — deeper edge analysis for one game id from `get_games`.

## 5. Read the envelope

Every result is `{ schemaVersion, data, meta, evidence }`. Before using data,
check `meta.asOf` (freshness), `meta.completeness`, and `meta.warnings`.
List tools paginate with `meta.pagination.nextCursor`. See
[`samples.md`](samples.md) for complete example payloads.

## 6. Know the limits

- Per-key rate limit: 120 requests per minute by default; a `429` carries
  `Retry-After`. Back off and retry after the indicated delay.
- Power scores and PAA are snapshot-relative and descriptive, not calibrated
  win probabilities.
- Seasons are 8-digit ids (`20252026`); omit the season argument for the
  current one.

Next: [`tools.md`](tools.md) for the full catalog and
[`glossary.md`](glossary.md) for the data semantics.
