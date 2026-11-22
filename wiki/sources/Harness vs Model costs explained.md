---
title: "Harness vs Model costs explained"
date: 2026-08-12
tags:
  - source
  - harness-engineering
  - token-economics
  - cost-optimization
  - video-transcript
source: "raw/video-transcripts/harness-vs-model-costs-explained.md"
url: "https://www.youtube.com/watch?v=8ji5vURIllM"
channel: "Caleb Writes Code"
---

# Harness vs Model costs explained

**URL**: https://www.youtube.com/watch?v=8ji5vURIllM  
**Channel**: [Caleb Writes Code](../entities/Caleb%20Writes%20Code.md)  
**Source File**: [raw/video-transcripts/harness-vs-model-costs-explained.md](../../raw/video-transcripts/harness-vs-model-costs-explained.md)  

---

## Executive Summary

In this 9-minute technical breakdown, **Caleb Writes Code** analyzes why the financial cost of running AI coding agents is dominated by **Harness Overhead** rather than the raw cost of the LLM base model.

While base model inference costs have dropped by 2–3x (e.g. GPT-5.6 Sol, open-weight models like Kimi K3, Qwen 3.8 Max, DeepSeek V4), thick agentic harnesses like [Claude Code](../entities/Claude%20Code.md), Cursor, OpenCode, and [Cline](../entities/Cline.md) introduce massive system prompt "tollgates" (8,000–30,000 tokens per turn) and multi-turn roundtrip oscillations that inflate cost per task by **4× to 15×** (up to 30× on simple prompts) compared to raw chat completions.

---

## Key Takeaways & Architectural Insights

### 1. Jevons' Paradox in AI Coding
- As the per-token cost of base intelligence drops, total developer token consumption explodes because users migrate from thin chat UIs (25 input tokens) to thick agentic harnesses (30,000 system prompt tokens + recursive tool loops).

### 2. The Harness System Prompt "Tollgate"
- **Thin Chat Interface**: Direct prompt (25 tokens) $\rightarrow$ Response (500 tokens) $\approx$ **$0.01**.
- **Thick Agent Harness (Claude Code)**: Same prompt $\rightarrow$ System prompt tollgate (8K–30K tokens) + tool loop $\approx$ **$0.37** (30× cost jump for the exact same task).
- **Harness Cost Variance (for identical prompt on Opus 5)**:
  - **Claude Code**: ~$0.37 (heavy feature set & full command definitions)
  - **OpenCode**: ~$0.11
  - **Cline**: ~$0.07 (open-source, lightweight system prompt)
  - **Pi**: ~$0.025

### 3. Server-Side Prompt Caching Economics
- Prompt caching (KV Cache reuse) is essential for agentic harnesses.
- **Provider Economics (H100 GPUs)**: An NVIDIA H100 GPU (~$3/hr rental) fitting a 1M context window across 12 quantized 5-minute cache slots can generate up to **$70/hour in caching revenue**.
- **1-Hour Cache Writes**: Providers like Anthropic offload inactive KV cache states from GPU VRAM to adjacent NVMe SSDs, reloading them on demand to offer lower $10/M token write rates over long sessions.

### 4. Subscription Walled Gardens vs. Multi-Harness Aggregators
- Flat-rate subscriptions (Claude Pro/Team, ChatGPT Plus) protect developers from per-turn token anxiety during long agent loops (10–20 min multi-turn builds).
- Open-weight aggregators (e.g. Cline Pass) offer unified subscriptions for open models (Kimi K3, GLM 5.2, DeepSeek V4) usable across multiple open harnesses.

---

## Related Knowledge Nodes

- **Concepts**:
  - [Harness Overhead vs Model Cost](../concepts/Harness%20Overhead%20vs%20Model%20Cost.md)
  - [Jevons Paradox in AI](../concepts/Jevons%20Paradox%20in%20AI.md)
  - [Harness Engineering](../concepts/Harness%20Engineering.md)
  - [Token Economics](../concepts/Token%20Economics.md)
  - [System Prompt Caching Optimization](../concepts/System%20Prompt%20Caching%20Optimization.md)
- **Entities**:
  - [Caleb Writes Code](../entities/Caleb%20Writes%20Code.md)
  - [Claude Code](../entities/Claude%20Code.md)
  - [Cline](../entities/Cline.md)
  - [Anthropic](../entities/Anthropic.md)
  - [OpenAI](../entities/OpenAI.md)
