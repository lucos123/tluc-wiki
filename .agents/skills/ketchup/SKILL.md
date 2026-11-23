---
name: ketchup
description: >
  Catch the user up quickly after stepping away from a session: a 1-3 sentence executive
  summary, one scannable status line per action item with concrete file/log/git evidence,
  and explicit open questions or blockers. Triggers on "ketchup", "catch me up",
  "what did I miss", "session status", "tóm tắt tình hình", or "nãy giờ làm tới đâu rồi".
argument-hint: "[--last-turns N]"
allowed-tools:
  - run_command
  - read_file
  - manage_task
  - manage_subagents
metadata:
  credits:
    session-catchup: pstack
    author: Lauren Tan
    adapted-from: oh-my-claudecode (ketchup)
---

# Ketchup

Summarize everything that happened while the user was away so they can act immediately without scrolling through long tool logs.

## Workflow

1. **Gather Live Workspace & Session Evidence**:
   Run [gather_status.py](./scripts/gather_status.py) to inspect the current git branch, changed files across `wiki/`, `mem/`, `output/`, and `.agents/`, recent `wiki/log.md` entries, and (if passed) recent `transcript.jsonl` turns:
   ```powershell
   python .agents/skills/ketchup/scripts/gather_status.py --format markdown
   ```
   When background commands or subagents might be active, also check `manage_task(Action="list")` and `manage_subagents(Action="list")`.
2. **Deliver the 3-Part Catch-Up Output**:
   - **Executive Summary** (`1–3` sentences): Current state of the work and the single item needing attention first.
   - **Action Items** (`1` line each): `[done | failed | running | blocked]` + exact evidence pointer (`wiki/log.md#L...`, modified file path, or observed test count).
   - **Open Questions & Blockers**: Everything waiting on user confirmation or blocked by a concrete error, naming why it is blocked.

## Hard Rules

- Account for every operation since the user's last message; hiding or softening a failure is unacceptable.
- Report in-flight background tasks and subagents strictly as `running` — never predict results before notifications arrive.
- Keep each action item to one scannable line with zero narrative paragraphs inside the item list.
