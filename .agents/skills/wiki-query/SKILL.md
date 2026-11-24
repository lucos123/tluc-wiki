---
name: wiki-query
description: >
  Answer questions using the wiki knowledge base across wiki/, mem/, and output/. Use when the user asks a
  question, requests an explanation, comparison, or analysis of topics covered in the wiki via /wiki-query or natural language.
  Searches the index, reads relevant pages, synthesizes an answer with citations, and optionally compounds valuable answers back into the wiki.
when_to_use: >
  Use whenever a user asks a question, requests a deep-dive analysis, comparison, or factual lookup
  across wiki/, mem/, output/, or raw sources.
argument-hint: "<question or query topic>"
allowed-tools:
  - run_command
  - read_file
  - write_file
  - edit_file
---

# Wiki Query Skill

Target Query: `$ARGUMENTS`

You are answering a question using a persistent Second Brain (`tluc-wiki`). Your goal is to provide a well-cited, synthesized answer spanning `wiki/`, `mem/`, and `output/`. Follow every step below precisely.

Refer to `examples/query-workflow-example.md` for a complete execution walkthrough.

## 1. Multi-Layer Search Strategy

Execute search across 4 distinct layers:

### Layer 1: Fast Helper Script Execution
Run the query search utility to quickly scan `index.md` and content pages outside LLM context:
```powershell
python .agents/skills/wiki-query/scripts/query_wiki.py "$ARGUMENTS"
```

### Layer 2: Master Index Scan & Targeted Page Reads
Read matching pages identified by the script across `wiki/`, `mem/`, and `output/`. Extract key metrics and cross-references (Standard Relative Markdown Links `[Page](path.md)`).

### Layer 3: Deep Search (`Select-String` / `rg`)
If Layers 1-2 leave gaps, run `Select-String` (PowerShell) or `rg` via `run_command` to locate exact keyword matches across markdown files in `wiki/`, `mem/`, and `output/`.

### Layer 4: Raw Source Consultation (If needed)
If deeper technical details or original quotes are required, read the underlying raw file in `raw/` (`raw/articles/`, `raw/video-transcripts/`, `raw/notes/`, `raw/pdfs/`).

## 2. Taxonomy, Citation & Epistemic Protocol

Structure the answer using the 5 question types defined in `references/query-taxonomy-guide.md`:
1. **Factual**: Direct specs with single-page citation.
2. **Comparative**: Side-by-side comparison table with multi-page citations.
3. **Analytical**: Deep synthesis, architecture diagrams, trade-off matrix.
4. **Gap-Finding**: Summary of covered vs missing topics.
5. **Exploratory**: Multi-node concept graph tracing.

Follow [epistemics.md](../deep-research/references/epistemics.md) in every synthesis:
- Label uncertain claims using the 5 confidence tiers (`Direct`, `Supported`, `Inferred`, `Speculative`, `Unknown`) and avoid certainty weasel phrases.
- Present conflicting sources side-by-side instead of smoothing contradictions.
- Run the 5-step Benchmark & Number Vetting checklist before quoting any comparative speedup, latency, throughput, cost delta, or eval score.

## 3. Compounding Criteria & Embedded Verification Gate

Follow compounding rules in `references/compounding-rules.md`:
- Compound to `wiki/analyses/` for new multi-source comparisons or syntheses.
- Compound to `output/reports/` for requested deliverables.

If compounding:
1. Write file with YAML frontmatter.
2. Update `index.md` and append log entry to `wiki/log.md`.
3. Run `python .agents/skills/wiki-lint/scripts/lint_wiki.py` (`"total_broken_links": 0`) and, for comparative or benchmark syntheses, `python .agents/skills/deep-research/scripts/check_research.py "<file>" --strict`.

## 4. Log Update
Append exactly one line to `wiki/log.md`:
```
## [YYYY-MM-DD] query | <Short description of the question>
```
