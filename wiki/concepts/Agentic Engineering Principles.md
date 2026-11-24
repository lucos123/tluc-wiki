---
title: "Agentic Engineering Principles"
date: 2026-11-24
tags:
  - concept
  - agentic-design
  - harness-engineering
  - code-quality
  - verification
source: "wiki/sources/Engineering Principles Library (pstack and OMC).md"
---

# Agentic Engineering Principles

**Agentic Engineering Principles** are compact, trigger-bound engineering heuristics originating in [Lauren Tan](../entities/Lauren%20Tan.md)'s `pstack` library and analyzed in [Engineering Principles Library (pstack and OMC)](../sources/Engineering%20Principles%20Library%20%28pstack%20and%20OMC%29.md). Instead of generic coding platitudes, each principle names **when it fires**, **what failure mode it prevents**, and **which agent role carries it**.

---

## 1. Position in the Trust Stack

Within [Poteto Trust Pyramid](Poteto%20Trust%20Pyramid.md), engineering principles occupy **Layer 4 (Prose / Judgment)**:
- **Before Automation Exists**: Principles steer architectural framing, premise validation, and minimal-diff trade-offs where static analysis cannot judge context.
- **Upward Graduation (*Encode Lessons in Structure*)**: Whenever a prose reminder repeats twice (`"Text rots; structure reruns"`), it graduates upward into Layer 1 (`codebase structure`), Layer 2 (`AST / schema linters`), or Layer 3 (`runtime checks` and [Verification Loop](Verification%20Loop.md) scripts).

---

## 2. High-Leverage Decision Triggers

Rather than reciting 24 slogans on every task, activate the matching heuristic when its concrete trigger appears:

| Trigger Condition | Principle | Operational Rule & Exit Check |
| :--- | :--- | :--- |
| `>= 2` failed fixes share one assumption | **Attack the Premise** | Halt fix #3; write the shared assumption explicitly, run a direct check to falsify/confirm it, then choose the next edit |
| Performing non-trivial manual edits a 3rd time | **Build the Lever** | Write a reusable script, codemod, or generator; reviewers verify the deterministic tool output |
| Stateful logic branches repeatedly across files | **Model the Domain** | Replace scattered conditionals with a single state table, typed schema, or state machine |
| External/framework input enters core logic | **Boundary & Type Discipline** | Validate untrusted inputs at boundaries (`parse, don't validate`), make illegal states unrepresentable, keep internal logic pure |
| Retries or crashes can leave partial side effects | **Make Operations Idempotent** | Design writes and state transitions so re-running converges to identical state (`register_ingest.py`, deterministic sync scripts) |
| Parallel workers touch shared files or state | **Separate Before Serializing** | Partition ownership per directory or worktree first ([Git Worktree Isolation](Git%20Worktree%20Isolation.md)); fall back to locks only when separation fails |
| Defensive check guards an impossible internal state | **Fix Root Causes** | Trace back to the first broken invariant and repair it at the origin instead of masking symptoms |
| Prompt prose states the same constraint a 2nd time | **Encode Lessons in Structure** | Convert the rule into a static lint rule, type guard, or runtime assertion and prove it catches the bad input |
| Quoting speedup, latency, throughput, or eval delta | **Explain the Number** | Identify the limiting bottleneck, verify end-to-end scope and `>= 5` repeats, and attach inline provenance (`measured` + source, `inferred`, or `estimate`) |

---

## 3. Pairwise Tensions & Required Guardrails

Many engineering principles act as opposing forces; applying either half blindly degrades software quality:

| Competing Principles | When Each Side Wins | Required Guardrail |
| :--- | :--- | :--- |
| **Minimal Diff** (*Laziness Protocol*, *Subtract Before You Add*) vs **Clean Redesign** (*Foundational Thinking*, *Redesign from First Principles*) | Use minimal diff + deletion on localized bugfixes; invoke first-principles redesign when a new requirement breaks existing data/state boundaries | Inspect core types and shared state before coding; avoid speculative wrappers for minor edits, and avoid brittle shims across broken seams |
| **One-Wave Legacy Deletion** (*Outcome-Oriented Execution*, *Migrate Callers & Delete*) vs **Backwards Compatibility** | Delete legacy callers and shims in one wave for bounded internal APIs | Require expand-and-contract phased rollouts for live zero-downtime databases or external versioned contracts |
| **Design Space Exploration** (*Exhaust the Design Space*) vs **Execution Velocity** | Draft 2–3 competing options when irreversible choices lack repo precedent | Skip formal option matrices on localized reversible changes |
| **Autonomy** (*Never Block on the Human*) vs **Human-Gated Safety** | Proceed first on reversible, low-risk local work and let users inspect the result | Always pause and confirm at irreversible boundaries, schema-protected stores (`mem/`, `raw/`), destructive actions, and ambiguous specs (`⚠️ Evolving claim`) |

---

## 4. Role-Scoped Principle Injection (Anti-Bloat Pattern)

Loading a flat 24-item rulebook into every prompt dilutes attention and accelerates [Context Rot](Context%20Rot.md). Pairing principle routing with [Progressive Disclosure](Progressive%20Disclosure.md) and [Subagent Architecture](Subagent%20Architecture.md) keeps instructions tight:

```
┌────────────────────────────────────────────────────────────────┐
│  Shared Baseline (All Agents)                                  │
│  • Guard the context window (delegate bulk reads to subagents) │
│  • Encode lessons in structure (lint/script > repeated prose)  │
└───────────────┬───────────────────────────────┬────────────────┘
                ▼                               ▼
┌───────────────────────────────┐ ┌──────────────────────────────┐
│  Design / Review Lanes        │ │  Build / Verification Lanes  │
│  • Critic/Debug: Attack the   │ │  • Exec: Minimal diff, types,│
│    premise, Fix root causes   │ │    idempotency, partition    │
│  • Arch: First principles,    │ │  • Verify: Real artifacts &  │
│    Domain models, 2-3 options │ │    Explain the number        │
└───────────────────────────────┘ └──────────────────────────────┘
```

---

## Related Pages

- **Entities**: [Lauren Tan](../entities/Lauren%20Tan.md)
- **Concepts**:
  - [AI Code Migration](AI%20Code%20Migration.md)
  - [Comprehension and Intent Debt](Comprehension%20and%20Intent%20Debt.md)
  - [Context Rot](Context%20Rot.md)
  - [Context Window Management](Context%20Window%20Management.md)
  - [Git Worktree Isolation](Git%20Worktree%20Isolation.md)
  - [Poteto Trust Pyramid](Poteto%20Trust%20Pyramid.md)
  - [Progressive Disclosure](Progressive%20Disclosure.md)
  - [Self-Improving Agents](Self-Improving%20Agents.md)
  - [Subagent Architecture](Subagent%20Architecture.md)
  - [Verification Loop](Verification%20Loop.md)
- **Sources**:
  - [All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI](../sources/All%20Code%20Is%20Slop%20%28Except%20Mine%29%20%E2%80%94%20Lauren%20Tan%2C%20SpaceXSI.md)
  - [Engineering Principles Library (pstack and OMC)](../sources/Engineering%20Principles%20Library%20%28pstack%20and%20OMC%29.md)
