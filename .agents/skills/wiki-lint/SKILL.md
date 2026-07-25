---
name: wiki-lint
description: >
  Perform a health check on the wiki knowledge base. Use when the user asks to
  lint, audit, check, review, or validate the wiki for consistency, broken links,
  orphan pages, contradictions, stale content, or missing cross-references.
  Runs automated checks via a bundled script and performs LLM-powered semantic
  analysis.
---

# Wiki Lint Skill

You are performing a health check on a personal knowledge base (the "wiki").
This is a two-phase process: automated structural checks (via a bundled Python
script) followed by LLM-powered semantic analysis. Follow every step below
precisely.

## Phase 1 — Automated Structural Checks

Run the bundled lint script to detect structural issues:

```
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```

The script outputs JSON with the following categories:
- **orphan_pages**: Wiki pages not listed in `index.md`
- **missing_pages**: Pages referenced in `index.md` but not found on disk
- **broken_links**: `[[wiki links]]` pointing to non-existent pages
- **missing_frontmatter**: Pages lacking the `---` frontmatter block
- **missing_fields**: Pages with incomplete frontmatter (missing title, date,
  tags, or source)
- **duplicate_titles**: Multiple pages with the same `title:` in frontmatter
- **date_format_errors**: Pages with non-standard date formats
- **stats**: Summary statistics (total pages, total links, coverage percentage)

Review the script output and organize issues by severity.

## Phase 2 — LLM-Powered Semantic Analysis

After reviewing the script output, perform these deeper checks by reading
relevant wiki pages:

### 2a. Cross-Reference Completeness

Read `index.md` and spot-check 5–10 wiki pages. For each page, ask:
- Does this page link to all other pages it **should** reference?
- Are there obvious connections missing? (e.g., a concept page that discusses
  a tool but doesn't link to the tool's entity page)

### 2b. Content Freshness

Check the `date:` field in page frontmatter:
- Flag pages older than 90 days as potentially stale
- Flag pages whose raw source has been updated more recently than the wiki page

### 2c. Stub Detection

Identify pages that are too thin to be useful:
- Pages with fewer than 5 lines of body content (excluding frontmatter)
- Pages that are just a title and a single sentence
- Pages that say "see [[Other Page]]" without adding original content

### 2d. Contradiction Detection

Look for conflicting claims across pages. Common patterns:
- Different pages attributing the same feature to different tools
- Conflicting statistics or timelines
- Evolving claims that aren't marked with the `⚠️ Evolving claim` convention

### 2e. Tag Consistency

Review tags across all pages:
- Identify tags used only once (may be typos or should be consolidated)
- Identify similar tags that should be merged (e.g., `ai-sdlc` vs `ai_sdlc`)
- Ensure entity pages use `entity` tag, concept pages use `concept` tag, etc.

### 2f. Index Completeness

Verify that `index.md` accurately reflects the wiki:
- Every page in `wiki/` should have an entry in `index.md`
- Entries should be alphabetically sorted within each section
- Descriptions should be concise and accurate

## Phase 3 — Generate Report

Compile your findings into a structured report. Use this format:

```markdown
# Wiki Health Check Report — YYYY-MM-DD

## Summary
- **Total pages**: N
- **Issues found**: N (🔴 X errors, 🟡 Y warnings, 🔵 Z info)
- **Wiki health score**: X/10

## 🔴 Errors (Must Fix)

Issues that break the wiki's integrity or usability.

### Broken Links
| Page | Broken Link | Suggested Fix |
|------|-------------|---------------|
| ... | ... | ... |

### Missing Frontmatter
- `wiki/path/to/page.md` — missing: title, tags

## 🟡 Warnings (Should Fix)

Issues that degrade quality but don't break anything.

### Orphan Pages
- `Page Name` — not listed in index.md

### Stale Content
- [[Page Name]] — last updated YYYY-MM-DD (N days ago)

### Stub Pages
- [[Page Name]] — only N lines of content

### Missing Cross-References
- [[Page A]] should link to [[Page B]] because...

## 🔵 Info (Nice to Fix)

Observations and improvement suggestions.

### Tag Inconsistencies
- Tag `x` used only once in [[Page Name]]
- Tags `a` and `b` appear to be duplicates

### Suggested Enrichments
- [[Page Name]] could be expanded with information about...

## Automated Check Output
<Paste or summarize the raw JSON output from the lint script>
```

### Severity Classification

| Severity | Criteria |
|----------|----------|
| 🔴 Error | Broken links, missing pages, corrupt frontmatter |
| 🟡 Warning | Orphan pages, stale content, stubs, missing cross-refs |
| 🔵 Info | Tag inconsistencies, enrichment suggestions, minor style issues |

### Health Score Calculation

Score the wiki on a 1-10 scale based on:
- **10**: No errors, no warnings, excellent coverage
- **7-9**: No errors, few warnings, good coverage
- **4-6**: Some errors or many warnings, gaps in coverage
- **1-3**: Many errors, significant structural problems

## Phase 4 — Propose Fixes

For each issue found, propose a concrete fix:

### Auto-Fixable Issues
These can be fixed immediately (with user approval):
- Adding missing pages to `index.md`
- Fixing alphabetical sorting in `index.md`
- Adding missing frontmatter fields with reasonable defaults
- Merging duplicate tags

### Manual-Review Issues
These require the user's judgment:
- Resolving contradictions (which source is correct?)
- Deciding whether to expand stub pages or remove them
- Choosing which missing cross-references to add

**Ask the user**: "Would you like me to auto-fix the N auto-fixable issues?"

## Phase 5 — Update `wiki/log.md`

Append exactly one line at the end of `wiki/log.md`:

```
## [YYYY-MM-DD] lint | <Short description of findings>
```

Example: `## [2026-07-06] lint | Found 3 broken links, 2 orphan pages, 5 stubs. Fixed index sorting.`

## Lint Quality Checklist

Before reporting to the user, verify:

- [ ] Bundled lint script was run and output reviewed
- [ ] At least 5 wiki pages were manually spot-checked for semantic issues
- [ ] All issues are classified by severity (🔴/🟡/🔵)
- [ ] Each issue has a concrete suggested fix
- [ ] Auto-fixable vs manual-review issues are clearly separated
- [ ] Health score is calculated and justified
- [ ] `wiki/log.md` is updated with the lint entry
