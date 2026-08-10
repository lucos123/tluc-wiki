---
title: "Orchestrate subagents at scale with dynamic workflows"
date: 2026-08-10
tags:
  - source
  - workflows
  - ultracode
  - harness-engineering
  - graph-engineering
  - claude-code
source: "[[raw/articles/claude-code/agent-architecture-subagents-workflows/workflows.md]]"
url: "https://code.claude.com/docs/en/workflows.md"
---

# Orchestrate subagents at scale with dynamic workflows

**URL**: https://code.claude.com/docs/en/workflows.md  
**Source File**: [[raw/articles/claude-code/agent-architecture-subagents-workflows/raw/articles/claude-code/agent-architecture-subagents-workflows/workflows.md]]  

---

## Executive Summary

This official Anthropic guide introduces **Dynamic Workflows** (`ultracode`) in [[Claude Code]].

Dynamic workflows shift multi-agent orchestration from turn-by-turn LLM reasoning into an executable, programmatic JavaScript script. This enables massive scaling (dozens to hundreds of agents per run) for large codebase audits, multi-file migrations, and deep research (`/deep-research`) without overwhelming context windows.

---

## Orchestration Paradigm Comparison

| Paradigm | What It Is | Who Controls Execution | Context Location | Scale Limits |
| --- | --- | --- | --- | --- |
| **Subagents** | Isolated worker spawned by model | LLM turn-by-turn | LLM context window | Few workers per turn |
| **Skills** | Modular prompt instructions | LLM following prompt | LLM context window | Turn-level guidance |
| **Agent Teams** | Lead agent supervising peers | Lead agent turn-by-turn | Shared task list | Handful of peer sessions |
| **Workflows** | Programmatic JS script | Background JS Runtime | Script variables | Dozens to 100+ agents |

---

## Key Workflow Triggers & Features

### 1. Bundled Workflow (`/deep-research`)
```bash
/deep-research What changed in the Node.js permission model between v20 and v22?
```
- Fans out web searches across multiple angles.
- Adversarially cross-checks claims across sources.
- Synthesizes a cited research report.

### 2. Prompt Keyword Trigger (`ultracode:`)
Prefixing a prompt with `ultracode:` instructs Claude to generate and execute a JS workflow script instead of turn-by-turn execution:
```text
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

### 3. Session Effort Level (`/effort ultracode`)
Setting `/effort ultracode` locks the session at `xhigh` reasoning effort and automatically plans dynamic workflows for all substantive tasks.

### 4. Workflow Storage (`.claude/workflows/`)
Workflows can be saved (`s` in `/workflows`) to `.claude/workflows/` (Project) or `~/.claude/workflows/` (Personal) for repeatable execution.

---

## Related Knowledge Nodes

- **Concepts**: [[Dynamic Workflows]], [[Ultracode Mode]], [[Subagent Architecture]], [[Graph Engineering]], [[Orchestrator Skill Pattern]].
- **Entities**: [[Claude Code]], [[Anthropic]].
