---
title: "Prompt Engineering"
date: 2026-11-15
tags:
  - concept
  - prompt-engineering
  - context-engineering
  - llm-foundations
source: "wiki/sources/Prompt Engineering Handbook.md"
---

# Prompt Engineering

**Prompt Engineering** is the discipline of designing, structuring, and iteratively refining inputs (prompts) to guide Large Language Models (LLMs) toward accurate, consistent, and useful outputs. On the [Agent Engineering Ladder](Agent%20Engineering%20Ladder.md), Prompt Engineering represents the foundational first rung that evolved into [Context Engineering](Context%20Engineering.md), Agent Skills, [Loop Engineering](Loop%20Engineering.md), and [Graph Engineering](Graph%20Engineering.md).

---

## Anatomy of an Effective Prompt (6 Core Components)

As synthesized in [Prompt Engineering Handbook](../sources/Prompt%20Engineering%20Handbook.md), a well-structured prompt combines up to six explicit building blocks:

```
Prompt = Role + Context + Task / Instruction + Input Data + Constraints + Output Format (+ Examples)
```

1. **Task / Instruction (Nhiệm vụ):** The exact action the model must perform.
2. **Context (Ngữ cảnh):** Background information, audience, or situational constraints explaining *why* it matters.
3. **Role / Persona (Vai trò — Optional):** Domain perspective or expertise framing the response style.
4. **Input Data (Dữ liệu đầu vào):** Source text, code, metrics, or records to process.
5. **Constraints (Ràng buộc):** Word limits, tone, stylistic boundaries, and explicit do/don't rules.
6. **Output Format (Định dạng đầu ra):** Target structural schema (bullet points, numbered steps, Markdown tables, JSON, prose).

---

## Prompting Frameworks

| Framework | Components | Best Suited For | Complexity |
| :--- | :--- | :--- | :--- |
| **CO-STAR** | **C**ontext, **O**bjective, **S**tyle, **T**one, **A**udience, **R**esponse | Content creation, marketing, user-facing communications | Medium |
| **R-T-F** | **R**ole, **T**ask, **F**ormat | Data analysis, structured reports, quick summaries | Low–Medium |
| **CLEAR** | **C**ontext, **L**ook/Role, **E**xpectation, **A**ction, **R**esult | Complex multi-step projects and problem solving | High |

---

## Iterative Prompting Workflow & Common Pitfalls

1. **6-Step Creation Loop:** Understand Problem $\rightarrow$ Plan Context $\rightarrow$ Write Prompt $\rightarrow$ Inspect Output $\rightarrow$ Refine $\rightarrow$ Final Output.
2. **Core Principles:** Be specific, give context, specify format and tone, add constraints, use examples, decompose complex tasks, keep phrasing simple, and iterate.
3. **Common Failure Modes:** Overly vague requests, excessively verbose prompts causing noise (related to [Context Rot](Context%20Rot.md)), missing output formatting, missing source context, and accepting the first output without review.

> ⚠️ **Evolving claim / Frontier Model Nuance:** While structured constraints and negative guardrails improve outputs in basic single-turn tasks, [Unhobbling Claude](Unhobbling%20Claude.md) (via [The new rules of context engineering for Claude 5 generation models](../sources/The%20new%20rules%20of%20context%20engineering%20for%20Claude%205%20generation%20models.md)) notes that over-constraining frontier reasoning/coding models with rigid negative rules in system prompts can trigger prompt clashes—requiring balance between explicit task specs and model autonomy.

---

## Systematic Prompt Debugging & Injection Defense (Production)

Synthesized from [AI Engineer Interview Notes](../sources/AI%20Engineer%20Interview%20Notes.md) (`koteswar.AI`):
1. **Six-Step Systematic Debugging Framework** *(replacing "prompt-tweaking by vibes")*:
   - **Reproduce**: Pin exact failing input and output.
   - **Isolate**: Test instruction alone with known-good context to distinguish instruction ambiguity from bad [RAG retrieval](Retrieval-Augmented%20Generation%20and%20Vector%20DBs.md).
   - **Inspect**: Factual miss $\rightarrow$ fix retrieval/grounding; task misunderstanding $\rightarrow$ rewrite instruction.
   - **Change One Variable**: Adjust instruction, few-shot examples, *or* temperature—never all three at once (never tune `temperature` and `top-p` together).
   - **Build a Regression Set**: Lock fixes against `10–20` repeatable eval test cases.
   - **Version Prompts**: Store prompts strictly in versioned code/config, never ephemeral chat threads, putting role/goal first and repeating critical constraints near the end to counter `Lost in the middle`.
2. **Indirect Prompt Injection Defense-in-Depth**: Malicious instructions embedded inside retrieved webpages or user data cannot be fixed by a single rule; layer **untrusted-data delimitation** (`<user_content>...</user_content>`), **least-privilege tool scopes**, **I/O pattern filtering**, **human confirmation for irreversible actions** (email, delete, purchase), and **anomalous tool-call monitoring**.

---

## Related Pages
- **Sources**:
  - [Prompt Engineering Handbook](../sources/Prompt%20Engineering%20Handbook.md)
  - [Token and API Price Guide](../sources/Token%20and%20API%20Price%20Guide.md)
  - [AI Engineer Interview Notes](../sources/AI%20Engineer%20Interview%20Notes.md)
  - [AI Complete Handbook](../sources/AI%20Complete%20Handbook.md)
- **Concepts**:
  - [Few-Shot Prompting](Few-Shot%20Prompting.md)
  - [Chain-of-Thought Prompting](Chain-of-Thought%20Prompting.md)
  - [Advanced Prompting Patterns](Advanced%20Prompting%20Patterns.md)
  - [Context Engineering](Context%20Engineering.md)
  - [Agent Engineering Ladder](Agent%20Engineering%20Ladder.md)
  - [AI System Design and Production Architecture](AI%20System%20Design%20and%20Production%20Architecture.md)
