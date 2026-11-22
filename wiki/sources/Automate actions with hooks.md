---
title: "Automate actions with hooks"
date: 2026-08-10
tags:
  - source
  - hooks
  - harness-engineering
  - automation
  - claude-code
source: "raw/articles/claude-code/hooks-tools-mcp-chrome/hooks-guide.md"
url: "https://code.claude.com/docs/en/hooks.md"
---

# Automate actions with hooks

**URL**: https://code.claude.com/docs/en/hooks.md  
**Source File**: [raw/articles/claude-code/hooks-tools-mcp-chrome/hooks-guide.md](../../raw/articles/claude-code/hooks-tools-mcp-chrome/hooks-guide.md)  

---

## Executive Summary

This official Anthropic guide details how to configure and run **Lifecycle Hooks** in [Claude Code](../entities/Claude%20Code.md).

Hooks execute deterministic shell commands, model evaluations, or agent checks at exact lifecycle events (`PreToolUse`, `PostToolUse`, `SessionStart`, `PermissionRequest`, `Stop`, `CwdChanged`). Unlike prompt instructions (which rely on LLM choice), hooks enforce non-negotiable project rules, format code automatically, and automate notifications.

---

## Lifecycle Event Summary

| Event Name | Trigger Phase | Action & Output Capabilities |
| --- | --- | --- |
| `SessionStart` | Session launch or resume | Context injection (`echo`), env loading via `$CLAUDE_ENV_FILE` |
| `PreToolUse` | Before tool execution | Exit code 2 blocks execution and returns stderr as feedback |
| `PostToolUse` | After tool succeeds | Auto-formatting via `jq` & `prettier` |
| `PermissionRequest` | Prior to user prompt | Auto-approve or modify mode via JSON stdout |
| `ConfigChange` | Config file modification | Audit logging to external files |
| `CwdChanged` | Working directory switch | Reactive env reloads (`direnv export bash`) |
| `Stop` | End of turn | Trigger model evaluation or clean-up logic |

---

## Hook Definition Syntax

In `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
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
  - [Verification Loop](../concepts/Verification%20Loop.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
