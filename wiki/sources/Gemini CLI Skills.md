---
title: Gemini CLI Skills
date: 2026-06-28
tags:
  - source
  - documentation
  - agentic-design
  - gemini-cli
source: "raw/articles/geminicli/gemini-overview-skills.md"
---

# Gemini CLI Skills

**Source File**: [raw/articles/geminicli/gemini-overview-skills.md](../../raw/articles/geminicli/gemini-overview-skills.md)

This document describes how the [Gemini CLI](../entities/Gemini%20CLI.md) implements Agent Skills, aligning with the open `agentskills.io` standard also used by [Claude Code](../entities/Claude%20Code.md) and [Codex](../entities/Codex.md).

## Key Concepts

- **Progressive Disclosure**: Gemini CLI scans discovery tiers at the start of a session but only injects the skill's name and description into the system prompt. The full instructions and resources (`SKILL.md`) are only loaded if the skill is explicitly activated.
- **Explicit Activation & Consent**: When Gemini identifies a relevant task, it must call the `activate_skill` tool. This triggers a UI confirmation prompt, requiring user consent before the agent is granted access to the skill's specific directory and its bundled assets.
- **Discovery Tiers**: Skills are discovered and prioritized across several locations:
  1. **Workspace**: `.gemini/skills/` or `.agents/skills/` (shared via version control).
  2. **User**: `~/.gemini/skills/` or `~/.agents/skills/` (personal workflows).
  3. **Extension**: Bundled within installed extensions.
  4. **Built-in**: Standard skills provided by the CLI.
- **Interoperability**: By checking the `.agents/skills/` alias, Gemini CLI maintains compatibility with skills built for other compliant agent platforms.
- **Management Utilities**: The CLI provides a robust set of commands (e.g., `/skills list`, `/skills enable`, `gemini skills install <git-url>`) to easily manage, link, and distribute specialized workflows.

## Synthesis Notes

The Gemini CLI's approach to Agent Skills reinforces a broader trend in [Harness Engineering](../concepts/Harness%20Engineering.md): shifting away from monolithic [Persistent Instruction Files](../concepts/Persistent%20Instruction%20File.md) (like `GEMINI.md`) towards on-demand, modular expertise. Its strict reliance on the `activate_skill` tool and user consent provides an interesting security model, ensuring that the LLM cannot arbitrarily access bundled scripts or templates without explicit user authorization.
