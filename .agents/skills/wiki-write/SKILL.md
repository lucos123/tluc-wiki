---
name: wiki-write
description: >
  Synthesize and generate formal, shareable deliverables in output/ (reports,
  documents, summaries, posts, visuals) using the wiki knowledge base and user
  context. Triggers when the user asks to write a report, produce a document, draft
  a blog post, create an executive summary, or generate visual diagrams via /wiki-write or natural language.
when_to_use: >
  Use whenever a formal report, research document, executive summary, blog post, or Mermaid visual
  diagram needs to be generated and saved into output/.
argument-hint: "<report|document|summary|post|visual> <title>"
arguments:
  - name: type
    description: "The deliverable category: report, document, summary, post, or visual"
  - name: title
    description: "The title of the deliverable"
allowed-tools:
  - run_command
  - read_file
  - write_file
  - edit_file
---

# Wiki Write Skill

Target Category: `$1` (or `$type`)
Deliverable Title: `$2` (or `$title`)

You are operating the persistent Second Brain (`tluc-wiki`). Your task is to retrieve structured knowledge from `wiki/`, user priorities from `mem/`, and raw sources from `raw/`, and synthesize them into high-quality, shareable deliverables saved in `output/`.

Refer to `examples/write-report-example.md` for a complete execution walkthrough.

## 1. Output Target Categories

| Category | Path | Use Case | Template Reference |
|----------|------|----------|-------------------|
| **Reports** | `output/reports/` | Research reports, multi-source comparisons | `references/deliverable-templates.md` (#1) |
| **Documents** | `output/documents/` | Architecture specs, design whitepapers | `references/deliverable-templates.md` (#2) |
| **Summaries** | `output/summaries/` | Executive summaries, quick digests | `references/deliverable-templates.md` (#3) |
| **Posts** | `output/posts/` | Blog posts, articles, presentations | Standard article format |
| **Visuals** | `output/visuals/` | Mermaid diagrams, visual workflow maps | `references/deliverable-templates.md` (#4) |

## 2. Write Pipeline (Retrieve $\rightarrow$ Draft $\rightarrow$ Refine $\rightarrow$ Output)

### Step 1 — Retrieve Context
1. Read `index.md` and gather all relevant pages across `wiki/concepts/`, `wiki/entities/`, `wiki/sources/`, and `mem/`.
2. Extract verified facts, performance benchmarks, and architectural patterns.

### Step 2 — Select Template & Draft
1. Load the corresponding template from `references/deliverable-templates.md`.
2. Populate frontmatter (`title`, `date`, `tags`, `type`).
3. Draft content using clear section headers, tables, and Standard Relative Markdown Links (`[Page Name](../../wiki/concepts/Page%20Name.md)`).

### Step 3 — Refine & Validate
- Verify zero fabricated claims by anchoring every citation in existing `wiki/` or `raw/` pages.
- **Epistemic & Benchmark Vetting**: Apply [epistemics.md](../deep-research/references/epistemics.md) (5 confidence tiers, zero certainty weasels, side-by-side contradictions, and the 5-step Benchmark & Number Vetting checklist) before citing any speedup, latency, throughput, pricing delta, or eval score.
- Follow prose discipline in [technical-writing](../technical-writing/SKILL.md) for drafts and [diagram](../diagram/SKILL.md) when embedding Mermaid diagrams.

### Step 4 — Save & Register Output
1. Write the file to `output/<category>/<Filename>.md`.
2. Update `index.md` under `## Generated Deliverables (output/)`.
3. Append log entry to `wiki/log.md`: `## [YYYY-MM-DD] write | <Output Title>`

### Step 5 — Embedded Verification Gate
Run structural verification and applicable deliverable checks before finishing:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
python .agents/skills/technical-writing/scripts/check_prose.py "output/<category>/<Filename>.md" --strict
python .agents/skills/deep-research/scripts/check_research.py "output/<category>/<Filename>.md" --strict
python .agents/skills/diagram/scripts/check_diagrams.py "output/<category>/<Filename>.md" --strict
```
Confirm `"total_broken_links": 0` from `lint_wiki.py`, pass `check_prose.py --strict` on text deliverables, run `check_research.py --strict` when reporting benchmarks or comparisons, and run `check_diagrams.py --strict` when Mermaid diagrams are present.
