#!/usr/bin/env python3
"""Minimal MCP Streamable HTTP client example (Python 3.8+, standard library only).

Usage:
    MCP_API_KEY=pr_live_... python3 examples/mcp-client.py
    MCP_URL=http://localhost:3000/mcp MCP_API_KEY=... python3 examples/mcp-client.py

Reads MCP_URL (default https://sports.raglab.services/mcp) and MCP_API_KEY.
Lists the tool catalog, then calls get_power_rankings for the current season.
"""

import json
import os
import urllib.error
import urllib.request

ENDPOINT = os.environ.get("MCP_URL", "https://sports.raglab.services/mcp")
API_KEY = os.environ.get("MCP_API_KEY")

if not API_KEY:
    raise SystemExit("Set MCP_API_KEY=pr_live_... (create a key at the developer page).")


def parse_body(content_type, text):
    """The server may answer with JSON or with an SSE `data:` line."""
    if "text/event-stream" not in content_type:
        return json.loads(text)
    for line in text.splitlines():
        if line.startswith("data: "):
            return json.loads(line[len("data: "):])
    raise RuntimeError("No SSE data line in response: %s" % text[:200])


def call(payload):
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer %s" % API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            content_type = response.headers.get("Content-Type", "")
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        raise RuntimeError("HTTP %s: %s" % (error.code, body[:300]))
    message = parse_body(content_type, text)
    if message.get("error"):
        raise RuntimeError("MCP error %s: %s" % (message["error"].get("code"), message["error"].get("message")))
    return message["result"]


def main():
    listing = call({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    print("%d tools available:\n" % len(listing["tools"]))
    for tool in listing["tools"]:
        print("- %s — %s" % (tool["name"], tool.get("title", "")))

    rankings = call({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "get_power_rankings", "arguments": {}},
    })
    if rankings.get("isError"):
        raise RuntimeError(rankings["content"][0]["text"] if rankings.get("content") else "get_power_rankings failed")
    payload = rankings.get("structuredContent")
    if payload is None:
        payload = json.loads(rankings["content"][0]["text"])
    print("\nget_power_rankings:\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
