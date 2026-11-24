---
title: "Engineering Principles Library (pstack and OMC)"
date: 2026-11-24
tags:
  - source
  - agentic-design
  - harness-engineering
  - code-quality
  - verification
source: "raw/articles/ai-other/pstack-omc-engineering-principles.md"
---

# Engineering Principles Library (pstack and OMC)

**Source File**: [raw/articles/ai-other/pstack-omc-engineering-principles.md](../../raw/articles/ai-other/pstack-omc-engineering-principles.md)  
**Lineage**: Original `pstack` library by [Lauren Tan](../entities/Lauren%20Tan.md) (`github.com/cursor/plugins/tree/main/pstack`) $\rightarrow$ `pstack-claude` port by Michael Denyer $\rightarrow$ OMC lane-mapped adaptation (`oh-my-claudecode/skills/principles/SKILL.md`).

---

## Executive Summary

This library distills **24 engineering judgment principles** across five groups (`Core`, `Architecture`, `Verification`, `Delegation`, `Meta`) and adds a **Lane Distribution Map** that routes only role-relevant principles into each subagent prompt. In [Poteto Trust Pyramid](../concepts/Poteto%20Trust%20Pyramid.md), these principles sit in **Layer 4 (Prose / Judgment)**: they shape how agents reason when deterministic rules do not decide the move, while constantly pushing recurring patterns upward into **Layers 1–3** (`"Text rots; structure reruns"`).

---

## Catalog of 24 Principles Across Five Groups

- **Core (`10` principles)**: *Laziness Protocol*, *Foundational Thinking*, *Redesign from First Principles*, *Attack the Premise*, *Subtract Before You Add*, *Minimize Reader Load*, *Outcome-Oriented Execution*, *Experience First*, *Exhaust the Design Space*, *Build the Lever*.
- **Architecture (`6` principles)**: *Model the Domain*, *Boundary Discipline*, *Type System Discipline*, *Make Operations Idempotent*, *Migrate Callers, Then Delete Legacy APIs*, *Separate Before Serializing Shared State*.
- **Verification (`5` principles)**: *Prove It Works*, *Fix Root Causes*, *Sequence Work into Verifiable Units*, *Test Behavior, Not Implementation*, *Explain the Number*.
- **Delegation (`2` principles)**: *Guard the Context Window*, *Never Block on the Human*.
- **Meta (`1` principle)**: *Encode Lessons in Structure*.

### Lane Distribution Map (Selective Injection)

Instead of loading all 24 rules into every prompt, the distribution map injects narrow subsets per specialist role (`critic`, `debugger`, `verifier`, `test-engineer`, `architect`, `planner`, `executor`, `scientist`, `designer`, `code-simplifier`, `writer`, `git-master`), reserving `Guard the context window`, `Never block on the human`, and `Encode lessons in structure` as cross-cutting baselines.

---

## Critical Evaluation & Vetting Matrix for `tluc-wiki`

Rather than importing all 24 principles uncritically, evaluation against our existing vault patterns splits them into three tiers:

### Tier 1 — High-Signal Heuristics Not Yet Named Explicitly in Our Wiki
- **Attack the Premise**: When two fixes sharing one underlying assumption fail the same check, halt fix #3, write the shared assumption explicitly, and test it directly. Sharpens debugging and plan review beyond generic retries.
- **Build the Lever**: Build a deterministic script, codemod, or generator before performing non-trivial manual edits a third time; reviewers verify the lever instead of hand-inspecting repetitive edits.
- **Make Operations Idempotent & Separate Before Serializing**: Prioritize eliminating shared mutable state (worktree/file partitioning) over locks, and design scripts/migrations so retries after partial failure converge cleanly (`register_ingest.py`, `lint_wiki.py`).
- **Fix Root Causes**: Reject defensive guards around states that cannot legitimately exist; trace to the originating invariant and repair it at the source.
- **Encode Lessons in Structure**: Reinforces [Poteto Trust Pyramid](../concepts/Poteto%20Trust%20Pyramid.md) directly (`Text rots; structure reruns`): the second time a human writes a reminder, encode it as a script, type guard, or lint check (`agent-doc-and-correction-rules.md` 5-Level Ladder).
- **Role-Scoped Principle Injection**: Directly pairs with [Progressive Disclosure](../concepts/Progressive%20Disclosure.md) and [Context Window Management](../concepts/Context%20Window%20Management.md) to avoid bloating subagent prompts.

### Tier 2 — Valid Discipline Requiring Pairwise Tension Guards

| Principle Pair / Tension | Valid Scope | Failure Mode Without Guardrail |
| :--- | :--- | :--- |
| *Laziness Protocol* + *Subtract Before You Add* vs *Foundational Thinking* + *Redesign from First Principles* | Local bugfixes/refactors favor smallest diff + deletion; new requirements that break core data shapes trigger clean redesign | Agents either over-abstract small fixes or stack brittle shims onto an outdated foundation |
| *Outcome-Oriented Execution* + *Migrate Callers, Then Delete Legacy APIs* | Bounded internal refactors and monorepo migrations where all callers are visible | Breaks zero-downtime DB rollouts or external versioned APIs that require expand-and-contract steps |
| *Exhaust the Design Space* (`2–3` options) vs token budget | High-stakes architectural forks without repository precedent | Wastes tokens comparing trivial alternatives on routine tasks |
| *Experience First* | Product/UX calls where user ergonomics compete with implementation simplicity | Turns subjective unless the UX-vs-cost trade-off is stated explicitly |

### Tier 3 — High-Risk Scope Boundary (`⚠️ Evolving claim`)
- ⚠️ **Evolving claim (`Never Block on the Human`)**: Proceeding first and letting users course-correct works **only** for strictly reversible, low-ambiguity execution steps. It conflicts directly with explicit human-gated controls across `tluc-wiki`:
  - `raw/` immutability and permanent deletions.
  - Confirmation-gated `mem/` preference edits ([wiki-manage](../../.agents/skills/wiki-manage/SKILL.md)).
  - Human-gated `.agents/skills/` improvements after ingestion ([wiki-ingest](../../.agents/skills/wiki-ingest/SKILL.md)).
  - Ambiguous multi-fork briefs where `sharpen` upfront scoping prevents speculative rework ([sharpen](../../.agents/skills/sharpen/SKILL.md)).

### Existing Wiki Overlap Map (Avoid Duplication)

| Principles Covered | Existing `tluc-wiki` Concept Pages | Integration Decision |
| :--- | :--- | :--- |
| *Prove It Works*, *Encode Lessons in Structure*, *Fix Root Causes* | [Poteto Trust Pyramid](../concepts/Poteto%20Trust%20Pyramid.md), [Verification Loop](../concepts/Verification%20Loop.md), [Comprehension and Intent Debt](../concepts/Comprehension%20and%20Intent%20Debt.md) | Synthesize as concrete decision triggers rather than repeating pyramid layers |
| *Guard the Context Window*, *Separate Before Serializing* | [Context Window Management](../concepts/Context%20Window%20Management.md), [Subagent Context Isolation](../concepts/Subagent%20Context%20Isolation.md), [Git Worktree Isolation](../concepts/Git%20Worktree%20Isolation.md) | Link directly and add the serialization-vs-partitioning order rule |
| *Sequence Work into Verifiable Units*, *Migrate Callers* | [AI Code Migration](../concepts/AI%20Code%20Migration.md), [Agentic Coding Workflow](../concepts/Agentic%20Coding%20Workflow.md) | Highlight internal one-wave vs external expand-and-contract boundary |
| *Explain the Number* | [Product Evals and Error Analysis](../concepts/Product%20Evals%20and%20Error%20Analysis.md), [epistemics.md](../../.agents/skills/deep-research/references/epistemics.md) | Cross-reference canonical 5-step benchmark vetting checklist |

---

## Related Pages

- **Entities**: [Lauren Tan](../entities/Lauren%20Tan.md)
- **Concepts**:
  - [Agentic Engineering Principles](../concepts/Agentic%20Engineering%20Principles.md)
  - [AI Code Migration](../concepts/AI%20Code%20Migration.md)
  - [Comprehension and Intent Debt](../concepts/Comprehension%20and%20Intent%20Debt.md)
  - [Context Window Management](../concepts/Context%20Window%20Management.md)
  - [Git Worktree Isolation](../concepts/Git%20Worktree%20Isolation.md)
  - [Poteto Trust Pyramid](../concepts/Poteto%20Trust%20Pyramid.md)
  - [Progressive Disclosure](../concepts/Progressive%20Disclosure.md)
  - [Verification Loop](../concepts/Verification%20Loop.md)
- **Sources**: [All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI](All%20Code%20Is%20Slop%20%28Except%20Mine%29%20%E2%80%94%20Lauren%20Tan%2C%20SpaceXSI.md)
