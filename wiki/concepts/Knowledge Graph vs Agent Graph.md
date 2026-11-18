---
title: "Knowledge Graph vs Agent Graph"
date: 2026-08-04
tags:
  - concept
  - graph-engineering
  - agentic-design
source: "[[Why Graph Engineering will 10x your Claude Codex]]"
---

# Knowledge Graph vs Agent Graph

The architectural distinction between **Knowledge Graphs** and **Agent Graphs** in AI agent system design, as detailed by [[Greg Isenberg]] in [[Why Graph Engineering will 10x your Claude Codex]].

---

## Comparison Matrix

| Dimension | Knowledge Graph | Agent Graph |
|:---|:---|:---|
| **Primary Focus** | *How information connects* across entities, claims, and data points. | *How work moves* across tasks, subagents, reviews, and approvals. |
| **Core Components** | Entity nodes, relational edges, vector embeddings (e.g., Microsoft GraphRAG). | Agent runtimes, tool sandboxes, fan-out/fan-in paths, human gates. |
| **Problem Solved** | Overcomes RAG retrieval failures when queries require multi-hop entity reasoning. | Overcomes single-chat context pollution, hallucination, and single-pass trust. |
| **Execution Mode** | Data indexing and query reasoning. | Active workflow execution and multi-agent coordination. |

---

## Production Convergence

In state-of-the-art enterprise AI agent systems, **Knowledge Graphs and Agent Graphs converge**:
- The **Knowledge Graph** provides the agent swarm with deep relational memory over company codebase, architecture, and customer history.
- The **Agent Graph** orchestrates how agents plan, execute, verify, and deliver code changes or research reports.

See [[Graph Engineering]], [[Agent Graph]], and [[Knowledge Representation, Logic and Bayesian Inference]] (for symbolic Semantic Networks, Frames, and `OWL` Ontologies).
