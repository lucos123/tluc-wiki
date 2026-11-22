---
title: "Agent Graph"
date: 2026-08-04
tags:
  - concept
  - graph-engineering
  - agentic-design
source: "wiki/sources/Why Graph Engineering will 10x your Claude Codex.md"
---

# Agent Graph

An **Agent Graph** is an execution workflow topology where discrete AI agent runtimes (nodes) perform specialized steps, checks, handoffs, and parallel tasks connected by data and control paths (edges).

Introduced by [Greg Isenberg](../entities/Greg%20Isenberg.md) in [Why Graph Engineering will 10x your Claude Codex](../sources/Why%20Graph%20Engineering%20will%2010x%20your%20Claude%20Codex.md).

---

## Core Mechanics

Unlike a linear chat thread, an Agent Graph structures work into discrete nodes:
1. **Planner Node**: Breaks down a prompt into specialized research or engineering angles.
2. **Parallel Subagent Nodes (Fan-Out)**: Specialized workers executing tasks concurrently in isolated context windows.
3. **Skeptic / Evaluator Node**: Dedicated review subagent attempting to invalidate weak findings or catch code bugs (see [Second Opinion Pattern](Second%20Opinion%20Pattern.md)).
4. **Merger Node (Fan-In)**: Combines surviving findings into a synthesized output.
5. **Human-in-the-Loop Gate**: Pauses execution for human approval before applying changes to production.

---

## Agent Graph vs. Knowledge Graph

- **Agent Graph**: Governs *how work moves* across agents and workflows.
- **Knowledge Graph**: Governs *how information connects* across entities and data points.

See [Knowledge Graph vs Agent Graph](Knowledge%20Graph%20vs%20Agent%20Graph.md) and [Graph Engineering](Graph%20Engineering.md).
