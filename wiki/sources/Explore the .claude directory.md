---
title: "Explore the .claude directory"
date: 2026-08-10
tags:
  - source
  - context-engineering
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/context-memory-rules/claude-directory.md]]"
url: "https://code.claude.com/docs/en/claude-directory.md"
---

# Explore the .claude directory

**URL**: https://code.claude.com/docs/en/claude-directory.md  
**Source File**: [[raw/articles/claude-code/context-memory-rules/claude-directory.md]]  

---

## Executive Summary

This interactive reference document maps the exact file tree architecture of the `.claude/` project directory and `~/.claude/` global home directory used by [[Claude Code]].

---

## The Complete `.claude/` Directory Map

```
your-project/
├── CLAUDE.md                    # Project instructions read every session (committed)
├── .mcp.json                    # Project MCP servers shared with team (committed)
├── .worktreeinclude             # Gitignored files to copy into new worktrees (committed)
└── .claude/
    ├── settings.json            # Enforced permissions, hooks, statusLine (committed)
    ├── settings.local.json      # Personal settings overrides (gitignored)
    ├── rules/                   # Topic-scoped rules (optionally path-gated)
    │   ├── testing.md
    │   └── api-design.md
    ├── skills/                  # Reusable Agent Skills (SKILL.md + assets)
    │   └── security-review/SKILL.md
    ├── agents/                  # Custom subagent definitions (subagent.md)
    │   └── refactor-expert.md
    ├── workflows/               # Multi-agent dynamic workflows (.md)
    └── output-styles/           # Custom system prompt formatting styles
```

---

## Global `~/.claude/` Home Directory Map

```
~/.claude/
├── CLAUDE.md                    # Global user preferences (loaded into all projects)
├── settings.json                # Global default permissions, model aliases, env vars
├── keybindings.json             # Custom keyboard shortcuts
├── rules/                       # Global rules applied to all repositories
├── skills/                      # Personal skills available across all projects
├── agents/                      # Global custom subagents
└── auto-memory/                 # Per-repository Auto Memory notes (MEMORY.md)
```

---

## Related Knowledge Nodes

- **Concepts**: [[Claude Directory Architecture]], [[Persistent Instruction File]], [[Path-Scoped Rules]], [[Auto Memory]], [[Subagent Context Isolation]].
- **Entities**: [[Claude Code]], [[Anthropic]].
