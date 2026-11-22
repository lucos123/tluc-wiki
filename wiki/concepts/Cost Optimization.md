---
title: "Cost Optimization"
date: 2026-08-10
tags:
  - concept
  - cost-optimization
  - harness-engineering
  - claude-code
source: "wiki/sources/Manage costs effectively.md"
---

# Cost Optimization

**Cost Optimization** encompasses the active engineering techniques used to minimize token consumption in [Claude Code](../entities/Claude%20Code.md) without sacrificing task completion quality or model reasoning precision.

---

## High-Impact Optimization Tactics

1. **Context Pruning & Multi-Turn Hygiene (`/clear`, `/compact`, `/autocompact`)**: Clearing sessions between unrelated tasks prevents stale context from compounding token costs across every subsequent turn. On 1M context models, set `/autocompact 200k` (Claude Code v2.1.221+) to prevent runaway multi-turn drag.
2. **Direct File Referencing via `@-Mentions`**: Referencing `@file.ts` attaches the file directly to Turn 1 payload, eliminating search turns (`grep`/`find`) and unnecessary `Read` tool invocations.
3. **Noisy Command Management**: Test outputs under 30,000 chars (`BASH_MAX_OUTPUT_LENGTH`) persist in context for all remaining turns. Specify quiet flags directly in `CLAUDE.md` (e.g. `vitest --reporter=dot`), install pre-execution output filtering hooks, or offload noisy tasks to subagents.
4. **Metacode Offloading**: Keeping `CLAUDE.md` under 200 lines by moving specialized workflow instructions into on-demand [Agent Skills](Agent%20Skills%20Architecture.md).
5. **Subagent Offloading**: Spawning subagents configured with `model: haiku` for high-volume log parsing or repo auditing; intermediate tool noise is discarded and only concise answers return to main context.
6. **Isolated `/loop` Execution**: Launching background `/loop` commands in clean, dedicated terminal sessions to avoid compounding main session context and incurring 1-hour cache TTL misses.
7. **Model × Effort Balancing & Zero-Thinking Grunt Work**: Setting `/model` and `/effort` at startup to protect prompt cache prefixes. For mechanical tasks, running `MAX_THINKING_TOKENS=0 claude` disables thinking token output completely.

---

## Related Knowledge Nodes

- **Concepts**:
  - [Token Economics](Token%20Economics.md)
  - [Cache Invalidation Patterns](Cache%20Invalidation%20Patterns.md)
  - [Context Window Management](Context%20Window%20Management.md)
  - [Subagent Context Isolation](Subagent%20Context%20Isolation.md)
  - [Harness Overhead vs Model Cost](Harness%20Overhead%20vs%20Model%20Cost.md)
  - [Effort Level and Model Selection](Effort%20Level%20and%20Model%20Selection.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
- **Sources**:
  - [Maximizing the Value of Your Claude Code Sessions](../sources/Maximizing%20the%20Value%20of%20Your%20Claude%20Code%20Sessions.md)
  - [Manage costs effectively](../sources/Manage%20costs%20effectively.md)
  - [How Claude Code uses prompt caching](../sources/How%20Claude%20Code%20uses%20prompt%20caching.md)
  - [Claude Code effort level and model selection](../sources/Claude%20Code%20effort%20level%20and%20model%20selection.md)
