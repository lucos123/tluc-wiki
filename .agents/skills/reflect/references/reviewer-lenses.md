# Reviewer Lenses (Antigravity 3-Panel Audit)

Each read-only `research` subagent audits the session `transcript.jsonl` (checking `transcript_full.jsonl` when `truncated_fields` hides key details) through **one** lens and returns at most **3 findings** with exact line citations.

---

## 1. Tooling Reviewer

Audit tool efficiency, script coverage, and context hygiene:
- Which workspace skills (`.agents/skills/*`) or built-in tools were invoked too late, too early, or skipped?
- Where did sequential tool calls waste turns instead of batching independent reads, searches, or edits?
- Which PowerShell, path-encoding, or syntax errors repeated and belong in a deterministic helper script or test?
- Were redundant file reads or multi-megabyte tool outputs inflating context (`input_tokens` vs `cache_read_tokens`)?
- Where could the agent have fetched state via local scripts or tools instead of asking the user manually?

## 2. Judgment Reviewer

Audit decision quality, root-cause rigor, and verification discipline:
- Where did edits start before reading target context or verifying assumptions on disk?
- Which fixes patched symptoms instead of eliminating the root cause across all callers?
- Which completion claims outran actual tool or test output?
- Where should the agent have paused to ask/re-plan (or proceeded without over-asking)?
- Which rule in `GEMINI.md` or `ctx/rules/` would have prevented the costliest mistake?

## 3. Divergent Reviewer

Audit missed alternatives and workflow simplicity:
- If the session restarted from turn 1, what cleaner first step would save the most work?
- Where did manual file-by-file edits ignore a deterministic codemod, batch script, `run_workflow`, or parallel `invoke_subagent` fan-out?
- What assumptions did the lead accept without testing an outside check?
- Watching the session at 10x speed, what single bottleneck stands out most?

---

## Required Finding Format

Return at most 3 items using this exact schema:

```text
FINDING: <one concrete, checkable sentence>
EVIDENCE: transcript.jsonl:L<line> (step_index=<N>) — <brief verbatim quote or observed command/error>
RECURRENCE: every-session | sometimes | once
ENFORCEMENT: script-or-test | lint-rule | ctx-rule | skill-text | note-only
PROPOSED-EDIT: <target file path in .agents/skills/, ctx/rules/, or GEMINI.md + section + concrete change>
```
