---
title: "Building Closed-Loop Evals for a Multimodal Agent at Scale"
date: 2026-07-30
tags:
  - source
  - loop-engineering
  - evals
  - multimodal
source_type: video
url: "https://www.youtube.com/watch?v=31GUkCBD-Uc"
channel: "AI Engineer"
speaker: "Soumya Gupta & Jai Chopra"
duration: "21m 38s"
source: "raw/video-transcripts/Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber.md"
---

# Building Closed-Loop Evals for a Multimodal Agent at Scale

**Channel**: AI Engineer  
**Speakers**: Soumya Gupta & Jai Chopra ([[Uber]])  
**URL**: https://www.youtube.com/watch?v=31GUkCBD-Uc  
**Duration**: 21m 38s  
**Transcript**: [[raw/video-transcripts/Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber.md]]

A technical presentation from Uber's Computer Vision team detailing how Uber Eats deploys multimodal image enhancement agents at scale ($90B run rate, 10,000 cities) using **Closed-Loop Evals** and automated prompt/config tuning without human intervention in real-time.

## Key Concepts

- **Multimodal Production Orchestration**:
  - **Understanding & Routing Agent**: VLM describes image $\rightarrow$ outputs structured data $\rightarrow$ router decides *Enhance* vs. *Skip*. Measured via precision/recall (high recall guardrail prevents bad images from slipping through; high precision prevents wasteful compute & image degradation).
  - **Image Editing & In-Loop QA Agent**: Generates image-specific prompts $\rightarrow$ passes to enhancement model $\rightarrow$ multi-dimensional QA gate (plating, color, faithfulness). Runs up to $K$ iterations. Evaluated via **Pass at K**.
  - **Publish-Ready QA Gate**: Final Swiss cheese redundancy layer for policy, brand compliance, and physics/object coherence before publishing to the menu.
  - **Flat Structured Logging**: Logs all sub-agent steps in a single flat JSON per request for aggregated rollups and root-cause diagnosis.
- **Closed-Loop Evals & Auto-Tuning Architecture**:
  - **Golden Dataset**: Human-labeled baseline with objective guidelines to remove subjective bias.
  - **Diagnosis Agent**: Umbrella agent that detects production vs. human label mismatches, localizes the faulty agent component, and triggers auto-tuning.
  - **Prompt Optimizer Sub-Agents**:
    - *Reflect Agent*: Analyzes failure cases, removes noise, identifies systemic dataset patterns.
    - *Synthesize Agent*: Updates agent prompt/config based on reflection notes.
  - **Automated Benchmarking**: Tests updated agent config against the Golden Dataset. If guardrail metrics pass, automatically registers and deploys the new agent version in production without human intervention.
- **Multi-Tier Feedback Loops**:
  - **Model Loop**: Offline human golden labels $\leftrightarrow$ Auto-tuning pipeline.
  - **Dogfooding Loop**: In-app employee & merchant feedback (thumbs up/down + text) fed back into Diagnosis Agent.
  - **Marketplace Conversion Loop**: Business metrics (add-to-cart, order completion) sliced by geo, dish, and device to tune specific segments.

## Synthesis Notes

This source extends the [[Loop Engineering]] framework into **Multimodal Production Applications at Industrial Scale**. 

Where [[Kyle Mistele]]'s [[Control-Loop Engineering]] focuses on codebase transformations via PRs, Uber's architecture demonstrates how to apply closed-loop evals (`[[Closed-Loop Evals]]`) to high-throughput user-facing AI services. It complements LangChain's [[Hill-Climbing Loop]] by providing a concrete enterprise implementation of an agent self-improving its own prompts/configs through continuous reflection on production traces.
