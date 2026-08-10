---
title: "Run agents in parallel"
date: 2026-08-10
tags:
  - source
  - agents
  - parallelism
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/agent-architecture-subagents-workflows/agents.md]]"
url: "https://code.claude.com/docs/en/agents.md"
---

# Run agents in parallel

**URL**: https://code.claude.com/docs/en/agents.md  
**Source File**: [[raw/articles/claude-code/agent-architecture-subagents-workflows/agents.md]]  

---

## Executive Summary

This official Anthropic guide presents the unified decision taxonomy for running parallel agent execution models in [[Claude Code]]: **Subagents**, **Agent View**, **Agent Teams**, and **Dynamic Workflows**.

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

- **Concepts**: [[Parallel Agent Architecture]], [[Subagent Architecture]], [[Dynamic Workflows]], [[Git Worktree Isolation]], [[Agent Teams Architecture]].
- **Entities**: [[Claude Code]], [[Anthropic]].
