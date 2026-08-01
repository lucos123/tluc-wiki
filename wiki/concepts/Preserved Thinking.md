---
title: Preserved Thinking
date: 2026-08-01
tags:
  - concept
  - ai-models
  - context-engineering
  - agentic-design
---

# Preserved Thinking

**Preserved Thinking** is an architectural pattern in reasoning models (pioneered by [[Moonshot AI]] in [[Kimi K3]] and [[Kimi K2.7 Code]]) where intermediate reasoning tokens (`reasoning_content`) from prior turns are preserved and passed back into the conversation context payload.

## How it Works

In standard chat APIs, only the final `content` string of an assistant message is retained in context, discarding the chain-of-thought tokens generated during reasoning. 

Under Preserved Thinking (`thinking.keep="all"`):
1. The assistant response contains both `reasoning_content` (internal chain-of-thought) and `content` (final answer).
2. The client appends the complete assistant message object back into `messages`.
3. In subsequent turns, the model "reads" its prior reasoning steps, allowing it to build directly upon its past analysis without re-deriving conclusions or losing state during multi-step tool calls.

```
Turn 1: User Prompt ──> Agent Reason (reasoning_content) ──> Final Answer (content)
                             │
                             ▼ (Preserved in context)
Turn 2: User Prompt ──> Agent Reason (builds on Turn 1 reasoning) ──> Final Answer
```

## Trade-offs

| Advantage | Challenge |
|-----------|-----------|
| **Multi-Turn Coherence**: Prevents the model from forgetting why it made prior decisions in complex workflows. | **Context & Token Inflation**: Historical reasoning tokens consume context budget and increase input token billing. |
| **Tool Calling Stability**: Ensures multi-step tool loops retain the rationale behind intermediate function invocations. | **Strict Payload Requirements**: Missing or modifying `reasoning_content` in turns can trigger API validation errors on enforced models like `kimi-k2.7-code`. |

See [[Kimi Thinking Models & Preserved Thinking Guide]] and [[Context Engineering]].
