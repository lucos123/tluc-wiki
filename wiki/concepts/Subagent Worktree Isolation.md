---
title: "Subagent Worktree Isolation"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - context-engineering
  - claude-code
source: "wiki/sources/Run parallel sessions with worktrees.md"
---

# Subagent Worktree Isolation

**Subagent Worktree Isolation** is the configuration pattern where subagent tasks (such as refactoring, linting, or research) execute inside an independent, temporary Git worktree.

---

## Frontmatter Configuration

In `.claude/agents/refactorer.md`:

```markdown
---
name: refactorer
description: Mechanical refactoring subagent
isolation: worktree
---
```

## Lifecycle & Cleanup

1. **Spawn**: Claude Code creates a temporary worktree under `.claude/worktrees/subagent-<id>/`.
2. **Execute**: The subagent reads, modifies, and tests code inside the isolated worktree without affecting the parent session's working directory.
3. **Automated Sweep**: If the subagent finishes with no changes, the worktree is deleted immediately. If changes exist, a periodic cleanup sweep removes the worktree after `cleanupPeriodDays`.

See [Run parallel sessions with worktrees](../sources/Run%20parallel%20sessions%20with%20worktrees.md), [Git Worktree Isolation](Git%20Worktree%20Isolation.md), and [Subagent Context Isolation](Subagent%20Context%20Isolation.md).
