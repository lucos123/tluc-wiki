---
title: "Keep Claude working toward a goal"
date: 2026-08-10
tags:
  - source
  - goal
  - loop-engineering
  - harness-engineering
  - claude-code
source: "raw/articles/claude-code/agent-architecture-subagents-workflows/goal.md"
url: "https://code.claude.com/docs/en/goal.md"
---

# Keep Claude working toward a goal

**URL**: https://code.claude.com/docs/en/goal.md  
**Source File**: [raw/articles/claude-code/agent-architecture-subagents-workflows/goal.md](../../raw/articles/claude-code/agent-architecture-subagents-workflows/goal.md)  

---

## Executive Summary

This official Anthropic guide details the `/goal` command in [Claude Code](../entities/Claude%20Code.md).

`/goal` establishes an autonomous, multi-turn session loop where a fast background evaluator model (Haiku) inspects the conversation transcript after each turn to check whether a specified completion condition has been empirically satisfied.

---

## Session Execution Loop Comparison

| Mechanism | Next Turn Trigger | Termination Criteria | Primary Use Case |
| --- | --- | --- | --- |
| **`/goal`** | Immediate after turn finishes | Model evaluator confirms condition met | Goal-driven multi-file refactoring or test fixing |
| **`/loop`** | Time interval elapses (e.g. 5m) | User stop or explicit completion | Periodic monitoring or background polling |
| **Stop Hook** | Immediate after turn finishes | Deterministic script exit code / custom prompt | CI integration or custom team verification gates |

---

## Operational Commands & Usage

```bash
# Set an active goal loop
/goal all tests in test/auth pass and git status is clean

# Check active goal status & evaluator reasons
/goal

# Clear active goal
/goal clear # or /goal cancel

# Non-interactive CLI goal execution
claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"
```

---

## Related Knowledge Nodes

- **Concepts**:
  - [Goal-Driven Loop](../concepts/Goal-Driven%20Loop.md)
  - [Loop Engineering](../concepts/Loop%20Engineering.md)
  - [Verification Loop](../concepts/Verification%20Loop.md)
  - [Second Opinion Pattern](../concepts/Second%20Opinion%20Pattern.md)
  - [Control-Loop Engineering](../concepts/Control-Loop%20Engineering.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
