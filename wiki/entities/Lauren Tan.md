---
title: "Lauren Tan"
date: 2026-11-17
tags:
  - entity
  - person
  - agentic-design
  - harness-engineering
  - ai-sdlc
source: "[[All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI]]"
---

# Lauren Tan

**Lauren Tan** (also known online as **Potato** / **`@poteto`**) is a Principal Engineer on the **Grok Bot** team at **SpaceX** (`SpaceXSI` / xAI) and former engineer at Cursor. She focuses on high-trust agentic engineering environments, deterministic static analysis, runtime/formal verification harnesses, and Electron/TypeScript client performance at scale.

---

## Notable Frameworks & Open-Source Contributions

- **[[Poteto Trust Pyramid]] (Inverse Trust Pyramid)**: Five-layer model for maximizing trust in coding agents by prioritizing codebase API/directory architecture (`codebase`) and custom compiler/lint rules (`static analysis`) before runtime/formal verification, prose (`AGENTS.md` / skills), and human review.
- **Dune Framework**: Internal Electron client framework (built for Grok Bot) applying "organic architecture" constraints—such as banning React `useEffect` in product code and blocking cross-boundary imports between `electron-renderer/` and `electron-main/`.
- **pstack (`github.com/cursor/plugins`)**: Personal agent plugin suite featuring verification and architectural skills including `/create-verification-skill` and `/state-chart`.

---

## Key Ingested Works

- [[All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI]] — AI Engineer Code Summit talk detailing how Grok Bot scaled to 11,000 merged PRs/month (~0.5% revert rate, 227 contributors) with faster runtime performance using 167+ custom lint rules, runtime feature maps, TLA+/Lean/Bombadil verification, and outer-loop autonomous fuzzing.

See [[Poteto Trust Pyramid]], [[Verification Loop]], [[Loop Engineering]], and [[AI Engineer]].
