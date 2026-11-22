---
title: "Manage costs effectively"
date: 2026-08-10
tags:
  - source
  - costs
  - token-economics
  - cost-optimization
  - claude-code
source: "raw/articles/claude-code/costs-models-checkpoints/costs.md"
url: "https://code.claude.com/docs/en/costs.md"
---

# Manage costs effectively

**URL**: https://code.claude.com/docs/en/costs.md  
**Source File**: [raw/articles/claude-code/costs-models-checkpoints/costs.md](../../raw/articles/claude-code/costs-models-checkpoints/costs.md)  

---

## Executive Summary

This official Anthropic guide details how to track, govern, and optimize token costs in [Claude Code](../entities/Claude%20Code.md).

Enterprise deployment averages ~$13 per developer per active day ($150–$250/month), with 90% of developers remaining below $30/day. Token consumption is governed by context size, model selection, reasoning effort, prompt caching, and subagent/MCP server execution.

---

## Cost Tracking & Attribution Metrics

### 1. The `/usage` Command
- Displays total dollar spend, API duration, wall duration, lines added/removed, and model breakdown (input, output, cache read, cache write).
- Provides percentage attribution by **Skill**, **Subagent**, **Plugin**, and **MCP Server**.

### 2. Organization Spend Governance
- **Claude for Teams / Enterprise**: Per-seat allowances (5-hour rolling + weekly window). Org analytics spend report & CSV exports.
- **Claude Console (API)**: Workspace spend caps, token rate limits (TPM/RPM per-user allocation table).
- **Cloud Providers**: Metered via OpenTelemetry exports, Claude Apps Gateway, or LLM Gateways (LiteLLM).

---

## High-Impact Token Reduction Strategies

```
┌─────────────────────────────────────────────────────────────┐
│                 Token Reduction Strategies                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Context Pruning: Run /clear between tasks; /compact      │
│ 2. CLAUDE.md Offloading: Move workflows to Agent Skills     │
│ 3. Hook Preprocessing: PreToolUse hooks filter 10K-line logs│
│ 4. Model & Effort Matching: Sonnet for code, Opus for plan  │
│ 5. Extended Thinking Tuning: Use /effort or MAX_THINKING     │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Knowledge Nodes

- **Concepts**:
  - [Token Economics](../concepts/Token%20Economics.md)
  - [Cost Optimization](../concepts/Cost%20Optimization.md)
  - [Context Window Management](../concepts/Context%20Window%20Management.md)
  - [Effort Level and Model Selection](../concepts/Effort%20Level%20and%20Model%20Selection.md)
  - [System Prompt Caching Optimization](../concepts/System%20Prompt%20Caching%20Optimization.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
