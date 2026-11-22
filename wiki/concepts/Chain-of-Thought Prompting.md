---
title: "Chain-of-Thought Prompting"
date: 2026-11-15
tags:
  - concept
  - prompt-engineering
  - llm-foundations
source: "wiki/sources/Prompt Engineering Handbook.md"
---

# Chain-of-Thought Prompting

**Chain-of-Thought (CoT) Prompting** (also called **Stepwise Prompting**) is a reasoning technique in [Prompt Engineering](Prompt%20Engineering.md) that guides an LLM to decompose complex problems into explicit intermediate logical steps before emitting the final answer.

---

## Core Mechanism

```
Understand Problem ──> Break Into Sub-Steps ──> Solve Step-by-Step ──> Final Answer (+ Self-Check)
```

- **Why it works:** Because LLMs predict tokens sequentially, generating explicit intermediate reasoning tokens constrains the probability distribution of the final conclusion, preventing premature guessing on multi-step arithmetic, syllogistic logic, and debugging tasks.
- **Logical Verification Example** (from [Prompt Engineering Handbook](../sources/Prompt%20Engineering%20Handbook.md)):
  - *Query:* "All cats are animals. Some animals are pets. Are all cats pets?"
  - *Direct Answer (Without CoT):* Prone to pattern-matching error ("Yes").
  - *Stepwise CoT:* Explicitly reasons over set inclusions ($\text{Cats} \subset \text{Animals}$; only a subset of $\text{Animals}$ are $\text{Pets}$) $\rightarrow$ correctly concludes **"No"**.

---

## CoT Extensions & Operational Best Practices

1. **Self-Consistency Prompting:** Samples multiple independent reasoning paths for the same prompt and selects the most consistent consensus answer—trading extra output tokens for higher accuracy on ambiguous reasoning tasks.
2. **Practical Tactics:** Use explicit cues (`"think step by step"`), request numbered steps, isolate the final conclusion on a dedicated final line, and optionally instruct the model to self-verify intermediate steps.

---

## Evolution Toward Native Reasoning Models

> ⚠️ **Evolving claim / Architectural shift:** Early CoT relied exclusively on prompt phrasing (`"let's think step by step"`). Modern frontier reasoning models internalize chain-of-thought natively via trained test-time compute—controlled through API parameters like [Reasoning Effort](Reasoning%20Effort.md) (`low`, `high`, `max`) and maintained across multi-turn tool loops via [Preserved Thinking](Preserved%20Thinking.md).

---

## Related Pages
- **Sources**: [Prompt Engineering Handbook](../sources/Prompt%20Engineering%20Handbook.md), [Kimi Thinking Models & Preserved Thinking Guide](../sources/Kimi%20Thinking%20Models%20%26%20Preserved%20Thinking%20Guide.md)
- **Concepts**:
  - [Prompt Engineering](Prompt%20Engineering.md)
  - [Few-Shot Prompting](Few-Shot%20Prompting.md)
  - [Advanced Prompting Patterns](Advanced%20Prompting%20Patterns.md)
  - [Reasoning Effort](Reasoning%20Effort.md)
  - [Preserved Thinking](Preserved%20Thinking.md)
