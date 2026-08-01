---
title: Responses API
date: 2026-08-01
tags:
  - concept
  - ai-models
  - tool
  - openai
---

# Responses API

The **Responses API** (`v1/responses`) is [[OpenAI]]'s next-generation agent endpoint that succeeds the legacy Chat Completions API.

## Key Features

- **Native Tool Integration**: Built-in support for web search, file search, image generation, code interpreter, hosted shell, apply patch, skills, computer use, tool search, and Model Context Protocol ([[Model Context Protocol|MCP]]).
- **Multi-Agent Coordination**: Native orchestration for subagent swarms and parallel execution workflows (`ultra` reasoning mode).
- **Deprecation of Chat Completions**: Standard CLI environments like `[[Codex]]` are transitioning exclusively to the Responses API for agent tool calls.

See [[OpenAI Models & Codex Integration Guide]] and [[Codex]].
