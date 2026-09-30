#!/usr/bin/env node
/**
 * Minimal MCP Streamable HTTP client example (Node 18+ or Bun).
 *
 * Usage:
 *   MCP_API_KEY=pr_live_... node examples/mcp-client.js
 *   MCP_URL=http://localhost:3000/mcp MCP_API_KEY=... node examples/mcp-client.js
 *
 * Reads MCP_URL (default https://sports.raglab.services/mcp) and MCP_API_KEY.
 * Lists the tool catalog, then calls get_power_rankings for the current season.
 */

const ENDPOINT = process.env.MCP_URL || "https://sports.raglab.services/mcp";
const API_KEY = process.env.MCP_API_KEY;

if (!API_KEY) {
  console.error("Set MCP_API_KEY=pr_live_... (create a key at the developer page).");
  process.exit(1);
}

/** The server may answer with JSON or with an SSE `data:` line. */
function parseBody(contentType, text) {
  if (!contentType.includes("text/event-stream")) return JSON.parse(text);
  const line = text.split("\n").find((entry) => entry.startsWith("data: "));
  if (!line) throw new Error(`No SSE data line in response: ${text.slice(0, 200)}`);
  return JSON.parse(line.slice(6));
}

async function call(payload) {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
    },
    body: JSON.stringify(payload),
  });
  const text = await response.text();
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${text.slice(0, 300)}`);
  const message = parseBody(response.headers.get("content-type") || "", text);
  if (message.error) throw new Error(`MCP error ${message.error.code}: ${message.error.message}`);
  return message.result;
}

async function main() {
  const list = await call({ jsonrpc: "2.0", id: 1, method: "tools/list" });
  console.log(`${list.tools.length} tools available:\n`);
  for (const tool of list.tools) console.log(`- ${tool.name} — ${tool.title}`);

  const rankings = await call({
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: { name: "get_power_rankings", arguments: {} },
  });
  if (rankings.isError) throw new Error(rankings.content?.[0]?.text || "get_power_rankings failed");
  console.log("\nget_power_rankings:\n");
  console.log(JSON.stringify(rankings.structuredContent ?? rankings.content?.[0]?.text, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
