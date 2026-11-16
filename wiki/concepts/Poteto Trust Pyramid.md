---
title: "Poteto Trust Pyramid"
date: 2026-11-17
tags:
  - concept
  - harness-engineering
  - verification
  - agentic-design
  - code-quality
source: "[[All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI]]"
---

# Poteto Trust Pyramid

The **Poteto Trust Pyramid** (also described as the **Inverse Trust Pyramid**) is an engineering hierarchy introduced by [[Lauren Tan]] (`@poteto`) in [[All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI]] for structuring an AI coding agent's environment. Rather than relying heavily on markdown rules (`AGENTS.md`), comments, or manual PR reviews, it inverts effort so the vast majority of quality enforcement lives in deterministic codebase design and static checks, reserving tokens and human judgment for high-level verification.

---

## The Five Inverted Layers (Top Leverage to Bottom Cost)

```
 ┌───────────────────────────────────────────────────────────┐  Lower cost /
 │       1. Codebase (APIs, architecture, refactoring)       │  Highest trust
 ├───────────────────────────────────────────────────────────┤
 │    2. Static Analysis (lints, types, compilers, CI)       │
 ├───────────────────────────────────────────────────────────┤
 │       3. Verification (Runtime CLIs + Formal/TLA+/Lean)   │
 ├───────────────────────────────────────────────────────────┤
 │           4. Prose (rules, skills, AGENTS.md)             │  Higher cost /
 ├───────────────────────────────────────────────────────────┤  Judgment only
 │                   5. Human Review                         │
 └───────────────────────────────────────────────────────────┘
```

| Layer | Examples & Enforcement | Core Principle |
| :--- | :--- | :--- |
| **1. Codebase** | API design, directory layout (`electron-renderer/` vs `electron-main/`), banning nuanced primitives (`useEffect`) in product code | **"Nuance tends to lead to slop."** Make invalid states unrepresentable and treat the codebase as a curated garden. |
| **2. Static Analysis** | Custom AST lint rules, dependency graph analyzers, file-naming invariants (`tick.hot.ts`), type systems, CI | Convert **every recurring agent correction** into a deterministic lint rule with clear root-cause error instructions (`7 -> 167` custom rules in 4 months). |
| **3. Verification** | **Runtime**: feature map + custom app CLI (`aria-click`, `snapshot`, `screenshot`) + Chrome DevTools Protocol.<br>**Formal & UI Property**: `TLA+`, `Lean`, `Bombadil`, state-chart skills. | Let agents check their own work end-to-end and spend the majority of compute/tokens (~70%) on automated verification. |
| **4. Prose** | `AGENTS.md` ([[Agent Onboarding Files]]), skills ([[Agent Skills Architecture]]), judgment rules | Only put guidance requiring contextual judgment in prose; never try to lint-by-Markdown. |
| **5. Human Review** | Reviewing verification artifacts (videos, screenshots, state charts, formal proofs) rather than raw diff lines | When determinism + verification hold, human review shrinks cleanly without losing production quality. |

---

## Anti-Patterns: Comments & Quick Fixes as Replication Vectors

Because codebase files form an agent's largest input context, workarounds behave like weeds in a garden:
- **Comment Justification Anti-Pattern**: When agents are allowed to add explanatory comments around quick hacks (`// release later, in case it comes back` + `setTimeout(..., 0)`), future agents copy both the anti-pattern and its rationale into shared modules—growing 1 flicker hack on Sep 9 to `183 timers` causing major GC jank by Oct 17.
- **Ban Non-Enforceable Escape Hatches**: Comments decay rapidly and cannot fail CI builds; banning ~99% of product-code comments forces agents to satisfy deterministic lint rules by fixing root causes rather than documenting excuses.
- **Foundations Before Factories**: Scaling autonomous [[Loop Engineering|outer loops]] on top of an undisciplined inner coding loop merely manufactures expensive slop faster. Solid codebase constraints and verification must precede autonomous release fuzzers and auto-merge pipelines.

---

## Relationships

- **Verification Execution**: Directly operationalizes [[Verification Loop]] with **feature map + CLI drivers**, formal verification (`TLA+`, `Lean`), and UI property-based fuzzing (`Bombadil`).
- **Governance & Debt Countermeasure**: Solves [[Comprehension and Intent Debt]] at the architectural root by moving invariants out of fragile prose and code comments into hard compiler/lint boundaries and inspectable verification artifacts.
- **Harness Design Synergy**: Extends [[Harness Engineering]], [[Deterministic Lifecycle Hooks]], [[Agent Onboarding Files]], and [[Automated Multi-Agent Code Review]].
