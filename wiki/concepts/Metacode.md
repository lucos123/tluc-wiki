---
title: "Metacode"
date: 2026-08-04
tags:
  - concept
  - context-engineering
  - harness-engineering
  - ai-sdlc
source: "[[Emerging Markdown Formats That Shape Coding Agent Behavior]]"
---

# Metacode

**Metacode** (or the *Metacode Layer*) is the structured taxonomy of version-controlled, agent-legible Markdown files (`AGENTS.md`, `SKILL.md`, `spec.md`, `ARCHITECTURE.md`, `MEMORY.md`) that sit alongside source code to guide AI coding agents.

Coined and detailed by [[Bilgin Ibryam]] in [[Emerging Markdown Formats That Shape Coding Agent Behavior]].

---

## Conceptual Overview

Historically, software intent, NFRs, architecture decisions, and operational playbooks lived scattered across Solution Architecture documents, ADRs, tickets, and Slack threads.

In an agent-ready repository, **metacode** brings all necessary project knowledge directly beside the codebase. When an AI agent reads both the source code and metacode, it functions as an **Intent Compiler** — translating human intent and architectural judgment directly into executable code changes.

---

## The 5 Categories of Metacode

1. **[[Agent Onboarding Files]]** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`): Standing rules, build commands, and constraints.
2. **Playbooks & Procedures** (`SKILL.md`): Portable, task-specific playbooks under the open Agent Skills standard.
3. **Spec & Plan Chains** (`spec.md`, `plan.md`, `tasks.md`): Versioned software design artifacts (e.g. [[GitHub Spec Kit]]).
4. **Domain Files** (`ARCHITECTURE.md`, `DESIGN.md`, `AUTH.md`, `REVIEW.md`): Specialized subsystem instructions.
5. **Durable Learned Context** (`MEMORY.md`): Auto-recorded machine memory following the [[Memory Promotion Path]].

---

## Relationship to Other Paradigms

- **[[Context Engineering]]**: Metacode is the primary vehicle for Context Engineering in software repositories.
- **[[Harness Engineering]]**: Metacode files configure the environment sandboxes and permissions of the agent harness.
- **[[Memory Architecture]]**: Metacode structures machine-local memory into long-term project rules.
