---
title: "Agent SDK Architecture"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - agent-sdk
  - claude-code
source: "wiki/sources/How the agent loop works.md"
---

# Agent SDK Architecture

The **Agent SDK Architecture** is the programmatic framework provided by Anthropic (`@anthropic-ai/claude-agent-sdk` for TypeScript and `claude_agent_sdk` for Python) allowing developers to embed the autonomous agent loop directly into custom enterprise software.

---

## Core Infrastructure Pillars

1. **Embedded Binary**: Bundles native agent binary runtimes, removing external dependencies.
2. **Tool Execution Engine**: Handles parallel concurrent execution for read tools (`Read`, `Glob`, `Grep`) and sequential execution for modifying tools (`Edit`, `Write`, `Bash`).
3. **Session Persistence & Mirroring**: Supports external transcript storage (Redis, S3, PostgreSQL) for multi-tenant scaling and pause/resume capabilities.
4. **Fine-Grained Permissions**: Evaluates `allowed_tools`, `disallowed_tools`, and `permission_mode` (`"default"`, `"acceptEdits"`, `"plan"`, `"dontAsk"`, `"auto"`, `"bypassPermissions"`).

See [How the agent loop works](../sources/How%20the%20agent%20loop%20works.md) and [Agent Loop Lifecycle](Agent%20Loop%20Lifecycle.md).
