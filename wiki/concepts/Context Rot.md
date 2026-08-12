---
title: "Context Rot"
date: 2026-08-12
tags:
  - concept
  - context-engineering
  - harness-engineering
source: "[[What Is Context Engineering Why It Matters for AI Agents]]"
---

# Context Rot

**Context Rot** (also known as context degradation or "needle-in-a-haystack" decay) is the phenomenon where an LLM's reasoning quality, instruction-following accuracy, and factual fidelity degrade as the volume of unmanaged or irrelevant context increases.

---

## Causes & Consequences

```
┌─────────────────────────────────────────────────────────────┐
│                       Context Rot Causes                    │
├─────────────────────────────────────────────────────────────┤
│ • Raw data dumps (e.g. thousands of unparsed log/chat pages)│
│ • Outdated or contradictory tool outputs                     │
│ • Unpruned multi-turn conversation history                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Degradation Consequences                 │
├─────────────────────────────────────────────────────────────┤
│ • Increased hallucination rates                             │
│ • Ignored system prompt guardrails                         │
│ • Severe token cost inflation without accuracy gains        │
└─────────────────────────────────────────────────────────────┘
```

## Mitigation Strategies

1. **Progressive Disclosure**: Load instructions, tools, and reference manuals on-demand via `ToolSearch` and `references/` subdirectories.
2. **Context Compaction & Pruning**: Use `/clear`, `/compact`, and automated background compaction to discard stale turns.
3. **Structured Context Processing**: Filter, summarize, and label incoming payloads before prompt submission.

See [[What Is Context Engineering Why It Matters for AI Agents]], [[Context Engineering]], and [[Context Window Management]].
