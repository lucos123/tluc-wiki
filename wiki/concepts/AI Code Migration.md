---
title: AI Code Migration
date: 2026-07-28
tags:
  - concept
  - agentic-design
  - ai-sdlc
  - harness-engineering
---

# AI Code Migration

A methodology for using AI agents to port a production codebase to a new language or framework, compressing what were formerly multi-year, multi-million-dollar projects into days or weeks for a single engineer. First documented at scale by [How Anthropic runs large-scale code migrations with Claude Code](../sources/How%20Anthropic%20runs%20large-scale%20code%20migrations%20with%20Claude%20Code.md).

## Core Principle

> **"You don't fix the code. You fix the process (loop) that produced the code."**

Engineers write migration rules and verification loops; agents translate, compile, and test until the new code's behaviour matches the original. Individual failures are the loop's job — human attention belongs on the **patterns**.

## Why Large Migrations Are Newly Viable

| Factor | Before AI | After AI |
|--------|----------|---------|
| Cost (1M lines) | $3–4M, 4+ years | $165K, 2 weeks |
| Career risk | Massive (90% parity = failure) | "Delete the branch and try again" |
| Trigger threshold | Must be existential | One chronic bottleneck can justify it |

The remaining constraints: token cost (tens to hundreds of thousands of dollars), and the need for a justifiable business case. Not every migration is worth running.

## Why AI Excels at Migrations

1. **Parallel work**: Thousands of independent units (files, modules) can run simultaneously.
2. **Built-in spec**: The old code *is* the specification.
3. **Objective referee**: Test suites provide ground truth — no human arbitrating quality.
4. **Self-writing queue**: Compiler errors and test failures become the next item automatically.
5. **Rule propagation**: A reviewer citing a rule turns every violation into a queue item and a rulebook update, preventing drift.

## Two Migration Modes

| Mode | When | Rulebook shape | Stress-test method |
|------|------|---------------|-------------------|
| **Structure-preserving** | Same architecture, new language | Lookup tables (types, idioms) | 2-agent translation diff |
| **Redesign** | New architecture + new language | Design document | Adversarial reviewers attack the design, then disposable end-to-end run |

## Six-Step Process

### Prerequisites: The Judge
Build a language-agnostic test harness before starting — this is the exit condition. The judge must pass against original code AND fail against deliberately broken code. If no existing test suite: have Claude create one from real-world scenarios and diff against the original.

### Step 1 — Rulebook + Dependency Map + Gap Inventory
- **Rulebook**: Codifies every translation decision. Comes before the gap inventory (gaps = what the rulebook's defaults won't cover).
- **Dependency map**: Orders parallel workstreams — which files migrate first, which batch together.
- **Gap inventory**: Implicit language requirements (e.g., manual memory management in Zig→Rust; type interfaces in Python→TypeScript).

### Step 2 — Stress-Test the Rules (Shakedown Cruise)
Mini-migration of ~3 files. Goal is to refine the rulebook, not make progress. **Throw out all translated files.**
- Agent A translates per rulebook; Agent B translates "like a senior [language] engineer"; Agent C diffs → new rules.

### Step 3 — Translate Everything
Fan-out parallel multi-agent loop: **implement → review → fix**.
- Implementers: smaller/cheaper models, fanned out broadly.
- Reviewers: largest model, adversarial, separate contexts, 2 per batch + tiebreak agent.
- Queue: mechanical and resumable ("done" = target file exists on disk).
- Rule propagation: repeated mistakes → rulebook sentence → regenerate affected batch. Never hand-patch code against a rule.
- `// TODO(port): <reason>` for items that can't be resolved in translation.

### Steps 4–6 — Compile → Smoke Test → Behaviour Match
Same loop with progressively less human judgment:
- **Compile**: Compiler error list becomes the queue. Systemic errors → encode classification logic.
- **Smoke test**: Crash groups by root cause → adversarial subagents.
- **Behaviour match**: Run judge against translated code. **Build daemon** serialises expensive rebuilds: fixers patch → daemon batches → one rebuild → re-run affected tests → feed results back. Repeated failures → amend the rule → regenerate only files that rule touched.

## Tiered Model Pattern

Token spend concentrates in loops. Design loops with cheaper models; use the largest model where its output propagates everywhere (rules, reviewers).

| Role | Recommended tier |
|------|-----------------|
| Rule-writers, reviewers | Largest available (e.g., Claude Fable 5) |
| Implementation fan-out | Mid-tier (e.g., Claude Sonnet) |
| Mechanical fixing loops | Mid-tier or small |

## Build Daemon Pattern
A separate process that is the *only process allowed to rebuild the binary*. Fixers write patches; daemon batches them, rebuilds once, re-runs only affected tests, feeds results back. **Serialises the most expensive operation without blocking parallel fix work.**

## Front-Load Human Hours
The rulebook and stress-test (Steps 1–2) require the most human judgment. Everything after Steps 1–2 is queues burning down. Return on invested human time is highest at the front.

## Related Entities
- [Jarred Sumner](../entities/Jarred%20Sumner.md): ran Zig→Rust migration of Bun (~1M lines)
- [Mike Krieger](../entities/Mike%20Krieger.md): ran Python→TypeScript migration (165K lines)
- [Claude Code](../entities/Claude%20Code.md): the agent environment used for these migrations

## Connections
- Embodies [Harness Engineering](Harness%20Engineering.md): the engineer designs the rules and loops, not the code.
- Extends [Context Engineering](Context%20Engineering.md): the old codebase is the context/spec; the judge is the verification harness.
- Relates to [The Factory Model (SDLC)](The%20Factory%20Model%20%28SDLC%29.md): systems that build software, applied to migration.
