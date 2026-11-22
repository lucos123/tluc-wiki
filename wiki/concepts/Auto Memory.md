---
title: "Auto Memory"
date: 2026-08-10
tags:
  - concept
  - memory
  - context-engineering
  - claude-code
source: "wiki/sources/How Claude remembers your project.md"
---

# Auto Memory

**Auto Memory** is the automated persistent memory mechanism in [Claude Code](../entities/Claude%20Code.md) where the model writes and updates its own notes based on developer corrections, debugging discoveries, and build quirks.

---

## Core Characteristics

1. **Model-Authored**: Unlike [Persistent Instruction File](Persistent%20Instruction%20File.md) (`CLAUDE.md`), Auto Memory is written autonomously by Claude during session interactions.
2. **Repository Scope**: Auto Memory notes are scoped per repository and shared across Git worktrees.
3. **Session Loading**: The first 200 lines (or 25 KB) of Auto Memory are automatically injected into context at session startup.
4. **Subagent Memory**: Custom subagents can also maintain independent Auto Memory files to preserve domain-specific learnings across runs.

See [How Claude remembers your project](../sources/How%20Claude%20remembers%20your%20project.md) and [Persistent Instruction File](Persistent%20Instruction%20File.md).
