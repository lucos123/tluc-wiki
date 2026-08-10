---
title: "Subagents in the SDK"
date: 2026-08-10
tags:
  - source
  - agent-sdk
  - subagents
  - harness-engineering
  - claude-code
source: "[[raw/articles/claude-code/agent-architecture-subagents-workflows/agent-sdk-subagents.md]]"
url: "https://code.claude.com/docs/en/agent-sdk-subagents.md"
---

# Subagents in the SDK

**URL**: https://code.claude.com/docs/en/agent-sdk-subagents.md  
**Source File**: [[raw/articles/claude-code/agent-architecture-subagents-workflows/agent-sdk-subagents.md]]  

---

## Executive Summary

This official Anthropic guide details how to programmatically define, configure, and orchestrate specialized **Subagents** using the Claude Agent SDK (Python & TypeScript).

Programmatic subagent definitions (`AgentDefinition`) allow applications to dynamically instantiate domain-specific worker agents with tailored system prompts, restricted tool pools, model overrides, and background execution settings.

---

## Programmatic Definition Schema

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Agent"],
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code review specialist.",
            prompt="You are a code review specialist...",
            tools=["Read", "Grep", "Glob"], # Read-only tool pool
            model="sonnet",                 # Model override
            background=True                 # Non-blocking async execution
        )
    }
)
```

---

## Context Isolation & Inheritance Matrix

| Included in Subagent Context | Excluded from Subagent Context |
| --- | --- |
| Subagent System Prompt (`AgentDefinition.prompt`) | Parent session conversation history |
| User Prompt passed via `Agent` tool | Parent session intermediate tool call results |
| Project `CLAUDE.md` instructions | Parent session system prompt |
| Dedicated tool pool (`tools` option) | Unpreloaded skills (unless in `skills` list) |

---

## Related Knowledge Nodes

- **Concepts**: [[SDK Subagents]], [[Subagent Architecture]], [[Subagent Context Isolation]], [[Agent SDK Architecture]].
- **Entities**: [[Claude Code]], [[Anthropic]].
