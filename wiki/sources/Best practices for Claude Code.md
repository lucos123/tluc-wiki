---
title: "Summary: Best practices for Claude Code"
date: 2026-06-28
tags:
  - best-practices
  - claude-code
  - agentic-design
source: "[[raw/Best practices for Claude Code.md]]"
---

# Best practices for Claude Code

## Summary
A comprehensive guide to effectively using Anthropic's [[Claude Code]] agentic coding environment. It emphasizes the importance of managing the context window, separating exploration from execution, and using verification loops.

## Key Insights
- **Manage Context Aggressively**: The context window is the most precious resource. Performance degrades as it fills. Use `/clear` between tasks, and rely on `/compact` or "autoDream" (background consolidation) to preserve important code patterns while freeing space.
- **Provide Verification**: Give Claude a check it can run (tests, builds, linters, screenshots). It enables Claude to iterate until the check passes without human intervention. This can be done via `/goal` or deterministic hooks.
- **Explore, Plan, Code**: Separate research from implementation. Use plan mode to map out the codebase, or spawn subagents for investigation to avoid cluttering the main context.
- **Configure the Environment**: Use `CLAUDE.md` for persistent context (see [[Persistent Instruction File]]), but keep it concise—bloated rule files cause Claude to ignore instructions. Extend capabilities with MCP servers, deterministic hooks, and reusable workflow skills (`SKILL.md`).
- **Parallelism and Scale**: Scale output by running non-interactive mode (`claude -p`) in CI, running multiple parallel sessions across isolated worktrees, and using an adversarial review step (a fresh subagent to review the diff).

## Associated Entities & Concepts
- [[Claude Code]]
- [[Persistent Instruction File]]
- [[Harness Engineering]]
