---
title: "How the agent loop works"
date: 2026-08-10
tags:
  - source
  - agent-sdk
  - harness-engineering
  - claude-code
source: "raw/articles/claude-code/context-memory-rules/agent-loop.md"
url: "https://code.claude.com/docs/en/agent-sdk/agent-loop.md"
---

# How the agent loop works

**URL**: https://code.claude.com/docs/en/agent-sdk/agent-loop.md  
**Source File**: [raw/articles/claude-code/context-memory-rules/agent-loop.md](../../raw/articles/claude-code/context-memory-rules/agent-loop.md)  

---

## Executive Summary

This official Anthropic reference explains the underlying architecture, message stream lifecycle, tool execution model, and control options powering the [Claude Code](../entities/Claude%20Code.md) Agent SDK in TypeScript and Python.

---

## The 5-Step Message Loop Lifecycle

```
Receive Prompt (SystemMessage 'init') ──> Evaluate & Respond (AssistantMessage)
  ──> Execute Tools (Parallel read / Sequential edit) ──> UserMessage (Tool Output)
        ──> [Repeat Turn Cycle until text-only response] ──> ResultMessage (Cost & Tokens)
```

### Core Message Types

1. **`SystemMessage`**: Session lifecycle metadata (`"init"`, `"compact_boundary"`, `"informational"`, `"worker_shutting_down"`).
2. **`AssistantMessage`**: Model responses containing text blocks and tool call definitions.
3. **`UserMessage`**: Tool execution results returned to the model or mid-loop user inputs.
4. **`StreamEvent`**: Real-time token deltas and tool input streaming chunks.
5. **`ResultMessage`**: Final stream marker containing cost, token counts, and result status (`"success"`, `"error_max_turns"`, `"error_max_budget_usd"`).

---

## Parallel vs Sequential Tool Execution

- **Read-Only Tools** (`Read`, `Glob`, `Grep`, MCP read tools): Executed concurrently/in parallel for speed.
- **State-Modifying Tools** (`Edit`, `Write`, `Bash`): Executed sequentially to prevent file diff corruption.
- **Custom Tools**: Default to sequential execution unless `readOnlyHint` annotation is set.

---

## Control & Reasoning Parameters

- **`max_turns`**: Caps total tool-use round trips.
- **`max_budget_usd`**: Hard spend limit; automatically halts background subagents when budget is reached.
- **`effort`**: Tunes reasoning depth (`"low"`, `"medium"`, `"high"`, `"xhigh"`, `"max"`).
- **`permission_mode`**: Controls tool execution gating (`"default"`, `"acceptEdits"`, `"plan"`, `"dontAsk"`, `"auto"`, `"bypassPermissions"`).

---

## Related Knowledge Nodes

- **Concepts**:
  - [Agent Loop Lifecycle](../concepts/Agent%20Loop%20Lifecycle.md)
  - [Agent SDK Architecture](../concepts/Agent%20SDK%20Architecture.md)
  - [Reasoning Effort](../concepts/Reasoning%20Effort.md)
  - [Context Window Management](../concepts/Context%20Window%20Management.md)
  - [Subagent Context Isolation](../concepts/Subagent%20Context%20Isolation.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
