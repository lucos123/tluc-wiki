---
title: "Ultracode Mode"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - effort-tuning
  - claude-code
source: "[[Orchestrate subagents at scale with dynamic workflows]]"
---

# Ultracode Mode

**Ultracode Mode** (`/effort ultracode` or `ultracode:` keyword) is an advanced execution configuration in [[Claude Code]] that pairs `xhigh` reasoning effort with automatic [[Dynamic Workflows]] script generation for substantive tasks.

---

## Activation Options

1. **Per-Prompt Keyword**: `ultracode: audit every API endpoint` (activates workflow script generation for a single turn).
2. **Session Effort Level**: `/effort ultracode` (locks session into `xhigh` effort and forces workflow planning for all substantive tasks).
3. **CLI Startup Flag**: `claude --effort ultracode`.

See [[Orchestrate subagents at scale with dynamic workflows]], [[Dynamic Workflows]], and [[Effort Level and Model Selection]].
