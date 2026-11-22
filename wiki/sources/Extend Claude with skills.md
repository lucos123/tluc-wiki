---
title: "Extend Claude with skills"
date: 2026-08-10
tags:
  - source
  - skills
  - harness-engineering
  - context-engineering
  - claude-code
source: "raw/articles/claude-code/agent-architecture-subagents-workflows/skills.md"
url: "https://code.claude.com/docs/en/skills.md"
---

# Extend Claude with skills

**URL**: https://code.claude.com/docs/en/skills.md  
**Source File**: [raw/articles/claude-code/agent-architecture-subagents-workflows/skills.md](../../raw/articles/claude-code/agent-architecture-subagents-workflows/skills.md)  

---

## Executive Summary

This official Anthropic guide details how to create, configure, and manage **Agent Skills** in [Claude Code](../entities/Claude%20Code.md). Based on the open [Agent Skills](https://agentskills.io) standard, skills extend Claude's toolset with custom instructions, workflows, and dynamic context.

Unlike `CLAUDE.md` instructions (which stay permanently in the context window), skill bodies load **on-demand** using [Progressive Disclosure](../concepts/Progressive%20Disclosure.md), drastically saving tokens until the skill is actually invoked.

---

## Key Skill Features & Frontmatter Reference

### 1. Hierarchy & Resolution Order
```
Enterprise/Managed Settings -> Personal (~/.claude/skills/) -> Project (.claude/skills/) -> Nested (apps/web/.claude/skills/)
```
- Higher tiers override lower tiers.
- Custom project/personal skills override bundled skills with matching names.
- Nested skills produce directory-qualified commands (`/apps/web:deploy`).

### 2. Frontmatter Control Parameters

```yaml
---
name: deploy
description: Deploy application to staging
disable-model-invocation: true # Only user can trigger via /deploy
user-invocable: true            # Appears in / menu
allowed-tools: Bash(git push *) # Pre-approves tool execution during invocation turn
model: claude-3-5-haiku-20241022# Temporary turn model override
effort: max                    # Temporary effort override
context: fork                  # Executes skill in dedicated subagent context
---
```

### 3. Dynamic Context Injection (`!`)
Inline shell execution dynamically populates content before Claude sees the prompt:
```markdown
## Current Diff
!`git diff HEAD`
```

---

## Related Knowledge Nodes

- **Concepts**:
  - [Agent Skills Architecture](../concepts/Agent%20Skills%20Architecture.md)
  - [Dynamic Context Injection](../concepts/Dynamic%20Context%20Injection.md)
  - [Progressive Disclosure](../concepts/Progressive%20Disclosure.md)
  - [Claude Code Skills](Claude%20Code%20Skills.md)
  - [Orchestrator Skill Pattern](../concepts/Orchestrator%20Skill%20Pattern.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
