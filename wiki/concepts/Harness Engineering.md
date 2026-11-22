---
title: Harness Engineering
date: 2026-07-28
tags:
  - concept
  - ai-sdlc
  - engineering_practice
---

# Harness Engineering

A core concept from [The New SDLC With Vibe Coding](../sources/The%20New%20SDLC%20With%20Vibe%20Coding.md) summarized by the equation:
`Agent = Model + Harness`

## Definition
The "harness" is the scaffolding wrapped around a raw AI model that allows it to actually accomplish tasks. 

Key mental models framing the harness include:
- **The Wild Horse Analogy** ([You Can Learn AI Agent Harness & Loop Engineering In 19 Min](../sources/You%20Can%20Learn%20AI%20Agent%20Harness%20%26%20Loop%20Engineering%20In%2019%20Min.md)): The raw LLM is a powerful **wild horse** (probabilistic, high-capacity, but unguided). The **harness** represents the bridle, saddle, and reins—the software architecture (memory pipelines, tool gates, RAG, execution loops) controlling the model to achieve maximum predictability and value.
- **The "Brain in a Jar" Metaphor** ([AI Model vs Agentic Harness What Actually Drives AI](../sources/AI%20Model%20vs%20Agentic%20Harness%20What%20Actually%20Drives%20AI.md)): On its own, a neural network is a capable "brain in a jar"—trapped, unable to open files, execute code, or navigate networks. The **agentic harness** provides embodiment, environmental sensors, actuators, and persistence.

### The Narrowing Benchmark Gap Thesis
As benchmark score gaps between frontier AI foundation models (Anthropic, OpenAI, Moonshot AI, Google) narrow to within a few percentage points, the base model itself is rarely the explanation when one AI product drastically outperforms another. Real-world capability divergence is driven predominantly by harness design.

## The 4 Memory Tiers in a Harness

1. **Working Memory (Context RAM)**: Ephemeral short-term context window holding current prompts and active chat history.
2. **Procedural Memory (Skills)**: Instruction files (`SKILL.md`) defining how to perform specific tasks.
3. **Semantic Memory (Durable Facts)**: Long-term domain facts retrieved via vector RAG, continuously updated by an asynchronous Summarizer Agent.
4. **Episodic Memory (Time-Series Events)**: Historical event logs retrieved via SQL + vector RAG queries.

## The 3-Stage Evolution of AI Engineering

As outlined in [Agent Harness explained in 8min](../sources/Agent%20Harness%20explained%20in%208min.md), agent engineering evolved through three distinct paradigms:
1. **Prompt Engineering (2022–2023)**: 4,000 token context window era (ChatGPT). Focused on personas and system instructions. Limited to single-shot tasks.
2. **Context Engineering (2023–2025)**: Enabled by tool calling, RAG, and MCP. Managed token budgets via continuous context compaction/summarization. Handled multi-step tasks, but degraded on long-duration tasks (12h+) as context summarization caused hallucinations or premature task completion.
3. **Harness Engineering (Coined early 2026)**: Outer execution layer controlling agent loops, swarms, and fresh-context iterations. Rather than continually shrinking context mid-task, the harness executes tasks from a PRD/checklist via fresh context windows per iteration.

```
Harness Engineering (Outer: Loops, Swarms, Fresh-Context Iterations)
  └── Context Engineering (Middle: Tool calling, RAG, MCP, Context Packing)
        └── Prompt Engineering (Inner: Personas, System Prompts, Directives)
```

## Components of a Harness
- **Agent-Computer Interface (ACI)**: Designing how the agent interacts with the computer (e.g., limiting search results, providing line-numbered code viewers, and integrating linter feedback). This alone can boost performance by 64% without changing the model.
- **Memory & Context Management**: Progressively compacting old context, and structuring memory into tiers (e.g., small index in context, topic files on demand, transcripts on disk), sometimes with "autoDream" background consolidation.
- **Multi-Agent Orchestration**: Using specialized sub-agents (e.g., Planner, Generator, Evaluator) to prevent the main agent from doing too much at once or stopping prematurely.
- **Persistent Instruction Files**: e.g., `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (see [Persistent Instruction File](Persistent%20Instruction%20File.md)).
- **Tools, Permissions & Extensibility**: Granular, single-purpose tools gated by deterministic risk classification. Extending capabilities by connecting external systems via Model Context Protocol (MCP) or packaging repeatable prompts into modular Agent Skills via `SKILL.md` (see [Claude Code Skills](../sources/Claude%20Code%20Skills.md)).
- **State & Safety**: Sandboxed execution environments. Checkpointing (snapshotting file states before edits) to provide a safe "undo" button, alongside YOLO modes for auto-approving trusted tool use.
- **Hooks**: Deterministic code running at lifecycle points (e.g., blocking commits or auto-formatting code) outside the LLM prompt (see [Claude Code Hooks](../sources/Claude%20Code%20Hooks.md)).
- **Observability**: Traces, logs, and cost metering.

## Implementations
- **SWE-agent**: Demonstrated massive performance gains simply through better ACI design.
- **Anthropic's 3-Agent Setup**: A Planner, Generator, and Evaluator working together.
- **Claude Code**: A production-grade harness revealed to use 5 stages of context compaction, 3-tier memory, and 40+ permission-gated tools (see [12 Agentic Harness Patterns from Claude Code](../sources/12%20Agentic%20Harness%20Patterns%20from%20Claude%20Code.md)).
- **Harness in Harness (Harness²)**: Systems like ClaudeKit and GoClaw that add further structured workflows, quality gates, and agent coordination on top of base harnesses.
- **[Enterprise Agent Stack](Enterprise%20Agent%20Stack.md)**: Production architecture for regulated industries (healthcare, finance) utilizing immutable event logs, decoupled zero-trust payload storage, and Human-Agent Equivalency to solve enterprise compliance and escalation (see [Why Your Enterprise Tech Stack Isn't Ready for AI Agents](../sources/Why%20Your%20Enterprise%20Tech%20Stack%20Isn%27t%20Ready%20for%20AI%20Agents.md)).
- **[AI Code Migration](AI%20Code%20Migration.md)**: The six-step migration methodology is harness engineering applied to full language ports. The engineer designs the *loops* (implement → review → fix), the *rules* (rulebook, gap inventory), and the *referee* (judge/test suite) — not the code itself. The build daemon serialises expensive rebuilds while fixers work in parallel. The rule-propagation mechanic (reviewer catches mistake → rulebook sentence added → affected batch regenerated) is the harness equivalent of automated quality gates: correctness constraints enforced *structurally*, not per-file.

## Key Insight: Harness Shifts the Engineer's Role

In mature harness implementations, the engineer's most valuable hours are:
1. **Designing the rules** (what is correct translation? what are the gaps?)
2. **Building the judge** (how do we verify correctness objectively?)
3. **Watching patterns** (when does the same mistake recur across many files?)

Everything else — execution, fixing, compiling, testing — runs in loops the harness drives. This mirrors the [Conductor vs Orchestrator](Conductor%20vs%20Orchestrator.md) framing from [My LLM coding workflow going into 2026](../sources/My%20LLM%20coding%20workflow%20going%20into%202026.md): the engineer as conductor of agent workstreams.

---

## Strategic Implications & Fluid Boundaries (IBM Framing)

### The Dual Evaluation Heuristic
As articulated in [AI Model vs Agentic Harness What Actually Drives AI](../sources/AI%20Model%20vs%20Agentic%20Harness%20What%20Actually%20Drives%20AI.md), asking whether "AI is good at a task" is underspecified. Practitioners must evaluate two distinct variables:
1. **Which AI Model is used?** (Raw reasoning depth, domain knowledge, pretraining tokens).
2. **Which Agentic Harness is wrapped around that model?** (Tool definitions, memory compaction, verification loops, permission boundaries).

A capable model wrapped in an unmanaged, naive harness will quickly derail; conversely, an efficient, smaller model wrapped in a rigorous harness with automated verification will consistently deliver production results.

### Fluid Boundaries & Co-Evolution
The division between model and harness is dynamic and continuously shifting:
- **Harness $\rightarrow$ Model**: Capabilities that originally lived entirely inside harness scaffolding (multi-step planning, self-reflection, chain-of-thought verification) are increasingly trained directly into the weights of reasoning models via thinking tokens.
- **Model $\rightarrow$ Harness**: Multi-hour adherence, zero-regression consistency, and organizational policy enforcement are increasingly offloaded from model weights into deterministic harness conventions (`AGENTS.md`, lifecycle hooks, worktree sandboxes).

---

## Minimal 6-Component Execution Loop (Non-Coding Domain Reference)

While coding harnesses layer IDE hooks, AST linters, and worktree sandboxes, transactional [Domain-Specific Agents](Domain-Specific%20Agents.md) (such as an order-lookup customer support bot profiled in [AI Harness 6 Core Components](../sources/AI%20Harness%206%20Core%20Components.md)) rely on six minimal cooperating primitives—**each with a distinct responsibility and non-zero residual error surface**:
1. **Agent Loop** ([Agent Loop Lifecycle](Agent%20Loop%20Lifecycle.md) / [Loop Engineering](Loop%20Engineering.md)): Cycles `Model -> Tool -> Observation` until completion, escalation, or hard step limits.
2. **Tool Calling**: Harness validates requested function/args, executes safely, and injects structured results back into context.
3. **Context Management** ([Context Window Management](Context%20Window%20Management.md)): Preserves active policy and system instructions while hooks/prompts compact aged conversation turns.
4. **External Checkpointing** ([Session Checkpoints](Session%20Checkpoints.md)): Stores progress outside the model so interrupted tasks reload from the last verified step (e.g., cached order lookup) rather than re-running from scratch.
5. **Permissions & Sandboxing** ([Cloud Agent Sandbox and Auto Mode](Cloud%20Agent%20Sandbox%20and%20Auto%20Mode.md)): Deterministically allows low-risk reads (`read order ✓`) while blocking high-risk mutations (`issue refund ✗`).
6. **Guardrails & Human Approval**: Inspects inputs, tool requests, and drafts (`Draft -> Pending Human Approval -> Sent`)—paired cleanly with confidence-gated routing in [AI System Design and Production Architecture](AI%20System%20Design%20and%20Production%20Architecture.md).

---

## Related Knowledge Nodes

- **Concepts**:
  - [Enterprise Agent Stack](Enterprise%20Agent%20Stack.md)
  - [Loop Engineering](Loop%20Engineering.md)
  - [Verification Loop](Verification%20Loop.md)
  - [Context Engineering](Context%20Engineering.md)
  - [Context Window Management](Context%20Window%20Management.md)
  - [Agent Onboarding Files](Agent%20Onboarding%20Files.md)
  - [Model Context Protocol](Model%20Context%20Protocol.md)
  - [Harness Overhead vs Model Cost](Harness%20Overhead%20vs%20Model%20Cost.md)
  - [Session Checkpoints](Session%20Checkpoints.md)
  - [Cloud Agent Sandbox and Auto Mode](Cloud%20Agent%20Sandbox%20and%20Auto%20Mode.md)
  - [Domain-Specific Agents](Domain-Specific%20Agents.md)
  - [AI System Design and Production Architecture](AI%20System%20Design%20and%20Production%20Architecture.md)
- **Entities**:
  - [IBM Technology](../entities/IBM%20Technology.md)
  - [AI Engineer](../entities/AI%20Engineer.md)
  - [Anterior](../entities/Anterior.md)
  - [Claude Code](../entities/Claude%20Code.md)
  - [Anthropic](../entities/Anthropic.md)
  - [OpenAI](../entities/OpenAI.md)
  - [Codex](../entities/Codex.md)
  - [Goon Nguyen](../entities/Goon%20Nguyen.md)
  - [Caleb Writes Code](../entities/Caleb%20Writes%20Code.md)
  - [Viet Nguyen AI](../entities/Viet%20Nguyen%20AI.md)
- **Sources**:
  - [AI Model vs Agentic Harness What Actually Drives AI](../sources/AI%20Model%20vs%20Agentic%20Harness%20What%20Actually%20Drives%20AI.md)
  - [Why Your Enterprise Tech Stack Isn't Ready for AI Agents](../sources/Why%20Your%20Enterprise%20Tech%20Stack%20Isn%27t%20Ready%20for%20AI%20Agents.md)
  - [12 Agentic Harness Patterns from Claude Code](../sources/12%20Agentic%20Harness%20Patterns%20from%20Claude%20Code.md)
  - [Agent Harness explained in 8min](../sources/Agent%20Harness%20explained%20in%208min.md)
  - [Harness vs Model costs explained](../sources/Harness%20vs%20Model%20costs%20explained.md)
  - [You Can Learn AI Agent Harness & Loop Engineering In 19 Min](../sources/You%20Can%20Learn%20AI%20Agent%20Harness%20%26%20Loop%20Engineering%20In%2019%20Min.md)
  - [AI Harness 6 Core Components](../sources/AI%20Harness%206%20Core%20Components.md)

