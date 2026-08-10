---
title: "Prompt-Based Hooks"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - verification
  - claude-code
source: "[[Automate actions with hooks]]"
---

# Prompt-Based Hooks

**Prompt-Based Hooks** (`"type": "prompt"`) are non-deterministic lifecycle hooks in [[Claude Code]] that send event payloads and transcript context to a fast evaluation model (e.g. Haiku) to evaluate complex semantic conditions at turn boundaries.

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

See [[Automate actions with hooks]], [[Claude Code Hooks]], and [[Goal-Driven Loop]].
