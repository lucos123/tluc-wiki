---
title: "Agent Loop Lifecycle"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - agentic-design
  - claude-code
source: "wiki/sources/How the agent loop works.md"
---

# Agent Loop Lifecycle

The **Agent Loop Lifecycle** is the event-driven execution stream that governs how an autonomous AI agent processes prompts, issues tool requests, handles user approvals, and iterates until goal completion.

---

## The 5 Message Types

```mermaid
graph TD
    System["1. SystemMessage (init)"] --> Assistant["2. AssistantMessage (Text + Tool Call)"]
    Assistant --> User["3. UserMessage (Tool Output Payload)"]
    User --> Stream["4. StreamEvent (Real-time Deltas)"]
    Stream --> Result["5. ResultMessage (Final Tokens & Cost)"]
```

## Turn Execution Rules

- **Turn Definition**: One complete round trip (Assistant tool call $\rightarrow$ System tool execution $\rightarrow$ User result payload).
- **Termination Signal**: The agent loop terminates when the model outputs a text-only `AssistantMessage` containing zero tool calls.
- **Circuit Breakers**: Loops are bounded using `max_turns` or `max_budget_usd`.

See [How the agent loop works](../sources/How%20the%20agent%20loop%20works.md), [Agent SDK Architecture](Agent%20SDK%20Architecture.md), and [Reasoning Effort](Reasoning%20Effort.md).
