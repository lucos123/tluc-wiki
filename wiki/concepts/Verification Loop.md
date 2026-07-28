---
title: Verification Loop
date: 2026-07-28
tags:
  - concept
  - agentic-design
  - harness-engineering
  - claude-code
---

# Verification Loop

A repeating cycle where an AI agent checks its own work — running tests, linters, compilers, or custom checks — and fixes what fails before reporting completion. The mechanism by which agentic systems can be left to run unsupervised while still converging on correct output.

## Why It Matters

Without verification loops, agentic tasks end when the agent *believes* the work is done. With them, tasks end when a check *confirms* the work is done. This shift:
- Reduces the number of human review cycles.
- Enables long autonomous runs (overnight, CI, batch jobs).
- Encodes organisational standards that survive model updates.

The core motion: convert every "correction I keep making by hand" into a loop the agent runs itself.

## The Agentic Loop

All agentic coding sessions follow a core structure:
```
Gather context → Take action → Verify results → (loop if results fail)
```
Verification is the third step. Agents already consume deterministic signals from the environment (compiler errors, type failures, lint output). Verification loops extend this to project-specific, workflow-specific, or qualitative checks.

## Gate Strength (from [[Best practices for Claude Code]])

Four levels of verification gate, ordered by strength:

| Level | Mechanism | When to use |
|-------|-----------|-------------|
| 1 | **In-prompt** | Ask Claude to run check and iterate in the same message. |
| 2 | **`/goal` condition** | Separate evaluator re-checks after every turn until condition holds. |
| 3 | **Stop hook** | Shell script blocks the turn from ending until check passes (cap: 8 blocks). |
| 4 | **Verification subagent** | Fresh model reviews the diff — no bias from having written the code. |

## Built-In Verification Support in Claude Code

| Mechanism | Scope |
|-----------|-------|
| `/verify` skill | Builds, runs, and observes application changes |
| Toolchain (linters, type-checkers, tests) | Automatic from environment signals |
| Code Review (research preview) | Managed multi-agent PR review, closeable with `@claude` |
| GitHub Actions integration | PR/push-triggered skill invocations |
| Spec validation skill | Checks changes against a markdown spec |
| Rubrics in Claude Managed Agents (beta) | Grader agent evaluates against rubric; failures loop back automatically |

## Four Deployment Modes (from [[Building verification loops in Claude Code with skills]])

### Standalone
Invoked explicitly. Best for cross-cutting checks that don't apply every time (security scans, accessibility audits, license headers). Outgrown when you run it after *every* change — that's the signal to promote it.

### Embedded
The check fires as part of the producing skill. Append the check to the skill's body. Works only for skills you own (not built-ins or plugin-managed skills).

### Chained
One skill calls another at its end. Creates an end-to-end automated flow.

**Anthropic CC team's chain** (used daily):
```
/code-review → /simplify → /verify → /design (if UI touched)
```

**Wrapper skill pattern** — add verification to skills you can't modify:
```markdown
# .claude/skills/safe-refactor/SKILL.md
Run /simplify on the current diff first.
When /simplify finishes, invoke /verify-no-public-api-changes.
```

Trade-off: chaining trades flexibility for automation and increases token spend.

### On Every PR
Same skills/rubrics applied via GitHub Actions to every PR, regardless of author. The check moves from personal to team infrastructure. Hold off while the chain is still in flux.

## Maturity Progression

```
Manual habit → Standalone skill → Embedded in workflow → Chained pipeline → Team PR gate
```

Each step removes a dependency on human memory.

## Creating a Verification Skill

1. **Identify**: What do you keep correcting manually after Claude's output?
2. **Write it in plain English**: The way you'd explain it to a new teammate.
3. **Create the skill**: `/skill-creator` interview, or hand-write in `.claude/skills/<name>/SKILL.md`.
4. **Confirm**: Invoke on a new task and verify the check runs as part of the output.
5. **Chain**: Connect to other skills when the flow has solidified.
6. **Promote**: Move to PR-level gate once stable.

**Key**: Checks don't need to be qualitative. "Reject any migration that drops a column without a backfill step" is a perfectly valid verification rule — deterministic, project-specific, and invisible to generic linters.

## Applications

- **Code quality**: linting, type-checking, style enforcement after edits.
- **Security**: blocking commits to `.env`, detecting credential leaks.
- **Specification compliance**: checking changes against a `DESIGN.md` or architecture spec.
- **Migration parity**: diffing translated code against the original (see [[AI Code Migration]]).
- **Behavioral parity**: running 7 real-world scenarios against both original and port.
- **Autonomous overnight testing**: Claude generates and runs its own test suite iteratively.

## Relationship to Loop Engineering

[[Loop Engineering]] is the outer structure — which loop type to use (turn-based, goal-based, time-based, proactive), how to trigger it, when to stop it. The Verification Loop is the *inner mechanism* — the check-and-fix cycle that runs within a loop iteration.

```
Loop Engineering  (which loop type, trigger, stop condition)
    └── Verification Loop  (check runs, failure handled, loop back)
```

The `/goal` loop type uses an *evaluator model* as its verification mechanism — Claude never self-judges "done enough," the evaluator decides and sends it back. The stop hook (gate strength 3) is the harness-level enforcement of verification before a turn can end. Both are applications of this concept.

## Related Concepts

- [[Harness Engineering]]: verification loops are a core mechanism of the harness — the "Verify results" step.
- [[Claude Code Skills]]: primary packaging mechanism for verification loops.
- [[Claude Code Hooks]]: deterministic complement — hooks fire at lifecycle events regardless of Claude's judgment; verification loops are invoked by or within agent turns.
- [[AI Code Migration]]: the judge (test suite), build daemon, and six-step loop are all large-scale verification loop applications.
- [[Best practices for Claude Code]]: defines gate strength levels and the adversarial review pattern.
