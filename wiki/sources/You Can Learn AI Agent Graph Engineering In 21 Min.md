---
title: "You Can Learn AI Agent Graph Engineering In 21 Min"
date: 2026-08-04
tags:
  - source
  - graph-engineering
  - loop-engineering
  - harness-engineering
  - agentic-design
source: "[[raw/video-transcripts/you-can-learn-ai-agent-graph-engineering-in-21-min.md]]"
url: "https://www.youtube.com/watch?v=IMLwvK08JVc"
channel: "Sean's AI Stories"
speaker: "Sean"
duration: "21m 31s"
---

# You Can Learn AI Agent Graph Engineering In 21 Min

**Channel**: [[Sean's AI Stories]]  
**URL**: https://www.youtube.com/watch?v=IMLwvK08JVc  
**Duration**: 21m 31s  
**Transcript File**: [[raw/video-transcripts/you-can-learn-ai-agent-graph-engineering-in-21-min.md]]  

---

## Executive Summary

In this 21-minute technical deep-dive, [[Sean's AI Stories]] demystifies the distinction between **[[Loop Engineering]]** and **[[Graph Engineering]]**, detailing the **[[Agent Engineering Ladder]]** (Prompt $\rightarrow$ Context $\rightarrow$ Skills $\rightarrow$ Loop $\rightarrow$ Graph Engineering).

The video introduces **[[Waku-Agent]]**, an open-source production agent framework (>700 stars) that combines deterministic Graph workflows (SOPs) with exploratory goal-based Loops and eval-driven quality gates.

---

## Key Takeaways & Concepts

### 1. The 5-Level [[Agent Engineering Ladder]]
```
Prompt Engineering (Role-playing, e.g. "act as Shakespeare")
  └── Context Engineering (Feeding CRM/RAG data into prompts)
        └── Skills (Procedural memory & SKILL.md playbooks)
              └── Loop Engineering (Goal-driven tool exploration: "go figure it out")
                    └── Graph Engineering (Controlled SOPs + Exploratory Sub-Loops)
```

### 2. Loop vs. Graph Trade-Offs
- **Loop**: Maximum autonomy, goal-driven tool calls, but unpredictable execution path and token inflation risk.
- **Graph**: Deterministic SOP execution, predictable handoffs, mass parallelization, but requires predefined workflow structure.
- **Production Synthesis**: Optimal systems embed goal-based Loops inside specific nodes of a deterministic Graph.

### 3. [[Waku-Agent]] Architecture
- Built by Sean, Waku-Agent demonstrates production Graph Engineering:
  1. **Router / Classifier Node**: Analyzes incoming user requests and selects the target Graph topology.
  2. **Memory Retrieval Node**: Pulls relevant persistent state.
  3. **Tool Execution Node**: Executes MCP / API tools.
  4. **Eval & Verification Gate**: Runs automated evaluation before returning the final response.

---

## Related Knowledge Nodes

- **Concepts**: [[Graph Engineering]], [[Agent Engineering Ladder]], [[Waku-Agent]], [[Loop Engineering]], [[Agent Graph]], [[Knowledge Graph vs Agent Graph]].
- **Entities**: [[Sean's AI Stories]], [[Peter Steinberger]], [[Greg Isenberg]], [[Caleb Writes Code]].
