---
title: "Hooks reference"
date: 2026-08-10
tags:
  - source
  - hooks
  - harness-engineering
  - reference
  - claude-code
source: "raw/articles/claude-code/hooks-tools-mcp-chrome/hooks-reference.md"
url: "https://code.claude.com/docs/en/hooks-reference.md"
---

# Hooks reference

**URL**: https://code.claude.com/docs/en/hooks-reference.md  
**Source File**: [raw/articles/claude-code/hooks-tools-mcp-chrome/hooks-reference.md](../../raw/articles/claude-code/hooks-tools-mcp-chrome/hooks-reference.md)  

---

## Executive Summary

This official Anthropic reference manual documents the complete lifecycle event topography, JSON payload schemas, execution contracts, and handler types for **Lifecycle Hooks** in [Claude Code](../entities/Claude%20Code.md).

---

## Complete Event Topography (31 Events)

```
Session Lifecycle:
  SessionStart ──> UserPromptSubmit ──> UserPromptExpansion ──> Agentic Loop ──> Stop/StopFailure ──> SessionEnd
                                                                   │
                                           ┌───────────────────────┴───────────────────────┐
                                           │ PreToolUse -> PermissionRequest -> PostToolUse │
                                           │ SubagentStart -> TaskCreated -> SubagentStop   │
                                           └───────────────────────────────────────────────┘
```

---

## Handler Types & Decision Control

### Handler Types
1. **`command`**: Local shell script reading JSON from stdin.
2. **`http`**: Remote REST API endpoint receiving JSON POST body.
3. **`prompt`**: Small model evaluation on prompt string.
4. **`agent`**: Subagent evaluation on context payload.
5. **`mcp`**: Invocation of external MCP tool.

### Exit Code & JSON Contract
- **Exit 0**: Neutral pass-through.
- **Exit 2**: Active rejection (blocks pending tool or prompt, returning stderr to model).
- **JSON stdout (`hookSpecificOutput`)**: Structured control over permissions and decisions.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive rm -rf command blocked by hook"
  }
}
```

---

## Related Knowledge Nodes

- **Concepts**:
  - [Claude Code Hooks](Claude%20Code%20Hooks.md)
  - [Deterministic Lifecycle Hooks](../concepts/Deterministic%20Lifecycle%20Hooks.md)
  - [Prompt-Based Hooks](../concepts/Prompt-Based%20Hooks.md)
  - [Harness Engineering](../concepts/Harness%20Engineering.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
