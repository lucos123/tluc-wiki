---
title: "Agent Onboarding Files"
date: 2026-08-04
tags:
  - concept
  - context-engineering
  - harness-engineering
source: "wiki/sources/Emerging Markdown Formats That Shape Coding Agent Behavior.md"
---

# Agent Onboarding Files

**Agent Onboarding Files** are persistent markdown instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) that serve as a "README for agents", allowing AI coding agents to discover repository structure, build commands, test suites, and coding constraints upon launching a task.

Detailed by [Bilgin Ibryam](../entities/Bilgin%20Ibryam.md) in [Emerging Markdown Formats That Shape Coding Agent Behavior](../sources/Emerging%20Markdown%20Formats%20That%20Shape%20Coding%20Agent%20Behavior.md).

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
- **Multi-Repo Routing Hubs ([Home Repo Pattern](Home%20Repo%20Pattern.md))**: As demonstrated by [Matt Pocock](../entities/Matt%20Pocock.md) in [The Home Repo The effortless multi-repo agent setup](../sources/The%20Home%20Repo%20The%20effortless%20multi-repo%20agent%20setup.md), central onboarding files can also hold `## Other Repos` pointer tables, `GLOSSARY-MAP.md` domain disambiguation links, and tiered category indexes (`docs/FRONTEND.md`, `docs/BACKEND.md`) via [Progressive Disclosure](Progressive%20Disclosure.md) so a single agent session navigates dozens or hundreds of repositories seamlessly.

See [Metacode](Metacode.md), [Context Engineering](Context%20Engineering.md), and [Home Repo Pattern](Home%20Repo%20Pattern.md).
