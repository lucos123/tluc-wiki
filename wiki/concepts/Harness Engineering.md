---
title: Harness Engineering
date: 2026-07-28
tags:
  - concept
  - ai-sdlc
  - engineering_practice
---

# Harness Engineering

A core concept from [[The New SDLC With Vibe Coding]] summarized by the equation:
`Agent = Model + Harness`

## Definition
The "harness" is the scaffolding wrapped around a raw AI model that allows it to actually accomplish tasks. 
As described in [[You Can Learn AI Agent Harness & Loop Engineering In 19 Min]], the raw LLM is like a powerful **wild horse** (probabilistic, high-capacity, but unguided). The **harness** represents the bridle, saddle, and reins—the software architecture (memory pipelines, tool gates, RAG, execution loops) controlling the model to achieve maximum predictability and value.

## The 4 Memory Tiers in a Harness

1. **Working Memory (Context RAM)**: Ephemeral short-term context window holding current prompts and active chat history.
2. **Procedural Memory (Skills)**: Instruction files (`SKILL.md`) defining how to perform specific tasks.
3. **Semantic Memory (Durable Facts)**: Long-term domain facts retrieved via vector RAG, continuously updated by an asynchronous Summarizer Agent.
4. **Episodic Memory (Time-Series Events)**: Historical event logs retrieved via SQL + vector RAG queries.

## The 3-Stage Evolution of AI Engineering

As outlined in [[Agent Harness explained in 8min]], agent engineering evolved through three distinct paradigms:
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
- **Persistent Instruction Files**: e.g., `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (see [[Persistent Instruction File]]).
- **Tools, Permissions & Extensibility**: Granular, single-purpose tools gated by deterministic risk classification. Extending capabilities by connecting external systems via Model Context Protocol (MCP) or packaging repeatable prompts into modular Agent Skills via `SKILL.md` (see [[Claude Code Skills]]).
- **State & Safety**: Sandboxed execution environments. Checkpointing (snapshotting file states before edits) to provide a safe "undo" button, alongside YOLO modes for auto-approving trusted tool use.
- **Hooks**: Deterministic code running at lifecycle points (e.g., blocking commits or auto-formatting code) outside the LLM prompt (see [[Claude Code Hooks]]).
- **Observability**: Traces, logs, and cost metering.

## Implementations
- **SWE-agent**: Demonstrated massive performance gains simply through better ACI design.
- **Anthropic's 3-Agent Setup**: A Planner, Generator, and Evaluator working together.
- **Claude Code**: A production-grade harness revealed to use 5 stages of context compaction, 3-tier memory, and 40+ permission-gated tools (see [[12 Agentic Harness Patterns from Claude Code]]).
- **Harness in Harness (Harness²)**: Systems like ClaudeKit and GoClaw that add further structured workflows, quality gates, and agent coordination on top of base harnesses.
- **[[AI Code Migration]]**: The six-step migration methodology is harness engineering applied to full language ports. The engineer designs the *loops* (implement → review → fix), the *rules* (rulebook, gap inventory), and the *referee* (judge/test suite) — not the code itself. The build daemon serialises expensive rebuilds while fixers work in parallel. The rule-propagation mechanic (reviewer catches mistake → rulebook sentence added → affected batch regenerated) is the harness equivalent of automated quality gates: correctness constraints enforced *structurally*, not per-file.

## Key Insight: Harness Shifts the Engineer's Role

In mature harness implementations, the engineer's most valuable hours are:
1. **Designing the rules** (what is correct translation? what are the gaps?)
2. **Building the judge** (how do we verify correctness objectively?)
3. **Watching patterns** (when does the same mistake recur across many files?)

Everything else — execution, fixing, compiling, testing — runs in loops the harness drives. This mirrors the [[Conductor vs Orchestrator]] framing from [[My LLM coding workflow going into 2026]]: the engineer as conductor of agent workstreams.
