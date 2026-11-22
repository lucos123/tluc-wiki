---
title: "Orchestrate teams of Claude Code sessions"
date: 2026-08-10
tags:
  - source
  - agent-teams
  - harness-engineering
  - parallelism
  - claude-code
source: "raw/articles/claude-code/agent-architecture-subagents-workflows/agent-teams.md"
url: "https://code.claude.com/docs/en/agent-teams.md"
---

# Orchestrate teams of Claude Code sessions

**URL**: https://code.claude.com/docs/en/agent-teams.md  
**Source File**: [raw/articles/claude-code/agent-architecture-subagents-workflows/agent-teams.md](../../raw/articles/claude-code/agent-architecture-subagents-workflows/agent-teams.md)  

---

## Executive Summary

This official Anthropic guide details **Agent Teams**, an experimental multi-session orchestration system in [Claude Code](../entities/Claude%20Code.md) (enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

Unlike Subagents (which only report summaries back to a single parent session), Agent Teams consist of a **Team Lead** and independent **Teammates** that share a unified task backlog (`~/.claude/tasks/`) and communicate directly via peer-to-peer mailboxes (`~/.claude/teams/`).

---

## Key Agent Teams Mechanics

### 1. Component Topography
- **Team Lead**: Primary Claude session coordinating project goals and task assignments.
- **Teammates**: Peer Claude sessions claiming tasks and executing code edits independently.
- **Shared Task Backlog**: Dependency-aware task list supporting auto-unblocking and race-condition file locking.
- **Inter-Agent Mailbox**: Peer-to-peer JSON mailbox system (`~/.claude/teams/{team-name}/inboxes/{agent-name}.json`).

### 2. Display Modes (`teammateMode`)
- **In-Process Mode**: Teammates run in main terminal; navigate via arrow keys and view/message teammates directly.
- **Split-Pane Mode (`tmux` / `iTerm2`)**: Visual side-by-side terminal panes for real-time monitoring.

### 3. Governance & Quality Gates
- **Plan Approval Gate**: Teammates can be locked in read-only plan mode until the Lead Agent reviews and approves their implementation plan.
- **Lifecycle Hooks**: Quality gates enforced via `TeammateIdle`, `TaskCreated`, and `TaskCompleted` hooks.

---

## Related Knowledge Nodes

- **Concepts**:
  - [Agent Teams Architecture](../concepts/Agent%20Teams%20Architecture.md)
  - [Inter-Agent Messaging](../concepts/Inter-Agent%20Messaging.md)
  - [Parallel Agent Architecture](../concepts/Parallel%20Agent%20Architecture.md)
  - [Subagent Architecture](../concepts/Subagent%20Architecture.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
