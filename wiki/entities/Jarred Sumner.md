---
title: Jarred Sumner
date: 2026-07-28
tags:
  - entity
  - person
  - claude-code
---

# Jarred Sumner

Co-founder of Bun and Member of Technical Staff (MTS) at Anthropic. Best known for building the Bun JavaScript runtime and for executing a landmark AI-assisted code migration from Zig to Rust.

## Bun: Zig → Rust Migration (2026)

Using [Claude Code](Claude%20Code.md) with Claude Fable 5 and Claude Opus 4.8, Sumner ported approximately **1 million lines of code** from Zig to Rust in less than two weeks. The migration achieved 100% test suite passage before merge, with 19 post-merge regressions (all subsequently fixed). The Rust port shipped inside Claude Code in June 2026.

**Token cost**: 5.9 billion uncached input tokens + 690 million output tokens ≈ $165,000 at API pricing.

**Key methodological choices**:
- Structure-preserving migration (same architecture, new language)
- Rulebook as lookup tables (type/idiom translations)
- 8 specialized review subagents, each targeting a distinct failure category
- Compiler (Cargo) deferred to Step 4 — too slow (minutes) for the inner loop
- Test suite written in TypeScript (third language, independent from both Zig and Rust)

**Results**:
- Memory usage: 6,745 MB → 609 MB (2,000 repeated builds benchmark)
- Binary: 19% smaller on Linux and Windows
- Performance: 2–5% faster across HTTP serving and real-world workloads (next build, tsc)
- ~4% of code in `unsafe` blocks (pointer operations at C/C++ boundaries)

## Background
Originally chose Zig for Bun because it offered C-level performance with radical simplicity, ideal for a solo founder "writing Bun in 1 year in a cramped Oakland apartment pre-LLM." By 2026, Bun CLI had 10+ million monthly downloads and was used extensively within Claude Code.

## See Also
- [AI Code Migration](../concepts/AI%20Code%20Migration.md) — the generalised six-step methodology drawn from his migration
- [How Anthropic runs large-scale code migrations with Claude Code](../sources/How%20Anthropic%20runs%20large-scale%20code%20migrations%20with%20Claude%20Code.md) — primary source
- [Jarred's own migration blog](https://bun.com/blog/bun-in-rust)
