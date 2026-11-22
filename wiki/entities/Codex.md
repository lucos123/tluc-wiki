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
- Relies heavily on [Persistent Instruction File](../concepts/Persistent%20Instruction%20File.md)s via `AGENTS.md` for project conventions.
- Configurable default model via `config.toml` (`model = "gpt-5.6"`), CLI flags (`codex -m gpt-5.6-sol`), and environment settings.
- Powered by the [GPT-5.6](GPT-5.6.md) family ([Sol](../sources/GPT-5.6%20Sol%20Model%20API%20Reference.md), [GPT-5.6 Terra](GPT-5.6%20Terra.md), [GPT-5.6 Luna](GPT-5.6%20Luna.md)) and `gpt-5.3-codex-spark`.
- **Reasoning & Subagent Modes**: Supports `low`, `medium`, `high`, `xhigh`, `max`, and **`ultra`** (multi-agent mode spawning 4 to 16 parallel subagents for complex tasks).
- Supports Model Context Protocol (MCP) and transitioning to the [Responses API](../concepts/Responses%20API.md) for hosted shell and computer use.
- Allows packaging repeated workflows into reusable Skills (`SKILL.md`) following the open Agent Skills standard. Uses progressive disclosure and hierarchical discovery (`.agents/skills/`) to manage context efficiently (see [Codex Skills](../sources/Codex%20Skills.md)).
- **Deprecations**: Legacy `gpt-5.4` and `gpt-5.4-mini` models retire on August 31, 2026 for ChatGPT sign-in users.

See [OpenAI Models & Codex Integration Guide](../sources/OpenAI%20Models%20%26%20Codex%20Integration%20Guide.md) and [Best practices – Codex](../sources/Best%20practices%20%E2%80%93%20Codex.md) for more details.
