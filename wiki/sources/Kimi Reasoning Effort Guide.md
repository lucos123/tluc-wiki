---
title: "Kimi Reasoning Effort Guide"
date: 2026-08-01
tags:
  - source
  - ai-models
  - moonshot-ai
source: "raw/kimi/model-capabilities/Reasoning Effort.md"
---

# Kimi Reasoning Effort Guide

**Source File**: [[raw/kimi/model-capabilities/Reasoning Effort.md]]

Documentation for configuring `[[Reasoning Effort]]` in [[Kimi K3]] models.

## Key Concepts

- **Top-Level Request Parameter**: `kimi-k3` uses a top-level `reasoning_effort` parameter supporting `"low"`, `"high"`, and `"max"` (default `"max"`).
- **Migration from K2.x**: Replaces the nested `thinking` block from K2.x (`thinking.type`, `thinking.keep`). Passing `thinking` to K3 returns an API error.
- **Context & Tool Calling Preservation**: Multi-turn conversations and function calls require returning the complete assistant message (including `reasoning_content` and `tool_calls`) back into `messages` as-is.

## Synthesis Notes

`[[Reasoning Effort]]` gives developers programmatic control over inference latency and token spend in reasoning models. It integrates directly with `[[Effort Level and Model Selection]]` principles.
