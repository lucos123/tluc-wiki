---
title: "SDK Subagents"
date: 2026-08-10
tags:
  - concept
  - agent-sdk
  - subagents
  - harness-engineering
  - claude-code
source: "[[Subagents in the SDK]]"
---

# SDK Subagents

**SDK Subagents** is the programmatic mechanism in the Claude Agent SDK for dynamically registering in-memory worker agents (`AgentDefinition`) that execute isolated tasks on behalf of a primary orchestrator.

---

## Architectural Topography

```mermaid
graph TD
    ParentQuery["Parent query(prompt=...)"] -- "Agent(code-reviewer, prompt)" --> SubagentProcess["Programmatic Subagent (AgentDefinition)"]
    SubagentProcess -- "Runs in fresh 200K context window" --> WorkPhase["Executes Read/Grep/Glob"]
    WorkPhase -- "Returns final message only" --> ParentQuery
```

## Key Capabilities

1. **In-Memory Programmatic Registration**: Can be registered dynamically via `ClaudeAgentOptions.agents` without writing `.claude/agents/*.md` files to disk.
2. **Precedence Hierarchy**: Programmatic SDK definitions take priority over disk-based project/personal subagents with identical names.
3. **Background Execution**: Subagents execute asynchronously by default without blocking the parent loop thread.

See [[Subagents in the SDK]], [[Subagent Architecture]], and [[Agent SDK Architecture]].
