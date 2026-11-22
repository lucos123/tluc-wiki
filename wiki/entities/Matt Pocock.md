---
title: "Matt Pocock"
date: 2026-11-18
tags:
  - entity
  - person
  - ai-engineering
  - context-engineering
---

# Matt Pocock

**Matt Pocock** (`@mattpocockuk`) is an educator, developer tooling builder, and creator of **AI Hero** (`aihero.dev`), Course Video Manager (`cvm`), **Sandcastle**, and open-source agent skills (`mattpocock/skills`). Formerly Turborepo DevRel at Vercel, he publishes practical architectures for multi-repo coding agents and personal knowledge systems.

## Core Architectural Contributions

- **[Home Repo Pattern](../concepts/Home%20Repo%20Pattern.md)** ([The Home Repo The effortless multi-repo agent setup](../sources/The%20Home%20Repo%20The%20effortless%20multi-repo%20agent%20setup.md)): Solves skill duplication and steering drift across multi-repo organizations (`20–40+` repos) by establishing a single central "home repository" (`personal-wiki`) housing versioned `.claude/skills/`, `settings.json`, `CLAUDE.md` / `AGENTS.md` repo pointer maps, and shared CLI tooling from which every agent session launches.
- **Karpathy-Style [llm-wiki](../concepts/llm-wiki.md) With Unified CLI Tooling**: Implements an operational business & personal knowledge base inside `personal-wiki/wiki/` (`audience/`, `me/`, `people/`, `research/`, `index.md`, `log.md`) driven by a single discoverable **`wiki <source> <verb>`** CLI uniting Gmail, Slack, Discord, X, YouTube, GitHub, Google Calendar, AI Hero CMS, Todoist, Cold Turkey, Vercel Reports, Buffer, and automated editing workflows.

## Ingested Works

- [The Home Repo The effortless multi-repo agent setup](../sources/The%20Home%20Repo%20The%20effortless%20multi-repo%20agent%20setup.md) (`2026-11-12`): 8m 53s walkthrough of the Home Repo setup, `CLAUDE.md` multi-repo pointers, automated git worktrees, `>40` repo scaling via progressive disclosure, and his `personal-wiki` CLI ecosystem.

## Related Concepts

- [Home Repo Pattern](../concepts/Home%20Repo%20Pattern.md)
- [Monorepo Context Engineering](../concepts/Monorepo%20Context%20Engineering.md)
- [llm-wiki](../concepts/llm-wiki.md)
- [Progressive Disclosure](../concepts/Progressive%20Disclosure.md)
- [Agent Onboarding Files](../concepts/Agent%20Onboarding%20Files.md)
- [Git Worktree Isolation](../concepts/Git%20Worktree%20Isolation.md)
