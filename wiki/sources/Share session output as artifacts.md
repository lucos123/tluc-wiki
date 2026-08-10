---
title: "Share session output as artifacts"
date: 2026-08-10
tags:
  - source
  - artifacts
  - web-publishing
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/hooks-tools-mcp-chrome/artifacts.md]]"
url: "https://code.claude.com/docs/en/artifacts.md"
---

# Share session output as artifacts

**URL**: https://code.claude.com/docs/en/artifacts.md  
**Source File**: [[raw/articles/claude-code/hooks-tools-mcp-chrome/artifacts.md]]  

---

## Executive Summary

This official Anthropic guide details **Session Artifacts** in [[Claude Code]].

Artifacts convert terminal session output into interactive HTML/Markdown web pages hosted on `claude.ai/code/artifact`. They allow developers to publish annotated pull request diffs, side-by-side design comparisons, live system health dashboards, and investigation progress boards that update live as tasks execute.

---

## Live Data & MCP Connector Integration

```
                                  ┌───────────────────────────────┐
                                  │   claude.ai/code/artifact    │
                                  └───────────────┬───────────────┘
                                                  │
                  ┌───────────────────────────────┴───────────────────────────────┐
                  ▼                                                               ▼
        [ Viewer Account Credentials ]                                  [ Live MCP Connectors ]
        Permission approval per viewer                                  Fetches fresh GitHub/Jira/
        Access controlled per viewer identity                           PostgreSQL data on render
```

---

## Page Constraints & Security Policy

| Constraint | Architectural Boundary |
| --- | --- |
| **No External Requests** | CSP blocks external fetch/XHR; CSS/JS inlined, images embedded as Data URIs. |
| **No Backend** | Static client-side bundles (no custom backend database/routing). |
| **Sandboxed Origin** | Served under `*.claudeusercontent.com` with 16MiB render size cap. |
| **Keyboard Shortcut** | `Ctrl+]` reopens most recent session artifact URL. |

---

## Related Knowledge Nodes

- **Concepts**: [[Interactive Session Artifacts]], [[Model Context Protocol]], [[Harness Engineering]].
- **Entities**: [[Claude Code]], [[Anthropic]].
