---
title: "Keep Claude working toward a goal"
date: 2026-08-10
tags:
  - source
  - goal
  - loop-engineering
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/agent-architecture-subagents-workflows/goal.md]]"
url: "https://code.claude.com/docs/en/goal.md"
---

# Keep Claude working toward a goal

**URL**: https://code.claude.com/docs/en/goal.md  
**Source File**: [[raw/articles/claude-code/agent-architecture-subagents-workflows/goal.md]]  

---

## Executive Summary

This official Anthropic guide details the `/goal` command in [[Claude Code]].

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

- **Concepts**: [[Goal-Driven Loop]], [[Loop Engineering]], [[Verification Loop]], [[Second Opinion Pattern]], [[Control-Loop Engineering]].
- **Entities**: [[Claude Code]], [[Anthropic]].
