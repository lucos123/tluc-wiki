---
title: "Progressive Disclosure"
date: 2026-08-04
tags:
  - concept
  - context-engineering
  - harness-engineering
source: "[[The new rules of context engineering for Claude 5 generation models]]"
---

# Progressive Disclosure

**Progressive Disclosure** is a context engineering architectural pattern where instructions, tool definitions, and skill playbooks are loaded on demand at the exact moment they are needed, rather than being stuffed upfront into the agent's system prompt.

Detailed by [[Thariq Shihipar]] in [[The new rules of context engineering for Claude 5 generation models]].

---

## Implementations in Agent Systems

1. **Deferred Tool Loading (`ToolSearch`)**: Tools (e.g. Task management tools) are declared in lightweight registries, and the agent uses a `ToolSearch` mechanism to load full tool schemas only when invoked.
2. **Skill Playbooks (`SKILL.md`)**: Specific procedures (e.g. verification, code review, migrations) are encapsulated in standalone skill files loaded dynamically when triggered by task intent.
3. **Hierarchical Context Trees**: Subsystem guidance is organized into nested `CLAUDE.md` or `AGENTS.md` files discovered as the agent navigates project subdirectories.

---

## Benefits

- **Token Economy**: Reduces standing system prompt token footprint by up to 80%.
- **Context Rot Prevention**: Prevents degradation of agent reasoning caused by large, noisy prompt payloads.

See [[Context Engineering]], [[Metacode]], and [[Unhobbling Claude]].
