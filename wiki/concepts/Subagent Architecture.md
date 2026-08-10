---
title: "Subagent Architecture"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - agentic-design
  - claude-code
source: "[[Create custom subagents]]"
---

# Subagent Architecture

**Subagent Architecture** is the multi-agent delegation pattern in [[Claude Code]] where a primary orchestrator agent spawns specialized worker subagents operating in isolated, fresh 200K context windows.

---

## Delegation Topography

```mermaid
graph TD
    MainSession["Main Session Context (Orchestrator)"] -- "Agent(code-reviewer, prompt)" --> SubagentWindow["Fresh Subagent Context (200K Window)"]
    SubagentWindow -- "Reads 50,000+ Tokens of Code/Logs" --> SubagentProcess["Subagent Execution Phase"]
    SubagentProcess -- "Returns Concise ~350 Token Summary" --> MainSession
```

## Key Architectural Advantages

1. **Context Window Protection**: Prevents massive file dumps, log outputs, and search results from degrading the main conversation context window.
2. **Cost Optimization**: Routes targeted research or search subtasks to smaller/cheaper models (e.g. `haiku`).
3. **Granular Permissions & Sandboxing**: Restricts tool pools (`disallowedTools: Write, Edit`) or forces worktree isolation (`isolation: worktree`).
4. **Scoped MCP Servers**: Connects heavy MCP servers (like Playwright or database connectors) strictly inside subagent windows, keeping their tool definitions out of the main prompt.

See [[Create custom subagents]], [[Subagent Context Isolation]], [[Subagent Worktree Isolation]], and [[Orchestrator Skill Pattern]].
