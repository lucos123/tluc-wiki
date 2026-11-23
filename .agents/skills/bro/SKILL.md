---
name: bro
description: >
  Restate the previous technical message or a dense wiki page in plain human language —
  zero unexplained jargon or acronyms, keeping every fact, number, and caveat intact.
  Triggers on "bro", "say it plainly", "no jargon", "explain simply", "nói dễ hiểu hơn",
  or "giải thích bình dân".
argument-hint: "[optional path-to-wiki-page or technical excerpt]"
allowed-tools:
  - read_file
metadata:
  credits:
    plain-restate: pstack
    author: Lauren Tan
    adapted-from: oh-my-claudecode (bro)
---

# Bro

Restate the last technical answer — or a specified page in `wiki/` — in plain human language without dropping accuracy.

## Rules

1. **Keep every fact, number, threshold, and unit intact**: Never simplify by omitting constraints, failure counts, or timing figures.
2. **Strip unexplained jargon**: Replace acronyms, internal codenames, and scaffolding terms with plain words in the user's active language (Vietnamese or English).
3. **Introduce actors plainly once**: Name each tool or system plainly at first mention (for example, *"trình kiểm tra link — công cụ tự rà đường dẫn hỏng"*), then keep that plain name consistent.
4. **One clear thought per sentence**: Keep sentences short and direct.
5. **Preserve honesty over smoothness**: If the original explanation overstated a result, hid a failing check, or skipped a caveat, state that gap explicitly instead of polishing it away.
6. **Size follows the facts**: Write as many plain sentences as the facts require — brevity that drops substance defeats plain explanation.
