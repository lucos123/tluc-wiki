---
title: "Kimi Thinking Models & Preserved Thinking Guide"
date: 2026-08-01
tags:
  - source
  - ai-models
  - moonshot-ai
source: "raw/articles/kimi/model-capabilities/thinking-models.md"
---

# Kimi Thinking Models & Preserved Thinking Guide

**Source File**: [raw/articles/kimi/model-capabilities/thinking-models.md](../../raw/articles/kimi/model-capabilities/thinking-models.md)

Deep-dive into reasoning tokens, `reasoning_content` extraction, and [Preserved Thinking](../concepts/Preserved%20Thinking.md) across the Kimi model family.

## Key Concepts

- **Thinking Model Matrix**:
  - `kimi-k3`: Always-on reasoning (`reasoning_effort`: `low`/`high`/`max`), Preserved Thinking always on.
  - `kimi-k2.7-code` & HighSpeed: Always-on thinking (`thinking.type="enabled"`), Preserved Thinking always on (`thinking.keep="all"`).
  - `kimi-k2.6`: Optional thinking (`thinking.type`), configurable Preserved Thinking (`thinking.keep`: `null` vs `"all"`).
  - `kimi-k2.5`: Optional thinking, Preserved Thinking **not supported**.
- **Preserved Thinking (`thinking.keep="all"`)**: Passing previous turns' `reasoning_content` back in `messages` allows models to preserve and continue complex chains of thought across multi-step agent interactions.
- **OpenAI SDK Reflection Pattern**: SDK types do not expose `reasoning_content` directly. Clients must check `hasattr(obj, "reasoning_content")` and retrieve via `getattr(obj, "reasoning_content")`.
- **Multi-Step Tool Calling Rules**: Must allocate `max_tokens >= 16000`, use fixed default temperatures, stream output, and retain `reasoning_content` in assistant messages.

## Synthesis Notes

[Preserved Thinking](../concepts/Preserved%20Thinking.md) is a major advancement for long-horizon agentic workflows ([Loop Engineering](../concepts/Loop%20Engineering.md)). By preserving intermediate thinking tokens across multi-turn tool loops, agents avoid re-reasoning from scratch, preserving context and coherence during complex multi-step tasks.
