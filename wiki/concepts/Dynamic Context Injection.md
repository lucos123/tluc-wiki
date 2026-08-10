---
title: "Dynamic Context Injection"
date: 2026-08-10
tags:
  - concept
  - context-engineering
  - harness-engineering
  - claude-code
source: "[[Extend Claude with skills]]"
---

# Dynamic Context Injection

**Dynamic Context Injection** is a prompt engineering feature in [[Claude Code]] skills where inline shell commands prefixed with `!` (such as `` !`git diff HEAD` `` or `` ```! bash ``` ``) are executed by the harness at render time, replacing the syntax with live stdout *before* the prompt reaches the LLM context window.

---

## Syntax & Usage

```markdown
## Active Uncommitted Edits

!`git diff HEAD`

## Environment Status

```!
npm run status --json
```
```

## Benefits

1. **Zero Model Hallucination**: Grounding decisions in live git state or environment diagnostic output rather than LLM assumptions.
2. **Context Freshness**: Guarantees up-to-the-second output dynamically evaluated on every skill invocation.

See [[Extend Claude with skills]] and [[Agent Skills Architecture]].
