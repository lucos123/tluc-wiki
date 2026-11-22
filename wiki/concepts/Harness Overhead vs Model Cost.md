---
title: "Harness Overhead vs Model Cost"
date: 2026-08-12
tags:
  - concept
  - harness-engineering
  - token-economics
  - cost-optimization
  - claude-code
source: "wiki/sources/Harness vs Model costs explained.md"
---

# Harness Overhead vs Model Cost

**Harness Overhead vs Model Cost** is the economic paradigm in agentic AI engineering detailing how financial spend is dominated by the surrounding environment (system prompts, tool definitions, multi-turn state roundtrips) rather than the raw cost of the LLM base model inference.

---

## Cost Divergence Mechanics

```mermaid
graph TD
    UserTask["Simple User Prompt (25 Tokens)"] --> PathA["Thin Chat UI"]
    UserTask --> PathB["Thick Agent Harness (e.g. Claude Code)"]

    PathA --> DirectCall["Direct Model Inference (25 Prompt + 500 Output Tokens)"]
    DirectCall --> LowCost["Cost: ~$0.01"]

    PathB --> Tollgate["System Prompt Tollgate (8,000 - 30,000 Tokens)"]
    Tollgate --> MultiTurn["Multi-Turn Tool Roundtrips (Read, Edit, Test)"]
    MultiTurn --> HighCost["Cost: ~$0.37 (30x Overhead)"]
```

## Primary Overhead Drivers

1. **System Prompt "Tollgate"**: Harnesses inject 8K–30K tokens of OS rules, tool schemas, and command instructions into every request payload.
2. **Multi-Turn Oscillation**: Agentic loops oscillate recursively between model requests and harness tool executions (e.g., check file $\rightarrow$ write file $\rightarrow$ run test $\rightarrow$ fix error), multiplying system prompt token billing on each turn.
3. **Harness Architecture Variance**: Harnesses vary in system prompt size for the exact same prompt (e.g., Claude Code ~$0.37 vs. Cline ~$0.07 vs. Pi ~$0.025).

See [Harness vs Model costs explained](../sources/Harness%20vs%20Model%20costs%20explained.md), [Jevons Paradox in AI](Jevons%20Paradox%20in%20AI.md), [Token Economics](Token%20Economics.md), and [System Prompt Caching Optimization](System%20Prompt%20Caching%20Optimization.md).
