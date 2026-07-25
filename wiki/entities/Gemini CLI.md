---
title: Gemini CLI
date: 2026-06-28
tags:
  - entity
  - tool
  - agent
---

# Gemini CLI

An open-source AI assistant by Google that brings the Gemini model into the terminal as an agentic command-line tool.

## Features
- **Extensibility**: Supports custom slash commands (e.g., `/test:gen`), MCP servers, and on-the-fly helper script generation. Also implements the open Agent Skills standard (`.agents/skills/`) to package on-demand expertise, utilizing progressive disclosure and explicit UI consent for activation (see [[Gemini CLI Skills]]).
- **Context Management**: Uses `GEMINI.md` as its [[Persistent Instruction File]], and explicit `@` file/image references. Features explicit memory addition (`/memory add`).
- **Safety and Reversibility**: Includes checkpointing (`/restore`) to snapshot files before modification, acting as an AI-specific undo button. Can operate in YOLO mode for auto-approvals.
- **System Assistant**: Beyond coding, it is frequently used as a "smart shell" to troubleshoot system configs, parse logs, and modify the OS environment.

See [[Gemini CLI Tips & Tricks]] for advanced usage patterns.
