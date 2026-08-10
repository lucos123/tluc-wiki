---
title: "Deterministic Lifecycle Hooks"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - automation
  - claude-code
source: "[[Automate actions with hooks]]"
---

# Deterministic Lifecycle Hooks

**Deterministic Lifecycle Hooks** is a [[Harness Engineering]] control mechanism in [[Claude Code]] where shell scripts are bound to explicit agent lifecycle events (`PreToolUse`, `PostToolUse`, `PermissionRequest`, `SessionStart`) to enforce non-negotiable safety guardrails and automated toolchains without relying on LLM probabilistic decision-making.

---

## Control Mechanisms

```mermaid
graph TD
    Event["Lifecycle Event (e.g. PreToolUse: Edit)"] --> HookExec["1. Execute Command Script (protect-files.sh)"]
    HookExec --> Check{"2. Exit Code check"}
    Check -- "exit 0" --> Allow["3. Allow Tool Execution"]
    Check -- "exit 2" --> Block["4. Block Execution & Pass Stderr to Model"]
```

## Key Applications

1. **File Edit Protection**: Intercepting `Edit` and `Write` calls to reject modifications to `.env` or `package-lock.json`.
2. **Auto-Formatting**: Running `prettier` or `eslint` via `PostToolUse` immediately after file writes.
3. **Environment Sync**: Dynamically exporting `direnv` environment variables into `$CLAUDE_ENV_FILE` on `CwdChanged` events.

See [[Automate actions with hooks]], [[Claude Code Hooks]], and [[Prompt-Based Hooks]].
