# Ingest Workflow Execution Example

This example demonstrates a complete end-to-end execution of the `wiki-ingest` skill.

---

## Input Command
```
/wiki-ingest raw/articles/ai-other/harness-engineering.md
```

---

## Execution Steps

1. **Pre-flight Check**: Verified `raw/articles/ai-other/harness-engineering.md` exists and has not been ingested yet.
2. **Source Summary Page Creation**: Created `wiki/sources/Harness Engineering.md`:
   ```markdown
   ---
   title: "Harness Engineering"
   date: 2026-07-28
   tags:
     - source
     - harness-engineering
     - agentic-design
   source: "[[raw/articles/ai-other/harness-engineering.md]]"
   ---

   # Harness Engineering

   **Source File**: [[raw/articles/ai-other/harness-engineering.md]]

   Overview of harness engineering principles by Goon Nguyen.
   ```
3. **Concept & Entity Page Creation**: Created/updated `wiki/concepts/Harness Engineering.md`.
4. **Index & Log Registration**: Updated `index.md` under `## Sources` and `## Concepts`, and appended `wiki/log.md`.
