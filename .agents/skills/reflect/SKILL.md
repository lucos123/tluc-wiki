---
name: reflect
description: >
  Audit an Antigravity session transcript with a 3-lens read-only panel (tooling, judgment,
  divergent alternatives) to extract cited recurring lessons and propose human-approved updates
  to .agents/skills/, ctx/rules/, or GEMINI.md. Triggers on "reflect", "what did we learn",
  "audit this session", "bank session lessons", or "tổng kết bài học / cải thiện skill".
argument-hint: "[--last-turns N | path-to-transcript.jsonl]"
allowed-tools:
  - read_file
  - run_command
  - invoke_subagent
  - edit_file
  - write_file
metadata:
  credits:
    transcript-review-panel: pstack
    author: Lauren Tan
    adapted-from: oh-my-claudecode (reflect)
---

# Reflect

After a complex or high-friction session, run an independent 3-lens transcript audit to capture recurring lessons before they evaporate — and apply skill or rule improvements only with explicit user approval.

## When to Use vs. Skip

- **Use**: A long session surfaced repeated errors, missed skills, wasted retries, or reusable shortcuts worth encoding.
- **Skip**: Routine short sessions with zero anomalies, or when the user only wants a status recap.

## 5-Step Workflow

### Step 1 — Index the Transcript First
Run [summarize_transcript.py](./scripts/summarize_transcript.py) against `<appDataDir>\brain\<conversation-id>\.system_generated\logs\transcript.jsonl` (pass `--last-turns 15` on multi-day logs) so reviewers get exact line anchors without blowing context:

```powershell
python .agents/skills/reflect/scripts/summarize_transcript.py "<path-to-transcript.jsonl>" --last-turns 15 --format markdown
```

### Step 2 — Seat the 3-Lens Panel in Parallel
Read [reviewer-lenses.md](./references/reviewer-lenses.md) and launch **three** read-only subagents in one parallel turn via `invoke_subagent` (`TypeName: "research"`):
1. `Role: "Tooling Reviewer"` — tool/skill choices, batching, script gaps, PowerShell pitfalls, cache/token waste.
2. `Role: "Judgment Reviewer"` — premature edits, symptom fixes, unverified claims, pause/proceed timing.
3. `Role: "Divergent Reviewer"` — missed simpler paths or built-in capabilities (`run_workflow`, `ask_question`, `invoke_subagent`).

Hand every reviewer the `transcript.jsonl` path (noting `transcript_full.jsonl` for lines with `truncated_fields`), the compact digest from Step 1, and its single lens. Require at most **3 findings per reviewer**, each backed by `transcript.jsonl:L<line>`.

### Step 3 — Wait for Every Reviewer (Reactive Wakeup)
Stop calling tools and wait for subagent notifications instead of polling. Wait until all 3 reviewers complete before synthesizing; if a reviewer times out or fails, name that seat as missing rather than dropping it silently.

### Step 4 — Synthesize & Climb the Enforcement Ladder
Merge duplicate findings, drop uncited claims, quote user rulings verbatim, and rank surviving lessons by `recurrence x impact`:
- **`every-session`**: Encode at the highest practical enforcement level (**script or unit test** $\rightarrow$ **lint check** $\rightarrow$ **`ctx/rules/`** $\rightarrow$ **`.agents/skills/<name>/SKILL.md`**), or propose a new skill via `workflow-skill-creator`.
- **`sometimes`**: Add a targeted gotcha note in the matching skill or `ctx/rules/`.
- **`once`**: Report as a one-line observation; do not bloat permanent skills.

### Step 5 — Propose First, Edit Only After User Approval
Present the ranked findings and concrete proposed diffs (exact target file, section, wording, or script change). **Never modify `.agents/skills/`, `ctx/rules/`, or `GEMINI.md` silently** — apply edits only after explicit user confirmation, then verify with unit tests and `lint_wiki.py`.

## Hard Rules

- Every finding cites exact `transcript.jsonl:L<line>` and `step_index`; uncited claims are dropped.
- Reviewers stay read-only; only the lead coordinator edits files after approval.
- Report observations about user choices neutrally, never as corrections.
- Never commit, push, or open a PR as part of reflection.
