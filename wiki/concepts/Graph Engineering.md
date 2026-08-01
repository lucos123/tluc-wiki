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

The practice of orchestrating complex agentic workflows by structuring multiple reliable agent runtimes (nodes) into directed graphs (DAGs or cyclic graphs) connected by explicit control and data paths (edges). Introduced in detail by [[Caleb Writes Code]] in [[Graph Engineering explained in 8min]].

## Evolution: Why Graphs Now?

```
Prompt Engineering (2022-2023)
  └── Context Engineering (2023-2025)
        └── Harness Engineering (2025-2026)
              └── Loop Engineering (2026)
                    └── Graph Engineering (2026+)
```

- **2023 Graph Attempts**: Early frameworks (AutoGen, early LangGraph) used graphs where nodes were simple LLM prompt calls. The system failed frequently because individual nodes were unreliable.
- **2026 Graph Shift**: Individual nodes are now fully harnessed, reliable coding/research agents (equipped with MCP, skills, tools, and sandboxes). The engineering bottleneck has shifted from *making the node work* to *designing optimal graph topologies*.

## Common Graph Topologies

### 1. Directed Acyclic Graph (DAG)
Execution flows strictly forward in distinct phases with no backward loops.
- **Example**: Deep Research workflows (e.g. 108 agents across 5 phases: Scoping $\rightarrow$ Search $\rightarrow$ Fetch $\rightarrow$ Verify/Vote $\rightarrow$ Report Synthesis).
- **Use case**: High-throughput parallel research, fan-out migrations, report generation.

### 2. Cyclic Graph
Execution contains feedback loops where control can transition backward based on evaluation.
- **Example**: Evaluator-Optimizer loops, Human-on-the-Loop resteering (`[[Control-Loop Engineering]]`).
- **Use case**: Quality-gated code generation, multi-pass refinement.

## Benefits and Challenges

| Advantage | Benefit |
|-----------|---------|
| **Mass Parallelization** | Concurrent execution across subagents drastically reduces wall-clock time. |
| **Context Isolation** | Subagents maintain clean, hyper-focused context windows, preventing "leaky summarization" bugs. |

| Challenge | Mitigation |
|-----------|------------|
| **Token Inflation (~15x)** | Use **Prompt Caching** to reduce input token costs by up to 90%. |
| **Runtime Contamination** | Use isolated **Git Worktrees** or sandbox containers per subagent node. |

## Relationship to [[Harness Engineering]] & [[Loop Engineering]]

- **[[Harness Engineering]]** optimizes the individual node (tools, memory, permissions).
- **[[Loop Engineering]]** structures the execution trigger and stop conditions for loops.
- **Graph Engineering** scales these nodes and loops horizontally into complex, multi-phase agent networks.
