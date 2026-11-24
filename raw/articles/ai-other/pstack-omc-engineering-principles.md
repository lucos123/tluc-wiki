---
title: "Engineering Principles Library (pstack and OMC)"
original_source: "https://github.com/cursor/plugins/tree/main/pstack"
port_source: "https://github.com/michael-denyer/pstack-claude"
adaptation: "oh-my-claudecode/skills/principles/SKILL.md"
author:
  - "Lauren Tan"
  - "Michael Denyer"
  - "oh-my-claudecode contributors"
created: 2026-11-24
tags:
  - "clippings"
  - "agentic-design"
  - "code-quality"
---

# Engineering Principles Library (pstack and OMC)

- **Original Library:** `pstack` — Lauren Tan (`https://github.com/cursor/plugins/tree/main/pstack`)
- **Claude Port:** `pstack-claude` — Michael Denyer (`https://github.com/michael-denyer/pstack-claude`)
- **Lane-Mapped Adaptation:** `oh-my-claudecode/skills/principles/SKILL.md` (Captured 2026-11-24)

---

## Overview & Usage Scope

Twenty-four engineering principles organized in five groups, mapped to the specialized agent lane carrying each principle. Framed as a discipline guide shaping how engineering decisions are evaluated rather than a blocking gate on its own.

- **When to apply:**
  - A fix has failed twice, or two fixes share one explanation.
  - Debugging, verification, or benchmarking work is starting.
  - A design choice repeats a shape assumption across files.
  - Delegation briefs are being written and standing role principles should travel with the prompt.
- **When to skip:**
  - A one-line mechanical edit with a deterministic check.
  - A hotfix under time pressure (note which principle was skipped and why in one line).

---

## 1. Core (10 Principles)

1. **Laziness Protocol**: When refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading, bias to deletion and the smallest change that solves the problem. Composes with minimal code discipline. Carried by `executor` and `code-simplifier`.
2. **Foundational Thinking**: Before writing logic, establish core types and data structures, scaffold-vs-feature sequencing, and what concurrent actors share. Carried by `architect` and `planner`.
3. **Redesign from First Principles**: When integrating a new requirement into an existing design, redesign as if the requirement had been foundational from day one instead of patching the old shape around it. Carried by `architect`.
4. **Attack the Premise**: When two or more attempted fixes share one assumption and all failed the same gate, stop writing fix three. Write the shared assumption down, test it directly, and let the result choose the next move. Carried by `critic` during plan gap analysis and by `debugger` before a third retry.
5. **Subtract Before You Add**: Before sequencing an addition, refactor, or rewrite, remove dead weight first and build on the simpler base. Carried by `executor` and `code-simplifier`.
6. **Minimize Reader Load**: When reviewing or shaping hard-to-trace code, count layers and hidden state, collapse one-caller wrappers, and shrink mutable scope. Carried by `code-simplifier` and `writer`.
7. **Outcome-Oriented Execution**: On planned rewrites and migrations with explicit phase boundaries, converge on the target architecture; do not preserve throwaway compatibility states. Carried by `planner`.
8. **Experience First**: For product, UX, or feature-scope trade-offs, choose user delight over implementation convenience, and state the trade-off explicitly when taking it. Carried by `designer`.
9. **Exhaust the Design Space**: For a novel interaction or architectural decision with no precedent, build 2–3 competing options and compare before committing. Carried by `architect`.
10. **Build the Lever**: For any non-trivial repeated work, build the tool that does or proves it (codemod, script, generator) rather than doing it manually a third time; the tool becomes the artifact a reviewer reruns. Carried by `executor`.

## 2. Architecture (6 Principles)

11. **Model the Domain**: When stateful logic branches repeatedly or repeats a shape assumption across files, encode the domain in a structure (state machine, typed model, registry, reducer) instead of scattering conditionals. Carried by `architect`.
12. **Boundary Discipline**: When wiring validation, error handling, or framework adapters, enforce guards at system boundaries, trust internal types, and keep business logic pure. Carried by `architect` and `executor`.
13. **Type System Discipline**: When designing types or signatures in a typed language, make illegal states unrepresentable, brand primitives, and parse external data at boundaries. Carried by `architect` and `executor`.
14. **Make Operations Idempotent**: Design commands, lifecycle steps, and loops running amid crashes and retries to converge to the same end state. Carried by `executor`.
15. **Migrate Callers, Then Delete Legacy APIs**: When introducing a new internal API while old callers exist, migrate every caller and delete the old surface in one wave; a compatibility shim with no expiry becomes a second system. Carried by `executor`.
16. **Separate Before Serializing Shared State**: When concurrent actors might write the same file, branch, key, or object, eliminate sharing first (e.g., a writer per worktree); locking is the fallback, not the first move. Carried by `executor` and `team`.

## 3. Verification (5 Principles)

17. **Prove It Works**: Done means verified against the real artifact (actual command output, passing test, rendered page), never a proxy and never `"it compiles"`. Carried by `verifier`.
18. **Fix Root Causes**: Trace each symptom to the first place the system went wrong and fix it there. A guard for a state that should not exist is a workaround, not a fix; it is legitimate only when that state itself is legitimate. Carried by `debugger` and enforced by `verifier`.
19. **Sequence Work into Verifiable Units**: For multi-step sweeps, migrations, or commit stacks, break work into small units ending in a check, verified before the next, ordered so the sequence proves itself. Carried by `planner` and `git-master`.
20. **Test Behavior, Not Implementation**: Assert what users of the code can observe so tests fail when behavior breaks and pass when only internals change. Carried by `test-engineer`.
21. **Explain the Number**: Before trusting, reporting, or acting on a measured number, identify what limits it and rule out measuring something else; label every claim measured, inferred, or guess in the same sentence. Carried by `scientist` and any lane reporting performance.

## 4. Delegation (2 Principles)

22. **Guard the Context Window**: Route bulk reading and large outputs to subagents; keep summaries in the lead thread. Applies to every lane and orchestrator.
23. **Never Block on the Human**: When tempted to ask `"should I do X?"` on reversible work, proceed, present the result, and let the human course-correct; reserve questions for product calls no experiment can settle. Carried by every lane.

## 5. Meta (1 Principle)

24. **Encode Lessons in Structure**: The second time you write the same instruction, stop writing it a third time: encode it as a lint rule, runtime check, script, or enforced workflow (`Text rots; structure reruns.`). Carried by `skillify` and `self-improve`.

---

## Lane Distribution Map & Reporting Rule

| Lane | Standing Principles |
| :--- | :--- |
| `critic` | Attack the premise |
| `debugger` | Attack the premise, Fix root causes |
| `verifier` | Prove it works, Fix root causes |
| `test-engineer` | Test behavior, not implementation |
| `architect` | Foundational Thinking, Redesign from First Principles, Model the domain, Exhaust the design space |
| `planner` | Foundational Thinking, Outcome-oriented execution, Sequence work into verifiable units |
| `executor` | Laziness Protocol, Subtract before you add, Make operations idempotent, Boundary discipline, Type system discipline, Migrate callers, Separate before serializing, Build the lever |
| `scientist` | Explain the number |
| `designer` | Experience first |
| `code-simplifier` | Laziness Protocol, Subtract before you add, Minimize reader load |
| `writer` | Minimize reader load |
| `git-master` | Sequence work into verifiable units |
| every lane | Guard the context window, Never block on the human, Encode lessons in structure |

- **Reporting Clause**: Name which principle shaped each non-obvious decision in one clause; if a principle conflicts with an explicit user instruction, the user instruction wins.
