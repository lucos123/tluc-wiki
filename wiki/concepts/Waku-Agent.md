---
title: "Waku-Agent"
date: 2026-08-04
tags:
  - concept
  - tool
  - graph-engineering
  - harness-engineering
source: "wiki/sources/You Can Learn AI Agent Graph Engineering In 21 Min.md"
---

# Waku-Agent

**Waku-Agent** is an open-source AI agent framework developed by [Sean's AI Stories](../entities/Sean%27s%20AI%20Stories.md) (>700 stars) that demonstrates production-grade [Graph Engineering](Graph%20Engineering.md).

---

## Architectural Workflow

```mermaid
graph TD
    User["User Request"] --> Router["1. Router / Classifier Node"]
    Router --> Memory["2. Memory Retrieval Node"]
    Memory --> Execution["3. Tool / MCP Execution Node"]
    Execution --> Eval["4. Eval & Verification Gate"]
    Eval --> Output["5. Final Response"]
```

1. **Router Node**: Classifies the incoming prompt and selects the appropriate Graph topology.
2. **Memory Retrieval Node**: Pulls relevant long-term and session state.
3. **Tool Execution Node**: Calls external APIs and MCP servers.
4. **Eval Gate**: Verifies response quality before output.

See [Graph Engineering](Graph%20Engineering.md) and [Agent Graph](Agent%20Graph.md).
