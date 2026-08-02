---
title: "Quickstart"
source: "https://platform.kimi.ai/docs/overview"
author:
published:
created: 2026-08-01
description: "Create an API Key and complete your first Kimi API call."
tags:
  - "clippings"
---
Kimi API lets you interact with Kimi models and is compatible with the OpenAI API format. Prepare an API Key, choose a model, and configure `base_url` to make requests through the HTTP API, Python SDK, or Node.js SDK.

[Kimi K3](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart) is now officially available — Kimi’s most capable model to date, with a 1M-token context window and native visual understanding. It is well suited for programming agent scenarios such as [Claude Code](https://platform.kimi.ai/docs/guide/claude-code-kimi), as well as knowledge work and deep reasoning.

## Get started

## Explore more features

## [Streaming output](https://platform.kimi.ai/docs/api/chat)

Enable `stream` to receive tokens as they are generated. Useful for chat, code generation, and long-form text output.

## [Multi-turn chat](https://platform.kimi.ai/docs/guide/engage-in-multi-turn-conversations-using-kimi-api)

Maintain a `messages` list to preserve context history, letting the model remember the conversation.

## [Multimodal input](https://platform.kimi.ai/docs/guide/use-kimi-vision-model)

Kimi K3, Kimi K2.7 Code, and Kimi K2.6 all support text, image, and video input.

## [Tool calls](https://platform.kimi.ai/docs/guide/use-kimi-api-to-complete-tool-calls)

Let the model call external functions or APIs for Agent tasks, web search, and complex workflows.

## [JSON Mode](https://platform.kimi.ai/docs/guide/use-json-mode-feature-of-kimi-api)

Force the model to output valid JSON for structured data extraction and downstream integration.

## [Thinking models](https://platform.kimi.ai/docs/guide/use-thinking-models)

Use reasoning capabilities for complex tasks, multi-step tool use, and Agent workflows.

### Streaming output

```json
{
  "model": "kimi-k3",
  "messages": [
    {
      "role": "user",
      "content": "Please explain what recursion is and give a Python example."
    }
  ],
  "stream": true
}
```

### Multimodal input

```json
{
  "model": "kimi-k3",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,..."
          }
        },
        {
          "type": "text",
          "text": "Please describe this image."
        }
      ]
    }
  ]
}
```

For larger videos, or images and videos that need to be referenced multiple times, we recommend using file uploads. Images should be no larger than 4K resolution, and videos should be no larger than 1080p.

## Related resources

## [Kimi K3 model](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)

View Kimi K3 capabilities, calling examples, and best practices.

## [Kimi K2.7 Code model](https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart)

View Kimi K2.7 Code capabilities, calling examples, and best practices.

## [Kimi K2.6 model](https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart)

View Kimi K2.6 capabilities, image/video understanding examples, and tool calling guidance.

## [Model list](https://platform.kimi.ai/docs/models)

View currently available model names and descriptions.

## [Join the Kimi Developer Community](https://platform.kimi.ai/docs/api/join-the-community)

Ask questions, share feedback, and showcase what you are building with Kimi.