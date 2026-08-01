---
title: "Reasoning Effort"
source: "https://platform.kimi.ai/docs/guide/use-reasoning-effort"
author:
published:
created: 2026-08-01
description: "Kimi K3 is our flagship model for long-horizon coding and end-to-end knowledge work, with a 1M-token context window and industry-leading intelligence. The Kimi API Platform provides K3, K2.7 Code, K2.6 and other large language model APIs, supporting long context, multimodal understanding, and Tool Calling."
tags:
  - "clippings"
---
Kimi K3 always reasons and configures **reasoning effort** with the top-level `reasoning_effort` request field. It supports `"low"`, `"high"`, and `"max"`, with `"max"` as the default.

## Set the reasoning effort

Set `reasoning_effort` at the top level of the Chat Completions request:

```json
{
  "model": "kimi-k3",
  "messages": [{"role": "user", "content": "Derive the general formula for this sequence: 1, 4, 9, 25, 64, ..."}],
  "reasoning_effort": "high"
}
```

When migrating from K2.x to K3, remove the K2.x `thinking` configuration and use top-level `reasoning_effort` as needed.

- curl
- python

```shellscript
$ curl https://api.moonshot.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $MOONSHOT_API_KEY" \
    -d '{
        "model": "kimi-k3",
        "messages": [
            {
                "role": "user",
                "content": "Derive the general formula for this sequence: 1, 4, 9, 25, 64, ..."
            }
        ],
        "reasoning_effort": "high"
    }'
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

completion = client.chat.completions.create(
    model="kimi-k3",
    messages=[
        {"role": "user", "content": "Derive the general formula for this sequence: 1, 4, 9, 25, 64, ..."},
    ],
    reasoning_effort="high",
)

message = completion.choices[0].message
if hasattr(message, "reasoning_content"):
    print(getattr(message, "reasoning_content"))
print(message.content)
```

## Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `reasoning_effort` | string | No | K3’s top-level reasoning-effort field; supports `"low"`, `"high"`, and `"max"`, with `"max"` as the default. |

For multi-turn conversations and tool calls, K3 requires the complete assistant message returned by the API to be passed back to `messages` as-is, including `reasoning_content` and `tool_calls`.

## Related reading

- [Kimi K3 API Tool Calling Best Practices](https://platform.kimi.ai/docs/guide/kimi-k3-tool-calling-best-practice): reasoning-effort configuration guidance for tool-calling scenarios
- [Thinking Mode](https://platform.kimi.ai/docs/guide/use-thinking-models): per-model thinking behavior and Preserved Thinking
- [Model Parameter Reference](https://platform.kimi.ai/docs/api/models-overview): parameter differences across models