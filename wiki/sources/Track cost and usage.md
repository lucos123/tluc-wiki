---
title: "Track cost and usage"
date: 2026-08-10
tags:
  - source
  - cost-tracking
  - agent-sdk
  - token-economics
  - claude-code
source: "[[raw/articles/claude-code/costs-models-checkpoints/cost-tracking.md]]"
url: "https://code.claude.com/docs/en/cost-tracking.md"
---

# Track cost and usage

**URL**: https://code.claude.com/docs/en/cost-tracking.md  
**Source File**: [[raw/articles/claude-code/costs-models-checkpoints/cost-tracking.md]]  

---

## Executive Summary

This official Anthropic guide details how to programmatically track token usage and estimate costs using the **Claude Agent SDK** (Python & TypeScript).

SDK cost tracking provides per-step token breakdowns on assistant messages, per-model breakdowns on result messages (`modelUsage`), and cumulative estimates (`total_cost_usd`), while highlighting critical accounting caveats like parallel tool message deduplication and subagent tree token aggregation.

---

## Subagent Cost Accounting Matrix

| Field | Subagent Accounting Scope |
| --- | --- |
| `usage` | **Top-level loop only**. Excludes subagent tokens. |
| `total_cost_usd` | **Entire agent tree**. Includes subagents + main loop. |
| `modelUsage` / `model_usage` | **Entire agent tree**. Includes subagents + main loop, broken down per model. |

---

## Parallel Tool Deduplication Rules

```typescript
// Parallel tool executions share identical message IDs and usage data.
// Deduplicate by msgId to avoid double-counting input/output tokens!
if (!seenIds.has(msgId)) {
  seenIds.add(msgId);
  totalInputTokens += message.message.usage.input_tokens;
  totalOutputTokens += message.message.usage.output_tokens;
}
```

---

## Related Knowledge Nodes

- **Concepts**: [[SDK Token Accounting]], [[Token Economics]], [[Cost Optimization]], [[Agent SDK Architecture]].
- **Entities**: [[Claude Code]], [[Anthropic]].
