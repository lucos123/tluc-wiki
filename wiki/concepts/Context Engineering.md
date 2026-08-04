---
title: Context Engineering
date: 2026-06-28
tags:
  - concept
  - ai-sdlc
  - engineering_practice
---

# Context Engineering

The practice of providing AI agents with rich, structured information about a codebase, architecture, conventions, and intent, as detailed in [[The New SDLC With Vibe Coding]].

## The Six Types of Context
1. **Instructions**: Core roles, goals, and boundaries.
2. **Knowledge**: Retrieved docs and domain data.
3. **Memory**: Short-term session logs and long-term persistent state.
4. **Examples**: Few-shot demonstrations and codebase patterns.
5. **Tools**: APIs and scripts the agent can invoke.
6. **Guardrails**: Hard constraints and safety rules.

## Static vs. Dynamic Context & [[Progressive Disclosure]]
- **Static Context**: Always loaded (e.g., [[Agent Onboarding Files]] like `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, system prompts). Reliable but consumes tokens on every interaction.
- **Dynamic Context & [[Progressive Disclosure]]**: Loaded on demand via deferred tool loading (`ToolSearch`), task skills, and tree-structured rules, as detailed by [[Thariq Shihipar]] in [[The new rules of context engineering for Claude 5 generation models]].

## The [[Unhobbling Claude]] Paradigm & 80% Prompt Pruning
Anthropic demonstrated that removing over **80% of Claude Code's system prompt** for frontier models (Claude Opus 5, Claude Fable 5) produced zero loss on coding evals. Overconstraining models with negative guardrails ("DO NOT write comments") causes prompt clashes; **[[Unhobbling Claude]]** trusts model judgment to match surrounding code idioms. The `/doctor` command (`claude doctor`) automates rightsizing repo context.

## The [[Metacode]] Metaphor & Repository Legibility
As detailed by [[Bilgin Ibryam]] in [[Emerging Markdown Formats That Shape Coding Agent Behavior]], Context Engineering is formalized in an agent-ready repository through **[[Metacode]]** — structured Markdown files (`AGENTS.md`, `SKILL.md`, `spec.md`, `ARCHITECTURE.md`, `MEMORY.md`) that make architectural intent and domain rules legible to AI agents acting as Intent Compilers. Machine-local observations follow the [[Memory Promotion Path]] to become durable project rules.

## Relationship to Harness Engineering
Context Engineering is considered a subset of [[Harness Engineering]]. While Context Engineering focuses on *what information* the agent receives to answer correctly, Harness Engineering focuses on the *entire ecosystem* surrounding the agent (tools, permissions, feedback loops, guardrails). Tools like [[Claude Code]] manage context using progressive compaction techniques (e.g., MicroCompact, AutoCompact) to prevent "context rot" over long sessions.

## Context Truncation & Preserved Thinking Patterns

As explored in [[Kimi Multi-turn Context Management Guide]] and [[Preserved Thinking]]:
- **System Prompt Pinning**: When implementing FIFO message truncation in stateless APIs, the `system` prompt must remain pinned at the top of every payload while pruning older `user` and `assistant` messages.
- **[[Preserved Thinking]]**: Preserving historical `reasoning_content` across multi-turn tool loops allows reasoning models (`[[Kimi K3]]`, `[[Kimi K2.7 Code]]`) to retain continuous chains of thought without re-deriving decisions.
