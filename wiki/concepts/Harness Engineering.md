---
title: Harness Engineering
date: 2026-06-28
tags:
  - concept
  - ai_sdlc
  - engineering_practice
---

# Harness Engineering

A core concept from [[The New SDLC With Vibe Coding]] summarized by the equation:
`Agent = Model + Harness`

## Definition
The "harness" is the scaffolding wrapped around a raw AI model that allows it to actually accomplish tasks. If the developer is the factory manager, the model is the engine, and the harness is the assembly line, sensors, and belts.

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
