---
title: Claude Code Hooks
date: 2026-06-28
tags:
  - source
  - documentation
  - agentic-design
  - claude-code
source: "[[raw/cc-hooks.md]]"
---

# Claude Code Hooks

**Source File**: [[raw/cc-hooks.md]]

This document outlines how [[Claude Code]] utilizes "Hooks", a core feature of [[Harness Engineering]] that allows users to run code deterministically at specific lifecycle points outside the LLM prompt.

## Key Concepts

- **Deterministic Control**: Hooks execute automatically when Claude Code edits files, finishes tasks, or needs input. They ensure certain actions (like linting or compliance checks) always happen, without relying on the LLM to remember them.
- **Lifecycle Events**: Claude Code supports a comprehensive set of events, including `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`, `PermissionRequest`, `ConfigChange`, and many others.
- **Hook Types**:
  - `command`: Runs shell commands (the default).
  - `http`: POSTs event data to a URL.
  - `mcp_tool`: Calls a tool on a connected MCP server.
  - `prompt`: Uses an LLM (like Claude Haiku) for a simple yes/no judgment call.
  - `agent`: Experimental multi-turn verification.
- **Input/Output via STDIN/STDOUT**: Hooks receive event data as JSON via standard input, and communicate their decisions (like blocking an action) via exit codes (e.g., exit 2 to block) or by printing a JSON object to standard output.
- **Matchers**: Hooks can be filtered using matchers (e.g., matching a specific tool name like `Bash` or `Edit|Write`) or using the `if` field for more granular pattern matching (e.g., `Bash(git *)`).

## Common Use Cases

- **Auto-Formatting**: Running `prettier` on every file edited (`PostToolUse` with an `Edit|Write` matcher).
- **Security Guardrails**: Blocking edits to protected files like `.env` or `.git/` (`PreToolUse` hooks that exit 2).
- **Environment Management**: Automatically reloading environment variables (like via `direnv`) when the working directory changes (`CwdChanged`).
- **Context Injection**: Pushing important guidelines back into the LLM's context window after it has been compressed (`SessionStart` with a `compact` matcher).
- **Auto-Approval**: Skipping permission dialogs for safe, trusted commands (returning `"behavior": "allow"` on a `PermissionRequest`).

## Synthesis Notes

Hooks represent the "scaffolding" in the `Agent = Model + Harness` equation. While [[Claude Code Skills]] provide the LLM with modular capabilities it *can* use, Hooks provide deterministic guarantees about what the system *must* do. This dual approach allows for a highly autonomous agent that remains strictly bounded by organizational security and workflow policies.
