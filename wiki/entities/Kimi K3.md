---
title: Kimi K3
date: 2026-08-01
tags:
  - entity
  - product
  - ai-models
---

# Kimi K3

Kimi K3 is an open-weights frontier AI model developed by [Moonshot AI](Moonshot%20AI.md), recognized for its hyper-sparse MoE architecture and extreme inference efficiency.

## Key Technical Specifications

- **2.8-Trillion Scale Open Weights**: The world's first open-source model in the 3-trillion parameter class (full weights released July 27, 2026). Delivers 2.5x overall scaling efficiency over K2.
- **Hyper-Sparse MoE**: 896 total experts with only 16 experts activated per token (1.8% activation ratio).
- **[Stable Latent MoE](../concepts/Stable%20Latent%20MoE.md)**: Compresses token representations before cross-GPU transmission to minimize NVLink interconnect bottlenecks, utilizing quantile balancing for stable router training.
- **Kimi Delta Attention (KDA)**: Sub-quadratic hybrid linear attention (3 KDA layers per 1 Gated MLA layer) providing 6x decoding throughput across 1M context windows with automatic prefix caching.
- **Configurable Reasoning & Features**: Always-on thinking mode configurable via `reasoning_effort` (`low`, `high`, `max`). Fully OpenAI API compatible (`base_url="https://api.moonshot.ai/v1"`), supporting [Dynamic Tool Loading](../concepts/Dynamic%20Tool%20Loading.md), structured outputs, and vision/video inputs. Serves as an open-weights backend for [Claude Code](Claude%20Code.md).

See [Kimi K3 Model Guide](../sources/Kimi%20K3%20Model%20Guide.md), [Kimi K3 explained in 13min](../sources/Kimi%20K3%20explained%20in%2013min.md), and [Stable Latent MoE](../concepts/Stable%20Latent%20MoE.md).
