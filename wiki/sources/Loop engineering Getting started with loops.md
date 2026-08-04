---
title: Loop engineering — Getting started with loops
date: 2026-07-28
tags:
  - source
  - claude-code
  - agentic-design
  - loop-engineering
  - harness-engineering
source: "[[raw/articles/claude-code/loop-engineering-getting-started-with-loops.md]]"
---

# Loop engineering — Getting started with loops

**Source File**: `raw/articles/claude-code/loop-engineering-getting-started-with-loops.md`
**Original URL**: https://claude.com/blog/getting-started-with-loops
**Authors**: Delba de Oliveira and Michael Segner, Claude Code team

The official Claude Code taxonomy of **loop engineering** — designing agents that repeat cycles of work until a stop condition is met. Four loop types, categorised by trigger, stop condition, primitive, and task type.

## Definition

> **Loops = agents repeating cycles of work until a stop condition is met.**

Loop engineering is the practice of *designing* those cycles — choosing the right trigger, the right stop condition, the right primitive, and the right quality-maintenance system — rather than issuing one-off prompts.

## The Four Loop Types

### 1. Turn-Based Loop

| Property | Detail |
|---------|--------|
| **Triggered by** | User prompt (manual) |
| **Stop criteria** | Claude judges task complete OR needs more context |
| **Best for** | Shorter tasks not part of a regular process/schedule |
| **Manage usage by** | Specific prompts + verification skills to reduce turns |
| **Primitive** | The basic agentic loop |

The default. Every prompt starts one. Claude gathers context → takes action → checks its work → responds. The human checks and writes the next prompt.

**Improving the loop**: Encode manual checks as a SKILL.md so Claude can self-verify end-to-end. The more quantitative the check, the easier self-verification is.

Example `verify-frontend-change` skill:
```markdown
---
name: verify-frontend-change
description: Verify any UI change end-to-end before declaring it done.
---
Never report a UI change as complete based on a successful edit alone.
1. Start the dev server and open the edited page in the browser.
2. Interact with the change: click, confirm expected state change, screenshot before/after.
3. Check browser console: zero new errors or warnings.
4. Run Chrome DevTools MCP performance trace and audit Core Web Vitals.
If any step fails, fix and rerun from step 1 — do not hand back partially verified work.
```

---

### 2. Goal-Based Loop (`/goal`)

| Property | Detail |
|---------|--------|
| **Triggered by** | Manual prompt in real-time |
| **Stop criteria** | Goal achieved OR max turns reached |
| **Best for** | Tasks with verifiable exit criteria |
| **Manage usage by** | Specific completion criteria + explicit turn cap |
| **Primitive** | `/goal` |

Each time Claude tries to stop, an **evaluator model** checks the condition and sends it back to work. Claude doesn't have to judge "good enough" — the evaluator decides. Deterministic criteria (test counts, score thresholds) are most effective.

```
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
```

---

### 3. Time-Based Loop (`/loop` and `/schedule`)

| Property | Detail |
|---------|--------|
| **Triggered by** | Specified time interval |
| **Stop criteria** | User cancels OR work completes (PR merges, queue empties) |
| **Best for** | Recurring work OR interfacing with external systems on an interval |
| **Manage usage by** | Longer intervals; react to events rather than time |
| **Primitives** | `/loop` (runs on local machine), `/schedule` (cloud, research preview) |

```
/loop 5m check my PR, address review comments, and fix failing CI
```

`/loop` stops when your machine turns off. `/schedule` persists in the cloud.

---

### 4. Proactive Loop

| Property | Detail |
|---------|--------|
| **Triggered by** | Event or schedule — no human in real-time |
| **Stop criteria** | Each task exits when goal met; routine runs until turned off |
| **Best for** | Recurring streams of well-defined work: bug reports, issue triage, migrations, dependency upgrades |
| **Manage usage by** | Route to smaller/faster models; save capable model for judgment calls |
| **Primitives** | `/schedule` + `/goal` + dynamic workflows + auto mode |

The most powerful composition. Example — autonomous bug triage pipeline:
```
/schedule every hour: check #project-feedback for bug reports.
/goal: don't stop until every report found this run is triaged, actioned,
and responded to. When fixing a bug, use a workflow to explore three
solutions in parallel worktrees and have a judge adversarially review them.
```

This single prompt composes: `/schedule` (trigger), `/goal` (exit condition), dynamic workflows (parallel exploration), auto mode (unattended execution), adversarial review (quality gate). This is the complete [[Harness Engineering]] stack in one prompt.

---

## The Decision Framework (Summary Table)

| Loop | You hand off | Use when | Reach for |
|------|------------|---------|-----------|
| Turn-based | The check | Exploring or deciding | Custom verification skills |
| Goal-based | The stop condition | You know what done looks like | `/goal` |
| Time-based | The trigger | Work happens on a schedule / external system | `/loop`, `/schedule` |
| Proactive | The prompt | Work is recurring and well-defined | All + dynamic workflows |

**Key**: Start with the simplest loop. Not all tasks require complex loops.

## Maintaining Code Quality in Loops

- **Keep codebase clean**: Claude follows existing patterns and conventions. Clean patterns → better loop output.
- **Give Claude a way to verify its own work**: Encode what "good" looks like with skills (see [[Claude Code Skills]] and [[Verification Loop]]).
- **Make docs easy to reach**: Framework/library docs kept accessible in context.
- **Second agent for code review**: Fresh context = less bias, not influenced by main agent's reasoning. Use `/code-review` or GitHub Code Review integration.
- **Fix the system, not just the instance**: When an individual result misses the standard, encode the fix as a rule/skill so all future iterations improve.

## Managing Token Usage in Loops

- **Right primitive + right model**: Smaller tasks don't need multiple agents. Some work uses cheaper/faster models.
- **Define clear stop criteria**: Be specific — so Claude arrives at done sooner (but not too soon).
- **Pilot before large runs**: Dynamic workflows can spawn hundreds of agents. Test on a small slice first.
- **Use scripts for deterministic work**: Running a script < reasoning through steps. A PDF skill can ship a form-filling script Claude runs each time, instead of re-deriving the code each run.
- **Match interval to change frequency**: Don't run routines more often than the thing you're watching changes.
- **Review usage**: `/usage` (by skills/subagents/MCPs), `/goal` with no args (turns + tokens so far), `/workflows` (per-agent token usage, stop any agent mid-run).
- **Model + effort = biggest cost lever**: See [[Effort Level and Model Selection]].

## Synthesis Notes

This is the structural companion to [[Verification Loop]] (which covers *how* to build checks) and [[Best practices for Claude Code]] (which covers *when* to verify). Together, all three form a complete loop engineering curriculum:
- **This source**: *what kind* of loop to use (taxonomy + primitives)
- **[[Verification Loop]]**: *how* to build the check inside a loop
- **[[Best practices for Claude Code]]**: *gate strength* levels and autonomous operation patterns

The **proactive loop** is the most significant concept here because it formalises what [[AI Code Migration]] and overnight autonomous test runs do in practice — a scheduled trigger, goal-based exit conditions, parallel dynamic workflows, and auto mode. The migration article used this pattern; this article names and systematises it.

The **"fix the system, not the instance"** quality principle directly echoes [[AI Code Migration]]'s rule-propagation mechanic: when a reviewer catches a mistake across many files, the fix is a rulebook sentence (not per-file patches). The same principle now stated as a general loop engineering best practice.

The insight that **scripts are cheaper than reasoning** is a subtle but important cost-optimisation principle: for deterministic work (form-filling, PDF manipulation, data transformation), packaging logic as an executable script that Claude runs is far more token-efficient than having Claude reason through the steps each time.

Cross-references: [[Loop Engineering]], [[Verification Loop]], [[Claude Code Skills]], [[Claude Code Hooks]], [[Best practices for Claude Code]], [[AI Code Migration]], [[Effort Level and Model Selection]], [[Harness Engineering]].
