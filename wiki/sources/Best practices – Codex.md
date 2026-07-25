---
title: "Summary: Best practices – Codex"
date: 2026-06-28
tags:
  - best-practices
  - codex
  - agentic-design
source: "[[raw/Best practices – Codex.md]]"
---

# Best practices – Codex

## Summary
A guide to getting the most out of OpenAI's [[Codex]] across its CLI, IDE extension, and app. It focuses on treating the agent as a teammate that you configure and improve over time, utilizing `AGENTS.md`, MCP, and automations.

## Key Insights
- **Strong Prompting Structure**: A good default prompt includes Goal, Context (using `@` mentions), Constraints, and "Done when" (verification criteria).
- **Persistent Guidance**: Use `AGENTS.md` (see [[Persistent Instruction File]]) as an open-format README for agents. It should include repo layout, build/test commands, conventions, and verification steps. Keep it practical and update it during retrospectives when Codex makes mistakes.
- **Automations and Skills**: Turn repeatable work (like log triage, PR review, release notes) into Skills (`SKILL.md`). Once a workflow is stable, use Automations to run it on a schedule in the background.
- **MCP for External Context**: Connect Codex to external tools (databases, issue trackers) using the Model Context Protocol (MCP) so you don't have to copy-paste live information.
- **Session Controls**: Keep one thread per coherent unit of work. Fork only when branching. Use subagents for bounded work to keep the main thread focused. Avoid the common mistake of one thread per project.

## Associated Entities & Concepts
- [[Codex]]
- [[Persistent Instruction File]]
- [[Harness Engineering]]
