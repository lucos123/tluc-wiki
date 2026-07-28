---
title: Loop Engineering
date: 2026-07-28
tags:
  - concept
  - agentic-design
  - claude-code
  - harness-engineering
---

# Loop Engineering

The practice of designing agent workflows as explicit **loops** — cycles of work that repeat until a stop condition is met — rather than issuing one-off prompts. A shift from "what to ask" to "how to structure the asking."

## Definition

> **Loops = agents repeating cycles of work until a stop condition is met.**

Loop engineering is the deliberate design of: trigger, stop condition, primitive, verification mechanism, and model/cost strategy for each loop type. It is the operational layer of [[Harness Engineering]] — the point where abstract scaffold design becomes concrete agent behaviour.

## The Four Loop Types

### Turn-Based (the default)
- **Trigger**: User prompt
- **Stop**: Claude judges done OR needs more context
- **Primitive**: The basic agentic loop
- **Use when**: Exploring, deciding, shorter one-off tasks

Every prompt starts a turn-based loop. The human is the stop condition. The key improvement lever is encoding manual checks as [[Claude Code Skills|skills]] so Claude can self-verify without asking.

### Goal-Based (`/goal`)
- **Trigger**: Manual prompt
- **Stop**: Evaluator model confirms goal achieved OR turn cap reached
- **Primitive**: `/goal`
- **Use when**: You know what "done" looks like — verifiable exit criteria

An evaluator model (separate from the working Claude) checks the condition after each turn and sends Claude back to work if unmet. Claude never judges "good enough" — the evaluator does. Deterministic criteria (test counts, score thresholds) are most effective.

```
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
```

### Time-Based (`/loop` and `/schedule`)
- **Trigger**: Time interval
- **Stop**: User cancels OR work naturally completes
- **Primitives**: `/loop` (local machine), `/schedule` (cloud, research preview)
- **Use when**: Recurring work or need to poll external systems

```
/loop 5m check my PR, address review comments, and fix failing CI
```

### Proactive (fully autonomous)
- **Trigger**: Event or schedule — no human in real-time
- **Stop**: Each task exits on goal; routine runs until turned off
- **Primitives**: `/schedule` + `/goal` + dynamic workflows + auto mode
- **Use when**: Recurring, well-defined work streams (bug reports, issue triage, migrations, dependency upgrades)

The most powerful composition. Example — autonomous feedback triage:
```
/schedule every hour: check #project-feedback for bug reports.
/goal: don't stop until every report found this run is triaged, actioned,
and responded to. When fixing a bug, use a workflow to explore three solutions
in parallel worktrees and have a judge adversarially review them.
```

This single prompt composes trigger + exit condition + parallel exploration + unattended execution + adversarial quality gate — the complete [[Harness Engineering]] stack.

## LangChain vs. Claude Code Loop Taxonomies

The concept of Loop Engineering is universal, but different frameworks categorize them slightly differently. LangChain's taxonomy maps closely to Claude Code's but explicitly introduces the concept of the **Hill-Climbing / Self-Improvement Loop** as the highest tier.

| Level | LangChain Taxonomy | Claude Code Equivalent | Focus |
|-------|--------------------|------------------------|-------|
| 1 | **Core Agent Loop** (Model + Tools) | **Turn-Based** | Task execution |
| 2 | **Verification Loop** (Grader) | **Goal-Based** | Reliability & Quality |
| 3 | **Event-Driven Loop** (Triggers) | **Time-Based** | Integration & Usage |
| 4 | **Hill-Climbing Loop** (Self-Improvement)| **Proactive** (with Eval) | System improvement |

### The Hill-Climbing Loop (Level 4)
While Claude Code's proactive loop focuses on autonomous *work* (e.g., triaging bugs), LangChain's Hill-Climbing loop focuses on autonomous *self-improvement*.
- **Mechanism**: A background agent runs over the **traces** of past executions.
- **Action**: It identifies failures and autonomously updates the agent's prompts, tools, memory, and skills, porting changes back to the source code.
- **Prerequisite**: Requires a robust **eval suite**. An agent cannot safely self-improve its own harness without evals to verify that the change is an actual improvement.
- **The Principle**: "The outer loop makes each inner loop more effective."

## The Decision Framework

| Loop | You hand off | Use when | Reach for |
|------|-------------|---------|-----------|
| Turn-based | The check | Exploring or deciding | Custom verification skills |
| Goal-based | The stop condition | You know what done looks like | `/goal` |
| Time-based | The trigger | Work is scheduled / external system | `/loop`, `/schedule` |
| Proactive | The prompt | Work is recurring and well-defined | All + dynamic workflows |

**Start with the simplest loop.** Not all tasks need complex multi-agent compositions.

## Loop Quality Principles

1. **Keep the codebase clean**: Claude follows existing patterns. Clean patterns → better loop output.
2. **Verify inside the loop**: Encode what "good" looks like as skills. The more quantitative, the better. (See [[Verification Loop]].)
3. **Use a second agent for review**: Fresh context = no bias from having done the work. Use `/code-review` or Code Review on GitHub.
4. **Fix the system, not the instance**: When one result fails, encode the fix as a rule/skill so all future iterations improve. (Same principle as [[AI Code Migration]]'s rule-propagation mechanic.)
5. **Make docs reachable**: Framework docs kept accessible so Claude has authoritative references.

## Token Cost Management

- **Right primitive + right model**: Don't spawn multi-agent loops for simple tasks.
- **Define precise stop criteria**: Claude reaches "done" sooner without over-running.
- **Pilot before large runs**: Dynamic workflows can spawn hundreds of agents. Test on a slice first.
- **Scripts over reasoning for deterministic work**: Running a script is far cheaper than having Claude reason through steps each time. Package deterministic logic as an executable.
- **Match interval to change frequency**: Don't poll faster than the thing you're watching changes.
- **Monitor**: `/usage`, `/goal` (turns + tokens), `/workflows` (per-agent usage; can stop any agent mid-run).
- **Model + effort are the biggest cost levers**: See [[Effort Level and Model Selection]].

## Relationship to [[Verification Loop]]

[[Verification Loop]] is the internal mechanism *inside* a loop — the check-and-fix cycle that runs within a single turn or goal iteration. Loop Engineering is the *outer* structure — which loop type to use, how to trigger it, when to stop it.

```
Loop Engineering  (outer: which loop type, when, how stopped)
    └── Verification Loop  (inner: what check runs, how failure is fixed)
```

## Relationship to [[Harness Engineering]]

Loop engineering is where harness design becomes operational. The harness provides the tools; loop engineering specifies *how often*, *under what conditions*, and *with what quality gates* those tools are used. The proactive loop is the harness running fully autonomously — no human in the loop.

## Progression of Autonomy

```
Turn-based → Goal-based → Time-based → Proactive
Human decides each turn   Human decides once   System decides always
```

Moving right along this spectrum:
- Removes more human bottlenecks
- Requires more precise stop conditions and quality gates
- Increases risk of runaway token spend (mitigation: pilots, turn caps, model selection)

## Key Insight: "Fix the System, Not the Instance"

When a loop produces a bad result, the instinct is to fix that result. The loop engineering reflex is to ask: **what rule or verification step would have caught this?** Encode the answer so the loop never produces that failure again. This is the agentic equivalent of a CI pipeline rule or a linter config — policy over patches.
