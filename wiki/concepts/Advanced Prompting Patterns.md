---
title: "Advanced Prompting Patterns"
date: 2026-11-15
tags:
  - concept
  - prompt-engineering
  - agentic-design
source: "[[Prompt Engineering Handbook]]"
---

# Advanced Prompting Patterns

Beyond single-shot instructions and [[Few-Shot Prompting]], **Advanced Prompting Patterns** structure multi-step reasoning, branching exploration, external tool invocation, and prompt self-optimization—serving as the conceptual bridge from static [[Prompt Engineering]] toward [[Loop Engineering]] and [[Graph Engineering]].

---

## Core Patterns Matrix

| Pattern | Mechanism | Optimal Use Case | Agentic Evolution |
| :--- | :--- | :--- | :--- |
| **[[Chain-of-Thought Prompting]]** | Linear step-by-step intermediate reasoning before final answer | Math, logic, debugging, structured explanations | Native [[Reasoning Effort]] & thinking tokens |
| **Self-Consistency** | Sample multiple reasoning paths and select consensus answer | High-accuracy reasoning with multiple valid paths | Ensemble / [[Second Opinion Pattern]] |
| **Role Prompting** | Assign domain persona or expert perspective | Specialist advice, creative tone, simulations | Subagent definitions & `SKILL.md` personas |
| **ReAct-Style** | Interleaved `Thought → Action → Observation → Repeat` loop | Web search, tool execution, grounded QA | Core execution cycle in [[Agent Loop Lifecycle]] |
| **Tree-of-Thought (ToT)** | Branch across candidate paths like a tree, evaluate, and pick optimal route | Complex planning, multi-constraint optimization | Branching workflow topologies in [[Agent Graph]] |
| **Prompt Chaining** | Decompose a large task into sequential sub-prompts (`Summary → Extract → Draft`) | Large documents, deterministic multi-stage pipelines | Deterministic DAGs & [[Dynamic Workflows]] |
| **Meta-Prompting** | Instruct the LLM to rewrite/improve the prompt before answering it | Refining ambiguous prompts into structured instructions | Automated prompt optimization in [[Closed-Loop Evals]] |

---

## Selection Heuristic

- **No single universal winner:** Combine patterns deliberately based on task complexity (e.g., *Role + Few-Shot + CoT* for Hybrid Prompting, or *Prompt Chaining + ReAct* for grounded research workflows).
- **Bridge to Harness Engineering:** When patterns like ReAct, Tree-of-Thought, and Prompt Chaining move from manual user copy-paste into software runtimes with persistent state, tools, and verification gates, they become [[Harness Engineering]], [[Loop Engineering]], and [[Graph Engineering]].

---

## Related Pages
- **Sources**: [[Prompt Engineering Handbook]], [[What Is Context Engineering]]
- **Concepts**: [[Prompt Engineering]], [[Chain-of-Thought Prompting]], [[Few-Shot Prompting]], [[Agent Engineering Ladder]], [[Loop Engineering]], [[Graph Engineering]]
