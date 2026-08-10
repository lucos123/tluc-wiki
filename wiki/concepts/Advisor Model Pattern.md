---
title: "Advisor Model Pattern"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - model-selection
  - claude-code
source: "[[Escalate hard decisions with the advisor tool]]"
---

# Advisor Model Pattern

**Advisor Model Pattern** is a dual-model escalation architecture in [[Claude Code]] (`/advisor`) where a primary worker model (Sonnet) executes routine file edits and tool calls while dynamically delegating high-stakes architectural choices, debugging deadlocks, or pre-commit reviews to a stronger advisor model (Opus).

---

## Technical Features

1. **Model-Driven Escalation**: The primary model autonomously decides when to invoke the advisor tool based on task ambiguity or error recurrence.
2. **Cache-Safe Integration**: Enabling or disabling `/advisor` appends guidance without invalidating the main model's prompt cache.
3. **Capability Hierarchy Requirement**: Advisor models must be at least as capable as the main model (e.g. Haiku/Sonnet $\rightarrow$ Opus).

See [[Escalate hard decisions with the advisor tool]], [[Second Opinion Pattern]], and [[Effort Level and Model Selection]].
