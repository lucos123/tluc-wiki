---
title: "Agent Onboarding Files"
date: 2026-08-04
tags:
  - concept
  - context-engineering
  - harness-engineering
source: "[[Emerging Markdown Formats That Shape Coding Agent Behavior]]"
---

# Agent Onboarding Files

**Agent Onboarding Files** are persistent markdown instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) that serve as a "README for agents", allowing AI coding agents to discover repository structure, build commands, test suites, and coding constraints upon launching a task.

Detailed by [[Bilgin Ibryam]] in [[Emerging Markdown Formats That Shape Coding Agent Behavior]].

---

## Standard vs. Vendor-Native Formats

- **`AGENTS.md`**: Neutral cross-tool standard supported by OpenAI Codex, Cursor, Cline, Gemini CLI, Copilot, and OpenCode.
- **`CLAUDE.md` & `.claude/rules/`**: Native standing instructions for Anthropic's Claude Code.
- **`GEMINI.md`**: Hierarchical context configuration for Google's Gemini CLI.
- **`.github/copilot-instructions.md`**: Native instructions for GitHub Copilot.

---

## Distinction from Skills

- **Onboarding Files (`AGENTS.md`)**: Describe *standing rules, constraints, and project context* that remain true across all tasks.
- **Skill Files (`SKILL.md`)**: Describe a *repeatable procedure* invoked for a specific, discrete task.

See [[Metacode]] and [[Context Engineering]].
