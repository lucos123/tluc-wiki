---
title: "Scale to many tools with tool search"
date: 2026-08-10
tags:
  - source
  - tool-search
  - context-engineering
  - harness-engineering
  - claude-code
source: "raw/articles/claude-code/hooks-tools-mcp-chrome/tool-search.md"
url: "https://code.claude.com/docs/en/tool-search.md"
---

# Scale to many tools with tool search

**URL**: https://code.claude.com/docs/en/tool-search.md  
**Source File**: [raw/articles/claude-code/hooks-tools-mcp-chrome/tool-search.md](../../raw/articles/claude-code/hooks-tools-mcp-chrome/tool-search.md)  

---

## Executive Summary

This official Anthropic guide details **Tool Search** (`ToolSearch`), a dynamic tool discovery and context optimization mechanism in [Claude Code](../entities/Claude%20Code.md).

When agent tool catalogs scale to hundreds or thousands of tools (where static tool schemas consume 10,000–20,000 tokens), Tool Search defers tool schema loading until needed, searching catalog indices on-demand and loading only the top 5 relevant tool definitions into context.

---

## Key Configuration Tuning (`ENABLE_TOOL_SEARCH`)

| Setting Value | Execution Behavior |
| --- | --- |
| `(unset)` | Tool search enabled by default on Claude 4.5+ models. |
| `auto` | Activates Tool Search when combined tool definition tokens exceed 10% of context window. |
| `auto:5` | Activates Tool Search when tool schemas exceed 5% of context window. |
| `false` | Disables Tool Search, forcing all schemas into context on every turn (recommended for <10 tools). |

---

## Performance Thresholds & Scale Limits

- **Maximum Catalog Capacity**: Up to 10,000 tools per session.
- **Top-K Retrieval**: Returns top 5 relevant tool schemas per `ToolSearch` query.
- **Token Efficiency**: Prevents context window saturation when mounting massive enterprise MCP tool clusters.

---

## Related Knowledge Nodes

- **Concepts**:
  - [Tool Search Architecture](../concepts/Tool%20Search%20Architecture.md)
  - [Progressive Disclosure](../concepts/Progressive%20Disclosure.md)
  - [Context Window Management](../concepts/Context%20Window%20Management.md)
  - [Model Context Protocol](../concepts/Model%20Context%20Protocol.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
