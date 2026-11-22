---
title: "Ultracode Mode"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - effort-tuning
  - claude-code
source: "wiki/sources/Orchestrate subagents at scale with dynamic workflows.md"
---

# Ultracode Mode

**Ultracode Mode** (`/effort ultracode` or `ultracode:` keyword) is an advanced execution configuration in [Claude Code](../entities/Claude%20Code.md) that pairs `xhigh` reasoning effort with automatic [Dynamic Workflows](Dynamic%20Workflows.md) script generation for substantive tasks.

---

## Activation Options

1. **Per-Prompt Keyword**: `ultracode: audit every API endpoint` (activates workflow script generation for a single turn).
2. **Session Effort Level**: `/effort ultracode` (locks session into `xhigh` effort and forces workflow planning for all substantive tasks).
3. **CLI Startup Flag**: `claude --effort ultracode`.

See [Orchestrate subagents at scale with dynamic workflows](../sources/Orchestrate%20subagents%20at%20scale%20with%20dynamic%20workflows.md), [Dynamic Workflows](Dynamic%20Workflows.md), and [Effort Level and Model Selection](Effort%20Level%20and%20Model%20Selection.md).
