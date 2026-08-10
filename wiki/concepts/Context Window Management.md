---
title: "Context Window Management"
date: 2026-08-10
tags:
  - concept
  - context-engineering
  - cost-optimization
  - claude-code
source: "[[Best practices for Claude Code]]"
---

# Context Window Management

**Context Window Management** is the single most critical practice in agentic software engineering. Because LLM performance degrades as context fills up with conversation history, file reads, and command outputs, active context management preserves model accuracy and reduces cost.

---

## Core Strategies

1. **Concise Persistent Files (`CLAUDE.md`)**: Keep advisory files lean. Bloated instruction files cause models to miss critical rules.
2. **Progressive Disclosure**: Use [[Progressive Disclosure]] (`SKILL.md`, `ToolSearch`) to load domain instructions and tools only on demand.
3. **Session Resetting & Compacting**: Use `/compact` or restart fresh sessions when switching tasks to prune stale conversation state.
4. **Plan Mode Isolation**: Perform exploration in `plan mode` so exploratory file reading doesn't pollute the main implementation context.

See [[Best practices for Claude Code]] and [[Progressive Disclosure]].
