---
title: "Prompt-Based Hooks"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - verification
  - claude-code
source: "wiki/sources/Automate actions with hooks.md"
---

# Prompt-Based Hooks

**Prompt-Based Hooks** (`"type": "prompt"`) are non-deterministic lifecycle hooks in [Claude Code](../entities/Claude%20Code.md) that send event payloads and transcript context to a fast evaluation model (e.g. Haiku) to evaluate complex semantic conditions at turn boundaries.

---

## Evaluation Workflow

```json
{
  "type": "prompt",
  "prompt": "Verify if the proposed git commit message adheres to Conventional Commits standards."
}
```

- Fires at lifecycle boundaries such as `Stop` or `PreToolUse`.
- Returns model evaluation reasons directly to the primary session.
- Forms the underlying engine powering the `/goal` command evaluator.

See [Automate actions with hooks](../sources/Automate%20actions%20with%20hooks.md), [Claude Code Hooks](../sources/Claude%20Code%20Hooks.md), and [Goal-Driven Loop](Goal-Driven%20Loop.md).
