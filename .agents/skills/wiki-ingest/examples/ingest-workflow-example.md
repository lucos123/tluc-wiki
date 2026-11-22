# Ingest Workflow Execution Example

This example demonstrates a complete end-to-end execution of the `wiki-ingest` skill.

---

## Input Command
```
/wiki-ingest raw/articles/ai-other/harness-engineering.md
```

---

## Execution Steps

1. **Pre-flight Check**: Verified raw input `raw/articles/ai-other/harness-engineering  Goon.md` exists.
2. **Source Summary Page Creation**: Created `wiki/sources/Harness Engineering.md`.
3. **Raw File Standardized Kebab-Case Renaming & Link Propagation**:
   - Renamed raw file: `raw/articles/ai-other/Harness Engineering  Goon.md` $\rightarrow$ `raw/articles/ai-other/harness-engineering.md`
   - Updated `source: "raw/articles/ai-other/harness-engineering.md"` in `wiki/sources/Harness Engineering.md`.
4. **Concept & Entity Page Creation**: Created/updated `wiki/concepts/Harness Engineering.md`.
5. **Index & Log Registration**: Updated `index.md` under `## Sources` and `## Concepts`, and appended `wiki/log.md`.
6. **Embedded Verification Gate**: Ran `python .agents/skills/wiki-lint/scripts/lint_wiki.py` to confirm 0 broken links and 100% health score.
