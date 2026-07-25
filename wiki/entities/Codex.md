---
title: Codex
date: 2026-06-28
tags:
  - entity
  - tool
  - agent
---

# Codex

An AI coding agent platform developed by OpenAI, accessible via CLI, IDE extension, and app. 

## Features
- Relies heavily on [[Persistent Instruction File]]s via `AGENTS.md` for project conventions.
- Supports Model Context Protocol (MCP) for connecting to external systems.
- Allows packaging repeated workflows into reusable Skills (`SKILL.md`) following the open Agent Skills standard. Uses progressive disclosure and hierarchical discovery (`.agents/skills/`) to manage context efficiently (see [[Codex Skills]]).
- Utilizes Subagents for bounded tasks (like exploration or testing) while preserving the main agent thread.

See [[Best practices – Codex]] for more details on effective usage.
