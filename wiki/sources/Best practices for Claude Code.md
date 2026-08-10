---
title: "Best practices for Claude Code"
date: 2026-08-10
tags:
  - source
  - best-practices
  - context-engineering
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/context-memory-rules/best-practices.md]]"
url: "https://code.claude.com/docs/en/best-practices.md"
---

# Best practices for Claude Code

**URL**: https://code.claude.com/docs/en/best-practices.md  
**Source File**: [[raw/articles/claude-code/context-memory-rules/best-practices.md]]  

---

## Executive Summary

This official Anthropic guide outlines essential patterns for working effectively with [[Claude Code]] across engineering workflows. The core constraint driving all best practices is that **LLM performance degrades as the context window fills up**.

The guide covers 5 key pillars:
1. **Verification Loops**: Giving Claude automated checks (tests, build exit codes, visual screenshots, `/goal` conditions, Stop hooks, or verification subagents) to close feedback loops autonomously.
2. **4-Phase Workflow**: Explore $\rightarrow$ Plan $\rightarrow$ Implement $\rightarrow$ Commit (using `plan` mode to separate research from code execution).
3. **Specific Prompting**: Providing precise constraints, `@file` references, error logs, and existing code patterns.
4. **Environment Setup**: Crafting concise `CLAUDE.md` files (advisory instructions), configuring permissions (Auto mode, sandboxing), connecting CLI tools, MCP servers, deterministic hooks, custom skills, and subagents.
5. **Session & Cost Management**: Managing context window degradation through compacting, resetting sessions, using fast mode, and selecting specialist models.

---

## Key Takeaways & Practices

### 1. The Verification Spectrum
| Verification Level | Mechanism | Best For |
| --- | --- | --- |
| **Prompt-level** | Request test execution & show evidence in the same turn | Quick one-off tasks |
| **Session-level** | Set `/goal` condition with automated evaluator | Multi-turn goal completion |
| **Deterministic Gate** | Stop hook blocking turn completion until pass | Production compliance |
| **Second Opinion** | Verification subagent / fresh-context model review | Refuting worker self-bias |

### 2. The 4-Phase Development Loop
```
Explore (Plan Mode: Shift+Tab)
  └── Plan (Generate implementation plan; Ctrl+G to edit)
        └── Implement (Execute code changes & run test suite)
              └── Commit (Create Git commit and open PR)
```

### 3. Effective `CLAUDE.md` Hygiene
- **Include**: Uninferrable Bash commands, custom code style rules, test runners, monorepo conventions.
- **Exclude**: Self-evident conventions, detailed API docs, information already readable in code.
- **Rule of Thumb**: *"Would removing this cause Claude to make mistakes?"* If not, prune it!

---

## Related Knowledge Nodes

- **Concepts**: [[Context Window Management]], [[Agentic Coding Workflow]], [[Verification Loop]], [[Persistent Instruction File]], [[Progressive Disclosure]], [[Unhobbling Claude]].
- **Entities**: [[Claude Code]], [[Anthropic]].
