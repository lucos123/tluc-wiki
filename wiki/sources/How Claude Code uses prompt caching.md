---
title: "How Claude Code uses prompt caching"
date: 2026-08-10
tags:
  - source
  - prompt-caching
  - cost-optimization
  - token-economics
  - claude-code
source: "raw/articles/claude-code/costs-models-checkpoints/prompt-caching.md"
url: "https://code.claude.com/docs/en/prompt-caching.md"
---

# How Claude Code uses prompt caching

**URL**: https://code.claude.com/docs/en/prompt-caching.md  
**Source File**: [raw/articles/claude-code/costs-models-checkpoints/prompt-caching.md](../../raw/articles/claude-code/costs-models-checkpoints/prompt-caching.md)  

---

## Executive Summary

This official Anthropic guide explains how **Prompt Caching** operates automatically within [Claude Code](../entities/Claude%20Code.md) to maximize token efficiency and response speed.

Prompt caching reuses identical API request prefixes (System Prompt $\rightarrow$ Project Context $\rightarrow$ History), billing cache reads at ~10% of standard input rates (`cache_read_input_tokens`). Understanding prefix matching prevents unintended cache invalidations caused by mid-session configuration changes.

---

## Cache Invalidation vs. Preservation Matrix

```
       ┌─────────────────────────────────────────────────────────────┐
       │               Prompt Cache Layering Order                   │
       ├─────────────────────────────────────────────────────────────┤
       │ 1. System Prompt   (Tool definitions, system prompts)       │
       │ 2. Project Context (CLAUDE.md, auto memory, rules)          │
       │ 3. Conversation    (User & Assistant messages, tool results)│
       └─────────────────────────────────────────────────────────────┘
```

| Execution Action | Cache Impact | Technical Rationale |
| --- | --- | --- |
| **Model Switch (`/model`)** | ❌ Full Cache Bust | Cache is keyed server-side by model ID. |
| **Effort Change (`/effort`)** | ❌ Full Cache Bust | Cache is keyed server-side by effort level. |
| **Fast Mode (`/fast`)** | ❌ Full Cache Bust (1st turn) | Injects fast-mode request header into cache key. |
| **Full Tool Deny** | ❌ System Prompt Invalidation | Modifies tool definition block in system prompt layer. |
| **Code File Edit** | ✅ Cache-Safe | Appends `<system-reminder>` to conversation layer. |
| **Skill Invocation** | ✅ Cache-Safe | Appends skill text as user message in conversation layer. |
| **Session Rewind (`/rewind`)** | ✅ Cache-Safe | Truncates history back to an existing warm prefix. |
| **Mid-session `CLAUDE.md` Edit** | ✅ Cache-Safe (Deferred) | CLAUDE.md is held in memory; edits take effect next session. |

---

## Cache Lifetime (TTL)

- **Subscription Plans (Pro/Max/Team/Enterprise)**: 1-hour TTL enabled automatically.
- **API Key & Cloud Providers (Bedrock/Vertex/Foundry)**: 5-minute default TTL (enable 1-hour TTL via `ENABLE_PROMPT_CACHING_1H=1`).
- **TTL Override**: Force 5-minute TTL via `FORCE_PROMPT_CACHING_5M=1`.

---

## Related Knowledge Nodes

- **Concepts**:
  - [System Prompt Caching Optimization](../concepts/System%20Prompt%20Caching%20Optimization.md)
  - [Cache Invalidation Patterns](../concepts/Cache%20Invalidation%20Patterns.md)
  - [Token Economics](../concepts/Token%20Economics.md)
  - [Cost Optimization](../concepts/Cost%20Optimization.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
