---
title: "Few-Shot Prompting"
date: 2026-11-15
tags:
  - concept
  - prompt-engineering
  - context-engineering
source: "[[Prompt Engineering Handbook]]"
---

# Few-Shot Prompting

**Few-Shot Prompting** (or in-context example-based prompting) is a technique in [[Prompt Engineering]] where an LLM is supplied with a small number of demonstration input–output pairs inside the prompt so it infers the desired pattern, formatting, and decision boundary before processing a new query.

---

## Prompting Spectrum by Example Count

| Mode | Examples | Accuracy | Output Control | Optimal Use Case |
| :--- | :---: | :---: | :---: | :--- |
| **Zero-Shot** | `0` | ★☆☆☆☆ | Low | Simple tasks, general knowledge, no examples available |
| **One-Shot** | `1` | ★★★☆☆ | Medium | Learning a quick output format, lightweight Q&A |
| **Few-Shot** | `2 – 10+` | ★★★★☆ | High | Classification, text transformation, strict schema consistency |
| **Instruction-Based** | Optional | ★★★★☆ | High | Explicit multi-constraint tasks (summarization, extraction) |
| **Role-Based** | Optional | ★★★★☆ | High | Persona-driven specialist guidance or simulation |
| **Hybrid** | Included | ★★★★★ | Very High | Complex multi-step reasoning combining Role + Examples + Instructions |

---

## Example Selection Principles

- **Quality over quantity:** A few well-chosen, unambiguous demonstrations outperform many noisy examples.
- **High-quality criteria:** Directly relevant to the target task, covers edge-case variations, pairs concise unambiguous inputs with exact target outputs, and maintains uniform formatting across every demonstration.
- **Anti-patterns:** Off-topic demonstrations, overly long/bloated examples (increasing token spend and [[Context Rot]]), or inconsistent output schemas across shots.

---

## Related Pages
- **Sources**: [[Prompt Engineering Handbook]], [[Token and API Price Guide]]
- **Concepts**: [[Prompt Engineering]], [[Chain-of-Thought Prompting]], [[Context Engineering]], [[Token Economics]]
