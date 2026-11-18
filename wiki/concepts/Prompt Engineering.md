---
title: "Prompt Engineering"
date: 2026-11-15
tags:
  - concept
  - prompt-engineering
  - context-engineering
  - llm-foundations
source: "[[Prompt Engineering Handbook]]"
---

# Prompt Engineering

**Prompt Engineering** is the discipline of designing, structuring, and iteratively refining inputs (prompts) to guide Large Language Models (LLMs) toward accurate, consistent, and useful outputs. On the [[Agent Engineering Ladder]], Prompt Engineering represents the foundational first rung that evolved into [[Context Engineering]], Agent Skills, [[Loop Engineering]], and [[Graph Engineering]].

---

## Anatomy of an Effective Prompt (6 Core Components)

As synthesized in [[Prompt Engineering Handbook]], a well-structured prompt combines up to six explicit building blocks:

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
3. **Common Failure Modes:** Overly vague requests, excessively verbose prompts causing noise (related to [[Context Rot]]), missing output formatting, missing source context, and accepting the first output without review.

> ⚠️ **Evolving claim / Frontier Model Nuance:** While structured constraints and negative guardrails improve outputs in basic single-turn tasks, [[Unhobbling Claude]] (via [[The new rules of context engineering for Claude 5 generation models]]) notes that over-constraining frontier reasoning/coding models with rigid negative rules in system prompts can trigger prompt clashes—requiring balance between explicit task specs and model autonomy.

---

## Systematic Prompt Debugging & Injection Defense (Production)

Synthesized from [[AI Engineer Interview Notes]] (`koteswar.AI`):
1. **Six-Step Systematic Debugging Framework** *(replacing "prompt-tweaking by vibes")*:
   - **Reproduce**: Pin exact failing input and output.
   - **Isolate**: Test instruction alone with known-good context to distinguish instruction ambiguity from bad [[Retrieval-Augmented Generation and Vector DBs|RAG retrieval]].
   - **Inspect**: Factual miss $\rightarrow$ fix retrieval/grounding; task misunderstanding $\rightarrow$ rewrite instruction.
   - **Change One Variable**: Adjust instruction, few-shot examples, *or* temperature—never all three at once (never tune `temperature` and `top-p` together).
   - **Build a Regression Set**: Lock fixes against `10–20` repeatable eval test cases.
   - **Version Prompts**: Store prompts strictly in versioned code/config, never ephemeral chat threads, putting role/goal first and repeating critical constraints near the end to counter `Lost in the middle`.
2. **Indirect Prompt Injection Defense-in-Depth**: Malicious instructions embedded inside retrieved webpages or user data cannot be fixed by a single rule; layer **untrusted-data delimitation** (`<user_content>...</user_content>`), **least-privilege tool scopes**, **I/O pattern filtering**, **human confirmation for irreversible actions** (email, delete, purchase), and **anomalous tool-call monitoring**.

---

## Related Pages
- **Sources**: [[Prompt Engineering Handbook]], [[Token and API Price Guide]], [[AI Engineer Interview Notes]], [[AI Complete Handbook]]
- **Concepts**: [[Few-Shot Prompting]], [[Chain-of-Thought Prompting]], [[Advanced Prompting Patterns]], [[Context Engineering]], [[Agent Engineering Ladder]], [[AI System Design and Production Architecture]]
