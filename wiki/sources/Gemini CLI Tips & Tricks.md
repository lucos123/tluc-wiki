---
title: "Summary: Gemini CLI Tips & Tricks"
date: 2026-06-28
tags:
  - best-practices
  - gemini-cli
  - agentic-design
source: "[[raw/gemini-cli-tips-tricks.md]]"
---

# Gemini CLI Tips & Tricks

## Summary
A compilation of ~30 pro-tips for using the open-source [[Gemini CLI]] by Google. It highlights the CLI's flexibility as a conversational, agentic command-line tool capable of system troubleshooting, tool creation, and multi-modal interactions.

## Key Insights
- **Persistent Context**: Uses `GEMINI.md` to load project-specific instructions automatically (see [[Persistent Instruction File]]).
- **Customization and Extensibility**: Create custom slash commands (e.g., `/test:gen`) mapped to prompt templates. Connect external tools and services via MCP servers (e.g., Google Docs, Figma, databases).
- **Memory & Checkpointing**: Use `/memory add` to store long-term facts across sessions. Enable checkpointing (`--checkpointing`) to take snapshots of files before edits, allowing an instant `/restore` (undo) if changes go wrong.
- **Explicit Context with `@`**: Use `@` to reference files, directories, and even images for explicit context injection, reducing hallucinations.
- **On-the-Fly Tool Creation**: Gemini CLI can write its own temporary helper scripts (e.g., in Python or Node.js) and execute them to solve specific tasks.
- **YOLO Mode**: Auto-approve tool actions for faster execution when the agent is trusted.
- **System Troubleshooting**: Use Gemini CLI outside of code projects to fix shell configs (`.bashrc`), diagnose system errors, or run headless commands in CI pipelines.

## Associated Entities & Concepts
- [[Gemini CLI]]
- [[Persistent Instruction File]]
- [[Harness Engineering]]
