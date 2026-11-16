---
title: "Inference Serving and Deployment Patterns"
date: 2026-11-16
tags:
  - concept
  - ai-deployment
  - llmops
  - inference-economics
source: "[[AI Deployment Notes]]"
---

# Inference Serving and Deployment Patterns

**Inference Serving and Deployment Patterns** defines how trained models execute predictions across workload shapes (`Batch`, `Real-Time`, `Async`), timing (`Offline` vs `Online`), physical topology (`Cloud`, `Edge`, `Hybrid`), and multi-layer serving infrastructure. See [[AI Deployment Notes]].

---

## 1. Execution & Prediction Timing Patterns

### A. Batch vs. Real-Time vs. Async Inference (*"How is inference executed?"*)
- **Batch Inference (Offline Jobs):** Scheduled or queue-triggered bulk execution over large datasets; optimizes **throughput and cost/item** via retryable workers (e.g., nightly product recommendations, bulk embeddings, document classification).
- **Real-Time Inference (Online Serving):** Always-on inference servers handling individual requests or micro-batches within milliseconds/seconds; optimizes **low latency (`p50/p95`) and availability** via autoscaling and fast timeouts/fallbacks (e.g., chatbots, fraud detection).
- **Async / Near Real-Time Inference:** `Request → Queue → Process → Notify / Fetch` for jobs too slow for synchronous HTTP responses yet too urgent for nightly batch (large file/video processing, image generation, long-running agents).

### B. Offline vs. Online Predictions (*"When are predictions computed?"*)
- **Offline Prediction:** Precomputed ahead of time from historical data and materialized into a database or feature store.
- **Online Prediction:** Computed on demand at interaction time using live session signals (clicks, context, location).
- **Hybrid Production Pattern (e.g., Recommendations):** Generate top-1,000 candidate items **offline**, then **online** ranking personalizes them against real-time session context.

---

## 2. Cloud vs. Edge vs. Hybrid Topology

| Dimension | Cloud Deployment | Edge / On-Device Deployment |
| :--- | :--- | :--- |
| **Location & Network** | Centralized data center; requires network connectivity | Local device/gateway (`CPU/GPU/NPU`); works offline or on constrained links |
| **Latency & Privacy** | Network round-trip + inference latency; data leaves device | Minimal latency; raw sensitive data stays local |
| **Model & Scale** | Supports huge LLMs/multimodal models; easy centralized scaling | Compute/power constrained $\rightarrow$ requires **smaller models + quantization/compression** and fleet rollouts |

**Hybrid Deployment:** Edge runs lightweight models for instant local filtering/decisions and offline resilience; selected events stream to Cloud for heavy aggregation, deeper inference, and periodic model updates pushed back to Edge.

---

## 3. Six-Layer End-to-End AI Deployment Architecture & Inference Servers

1. **Access Layer:** API Gateway / Load Balancer (auth, rate limiting, routing).
2. **Application / Orchestration Layer:** Prompt construction, RAG, tool calling, business logic, guardrails.
3. **AI Services:** Retrieval, embeddings, reranking, vector stores (e.g., ChromaDB), external APIs.
4. **Model Serving Layer (`Model ≠ Model Server ≠ API`):** Inference servers (`NVIDIA Triton`, `vLLM`, `TGI`, `TorchServe`, `BentoML`) or managed platforms (`AWS SageMaker`, `Azure AI Foundry`, `Google Vertex AI`) managing model loading, **dynamic batching** (trading wait latency for GPU throughput), scheduling, and health checks.
5. **Compute & Infrastructure:** `CPU / GPU / NPU` pools orchestrated via Kubernetes (`EKS`, `GKE`, `AKS`), Terraform, and CI/CD.
6. **Cross-Cutting Operations:** Observability (`Logs, Metrics, Traces, Cost, Model Quality, Alerts` via Grafana) + Security (`Access control, Secrets, Audit, Safety Guardrails`) + Reliability (`Retry with backoff, Fallback model, Cached response, Graceful degradation`).

### LLM Inference Pipeline & Core Serving Metrics
```
User Prompt → Tokenization → Prefill (input processing) → Iterative Token Generation → Streaming / Full Response
```
- **Key Metrics:** **Time to First Token (`TTFT`)**, **Tokens per Second (`TPS` / throughput)**, **Inter-token latency**, **Context length** (KV-cache memory footprint), **GPU memory utilization**, and concurrent sessions—connecting directly to [[Inference Speed vs Intelligence Trade-off]], [[Tokenization]], and [[Token Economics]].

---

## Related Pages
- **Sources**: [[AI Deployment Notes]]
- **Concepts**: [[AI Deployment Lifecycle and Environments]], [[Model Packaging and Versioning]], [[Inference Speed vs Intelligence Trade-off]], [[Tokenization]], [[Token Economics]]
