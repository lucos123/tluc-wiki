---
title: Graph Engineering
date: 2026-08-01
tags:
  - concept
  - agentic-design
  - harness-engineering
  - loop-engineering
---

# Graph Engineering

The practice of orchestrating complex agentic workflows by structuring multiple reliable agent runtimes (nodes) into directed graphs (DAGs or cyclic graphs) connected by explicit control and data paths (edges). Detailed by [[Caleb Writes Code]] in [[Graph Engineering explained in 8min]], [[Greg Isenberg]] in [[Why Graph Engineering will 10x your Claude Codex]], and [[Sean's AI Stories]] in [[You Can Learn AI Agent Graph Engineering In 21 Min]].

## Evolution & The [[Agent Engineering Ladder]]

```
Prompt Engineering (Role-Playing: "act as Shakespeare")
  └── Context Engineering (Feeding CRM/RAG data into prompts)
        └── Skills (Procedural memory & SKILL.md playbooks)
              └── Loop Engineering (Goal-driven tool exploration: "go figure it out")
                    └── Graph Engineering (Controlled SOPs + Exploratory Sub-Loops)
```

- **The Viral Shift**: Sparked on July 18, 2026 by [[Peter Steinberger]] (*"Are we still talking about loops or did we shift to graphs yet?"*).
- **2023 Graph Attempts vs 2026 Shift**: Early frameworks failed because individual prompt nodes were fragile. In 2026, individual nodes are fully harnessed agents. The bottleneck shifted from *node capability* to *graph topology design*.
- **Production Frameworks**: Open-source implementations like [[Waku-Agent]] demonstrate routing requests across dynamic graphs, memory nodes, tool calls, and eval gates.

## Knowledge Graph vs. Agent Graph

As clarified by [[Greg Isenberg]], graph engineering encompasses two distinct but complementary layers (see [[Knowledge Graph vs Agent Graph]]):
- **Knowledge Graph**: Helps AI reason over *how information connects* across entities, topics, and claims (e.g., Microsoft GraphRAG).
- **[[Agent Graph]]**: Helps AI reason over *how work moves* (planner nodes, parallel fan-out subagents, skeptic reviewer nodes, merger nodes, human gates).

## Common Graph Topologies & Design Patterns

### 1. Directed Acyclic Graph (DAG) & Fan-Out / Fan-In
Execution flows strictly forward in distinct phases with no backward loops.
- **Example**: Deep Research workflows (e.g. 108 agents across 5 phases: Scoping $\rightarrow$ Search $\rightarrow$ Fetch $\rightarrow$ Verify/Vote $\rightarrow$ Report Synthesis) or Claude Code code migrations (12 parallel subagents).

### 2. Cyclic Graph & Evaluator-Optimizer Loops
Execution contains feedback loops where control can transition backward based on evaluation.
- **Example**: Evaluator-Optimizer loops, Human-on-the-Loop resteering (`[[Control-Loop Engineering]]`).

### 3. The 4 Core Graph Design Patterns
1. **Sequence Node**: Step-by-step sequential dependencies (Thesis $\rightarrow$ Script $\rightarrow$ Visual Diagram).
2. **Fan-Out / Parallel Nodes**: Distributing research angles across concurrent subagents in isolated context windows.
3. **Evaluator / Skeptic Node**: Dedicated quality-gate subagent reviewing work before merging (see [[Second Opinion Pattern]]).
4. **Human-in-the-Loop Gate**: Pausing execution for human approval before applying changes to production.

## Benefits and Challenges

| Advantage | Benefit |
|-----------|---------|
| **Mass Parallelization** | Concurrent execution across subagents drastically reduces wall-clock time. |
| **Context Isolation** | Subagents maintain clean, hyper-focused context windows, preventing "leaky summarization" bugs. |

| Challenge | Mitigation |
|-----------|------------|
| **Token Inflation (~15x)** | Use **Prompt Caching** to reduce input token costs by up to 90%. |
| **Runtime Contamination** | Use isolated **Git Worktrees** or sandbox containers per subagent node. |
| **Error Cascading & Masked Root Cause** | Use the [[Second Opinion Pattern]] (`claude -p`), Opus judge models, and the [[Orchestrator Skill Pattern]] (see [[Anthropic Just Fixed Graph Engineering's Greatest Flaw]]). |

## Relationship to [[Harness Engineering]] & [[Loop Engineering]]

- **[[Harness Engineering]]** optimizes the individual node (tools, memory, permissions).
- **[[Loop Engineering]]** structures the execution trigger and stop conditions for loops.
- **Graph Engineering** scales these nodes and loops horizontally into complex, multi-phase agent networks.
