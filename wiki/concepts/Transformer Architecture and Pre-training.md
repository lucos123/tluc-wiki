---
title: "Transformer Architecture and Pre-training"
date: 2026-11-17
tags:
  - concept
  - llm-foundations
  - deep-learning
  - machine-learning
source: "wiki/sources/LLM Handbook 50 Concepts.md"
---

# Transformer Architecture and Pre-training

The **Transformer** architecture—introduced in *Attention Is All You Need* (2017)—forms the neural backbone of modern Large Language Models (LLMs). Combined with self-supervised **next-token pre-training** over trillion-token corpora, Transformers give rise to emergent capabilities such as in-context learning, zero-shot generalization, and step-by-step reasoning without task-specific feature engineering ([LLM Handbook 50 Concepts](../sources/LLM%20Handbook%2050%20Concepts.md)).

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

### 1. Scaled Dot-Product, Masking & Multi-Head Self-Attention
Self-attention projects input embeddings $X \in \mathbb{R}^{n \times d_{\text{model}}}$ via learned weight matrices ($Q = XW_Q, K = XW_K, V = XW_V$) and computes contextual weights across all tokens, with optional mask matrix $M$ ($0$ valid, $-\infty$ masked):

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V$$

Where `Q` = Query, `K` = Key, `V` = Value, and `d_k` scales dot-product variance. **Multi-Head Attention** concatenates $h$ parallel heads ($\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W_O$) so different subspaces track syntax, coreference, and semantics simultaneously. Because computing $QK^T$ and Softmax takes **$O(n^2 \cdot d)$ time and $O(n^2)$ memory** in sequence length $n$, long-context scaling motivates sparse/linear attention variants (`Sparse Transformer`, `Longformer`, `BigBird`) ([LLM Handwritten Study Guide 15 Pages](../sources/LLM%20Handwritten%20Study%20Guide%2015%20Pages.md)).

### 2. LayerNorm, Residual Blocks, Positional Math & Feed-Forward Sublayers
- **Residual + Layer Normalization**: Replaces batch-dependent BatchNorm with per-feature stabilization $y = \text{LayerNorm}(x + \text{Sublayer}(x))$ where $\text{LN}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}\cdot\gamma + \beta$ (works cleanly even with tiny batch sizes).
- **Feed-Forward Network (`FFN`)**: Position-wise 2-layer MLP expanding $d_{\text{model}} = 512 \rightarrow d_{\text{ff}} = 2048$ with `ReLU`, `Tanh`, or **`GELU`** ($f(x) = x\,\Phi(x)$, using Gaussian CDF for smoother gradients favored in `BERT` and `GPT`): $\text{FFN}(x) = \text{GELU}(xW_1 + b_1)W_2 + b_2$.
- **Positional Encodings (Permutation Invariance Fix)** ([Transformers Detailed Notes and Revision Guide](../sources/Transformers%20Detailed%20Notes%20and%20Revision%20Guide.md)): Because Self-Attention is permutation-invariant (cannot distinguish *"dog bites man"* from *"man bites dog"*), Transformers inject positional signals across three generations:
  - *Sinusoidal PE*: Deterministic $PE(pos, 2i) = \sin(pos / 10000^{2i/d_{\text{model}}})$ and $PE(pos, 2i+1) = \cos(pos / 10000^{2i/d_{\text{model}}})$ enabling length extrapolation.
  - *Learned / Relative PE*: Trainable position lookup tables vs relative offset biases (`Transformer-XL`, `T5`).
  - *Long-Context Extrapolation (`32K–200K+`)*: **`RoPE`** (Rotary Position Embedding), **`ALiBi`**, **`LongRoPE`**, and **`YaRN`** paired with sliding-window / sparse attention.

### 3. Encoder vs. Decoder vs. Encoder-Decoder & BERT Variants
| Architecture | Attention Direction | Primary Objective | Canonical Examples |
| :--- | :--- | :--- | :--- |
| **Encoder-Only** | Bidirectional (sees past + future tokens) | Masked understanding, classification, NER, dense retrieval embeddings | `BERT`, **`RoBERTa`** (no NSP, dynamic masking), **`ALBERT`** (factorized / shared params), **`DistilBERT`** (distilled), **`ELECTRA`** (replaced-token detection), **`DeBERTa`** (disentangled attention) |
| **Decoder-Only** | Unidirectional / Causal upper-triangle mask | Autoregressive **next-token prediction** | `GPT` family, `Claude`, `LLaMA`, `Mistral` |
| **Encoder-Decoder** | Bidirectional Encoder + Causal & **Cross-Attention** Decoder ($Q$ from Decoder, $K/V$ from Encoder) | Sequence-to-sequence translation & structured summarization | `T5` (text-to-text, relative bias), `BART`, `mT5` |

### 4. Sparse Scaling via Mixture of Experts (`MoE`)
Rather than activating all parameters for every token, **MoE** gating networks (`Switch Transformer`, `GLaM`, `Mixtral`) route each token to only a subset of specialized feed-forward "expert" subnetworks (e.g., `Mixtral 8x7B` contains 8 experts totaling `47B` parameters, yet activates only 2 experts / `~13B` params per forward pass), drastically improving quality-per-FLOP.

---

## Tokenization, Dense Embeddings & Context Windows

- **[Tokenization](Tokenization.md)**: Subword **Byte Pair Encoding (BPE)** (`~50k` vocab in `tiktoken`) avoids Out-Of-Vocabulary explosion from word-level splits while preventing excessive sequence lengths from character-level splits (`100 tokens ≈ 75 words`).
- **Dense Semantic Embeddings**: `Token ID` lookup maps discrete tokens to dense vectors (`GPT-2: 768 dims`, `Llama: 4096 dims`, `GPT-3: 12,288 dims`) preserving semantic geometry (`king - man + woman = queen`), summed with **Positional Embeddings** (sinusoidal or learned) since self-attention has no inherent sequence order.
- **[Context Window](Context%20Window%20Management.md) Growth**: Expanded from `2,048` (`GPT-3`) and `8k–128k` (`GPT-4`) to `200k` (`Claude`) and `1M–10M` (`Gemini`), enabling whole-codebase and long-document reasoning.

---

## Pre-Training Mechanics & Scaling Laws

- **Self-Supervised Objective**: Maximize $\sum \log P(t_i \mid t_1, \dots, t_{i-1})$ across massive web/domain datasets via Gradient Descent without manual labeling, yielding a **Pre-trained Base Model**.
- **Training Corpus Composition**: Large-scale web crawls (`Common Crawl ~60%`), long-context `Books (~15%)`, high-quality `Wikipedia (~3%)`, `GitHub` code, and `ArXiv` reasoning papers—requiring aggressive quality filtering and deduplication.
- **Scaling Laws**:
  - **Kaplan et al. Power Law**: Loss decreases smoothly as a power law ($\text{Loss} \propto N^{-0.07}$) when scaling parameters, dataset size, and compute (`GPT-3 ≈ $4M`, `GPT-4 ≈ $100M` across thousands of A100 GPUs).
  - **Chinchilla Optimal Scaling**: Model size and training token count contribute equally to compute efficiency—training a `70B` model on `1.4T` tokens outperforms a `280B` model under-trained on `300B` tokens for the same compute budget.

---

## Relationships

- **Sources**: [LLM Handbook 50 Concepts](../sources/LLM%20Handbook%2050%20Concepts.md), [LLM Handwritten Study Guide 15 Pages](../sources/LLM%20Handwritten%20Study%20Guide%2015%20Pages.md), [Transformers Detailed Notes and Revision Guide](../sources/Transformers%20Detailed%20Notes%20and%20Revision%20Guide.md), [AI Complete Handbook](../sources/AI%20Complete%20Handbook.md)
- **Foundational Input Layer**: Directly extends [Tokenization](Tokenization.md) and neural building blocks ($z = \sum w_i x_i + b$, `Sigmoid`/`Tanh`/`ReLU`/`Leaky ReLU`, `MSE`/`BCE`/`CCE`, Backpropagation across `CNN`/`RNN`/`LSTM`/`Autoencoder`/`GAN`), feeding [LLM Pretraining, Optimization and Decoding](LLM%20Pretraining%2C%20Optimization%20and%20Decoding.md) and [LLM Fine-Tuning and Alignment](LLM%20Fine-Tuning%20and%20Alignment.md).
- **Context & Retrieval**: Governs how [Context Window Management](Context%20Window%20Management.md) and [Retrieval-Augmented Generation and Vector DBs](Retrieval-Augmented%20Generation%20and%20Vector%20DBs.md) allocate scarce attention capacity.
- **Inference Trade-offs**: Connects to [LLM Inference Optimization and Security](LLM%20Inference%20Optimization%20and%20Security.md) (`KV Cache`, `Flash Attention`, and `MoE` routing efficiency).
- **Vision & Multimodal Extension**: Adapts `Patchification + Positional Encoding + Encoder` architectures into [Vision Transformers and Multimodal AI](Vision%20Transformers%20and%20Multimodal%20AI.md) (`ViT`, `DETR`, `CLIP`, Multimodal fusion; [Computer Vision Handbook](../sources/Computer%20Vision%20Handbook.md)).
