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
  - view_file
  - write_to_file
  - replace_file_content
  - grep_search
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
- Ensure zero hallucinated claims — root all citations in existing wiki/source pages.
- Ensure Mermaid diagrams follow valid syntax.

### Step 4 — Save & Register Output
1. Write the file to `output/<category>/<Filename>.md`.
2. Update `index.md` under `## Generated Deliverables (output/)`.
3. Append log entry to `wiki/log.md`: `## [YYYY-MM-DD] write | <Output Title>`

### Step 5 — Embedded Verification Gate
Run structural health check to verify all output citations resolve to valid pages:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```
Confirm `"total_broken_links": 0` before presenting completion report to the user.
