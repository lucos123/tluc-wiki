---
title: "Summary: 12 Agentic Harness Patterns from Claude Code"
date: 2026-06-28
tags:
  - patterns
  - agentic-design
  - claude-code
source: "[[raw/12-agentic-harness-patterns-from-claude-code.md]]"
---

# 12 Agentic Harness Patterns from Claude Code

## Summary
This article outlines 12 design patterns extracted from the leaked source code of Anthropic's [[Claude Code]]. The patterns are categorized into Memory & Context, Workflow & Orchestration, Tools & Permissions, and Automation, demonstrating how production-grade agents rely heavily on their harness.

## The Patterns
### Memory and Context
1. **Persistent Instruction File**: Project-level configuration loaded at session start.
2. **Scoped Context Assembly**: Dynamically loading instructions based on directory scope.
3. **Tiered Memory**: Organizing memory into distinct layers (e.g., 200-line index in context, topic files on demand, transcripts on disk).
4. **Dream Consolidation**: Background processing to deduplicate, prune, and reorganize agent memory ("autoDream").
5. **Progressive Context Compaction**: Applying multiple stages of compression as context ages (e.g., Microcompact, Autocompact).

### Workflow and Orchestration
6. **Explore-Plan-Act Loop**: Forcing the agent to map the codebase and plan before getting write permissions.
7. **Context-Isolated Subagents**: Spawning separate agents with restricted context/tools to avoid pollution.
8. **Fork-Join Parallelism**: Spawning multiple subagents in parallel across isolated worktrees.

### Tools and Permissions
9. **Progressive Tool Expansion**: Starting with a minimal default toolset and activating others on demand.
10. **Command Risk Classification**: Pre-parsing commands to deterministically gate dangerous actions.
11. **Single-Purpose Tool Design**: Providing constrained tools (e.g., `FileEditTool`) instead of raw shell access.

### Automation
12. **Deterministic Lifecycle Hooks**: Running necessary shell commands automatically at specific lifecycle points outside the LLM prompt.

## Associated Entities & Concepts
- [[Claude Code]]
- [[Harness Engineering]]
