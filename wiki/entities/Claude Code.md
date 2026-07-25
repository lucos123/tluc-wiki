---
title: Claude Code
date: 2026-06-28
tags:
  - entity
  - tool
  - agent
---

# Claude Code

An agentic coding environment developed by Anthropic. 

## Design and Harness
A leak of its source code in early 2026 revealed advanced [[Harness Engineering]] patterns, including:
- **Progressive Context Compaction**: 5 levels of context compression to manage token limits.
- **Tiered Memory**: A 3-layer memory system including an "autoDream" consolidation mode.
- **Modular Skills Architecture**: Extending capabilities via `SKILL.md` files (following the Agent Skills standard) which support dynamic context injection, subagent execution, and precise invocation control (see [[Claude Code Skills]]).
- **Lifecycle Hooks**: Deterministic shell, prompt, or MCP commands that fire automatically at key events (e.g., `PreToolUse`, `SessionStart`) to enforce guardrails and format code (see [[Claude Code Hooks]]).
- **Monorepo Scoping**: Tools to restrict context across large codebases using hierarchical instruction files, exclusion patterns, and sparse worktrees (see [[Claude Code Monorepo Setup]]).
- **Permission-Gated Tools**: Over 40 single-purpose tools with deterministic risk classification.

## Best Practices
To maintain performance given the finite context window, users are encouraged to:
- Rely on `CLAUDE.md` for a [[Persistent Instruction File]], but prune it aggressively.
- Provide verification steps (tests, linters) to enable autonomous loops.
- Use `/clear` between tasks and leverage `/compact` and subagents to keep the main context clean.

See [[12 Agentic Harness Patterns from Claude Code]], [[Best practices for Claude Code]], and [[Harness Engineering]] for deep dives into its architecture.
