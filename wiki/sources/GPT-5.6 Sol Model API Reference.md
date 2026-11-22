---
title: "GPT-5.6 Sol Model API Reference"
date: 2026-08-01
tags:
  - source
  - ai-models
  - openai
source: "raw/articles/openai/model/gpt-5-6-sol-model-api-reference.md"
---

# GPT-5.6 Sol Model API Reference

**Source File**: [raw/articles/openai/model/gpt-5-6-sol-model-api-reference.md](../../raw/articles/openai/model/gpt-5-6-sol-model-api-reference.md)

Official API reference for `gpt-5.6-sol` (alias `gpt-5.6`), [OpenAI](../entities/OpenAI.md)'s flagship model for complex professional work.

## Key Specifications

- **Role**: SOTA flagship model for complex coding, computer use, research, and cybersecurity.
- **Context & Output**: 1,050,000 token context window; 128,000 max output tokens. Knowledge cutoff: Feb 16, 2026.
- **Pricing**:
  - Uncached input: $5.00 / 1M tokens.
  - Cached input: $0.50 / 1M tokens (cache writes at 1.25x input rate).
  - Output: $30.00 / 1M tokens.
  - Long Context Multiplier: Prompts with >272K input tokens are billed at 2x input and 1.5x output.
- **Modalities**: Text & Image input; Text output.
- **Supported Tools via Responses API**: Web search, File search, Image generation, Code interpreter, Hosted shell, Apply patch, Skills, Computer use, MCP, Tool search.

## Synthesis Notes

`gpt-5.6-sol` represents OpenAI's top-tier frontier model. It integrates directly with [Codex](../entities/Codex.md) CLI and provides full support for [Responses API](../concepts/Responses%20API.md) native tools and multi-agent coordination ([Graph Engineering](../concepts/Graph%20Engineering.md)).
