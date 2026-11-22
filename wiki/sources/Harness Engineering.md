---
title: "Summary: Harness Engineering (Goon Nguyen)"
date: 2026-06-28
tags:
  - harness-engineering
  - system-design
source: "raw/articles/ai-other/harness-engineering.md"
---

# Harness Engineering là gì?

## Summary
This article defines [Harness Engineering](../concepts/Harness%20Engineering.md) as the practice of building the entire environment around an AI model (tools, permissions, memory, feedback loops, guardrails). It argues that the model is merely what thinks, while the harness determines what it thinks about and how effectively it operates.

## Key Insights
- **Evolution of Focus**: Prompt Engineering (questions) → [Context Engineering](../concepts/Context%20Engineering.md) (input data) → [Harness Engineering](../concepts/Harness%20Engineering.md) (entire ecosystem).
- **SWE-agent Findings**: Interface design (Agent-Computer Interface) like limiting search results, prepending line numbers, and adding linter feedback can improve performance by 64% without changing the model.
- **Anthropic's Multi-Agent Architecture**: To solve failures like "doing too much at once" or "declaring victory early", Anthropic evolved to a 3-agent setup: Planner, Generator, and Evaluator. This dramatically improved success rates for complex tasks.
- **Claude Code Leak**: Validated that the value lies in the harness, utilizing 5 stages of context management, 3-tier memory with "autoDream" consolidation, and 40+ permission-gated tools.
- **Harness in Harness (Harness²)**: Systems like ClaudeKit and GoClaw add another layer of structured workflows, quality gates, and multi-agent coordination on top of existing harnesses.

## Associated Entities & Concepts
- [Harness Engineering](../concepts/Harness%20Engineering.md)
- [Context Engineering](../concepts/Context%20Engineering.md)
- [Claude Code](../entities/Claude%20Code.md)
