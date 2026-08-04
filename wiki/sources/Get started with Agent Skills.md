---
title: Get started with Agent Skills
date: 2026-06-28
tags:
  - source
  - documentation
  - gemini-cli
source: "[[raw/get-started-with-agent-skills.md]]"
---

# Get started with Agent Skills

**Source File**: [[raw/get-started-with-agent-skills.md]]

This tutorial outlines how to manually create a new Agent Skill for the [[Gemini CLI]], using an "API Auditor" skill as a practical example.

## Key Concepts

- **Directory Structure**: A skill is a folder (e.g., `.gemini/skills/api-auditor/`) containing a `SKILL.md` file and optional bundled scripts (e.g., `scripts/audit.js`).
- **`SKILL.md` Requirements**: 
  - Must be named exactly `SKILL.md` (case-sensitive).
  - Must contain YAML frontmatter with `name:` and `description:` at the very top of the file.
  - The `name:` field in the frontmatter determines the skill's identity, regardless of the folder name.
- **Discovery Quirks**: 
  - Workspace skills only load if the workspace folder is marked as trusted (via `/trust`).
  - `SKILL.md` must be at the root of the `.gemini/skills/` directory or exactly one sub-directory deep. Deeper nesting is ignored.
- **Execution Flow**: When a user prompt matches the skill's description, the Gemini agent implicitly triggers the `activate_skill` tool, prompts the user for consent, and then uses the `run_shell_command` tool to execute the bundled script (e.g., `node .gemini/skills/api-auditor/scripts/audit.js <url>`).
- **Automated Alternative**: Users can prompt the built-in `skill-creator` to scaffold this boilerplate automatically.
