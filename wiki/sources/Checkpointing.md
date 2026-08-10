---
title: "Checkpointing"
date: 2026-08-10
tags:
  - source
  - checkpointing
  - rewind
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/costs-models-checkpoints/checkpointing.md]]"
url: "https://code.claude.com/docs/en/checkpointing.md"
---

# Checkpointing

**URL**: https://code.claude.com/docs/en/checkpointing.md  
**Source File**: [[raw/articles/claude-code/costs-models-checkpoints/checkpointing.md]]  

---

## Executive Summary

This official Anthropic guide details **Session Checkpointing** in [[Claude Code]].

Checkpointing automatically captures code state before each user prompt (storing the 100 most recent snapshots for 30 days), allowing developers to undo bad edits, branch conversations, and rewind session state using `/rewind` or pressing `Esc` twice.

---

## Rewind Execution Topography

```
                       ┌───────────────────────────────┐
                       │    /rewind (Double Esc)       │
                       └───────────────┬───────────────┘
                                       │
      ┌──────────────────┬─────────────┴────────────┬──────────────────┐
      ▼                  ▼                          ▼                  ▼
 [ Restore Code &   [ Restore Code ]      [ Restore Conversation ] [ Summarize ]
   Conversation ]     Reverts file edits    Rewinds history,        Compresses context
 Reverts both code    only; keeps history   keeps code edits        to free tokens
 and conversation
```

---

## Tracking Scope & Boundaries

- **Tracked**: Direct file modifications executed by Claude Code editing tools (`Edit`, `Write`).
- **Untracked (Bypassed)**: Shell modifications via `Bash` (`rm`, `mv`, `cp`), external editor edits, background subagents, and symlinks/hard links.

---

## Related Knowledge Nodes

- **Concepts**: [[Session Checkpoints]], [[Context Window Management]], [[Harness Engineering]], [[Cache Invalidation Patterns]].
- **Entities**: [[Claude Code]], [[Anthropic]].
