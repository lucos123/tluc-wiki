---
title: "Explore the context window"
date: 2026-08-10
tags:
  - source
  - context-engineering
  - cost-optimization
  - claude-code
source: "[[raw/articles/claude-code/context-memory-rules/context-window.md]]"
url: "https://code.claude.com/docs/en/context-window.md"
---

# Explore the context window

**URL**: https://code.claude.com/docs/en/context-window.md  
**Source File**: [[raw/articles/claude-code/context-memory-rules/context-window.md]]  

---

## Executive Summary

This interactive guide from Anthropic details how [[Claude Code]]'s 200,000 token context window fills up during a live session, what loads at startup, how file reads and hooks consume tokens, and how subagents protect main session context.

---

## Startup Context Token Allocation Breakdown

```
[System Prompt (4,200t)] ──> [Auto Memory (680t)] ──> [Env Info (280t)]
  ──> [MCP Tool Names (120t)] ──> [Skill Summaries (450t)] ──> [~/.claude/CLAUDE.md (320t)]
        ──> [Project CLAUDE.md (1,800t)]
              =======================================================
              Total Baseline Startup Context: ~8,450 - 9,500 tokens
```

### Key Context Consumption Factors

1. **File Reads Dominate**: Single file reads (`Read src/api/auth.ts`) consume 2,000–5,000+ tokens per turn. Reading multiple files during exploration quickly fills the 200K limit.
2. **Path-Scoped Rules (`.claude/rules/*.md`)**: Load on-demand only when matching glob files are read (e.g. `api-conventions.md` adding 380 tokens when reading `src/api/**`).
3. **Hook Output Ingestion**: PostToolUse hook output injected via `additionalContext` enters context directly, whereas plain exit 0 stdout is written only to debug logs.
4. **Subagent Context Isolation**: Delegating exploration or heavy research to a subagent executes 15,000+ tokens of file reading inside a **fresh, isolated 200K context window**, returning only a ~350 token summary to the main window.

---

## Related Knowledge Nodes

- **Concepts**: [[Context Window Management]], [[Subagent Context Isolation]], [[Path-Scoped Rules]], [[Progressive Disclosure]], [[Persistent Instruction File]].
- **Entities**: [[Claude Code]], [[Anthropic]].
