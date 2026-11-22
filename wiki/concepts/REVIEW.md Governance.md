---
title: "REVIEW.md Governance"
date: 2026-08-10
tags:
  - concept
  - harness-engineering
  - verification
  - claude-code
source: "wiki/sources/Code Review.md"
---

# REVIEW.md Governance

**REVIEW.md Governance** is the configuration pattern where a top-level `REVIEW.md` file in a repository root overrides default automated code review behavior by injecting highest-priority instructions into review agents.

---

## Configuration Capabilities

```markdown
# Review Instructions

## What Important Means
Reserve Important for data leaks, unindexed queries, and breaking API changes.

## Nit Capping
Report at most 5 nits per review. Summarize the rest.

## Do Not Report
- Generated files under src/gen/
- Formatting or lint issues enforced by CI
```

## Distinct Roles: `CLAUDE.md` vs `REVIEW.md`

- **`CLAUDE.md`**: Broad project context read during interactive coding sessions.
- **`REVIEW.md`**: High-priority instruction block injected verbatim into the system prompt of review pipeline agents to control severity, nit volume, path exclusions, and repo-specific checks.

See [Code Review](../sources/Code%20Review.md) and [Automated Multi-Agent Code Review](Automated%20Multi-Agent%20Code%20Review.md).
