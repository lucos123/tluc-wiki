---
title: "Cost Optimization"
date: 2026-08-10
tags:
  - concept
  - cost-optimization
  - harness-engineering
  - claude-code
source: "[[Manage costs effectively]]"
---

# Cost Optimization

**Cost Optimization** encompasses the active engineering techniques used to minimize token consumption in [[Claude Code]] without sacrificing task completion quality or model reasoning precision.

---

## High-Impact Optimization Tactics

1. **Context Pruning (`/clear`, `/compact`)**: Clearing sessions between unrelated tasks prevents stale context from compounding token costs across every subsequent turn.
2. **Metacode Offloading**: Keeping `CLAUDE.md` under 200 lines by moving specialized workflow instructions into on-demand [[Agent Skills Architecture|Agent Skills]].
3. **Deterministic PreToolUse Filtering**: Using pre-execution hooks to filter 10,000-line test runner outputs down to failure snippets before passing to LLM context.
4. **Model × Effort Balancing**: Pairing Sonnet for implementation with Opus for high-level architecture, and tuning `/effort` or `MAX_THINKING_TOKENS`.

See [[Manage costs effectively]], [[Token Economics]], and [[Context Window Management]].
