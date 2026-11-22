---
title: "Domain-Specific Agents"
date: 2026-11-16
tags:
  - concept
  - agentic-design
  - harness-engineering
  - cost-optimization
source: "wiki/sources/Why Domain-specific Agents Are the Future.md"
---

# Domain-Specific Agents

**Domain-Specific Agents** is an architectural paradigm proposed by [Justin Schroeder](../entities/Justin%20Schroeder.md) ([Standard Agents](../entities/Standard%20Agents.md)) in [Why Domain-specific Agents Are the Future](../sources/Why%20Domain-specific%20Agents%20Are%20the%20Future.md) arguing that reliable, enterprise-grade AI requires composing **many small, tightly scoped agents**—each built around one or two business processes with a complete, bounded harness—rather than wiring skills/tools onto a single monolithic generalist agent.

---

## 1. The Factory Electrification Analogy ("Line Shaft Era")

During the Industrial Revolution, factories used one massive central steam engine driving rotating overhead **line shafts** belted down to every machine—unsafe, inefficient, and coupled. When electric motors arrived, factories spent ~30 years merely swapping the central steam engine for a giant electric motor without redesigning workflows. **What revolutionized manufacturing was standardized unit-drive electricity** (`120V / 60Hz`, `220V`) powering independent, interchangeable machines at each workstation.

- **Line Shaft Era of Agents (Current Anti-Pattern):** Dropping a giant frontier model in the center ("Claude God") and belting every tool/process (`GitHub`, `Gmail`, `Figma`, `Docs`, `Sheets`, `Calendar`) onto it via [Agent Skills Architecture](Agent%20Skills%20Architecture.md) or [Model Context Protocol](Model%20Context%20Protocol.md) servers.
- **Unit-Drive Era (Target State):** Many small **domain-specific agents** (`Figma Agent`, `Gmail Agent`, `Navan Agent`, `Google Sheets Agent`), each encapsulating its own `Model + System Prompt + Tools + Messages`, coordinated by a top-level orchestrator (similar to [Subagent Architecture](Subagent%20Architecture.md) and [Orchestrator Skill Pattern](Orchestrator%20Skill%20Pattern.md)).

---

## 2. Three Drivers: Integration, Trust, Efficacy

### A. Integration
Real-world Main Street businesses (e.g., an HVAC contractor's fleet maintenance workflow: *report issue $\rightarrow$ assess priority $\rightarrow$ schedule repair $\rightarrow$ update records $\rightarrow$ return to fleet*) want software deeply embedded into one concrete line-of-business process—not an open-ended general assistant with unbounded steps ([Claude Code](../entities/Claude%20Code.md), [Codex](../entities/Codex.md)).

### B. Trust (`Agent = Harness` & Gmail Agent vs. Gmail Skill)
Schroeder equates an **Agent** with its **[Harness](Harness%20Engineering.md)**: deterministic software utilizing non-deterministic model outputs across five layers (`Model → System Prompt → Tools {Function, Prompt, Agent} → Deterministic Hooks → Agent Rules`, plus optional filesystem/code execution).
- **Gmail Agent $>$ Gmail Skill:** A dedicated **Gmail Agent** physically lacks non-Gmail tools (satisfying **Principle of Least Privilege**, Law of Demeter, Separation of Concerns, and Composition over Inheritance—like NASA's Apollo 11 Mission Control specialists). A generalist assistant running a **Gmail Markdown Skill** retains dangerous cross-domain permissions (`prod` infra, social media) that expand blast radius.

### C. Efficacy, Jagged Models & Token Economics
- **Anti-Public-Benchmark Stance ("Streetlight Effect"):** Public leaderboards fail to measure narrow operational reliability. Domain decomposition enables deterministic **non-public process evals** per workflow (aligned with [Model Evaluation and Validation](Model%20Evaluation%20and%20Validation.md) and [Closed-Loop Evals](Closed-Loop%20Evals.md)).
- **Exploiting Jagged Models:** Models exhibit highly uneven strengths across niches (demonstrated in **Model Zen Garden**, where **Tencent HY3** built a 3D scene for `$0.60` outperforming general frontier models like `Sol 6.1`). Domain-specific agents let teams match each sub-task to whichever small model excels at it.
- **Extreme Token & Cost Efficiency:** In Standard Agents' task benchmarks (`Pass@1` vs. log-scale cost), **DeepSeek V4.1 Flash (`max`)** hit `77.0%` at ~`$0.20`/task—making small models practical and **137x cheaper per task** than large frontier models (extending [Token Economics](Token%20Economics.md) and [Effort Level and Model Selection](Effort%20Level%20and%20Model%20Selection.md)).

---

## 3. Five Standards Required for Open Agent Ecosystems

To enable an `npm install` / `pip install` ecosystem of interchangeable agents (and avoid vendor lock-in or silent model regressions):
1. **Domain Specific:** Scoped to 1–2 concrete tasks/workflows.
2. **Full Harness:** Ships editable harness code (`System Prompt`, `Tools`, [Deterministic Lifecycle Hooks](Deterministic%20Lifecycle%20Hooks.md), `Agent Rules`), not just passive markdown instructions.
3. **Portable:** Installable across runtimes like packages (`npm`/`pip`).
4. **Vendor Agnostic & Pinned:** Binds exact model ID, provider, and quantization so verified efficacy holds across machines; once verified, **never auto-upgrade the underlying model until deprecation**.
5. **Composable:** Standardized agent-to-agent messaging under orchestrators.

---

## Related Pages
- **Sources**: [Why Domain-specific Agents Are the Future](../sources/Why%20Domain-specific%20Agents%20Are%20the%20Future.md)
- **Entities**:
  - [Justin Schroeder](../entities/Justin%20Schroeder.md)
  - [Standard Agents](../entities/Standard%20Agents.md)
  - [Claude Code](../entities/Claude%20Code.md)
  - [Codex](../entities/Codex.md)
- **Concepts**:
  - [Harness Engineering](Harness%20Engineering.md)
  - [Agent Skills Architecture](Agent%20Skills%20Architecture.md)
  - [Subagent Architecture](Subagent%20Architecture.md)
  - [Orchestrator Skill Pattern](Orchestrator%20Skill%20Pattern.md)
  - [Deterministic Lifecycle Hooks](Deterministic%20Lifecycle%20Hooks.md)
  - [Model Context Protocol](Model%20Context%20Protocol.md)
  - [Token Economics](Token%20Economics.md)
  - [Effort Level and Model Selection](Effort%20Level%20and%20Model%20Selection.md)
  - [Closed-Loop Evals](Closed-Loop%20Evals.md)
