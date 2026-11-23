---
name: deep-research
description: >
  Conduct open-ended, evidence-first investigation across tluc-wiki (wiki/, raw/) and external
  official documentation via search_web and parallel research subagents when facts are unsettled,
  sources conflict, or a high-stakes choice needs 5-tier epistemic labeling (Direct, Supported,
  Inferred, Speculative, Unknown). Triggers on "deep research", "investigate", "verify claim",
  "nghiên cứu chuyên sâu", or "điều tra bằng chứng".
argument-hint: "<research question | claim to verify>"
allowed-tools:
  - read_file
  - run_command
  - search_web
  - invoke_subagent
  - write_file
  - edit_file
metadata:
  credits:
    investigation-epistemics: pstack
    author: Lauren Tan
    adapted-from: oh-my-claudecode (research, why/epistemics, benchmark-checklist)
---

# Deep Research

Replace assumptions with cited evidence across local ground truth and official sources, and state explicitly what remains unknown.

## Scope & Boundary vs. `wiki-query`

- **Use `wiki-query`** for lookups already answered inside existing `tluc-wiki` pages.
- **Use `deep-research`** when questions span `wiki/` + `raw/` + external docs (`search_web`), when sources contradict, or when explicit confidence tiers are needed before deciding.
- Research answers questions — never modify code or unrelated files as a side effect (write to `wiki/analyses/` or `output/reports/` only when requested or compounding approved).

## 5-Step Protocol

1. **Frame the Question & Reject Leading Premises**: State the exact question and what evidence counts as an answer. Treat any hypothesis embedded in the user's request as one candidate to test, not a conclusion to confirm (**Anti-Sycophancy**).
2. **Search Local Ground Truth First**: Check `index.md`, `wiki/`, and `raw/` via `query_wiki.py` or `read_file` before searching externally — local verified sources outrank recollection.
3. **Sweep External Authoritative Sources**: Query primary documentation, official specifications, papers, or changelogs with `search_web`, checking counter-evidence and publication dates.
4. **Scale Deliberately**:
   - *Narrow lookup* $\rightarrow$ investigate directly.
   - *Independent sub-questions* $\rightarrow$ fan out parallel read-only subagents via `invoke_subagent` (`TypeName: "research"`).
   - *Open-ended discovery* $\rightarrow$ continue passes until an additional pass surfaces zero new evidence.
5. **Synthesize with 5-Tier Epistemics**: Follow [epistemics.md](./references/epistemics.md) to assign every claim a tier (**Direct**, **Supported**, **Inferred**, **Speculative**, **Unknown**), quote human rulings verbatim, preserve contradictions side-by-side (`> ⚠️ **Evolving claim**`), and vet measured benchmarks before quoting numbers.

## Required Brief Structure

1. **Question & Scope**
2. **Executive Answer** (outcome first, one paragraph)
3. **Findings by Confidence Tier** (`Direct` / `Supported` / `Inferred` / `Speculative`, each paired with a Markdown link or `file:line` reference)
4. **Contradictions & Trade-offs** (if sources disagree)
5. **What Remains Unknown** (concrete gaps naming every source checked and what was not found)
6. **Recommended Next Step** (or compound cleanly into `wiki/analyses/` / `output/reports/` with Standard Relative Markdown Links)

## Deterministic Verification Gate

Before finalizing any saved brief in `wiki/analyses/` or `output/reports/`, validate citations and epistemic hygiene with [check_research.py](./scripts/check_research.py):

```powershell
python .agents/skills/deep-research/scripts/check_research.py "<target-file>" --strict
```

Also run `python .agents/skills/wiki-lint/scripts/lint_wiki.py` whenever compounding pages inside `wiki/`, `mem/`, or `output/`.
