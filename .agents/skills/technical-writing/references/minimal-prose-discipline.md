# Minimal Prose Discipline (Conversational Replies & Status Reports)

Use this discipline when writing conversational prose to the user: chat replies, task progress summaries, failure reports, and session handoffs. It compresses commentary while protecting technical accuracy and safety.

- **Scope**: Governs in-conversation replies only. Durable artifacts (`wiki/`, `output/`, `mem/`, docs) follow `SKILL.md` and `GEMINI.md`.
- **Language Preservation**: Compresses phrasing style, never changes the user's language (write clear, natural Vietnamese when replying in Vietnamese).

## Core Rules

1. **Protect the Core**: Quote code, commands, file paths, exact error messages, numbers, units, API/CLI names, and commit-type keywords byte-for-byte. Paraphrasing an error string or path creates a wrong error.
2. **Never Drop Meaning-Bearers**: Keep every negator and scope limiter intact (`not`, `never`, `no`, `only`, `except`, and Vietnamese markers `không`, `chưa`, `chỉ`, `trừ`, `ngoại trừ`). Terseness must never flip a truth value or break Vietnamese grammar.
3. **Cut Throat-Clearing**: Remove filler (*"just", "basically", "actually", "như vậy là", "thật ra thì"*), empty pleasantries, and hedges where the tool result is already known. Delete dead lines in the same edit.
4. **Conclusion First, One Term per Referent**: Lead with the outcome ("so what?" in line 1); use consistent terminology throughout rather than rotating synonyms.
5. **No Tool-Call Narration**: Do not narrate visible tool actions (*"Now I will read the file..."*). State only findings, decisions, warnings, or the next step.
6. **Errors & Completions as Plain Facts**:
   - Failure: state *what* failed, *why*, and the *next step* — no apology padding or minimization.
   - Completion: state *what shipped* and *where the verified evidence lives* (`file:///...` links + observed counts).
   - Deferral: always name *when* deferred work happens.
7. **Close on the Next Action**: End on a concrete command, decision question, or pointer the reader can act on immediately.

## Auto-Clarity Safety Suspension

Never compress prose when brevity introduces risk or ambiguity. Revert to full, explicit sentences for:
- Security warnings and irreversible-action confirmations (deletions, overwrites, credential risks).
- Multi-step ordered instructions where dropping a conjunction could reorder execution.
- Technical caveats where terse wording admits two interpretations.

## Pre-Send Check

- Commands, paths, errors, numbers, and negators match tool output byte-for-byte.
- Line 1 answers the user's core question; the last line states the next actionable step.
- Warnings, confirmations, and step sequences use full plain prose.
