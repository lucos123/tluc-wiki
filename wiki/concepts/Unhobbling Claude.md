---
title: "Unhobbling Claude"
date: 2026-08-04
tags:
  - concept
  - context-engineering
  - harness-engineering
  - claude-code
source: "wiki/sources/The new rules of context engineering for Claude 5 generation models.md"
---

# Unhobbling Claude

**Unhobbling Claude** is the context engineering design principle of removing rigid, overconstraining system prompt rules ("never write comments", "do not create intermediate files") in favor of allowing frontier AI models (Claude Opus 5, Claude Fable 5) to use surrounding code context and autonomous judgment.

Detailed by [Thariq Shihipar](../entities/Thariq%20Shihipar.md) in [The new rules of context engineering for Claude 5 generation models](../sources/The%20new%20rules%20of%20context%20engineering%20for%20Claude%205%20generation%20models.md).

---

## Background & Core Principle

In earlier agent architectures, rigid negative guardrails were necessary to prevent worst-case scenarios (e.g. deleting files or generating low-quality comments). However, as model intelligence evolved, these standing constraints created prompt clashes (e.g. system prompt instructing "DO NOT add comments" while the user's prompt requested documentation).

Anthropic demonstrated that **removing over 80% of Claude Code's system prompt** caused no measurable loss on coding benchmarks, while drastically reducing context token overhead and eliminating prompt friction.

---

## Key Rules of Unhobbling

1. **Replace Rigid Rules with Adaptive Guidance**: Instead of "never write multi-line comments", instruct the agent to "write code that matches the surrounding comment density, naming, and idiom".
2. **Shift from Few-shot Examples to Interface Design**: Avoid overly prescriptive few-shot examples that constrain exploration; instead, design clean tool parameters and typed enumerations.
3. **Run `/doctor prompt-audit` & Retain Only Non-Code Facts**: As [Lydia Hallie](../entities/Lydia%20Hallie.md) notes in [Rethinking Claude Code Best Practices — Lydia Hallie, Anthropic](../sources/Rethinking%20Claude%20Code%20Best%20Practices%20%E2%80%94%20Lydia%20Hallie%2C%20Anthropic.md), on frontier models (`Opus 5.5`), stale directives (`"IMPORTANT!"`, `"We're on Node 18"`, `"Think hard"`) actively degrade performance via extra tool calls; keep *only* facts invisible in source code (`"src/legacy still serves our mobile apps"`).

See [Context Engineering](Context%20Engineering.md), [Progressive Disclosure](Progressive%20Disclosure.md), and [Best practices for Claude Code](../sources/Best%20practices%20for%20Claude%20Code.md).
