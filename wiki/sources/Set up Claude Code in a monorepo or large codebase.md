---
title: "Set up Claude Code in a monorepo or large codebase"
date: 2026-08-10
tags:
  - source
  - large-codebase
  - monorepo
  - context-engineering
  - harness-engineering
  - claude-code
source: "raw/articles/claude-code/large-codebases-sdlc-worktrees/large-codebases.md"
url: "https://code.claude.com/docs/en/large-codebases.md"
---

# Set up Claude Code in a monorepo or large codebase

**URL**: https://code.claude.com/docs/en/large-codebases.md  
**Source File**: [raw/articles/claude-code/large-codebases-sdlc-worktrees/large-codebases.md](../../raw/articles/claude-code/large-codebases-sdlc-worktrees/large-codebases.md)  

---

## Executive Summary

This official Anthropic guide details how to configure [Claude Code](../entities/Claude%20Code.md) for large single-tree repositories and monorepos. In large codebases, default configurations risk filling context windows with instructions, file reads, and build output from unrelated subsystems.

The guide outlines 6 core optimization techniques:
1. **Per-directory `CLAUDE.md` Layering**: Root instructions cover global standards while package-level `CLAUDE.md` files provide local context.
2. **`claudeMdExcludes`**: Skipping irrelevant instruction files (`"**/packages/web/**"`) when starting from the root directory.
3. **`permissions.deny` Read Restrictions**: Explicitly blocking reads of generated code, build output, and vendored packages (`"Read(./**/dist/**)"`).
4. **Code Intelligence (LSP Plugins)**: Using Language Server Protocol plugins (`typescript-lsp`) for definition lookup rather than costly grep file scanning.
5. **Sparse Worktree Checkouts (`sparsePaths`)**: Checking out only touched subdirectories when starting parallel Git worktrees (`.worktree.sparsePaths`).
6. **Cross-Package Access (`--add-dir`)**: Granting access to sibling packages using `--add-dir` or `additionalDirectories`.

---

## Feature Matrix for Large Codebases

| Subsystem Problem | Optimization Technique | Configuration Key / Command |
| --- | --- | --- |
| Context polluted by global instructions | Per-directory `CLAUDE.md` | Place `CLAUDE.md` inside `packages/api/` |
| Other team's `CLAUDE.md` loading | Exclude irrelevant instruction files | `claudeMdExcludes: ["**/packages/web/**"]` |
| File reads scanning generated code | Block `Read` on build/vendored code | `permissions.deny: ["Read(./**/dist/**)"]` |
| High token cost of searching definitions | Code intelligence LSP plugin | `/plugin install typescript-lsp@claude-plugins-official` |
| Worktree creation takes too long | Sparse Git worktrees | `"worktree": { "sparsePaths": ["packages/api"] }` |
| Need sibling package access | Cross-directory access grant | `claude --add-dir ../shared` |

---

## Related Knowledge Nodes

- **Concepts**:
  - [Monorepo Context Engineering](../concepts/Monorepo%20Context%20Engineering.md)
  - [Sparse Worktree Checkouts](../concepts/Sparse%20Worktree%20Checkouts.md)
  - [Claude Code Monorepo Setup](Claude%20Code%20Monorepo%20Setup.md)
  - [Path-Scoped Rules](../concepts/Path-Scoped%20Rules.md)
  - [Context Window Management](../concepts/Context%20Window%20Management.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
