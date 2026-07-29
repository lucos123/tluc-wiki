---
title: Closed-Loop Evals
date: 2026-07-30
tags:
  - concept
  - evals
  - loop-engineering
  - harness-engineering
---

# Closed-Loop Evals

An automated architecture where production agent executions are continuously evaluated against golden datasets and business metrics, driving autonomous prompt and configuration updates without human intervention. Introduced by [[Uber]] engineers Soumya Gupta & Jai Chopra in [[Building Closed-Loop Evals for a Multimodal Agent at Scale]].

## Core Architecture

```
Production Runs ──> Mismatch Detection ──> Diagnosis Agent ──> Reflect Agent ──> Synthesize Agent ──> Benchmarking ──> Auto-Deploy
```

1. **Golden Dataset**: Human-labeled baseline datasets collected under strict objective guidelines to serve as the ground truth.
2. **Diagnosis Agent**: An umbrella agent that monitors production traces vs. golden labels, localizes component failures, and triggers the auto-tuning pipeline.
3. **Prompt Optimizer (Reflect + Synthesize)**:
   - **Reflect Agent**: Analyzes mismatches, filters noise, and identifies systemic failure patterns.
   - **Synthesize Agent**: Generates updated prompt templates and agent configs.
4. **Automated Benchmarking**: Tests the new config against the Golden Dataset. If guardrail metrics (e.g., recall, precision, Pass at K) pass, the new config is registered and deployed to production automatically.

## Key Metrics in Closed-Loop Systems

- **Recall & Precision (Routing)**: Guardrail metric to ensure low-quality input doesn't slip through (high recall) while avoiding wasteful compute on already high-quality inputs (high precision).
- **Pass at K**: The cumulative pass rate of an agentic edit loop after $K$ iterations of feedback from an in-loop QA Gate.
- **Faithfulness & Completeness**: Guardrail checks preventing AI hallucination (e.g. adding unwanted items) or deletion of key elements.

## Relationship to [[Hill-Climbing Loop]] & [[Control-Loop Engineering]]

Closed-Loop Evals represents the enterprise production implementation of LangChain's [[Hill-Climbing Loop]] (Level 4 loop engineering). While [[Control-Loop Engineering]] focuses on codebase modification PRs, Closed-Loop Evals focuses on high-throughput user-facing services (e.g. image processing, customer support).
