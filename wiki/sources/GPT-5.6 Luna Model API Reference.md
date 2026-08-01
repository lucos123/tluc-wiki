---
title: "GPT-5.6 Luna Model API Reference"
date: 2026-08-01
tags:
  - source
  - ai-models
  - openai
source: "raw/openai/model/GPT-5.6 Luna Model  OpenAI API.md"
---

# GPT-5.6 Luna Model API Reference

**Source File**: [[raw/openai/model/GPT-5.6 Luna Model  OpenAI API.md]]

Official API reference for `gpt-5.6-luna`, [[OpenAI]]'s fast, cost-sensitive model tier.

## Key Specifications

- **Role**: High-volume, repeatable tasks (extraction, classification, transformation, structured summaries) corresponding to the nano model tier.
- **Context & Output**: 1,050,000 token context window; 128,000 max output tokens. Knowledge cutoff: Feb 16, 2026.
- **Pricing**:
  - Uncached input: $0.20 / 1M tokens.
  - Cached input: $0.02 / 1M tokens.
  - Output: $1.20 / 1M tokens.
  - Long Context Multiplier: Prompts with >272K input tokens billed at 2x input and 1.5x output.
- **Modalities**: Text & Image input; Text output.

## Synthesis Notes

`[[GPT-5.6 Luna]]` is designed for massive parallelization in agent subagent swarms (`[[Graph Engineering]]`). At $0.20 / $1.20 per 1M tokens, it enables cheap background filtering and structured data extraction.
