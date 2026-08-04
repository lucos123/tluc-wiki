---
title: "Unhobbling Claude"
date: 2026-08-04
tags:
  - concept
  - context-engineering
  - harness-engineering
  - claude-code
source: "[[The new rules of context engineering for Claude 5 generation models]]"
---

# Unhobbling Claude

**Unhobbling Claude** is the context engineering design principle of removing rigid, overconstraining system prompt rules ("never write comments", "do not create intermediate files") in favor of allowing frontier AI models (Claude Opus 5, Claude Fable 5) to use surrounding code context and autonomous judgment.

Detailed by [[Thariq Shihipar]] in [[The new rules of context engineering for Claude 5 generation models]].

---

## Background & Core Principle

In earlier agent architectures, rigid negative guardrails were necessary to prevent worst-case scenarios (e.g. deleting files or generating low-quality comments). However, as model intelligence evolved, these standing constraints created prompt clashes (e.g. system prompt instructing "DO NOT add comments" while the user's prompt requested documentation).

Anthropic demonstrated that **removing over 80% of Claude Code's system prompt** caused no measurable loss on coding benchmarks, while drastically reducing context token overhead and eliminating prompt friction.

---

## Key Rules of Unhobbling

1. **Replace Rigid Rules with Adaptive Guidance**: Instead of "never write multi-line comments", instruct the agent to "write code that matches the surrounding comment density, naming, and idiom".
2. **Shift from Few-shot Examples to Interface Design**: Avoid overly prescriptive few-shot examples that constrain exploration; instead, design clean tool parameters and typed enumerations.
3. **Use `/doctor` (`claude doctor`)**: Run automated context audits to prune stale, overconstrained rules from `CLAUDE.md` and `SKILL.md`.

See [[Context Engineering]] and [[Progressive Disclosure]].
