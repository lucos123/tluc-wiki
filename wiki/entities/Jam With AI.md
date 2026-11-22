---
title: "Jam With AI"
date: 2026-11-22
tags:
  - entity
  - organization
  - creator
  - system-design
  - production-ai
url: "https://www.youtube.com/@JamWithAI"
---

# Jam With AI

**Jam With AI** is a technical AI engineering channel, newsletter (`jamwithai.substack.com`), and open-source resource hub (`github.com/jamwithai`) created and hosted by **Shirin Khosravi Jam** (AI & ML Engineering Manager with 10+ years of experience). The platform focuses on visual, first-principles walkthroughs of production AI system architecture, agent workflows, evaluation, and scalable deployment infrastructure.

---

## Core Focus Areas
- **Production AI System Design**: Request-lifecycle infrastructure surrounding LLM and agent services—covering traffic ingress, admission control, multi-layer caching, async queuing, resilience engineering, stateless scaling, and GPU-aware autoscaling (see [Production AI Resilience and Scaling Patterns](../concepts/Production%20AI%20Resilience%20and%20Scaling%20Patterns.md)).
- **Inside the Core AI Service**: Practical service blueprints combining FastAPI endpoints, agentic orchestration workflows, vector/relational data stores, end-to-end tracing, and quality evaluations.
- **Visual System Walkthroughs**: Clean, incremental dark-mode architectural diagrams contrasting naive single-user prototypes against `10,000+`-user production topologies.

---

## Channels & Ecosystem
- **YouTube Channel**: `Jam With AI | Shirin Khosravi Jam`
- **Newsletter**: `https://jamwithai.substack.com/welcome`
- **Code Repositories**: `https://github.com/jamwithai`
- **Creator Profile**: Shirin Khosravi Jam (`https://www.linkedin.com/in/shirin-khosravi-jam/`)

---

## Ingested Sources
- [Agent Memory The 7 Types You Should Know](../sources/Agent%20Memory%20The%207%20Types%20You%20Should%20Know.md) *(2026-07-01, Companion Substack w/ Shantanu Ladhwe)* — Written precursor anchoring the 7 memory types in CoALA/MemGPT/Generative Agents, distinguishing Stored-vs-Active and What-vs-Where axes, `Thread ID` checkpointers, episodic reflection, guardrail procedures, and `Temporal` prospective execution.
- [How a Production AI Agent System Actually Works](../sources/How%20a%20Production%20AI%20Agent%20System%20Actually%20Works.md) *(2026-08-21, Video 1)* — Architectural breakdown of the inner 9-layer core Python production AI agent stack (`Uvicorn`/`FastAPI`, `Pydantic`, `LangGraph`, `Postgres + pgvector`, `Redis`, `LiteLLM`, `Langfuse`/`Opik`, `Pytest` + AI Evals, `uv`/`Ruff`).
- [AI Agent Memory 7 Types Explained in 12 Minutes](../sources/AI%20Agent%20Memory%207%20Types%20Explained%20in%2012%20Minutes.md) *(2026-08-28)* — Architectural taxonomy of 7 AI Agent memory responsibilities (Working, Semantic, Episodic, Procedural, External, Parametric, Prospective) demonstrated end-to-end in an Email Agent.
- [AI System Design 7 Patterns Explained in 17 Minutes](../sources/AI%20System%20Design%207%20Patterns%20Explained%20in%2017%20Minutes.md) *(2026-09-10, Video 2)* — Complete video walkthrough of the 7 surrounding production infrastructure patterns wrapping the Core AI Service under load, plus AI observability and system design interview methodology.
- [System Design for AI Engineers 7 Patterns](../sources/System%20Design%20for%20AI%20Engineers%207%20Patterns.md) *(2026-04-09, Companion Substack)* — Companion interview-focused article adding interview signals, Denial-of-Wallet defense, weighted/least-connections GPU load balancing, semantic caching nuances, and reference books.
- [System Design for Engineers 162 Concepts](../sources/System%20Design%20for%20Engineers%20162%20Concepts.md) *(Substack Resource Map)* — Curated 17-part, 162-concept system design curriculum (324 article/video links, 15 ⭐ core concepts, per-part interview signals, and 8 follow-up diagnostics); full link catalog in [System Design 162 Concepts Resource Map](../references/System%20Design%20162%20Concepts%20Resource%20Map.md).
- [All GPU Related Concepts Simply Explained](../sources/All%20GPU%20Related%20Concepts%20Simply%20Explained.md) *(Substack Visual Guide)* — Visual reference covering 55+ GPU hardware, memory hierarchy, numerical precision (`TF32`/`BF16`/`FP8`/`FP4`), NVIDIA generations (`V100`–`B200`), `DP`/`TP`/`PP` parallelism, `NVLink`/`NCCL`/`AllReduce`, and scaling bottlenecks; synthesized into [GPU Architecture and Distributed Scaling](../concepts/GPU%20Architecture%20and%20Distributed%20Scaling.md).

## Related Pages
- [System Design 162 Concepts Resource Map](../references/System%20Design%20162%20Concepts%20Resource%20Map.md)
- [GPU Architecture and Distributed Scaling](../concepts/GPU%20Architecture%20and%20Distributed%20Scaling.md)
- [Production AI Agent Service Stack](../concepts/Production%20AI%20Agent%20Service%20Stack.md)
- [Production AI Resilience and Scaling Patterns](../concepts/Production%20AI%20Resilience%20and%20Scaling%20Patterns.md)
- [AI Agent Memory Types](../concepts/AI%20Agent%20Memory%20Types.md)
- [AI System Design and Production Architecture](../concepts/AI%20System%20Design%20and%20Production%20Architecture.md)
- [Inference Serving and Deployment Patterns](../concepts/Inference%20Serving%20and%20Deployment%20Patterns.md)
