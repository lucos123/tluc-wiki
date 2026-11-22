---
title: "Subagent Context Isolation"
date: 2026-08-10
tags:
  - concept
  - context-engineering
  - harness-engineering
  - claude-code
source: "wiki/sources/Explore the context window.md"
---

# Subagent Context Isolation

**Subagent Context Isolation** is a core pattern in [Harness Engineering](Harness%20Engineering.md) and [Context Engineering](Context%20Engineering.md) where heavy research, file exploration, or code auditing is delegated to an auxiliary subagent running in a separate, isolated context window.

---

## Architectural Mechanics

```mermaid
graph TD
    Main["Main Session (Context: 12,000 / 200,000t)"] -- "Prompt: Research auth flow" --> Sub["Subagent Session (Fresh Context: 0 / 200,000t)"]
    Sub -- "Reads 8 files (16,000t)" --> Sub
    Sub -- "Analyzes & Verifies" --> Sub
    Sub -- "Returns 350t Summary Result" --> Main
```

## Benefits

1. **Context Protection**: Prevents main conversation window from thrashing or reaching context compaction during codebase exploration.
2. **Cost Efficiency**: Reduces input token costs on subsequent main turn calls by keeping the main context slim.
3. **Task Specialization**: Subagents run with custom system prompts, specialized skill subsets, or path restrictions tailored to their specific subtask.

See [Explore the context window](../sources/Explore%20the%20context%20window.md), [Context Window Management](Context%20Window%20Management.md), and [Second Opinion Pattern](Second%20Opinion%20Pattern.md).
