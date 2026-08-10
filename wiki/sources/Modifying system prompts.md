---
title: "Modifying system prompts"
date: 2026-08-10
tags:
  - source
  - system-prompts
  - context-engineering
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/context-memory-rules/modifying-system-prompts.md]]"
url: "https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts.md"
---

# Modifying system prompts

**URL**: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts.md  
**Source File**: [[raw/articles/claude-code/context-memory-rules/modifying-system-prompts.md]]  

---

## Executive Summary

This guide explains how to customize and optimize system prompts in [[Claude Code]] and the Agent SDK. It details the 3 starting points (`minimal`, `claude_code` preset, custom string), 4 customization methods (`CLAUDE.md`, output styles, `append`, custom prompt), and how `excludeDynamicSections` maximizes prompt cache hits across fleet sessions.

---

## 4 Customization Approaches Compared

| Method | Where Written | Scope | System Prompt Cache Shared Across Machines? |
| --- | --- | --- | --- |
| **`CLAUDE.md`** | Markdown files in project or `~/.claude/` | Project or User | Yes (injected as conversation context, not system prompt) |
| **Output Styles** | `.claude/output-styles/` markdown | Project or User | Depends on `keep-coding-instructions` |
| **Preset `append`** | SDK options `systemPrompt.append` | Code runtime | Yes when `excludeDynamicSections: true` |
| **Custom String** | SDK options `systemPrompt` (string) | Code runtime | Yes (if string is identical) |

---

## Prompt Caching Optimization (`excludeDynamicSections`)

By default, the `claude_code` preset embeds dynamic per-session context (working directory, git branch, OS version) inside the system prompt. This causes cache misses across different machines or directories.

Setting `excludeDynamicSections: true` moves working directory and environment info into the *first user message*, leaving the system prompt completely static and enabling **100% prompt cache hit rates across distributed fleet agents**.

---

## Related Knowledge Nodes

- **Concepts**: [[System Prompt Caching Optimization]], [[Agent SDK Architecture]], [[Persistent Instruction File]], [[Context Window Management]].
- **Entities**: [[Claude Code]], [[Anthropic]].
