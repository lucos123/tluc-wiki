---
title: "Create custom subagents"
date: 2026-08-10
tags:
  - source
  - subagents
  - harness-engineering
  - context-engineering
  - claude-code
source: "[[raw/articles/claude-code/agent-architecture-subagents-workflows/sub-agents.md]]"
url: "https://code.claude.com/docs/en/sub-agents.md"
---

# Create custom subagents

**URL**: https://code.claude.com/docs/en/sub-agents.md  
**Source File**: [[raw/articles/claude-code/agent-architecture-subagents-workflows/sub-agents.md]]  

---

## Executive Summary

This official Anthropic guide details how to build and orchestrate specialized AI **Subagents** in [[Claude Code]].

Subagents run in their own isolated context windows with custom system prompts, specific tool permissions, and optional worktree isolation. By offloading heavy searches, logs, and multi-file analysis to subagents, developers keep the main session context small, focused, and performant.

---

## Built-in vs. Custom Subagents

### Built-in Subagents
- **`Explore`**: Fast, read-only agent for code searching and file navigation.
- **`Plan`**: Read-only research agent executing under Plan Mode (`/plan`).
- **`General-purpose`**: Full-capability agent for complex tasks requiring both exploration and code edits.

### Custom Subagent Scope & Resolution Order
```
1. Managed Settings (Org-wide) 
   └─> 2. --agents CLI Flag (Session-level)
        └─> 3. Project (.claude/agents/)
             └─> 4. User Personal (~/.claude/agents/)
                  └─> 5. Plugin (plugin-name:agent-name)
```

---

## YAML Frontmatter Reference

```yaml
---
name: code-improver
description: Scans modified files and suggests readability and security improvements.
tools: Read, Grep, Glob, Bash    # Specific tool allowlist
disallowedTools: Write, Edit     # Explicit tool denylist
model: sonnet                    # sonnet | opus | haiku | inherit
permissionMode: acceptEdits      # default | acceptEdits | dontAsk | bypassPermissions
isolation: worktree              # Runs subagent inside temporary isolated git worktree
skills:                          # Preloads full skill markdown at startup
  - refactoring-patterns
mcpServers:                      # Inline MCP servers scoped ONLY to this subagent
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
---
```

---

## Related Knowledge Nodes

- **Concepts**: [[Subagent Architecture]], [[Subagent Context Isolation]], [[Subagent Worktree Isolation]], [[Agent Skills Architecture]], [[Orchestrator Skill Pattern]].
- **Entities**: [[Claude Code]], [[Anthropic]].
