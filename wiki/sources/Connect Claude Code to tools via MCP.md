---
title: "Connect Claude Code to tools via MCP"
date: 2026-08-10
tags:
  - source
  - mcp
  - harness-engineering
  - integrations
  - claude-code
source: "raw/articles/claude-code/hooks-tools-mcp-chrome/mcp.md"
url: "https://code.claude.com/docs/en/mcp.md"
---

# Connect Claude Code to tools via MCP

**URL**: https://code.claude.com/docs/en/mcp.md  
**Source File**: [raw/articles/claude-code/hooks-tools-mcp-chrome/mcp.md](../../raw/articles/claude-code/hooks-tools-mcp-chrome/mcp.md)  

---

## Executive Summary

This official Anthropic guide details how to integrate external tools, databases, and services into [Claude Code](../entities/Claude%20Code.md) using the **Model Context Protocol (MCP)**.

MCP provides standardized interfaces for local tools (`stdio`), remote APIs (`http`/`streamable-http`), and bidirectional event streams (`ws`), enabling Claude Code to query databases (PostgreSQL), fetch issue trackers (Jira/GitHub), inspect monitoring dashboards (Sentry), and auto-react to webhooks.

---

## MCP Transport Modes

```
               ┌─────────────────────────────────────────┐
               │    Claude Code Agent Host Engine         │
               └────────────────────┬────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
 [ HTTP Transport ]         [ stdio Transport ]         [ WebSocket Transport ]
  Remote Cloud APIs          Local Process Spawn         Bidirectional Events
 (Notion, GitHub, REST)      (npx, python, env)          (wss:// sockets)
```

---

## Configuration & CLI Commands

```bash
# Add HTTP server (recommended for remote APIs)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Add stdio server (local subprocess)
claude mcp add --env AIRTABLE_API_KEY=xyz --transport stdio airtable -- npx -y airtable-mcp-server

# List & get details
claude mcp list
claude mcp get notion
```

---

## Related Knowledge Nodes

- **Concepts**:
  - [Model Context Protocol](../concepts/Model%20Context%20Protocol.md)
  - [MCP Transports](../concepts/MCP%20Transports.md)
  - [Tool Search Architecture](../concepts/Tool%20Search%20Architecture.md)
  - [Harness Engineering](../concepts/Harness%20Engineering.md)
- **Entities**:
  - [Claude Code](../entities/Claude%20Code.md)
  - [Anthropic](../entities/Anthropic.md)
  - [Model Context Protocol](../concepts/Model%20Context%20Protocol.md)
