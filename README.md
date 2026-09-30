# RagLab Sports — NHL Power Ranking public documentation

Open documentation for the RagLab NHL power-ranking platform. This repository
(`https://github.com/raglab-ca/sports`) is generated from the private source codebase — see **Generated
files** below — and contains no model implementation.

- **Live site:** https://sports.raglab.services
- **MCP endpoint:** https://sports.raglab.services/mcp (POST, Streamable HTTP, bearer API key)
- **MCP server:** `nhl-power-ranking` v2.1.0 · contract schema
  v1.0.0 · 47 tools, 7 prompts,
  3 resources
- **Power model:** v1.4.0 · 78 metrics across
  7 sections (definitions only — formulas are not published)

## Files

- [`llms.txt`](llms.txt) — concise index of this repository and the MCP
  surface for LLM crawlers ([llmstxt.org](https://llmstxt.org)).
- [`llms-full.txt`](llms-full.txt) — complete context: server instructions,
  every tool with parameters, prompts, resources, the data glossary, and
  redacted metric definitions.
- [`agent-card.json`](agent-card.json) — A2A-shaped discovery card. The live
  copy is served at https://sports.raglab.services/.well-known/agent-card.json.
- [`docs/quickstart.md`](docs/quickstart.md) — six steps from API key to first
  tool call.
- [`docs/developers.md`](docs/developers.md) — API keys, client setup, result
  envelope, and error codes.
- [`docs/tools.md`](docs/tools.md) — full MCP tool catalog with parameters.
- [`docs/samples.md`](docs/samples.md) — complete example payloads for common
  tools.
- [`docs/prompts.md`](docs/prompts.md) — built-in prompt workflows.
- [`docs/resources.md`](docs/resources.md) — readable server resources.
- [`docs/glossary.md`](docs/glossary.md) — freshness, identifiers, and
  methodology notes.
- [`docs/metrics.md`](docs/metrics.md) — power metric definitions: what each
  metric represents, its unit, and its direction. Computation details are not
  published.
- [`docs/manifest.redacted.json`](docs/manifest.redacted.json) —
  machine-readable redacted model manifest.
- [`examples/`](examples) — minimal MCP clients in JavaScript and Python, plus
  a client configuration sample.

## What is not here

The power model implementation, scoring formulas, normalization and
aggregation internals, data sources, ingestion jobs, and the private web
application are not part of this repository. The MCP server exposes live data
to authenticated clients; see [`docs/developers.md`](docs/developers.md).

## Access

The MCP server is read-only and requires an API key created from
https://sports.raglab.services/developers with an active Pro entitlement (the `mcp_server`
feature). Unauthenticated requests are rejected.

## Generated files

`llms.txt`, `llms-full.txt`, `agent-card.json`, and everything under `docs/`
except `developers.md` are generated at export time from the live server
catalog, then pushed here by CI. Do not edit generated files by hand; changes
belong in the source repository.

Synced from commit `local`.

## License

MIT — see [LICENSE](LICENSE). The license covers this documentation and the
example clients only; the RagLab platform itself is proprietary.
