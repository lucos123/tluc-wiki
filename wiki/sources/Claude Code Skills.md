---
title: Claude Code Skills
date: 2026-06-28
tags:
  - source
  - documentation
  - agentic-design
  - claude-code
source: "[[raw/cc-skills.md]]"
---

# Claude Code Skills

**Source File**: [[raw/cc-skills.md]]

This documentation outlines how to extend [[Claude Code]]'s capabilities by creating custom skills. Skills represent a major evolution in [[Harness Engineering]], moving from static instruction files like [[Persistent Instruction File|CLAUDE.md]] to modular, dynamically loaded capabilities.

## Key Concepts

- **Agent Skills Standard**: Claude Code skills are based on the open standard from `agentskills.io` but extend it with proprietary features for invocation control, subagent execution, and context injection.
- **Dynamic Context Injection**: Skills can execute shell commands (e.g., `!`git diff HEAD``) before Claude sees the prompt, seamlessly injecting live environment data directly into the LLM context.
- **Invocation Control**:
  - `disable-model-invocation: true`: Ensures only the user can trigger a skill manually (for workflows with side effects like deploying).
  - `user-invocable: false`: Ensures only Claude can use it (useful for background knowledge or internal context).
- **Subagent Execution**: Setting `context: fork` allows the skill to be run inside an isolated subagent (like an `Explore` or `Plan` agent) to protect the main session's context window.
- **Bundled Skills**: Claude Code ships with prompt-based bundled skills like `/run`, `/verify`, and `/run-skill-generator` which automatically build and run projects without falling back to just unit tests.
- **Pre-approved Tools**: The `allowed-tools` frontmatter field allows skills to bypass normal security prompts for specific commands, assuming the user has trusted the workspace.

## Synthesis Notes
The transition from large, monolithic context files to modular `SKILL.md` directories is a significant pattern in the "Harness Engineering" landscape. By only loading a skill's body into context when it is invoked, systems like Claude Code can maintain a rich toolkit without exhausting the LLM's finite context window. Furthermore, wrapping subagents inside slash-command skills (via `context: fork`) makes multi-agent orchestration accessible directly from the CLI chat prompt.
