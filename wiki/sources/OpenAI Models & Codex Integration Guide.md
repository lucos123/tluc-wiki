---
title: "OpenAI Models & Codex Integration Guide"
date: 2026-08-01
tags:
  - source
  - ai-models
  - codex
  - openai
source: "raw/articles/openai/model/models.md"
---

# OpenAI Models & Codex Integration Guide

**Source File**: [[raw/articles/openai/model/models.md]]

Documentation for selecting and configuring [[OpenAI]] models within [[Codex]] CLI, IDE extensions, and desktop applications.

## Key Concepts

- **Model Selection in Codex**:
  - Launch CLI flag: `codex -m gpt-5.6-sol` or `codex exec -m gpt-5.6-terra "task"`.
  - Global configuration: `config.toml` setting `model = "gpt-5.6"`.
- **Reasoning Effort Tiers**:
  - `low` / `light`: Fast, well-scoped tasks.
  - `medium`: Default balance of speed and planning depth.
  - `high` / `xhigh`: Complex multi-step analysis and trade-off evaluation.
  - `max`: Single-agent reasoning time extension for the hardest tasks.
  - `ultra`: Multi-agent parallel subagent execution (4 subagents by default, up to 16).
- **Specialized Research Model**:
  - `gpt-5.3-codex-spark`: Text-only real-time research model (>1,000 t/s) available to Pro subscribers for near-instant coding loops.
- **Deprecation Schedule**:
  - `gpt-5.4` and `gpt-5.4-mini` retire from Codex ChatGPT sign-in on **August 31, 2026**. (Migrate configs to `gpt-5.6-terra` and `gpt-5.6-luna`).
  - Chat Completions API support in Codex CLI is deprecated in favor of `[[Responses API]]`.

## Synthesis Notes

This guide illustrates how `[[Codex]]` harnesses `[[GPT-5.6]]` models. The inclusion of `ultra` mode (spawning parallel subagents) bridges single-agent harness execution with multi-agent `[[Graph Engineering]]`.
