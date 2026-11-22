---
title: "Run agents in parallel"
date: 2026-08-10
tags:
  - source
  - agents
  - parallelism
  - harness-engineering
  - claude-code
source: "raw/articles/claude-code/agent-architecture-subagents-workflows/agents.md"
url: "https://code.claude.com/docs/en/agents.md"
---

# Run agents in parallel

**URL**: https://code.claude.com/docs/en/agents.md  
**Source File**: [raw/articles/claude-code/agent-architecture-subagents-workflows/agents.md](../../raw/articles/claude-code/agent-architecture-subagents-workflows/agents.md)  

---

## Executive Summary

This official Anthropic guide presents the unified decision taxonomy for running parallel agent execution models in [Claude Code](../entities/Claude%20Code.md): **Subagents**, **Agent View**, **Agent Teams**, and **Dynamic Workflows**.

---

## Comparative Matrix of Parallel Execution Approaches

| Approach | Primary Use Case | Coordinator | Worker Communication | Workspace Isolation | Scale Limit |
| --- | --- | --- | --- | --- | --- |
| **Subagents** | Context isolation for side research | Parent LLM session | Reports summary to parent | Optional (`isolation: worktree`) | Few workers per turn |
| **Agent View** | Independent tasks dispatched by user | Human developer | Cross-session messaging | Automated worktrees | Multi-task dashboard |
| **Agent Teams** | Multi-agent peer collaboration on projects | Lead Agent | Shared task list + Direct messaging | Partitioned file paths | Handful of peer sessions |
| **Dynamic Workflows** | Massive codebase audits / multi-file refactors | Background JS Script | Variable passing & JS arrays | Script-governed execution | Dozens to 100+ agents |

---

## Related Knowledge Nodes

- **Concepts**:
  - [Parallel Agent Architecture](../concepts/Parallel%20Agent%20Architecture.md)
  - [Subagent Architecture](../concepts/Subagent%20Architecture.md)
  - [Dynamic Workflows](../concepts/Dynamic%20Workflows.md)
  - [Git Worktree Isolation](../concepts/Git%20Worktree%20Isolation.md)
  - [Agent Teams Architecture](../concepts/Agent%20Teams%20Architecture.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
