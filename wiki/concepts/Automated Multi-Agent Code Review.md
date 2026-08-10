---
title: "Automated Multi-Agent Code Review"
date: 2026-08-10
tags:
  - concept
  - verification
  - agentic-design
  - claude-code
source: "[[Code Review]]"
---

# Automated Multi-Agent Code Review

**Automated Multi-Agent Code Review** is a production verification architecture in [[Claude Code]] where a fleet of specialized subagents analyzes PR diffs in parallel against full codebase context, supported by an empirical verification step to eliminate false positives.

---

## Architectural Stages

```mermaid
graph TD
    PR["PR Trigger (@claude review / Git Push)"] --> FanOut["1. Multi-Agent Fan-Out"]
    FanOut --> LogicAgent["Logic Agent"]
    FanOut --> SecAgent["Security Agent"]
    FanOut --> RegrAgent["Regression Agent"]
    LogicAgent --> Verification["2. Verification & Falsification Step"]
    SecAgent --> Verification
    RegrAgent --> Verification
    Verification --> Dedupe["3. Deduplication & Severity Ranking"]
    Dedupe --> Output["4. Inline Annotations & Check Run JSON"]
```

## Key Benefits

1. **False Positive Suppression**: Findings are cross-checked against live codebase behavior before posting.
2. **Severity Calibration**: Issues are ranked into 🔴 Important, 🟡 Nit, and 🟣 Pre-existing categories.
3. **Local Terminal Alternative**: Available locally via the `/code-review` command.

See [[Code Review]], [[REVIEW.md Governance]], and [[Second Opinion Pattern]].
