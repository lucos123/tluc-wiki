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
- **Production AI System Design**: Request-lifecycle infrastructure surrounding LLM and agent services—covering traffic ingress, admission control, multi-layer caching, async queuing, resilience engineering, stateless scaling, and GPU-aware autoscaling (see [[Production AI Resilience and Scaling Patterns]]).
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
- [[How a Production AI Agent System Actually Works]] *(2026-08-21, Video 1)* — Architectural breakdown of the inner 9-layer core Python production AI agent stack (`Uvicorn`/`FastAPI`, `Pydantic`, `LangGraph`, `Postgres + pgvector`, `Redis`, `LiteLLM`, `Langfuse`/`Opik`, `Pytest` + AI Evals, `uv`/`Ruff`).
- [[AI Agent Memory 7 Types Explained in 12 Minutes]] *(2026-08-28)* — Architectural taxonomy of 7 AI Agent memory responsibilities (Working, Semantic, Episodic, Procedural, External, Parametric, Prospective) demonstrated end-to-end in an Email Agent.
- [[AI System Design 7 Patterns Explained in 17 Minutes]] *(2026-09-10, Video 2)* — Complete video walkthrough of the 7 surrounding production infrastructure patterns wrapping the Core AI Service under load, plus AI observability and system design interview methodology.
- [[System Design for AI Engineers 7 Patterns]] *(2026-04-09, Companion Substack)* — Companion interview-focused article adding interview signals, Denial-of-Wallet defense, weighted/least-connections GPU load balancing, semantic caching nuances, and reference books.

## Related Pages
- [[Production AI Agent Service Stack]]
- [[Production AI Resilience and Scaling Patterns]]
- [[AI Agent Memory Types]]
- [[AI System Design and Production Architecture]]
- [[Inference Serving and Deployment Patterns]]
