---
title: Codex Skills
date: 2026-06-28
tags:
  - source
  - documentation
  - agentic-design
  - codex
source: "raw/articles/openai/codex-skills.md"
---

# Codex Skills

**Source File**: [raw/articles/openai/codex-skills.md](../../raw/articles/openai/codex-skills.md)

This document outlines how OpenAI's [Codex](../entities/Codex.md) utilizes Agent Skills to package reusable workflows, scripts, and resources. Like [Claude Code Skills](Claude%20Code%20Skills.md), it builds upon the open `agentskills.io` standard.

## Key Concepts

- **Progressive Disclosure**: To save on context window usage, Codex only loads the `name`, `description`, and file path of available skills into its initial prompt (capped at 2% of context). The full `SKILL.md` is only read if Codex decides the skill is relevant.
- **Invocation**: 
  - **Explicit**: Using `$` or `/skills` in the prompt.
  - **Implicit**: Codex automatically matches the user's task to a skill's description.
- **Skill Structure**: A directory containing `SKILL.md`, and optionally `scripts/`, `references/`, `assets/`, and an `agents/openai.yaml` for UI metadata and dependencies (like requiring specific MCP servers).
- **Skill Discovery Hierarchy**: Skills can be defined in multiple scopes:
  - `REPO`: `.agents/skills/` scanned up to the repository root.
  - `USER`: `~/.agents/skills/` for personal workflows.
  - `ADMIN` and `SYSTEM`: For machine-wide or bundled skills.
- **Creation via Demonstration**: Using Codex's "Record & Replay" feature, users can demonstrate a workflow, and Codex will automatically draft a reusable skill from the steps. Alternatively, use `$skill-creator`.
- **Distribution via Plugins**: While skill folders are best for local or repo-scoped use, they can be bundled with app mappings and MCP servers into Plugins for wider distribution.

## Synthesis Notes

The adoption of the open Agent Skills standard by both [Codex](../entities/Codex.md) and [Claude Code](../entities/Claude%20Code.md) highlights a major trend in [Harness Engineering](../concepts/Harness%20Engineering.md). Monolithic [Persistent Instruction Files](../concepts/Persistent%20Instruction%20File.md) (like `AGENTS.md`) are increasingly being supplemented or replaced by modular, on-demand skill directories. Codex's addition of "Progressive Disclosure" and UI metadata via `openai.yaml` shows an ecosystem evolving beyond simple text prompts into structured, installable agent capabilities.
