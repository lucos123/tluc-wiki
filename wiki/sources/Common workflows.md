---
title: "Common workflows"
date: 2026-08-10
tags:
  - source
  - workflows
  - recipes
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/large-codebases-sdlc-worktrees/common-workflows.md]]"
url: "https://code.claude.com/docs/en/common-workflows.md"
---

# Common workflows

**URL**: https://code.claude.com/docs/en/common-workflows.md  
**Source File**: [[raw/articles/claude-code/large-codebases-sdlc-worktrees/common-workflows.md]]  

---

## Executive Summary

This official Anthropic guide provides concrete prompt recipes and operational patterns for everyday software engineering tasks in [[Claude Code]], including codebase exploration, bug fixing, refactoring, test generation, PR creation, session resuming, and shell piping.

---

## Workflow Recipe Taxonomy

```
Codebase Exploration ──> Bug Fixing ──> Refactoring ──> Testing ──> PR Creation
```

### 1. Codebase Exploration
- Start broad: `"give me an overview of this codebase"`.
- Drill down into domain boundaries: `"explain how authentication is handled"`.
- Trace execution flows: `"trace the login process from front-end to database"`.

### 2. Efficient Bug Fixing
- Feed empirical errors: `"I'm seeing an error when running npm test: [paste log]"`.
- Force root-cause analysis over error suppression.
- Require passing test verification before completion.

### 3. Incremental Refactoring
- Identify legacy patterns: `"find deprecated API usage"`.
- Apply refactors in small, testable increments maintaining backward compatibility.

### 4. Test Scaffolding
- Scan for uncovered functions: `"find uncovered functions in NotificationsService"`.
- Generate test cases covering edge conditions, null values, and boundary limits.

### 5. Session Resuming & Git PR Linking
- Name sessions explicitly using `/name <topic>`.
- Resume existing sessions via `/resume`, `claude --continue`, or `claude --from-pr <pr-number>`.
- Pipe shell logs directly into headless sessions: `cat error.log | claude -p "explain this error"`.

---

## Related Knowledge Nodes

- **Concepts**: [[Agentic Workflow Recipes]], [[Agentic Coding Workflow]], [[Git Worktree Isolation]], [[Subagent Context Isolation]].
- **Entities**: [[Claude Code]], [[Anthropic]].
