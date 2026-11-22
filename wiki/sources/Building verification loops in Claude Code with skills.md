---
title: Building verification loops in Claude Code with skills
date: 2026-07-28
tags:
  - source
  - claude-code
  - agentic-design
  - verification
  - harness-engineering
source: "raw/articles/claude-code/building-verification-loops-in-claude-code-with-skills.md"
---

# Building verification loops in Claude Code with skills

**Source File**: `raw/articles/claude-code/building-verification-loops-in-claude-code-with-skills.md`
**Original URL**: https://claude.com/blog/building-verification-loops-in-claude-code-with-skills
**Author**: Delba de Oliveira, Claude Code team

How to convert manual quality checks into [verification loops](../concepts/Verification%20Loop.md) — automated, iterative cycles where Claude checks and fixes its own work before responding. The article covers built-in support, skill creation, and a progression of deployment modes.

## The Agentic Loop

All agentic coding sessions follow a core loop:

```
Gather context → Take action → Verify results → (loop if needed)
```

Verification is how agents check their work before responding. [Claude Code](../entities/Claude%20Code.md) already infers deterministic signals from the codebase — type checkers, linters, tests, runtime errors. **Everything Claude can't infer becomes a manual check by the human.** Verification loops convert those manual steps into skills Claude runs itself.

## Built-In Verification Support

Six mechanisms that work before writing any custom skill:

| Mechanism | What it does |
|-----------|-------------|
| `/verify` skill | Builds, runs, and observes changes in the application. |
| **Toolchain integration** | Catches and acts on error codes from linters, compilers, etc. Best practice: list exact build/test commands in `CLAUDE.md` so Claude doesn't have to infer them. |
| **Code Review** (research preview) | Managed multi-agent service that runs automated review passes on PRs. Comment `@claude` on a finding to close the loop from within GitHub. |
| **GitHub Actions** | Invoke a verification skill on every push or PR via a defined job. Same checks, every change, no author dependency. |
| **Spec validation** | A skill that checks each change against a markdown spec in the repo and fixes violations. |
| **Rubrics in Claude Managed Agents** (beta) | A managed service with a separate grader agent that verifies outcomes against a rubric. Failures loop back for rework automatically. |

## Creating a Custom Verification Loop

**Step 1 — Write down what you check manually.** Start from existing habits. If you keep making the same corrections after Claude's output, those corrections are the loop's content.

**Step 2 — Make it a skill.** Fastest path: install the skill-creator plugin and run `/skill-creator Create a skill for verifying X. Interview me about my workflow.`

Manual path: drop a `SKILL.md` into `.claude/skills/<name>/`.

**Minimal skill example** (`verify-log-hygiene`):
```markdown
---
name: verify-log-hygiene
description: Check that error logs include the request ID and never
  include the request body. Use when the diff touches error handling
  or logging.
allowed-tools: [Read, Edit, Grep]
---
Read the error-handling paths in the current diff.

For each log call on an error path, confirm it includes the request ID
and does not pass the request body, headers, or any user-supplied payload.

Report each violation with file:line, then fix it.
```

**Key insight**: The check doesn't need to be qualitative to belong here. "Reject any migration that drops a column without a backfill step" is a deterministic, project-specific rule no generic linter catches — but a skill will.

## Four Deployment Modes

### 1. Standalone
You invoke it explicitly after the artifact exists. Best for **cross-cutting checks** that don't apply every time: pre-commit security scans, accessibility audits, license-header verification.

*Signal you've outgrown it*: when you run it after every change. Promote to Embedded or Chained.

### 2. Embedded
The check fires automatically as part of the **producing skill**. Simplest form: append one or two lines to the producing skill's body (e.g., `After creating the component file, run eslint on it and address any errors before reporting completion.`).

**Constraints**:
- Only works for skills you own (hand-written or project-level SKILL.md).
- Built-in and plugin-managed skills are off-limits for embedding.
- Skip for cross-workflow checks — those belong in Standalone.

### 3. Chained
One skill calls another at its end. The Anthropic Claude Code team's daily chain:
```
/code-review → /simplify → /verify → /design (if UI touched)
```

**Wrapper skill pattern** — for adding verification to skills you *can't* modify:
```markdown
# .claude/skills/safe-refactor/SKILL.md
Run /simplify on the current diff first.
When /simplify finishes, invoke /verify-no-public-api-changes.
```
What was a personal habit ("I always run /verify after /simplify") becomes a contract that runs automatically.

**Trade-off**: chaining trades flexibility for automation and increases token spend. Test loops before deploying broadly.

### 4. On Every PR (Team Infrastructure)
The same skills and rubrics applied via GitHub Actions to every PR, regardless of author. "Verification stops being personal infrastructure and becomes team infrastructure."

Hold off on PR-wide gates while the chain is still in flux — every adjustment becomes a team-visible event.

## Synthesis: The Loop Engineering Progression

```
Identify manual check
       ↓
Try /verify built-in first
       ↓
Write procedure in plain English
       ↓
Create skill (skill-creator or manual)
       ↓
Invoke on new task → confirm → iterate
       ↓
Add chaining for end-to-end flow
       ↓
Promote to PR-level team gate
```

Each step pushes the check from "something I remember to do" toward "something the system always does."

## Synthesis Notes

This source operationalises the verification principles described in [Best practices for Claude Code](Best%20practices%20for%20Claude%20Code.md) (which names four gate strengths: in-prompt, `/goal`, Stop hook, verification subagent). Those are *when* to verify; this article explains *how* to structure the verification loop and where to deploy it.

The four deployment modes (Standalone → Embedded → Chained → On every PR) form a natural maturity ladder. Each level removes a dependency on human memory and adds it to the harness — the core [Harness Engineering](../concepts/Harness%20Engineering.md) motion.

The **wrapper skill pattern** is particularly useful: it makes the "can't modify this skill" limitation irrelevant by creating a thin orchestration wrapper. This is analogous to the Adapter pattern in software design — adapting an interface without modifying the original.

The **Rubrics in Claude Managed Agents** feature represents a fully managed version of the verification loop — where even the grader is an agent and failures loop back automatically. This is the endpoint of the progression: a system that generates, implements, verifies, and re-iterates without human intervention.

Cross-references: [Verification Loop](../concepts/Verification%20Loop.md), [Claude Code Skills](Claude%20Code%20Skills.md), [Claude Code Hooks](Claude%20Code%20Hooks.md) (deterministic complement), [Best practices for Claude Code](Best%20practices%20for%20Claude%20Code.md), [AI Code Migration](../concepts/AI%20Code%20Migration.md) (verification loops as core mechanism), [Harness Engineering](../concepts/Harness%20Engineering.md).
