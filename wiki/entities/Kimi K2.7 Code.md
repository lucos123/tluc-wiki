---
title: Kimi K2.7 Code
date: 2026-08-01
tags:
  - entity
  - product
  - ai-models
---

# Kimi K2.7 Code

`kimi-k2.7-code` is a dedicated long-horizon coding and agentic model developed by [Moonshot AI](Moonshot%20AI.md).

## Key Features

- **Long-Horizon Coding & Reduced Overthinking**: Delivers a 10% performance gain in agentic benchmark tasks over K2.6 while reducing overthinking tendencies by 30%.
- **Context & HighSpeed Variant**: Offers a 256K-token context window. Includes `kimi-k2.7-code-highspeed`, generating 180–260 tokens/second for low-latency interactive developer workflows.
- **Always-on Thinking & Strict Parameters**: Runs with mandatory thinking mode (`thinking: {"type": "enabled"}`). Enforces fixed API parameters (`temperature=1.0`, `top_p=0.95`, `n=1`) and requires `reasoning_content` retention in multi-turn tool calling.
- **Multimodal Tool Use**: Supports joint vision understanding (text, image, video) and function calling.

See [Kimi K2.7 Code Guide](../sources/Kimi%20K2.7%20Code%20Guide.md).
