---
title: Mike Krieger
date: 2026-07-28
tags:
  - entity
  - person
  - claude-code
---

# Mike Krieger

Co-lead of Anthropic Labs. Known for executing a Python-to-TypeScript migration of 165,000 lines over a single weekend using [Claude Code](Claude%20Code.md), and for his iterative "discard and re-run" methodology.

## Python → TypeScript Migration (2026)

Migrated an internal tool codebase — 165,000 lines of Python — to TypeScript over a weekend. The tool ships to users as a single binary. Key driver: 8-minute compile time per platform (30-minute total across build matrix) → after migration: **~2 seconds** compile, binary starts 6x faster, retired a separate deployment pipeline.

**Token cost**: ~27 million tokens for main portion.

**Process**: 8 phase gates, 3 adversarial review rounds, final parity check diffing every command's output against Python original.

**Key methodological choices**:
- **Redesign migration** (new architecture, new language) — rulebook was a design document, not lookup tables
- **Discard-and-re-run**: Ran the full end-to-end migration multiple times, discarding output each time, refining rules with each pass, keeping only the 3rd run
- **Parity harness**: 7 real-world scenarios; any behaviour change = bug
- **No existing test suite**: Had Claude design + run its own autonomous test suite overnight, 4 consecutive nights
- **TypeScript compiler inside the loop**: Fast enough (seconds) to check units inline
- **12 Claude Sonnet subagents** fanned out for main translation

**Build approach for behaviour matching**: Each failing scenario got its own fix agent; loop ran until all 7 passed. Then Claude designed broader autonomous tests and ran them overnight — "it caught the paper cuts no scenario list would have predicted."

## Key Insight
The "discard-and-re-run" pattern for redesign migrations is the equivalent of what Jarred Sumner's stress-test (Step 2) does for structure-preserving migrations: it validates and refines the rulebook/design before committing to incremental progress. The difference is scale — Mike discarded full end-to-end runs rather than 3-file samples.

## See Also
- [AI Code Migration](../concepts/AI%20Code%20Migration.md) — generalised methodology
- [How Anthropic runs large-scale code migrations with Claude Code](../sources/How%20Anthropic%20runs%20large-scale%20code%20migrations%20with%20Claude%20Code.md) — primary source
- [Jarred Sumner](Jarred%20Sumner.md) — counterpart case study (structure-preserving migration)
