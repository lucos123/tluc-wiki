---
title: "Transformer Architecture and Pre-training"
date: 2026-11-17
tags:
  - concept
  - llm-foundations
  - deep-learning
  - machine-learning
source: "[[LLM Handbook 50 Concepts]]"
---

# Transformer Architecture and Pre-training

The **Transformer** architecture—introduced in *Attention Is All You Need* (2017)—forms the neural backbone of modern Large Language Models (LLMs). Combined with self-supervised **next-token pre-training** over trillion-token corpora, Transformers give rise to emergent capabilities such as in-context learning, zero-shot generalization, and step-by-step reasoning without task-specific feature engineering ([[LLM Handbook 50 Concepts]]).

---

## End-to-End Transformer Forward Flow

```
Raw Input Text ──▶ Tokenization (Token IDs)
                        │
                        ▼
               Token + Positional Embeddings (Dense Vectors)
                        │
                        ▼
          ┌───────────────────────────────────┐
          │ Transformer Block × N Layers      │
          │  • Multi-Head Self-Attention      │  (GPT-2: 12 layers,
          │  • Add & Norm (Residual+LayerNorm)│   GPT-3: 96 layers)
          │  • Feed Forward Network (MLP)     │
          │  • Add & Norm (Residual+LayerNorm)│
          └───────────────────────────────────┘
                        │
                        ▼
             Output Logits (Next-Token Probabilities)
```

---

## Core Architectural Mechanisms

### 1. Scaled Dot-Product & Multi-Head Self-Attention
Self-attention computes dynamic contextual weights measuring how strongly every token attends to all other tokens in the sequence (e.g., resolving `"it"` back to `"cat"` in `"The cat sat because it was tired"`):

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Where `Q` = Query, `K` = Key, `V` = Value, and `d_k` scales variance cleanly. **Multi-Head Attention** runs multiple attention projections in parallel (e.g., `12 heads × 64 dims`) so different heads capture distinct syntactic, semantic, and coreference relationships simultaneously.

### 2. Encoder vs. Decoder Topologies
| Architecture | Attention Direction | Primary Objective | Canonical Examples |
| :--- | :--- | :--- | :--- |
| **Encoder-Only** | Bidirectional (sees past + future tokens) | Masked understanding, classification, dense representation | BERT, sentence embedding models |
| **Decoder-Only** | Unidirectional / Causal (attends strictly to past tokens) | Autoregressive **next-token prediction** | GPT family (`GPT-2` to `GPT-4`), Claude, Llama |

### 3. Sparse Scaling via Mixture of Experts (`MoE`)
Rather than activating all parameters for every token, **MoE** layers route each token to only a subset of specialized feed-forward "expert" subnetworks (e.g., `Mixtral 8x7B` contains 8 experts totaling `47B` parameters, yet activates only 2 experts / `~13B` params per forward pass), drastically improving quality-per-FLOP.

---

## Tokenization, Dense Embeddings & Context Windows

- **[[Tokenization]]**: Subword **Byte Pair Encoding (BPE)** (`~50k` vocab in `tiktoken`) avoids Out-Of-Vocabulary explosion from word-level splits while preventing excessive sequence lengths from character-level splits (`100 tokens ≈ 75 words`).
- **Dense Semantic Embeddings**: `Token ID` lookup maps discrete tokens to dense vectors (`GPT-2: 768 dims`, `Llama: 4096 dims`, `GPT-3: 12,288 dims`) preserving semantic geometry (`king - man + woman = queen`), summed with **Positional Embeddings** (sinusoidal or learned) since self-attention has no inherent sequence order.
- **[[Context Window Management|Context Window]] Growth**: Expanded from `2,048` (`GPT-3`) and `8k–128k` (`GPT-4`) to `200k` (`Claude`) and `1M–10M` (`Gemini`), enabling whole-codebase and long-document reasoning.

---

## Pre-Training Mechanics & Scaling Laws

- **Self-Supervised Objective**: Maximize $\sum \log P(t_i \mid t_1, \dots, t_{i-1})$ across massive web/domain datasets via Gradient Descent without manual labeling, yielding a **Pre-trained Base Model**.
- **Training Corpus Composition**: Large-scale web crawls (`Common Crawl ~60%`), long-context `Books (~15%)`, high-quality `Wikipedia (~3%)`, `GitHub` code, and `ArXiv` reasoning papers—requiring aggressive quality filtering and deduplication.
- **Scaling Laws**:
  - **Kaplan et al. Power Law**: Loss decreases smoothly as a power law ($\text{Loss} \propto N^{-0.07}$) when scaling parameters, dataset size, and compute (`GPT-3 ≈ $4M`, `GPT-4 ≈ $100M` across thousands of A100 GPUs).
  - **Chinchilla Optimal Scaling**: Model size and training token count contribute equally to compute efficiency—training a `70B` model on `1.4T` tokens outperforms a `280B` model under-trained on `300B` tokens for the same compute budget.

---

## Relationships

- **Foundational Input Layer**: Directly extends [[Tokenization]] and feeds [[LLM Fine-Tuning and Alignment]].
- **Context & Retrieval**: Governs how [[Context Window Management]] and [[Retrieval-Augmented Generation and Vector DBs]] allocate scarce attention capacity.
- **Inference Trade-offs**: Connects to [[LLM Inference Optimization and Security]] (`KV Cache`, `Flash Attention`, and `MoE` routing efficiency).
