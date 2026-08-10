---
title: "SDK Agent Skills"
date: 2026-08-10
tags:
  - concept
  - agent-sdk
  - skills
  - harness-engineering
  - claude-code
source: "[[Agent Skills in the SDK]]"
---

# SDK Agent Skills

**SDK Agent Skills** is the programmatic mechanism within the Claude Agent SDK for discovering, filtering, and mounting filesystem-based [[Agent Skills Architecture|Agent Skills]] into custom agent applications.

---

## SDK Skill Lifecycle

```mermaid
graph TD
    Config["ClaudeAgentOptions(setting_sources=['user', 'project'])"] --> Discover["1. Filesystem Discovery (~/.claude/skills & .claude/skills)"]
    Discover --> Filter["2. Filter via skills=['pdf', 'docx'] or 'all'"]
    Filter --> InitStream["3. SDK Yields SystemMessage(init, skills=[...])"]
    InitStream --> Execute["4. Model Autonomously Invokes Skill Tool"]
```

## Key Architectural Constraints

1. **Strict Filesystem Binding**: Skills cannot be registered inline as in-memory code objects; they must be saved on disk as `SKILL.md` files.
2. **Central Tool Authorization**: `allowed-tools` inside `SKILL.md` is ignored by the SDK; permissions must be declared in `ClaudeAgentOptions.allowed_tools`.

See [[Agent Skills in the SDK]], [[Agent Skills Architecture]], and [[Agent SDK Architecture]].
