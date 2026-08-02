---
name: wiki-query
description: >
  Answer questions using the wiki knowledge base across wiki/, mem/, and output/. Use when the user asks a
  question, requests an explanation, comparison, or analysis of topics covered in the wiki via /wiki-query or natural language.
  Searches the index, reads relevant pages, synthesizes an answer with citations, and optionally compounds valuable answers back into the wiki.
argument-hint: "<question or query topic>"
---

# Wiki Query Skill

Target Query: `$ARGUMENTS`

You are answering a question using a persistent Second Brain (`tluc-wiki`). Your goal is to provide a well-cited, synthesized answer spanning `wiki/`, `mem/`, and `output/`. Follow every step below precisely.

## 1. Multi-Layer Search Strategy

Execute search across 4 distinct layers:

### Layer 1: Master Index Scan
Read `index.md` to map available pages across `## Concepts`, `## Entities`, `## Sources`, `## Personal Memory & Projects (mem/)`, and `## Generated Deliverables (output/)`.

### Layer 2: Targeted Page Reads
Read identified pages in `wiki/`, `mem/`, or `output/`. Extract key facts, metrics, and cross-references (`[[wiki links]]`).

### Layer 3: Deep Search (Grep)
If Layers 1-2 don't provide complete coverage, use `grep_search` to find exact keyword matches across all markdown files in `wiki/`, `mem/`, and `output/`.

### Layer 4: Raw Source Consultation (If needed)
If deeper technical details or original quotes are required, read the underlying raw file in `raw/` (`raw/articles/`, `raw/video-transcripts/`, `raw/notes/`, `raw/pdfs/`).

## 2. Citation Protocol

Always cite pages when making claims:
- Direct reference: `According to [[Page Name]], ...`
- Paraphrasing: `... (see [[Page Name]])`
- Contradictions: `⚠️ Evolving claim: [[Source A]] states X, while [[Source B]] argues Y.`

## 3. Compounding Criteria (Answer $\rightarrow$ Wiki Page)

Evaluate whether the synthesized answer should be filed back into the Second Brain:

- **Compound to `wiki/analyses/`**: If the answer creates a new multi-source comparison or architectural synthesis.
- **Compound to `output/reports/`**: If the user requested a formal report deliverable.

If compounding is approved:
1. Create the page with full YAML frontmatter.
2. Update `index.md` and append log entry to `wiki/log.md`.

## 4. Log Update
Append exactly one line to `wiki/log.md`:
```
## [YYYY-MM-DD] query | <Short description of the question>
```
