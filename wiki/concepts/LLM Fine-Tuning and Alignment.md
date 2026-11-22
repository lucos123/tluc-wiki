---
title: "LLM Fine-Tuning and Alignment"
date: 2026-11-17
tags:
  - concept
  - llm-foundations
  - machine-learning
  - alignment
source: "wiki/sources/LLM Handbook 50 Concepts.md"
---

# LLM Fine-Tuning and Alignment

A **Pre-trained Base Model** (produced via [Transformer Architecture and Pre-training](Transformer%20Architecture%20and%20Pre-training.md)) predicts plausible continuations rather than following instructions safely or accurately. Transforming a base completion model into a helpful, reliable assistant requires two sequential adaptation phases: **Instruction Fine-Tuning** (including parameter-efficient methods like **LoRA** / **QLoRA**) and **Human Preference Alignment** (**RLHF**, **DPO**, and **Constitutional AI**) ([LLM Handbook 50 Concepts](../sources/LLM%20Handbook%2050%20Concepts.md)).

---

## Instruction Tuning & Fine-Tuning Paradigms

- **Base Model vs. Instruction-Tuned Behavior**: Given `"What is AI?"`, a raw base model may simply repeat or continue surrounding prompt text, whereas an instruction-tuned model trained under Supervised Fine-Tuning loss ($L_{\text{SFT}} = -\frac{1}{N}\sum_{i=1}^N \log p(y_i \mid x_i)$) over `(instruction, response)` corpora (`FLAN`, `T0`, `Dolly`, `ShareGPT`, `OpenAssistant`, `Self-Instruct`, `Distilabel`) directly answers queries as an assistant ([LLM Handwritten Study Guide 15 Pages](../sources/LLM%20Handwritten%20Study%20Guide%2015%20Pages.md)).
- **Fine-Tuning Approaches**:

| Method | Parameters Updated | Hardware / Cost Profile | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Full Fine-Tuning** | `100%` of weights | Very expensive, multi-GPU cluster required | Updates entire pre-trained model on target domain |
| **LoRA (PEFT)** | `~0.1%` of weights | Low VRAM, `7B` fits on `1 GPU` | Freezes `W` and trains low-rank adapters: $W' = W + \Delta W = W + BA$ where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times d}$ ($r = 8$ or $16$) |
| **QLoRA** | `~0.1%` + `4-bit` (`NF4`) | Ultra-low VRAM, `65B` fits on `1x 48GB GPU` | Combines 16-bit LoRA adapters with `NF4` 4-bit quantized frozen base weights |
| **Adapters & Prefix Tuning** | Bottleneck modules (`~1–3%`) | Modular multi-task swapping | Inserts frozen-backbone bottlenecks via **Houlsby** (serial), **Pfeiffer** (parallel), or **Compacter** layers |

---

## Alignment Frameworks (`3H`: Helpful, Harmless, Honest)

Even instruction-tuned models can output toxic, biased, or fabricated responses. Alignment calibrates outputs around human values (**Helpful**, **Harmless**, **Honest**).

### 1. Three-Stage RLHF (`SFT -> RM -> PPO`)
1. **Supervised Fine-Tuning (`SFT`)**: Fine-tune the base model on high-quality human-written demonstrations.
2. **Reward Model (`RM`) Training**: Humans rank pairs/lists of candidate model completions ($A > B \implies \text{RM}(A) > \text{RM}(B)$); train a reward model to score alignment automatically.
3. **Reinforcement Learning (`PPO`)**: Update the SFT policy with **Proximal Policy Optimization** to maximize RM scores while enforcing a **KL-divergence penalty** against the original SFT weights to prevent policy collapse or reward hacking.

### 2. Direct Preference Optimization (`DPO`)
Eliminates the complexity and instability of training a separate Reward Model and running PPO loops. Instead, **DPO** optimizes the policy $\pi_\theta$ directly against a frozen reference policy $\pi_{\text{ref}}$ over winning/losing preference pairs $(y_w, y_l)$ from datasets like `Anthropic HH` and `UltraFeedback`:

$$\mathcal{L}_{\text{DPO}} = -\mathbb{E}\left[\log \sigma\left(\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}\right)\right]$$

### 3. Constitutional AI ([Anthropic](../entities/Anthropic.md))
Replaces heavy human feedback labeling for safety principles with an explicit written constitution: the model critiques and revises its own responses against constitutional rules (`RLAIF`).

---

## Decision Boundary: Prompting vs. RAG vs. Fine-Tuning

In production systems ([AI Engineer Interview Notes](../sources/AI%20Engineer%20Interview%20Notes.md), [LLM Handbook 50 Concepts](../sources/LLM%20Handbook%2050%20Concepts.md)), teams follow a strict 3-rung escalation rule—*"Prompting is cheapest to change but weakest at knowledge; RAG grounds answers in fresh data at the cost of retrieval latency and pipeline complexity; fine-tuning bakes in behavior at the cost of upfront data and training effort"*:
1. **Prompting First**: Free to iterate; sufficient for most format, tone, and CoT reasoning tasks.
2. **RAG Second** ([Retrieval-Augmented Generation and Vector DBs](Retrieval-Augmented%20Generation%20and%20Vector%20DBs.md)): Chosen for dynamic, external, or proprietary factual knowledge requiring attribution and suppressed hallucinations.
3. **Fine-Tuning (`LoRA` / Distillation) Last**: Chosen only after prompting + RAG prove inadequate, when demanding strict domain style across thousands of calls (`100s+` curated pairs) or distilling a specialized workflow onto a smaller, faster model—**never to inject rapidly changing facts**.

| Criterion | Choose **RAG** ([Retrieval-Augmented Generation and Vector DBs](Retrieval-Augmented%20Generation%20and%20Vector%20DBs.md)) | Choose **Fine-Tuning** (`LoRA / SFT`) |
| :--- | :--- | :--- |
| **Primary Goal** | Inject fresh, proprietary, or fast-changing factual knowledge | Adapt response style, tone, strict formatting, or distill smaller/faster models |
| **Cost & Iteration** | Moderate ongoing infra + retrieval tokens; instant doc updates | Upfront curation (`100s+` pairs) & GPU training + hosting |
| **Attribution** | Supports explicit source citations and reduces hallucination | Encodes patterns implicitly; risks overfitting & catastrophic forgetting |

---

## Relationships

- **Sources**: [LLM Handbook 50 Concepts](../sources/LLM%20Handbook%2050%20Concepts.md), [LLM Handwritten Study Guide 15 Pages](../sources/LLM%20Handwritten%20Study%20Guide%2015%20Pages.md), [AI Engineer Interview Notes](../sources/AI%20Engineer%20Interview%20Notes.md)
- **Upstream Foundation**: Adapts base checkpoints from [Transformer Architecture and Pre-training](Transformer%20Architecture%20and%20Pre-training.md) and [LLM Pretraining, Optimization and Decoding](LLM%20Pretraining%2C%20Optimization%20and%20Decoding.md).
- **Complementary Knowledge Injection**: Pairs with [Retrieval-Augmented Generation and Vector DBs](Retrieval-Augmented%20Generation%20and%20Vector%20DBs.md), [Prompt Engineering](Prompt%20Engineering.md), and [AI System Design and Production Architecture](AI%20System%20Design%20and%20Production%20Architecture.md).
- **Safety & Evaluation**: Connects to **Red Teaming**, **Guardrails**, and alignment evaluation in [AI Evaluation, Safety and Governance](AI%20Evaluation%2C%20Safety%20and%20Governance.md), [LLM Inference Optimization and Security](LLM%20Inference%20Optimization%20and%20Security.md), and [Closed-Loop Evals](Closed-Loop%20Evals.md).
