---
title: Stable Latent MoE
date: 2026-08-01
tags:
  - concept
  - ai-models
  - cost-optimization
---

# Stable Latent MoE

A Mixture of Experts (MoE) model architecture designed to solve the communication bottleneck when serving ultra-large, sparse models across GPU supernodes. Detailed in [[Kimi K3 explained in 13min]].

## Key Architecture

1. **Token Compression (Latent MoE)**: Token embeddings are down-projected into a lower-dimensional latent space before being routed across GPU interconnects (NVLink/Infiniband). This reduces transmitted data volume and compute overhead across split experts.
2. **Hyper-Sparsity**: Scales total expert counts into the hundreds (e.g. 896 experts in [[Kimi K3]]) while keeping activated expert ratios ultra-low (~1.8%, 16 experts/token).
3. **Quantile Balancing**: Replaces fixed bias penalties with percentile-curve ranking to stably train the router when selecting a tiny subset of experts from hundreds of candidates.

## Impact on Agentic Systems

By drastically lowering cross-GPU communication latency and inference cost, Stable Latent MoE allows continuous high-throughput token generation for multi-agent loops (`[[Loop Engineering]]`) and graph workflows (`[[Graph Engineering]]`).
