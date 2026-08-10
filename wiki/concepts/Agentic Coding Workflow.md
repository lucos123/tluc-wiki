---
title: "Agentic Coding Workflow"
date: 2026-08-10
tags:
  - concept
  - agentic-design
  - harness-engineering
  - best-practices
source: "[[Best practices for Claude Code]]"
---

# Agentic Coding Workflow

The **Agentic Coding Workflow** is the operational methodology where an engineer transitions from writing code manually to directing an autonomous agent ([[Claude Code]]) through a structured 4-phase lifecycle:

```mermaid
graph TD
    Explore["1. Explore (Plan Mode)"] --> Plan["2. Plan (Architectural Spec)"]
    Plan --> Implement["3. Implement (Execute & Verify)"]
    Implement --> Commit["4. Commit & PR"]
```

## Core Principles

1. **Autonomous Execution**: The agent reads files, executes commands, fixes errors, and verifies its own work.
2. **Phase Separation**: Separating research/planning (non-modifying `plan mode`) from code editing avoids implementing the wrong solution.
3. **Evidence-Based Success**: Requiring the agent to produce empirical evidence (passing test logs, build outputs, visual diffs) before ending a turn.

See [[Best practices for Claude Code]], [[Verification Loop]], and [[Context Window Management]].
