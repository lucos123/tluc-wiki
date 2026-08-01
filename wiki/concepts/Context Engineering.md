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

## Static vs. Dynamic Context
- **Static Context**: Always loaded (e.g., `AGENTS.md`, system prompts). Reliable but consumes tokens on every interaction.
- **Dynamic Context**: Loaded on demand (e.g., RAG, triggered skills). Efficient but requires orchestration to summon correctly.

## Relationship to Harness Engineering
Context Engineering is considered a subset of [[Harness Engineering]]. While Context Engineering focuses on *what information* the agent receives to answer correctly, Harness Engineering focuses on the *entire ecosystem* surrounding the agent (tools, permissions, feedback loops, guardrails). Tools like [[Claude Code]] manage context using progressive compaction techniques (e.g., MicroCompact, AutoCompact) to prevent "context rot" over long sessions.

## Context Truncation & Preserved Thinking Patterns

As explored in [[Kimi Multi-turn Context Management Guide]] and [[Preserved Thinking]]:
- **System Prompt Pinning**: When implementing FIFO message truncation in stateless APIs, the `system` prompt must remain pinned at the top of every payload while pruning older `user` and `assistant` messages.
- **[[Preserved Thinking]]**: Preserving historical `reasoning_content` across multi-turn tool loops allows reasoning models (`[[Kimi K3]]`, `[[Kimi K2.7 Code]]`) to retain continuous chains of thought without re-deriving decisions.
