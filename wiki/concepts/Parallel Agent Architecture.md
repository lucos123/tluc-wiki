---
title: "Parallel Agent Architecture"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - parallelism
  - agentic-design
  - claude-code
source: "[[Run agents in parallel]]"
---

# Parallel Agent Architecture

**Parallel Agent Architecture** is the system design framework in [[Claude Code]] for structuring multi-agent execution across four distinct operational modalities based on coordination mechanisms, communication topographies, and file isolation boundaries.

---

## Architectural Decision Framework

```mermaid
graph TD
    Request["Parallel Task Request"] --> Who{"Who Coordinates?"}
    Who -- "Parent LLM Turn" --> Subagents["1. Subagents (Context-Isolated Workers)"]
    Who -- "Human Developer" --> AgentView["2. Agent View (Background Session Dashboard)"]
    Who -- "Lead Agent" --> AgentTeams["3. Agent Teams (Shared Task List & Inter-Agent Messages)"]
    Who -- "JS Script Code" --> Workflows["4. Dynamic Workflows (JS Runtime Script Execution)"]
```

## Selection Criteria

1. **Subagents**: Use when side-tasks (logs, large file reads) threaten to saturate the primary context window.
2. **Agent View**: Use when managing multiple completely independent feature tasks across git worktrees.
3. **Agent Teams**: Use when a complex project requires peer agents with specialized roles communicating via a shared task backlog.
4. **Dynamic Workflows**: Use when fanning out audits or refactors to 100+ agents with automated cross-verification.

See [[Run agents in parallel]], [[Subagent Architecture]], [[Dynamic Workflows]], and [[Git Worktree Isolation]].
