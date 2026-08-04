---
title: Managing Agent Skills
date: 2026-06-28
tags:
  - source
  - documentation
  - gemini-cli
source: "[[raw/managing-agent-skills.md]]"
---

# Managing Agent Skills

**Source File**: [[raw/managing-agent-skills.md]]

This document provides a guide on managing Agent Skills within the [[Gemini CLI]]. It expands upon the concepts introduced in [[Gemini CLI Skills]].

## Key Concepts

- **Discovery Tiers**: Skills load based on precedence: Workspace (`.gemini/skills/` or `.agents/skills/`) > User (`~/.gemini/skills/`) > Extension > Built-in. If multiple skills have the same name, the higher-precedence one wins.
- **In-Session Management**:
  - `/skills list [all|nodesc]`: View available expertise.
  - `/skills reload` (or `/skills refresh`): Hot-reload skills from disk without restarting the session.
  - `/skills disable <name>` / `/skills enable <name>`: Toggle skills.
- **Terminal Utilities**:
  - `gemini skills install <url>`: Installs a skill from a remote git repository or local `.skill` package. Defaults to user scope, can use `--scope workspace`.
  - `gemini skills link <path>`: Symlinks a local directory for development.
  - `gemini skills uninstall <name>`: Removes the skill.
- **Security & Consent**: Installation from URLs requires confirmation, and the agent must explicitly ask for activation consent every time a skill is triggered.
