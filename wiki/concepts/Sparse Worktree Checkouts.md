---
title: "Sparse Worktree Checkouts"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - monorepo
  - claude-code
source: "wiki/sources/Set up Claude Code in a monorepo or large codebase.md"
---

# Sparse Worktree Checkouts

**Sparse Worktree Checkouts** is a Git harness engineering optimization in [Claude Code](../entities/Claude%20Code.md) that utilizes `git sparse-checkout` to check out only specified subdirectories when spawning isolated parallel Git worktrees (`--worktree`).

---

## Configuration

In `.claude/settings.json`:

```json
{
  "worktree": {
    "sparsePaths": [
      ".claude",
      "packages/api",
      "packages/shared"
    ]
  }
}
```

## Benefits

1. **Subagent Spawning Speed**: Parallel subagents spawned with `isolation: worktree` start significantly faster because large unneeded packages are omitted.
2. **Disk Storage Savings**: Reduces duplicate checkout footprints in large monorepos.
3. **Context Cleanliness**: Eliminates file reads on unrelated directories within subagent sessions.

See [Set up Claude Code in a monorepo or large codebase](../sources/Set%20up%20Claude%20Code%20in%20a%20monorepo%20or%20large%20codebase.md) and [Monorepo Context Engineering](Monorepo%20Context%20Engineering.md).
