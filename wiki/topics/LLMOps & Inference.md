---
title: "LLMOps & Inference"
date: 2026-08-02
tags:
  - concept
  - topic
  - inference-economics
---

# LLMOps & Inference

**LLMOps & Inference** encompasses model serving architectures, token economics, latency trade-offs, and infrastructure optimization.

## Core Concepts

- [[GPU Architecture and Distributed Scaling]]: Hardware-to-cluster mental model spanning SMs, Tensor Cores, HBM bandwidth, precision (`TF32`/`BF16`/`FP8`/`FP4`), NVIDIA generations (`V100`–`B200`), `DP`/`TP`/`PP` parallelism, `NVLink`/`NCCL`/`AllReduce`, and scaling bottlenecks.
- [[Inference Speed vs Intelligence Trade-off]]: 3D trade-off space balancing token speed, intelligence, and token efficiency.
- [[Stable Latent MoE]]: Sparse expert routing architecture (e.g. [[Kimi K3]]).
- [[Cerebras Systems]]: Wafer-scale ultra-fast inference (>750 t/s).
- [[Responses API]]: OpenAI's agent endpoint for tool use and subagent execution.
