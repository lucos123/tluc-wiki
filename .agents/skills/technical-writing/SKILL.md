---
name: technical-writing
description: >
  Write, edit, or tighten technical prose and status replies across tluc-wiki (output/reports,
  output/documents, output/summaries, output/posts, wiki/analyses, READMEs, RFCs, commit
  messages, and PR descriptions). Triggers when the user asks to write cleanly, remove AI fluff,
  tighten a draft, check prose quality, or apply technical-writing / minimal-prose standards.
argument-hint: "<path-to-markdown-file | topic-or-surface>"
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
metadata:
  credits:
    layered-writing-standard: pstack
    author: Lauren Tan
    adapted-from: oh-my-claudecode (technical-writing + minimal-prose-discipline)
---

# Technical Writing

Produce shipping-grade technical documents and crisp conversational updates in `tluc-wiki`: outcome first, one authoritative home per fact, verifiable evidence inline, and zero AI filler.

## 1. The Five-Rule Standard

1. **Outcome First**: Lead sentence states what changed, for whom, and what the reader can do now; background context follows only after the reader knows why it matters.
2. **One Meaning, One Home**: Keep each canonical definition or rule in one authoritative file (`wiki/concepts/`, `ctx/rules/`, `GEMINI.md`) and link elsewhere via Standard Relative Markdown Links (`[Page Name](../concepts/Page%20Name.md)`, RFC 3986 percent-encoded) instead of duplicating text that drifts.
3. **Checkable Statements**: Replace vague adjectives (e.g., `"fast"`, `"significantly better"`, `"vượt trội"`) with verifiable metrics, commands, file paths, or cited benchmarks (`0.8s, 28/28 pass`). Distinguish **Verified** evidence from **Inferred** claims explicitly.
4. **Layered Structure**: Summary / verdict first $\rightarrow$ structured comparison tables or steps $\rightarrow$ edge cases and references. Each layer must stand on its own so readers can stop at any depth.
5. **Zero Filler & AI Tells**: Cut throat-clearing (e.g., `"In today's fast-paced world..."`, `"Trong thời đại công nghệ..."`), pleasantries, and decorative tables restating prose. Delete more than you add.

## 2. Surface Playbook (`tluc-wiki`)

| Surface | Opening & Required Structure | Verification Target |
| :--- | :--- | :--- |
| **Reports & Analyses** (`output/reports/`, `wiki/analyses/`) | Executive thesis first; evidence-backed comparison matrix; explicit trade-offs & `> ⚠️ **Evolving claim**` notes; nested sub-bullets in `## Related Pages` for `>= 3` links | Grounded in `wiki/sources/` or `raw/` paths + `lint_wiki.py` |
| **Docs & RFCs** (`output/documents/`) | Problem, hard constraints, options evaluated (why losers lost), decision, concrete rollout steps | Concrete acceptance checks per step |
| **README & Onboarding** | What it is, who it is for, shortest working command/example, then architecture tree | Every command copy-pastable and verified |
| **Commits & PRs** | Commit subject `<= 72` chars stating *what* changed; body states *why* and the constraint; PR includes claim + before/after evidence + reversibility | Exact test command & observed counts |
| **Chat Replies & Status Reports** | Read [minimal-prose-discipline.md](./references/minimal-prose-discipline.md) before tightening conversational replies, status updates, or session pointers | Protected core quoted byte-for-byte |

## 3. Bilingual & Formatting Guardrails (EN / VI)

- **Protected Technical Core**: Keep English identifiers, formulas, CLI flags, commands, paths, and error outputs exact inside Vietnamese prose; never paraphrase numbers or invert negators.
- **KaTeX Dollar Safety**: Escape literal currency `$` as `\$` in prose (e.g., `\$5.00` và `\$30.00`) or wrap inside backticks so KaTeX never turns prose between two dollar signs into math.
- **Standard Markdown Links Only**: Never emit `[[Wikilinks]]`; encode paths with `quote(rel_path, safe="/-._~")`.

## 4. Deterministic Verification Gate

Run [check_prose.py](./scripts/check_prose.py) on any authored or edited document before finalizing (`--strict` exits `1` on warnings too):

```powershell
python .agents/skills/technical-writing/scripts/check_prose.py "<target-file>" --strict
```

1. Confirm `"error": 0` (`legacy-wikilink`) and resolve or justify every `ai-filler-phrase`, `vague-unquantified-claim`, `katex-currency-collision`, `dense-related-links`, and `long-intro-wall` warning.
2. When modifying files inside `wiki/`, `mem/`, or `output/`, also run `python .agents/skills/wiki-lint/scripts/lint_wiki.py` to confirm `total_broken_links: 0`.
