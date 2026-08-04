---
title: "Waku-Agent"
date: 2026-08-04
tags:
  - concept
  - tool
  - graph-engineering
  - harness-engineering
source: "[[You Can Learn AI Agent Graph Engineering In 21 Min]]"
---

# Waku-Agent

**Waku-Agent** is an open-source AI agent framework developed by [[Sean's AI Stories]] (>700 stars) that demonstrates production-grade [[Graph Engineering]].

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

See [[Graph Engineering]] and [[Agent Graph]].
