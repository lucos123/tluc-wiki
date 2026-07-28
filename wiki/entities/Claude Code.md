---
title: Claude Code
date: 2026-07-28
tags:
  - entity
  - tool
  - agent
  - claude-code
---

# Claude Code

An agentic coding environment developed by Anthropic. Unlike a chatbot, Claude Code autonomously reads files, runs commands, makes changes, and iterates through problems with or without user supervision.

## Core Architecture

Claude Code's design follows the `Agent = Model + Harness` equation from [[Harness Engineering]]:
- **Progressive Context Compaction**: Summarises conversation history to free space while preserving key code patterns and decisions. Configurable with `/compact <instructions>`.
- **Tiered Memory**: Persistent context via [[Persistent Instruction File|CLAUDE.md]] (always loaded), skills (on-demand), and subagent memory (isolated per-task).
- **Permission-Gated Tools**: 40+ single-purpose tools with deterministic risk classification. Permission modes: `default`, `acceptEdits`, `auto`, `bypassPermissions`.

## Extension System

Four complementary mechanisms for extending Claude Code's behaviour (each loaded differently):

| Mechanism | When active | Deterministic? | Source |
|-----------|------------|---------------|--------|
| CLAUDE.md | Always (every session) | No (advisory) | [[Persistent Instruction File]] |
| Skills | On demand (invoked or auto-matched) | No (LLM-driven) | [[Claude Code Skills]] |
| Hooks | At lifecycle events (guaranteed) | Yes | [[Claude Code Hooks]] |
| Subagents | When delegated | Isolated context | |
| MCP servers | When connected | Via tools | |
| Plugins | When installed | Bundles all above | |

## Session Management

- **Checkpointing**: Every prompt creates a checkpoint. `Esc+Esc` or `/rewind` restores conversation and/or code state to any earlier checkpoint. Checkpoints persist across sessions.
- **`/btw`**: Throwaway side-question overlay — answer appears in dismissible overlay and **never enters conversation history**. No context cost.
- **`/clear`**: Resets context entirely between unrelated tasks.
- **`/compact`**: Compacts history with optional focus instructions.
- **Session naming**: `/rename` for branch-like session management. `claude --continue` / `claude --resume` for multi-sitting tasks.

## Parallel and Autonomous Operation

- **Non-interactive mode**: `claude -p "prompt"` for CI, pre-commit hooks, and scripts. Supports `--output-format json/stream-json`.
- **Worktrees**: Isolated git checkouts for parallel sessions without edit collisions.
- **Auto mode** (`--permission-mode auto`): Classifier model reviews commands and blocks risky actions (scope escalation, unknown infrastructure, hostile-content-driven commands). Lets routine work proceed unattended.
- **Agent teams**: Automated coordination of multiple Claude sessions with shared task queues, inter-agent messaging, and a designated team lead.
- **Fan-out**: Loop `claude -p` over files/tasks; use `--allowedTools` to scope per-batch.

## Verification Patterns

Four levels of verification gate strength (see [[Best practices for Claude Code]]):
1. **In-prompt**: ask Claude to run check and iterate in same message.
2. **`/goal` condition**: separate evaluator re-checks after every turn.
3. **Stop hook**: script blocks turn ending until check passes (8-block cap).
4. **Verification subagent**: fresh model reviews the diff (no writer bias).

## Monorepo Support

Hierarchical CLAUDE.md layering, `claudeMdExcludes`, `Read` deny rules, sparse worktrees (`worktree.sparsePaths`), per-directory skills, and code intelligence plugins. See [[Claude Code Monorepo Setup]].

## Large-Scale Code Migration

Claude Code (with Claude Fable 5 / Opus 4.8) has demonstrated the ability to run full language-port migrations at industrial scale. Two case studies from Anthropic engineers in 2026:
- [[Jarred Sumner]]: Bun Zig→Rust (~1M lines, <2 weeks, $165K in tokens)
- [[Mike Krieger]]: Internal tool Python→TypeScript (165K lines, 1 weekend)

The [[AI Code Migration]] methodology uses Claude Code for: multi-agent implementation fan-out, adversarial review loops, build daemon orchestration, and autonomous overnight test generation. The core shift: engineers design *loops and rules*, not code.

## Related Sources

- [[Best practices for Claude Code]] — practitioner's guide to context, verification, and scaling.
- [[Claude Code Skills]] — modular capability extension system.
- [[Claude Code Hooks]] — deterministic lifecycle event automation.
- [[Claude Code Monorepo Setup]] — large codebase scoping.
- [[12 Agentic Harness Patterns from Claude Code]] — leaked production architecture patterns.
- [[Harness Engineering]] — the theoretical framework Claude Code embodies.
