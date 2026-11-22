---
title: "GPT-5.6 Terra Model API Reference"
date: 2026-08-01
tags:
  - source
  - ai-models
  - openai
source: "raw/articles/openai/model/gpt-5-6-terra-model-api-reference.md"
---

# GPT-5.6 Terra Model API Reference

**Source File**: [raw/articles/openai/model/gpt-5-6-terra-model-api-reference.md](../../raw/articles/openai/model/gpt-5-6-terra-model-api-reference.md)

Official API reference for `gpt-5.6-terra`, [OpenAI](../entities/OpenAI.md)'s balanced model for everyday workloads.

## Key Specifications

- **Role**: Everyday workhorse model balancing high intelligence and cost, competitive with GPT-5.5 at ~1/16th total cost.
- **Context & Output**: 1,050,000 token context window; 128,000 max output tokens. Knowledge cutoff: Feb 16, 2026.
- **Pricing**:
  - Uncached input: $2.00 / 1M tokens.
  - Cached input: $0.20 / 1M tokens.
  - Output: $12.00 / 1M tokens.
  - Long Context Multiplier: Prompts with >272K input tokens are billed at 2x input and 1.5x output.
- **Modalities**: Text & Image input; Text output.

## Synthesis Notes

[GPT-5.6 Terra](../entities/GPT-5.6%20Terra.md) serves as the primary replacement for legacy `gpt-5.4` and `gpt-5.5` models in standard developer automation workflows, offering high reasoning capability at a 60% discount over `gpt-5.6-sol`.
