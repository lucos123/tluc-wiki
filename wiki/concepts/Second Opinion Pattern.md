---
title: "Second Opinion Pattern"
date: 2026-08-02
tags:
  - concept
  - agentic-design
  - verification
  - harness-engineering
source: "wiki/sources/Anthropic Just Fixed Graph Engineering's Greatest Flaw.md"
---

# Second Opinion Pattern

The **Second Opinion Pattern** is an agentic verification design pattern where an agent's work is reviewed by a completely separate, fresh-context model instance rather than the worker agent that generated the code or artifact.

First detailed in [Anthropic Just Fixed Graph Engineering's Greatest Flaw](../sources/Anthropic%20Just%20Fixed%20Graph%20Engineering%27s%20Greatest%20Flaw.md) by [AI LABS](../entities/AI%20LABS.md).

---

## The Core Problem: Worker Self-Review Bias

When an AI agent reviews its own output within the same conversation window, it evaluates its work using the exact same context, reasoning traces, and assumptions that created the code. This causes:
1. **Inherited Hallucinations**: The worker agent validates its own flawed logic.
2. **Context Blindness**: The worker misses edge cases obscured by its prior context.

---

## Mechanics & Execution Strategy

1. **Fresh Session Spawning**: Launch a separate background session (e.g. via `claude -p` or a dedicated subagent invocation) with zero prior chat context.
2. **Model Override for Judges**: Run the reviewer session on a higher-intelligence model (e.g. Opus over Haiku). Cheap models generate false positives by misinterpreting intentional design choices as bugs.
3. **Unbiased Code Review**: The fresh reviewer receives only the original specification and the generated code, evaluating it objectively.
4. **Report Fan-In**: Findings return to the main orchestration loop for remediation.

---

## Relationship to Other Patterns

- **[Verification Loop](Verification%20Loop.md)**: Serves as the highest-tier verification gate (Standalone or Subagent review).
- **[Graph Engineering](Graph%20Engineering.md)**: Essential for node verification in fan-out DAGs.
- **[Harness Engineering](Harness%20Engineering.md)**: Implemented via harness CLI flags (`-p`) or subagent execution primitives.
