---
title: "MCP Transports"
date: 2026-08-10
tags:
  - concept
  - mcp
  - harness-engineering
  - claude-code
source: "[[Connect Claude Code to tools via MCP]]"
---

# MCP Transports

**MCP Transports** define the physical communication channels used by the [[Model Context Protocol]] in [[Claude Code]] to exchange tool definitions, resource schemas, and execution requests between agent hosts and tool servers.

---

## Transport Modalities

1. **HTTP (`streamable-http`)**: Recommended standard for cloud-based microservices and SaaS APIs. Supports OAuth, custom headers, and request caching (`MCP_DISCOVERY_CACHE`).
2. **stdio**: Spawns local child processes (`npx`, `python`) on the developer's machine. Receives `$CLAUDE_PROJECT_DIR` in environment. Requires `--` syntax separator.
3. **WebSocket (`ws`)**: Persistent bidirectional transport (`wss://`) ideal for event-driven channel push updates (Slack/Discord webhooks).
4. **SSE (`sse`)**: Legacy Server-Sent Events transport (deprecated in favor of HTTP).

See [[Connect Claude Code to tools via MCP]], [[Model Context Protocol]], and [[Tool Search Architecture]].
