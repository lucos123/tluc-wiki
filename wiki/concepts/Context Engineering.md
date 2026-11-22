---
title: Context Engineering
date: 2026-06-28
tags:
  - concept
  - ai-sdlc
  - engineering_practice
---

# Context Engineering

The practice of providing AI agents with rich, structured information about a codebase, architecture, conventions, and intent, as detailed in [The New SDLC With Vibe Coding](../sources/The%20New%20SDLC%20With%20Vibe%20Coding.md).

## The Six Types of Context
1. **Instructions**: Core roles, goals, and boundaries.
2. **Knowledge**: Retrieved docs and domain data.
3. **Memory**: Functional agent recall spanning seven responsibilities—working, semantic, episodic, procedural, external, parametric, and prospective triggers (see [AI Agent Memory Types](AI%20Agent%20Memory%20Types.md)).
4. **Examples**: Few-shot demonstrations and codebase patterns.
5. **Tools**: APIs and scripts the agent can invoke.
6. **Guardrails**: Hard constraints and safety rules.

## Static vs. Dynamic Context & [Progressive Disclosure](Progressive%20Disclosure.md)
- **Static Context**: Always loaded (e.g., [Agent Onboarding Files](Agent%20Onboarding%20Files.md) like `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, system prompts). Reliable but consumes tokens on every interaction.
- **Dynamic Context & [Progressive Disclosure](Progressive%20Disclosure.md)**: Loaded on demand via deferred tool loading (`ToolSearch`), task skills, and tree-structured rules, as detailed by [Thariq Shihipar](../entities/Thariq%20Shihipar.md) in [The new rules of context engineering for Claude 5 generation models](../sources/The%20new%20rules%20of%20context%20engineering%20for%20Claude%205%20generation%20models.md).

## The [Unhobbling Claude](Unhobbling%20Claude.md) Paradigm & 80% Prompt Pruning
Anthropic demonstrated that removing over **80% of Claude Code's system prompt** for frontier models (Claude Opus 5, Claude Fable 5) produced zero loss on coding evals. Overconstraining models with negative guardrails ("DO NOT write comments") causes prompt clashes; **[Unhobbling Claude](Unhobbling%20Claude.md)** trusts model judgment to match surrounding code idioms. The `/doctor` command (`claude doctor`) automates rightsizing repo context.

## The [Metacode](Metacode.md) Metaphor & Repository Legibility
As detailed by [Bilgin Ibryam](../entities/Bilgin%20Ibryam.md) in [Emerging Markdown Formats That Shape Coding Agent Behavior](../sources/Emerging%20Markdown%20Formats%20That%20Shape%20Coding%20Agent%20Behavior.md), Context Engineering is formalized in an agent-ready repository through **[Metacode](Metacode.md)** — structured Markdown files (`AGENTS.md`, `SKILL.md`, `spec.md`, `ARCHITECTURE.md`, `MEMORY.md`) that make architectural intent and domain rules legible to AI agents acting as Intent Compilers. Machine-local observations follow the [Memory Promotion Path](Memory%20Promotion%20Path.md) to become durable project rules.

## Relationship to Harness Engineering
Context Engineering is considered a subset of [Harness Engineering](Harness%20Engineering.md). While Context Engineering focuses on *what information* the agent receives to answer correctly, Harness Engineering focuses on the *entire ecosystem* surrounding the agent (tools, permissions, feedback loops, guardrails). Tools like [Claude Code](../entities/Claude%20Code.md) manage context using progressive compaction techniques (e.g., MicroCompact, AutoCompact) to prevent "context rot" over long sessions.

## Context Truncation & Preserved Thinking Patterns

As explored in [Kimi Multi-turn Context Management Guide](../sources/Kimi%20Multi-turn%20Context%20Management%20Guide.md) and [Preserved Thinking](Preserved%20Thinking.md):
- **System Prompt Pinning**: When implementing FIFO message truncation in stateless APIs, the `system` prompt must remain pinned at the top of every payload while pruning older `user` and `assistant` messages.
- **[Preserved Thinking](Preserved%20Thinking.md)**: Preserving historical `reasoning_content` across multi-turn tool loops allows reasoning models ([Kimi K3](../entities/Kimi%20K3.md), [Kimi K2.7 Code](../entities/Kimi%20K2.7%20Code.md)) to retain continuous chains of thought without re-deriving decisions.
