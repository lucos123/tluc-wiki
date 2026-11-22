---
title: "Find bugs with ultrareview"
date: 2026-08-10
tags:
  - source
  - code-review
  - ultrareview
  - verification
  - claude-code
source: "raw/articles/claude-code/large-codebases-sdlc-worktrees/ultrareview.md"
url: "https://code.claude.com/docs/en/ultrareview.md"
---

# Find bugs with ultrareview

**URL**: https://code.claude.com/docs/en/ultrareview.md  
**Source File**: [raw/articles/claude-code/large-codebases-sdlc-worktrees/ultrareview.md](../../raw/articles/claude-code/large-codebases-sdlc-worktrees/ultrareview.md)  

---

## Executive Summary

This official Anthropic guide introduces **Ultrareview** (`/code-review ultra` or `/ultrareview`), a deep cloud-sandboxed multi-agent code review architecture in [Claude Code](../entities/Claude%20Code.md).

Unlike local `/code-review`, Ultrareview uploads the branch diff or GitHub PR to a remote cloud sandbox where a multi-agent reviewer fleet inspects, reproduces, and independently verifies every finding before surfacing results.

---

## Local vs. Cloud Ultrareview Comparison

| Feature | Local `/code-review` | Cloud `/code-review ultra` |
| --- | --- | --- |
| **Execution Environment** | Local terminal session | Remote cloud sandbox (claude.ai infrastructure) |
| **Verification Depth** | Local effort level tuning | Multi-agent fleet with mandatory falsification verification |
| **Duration** | Seconds to ~2 minutes | 5 to 10 minutes (background async execution) |
| **Local CPU Load** | Consumes local CPU & RAM | Zero local CPU/resource overhead |
| **Costing** | Standard plan token usage | 3 free runs (Pro/Max), then ~$5–$25 usage credits |
| **Best Used For** | Fast iterative feedback during coding | Pre-merge confidence on major PRs and critical branches |

---

## Usage Commands

```bash
# Review current working branch against default branch
/code-review ultra

# Review branch against custom base (develop)
/code-review ultra develop

# Review specific GitHub PR
/code-review ultra 1234

# Headless CI script execution
claude ultrareview --json --timeout 30
```

---

## Related Knowledge Nodes

- **Concepts**:
  - [Cloud Sandboxed Ultrareview](../concepts/Cloud%20Sandboxed%20Ultrareview.md)
  - [Automated Multi-Agent Code Review](../concepts/Automated%20Multi-Agent%20Code%20Review.md)
  - [Verification Loop](../concepts/Verification%20Loop.md)
  - [REVIEW.md Governance](../concepts/REVIEW.md%20Governance.md)
- **Entities**: [Claude Code](../entities/Claude%20Code.md), [Anthropic](../entities/Anthropic.md).
