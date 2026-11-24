---
name: wiki-lint
description: >
  Perform a structural and semantic health check on the Second Brain (wiki/, mem/, output/).
  Use when the user asks to lint, audit, check, review, or validate the wiki for consistency,
  broken links, orphan pages, contradictions, stale content, or missing cross-references via /wiki-lint or natural language.
when_to_use: >
  Use whenever a structural or semantic health check of the Second Brain is needed, or after major content updates.
argument-hint: "[--auto-fix]"
allowed-tools:
  - run_command
  - read_file
  - write_file
  - edit_file
---

# Wiki Lint Skill

Options: `$ARGUMENTS`

You are performing a health check on the Second Brain (`tluc-wiki`). This is a 5-phase process: automated structural checks (via `lint_wiki.py`) followed by LLM-powered semantic analysis, report generation, fix proposals, and log updates.

## 1. Execution Phases

### Phase 1 — Automated Structural Script Execution
Run the structural health checker and the skill/rule discipline linter:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
python .agents/skills/wiki-lint/scripts/lint_skills.py --strict
```

The script audits:
- `orphan_pages`: Pages in `wiki/`, `mem/`, or `output/` not listed in `index.md`.
- `missing_pages`: Links in `index.md` pointing to non-existent pages.
- `broken_links`: Standard Markdown links (and any frontmatter `source:` paths) pointing to missing targets on disk.
- `legacy_wikilinks`: Any leftover `[[...]]` Obsidian wikilink syntax remaining outside fenced/inline code blocks.
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

### Phase 4 — Interactive 1-Click Auto-Fix Protocol
If `$ARGUMENTS` contains `--auto-fix` or if the user requests automatic repair:
1. **Orphan Pages**: Automatically add orphan pages into `index.md` under the appropriate category (`## Concepts`, `## Entities`, `## Sources`, `## Personal Memory & Projects (mem/)`, or `## Generated Deliverables (output/)`).
2. **Index Sorting**: Automatically sort all entries in `index.md` alphabetically within each section.
3. **Missing Frontmatter**: Add standard YAML frontmatter blocks to any unformatted markdown files.
4. **Skill & Rule Repairs**: When repairing `.agents/skills/` or `ctx/rules/`, apply [agent-doc-and-correction-rules.md](../../../ctx/rules/agent-doc-and-correction-rules.md) (climb the 5-Level Mistake Elimination Ladder and prove each fix fires before re-running lint).
5. **Re-run Lint**: Run `python .agents/skills/wiki-lint/scripts/lint_wiki.py` and `python .agents/skills/wiki-lint/scripts/lint_skills.py --strict` to confirm `0` errors remain.

### Phase 5 — Log Update
Append exactly one line to `wiki/log.md`:
```
## [YYYY-MM-DD] lint | <Summary of health check findings>
```
