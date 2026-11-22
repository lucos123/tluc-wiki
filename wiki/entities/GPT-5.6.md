---
title: GPT-5.6
date: 2026-07-18
tags:
  - entity
  - product
  - ai-models
  - frontier-ai
---

# GPT-5.6

GPT-5.6 is OpenAI's frontier model family launched on July 9, 2026, comprising three tiers: **Sol** (flagship), **Terra** (balanced), and **Luna** (cost-efficient). It succeeds GPT-5.5 and emphasizes efficiency-per-token alongside raw capability.

## Model Tiers

| Tier | Role | Positioning |
|------|------|-------------|
| **Sol** | Flagship | State-of-the-art across coding, knowledge work, cybersecurity, science. Estimated 2T–4T parameter scale. Offered in 2 serving tiers: Standard (40–50 t/s on NVIDIA B300) and Ultra-Fast (750 t/s on [Cerebras Systems](Cerebras%20Systems.md) WSE-3 chips). |
| **Terra** | Balanced | Everyday work; outperforms Claude Fable 5 at ~1/16th cost |
| **Luna** | Cost-efficient | Most affordable; also outperforms Fable 5 at ~1/16th cost |

## Reasoning Effort Levels

GPT-5.6 supports graduated compute investment:

- **low / medium / high / xhigh / max**: Increasing reasoning depth and token usage
- **ultra**: New tier that coordinates **4 agents in parallel** by default (scalable to 16), trading higher token use for stronger results and faster time-to-result

## Key Capabilities

### Programmatic Tool Calling
GPT-5.6 can write and run lightweight programs that coordinate tools, process intermediate results, and adapt workflows — reducing tokens, round trips, and developer guidance. See [Programmatic Tool Calling](../concepts/Programmatic%20Tool%20Calling.md).

### Design Judgment
Creates tasteful, ergonomic interfaces from high-level direction. Uses computer-use capabilities to inspect and refine *rendered output* (not just source code), catching visual/functional issues before handoff.

### End-to-End Knowledge Work
Integrates with Slack, Notion, Microsoft 365, Google Drive. Converts messy real-world context into expert-level, shareable artifacts (presentations, documents, spreadsheets).

### Multi-Agent Coordination
The `ultra` setting and multi-agent beta in the Responses API allow parallel workstreams. On BrowseComp, 16-agent configuration achieves 93.4% (vs. 90.8% for 1 agent at max reasoning).

## Benchmark Highlights

- **Agents' Last Exam**: 53.6 (Sol, xhigh) — new SOTA, +13.1 over Fable 5
- **Coding Agent Index**: 80.0 (Sol, max) — new SOTA, +2.8 over Fable 5, <½ output tokens, <½ time, ~⅓ less cost
- **BrowseComp**: 92.2% (Sol) — new SOTA
- **OSWorld 2.0**: 62.6% (Sol) — surpasses Opus 4.8 with 85% fewer output tokens
- **Terminal-Bench 2.1 & DeepSWE**: New SOTA for complex command-line and long-horizon engineering

## Safety

Most robust safeguards to date. Layered approach: model-level protections + real-time checks + monitoring + trust-calibrated access. Extensive evaluation combining human red teaming with automated testing and trusted partner review.

## Sources

- [GPT-5.6: Frontier Intelligence That Scales With Your Ambition](../sources/GPT-5.6%20Frontier%20Intelligence.md)
