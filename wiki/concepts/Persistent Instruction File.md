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
- **`CLAUDE.md`**: Used by [[Claude Code]]. Best practices dictate keeping it extremely concise to prevent instructions from being lost in the noise. In large codebases, it supports hierarchical layering (per-directory files) and explicit exclusions (`claudeMdExcludes`) to ensure only relevant context is loaded (see [[Claude Code Monorepo Setup]]).
- **`AGENTS.md`**: Used by OpenAI's [[Codex]]. Encouraged to be treated as a team-wide README for agents, containing build commands, PR expectations, and verification rules.
- **`GEMINI.md`**: Used by the [[Gemini CLI]]. Can be layered hierarchically (global vs. project-specific) and supports `@include` imports for modularizing context.

## Benefits
- Prevents users from manually re-typing conventions in every prompt.
- Serves as a living document; when an agent makes a mistake, developers update the file during retrospectives so the mistake is not repeated.
