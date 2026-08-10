---
title: "Session Checkpoints"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - state-management
  - claude-code
source: "[[Checkpointing]]"
---

# Session Checkpoints

**Session Checkpoints** is an automatic state management mechanism in [[Claude Code]] that captures file snapshots before every user prompt (retaining up to 100 recent checkpoints per session) to enable instant code and conversation rewinding (`/rewind`).

---

## Capabilities & Workflows

1. **Selective State Restoration**: Restores code edits only, conversation history only, or both simultaneously.
2. **Context Summarization**: Compresses transcript history forward or backward from any selected checkpoint to recover context window budget without losing file changes.
3. **Cache Preservation**: Rewinding to an earlier prompt restores a warm, pre-existing prompt cache prefix.

See [[Checkpointing]], [[Context Window Management]], and [[Harness Engineering]].
