---
title: Effort Level and Model Selection
date: 2026-07-28
tags:
  - concept
  - claude-code
  - cost-optimization
  - agentic-design
---

# Effort Level and Model Selection

A 2-dimensional decision framework for configuring [[Claude Code]]'s output quality and cost. **Model selection** controls which capability ceiling is available; **effort level** controls how thoroughly Claude works toward that ceiling within a single turn.

## The Conceptual Split

| Dimension | What it controls | What it doesn't control |
|-----------|-----------------|------------------------|
| **Model** | Which frozen weights handle the request; capability ceiling; per-token cost | How much work Claude does |
| **Effort** | How many files Claude reads; how many steps before checking in; how much it self-verifies | The capability ceiling |

These are orthogonal dials. On hard tasks they complement each other; on routine tasks one often suffices.

## How Models Work (Conceptual)

Models are **frozen weights** — billions of numerical parameters set during training and read-only during inference. Your prompt, CLAUDE.md, and context *steer* the prediction for one request but don't modify the weights. Changing the model swaps which set of frozen weights handles the request.

**Implication**: Context engineering (CLAUDE.md, skills, RAG docs) is pure steering — effective for that request, not retained. Capability limits are inherent to the weights, not context.

## How Effort Works (Conceptual)

Effort level is sent to the model as part of the request. Behavior at each effort level is *trained into* the frozen weights — it's a first-class input the model responds to, not a post-processing filter.

Higher effort = more output tokens across all categories (thinking, tool calls, text) before reporting completion. Example: roughly **7x more tokens** at high vs low effort for the same prompt.

Key nuances:
- Plans created at high effort are **not frozen** — Claude updates them as it receives results and skips unnecessary steps.
- Claude is trained against "overthinking" — it won't artificially inflate usage on simple tasks even at max effort.
- Effort = how far Claude is *willing* to travel along the capability curve, not how far it *will* travel.

## The Specialist / Expert / Generalist Framework

| Model | Metaphor | Core strength | Best suited for |
|-------|---------|--------------|----------------|
| **Claude Fable 5** | Specialist | Rare cross-domain pattern recognition. Completes tasks Opus/Sonnet cannot at any effort. | Subtle bugs, ambiguous architecture, novel problems |
| **Claude Opus 4.8** | Expert | Deep experience + ambiguity handling. Better than Opus 4.7 at same token count. | Hard, well-bounded problems requiring expertise |
| **Claude Sonnet** | Great generalist | Thorough, reads everything, deep familiarity with *your specific code* | Routine, precisely-described, well-scoped changes |

**Effort as time**: Effort decides how much time any of these people gets with your problem.
- Opus at low effort = quick read by an expert (pattern recognition, not careful review).
- Sonnet at high effort = whole afternoon with a generalist (thorough, deep familiarity with your code).
- Fable even at low effort = specialist glancing at the problem and still seeing what others miss.

## The Diagnostic Heuristic

When Claude gets something wrong:

**Step 1**: Check context quality first. Is the prompt clear? Right tools connected? CLAUDE.md scoped correctly? Right skills available? If effort is being increased for a task that shouldn't need it, the fix is upstream.

**Step 2** (if context is clear and Claude still fails):

```
Did it not TRY hard enough?     →  raise effort
Did it not KNOW enough?         →  upgrade model
```

| Signal | Diagnosis | Fix |
|--------|----------|-----|
| Skipped a file, didn't run tests, bailed mid-refactor | Didn't try hard enough | Raise effort |
| Right context, clearly tried, confidently wrong | Didn't know enough | Upgrade model |
| On a larger model, work has been routine for a while | Overpaying | Drop to smaller model |

## Cost Interaction: Model × Effort

| Task type | Optimal strategy |
|-----------|-----------------|
| **Routine** | Smaller model + default effort. Larger model burns extra verification tokens at higher per-token rate for no quality gain. |
| **Hard/complex** | Larger model may be *cheaper per task* despite higher per-token cost — smaller model grinds toward its ceiling burning many iterations. |
| **Fable-required** | Only Fable can reach completion at any effort level. No substitution possible. |

**The substitution limit**: Model and effort are not substitutes on genuinely hard tasks. A capability ceiling in the weights cannot be overcome by higher effort — the task simply can't be done at that model tier.

## Practical Guidelines

- **Use defaults for most tasks.** Default effort = calibrated to what most people would want to spend.
- **Tune effort as a general preference** (by domain or work type), not task-by-task.
- **Reach for dials only after a miss**, and only after checking context quality.

## Connections to Other Wiki Concepts

- **[[AI Code Migration]]**: Tiered model strategy (Fable for rule-writers/reviewers, Sonnet for fan-out) has principled basis here. Sonnet at high effort = deep familiarity with your specific code; Fable saved for cross-file pattern recognition that rewrites entire batches.
- **[[Verification Loop]]**: Higher effort = more self-verification steps. Stop hooks enforce verification *regardless* of effort — critical for low-effort runs.
- **[[Context Engineering]]**: Context steers, weights teach. CLAUDE.md and skills are steering inputs that expire per-request. The weights hold all durable knowledge.
- **[[Harness Engineering]]**: Model selection makes the model itself a configurable harness component — not just scaffolding around it.
- **[[Claude Code Skills]]**: The `effort` frontmatter field lets skills override effort level for their scope (e.g., `effort: high` for a migration skill, `effort: low` for a quick lint check).
