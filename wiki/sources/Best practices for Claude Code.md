---
title: Best practices for Claude Code
date: 2026-07-28
tags:
  - source
  - best-practices
  - claude-code
  - agentic-design
source: "[[raw/best-practices-for-claude-code.md]]"
---

# Best practices for Claude Code

**Source File**: [[raw/best-practices-for-claude-code.md]]

Official Anthropic guide covering patterns for effective use of [[Claude Code]] across context management, verification, communication, environment setup, session management, and scaling with parallel sessions.

## Key Concepts

- **Context Window as Primary Constraint**: All best practices stem from one constraint — the context window fills fast and LLM performance degrades as it fills. A single debugging session can consume tens of thousands of tokens. Core remedies: `/clear` between unrelated tasks, `/compact` with targeted instructions (e.g., `/compact Focus on API changes`), `/btw` for throwaway side-questions that never enter history, and subagents for investigation.

- **Verification Loop Design**: Give Claude a runnable check so "looks done" is never the only signal. Four levels of gate strength:
  1. **In-prompt**: ask Claude to run & iterate in the same message.
  2. **`/goal` condition**: a separate evaluator re-checks after every turn until the condition holds.
  3. **Stop hook**: a shell script blocks the turn from ending until it passes (overridden after 8 consecutive blocks).
  4. **Verification subagent**: a fresh model tries to refute the result (no bias from having written the code).

- **Explore → Plan → Code**: Use plan mode to separate research from implementation. Skip planning only when the task is trivial (one sentence diff). After Claude interviews you and writes a spec to `SPEC.md`, start a fresh session to execute — clean context focused on implementation.

- **CLAUDE.md as Persistent Context**: CLAUDE.md loads every session; treat it like code. Use `@path/to/file` imports for modularity. Place it in `~/.claude/` (global), project root (team-shared, checked in), or `CLAUDE.local.md` (personal, gitignored). Keep it short — if a rule gets lost in noise, Claude ignores it. Emphasis markers (`IMPORTANT`, `YOU MUST`) improve adherence for critical rules.

- **Environment Setup — Tiered Extensions**: Claude Code extensions form a clear hierarchy:
  - **CLAUDE.md**: always-on persistent context for facts & rules.
  - **Skills** (`.claude/skills/`): modular knowledge & workflows loaded on demand (see [[Claude Code Skills]]).
  - **Hooks** (`.claude/settings.json`): deterministic shell scripts for guaranteed actions (see [[Claude Code Hooks]]).
  - **Subagents** (`.claude/agents/`): isolated task runners with their own tool-set and model.
  - **MCP servers**: external integrations (databases, Notion, Figma).
  - **Plugins** (`/plugin`): bundled skills + hooks + MCP servers from marketplace.

- **Session Management**: Every prompt creates a checkpoint. `Esc+Esc` or `/rewind` opens the rewind menu to restore conversation, code, or both. `/rename` gives sessions descriptive names (treated like git branches). `claude --continue` / `claude --resume` for multi-sitting tasks. After two failed corrections on the same issue, `/clear` and rewrite the prompt.

- **Parallel Sessions & Scaling**:
  - **Non-interactive**: `claude -p "prompt"` for CI, pre-commit hooks, scripts. Add `--output-format stream-json --verbose` for programmatic parsing.
  - **Worktrees**: isolated git checkouts so parallel sessions don't collide.
  - **Auto mode**: `claude --permission-mode auto` — a classifier blocks risky actions and lets routine work proceed unattended.
  - **Agent teams**: automated coordination of multiple sessions with shared tasks, messaging, and a designated team lead.
  - **Writer/Reviewer pattern**: Session A implements, Session B reviews in a fresh context (no bias from having written the code), A fixes gaps.
  - **Fan-out**: loop `claude -p` per file/task; use `--allowedTools` to scope permissions for batch ops.

- **Adversarial Review**: Before counting work as done in unattended runs, use `/code-review` (bundled skill) or a manual subagent prompt to review the diff against the plan in a fresh context. Tell the reviewer to flag only correctness gaps — chasing every style finding leads to over-engineering.

- **Common Anti-patterns**:
  - *Kitchen-sink session*: mixing unrelated tasks → fix with `/clear`.
  - *Correcting loop*: same mistake corrected 2+ times → `/clear` and rewrite with learnings baked in.
  - *Over-specified CLAUDE.md*: rules get lost in noise → ruthlessly prune.
  - *Trust-then-verify gap*: plausible but wrong → always provide a runnable check.
  - *Infinite exploration*: unscoped `investigate X` fills context → use subagents or narrow the scope.

## Synthesis Notes

This source significantly expands on the 2026-06-28 ingest. The biggest additions are:
1. **`/btw`** — side-question overlay that never enters context history (entirely new pattern).
2. **Checkpointing** — `/rewind` restores conversation and/or code state from any earlier prompt checkpoint, enabling risk-free experimentation.
3. **Auto mode** — classifier-gated unattended execution, enabling long autonomous runs without constant approval.
4. **Agent teams** — coordinated multi-session fan-out, moving from "one human, one Claude" to orchestrated agent pools.
5. **Adversarial review as a standard step** — explicitly naming the fresh-context reviewer pattern as a workflow primitive.

Closely related to [[Harness Engineering]] (the "environment shapes the agent" thesis), [[Context Engineering]], and [[Persistent Instruction File]]. The best-practices doc is essentially the practitioner's manual for the theoretical frames established in [[12 Agentic Harness Patterns from Claude Code]].
