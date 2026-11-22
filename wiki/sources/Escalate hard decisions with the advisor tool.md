---
title: "Escalate hard decisions with the advisor tool"
date: 2026-08-10
tags:
  - source
  - advisor
  - model-selection
  - harness-engineering
  - claude-code
source: "raw/articles/claude-code/costs-models-checkpoints/advisor.md"
url: "https://code.claude.com/docs/en/advisor.md"
---

# Escalate hard decisions with the advisor tool

**URL**: https://code.claude.com/docs/en/advisor.md  
**Source File**: [raw/articles/claude-code/costs-models-checkpoints/advisor.md](../../raw/articles/claude-code/costs-models-checkpoints/advisor.md)  

---

## Executive Summary

This official Anthropic guide details the **Advisor Tool** (`/advisor`) in [Claude Code](../entities/Claude%20Code.md).

The Advisor tool enables a primary execution model (e.g. Sonnet 4.6) to consult a stronger advisor model (e.g. Opus 5) at critical decision points, recurring error loops, or before task completion. The advisor inspects the full conversation history and returns guidance before execution continues.

---

## Model Pairing Hierarchy & Options

```
                    ┌────────────────────────────────┐
                    │ Primary Execution Session      │
                    │ (Sonnet 4.6 / Haiku 4.5)       │
                    └───────────────┬────────────────┘
                                    │ Escalates hard decisions
                                    ▼
                    ┌────────────────────────────────┐
                    │ Advisor Model                  │
                    │ (Opus 5 / Fable 5)             │
                    └────────────────────────────────┘
```

| Main Model | Accepted Advisor Models | Common Pairing Rationale |
| --- | --- | --- |
| **Sonnet 4.6** | Opus, Fable, Sonnet | Sonnet executes routine code; Opus supervises architecture. |
| **Haiku 4.5** | Opus, Fable, Sonnet | Lowest-cost main worker with strong Opus planning checks. |
| **Opus 4.6** | Opus 4.6+, Sonnet 5, Fable | High-stakes tasks requiring independent second-opinion checks. |

---

## Activation Commands

```bash
# Enable advisor via interactive CLI or command
/advisor opus

# Set via launch flag
claude --advisor opus

# Disable advisor
/advisor off
```

---

## Related Knowledge Nodes

- **Concepts**:
  - [Advisor Model Pattern](../concepts/Advisor%20Model%20Pattern.md)
  - [Second Opinion Pattern](../concepts/Second%20Opinion%20Pattern.md)
  - [Effort Level and Model Selection](../concepts/Effort%20Level%20and%20Model%20Selection.md)
  - [Cost Optimization](../concepts/Cost%20Optimization.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
