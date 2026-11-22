---
title: "AI Harness 6 Core Components"
date: 2026-11-21
tags:
  - source
  - harness-engineering
  - agentic-design
  - visual-guide
source: "raw/articles/ai-other/ai-harness-six-components.md"
---

# AI Harness 6 Core Components (AI Harness làm gì để agent hoàn thành công việc?)

**Curated & Shared by:** [Viet Nguyen AI](../entities/Viet%20Nguyen%20AI.md) (`vietnh1009`, `2026-11-21`)
**Source Post:** [Facebook Post](https://www.facebook.com/vietnh1009/posts/pfbid0VejzMavZhUeQeLTd2UH1fPE85gJmK9ZeRiYDbo48aVeJr6ToxfjWsupR6HweFY82l)
**Raw Source File:** [raw/articles/ai-other/ai-harness-six-components.md](../../raw/articles/ai-other/ai-harness-six-components.md)
**Infographic Diagram:** `raw/assets/ai-harness-six-components-01.jpg` (`800x934`)

![AI Harnesses — 6 Must Know Terms](../../raw/assets/ai-harness-six-components-01.jpg)

---

## Executive Summary

A concise visual synthesis shared by [Viet Nguyen AI](../entities/Viet%20Nguyen%20AI.md) unpacking the foundational equation `Agent = Model + Harness`—where the language model provides next-step **predictions** while the **harness** orchestrates execution, state, safety, and boundaries. Using a concrete **e-commerce customer support agent** (looking up delivery status and drafting a reply), the diagram breaks a working harness down into six orthogonal operational subsystems.

---

## Six Core Harness Subsystems (Order Support Reference Flow)

| # | Term (EN / VI) | Core Harness Responsibility | Order-Support Concrete Flow | Related Wiki Concepts |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Agent Loop** *(Vòng lặp agent)* | Calls model, executes requested tools, feeds observations back until done, blocked for help, or capped by iteration limits | `Request -> Model <-> Tool -> Done? -> Final answer` | [Agent Loop Lifecycle](../concepts/Agent%20Loop%20Lifecycle.md), [Loop Engineering](../concepts/Loop%20Engineering.md) |
| 2 | **Tool Calling** *(Gọi công cụ)* | Validates model-emitted tool names/arguments, runs deterministic handlers, returns structured observations | `get order` $\rightarrow$ checks delivery $\rightarrow$ `"delivered"` | [Programmatic Tool Calling](../concepts/Programmatic%20Tool%20Calling.md), [AI System Design and Production Architecture](../concepts/AI%20System%20Design%20and%20Production%20Architecture.md) |
| 3 | **Context Management** *(Quản lý ngữ cảnh)* | Combines policy, instructions, chat history, and tool results; compacts old turns via prompts and hooks when windows fill | Compacts `Old chat` while keeping `Policy` + `Instructions` | [Context Window Management](../concepts/Context%20Window%20Management.md), [Context Engineering](../concepts/Context%20Engineering.md) |
| 4 | **Checkpointing** *(Lưu trạng thái)* | Persists external workflow state outside the model so interrupted runs reload cleanly and resume | Saves `Checkpoint: order delivered` $\rightarrow$ resumes drafting post-restart | [Session Checkpoints](../concepts/Session%20Checkpoints.md), [Memory Architecture](../concepts/Memory%20Architecture.md) |
| 5 | **Permissions & Sandboxing** *(Phân quyền & cách ly)* | Enforces allow/block lists on tools, files, actions, and code execution sandboxes before execution | `Read order ✓` allowed vs. `Issue refund ✗` blocked | [Cloud Agent Sandbox and Auto Mode](../concepts/Cloud%20Agent%20Sandbox%20and%20Auto%20Mode.md), [Deterministic Lifecycle Hooks](../concepts/Deterministic%20Lifecycle%20Hooks.md) |
| 6 | **Guardrails** *(Kiểm soát an toàn)* | Inspects inputs, outputs, and tool requests; pauses sensitive deliveries for human approval—**explicitly noting controls can still miss errors** | `Draft ready -> Human approval (Pending / Approved -> Sent)` | [Verification Loop](../concepts/Verification%20Loop.md), [AI Evaluation, Safety and Governance](../concepts/AI%20Evaluation%2C%20Safety%20and%20Governance.md) |

---

## Cross-Source Synthesis

1. **Generalizes Coding Harness Concepts to Domain Agents**: Whereas [Agent Harness explained in 8min](Agent%20Harness%20explained%20in%208min.md) and [AI Model vs Agentic Harness What Actually Drives AI](AI%20Model%20vs%20Agentic%20Harness%20What%20Actually%20Drives%20AI.md) focus on software-engineering CLI harnesses (worktrees, linters, file checkpoints), this infographic grounds the exact same six primitives inside a customer-facing order-support workflow—mirroring the transactional escalation architecture in [AI System Design and Production Architecture](../concepts/AI%20System%20Design%20and%20Production%20Architecture.md) and [Domain-Specific Agents](../concepts/Domain-Specific%20Agents.md).
2. **Non-Overlapping Defense Warning**: Emphasizing that *"each layer has a distinct role and can still miss errors"* aligns with defense-in-depth principles in [Cloud Agent Sandbox and Auto Mode](../concepts/Cloud%20Agent%20Sandbox%20and%20Auto%20Mode.md), [Poteto Trust Pyramid](../concepts/Poteto%20Trust%20Pyramid.md), and prompt-injection defenses in [Prompt Engineering](../concepts/Prompt%20Engineering.md).

---

## Related Pages
- **Entities**: [Viet Nguyen AI](../entities/Viet%20Nguyen%20AI.md)
- **Primary Concept Hub**: [Harness Engineering](../concepts/Harness%20Engineering.md)
- **Connected Concepts**:
  - [Agent Loop Lifecycle](../concepts/Agent%20Loop%20Lifecycle.md)
  - [Context Window Management](../concepts/Context%20Window%20Management.md)
  - [Session Checkpoints](../concepts/Session%20Checkpoints.md)
  - [Cloud Agent Sandbox and Auto Mode](../concepts/Cloud%20Agent%20Sandbox%20and%20Auto%20Mode.md)
  - [Deterministic Lifecycle Hooks](../concepts/Deterministic%20Lifecycle%20Hooks.md)
  - [AI System Design and Production Architecture](../concepts/AI%20System%20Design%20and%20Production%20Architecture.md)
  - [Domain-Specific Agents](../concepts/Domain-Specific%20Agents.md)
- **Companion Sources**:
  - [AI Model vs Agentic Harness What Actually Drives AI](AI%20Model%20vs%20Agentic%20Harness%20What%20Actually%20Drives%20AI.md)
  - [Agent Harness explained in 8min](Agent%20Harness%20explained%20in%208min.md)
  - [12 Agentic Harness Patterns from Claude Code](12%20Agentic%20Harness%20Patterns%20from%20Claude%20Code.md)
