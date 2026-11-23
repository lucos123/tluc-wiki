---
name: sharpen
description: >
  Clarify ambiguous, contested, or multi-fork briefs before execution via either a 3-part
  goal playback (Goal, Problem/Assumptions, Success Check) or full brief sharpening
  (Consumer, 4-Question Expert Lens, Observable Done-Check, Non-Goals, and at most one
  clarifying fork). Triggers on "sharpen", "clarify brief", "in your own words",
  "scope this task", "làm rõ yêu cầu", or "chốt phạm vi trước khi làm".
argument-hint: "[--playback] <vague brief or task>"
allowed-tools:
  - read_file
  - ask_question
  - run_command
metadata:
  credits:
    task-aiming-and-playback: pstack
    author: Lauren Tan
    adapted-from: oh-my-claudecode (sharpen, in-your-own-words)
---

# Sharpen

Aim an ambiguous request at its concrete consumer and verifiable exit check before executing — without locking implementation choices that execution should decide.

## When to Use vs. Skip

- **Use**: A brief has unclear scope, conflicting constraints, or multiple interpretations ahead of substantial work (`output/reports/`, `mem/projects/`, new skills, or SOP playbooks).
- **Skip**: Specific, unambiguous, or small routine tasks — execute directly and report the evidence.

## Mode A — Quick Playback (`--playback` or Fast Alignment)

Before running edits on an ambiguous task, play the request back in **your own words** (never repeat user wording verbatim):

1. **Goal**: What concrete deliverable or state the user gets when finished.
2. **Problem & Assumptions**: What blocks the goal, plus assumptions named inline (`"Assuming output/reports/, not wiki/concepts/"`).
3. **Success Check**: The observable command, render, or behavior proving it worked.

Close with: *"Right? Correct me where I drifted."* Wait for confirmation on risky or irreversible changes; proceed and report the chosen interpretation on reversible work.

## Mode B — Full Brief Sharpening (Default)

1. **Name the Consumer**: Identify who uses the result (wiki reader, TVV team, script caller) and what changes for them observably.
2. **Apply the 4-Question Expert Lens** (*deeper, not bigger*):
   - What would a top specialist include that the request left unstated?
   - What rawest source (`raw/`, official docs, real logs) outranks pre-digested summaries?
   - Which `tluc-wiki` tools or skills (`wiki-query`, `deep-research`, `lint_wiki.py`) fit best?
   - What independent **outside check** beyond opinion proves the output holds?
3. **Name the Done-Check**: State the cheapest observable pass condition (command output, passing tests, rendered links).
4. **Name Non-Goals**: List explicitly what stays out of scope this round.
5. **At Most One Question**: Ask **one** focused question (`ask_question` for multi-option forks; plain text for yes/no) only if two valid interpretations alter the work materially; otherwise state your choice and proceed.
6. **Escalate When Unsharpenable**: If neither a consumer nor a done-check can be named, stop and recommend `/grill-me` for a structured interview.

## Rules & Examples

- Sharpen the **target**, not implementation steps unless the user pinned them.
- Keep sharpened briefs `<= 250` words so a fresh session with zero chat history can execute them.
- Worked EN/VI examples live in [playback-and-examples.md](./references/playback-and-examples.md).

## Deterministic Verification Gate

Validate written briefs or playbooks with [check_brief.py](./scripts/check_brief.py):

```powershell
python .agents/skills/sharpen/scripts/check_brief.py "<brief-file>" --strict
```
