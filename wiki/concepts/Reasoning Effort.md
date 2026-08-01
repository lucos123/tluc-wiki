---
title: Reasoning Effort
date: 2026-08-01
tags:
  - concept
  - ai-models
  - cost-optimization
---

# Reasoning Effort

**Reasoning Effort** is a top-level model control parameter used in reasoning LLMs like [[Kimi K3]] to dynamically adjust the depth, token budget, and latency of internal chain-of-thought processing before producing a final answer.

## Levels of Effort

- **`low`**: Reduces internal reasoning steps to minimize response latency and token spend. Ideal for simple queries, straightforward code edits, or high-throughput batch steps.
- **`high`**: Allocates significant reasoning budget for moderate-to-complex analytical or algorithmic tasks.
- **`max`** *(Default)*: Unlocks maximum reasoning budget for hard mathematical proofs, complex multi-step refactoring, and high-difficulty agentic planning.

## Integration with [[Effort Level and Model Selection]]

Reasoning Effort allows developers to implement 2D optimization (Model Choice $\times$ Effort Level):
- Fast, low-effort runs for routine checks inside `[[Verification Loop]]`s.
- Max-effort runs for initial planning and root-cause debugging.

See [[Kimi Reasoning Effort Guide]] and [[Effort Level and Model Selection]].
