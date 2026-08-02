---
title: "Kimi K3 Model Guide"
date: 2026-08-01
tags:
  - source
  - ai-models
  - claude-code
  - moonshot-ai
source: "raw/articles/kimi/Kimi K3.md"
---

# Kimi K3 Model Guide

**Source File**: [[raw/articles/kimi/Kimi K3.md]]

Documentation for [[Kimi K3]], [[Moonshot AI]]'s 2.8-trillion parameter flagship open-source model designed for 1M-token long-horizon coding, knowledge work, and deep reasoning.

## Key Concepts

- **2.8-Trillion Scale Open Model**: The world's first open-source model in the 3-trillion parameter class. Built on Kimi Delta Attention (KDA), Attention Residuals (AttnRes), and [[Stable Latent MoE]] (16/896 active experts, 1.8% activation ratio). Provides 2.5x overall scaling efficiency over K2.
- **1M Context & Automatic Caching**: Features a 1M-token context window with automatic prefix caching. Caching triggers automatically for prefixes over 256 tokens with flat pay-as-you-go billing (no context-length penalties).
- **Reasoning Effort Control**: Always-on thinking model with a configurable `reasoning_effort` parameter (`low`, `high`, `max` [default]).
- **API Features & OpenAI Compatibility**: Fully compatible with OpenAI SDK (`base_url="https://api.moonshot.ai/v1"`). Supports:
  - **Structured Output**: `json_schema` with `strict: true`.
  - **Partial Mode**: `partial=True` on assistant messages to enforce specific output prefixes.
  - **Dynamic Tool Loading**: Declaring tools inside `system` messages without `content`.
  - **Vision & Video Input**: Base64 encoding or file upload via `ms://<file-id>`.
- **[[Claude Code]] Backend**: Positioned as a premier open-weights backend for long-horizon coding tools like Claude Code.

## Synthesis Notes

This source establishes `[[Kimi K3]]` as a major benchmark in the open-source model landscape. Its 2.8T scale and 1.8% activation ratio combine ultra-sparse MoE with linear attention (KDA), providing the raw model capabilities required to serve multi-agent graphs (`[[Graph Engineering]]`) and execution loops (`[[Loop Engineering]]`) cost-effectively.
