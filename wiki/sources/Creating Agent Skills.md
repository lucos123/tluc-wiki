---
title: Creating Agent Skills
date: 2026-06-28
tags:
  - source
  - documentation
  - gemini-cli
source: "raw/articles/geminicli/creating-agent-skills.md"
---

# Creating Agent Skills

**Source File**: [raw/articles/geminicli/creating-agent-skills.md](../../raw/articles/geminicli/creating-agent-skills.md)

This document covers both the automated and manual workflows for creating Agent Skills for the [Gemini CLI](../entities/Gemini%20CLI.md), adhering to the `agentskills.io` standard.

## Key Concepts

- **Automated Creation**: 
  - The `skill-creator` is a built-in meta-skill. A user can simply prompt Gemini (e.g., "Create a new skill called 'code-reviewer'...") and the agent will automatically generate the directory, scaffold the `SKILL.md` with correct frontmatter, and create standard subdirectories (`scripts/`, `references/`, `assets/`).
- **Manual Structure**:
  - `SKILL.md`: Required instructions and metadata.
  - `scripts/`: Optional executable scripts.
  - `references/`: Optional static documentation.
  - `assets/`: Optional templates.
- **Trigger Mechanics**: The `description` field in the frontmatter is critical, as it is the sole signal Gemini uses to decide whether to activate the skill.
- **Advanced Development Scripts**: The core Gemini package includes Node.js scripts for developing skills:
  - `init_skill.cjs`: Initializes boilerplate.
  - `validate_skill.cjs`: Lints the skill structure.
  - `package_skill.cjs`: Packages the directory into a `.skill` zip file for distribution.
