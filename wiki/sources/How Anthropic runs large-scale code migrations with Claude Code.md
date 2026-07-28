---
title: How Anthropic runs large-scale code migrations with Claude Code
date: 2026-07-28
tags:
  - source
  - claude-code
  - agentic-design
  - ai-sdlc
  - harness-engineering
source: "raw/claude-code/How Anthropic runs large-scale code migrations with Claude Code.md"
---

# How Anthropic runs large-scale code migrations with Claude Code

**Source File**: `claude-code/How Anthropic runs large-scale code migrations with Claude Code.md`
**Original URL**: https://claude.com/blog/ai-code-migration

Anthropic's engineering blog post documenting how individual developers ran million-line code migrations using [[Claude Code]], Claude Fable 5, and Claude Opus 4.8. Presents two real case studies and a generalised six-step methodology with open-source starter kit.

## Core Insight

> **"You don't fix the code. You fix the process (loop) that produced the code."**

Individual failures are the loop's job. Human attention belongs on the patterns. This reframes large migrations from a code-quality problem into a workflow-design problem — a direct application of [[Harness Engineering]].

## Case Studies

### Jarred Sumner — Bun: Zig → Rust (structure-preserving)
- **Scale**: ~1 million lines of code
- **Duration**: Less than 2 weeks
- **Models**: Claude Fable 5 + Claude Opus 4.8 for key steps; Sonnet for implementation fan-out
- **Token cost**: 5.9B input + 690M output ≈ **$165,000 at API pricing**
- **Test suite**: TypeScript (third language, independent from both Zig and Rust)
- **Outcome**: 100% test suite passing before merge; 19 post-merge regressions (all fixed and shipped in production)
- **Results**: Memory usage dropped 6,745 MB → 609 MB; binary 19% smaller; 2–5% faster; ~4% code in `unsafe` blocks (pointer ops at C/C++ boundaries)
- **Approach**: Rulebook as lookup tables (types/idioms); 8 specialized review subagents for 8 failure categories; compiler deferred to Step 4 (cargo too slow for inner loop)

### Mike Krieger — Python → TypeScript (redesign)
- **Scale**: 165,000 lines
- **Duration**: Weekend
- **Models**: Claude Fable 5 + Claude Sonnet (12 fanned-out subagents for main migration)
- **Token cost**: ~27M tokens for main portion
- **Process**: 8 phase gates, 3 adversarial review rounds, final parity check diffing every command's output against Python original
- **Approach**: Ran the entire migration end-to-end, revised rules and workflow based on results, ran again — **discarding output each time** — until the 3rd run was kept. Parity harness: 7 real-world scenarios. Also had Claude design + run its own autonomous test suite overnight for 4 consecutive nights.
- **Rulebook**: Design document (not lookup tables, because redesign not port)
- **Judge**: 7 real-world scenarios diffed against Python original; any behavior change = bug

## Six-Step Process

### Prerequisites: Build the Judge
Build a language-agnostic test suite before starting — this is the exit condition.
1. **Categorize** existing tests (external-callable vs. internal-dependent).
2. **Rewrite** external-facing tests as portable assertions runnable against both original and port. Use adversarial agents to verify rewrites don't weaken assertions.
3. **Validate** the judge: must pass against original, must fail against deliberately broken code.
4. **If no test suite exists**: have Claude create one from 7+ real-world scenarios, diff against original.

### Step 1 — Create Rulebook, Dependency Map, Gap Inventory
- **Rulebook**: Architectural decisions first. Structure-preserving → lookup tables (types, idioms, memory patterns). Redesign → design document.
- **Dependency map**: Discovered via deterministic script (agents create + run the script). Needed to order parallel workstreams (which files to migrate first, which to batch together).
- **Gap inventory**: Implicit language-specific requirements the rulebook defaults won't cover (Zig→Rust: manual memory management; Python→TypeScript: type interfaces/contracts). Order matters: rulebook must precede gap inventory.
- **Skeptic reviewers**: Adversarial agents specifically designed to find each category of gap.

### Step 2 — Stress-Test the Rules ("Shakedown Cruise")
Mini-migration of 3 files:
- Agent A: translate per rulebook
- Agent B: translate "like a senior [target language] engineer"
- Agent C: diff to produce new translation rules

**Throw out all translated files** — goal is to refine rules, not make progress. Only works for structure-preserving migrations. For redesigns (Mike): attack design document with adversarial reviewers, then run a disposable end-to-end.

### Step 3 — Translate Everything
Multi-agent implement → review → fix loop:
- **Implementers**: smaller models (Sonnet) fanned out in parallel (12 subagents)
- **Reviewers**: larger models (Fable), adversarial, separate contexts
- **2 reviewers per batch**; disagreement → 3rd agent tiebreak
- **Work queue**: mechanical, rebuilt from disk state each time (done = target file exists). **Resumable by construction.**
- **Rule propagation**: When reviewer catches same mistake across files, add one sentence to rulebook and regenerate affected batch. Code never gets hand-patched against the rulebook.
- **TODOs**: Unresolvable items flagged as `// TODO(port): <reason>` for compiler step
- **Compiler placement**: Inside loop if fast (TypeScript = seconds); deferred if slow (Cargo/Rust = minutes)

### Steps 4, 5, 6 — Compile → Smoke Test → Behavior Match
Same loop architecture with progressively less human judgment:
- **Step 4 (Compile)**: Orchestrator invokes compiler across workspace; fixer agents burn through error list in parallel + adversarial review; repeat. Systemic errors (e.g., thousands of Rust module errors from cyclic imports) → encode logic to classify/fix the root cause.
- **Step 5 (Smoke test)**: Crashes group by root cause → adversarial subagents review each group.
- **Step 6 (Behavior match)**: Run judge (test suite) against translated code. **Build daemon** serializes rebuilds: fixers write patches → daemon batches → one rebuild → re-run affected tests → feed results back. When same failure repeats across many tests → amend the rule → regenerate only files that rule touched.

## Advisory Model Pattern
Use multiple model tiers deliberately:
| Role | Model tier | Why |
|------|-----------|-----|
| Reviewers & rule-writers | Largest (Fable 5) | Highest judgment; rules propagate everywhere |
| Implementation fan-out | Medium (Sonnet) | High-volume; cost concentrates in loops |
| Compilation triage | Medium/small | Mechanical matching |

## Best Practices
- **Don't follow this guide blindly** — plan your specific migration with Claude first.
- **Don't focus on individual failures** — that's the loop's job. Watch the patterns.
- **Make review adversarial, verification mechanical** — adversarial review for autonomous runs; scripts (compiler, diff, test suite) as referee.
- **Front-load human hours** — rulebook + stress-test are the most time-consuming steps. Everything after is queues burning down.
- **Make the queue mechanical & resumable** — "done" = output file exists on disk.
- **Don't use largest model for everything** — tiered model usage by role.

## New Entities & Concepts Introduced
- [[Jarred Sumner]]: Bun co-founder, Anthropic MTS — ran Zig→Rust migration
- [[Mike Krieger]]: Anthropic Labs co-lead — ran Python→TypeScript migration
- [[AI Code Migration]]: the six-step methodology itself

## Synthesis Notes

This source marks a qualitative shift in what [[Claude Code]] is used for. Previous sources covered coding assistance and agentic workflows within existing codebases. This source shows that entire *language ecosystems* can be ported by a single engineer over days — a formerly multi-year, multi-million-dollar endeavour.

The "fix the loop, not the code" insight directly extends [[Harness Engineering]]: the engineer's job shifts from writing or reviewing code to designing and iterating the rules, verification machinery, and agent orchestration that *produces* correct code. The most valuable human hours are now in the prerequisites and Step 2 (shakedown cruise) — everything after is execution.

The tiered model usage (Fable for rule-writers/reviewers, Sonnet for implementers) is a cost-optimisation pattern that will likely become standard practice: token spend concentrates in the loops, so loops should use cheaper models, while the "upstream" decisions (rules that every downstream agent follows) warrant the best model.

The "build daemon" in Step 6 is an elegant concurrency solution: multiple fixer agents writing patches simultaneously while only one rebuild runs at a time. This is a general pattern for any situation where a shared expensive resource (compiler, integration test, deploy) must be serialized but the work feeding it is parallelizable.

Mike's approach of running the entire migration 3 times and discarding output until the 3rd run contrasts with Jarred's incremental approach — showing that for redesigns, convergence of the rulebook is more valuable than incremental progress.

Cross-references: [[Harness Engineering]], [[Claude Code]], [[Best practices for Claude Code]] (adversarial review, subagents), [[My LLM coding workflow going into 2026]] (parallel agentic workflows).
