---
title: "Lauren Tan"
date: 2026-11-17
tags:
  - entity
  - person
  - agentic-design
  - harness-engineering
  - ai-sdlc
source: "wiki/sources/All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI.md"
---

# Lauren Tan

**Lauren Tan** (also known online as **Potato** / **`@poteto`**) is a Principal Engineer on the **Grok Bot** team at **SpaceX** (`SpaceXSI` / xAI) and former engineer at Cursor. She focuses on high-trust agentic engineering environments, deterministic static analysis, runtime/formal verification harnesses, and Electron/TypeScript client performance at scale.

---

## Notable Frameworks & Open-Source Contributions

- **[Poteto Trust Pyramid](../concepts/Poteto%20Trust%20Pyramid.md) (Inverse Trust Pyramid)**: Five-layer model for maximizing trust in coding agents by prioritizing codebase API/directory architecture (`codebase`) and custom compiler/lint rules (`static analysis`) before runtime/formal verification, prose (`AGENTS.md` / skills), and human review.
- **Dune Framework**: Internal Electron client framework (built for Grok Bot) applying "organic architecture" constraints—such as banning React `useEffect` in product code and blocking cross-boundary imports between `electron-renderer/` and `electron-main/`.
- **pstack (`github.com/cursor/plugins`)**: Personal agent plugin suite featuring verification, benchmark-vetting, and architectural skills (`/create-verification-skill`, `/state-chart`) alongside the 24-principle library synthesized in [Agentic Engineering Principles](../concepts/Agentic%20Engineering%20Principles.md).

---

## Key Ingested Works

- [All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI](../sources/All%20Code%20Is%20Slop%20%28Except%20Mine%29%20%E2%80%94%20Lauren%20Tan%2C%20SpaceXSI.md) — AI Engineer Code Summit talk detailing how Grok Bot scaled to 11,000 merged PRs/month (~0.5% revert rate, 227 contributors) with faster runtime performance using 167+ custom lint rules, runtime feature maps, TLA+/Lean/Bombadil verification, and outer-loop autonomous fuzzing.
- [Engineering Principles Library (pstack and OMC)](../sources/Engineering%20Principles%20Library%20%28pstack%20and%20OMC%29.md) — Catalog and critical evaluation of Lauren Tan's 24 `pstack` engineering judgment principles (Core, Architecture, Verification, Delegation, Meta) and selective role-based injection.

See [Poteto Trust Pyramid](../concepts/Poteto%20Trust%20Pyramid.md), [Agentic Engineering Principles](../concepts/Agentic%20Engineering%20Principles.md), [Verification Loop](../concepts/Verification%20Loop.md), [Loop Engineering](../concepts/Loop%20Engineering.md), and [AI Engineer](AI%20Engineer.md).
