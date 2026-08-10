---
title: "Run parallel sessions with worktrees"
date: 2026-08-10
tags:
  - source
  - worktrees
  - harness-engineering
  - parallelism
  - claude-code
source: "[[raw/articles/claude-code/large-codebases-sdlc-worktrees/worktrees.md]]"
url: "https://code.claude.com/docs/en/worktrees.md"
---

# Run parallel sessions with worktrees

**URL**: https://code.claude.com/docs/en/worktrees.md  
**Source File**: [[raw/articles/claude-code/large-codebases-sdlc-worktrees/worktrees.md]]  

---

## Executive Summary

This official Anthropic guide explains how to use Git worktrees (`--worktree`) in [[Claude Code]] to isolate parallel agent sessions so file modifications never collide across concurrent tasks.

---

## Key Worktree Mechanisms

### 1. Launching Parallel Worktrees
```bash
claude --worktree feature-auth
claude --worktree "#1234" # Branch from PR #1234
```
- Worktrees are created under `.claude/worktrees/<name>/` on branch `worktree-<name>`.
- Multiple terminals can run independent sessions simultaneously without dirtying the primary Git checkout.

### 2. Copying Gitignored Environment Files (`.worktreeinclude`)
Because a worktree is a fresh Git checkout, untracked files like `.env` are missing by default. Placing `.worktreeinclude` at the project root copies specified gitignored files into every new worktree:
```text
.env
.env.local
config/secrets.json
```

### 3. Subagent Worktree Isolation (`isolation: worktree`)
Custom subagents can be forced to run in dedicated worktrees via YAML frontmatter:
```markdown
---
name: refactorer
isolation: worktree
---
```
Claude Code automatically cleans up subagent worktrees upon task completion if no uncommitted changes remain.

### 4. Base Branch Tuning (`worktree.baseRef`)
- `"fresh"` (Default): Branches off `origin/HEAD` (`main`) to guarantee a clean baseline.
- `"head"`: Branches off the local checkout's current `HEAD` to inherit unpushed local commits.

### 5. Multi-Layer Isolation Enforcement
Claude Code enforces strict sandbox boundaries:
- Blocks file edits (`Edit`, `Write`, `NotebookEdit`) targeting the main checkout.
- Blocks `Bash` or PowerShell commands whose working directory resolves to the main checkout.
- Blocks Git command redirects (`git -C`, `GIT_WORK_TREE`) pointing to the main checkout.

---

## Related Knowledge Nodes

- **Concepts**: [[Git Worktree Isolation]], [[Subagent Worktree Isolation]], [[Sparse Worktree Checkouts]], [[Monorepo Context Engineering]].
- **Entities**: [[Claude Code]], [[Anthropic]].
