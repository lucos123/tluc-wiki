---
title: "LLM Fine-Tuning and Alignment"
date: 2026-11-17
tags:
  - concept
  - llm-foundations
  - machine-learning
  - alignment
source: "[[LLM Handbook 50 Concepts]]"
---

# LLM Fine-Tuning and Alignment

A **Pre-trained Base Model** (produced via [[Transformer Architecture and Pre-training]]) predicts plausible continuations rather than following instructions safely or accurately. Transforming a base completion model into a helpful, reliable assistant requires two sequential adaptation phases: **Instruction Fine-Tuning** (including parameter-efficient methods like **LoRA** / **QLoRA**) and **Human Preference Alignment** (**RLHF**, **DPO**, and **Constitutional AI**) ([[LLM Handbook 50 Concepts]]).

---

## Instruction Tuning & Fine-Tuning Paradigms

- **Base Model vs. Instruction-Tuned Behavior**: Given `"What is AI?"`, a raw base model may simply repeat or continue surrounding prompt text, whereas an instruction-tuned model trained on `(instruction, response)` pairs directly answers the query as an assistant.
- **Fine-Tuning Approaches**:

| Method | Parameters Updated | Hardware / Cost Profile | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Full Fine-Tuning** | `100%` of weights | Very expensive, multi-GPU cluster required | Updates entire pre-trained model on target domain |
| **LoRA (PEFT)** | `~0.1%` of weights | Low VRAM, `7B` fits on `1 GPU` | Freezes `W` and trains low-rank adapters: $W + BA$ where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$ ($r = 8$ or $16$) |
| **QLoRA** | `~0.1%` + `4-bit` base | Ultra-low VRAM, `65B` fits on `1x 48GB GPU` | Combines LoRA adapters with 4-bit quantized frozen base weights |

---

## Alignment Frameworks (`3H`: Helpful, Harmless, Honest)

Even instruction-tuned models can output toxic, biased, or fabricated responses. Alignment calibrates outputs around human values (**Helpful**, **Harmless**, **Honest**).

### 1. Three-Stage RLHF (`SFT -> RM -> PPO`)
1. **Supervised Fine-Tuning (`SFT`)**: Fine-tune the base model on high-quality human-written demonstrations.
2. **Reward Model (`RM`) Training**: Humans rank pairs/lists of candidate model completions ($A > B \implies \text{RM}(A) > \text{RM}(B)$); train a reward model to score alignment automatically.
3. **Reinforcement Learning (`PPO`)**: Update the SFT policy with **Proximal Policy Optimization** to maximize RM scores while enforcing a **KL-divergence penalty** against the original SFT weights to prevent policy collapse or reward hacking.

### 2. Direct Preference Optimization (`DPO`)
Eliminates the complexity and instability of training a separate Reward Model and running PPO loops. Instead, **DPO** optimizes the policy directly over `(chosen, rejected)` preference pairs using a binary cross-entropy objective on policy vs reference log-probability ratios—making alignment simpler, more stable, and widely favored in modern post-training.

### 3. Constitutional AI (`[[Anthropic]]`)
Replaces heavy human feedback labeling for safety principles with an explicit written constitution: the model critiques and revises its own responses against constitutional rules (`RLAIF`).

---

## Decision Boundary: Fine-Tuning vs. RAG

| Criterion | Choose **RAG** ([[Retrieval-Augmented Generation and Vector DBs]]) | Choose **Fine-Tuning** (`LoRA / SFT`) |
| :--- | :--- | :--- |
| **Primary Goal** | Inject fresh, proprietary, or fast-changing factual knowledge | Adapt response style, tone, strict formatting, or specialized reasoning habits |
| **Cost & Iteration** | Cheaper, instant updates by re-indexing documents | Higher compute/dataset preparation upfront |
| **Attribution** | Supports explicit source citations and reduces hallucination | Encodes knowledge implicitly into model weights |

---

## Relationships

- **Upstream Foundation**: Adapts base checkpoints from [[Transformer Architecture and Pre-training]].
- **Complementary Knowledge Injection**: Pairs with [[Retrieval-Augmented Generation and Vector DBs]] and [[Prompt Engineering]] (the lowest-cost adaptation layer).
- **Safety & Evaluation**: Connects to **Red Teaming**, **Guardrails**, and alignment evaluation in [[LLM Inference Optimization and Security]] and [[Closed-Loop Evals]].
