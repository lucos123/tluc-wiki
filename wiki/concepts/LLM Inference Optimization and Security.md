---
title: "LLM Inference Optimization and Security"
date: 2026-11-17
tags:
  - concept
  - llmops
  - cost-optimization
  - security
  - verification
source: "[[LLM Handbook 50 Concepts]]"
---

# LLM Inference Optimization and Security

Deploying large models (`7B–175B+`) in production requires balancing **latency, GPU memory, and unit economics** alongside **rigorous evaluation, hallucination mitigation, adversarial security, and data privacy**. Together, these optimization and governance layers turn raw foundation models into reliable production systems ([[LLM Handbook 50 Concepts]]).

---

## 1. Model Compression & Quantization

| Technique | Mechanism | Practical Impact |
| :--- | :--- | :--- |
| **FP32 $\rightarrow$ FP16** | Half-precision float weights | `2×` smaller footprint, faster mixed-precision compute |
| **INT8 Quantization** | 8-bit integer weight representation | `4×` smaller memory with minimal quality degradation |
| **INT4 (`GPTQ` / `AWQ`)** | 4-bit weights (**AWQ** preserves activation-salient weights, often outperforming GPTQ) | `8×` memory savings vs FP32; powers edge 7B inference and **QLoRA** |
| **Pruning** | Zero out/remove ~50% low-salience weights or connections | Smaller model footprint and lower compute |
| **Knowledge Distillation** | Train small `7B` *student* model to mimic large `70B` *teacher* outputs | Retains strong task accuracy at a fraction of inference cost |

---

## 2. Inference Acceleration & Serving Economics

- **KV Cache**: Caches attention Key and Value tensors across prior decoding steps to avoid redundant recomputation (`>2×` faster token generation).
- **Flash Attention**: IO-aware GPU SRAM tiling minimizing HBM memory reads/writes and VRAM footprint.
- **Continuous Batching & `vLLM`**: Dynamic request batching combined with **PagedAttention** cuts GPU memory fragmentation—delivering up to **24× higher throughput** over naive Hugging Face Transformers baselines alongside **Hugging Face TGI** and **NVIDIA TensorRT-LLM** (see [[Inference Serving and Deployment Patterns]] and [[LLMOps & Inference]]).
- **Speculative Decoding**: A small fast *draft* model proposes multi-token lookaheads verified in parallel by the large target model (`>2×` speedup with mathematically unchanged distribution).
- **Model Parallelism & A100 Sizing Reference**:

| Model Size | Reference GPU Topology | Approximate Self-Hosted Rate | Deployment Context |
| :--- | :--- | :--- | :--- |
| `7B` | `1× A100 16GB` (or 4-bit quantized edge) | `~$0.50/hr` | Local Ollama/LM Studio, mobile edge |
| `13B` | `1× A100 40GB` | `~$1.50/hr` | Recommended open-source baseline |
| `70B` | `2× A100 80GB` (tensor/pipeline parallel) | `~$4/hr` | High-capability private hosting |
| `175B` | `8× A100 80GB` | `~$16/hr` | vs managed API baseline (`~$0.02 / 1k tokens` GPT-3 ref) |

---

## 3. Evaluation Benchmarks, Contamination & Hallucinations

- **Automated Metrics & Benchmarks**: `Perplexity` (lower = better next-token calibration), `Accuracy`, `F1`, `BLEU/ROUGE`; alongside capability benchmarks `MMLU` (`GPT-3 43% -> GPT-4 86%`), `GSM8K` math (`15% -> 92%`), `HumanEval` (`164` coding problems), `HellaSwag`, `TruthfulQA`, `BIG-Bench`, and **Chatbot Arena** human Elo ratings.
- **Data Contamination**: Benchmark leakage into training data inflates apparent scores through memorization rather than true generalization (mitigated via fresh private evals in [[Closed-Loop Evals]] and [[Model Evaluation and Validation]]).
- **Hallucination Taxonomy & Mitigations**: Distinguishes **Intrinsic Hallucinations** (contradicting provided context) from **Extrinsic Hallucinations** (unverifiable against sources). Mitigate with RAG citations, lower temperature, grounded prompting, truthful fine-tuning, and automated fact checking.

---

## 4. Security Attacks, Guardrails & Privacy

| Threat / Attack Vector | Mechanism | Defensive Controls |
| :--- | :--- | :--- |
| **Prompt Injection** | Adversarial input (`"Ignore previous instructions..."`) hijacking system behavior | Input Validation/sanitization, context isolation, privilege separation (see [[Agent Skills Security Audit]]) |
| **Jailbreaking** | Role-play bypasses (`DAN - Do Anything Now`) circumventing safety filters | **RLHF / DPO / Constitutional AI**, Red Teaming, Output Filtering, Guardrails (`NeMo Guardrails`, `Llama Guard`) |
| **Data Poisoning** | Corrupting training/fine-tuning corpora with backdoors or bias | Strict training data validation, provenance auditing ([[Software Supply Chain Security]]) |
| **Model Inversion / Leakage** | Extracting memorized PII or training secrets via targeted querying | **Differential Privacy**, **Federated Learning**, **PII Anonymization**, opt-out of training on user data |

---

## Relationships

- **Serving & Economics**: Deepens [[Inference Serving and Deployment Patterns]], [[LLMOps & Inference]], [[AI Deployment Lifecycle and Environments]], and [[Cost Optimization]].
- **Evaluation & Verification**: Pairs with [[Model Evaluation and Validation]], [[Closed-Loop Evals]], and [[Verification Loop]].
- **Security**: Complements [[Agent Skills Security Audit]] and [[Software Supply Chain Security]].
