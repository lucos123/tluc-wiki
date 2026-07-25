---
title: Programmatic Tool Calling
date: 2026-07-18
tags:
  - concept
  - agentic-design
  - ai-models
---

# Programmatic Tool Calling

A capability introduced with [[GPT-5.6]] where the model writes and runs lightweight programs that coordinate tools, process intermediate results, monitor progress, and choose next actions as work unfolds: [[GPT-5.6: Frontier Intelligence That Scales With Your Ambition]].

## Definition

Instead of requiring developers to script every step or passing every tool response back through the model, Programmatic Tool Calling allows the model itself to generate code that:

1. **Filters** large amounts of intermediate data
2. **Retains** only what matters
3. **Adapts** its workflow along the way

This reduces the number of tokens consumed, the number of model round trips, and the amount of developer guidance needed for tool-heavy tasks.

## Relationship to Other Concepts

Programmatic Tool Calling sits at the intersection of several existing wiki concepts:

- **[[Conductor vs Orchestrator]]**: This pushes strongly toward the Orchestrator mode — the model scripts its own tool orchestration rather than relying on developer scaffolding.
- **[[Harness Engineering]]**: Reduces the need for external harness complexity by internalizing tool coordination into the model layer.
- **[[Context Engineering]]**: By filtering intermediate data and retaining only relevant results, the model effectively manages its own context window.

## Implementation

Available through OpenAI's Responses API. The model generates executable code that invokes tools in sequence or parallel, evaluates results, and decides on next steps without returning control to the developer between each tool call.
