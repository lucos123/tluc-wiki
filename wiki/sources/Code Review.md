---
title: "Code Review"
date: 2026-08-10
tags:
  - source
  - code-review
  - harness-engineering
  - verification
  - claude-code
source: "[[raw/articles/claude-code/large-codebases-sdlc-worktrees/code-review.md]]"
url: "https://code.claude.com/docs/en/code-review.md"
---

# Code Review

**URL**: https://code.claude.com/docs/en/code-review.md  
**Source File**: [[raw/articles/claude-code/large-codebases-sdlc-worktrees/code-review.md]]  

---

## Executive Summary

This official Anthropic guide details [[Claude Code]]'s managed **Code Review** feature. Code Review uses a fleet of specialized subagents to analyze GitHub pull requests in parallel against the entire codebase, identifying logic bugs, security vulnerabilities, and subtle regressions while running verification checks to eliminate false positives.

---

## Key Review Pillars

### 1. Multi-Agent Review Pipeline
```
PR Push / Command (@claude review)
  ├── Agent 1 (Logic Errors & Race Conditions)
  ├── Agent 2 (Security & Tenant Leakage)
  ├── Agent 3 (Regressions & Broken Edge Cases)
  └── Verification Step (Falsification check against full codebase)
        └── Output: GitHub Check Run & Line Annotations
```

### 2. Severity Markers
- 🔴 **Important**: Severe bug that should be resolved before merging.
- 🟡 **Nit**: Minor code quality or style recommendation.
- 🟣 **Pre-existing**: Flaw that already existed prior to the PR diff.

### 3. Local Execution (`/code-review`)
Developers can run local diff reviews in their terminal session using `/code-review` without needing GitHub App integration.

### 4. Custom Governance via `REVIEW.md`
Placing a `REVIEW.md` file at the repository root injects top-priority instructions directly into every agent in the review pipeline. Key tuning capabilities:
- **Redefining Severity**: Explicitly defining what constitutes an Important bug for the repository.
- **Nit Capping**: Restricting inline nit comments (e.g., "Report at most 5 nits per review").
- **Exclusion Paths**: Skipping generated code (`src/gen/`), lockfiles, or test fixtures.
- **Mandatory Repository Checks**: Forcing checks like tenant scoping or integration test presence.

---

## Related Knowledge Nodes

- **Concepts**: [[Automated Multi-Agent Code Review]], [[REVIEW.md Governance]], [[Verification Loop]], [[Second Opinion Pattern]], [[Claude Code Monorepo Setup]].
- **Entities**: [[Claude Code]], [[Anthropic]].
