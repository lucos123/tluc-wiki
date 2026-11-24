# Agent-Facing Document & Defect-Correction Rules

> Adapted for `tluc-wiki` from `oh-my-claudecode`'s `agent-doc-discipline` and `correct` concepts. Applies to `.agents/skills/*/SKILL.md`, `GEMINI.md`, `ctx/rules/*.md`, and `ctx/prompts/*.md`.

## Part 1 — Agent-Facing Document Discipline

- **Zero-Chat-History Test**: Write every instruction so a fresh session with zero prior chat context can execute it verbatim. Never write vague phrases such as `"like earlier"` or `"keep it clean"`; state exact paths, thresholds, or commands.
- **Checkable Rule + Why**: Pair every rule with a concrete check (metric, regex, exit condition, or command) and the failure mode it prevents.
- **One Meaning, One Home**: Store each canonical workflow, schema, or script contract in one file and point to it using Standard Relative Markdown Links (`[label](relative/path.md)`); never duplicate rule text across multiple `SKILL.md` files.
- **Never Restate Tool Lookups**: Link sibling `scripts/` or `references/` files or run `--help` instead of copying CLI flags, schemas, or directory trees into skill prose.
- **Progressive Disclosure (`< 500` Lines)**: Put quick-start steps and exact commands near the top of `SKILL.md`, keep `SKILL.md` under `500` lines, and move extended rubrics or examples into `references/`.
- **Numbered Steps with Done Criteria**: Any workflow with `3+` sequential steps must use a numbered list where each step specifies its completion check or exit signal.
- **Glanceable Lists**: Start every bullet with a **bold lead** naming the rule or check so agents scanning quickly catch the constraint immediately.
- **Prompt the Positive & Scrape Barnacles**: Write what to do rather than vague prohibitions (`"don't use..."` -> exact replacement tool or command). Whenever editing an agent doc, remove dead paths, obsolete flags, and deprecated pre-Antigravity tool names (`view_file`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `grep_search`).
- **Session Boundary Discipline**: State explicitly when work is `deferred` rather than finished, close replies on the next concrete action, and re-state the active step when resuming mid-flow.

---

## Part 2 — Mistake Elimination Ladder & "Prove It Fires"

When fixing a recurring agent mistake or pipeline defect, climb from Level 1 downward and implement the highest practical enforcement mechanism instead of adding prose reminders first:

1. **Level 1 — Structural / Schema / Static Lint Guard**: Catch violations automatically via repository linters (`lint_skills.py`, `lint_wiki.py`, `check_prose.py`) or strict YAML/schema rules.
2. **Level 2 — Type & Contract Guard**: Enforce invariants through Python type hints, dataclasses, and strict input parsing.
3. **Level 3 — Runtime Fail-Closed Assertion**: Fail loudly with explicit exit code `1` on invalid state (`--strict`, path validation, UTF-8 decoding).
4. **Level 4 — Automated Script / Unit-Tested Transform**: Build a deterministic helper script paired with `unittest` regression tests (`test_*.py`) covering the exact defect.
5. **Level 5 — Rule / Skill Prose (Last Resort)**: Write prose instructions only for judgment calls that deterministic checks cannot capture, or to point to the script that enforces them.

### Verification Gate ("Prove It Fires")

- **Reproduce Failure Before Accepting Fix**: Confirm a new lint rule, script guard, or unit test fails on the targeted bad input before trusting it cleanly passes (`exit 0`) after the fix.
- **Never Weaken Enforcement**: Never lower a lint threshold, drop a `--strict` flag, or relax a `unittest` assertion solely to force a failing check green.
- **Mandatory Post-Edit Check**: Run the skill and rule linter before finishing any edit to `.agents/skills/` or `ctx/rules/`:
  ```powershell
  python .agents/skills/wiki-lint/scripts/lint_skills.py --strict
  ```
