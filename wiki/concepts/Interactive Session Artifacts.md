---
title: "Interactive Session Artifacts"
date: 2026-08-10
tags:
  - concept
  - web-publishing
  - harness-engineering
  - claude-code
source: "wiki/sources/Share session output as artifacts.md"
---

# Interactive Session Artifacts

**Interactive Session Artifacts** is a web-publishing feature in [Claude Code](../entities/Claude%20Code.md) that transforms CLI session state into client-side HTML/Markdown visual dashboards hosted on `claude.ai/code/artifact`.

---

## Technical Features

1. **Connector-Backed Rendering**: Artifacts invoke cloud [MCP connectors](Model%20Context%20Protocol.md) (GitHub, Jira, PostgreSQL) using the viewer's active credentials to fetch fresh data on page load.
2. **Strict CSP Boundary**: Inlines all JavaScript and CSS assets into a single static file (max 16 MiB) rendered under a sandboxed `*.claudeusercontent.com` domain.
3. **Multi-Session Versioning**: Artifact URLs (`https://claude.ai/code/artifact/<id>`) accept updates from multiple Claude sessions or team editors.

See [Share session output as artifacts](../sources/Share%20session%20output%20as%20artifacts.md), [Model Context Protocol](Model%20Context%20Protocol.md), and [Harness Engineering](Harness%20Engineering.md).
