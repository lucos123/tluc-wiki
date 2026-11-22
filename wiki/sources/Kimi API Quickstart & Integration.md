---
title: "Kimi API Quickstart & Integration"
date: 2026-08-01
tags:
  - source
  - ai-models
  - moonshot-ai
source: "raw/articles/kimi/quickstart.md"
---

# Kimi API Quickstart & Integration

**Source File**: [raw/articles/kimi/quickstart.md](../../raw/articles/kimi/quickstart.md)

Integration guide for connecting applications and agent tools to [Moonshot AI](../entities/Moonshot%20AI.md)'s API endpoints.

## Key Concepts

- **OpenAI API Compatibility**: Kimi API adopts the OpenAI Chat Completions schema (`base_url="https://api.moonshot.ai/v1"`), enabling drop-in integration with existing SDKs, libraries, and agent CLI tools like [Claude Code](../entities/Claude%20Code.md).
- **Core Platform Capabilities**:
  - **Streaming**: Separate deltas returned for `reasoning_content` and final answer `content`.
  - **Multimodal Input**: Text, image, and video support. Recommends Base64 for small media and the Files API (`ms://<file-id>`) for large media or repeated references. Max resolution limits: 4K for images, 1080p for videos.
  - **Tool Calling & JSON Mode**: Supports function calling and strict `json_schema` enforcement.
  - **Thinking Models**: Native chain-of-thought reasoning across K3, K2.7, and K2.6 models.

## Synthesis Notes

By adopting complete OpenAI API compatibility, [Moonshot AI](../entities/Moonshot%20AI.md) enables seamless integration into modern agent harnesses ([Harness Engineering](../concepts/Harness%20Engineering.md)). Developers can switch agent backends to [Kimi K3](../entities/Kimi%20K3.md) or [Kimi K2.7 Code](../entities/Kimi%20K2.7%20Code.md) simply by configuring `base_url` and `api_key`.
