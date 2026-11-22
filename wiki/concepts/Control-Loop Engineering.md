---
title: Control-Loop Engineering
date: 2026-07-29
tags:
  - concept
  - loop-engineering
  - harness-engineering
---

# Control-Loop Engineering

The application of **Classical Control Theory** to agentic software engineering. Introduced by [Kyle Mistele](../entities/Kyle%20Mistele.md) at [HumanLayer](../entities/HumanLayer.md) in [Loop Engineering from First Principles](../sources/Loop%20Engineering%20from%20First%20Principles.md), it frames codebase modification as driving a dynamic system toward a desired state via incremental, measured feedback loops rather than all-at-once code generation.

## Contrast with "Blind Ralph Loops"

| Dimension | Blind Ralph Loop | Control-Loop Engineering |
|-----------|------------------|--------------------------|
| **Approach** | Pipe prompt to agent in unconstrained loop | Incremental state changes guided by sensors |
| **Output** | 40,000-line unreviewable PRs | Daily 1-file/1-procedure small PRs |
| **Use Case** | Single-dev side projects, non-critical systems | Production team codebases with SLAs & regulation |
| **Code Review** | Bypassed or impossible | Mandatory, low-friction, human-in-the-loop |
| **Token Spend** | High runaway costs | Budgeted, targeted, token-efficient |

## The 5 Core Components

1. **Set Point**: The desired end-state of the codebase (e.g. 100% RPC endpoints migrated to new framework).
2. **Sensor**: Measures the current error/violations. Can be deterministic (`ast-grep`, ESLint, `packwerk`), hybrid (React Doctor), or non-deterministic (agent skills).
3. **Controller**: Decides the next incremental control signal (e.g., selecting the smallest violation or highest-telemetry-error procedure to minimize risk).
4. **Actuator**: Agent + Skill applying the change in a single context window, committing and opening a PR.
5. **Disturbance Dampener**: CI check enforcing baseline metrics on main/PRs so teammates don't re-introduce deprecated patterns during active loop runs.

## Operational Patterns

### 1. Human-on-the-Loop Resteering (`FEEDBACK.md`)
Instead of constantly editing prompt templates or checking out branches when an agent makes a mistake, maintain a version-controlled `FEEDBACK.md`. Leaving a `/iterate` comment on a PR triggers the workflow to inspect the diff/comments, fix the code, and write lessons into `FEEDBACK.md` for future loop runs.

### 2. Adaptive Flow Control
To prevent PR stacking and review fatigue, the workflow checks if a PR from a previous run (identified by a loop label) is still open. If unreviewed, the workflow shuts down immediately without generating new work.

### 3. Velocity Scaling
Once a loop's reliability is established, scale velocity by:
- Increasing batch size per context window.
- Spawning separate implementation context windows per item.
- Running parallel workflows assigning PRs across team members.

## Relationship to [Harness Engineering](Harness%20Engineering.md) & [Loop Engineering](Loop%20Engineering.md)

Control-Loop Engineering serves as an operational framework within [Loop Engineering](Loop%20Engineering.md) for team-based production environments. While [Verification Loop](Verification%20Loop.md) provides inner-loop test/linter feedback, Control-Loop Engineering structures the outer control system governing PR generation, team review, and feedback persistence.
