---
title: "Advanced Prompting Patterns"
date: 2026-11-15
tags:
  - concept
  - prompt-engineering
  - agentic-design
source: "wiki/sources/Prompt Engineering Handbook.md"
---

# Advanced Prompting Patterns

Beyond single-shot instructions and [Few-Shot Prompting](Few-Shot%20Prompting.md), **Advanced Prompting Patterns** structure multi-step reasoning, branching exploration, external tool invocation, and prompt self-optimization—serving as the conceptual bridge from static [Prompt Engineering](Prompt%20Engineering.md) toward [Loop Engineering](Loop%20Engineering.md) and [Graph Engineering](Graph%20Engineering.md).

---

## Core Patterns Matrix

| Pattern | Mechanism | Optimal Use Case | Agentic Evolution |
| :--- | :--- | :--- | :--- |
| **[Chain-of-Thought Prompting](Chain-of-Thought%20Prompting.md)** | Linear step-by-step intermediate reasoning before final answer | Math, logic, debugging, structured explanations | Native [Reasoning Effort](Reasoning%20Effort.md) & thinking tokens |
| **Self-Consistency** | Sample multiple reasoning paths and select consensus answer | High-accuracy reasoning with multiple valid paths | Ensemble / [Second Opinion Pattern](Second%20Opinion%20Pattern.md) |
| **Role Prompting** | Assign domain persona or expert perspective | Specialist advice, creative tone, simulations | Subagent definitions & `SKILL.md` personas |
| **ReAct-Style** | Interleaved `Thought → Action → Observation → Repeat` loop | Web search, tool execution, grounded QA | Core execution cycle in [Agent Loop Lifecycle](Agent%20Loop%20Lifecycle.md) |
| **Tree-of-Thought (ToT)** | Branch across candidate paths like a tree, evaluate, and pick optimal route | Complex planning, multi-constraint optimization | Branching workflow topologies in [Agent Graph](Agent%20Graph.md) |
| **Prompt Chaining** | Decompose a large task into sequential sub-prompts (`Summary → Extract → Draft`) | Large documents, deterministic multi-stage pipelines | Deterministic DAGs & [Dynamic Workflows](Dynamic%20Workflows.md) |
| **Meta-Prompting** | Instruct the LLM to rewrite/improve the prompt before answering it | Refining ambiguous prompts into structured instructions | Automated prompt optimization in [Closed-Loop Evals](Closed-Loop%20Evals.md) |

---

## Selection Heuristic

- **No single universal winner:** Combine patterns deliberately based on task complexity (e.g., *Role + Few-Shot + CoT* for Hybrid Prompting, or *Prompt Chaining + ReAct* for grounded research workflows).
- **Bridge to Harness Engineering:** When patterns like ReAct, Tree-of-Thought, and Prompt Chaining move from manual user copy-paste into software runtimes with persistent state, tools, and verification gates, they become [Harness Engineering](Harness%20Engineering.md), [Loop Engineering](Loop%20Engineering.md), and [Graph Engineering](Graph%20Engineering.md).

---

## Related Pages
- **Sources**: [Prompt Engineering Handbook](../sources/Prompt%20Engineering%20Handbook.md), [What Is Context Engineering](../sources/What%20Is%20Context%20Engineering.md)
- **Concepts**:
  - [Prompt Engineering](Prompt%20Engineering.md)
  - [Chain-of-Thought Prompting](Chain-of-Thought%20Prompting.md)
  - [Few-Shot Prompting](Few-Shot%20Prompting.md)
  - [Agent Engineering Ladder](Agent%20Engineering%20Ladder.md)
  - [Loop Engineering](Loop%20Engineering.md)
  - [Graph Engineering](Graph%20Engineering.md)
