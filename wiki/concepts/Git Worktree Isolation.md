---
title: "Git Worktree Isolation"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - parallelism
  - claude-code
source: "[[Run parallel sessions with worktrees]]"
---

# Git Worktree Isolation

**Git Worktree Isolation** is a core [[Harness Engineering]] pattern in [[Claude Code]] where each parallel agent session is assigned a dedicated Git worktree (`.claude/worktrees/<name>/`), isolating file modifications and branch state from other concurrent sessions.

---

## Architectural Workflow

```mermaid
graph TD
    MainRepo["Main Checkout (/repo)"] --> WT1["Worktree 1 (.claude/worktrees/feature-auth)"]
    MainRepo --> WT2["Worktree 2 (.claude/worktrees/fix-bug-456)"]
    WT1 -- "Isolated Edits" --> Branch1["Branch: worktree-feature-auth"]
    WT2 -- "Isolated Edits" --> Branch2["Branch: worktree-fix-bug-456"]
```

## Key Capabilities

1. **Collision-Free Parallelism**: Developers can run 5+ concurrent agent sessions building different features without file edit conflicts.
2. **Environment Mirroring (`.worktreeinclude`)**: Automatically copies `.env` and local credentials into fresh worktrees.
3. **Subagent Worktree Isolation**: Subagents configured with `isolation: worktree` run inside temporary worktrees that automatically self-clean upon completion.

See [[Run parallel sessions with worktrees]], [[Subagent Worktree Isolation]], and [[Sparse Worktree Checkouts]].
