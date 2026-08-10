---
title: "Agent Skills in the SDK"
date: 2026-08-10
tags:
  - source
  - agent-sdk
  - skills
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/agent-architecture-subagents-workflows/agent-sdk-skills.md]]"
url: "https://code.claude.com/docs/en/agent-sdk-skills.md"
---

# Agent Skills in the SDK

**URL**: https://code.claude.com/docs/en/agent-sdk-skills.md  
**Source File**: [[raw/articles/claude-code/agent-architecture-subagents-workflows/agent-sdk-skills.md]]  

---

## Executive Summary

This official Anthropic guide details how to integrate and manage **Agent Skills** programmatically using the Claude Agent SDK (Python & TypeScript).

---

## Key SDK Integration Rules

### 1. Filesystem Artifact Requirement
Unlike Subagents (which can be declared dynamically in code), Skills **must** exist on disk as `SKILL.md` files inside `.claude/skills/` directories.

### 2. File Discovery & Configuration
Skills are discovered at process initialization based on `setting_sources`:
```python
options = ClaudeAgentOptions(
    cwd=os.getcwd(),
    setting_sources=["user", "project"], # Discovers ~/.claude/skills & .claude/skills
    skills="all", # Enables all discovered skills
    allowed_tools=["Read", "Write", "Bash"]
)
```

### 3. Skill Selection Filtering
- `skills="all"`: Enable all discovered skills.
- `skills=["pdf", "docx"]`: Enable a specific subset of skills.
- `skills=[]`: Hide all skills from the session context.

### 4. SDK Tool Restriction Caveat
> [!IMPORTANT]
> The `allowed-tools` YAML frontmatter field in `SKILL.md` is **ignored** when running via the SDK. Tool authorization must be managed centrally via `allowed_tools` and `permission_mode` in `ClaudeAgentOptions`.

---

## Related Knowledge Nodes

- **Concepts**: [[SDK Agent Skills]], [[Agent Skills Architecture]], [[Agent SDK Architecture]], [[Progressive Disclosure]].
- **Entities**: [[Claude Code]], [[Anthropic]].
