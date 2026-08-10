---
title: Persistent Instruction File
date: 2026-06-28
tags:
  - concept
  - harness-engineering
---

# Persistent Instruction File

A core pattern in [[Harness Engineering]] and [[Context Engineering]] where an agent is configured via an open-format Markdown file placed in the repository root or global user directory.

## Implementations
Different coding agents have adopted this pattern, usually under different names, but serving the identical purpose of providing durable, context-rich guidance:
- **`CLAUDE.md`**: Used by [[Claude Code]]. Best practices dictate keeping it concise (<200 lines) to prevent context bloat. Supports hierarchical loading (from OS Managed policy `/etc/claude-code/CLAUDE.md` down to `~/.claude/CLAUDE.md`, `./CLAUDE.md`, and `./CLAUDE.local.md`), `@path` file imports, `.claude/rules/*.md` [[Path-Scoped Rules]], and `@AGENTS.md` imports / symlinks.
- **`AGENTS.md`**: Used by OpenAI's [[Codex]]. Encouraged to be treated as a team-wide README for agents, containing build commands, PR expectations, and verification rules.
- **`GEMINI.md`**: Used by the [[Gemini CLI]]. Can be layered hierarchically (global vs. project-specific) and supports `@include` imports for modularizing context.

## Complementary Mechanisms
- **[[Auto Memory]]**: Model-authored notes created automatically by Claude Code to record discovered build fixes and user corrections without manual developer editing.
- **[[Path-Scoped Rules]]**: Conditional rule files in `.claude/rules/` that load lazily only when matching glob paths are read.

## Benefits
- Prevents users from manually re-typing conventions in every prompt.
- Serves as a living document; when an agent makes a mistake, developers update the file during retrospectives so the mistake is not repeated.
