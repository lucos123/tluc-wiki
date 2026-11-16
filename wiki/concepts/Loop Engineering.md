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

### The Hill-Climbing Loop (Level 4: Self-Improvement)
While Claude Code's proactive loop focuses on autonomous *work* (e.g., triaging bugs), LangChain's Hill-Climbing loop focuses on autonomous *self-improvement*.
- **Mechanism**: A background agent runs over the **traces** and in-situ human review comments of past executions.
- **Production Paradigm**: As implemented in [[Self-Improving Agents]] by [[Warp]] on the [[Anthropic]] platform, an **Outer Improver Skill** running in an orchestration platform (Oz) monitors human PR feedback, generates minimal focused diffs to the **Inner Base Skill**, and opens a Git PR for maintainer approval.
- **Action**: It identifies failures and autonomously updates the agent's prompts, tools, memory, and skills, porting changes back to the source code.
- **Prerequisite**: Requires a robust **eval suite** and verification harness. An agent cannot safely self-improve its own harness without evals to verify that the change is an actual improvement.
- **The Principle**: "The outer loop makes each inner loop more effective." (See [[Self-Improving Agents]] and [[How Warp Builds Self-Improving Agents on Claude]]).

## Control-Loop Engineering (First Principles)

Introduced by [[Kyle Mistele]] at [[HumanLayer]] in [[Loop Engineering from First Principles]], **[[Control-Loop Engineering]]** grounds agentic loop design in Classical Control Theory to solve the problem of unreviewable "blind Ralph loops" in production team codebases.

Key components and patterns include:
- **Set Point & Sensors**: Define target states and measure errors using deterministic tools (`ast-grep`, ESLint) or agent skills.
- **Adaptive Flow Control**: Automatically pauses loop execution if previous PRs generated by the loop remain unreviewed, preventing PR fatigue and stacking.
- **Human-on-the-Loop Resteering**: Uses a version-controlled `FEEDBACK.md` file updated via `/iterate` PR comments to steer agents without high-friction prompt editing.

## Multi-Loop Stacking & The 6 Components

As analyzed in [[Loop Engineering explained in 8min]], agent architectures function by **stacking loops on top of loops**:
1. **Level 1 (Context Loop)**: Tool-calling loop inside [[Context Engineering]] (Model $\rightarrow$ Tool $\rightarrow$ Observation $\rightarrow$ Answer).
2. **Level 2 (Harness Loop)**: PRD/checklist task iteration loop inside [[Harness Engineering]] (Task 1 $\rightarrow$ Task 2 $\rightarrow$ Task 3 with fresh context).
3. **Level 3 (Loop Engineering)**: Self-guided automation loop (Scheduled/Event trigger $\rightarrow$ Harness Run $\rightarrow$ Verification $\rightarrow$ Repeat).

### Addy Osmani's 6 Components of Loop Engineering

To build a self-guided loop that prompts itself, [[Addy Osmani]] identifies 6 core components:
1. **Automation**: Scheduled or event-driven triggers (cron, webhooks, `/schedule`).
2. **Worktrees**: Git worktrees to isolate context and state across parallel task executions.
3. **Skills**: Modular domain execution skills (`SKILL.md`).
4. **Plugins & Connectors**: MCP servers, database bridges, external API integrations.
5. **Sub-agents**: Task specialization and adversarial self-verification (e.g. reviewer/evaluator agents).
6. **State**: Persistent instruction files (`AGENTS.md`), memory, and execution tracking.

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

## Core 4-Stage Cycle, State Spine & Human Safeguards

As structured in [[IBM Technology]]'s [[What Is Loop Engineering Building Better AI Agents]], every loop implementation can also be viewed visually as a 4-stage inner execution ring (`Goal -> Action -> Observe -> Adjust`) surrounded by five engineering pillars:
1. **Triggers**: Scheduled crons and event-driven [[Deterministic Lifecycle Hooks|hooks]] initiating the `Goal`.
2. **Context Engineering**: Compaction ([[Context Window Management]]) and [[Progressive Disclosure]] of [[Agent Skills Architecture|skills]] feeding only high-signal context into each iteration.
3. **The Spine (Persistent State)**: Durable Markdown execution logs inside the loop recording prior attempts, what succeeded, and what failed across passes.
4. **Tools & Subagents**: [[Model Context Protocol|MCP]]/API integrations powering `Action`, and independent checker [[Subagent Architecture|subagents]] supporting `Observe`.
5. **Human-in-the-Loop Safeguards**: Even well-engineered loops require humans to **write verifiable goals**, **write explicit intent** (preventing test-relaxing reward hacks), and **read outputs** to avoid [[Comprehension and Intent Debt]] and cognitive surrender. See [[raw/screenshots/ibm-loop-engineering/06.jpg]] and [[raw/screenshots/ibm-loop-engineering/09.jpg]].
