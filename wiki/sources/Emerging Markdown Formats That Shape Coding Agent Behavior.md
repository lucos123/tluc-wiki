---
title: "Emerging Markdown Formats That Shape Coding Agent Behavior"
date: 2026-08-04
tags:
  - source
  - context-engineering
  - harness-engineering
  - metacode
  - agentic-design
  - ai-sdlc
source: "raw/articles/ai-other/emerging-markdown-formats-that-shape-coding-agent-behavior.md"
url: "https://generativeprogrammer.com/p/emerging-markdown-formats-that-shape"
author: "Bilgin Ibryam"
---

# Emerging Markdown Formats That Shape Coding Agent Behavior

**Source File**: [raw/articles/ai-other/emerging-markdown-formats-that-shape-coding-agent-behavior.md](../../raw/articles/ai-other/emerging-markdown-formats-that-shape-coding-agent-behavior.md)  
**Author**: [Bilgin Ibryam](../entities/Bilgin%20Ibryam.md)  
**URL**: https://generativeprogrammer.com/p/emerging-markdown-formats-that-shape  
**Published Date**: 2026-08-01  

---

## Executive Summary

In this foundational article, [Bilgin Ibryam](../entities/Bilgin%20Ibryam.md) introduces the concept of **[Metacode](../concepts/Metacode.md)** — the growing taxonomy of agent-facing Markdown formats (`AGENTS.md`, `SKILL.md`, `spec.md`, `ARCHITECTURE.md`, `MEMORY.md`) that move project knowledge, NFRs, architectural boundaries, design tokens, and learned context directly beside source code in version control.

By reading both source code and metacode, AI coding agents act as **Intent Compilers**, translating human intent and architectural judgment directly into executable software changes.

---

## Key Taxonomy of Agent-Facing Markdown Formats

![Project knowledge moves from scattered systems into an agent-ready repository](file:///c:/ttluc/Project/learn-ai/tluc-wiki/raw/assets/metacode-scattered-to-agent-ready.png)

### 1. [Agent Onboarding Files](../concepts/Agent%20Onboarding%20Files.md) (Standing Rules & Constraints)
- **`AGENTS.md`**: Neutral cross-tool standard ("README for agents") describing repository layout, build commands, test suites, and coding conventions (supported by Codex, Cursor, Gemini CLI, Copilot).
- **Vendor-Native Bridges**: `CLAUDE.md` / `.claude/rules/` (Claude Code), `GEMINI.md` (Gemini CLI), `.github/copilot-instructions.md`, `.clinerules/`.

### 2. Repeatable Playbooks (`SKILL.md` / Agent Skills)
- Portable packages describing step-by-step procedures for specific tasks (e.g. database migrations, API audits).
- Boundary: `AGENTS.md` provides standing context; `SKILL.md` provides procedure invoked on demand.

### 3. Reviewable Design & Spec Chains (`GitHub Spec Kit`, `PLANS.md`)
- Moving planning out of chat history into versioned Markdown files:
  `spec.md` (requirements) $\rightarrow$ `plan.md` (technical design) $\rightarrow$ `tasks.md` (executable units) $\rightarrow$ implementation & validation.

### 4. Domain & Architectural Guidance
- `ARCHITECTURE.md`: System boundaries, NFRs, ADRs.
- `DESIGN.md`: Visual identity, design tokens (Google Labs).
- `AUTH.md`: Service-hosted authentication recipes (WorkOS).
- `REVIEW.md`: Review priorities, severity, and skipped files (Kilo).

### 5. Memory & Context Promotion Path ([Memory Promotion Path](../concepts/Memory%20Promotion%20Path.md))
- **Machine-Local Auto Memory**: `MEMORY.md`, `debugging.md` (recorded automatically by agents).
- **Promotion Loop**: Tentative local observation $\rightarrow$ Human review $\rightarrow$ Promoted to shared project rule (`AGENTS.md`, `SKILL.md`, `ARCHITECTURE.md`).

---

## Comparison Matrix

![Comparison of agent-facing Markdown formats](file:///c:/ttluc/Project/learn-ai/tluc-wiki/raw/assets/metacode-formats-comparison-matrix.png)

| Category | Typical Formats | Author | Scope | Support Status |
|:---|:---|:---|:---|:---|
| **Onboarding & Rules** | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Human | Project / Directory | Cross-tool & Vendor Native |
| **Playbooks & Procedures** | `SKILL.md` (Agent Skills) | Human | Task / Workflow | Open Standard (`agentskills.io`) |
| **Specs & Plans** | `spec.md`, `plan.md`, `tasks.md` | Human & Agent | Single Change | Cross-tool (`Spec Kit`, `OpenSpec`) |
| **Domain Instructions** | `ARCHITECTURE.md`, `DESIGN.md`, `AUTH.md` | Human & Agent | Subsystem / Domain | Established & Emerging Experiments |
| **Learned Context** | `MEMORY.md`, `debugging.md` | Agent (Auto) | Machine / Repo | Vendor Native (Claude Code) |

---

## Related Knowledge Nodes

- **Concepts**:
  - [Metacode](../concepts/Metacode.md)
  - [Agent Onboarding Files](../concepts/Agent%20Onboarding%20Files.md)
  - [Memory Promotion Path](../concepts/Memory%20Promotion%20Path.md)
  - [Context Engineering](../concepts/Context%20Engineering.md)
  - [Harness Engineering](../concepts/Harness%20Engineering.md)
  - [Memory Architecture](../concepts/Memory%20Architecture.md)
- **Entities**:
  - [Bilgin Ibryam](../entities/Bilgin%20Ibryam.md)
  - [GitHub Spec Kit](../entities/GitHub%20Spec%20Kit.md)
  - [Claude Code](../entities/Claude%20Code.md)
  - [Codex](../entities/Codex.md)
  - [Gemini CLI](../entities/Gemini%20CLI.md)
  - [Moonshot AI](../entities/Moonshot%20AI.md)
