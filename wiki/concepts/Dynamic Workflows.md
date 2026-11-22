---
title: "Dynamic Workflows"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - graph-engineering
  - claude-code
source: "wiki/sources/Orchestrate subagents at scale with dynamic workflows.md"
---

# Dynamic Workflows

**Dynamic Workflows** is a programmatic multi-agent orchestration architecture in [Claude Code](../entities/Claude%20Code.md) where complex, large-scale agent operations are codified as JavaScript execution scripts run by a background runtime rather than being navigated turn-by-turn inside an LLM context window.

---

## Architectural Topography

```mermaid
graph TD
    UserPrompt["Prompt (ultracode: audit routes)"] --> ScriptGen["1. Claude Writes JS Workflow Script"]
    ScriptGen --> ScriptRuntime["2. Background JS Runtime Execution"]
    ScriptRuntime --> Agent1["Worker Agent 1 (src/routes/auth.ts)"]
    ScriptRuntime --> Agent2["Worker Agent 2 (src/routes/users.ts)"]
    ScriptRuntime --> AgentN["Worker Agent N (...)"]
    Agent1 & Agent2 & AgentN --> AdvReview["3. Adversarial Cross-Verification Step"]
    AdvReview --> FinalReport["4. Final Consolidated Report to User Session"]
```

## Key Capabilities

1. **Context Window Savings**: Intermediate worker outputs live in JavaScript runtime variables rather than polluting the parent LLM context.
2. **Massive Scale**: Enables scaling to 100+ concurrent subagents in a single execution.
3. **Adversarial Verification**: Scripts can enforce multi-pass cross-verification where subagents audit and vote on each other's findings.

See [Orchestrate subagents at scale with dynamic workflows](../sources/Orchestrate%20subagents%20at%20scale%20with%20dynamic%20workflows.md), [Ultracode Mode](Ultracode%20Mode.md), [Subagent Architecture](Subagent%20Architecture.md), and [Graph Engineering](Graph%20Engineering.md).
