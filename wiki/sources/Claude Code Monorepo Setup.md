---
title: Claude Code Monorepo Setup
date: 2026-06-28
tags:
  - source
  - documentation
  - agentic-design
  - claude-code
source: "[[raw/cc-mono and large repo.md]]"
---

# Claude Code Monorepo Setup

**Source File**: [[raw/cc-mono and large repo.md]]

This document outlines strategies for configuring [[Claude Code]] to handle large, multi-package codebases (monorepos) without overwhelming the LLM's context window.

## Key Concepts

- **Hierarchical `CLAUDE.md` Layering**: Instead of one massive [[Persistent Instruction File]] at the repository root, developers can place `CLAUDE.md` files in each subsystem/package. Claude loads the root instructions, plus the specific directory's instructions where the task is initiated.
- **Exclusion Management**: Large projects can use the `claudeMdExcludes` setting to prevent Claude from loading irrelevant instruction files from other teams' packages. Additionally, `permissions.deny` rules can block Claude from reading generated code, build output, or vendored dependencies.
- **Sparse Worktrees**: To accelerate isolated subagent tasks, `worktree.sparsePaths` enables git sparse-checkouts, checking out only the required directories for a specific subtask rather than cloning the entire massive repo. Symlinking (`symlinkDirectories`) can be used to avoid duplicating massive folders like `node_modules`.
- **Per-Package Skills**: Instead of loading every prompt/skill into memory, developers can scope [[Claude Code Skills]] to specific directories (e.g., `packages/api/.claude/skills/`). The skill only loads when Claude operates within that package.
- **Code Intelligence**: By installing Language Server Protocol (LSP) plugins (e.g., typescript-lsp), Claude can jump straight to definitions and find references without needing to expensively `grep` the entire monorepo.

## Synthesis Notes

Managing an agent in a massive codebase is an exercise in [[Context Engineering]]. Providing Claude with access to *everything* paradoxically degrades performance. The "Harness Engineering" solution is to enforce strict scoping—whether through layered instructions, sparse worktrees, or directory-bound skills—ensuring the agent only sees what is immediately relevant to its current context.
