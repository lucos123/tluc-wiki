---
title: "Kimi K2.7 Code Guide"
date: 2026-08-01
tags:
  - source
  - ai-models
  - claude-code
  - moonshot-ai
source: "raw/kimi/Kimi K2.7 Code.md"
---

# Kimi K2.7 Code Guide

**Source File**: [[raw/kimi/Kimi K2.7 Code.md]]

Documentation for `[[Kimi K2.7 Code]]`, [[Moonshot AI]]'s dedicated long-horizon coding and agentic reasoning model.

## Key Concepts

- **Dedicated Coding Architecture**: Optimized for long-horizon coding and instruction compliance, yielding a 10% gain in agentic capabilities over K2.6 and reducing overthinking by 30%.
- **Context & HighSpeed Variant**: Provides a 256K context window. Includes `kimi-k2.7-code-highspeed`, generating 180–260 tokens/second for rapid developer feedback loops.
- **Thinking Mode & Enforced Hyperparameters**:
  - Always-on thinking mode (`thinking: {"type": "enabled"}`).
  - Fixed API hyperparameters enforced: `temperature=1.0`, `top_p=0.95`, `n=1`, `presence_penalty=0.0`, `frequency_penalty=0.0`.
  - Tool choice restricted to `"auto"` or `"none"`.
- **Multi-Turn Tooling Rules**: In multi-step tool calls, clients **must** retain `reasoning_content` in assistant messages within the context window to prevent API errors.
- **Multimodal Function Calling**: Demonstrates combining visual understanding (base64 video encoding) with function calling (`watch_video_clip`) and ffmpeg clipping for video-based agent loops.

## Synthesis Notes

`[[Kimi K2.7 Code]]` provides a targeted alternative to generalist models for agentic software engineering. Its HighSpeed variant (180–260 t/s) directly addresses developer latency bottlenecks in turn-based and goal-based loops (`[[Loop Engineering]]`), while its strict requirement to retain `reasoning_content` reflects Moonshot's approach to state preservation in multi-step tool calling.
