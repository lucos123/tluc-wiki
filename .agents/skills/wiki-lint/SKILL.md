---
name: wiki-lint
description: >
  Perform a structural and semantic health check on the Second Brain (wiki/, mem/, output/).
  Use when the user asks to lint, audit, check, review, or validate the wiki for consistency,
  broken links, orphan pages, contradictions, stale content, or missing cross-references via /wiki-lint or natural language.
argument-hint: "[--auto-fix]"
---

# Wiki Lint Skill

Options: `$ARGUMENTS`

You are performing a health check on the Second Brain (`tluc-wiki`). This is a 5-phase process: automated structural checks (via `lint_wiki.py`) followed by LLM-powered semantic analysis, report generation, fix proposals, and log updates.

## 1. Execution Phases

### Phase 1 — Automated Structural Script Execution
Run the structural health checker:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```

The script audits:
- `orphan_pages`: Pages in `wiki/`, `mem/`, or `output/` not listed in `index.md`.
- `missing_pages`: Links in `index.md` pointing to non-existent pages.
- `broken_links`: `[[wiki links]]` pointing to missing targets.
- `missing_frontmatter`: Pages missing the `---` frontmatter block.
- `missing_fields`: Incomplete required frontmatter (`title`, `date`, `tags`, `source`).
- `duplicate_titles`: Duplicate `title:` values in frontmatter.
- `date_format_errors`: Non `YYYY-MM-DD` date strings.
- `stats`: Coverage percentage and total page/link metrics.

### Phase 2 — Semantic Audit
Read 5–10 pages across `wiki/`, `mem/`, and `output/`. Check:
1. **Cross-Reference Completeness**: Are obvious entity/concept links missing?
2. **Freshness & Stubs**: Are pages older than 90 days or containing under 5 lines?
3. **Contradictions**: Are conflicting statistics or evolving claims marked with `⚠️ Evolving claim`?

### Phase 3 — Generate Structured Health Report
Generate a Markdown health report with severity classification (🔴 Errors, 🟡 Warnings, 🔵 Info) and a 1-10 Health Score.

### Phase 4 — Auto-Fix Proposals
Separate auto-fixable issues (adding orphans to `index.md`, fixing alphabetical sort, completing missing frontmatter fields) from manual-review issues (resolving source contradictions).

### Phase 5 — Log Update
Append exactly one line to `wiki/log.md`:
```
## [YYYY-MM-DD] lint | <Summary of health check findings>
```
