---
title: "LLM Handbook 50 Concepts"
date: 2026-11-17
tags:
  - source
  - visual-guide
  - llm-foundations
  - machine-learning
source: "raw/articles/ai-other/llm-handbook-50-concepts.md"
source_type: visual-notes
url: "https://web.facebook.com/vietnh1009/posts/pfbid0g3aXPLj3DsP3HWD4qytFnqe9gnyb4Pu8hfyy1PoyuFJCKkzymTqV1qCJcWF2C44vl"
original_url: "https://www.instagram.com/p/DdjbVVblt_Y/?img_index=1"
author: "Viet Nguyen AI"
---

# LLM Handbook 50 Concepts (Cẩm nang LLM - 50 khái niệm cần nắm vững)

**Source**: [raw/articles/ai-other/llm-handbook-50-concepts.md](../../raw/articles/ai-other/llm-handbook-50-concepts.md) | **Author / Adapter**: [Viet Nguyen AI](../entities/Viet%20Nguyen%20AI.md) (`vietnh1009`, published `2026-11-11`) | **Original Instagram Source**: https://www.instagram.com/p/DdjbVVblt_Y/?img_index=1

---

## Executive Summary

A 20-page Vietnamese visual sketchnote handbook translating and adapting 50 core concepts spanning the entire Large Language Model (LLM) engineering lifecycle—from Transformer internals and tokenization through pre-training scaling laws, PEFT (`LoRA`/`QLoRA`), alignment (`RLHF`/`DPO`), prompting, RAG/Vector DBs, ReAct agents, inference optimization (`Quantization`, `KV Cache`, `vLLM`), security/privacy, portfolio projects, and LLM interview preparation.

---

## Knowledge Pillar Breakdown

### 1. Foundations: Transformers, Tokenization & Pre-Training (Pages 1–4)
- **LLM Scale & Emergent Abilities**: Models ranging from `117M` (`GPT-1`) and `1.5B` (`GPT-2`) to `175B` (`GPT-3`) and `~1.7T` (`GPT-4`), unlocking zero-shot, few-shot, and in-context reasoning over traditional task-specific ML.
- **[Transformer Internals](../concepts/Transformer%20Architecture%20and%20Pre-training.md)**: Input text $\rightarrow$ [Tokenization](../concepts/Tokenization.md) (`Subword BPE`, `tiktoken`, ~50k vocab, `1 token ≈ 0.75 words`) $\rightarrow$ Dense Embeddings (`768 / 4096 / 12288 dims`) + Positional Encodings $\rightarrow$ stacked `Self-Attention` (`softmax(QK^T / sqrt(d_k))V`, Multi-Head) + MLP blocks $\rightarrow$ next-token probability logits. Contrasts bidirectional Encoders (`BERT`) vs unidirectional Decoders (`GPT`).
- **Pre-training & Scaling**: Self-supervised next-token prediction over curated corpora (`Common Crawl 60%`, `Books 15%`, `Wikipedia 3%`, `GitHub Code`, `ArXiv`) governed by Kaplan Power Laws (`Loss ~ N^-0.07`) and **Chinchilla** compute-optimal balance (`70B + 1.4T tokens > 280B + 300B tokens`).

### 2. Adaptation, Alignment & Prompting (Pages 5–7)
- **[Fine-Tuning (PEFT)](../concepts/LLM%20Fine-Tuning%20and%20Alignment.md)**: Instruction tuning turns base text-completers into assistant models; **LoRA** freezes `W` and trains low-rank `BA` (`~0.1% params`, `r=8/16`), while **QLoRA** quantizes weights to 4-bit to fine-tune `65B` models on a single `48GB` GPU.
- **Alignment (`3H`: Helpful, Harmless, Honest)**: Classical 3-stage **RLHF** (`SFT -> Reward Model -> PPO with KL penalty`) vs modern **DPO** (optimizes directly on human preference pairs without an explicit RM or PPO) and **[Anthropic](../entities/Anthropic.md) Constitutional AI**.
- **[Prompt Engineering](../concepts/Prompt%20Engineering.md) & Sampling**: Zero-shot, [Few-Shot Prompting](../concepts/Few-Shot%20Prompting.md), [Chain-of-Thought Prompting](../concepts/Chain-of-Thought%20Prompting.md) (`CoT`), Role/Instruction/Format controls, and decoding controls (`Temperature 0 / 0.7 / 1.0`, `Top-p 0.9`, `Top-k 50`).

### 3. Applications: RAG, Vector DBs & Agents (Pages 8–10, 14)
- **[RAG Pipeline](../concepts/Retrieval-Augmented%20Generation%20and%20Vector%20DBs.md)**: `Documents -> Recursive Chunking (500-1000 tokens, overlap 50-100) -> Embeddings -> Vector DB (HNSW / Cosine Similarity) -> Top-k Retrieval (k=3-5) -> Augmented Prompt -> Cited Generation`, enhanced via **Query Rewriting**, **HyDE**, **Re-ranking**, **Parent Document Retriever**, and **Self-RAG**.
- **LLM Agents & Frameworks**: `Agent = LLM + Reasoning + Planning + Tools + Memory + Goal` operating via the `Thought -> Action -> Observation` (**ReAct**) loop and Function Calling, implemented with `LangChain`, `LlamaIndex`, `LangGraph`, `Semantic Kernel`, `Haystack`, and `CrewAI`. (See [Agent Loop Lifecycle](../concepts/Agent%20Loop%20Lifecycle.md).)

### 4. Evaluation, Inference Optimization, Security & Infra (Pages 11–13, 17–18)
- **[Evaluation & Hallucination Control](../concepts/LLM%20Inference%20Optimization%20and%20Security.md)**: Perplexity, Accuracy, F1, BLEU/ROUGE, `MMLU`, `GSM8K`, `HumanEval`, `TruthfulQA`, `Chatbot Arena`, **Data Contamination**, and mitigating **Intrinsic vs. Extrinsic Hallucinations** (see also [Model Evaluation and Validation](../concepts/Model%20Evaluation%20and%20Validation.md)).
- **Inference Scaling & Serving**: `FP16 / INT8 / INT4` (`GPTQ`, `AWQ`), **Pruning**, **Distillation** (`70B -> 7B`), **KV Cache** (`>2x` speedup), **Flash Attention** (IO-aware tiling), **Speculative Decoding** (`>2x`), **vLLM** (`PagedAttention` + continuous batching, up to `24x` faster than baseline Hugging Face), `TGI`, `TensorRT-LLM`, plus `A100` cluster sizing (`$0.50/hr` for `7B` up to `$16/hr` for `175B` across `8x A100 80GB`). (Connects to [Inference Serving and Deployment Patterns](../concepts/Inference%20Serving%20and%20Deployment%20Patterns.md) and [Cost Optimization](../concepts/Cost%20Optimization.md).)
- **Security & Privacy**: Defending against Prompt Injection, Jailbreaking (`DAN`), Data Poisoning, and Model Inversion via Input Validation, Output Filtering, Guardrails (`NeMo Guardrails`, `Llama Guard`), Red Teaming, Differential Privacy, Federated Learning, and PII Anonymization.
- **2024–2026 Macro Trends**: Multimodal LLMs, `1M–10M` context windows ([Context Window Management](../concepts/Context%20Window%20Management.md)), Small Language Models (`Phi-3 3.8B`), **Mixture of Experts (`MoE`)** (`Mixtral 8x7B` activating `13B` of `47B` params), inference-time `o1`-style reasoning, and Open-Weight vs Closed API trade-offs.

### 5. Portfolio, Interview Prep & Career Roadmap (Pages 15–16, 19–20)
- Recommends a 6-project portfolio (`Private RAG Chatbot`, `Tool-Using ReAct Agent`, `LoRA Fine-Tune on Llama 7B`, `Function Calling`, `AI SaaS`, `YouTube Chat`), an 8-month structured roadmap from Python to Agents, and drills the 15 highest-frequency LLM interview traps (e.g., Encoder vs Decoder, `Fine-tuning vs RAG`, `RLHF vs DPO`).

---

## Visual Slide Index (20 Pages)

| Page | Topic | Screenshot | Key Visual Highlights |
| :--- | :--- | :--- | :--- |
| 01 | LLM Foundations & Timeline | [raw/screenshots/llm-handbook-50-concepts/00.jpg](../../raw/screenshots/llm-handbook-50-concepts/00.jpg) | Traditional ML vs LLM; `GPT-1` (`117M`) to `GPT-4` (`~1.7T`) |
| 02 | Transformer Architecture | [raw/screenshots/llm-handbook-50-concepts/01.jpg](../../raw/screenshots/llm-handbook-50-concepts/01.jpg) | Self-Attention `softmax(QK^T/sqrt(d_k))V`, Multi-Head, Encoder vs Decoder |
| 03 | Tokenization & Embeddings | [raw/screenshots/llm-handbook-50-concepts/02.jpg](../../raw/screenshots/llm-handbook-50-concepts/02.jpg) | Word vs Char vs BPE (`~50k`), Vector arithmetic, Context Windows |
| 04 | Pre-training & Scaling Laws | [raw/screenshots/llm-handbook-50-concepts/03.jpg](../../raw/screenshots/llm-handbook-50-concepts/03.jpg) | Common Crawl/Books/GitHub mix, Kaplan & Chinchilla laws |
| 05 | Fine-tuning & Instruction Tuning | [raw/screenshots/llm-handbook-50-concepts/04.jpg](../../raw/screenshots/llm-handbook-50-concepts/04.jpg) | Full FT vs LoRA (`~0.1%`, `W+BA`) vs QLoRA (`4-bit`, `65B/48GB`) |
| 06 | RLHF, DPO & Alignment | [raw/screenshots/llm-handbook-50-concepts/05.jpg](../../raw/screenshots/llm-handbook-50-concepts/05.jpg) | `3H` criteria, 3-step `SFT+RM+PPO` vs Reward-Model-free `DPO` |
| 07 | Prompt Engineering & Sampling | [raw/screenshots/llm-handbook-50-concepts/06.jpg](../../raw/screenshots/llm-handbook-50-concepts/06.jpg) | Zero/Few-shot, CoT, Role/Format, Temperature/Top-p/Top-k |
| 08 | RAG Architecture | [raw/screenshots/llm-handbook-50-concepts/07.jpg](../../raw/screenshots/llm-handbook-50-concepts/07.jpg) | Standard RAG pipeline vs Advanced RAG (`HyDE`, `Re-ranking`, `Self-RAG`) |
| 09 | Vector DBs & Chunking | [raw/screenshots/llm-handbook-50-concepts/08.jpg](../../raw/screenshots/llm-handbook-50-concepts/08.jpg) | Embedding dims, Cosine similarity, `HNSW`, 6 Vector DB comparison |
| 10 | LLM Agents & ReAct | [raw/screenshots/llm-handbook-50-concepts/09.jpg](../../raw/screenshots/llm-handbook-50-concepts/09.jpg) | `Thought -> Action -> Observation`, Function Calling, LangGraph/CrewAI |
| 11 | Evaluation & Hallucinations | [raw/screenshots/llm-handbook-50-concepts/10.jpg](../../raw/screenshots/llm-handbook-50-concepts/10.jpg) | Metrics, 7 Benchmarks, Contamination, Intrinsic vs Extrinsic Hallucinations |
| 12 | Optimization & Quantization | [raw/screenshots/llm-handbook-50-concepts/11.jpg](../../raw/screenshots/llm-handbook-50-concepts/11.jpg) | `FP32..INT4`, `GPTQ`, `AWQ`, `KV Cache`, `Flash Attention`, `Speculative Decoding` |
| 13 | Security, Safety & Privacy | [raw/screenshots/llm-handbook-50-concepts/12.jpg](../../raw/screenshots/llm-handbook-50-concepts/12.jpg) | Injection/Jailbreak/Poisoning defenses, Guardrails, Differential Privacy |
| 14 | Frameworks & Code Snippets | [raw/screenshots/llm-handbook-50-concepts/13.jpg](../../raw/screenshots/llm-handbook-50-concepts/13.jpg) | `LangChain`, `LlamaIndex`, `Ollama`, `vLLM`, `TGI` + Python RAG snippet |
| 15 | 6 Portfolio Projects | [raw/screenshots/llm-handbook-50-concepts/14.jpg](../../raw/screenshots/llm-handbook-50-concepts/14.jpg) | RAG Chatbot, ReAct Agent, LoRA, Function Calling, AI SaaS, YouTube Chat |
| 16 | Interview Q&A & Traps | [raw/screenshots/llm-handbook-50-concepts/15.jpg](../../raw/screenshots/llm-handbook-50-concepts/15.jpg) | Q1–Q10 walkthrough + importance/trap matrix |
| 17 | Scaling & GPU Costs | [raw/screenshots/llm-handbook-50-concepts/16.jpg](../../raw/screenshots/llm-handbook-50-concepts/16.jpg) | `vLLM (24x)` vs `TGI` vs `TensorRT-LLM`, `A100` cost breakdown (`7B–175B`) |
| 18 | Trends & Future of LLMs | [raw/screenshots/llm-handbook-50-concepts/17.jpg](../../raw/screenshots/llm-handbook-50-concepts/17.jpg) | Multimodal, 1M–10M context, SLMs, MoE, `o1`, Closed vs Open Source |
| 19 | Career, Salaries & Roadmap | [raw/screenshots/llm-handbook-50-concepts/18.jpg](../../raw/screenshots/llm-handbook-50-concepts/18.jpg) | 8–10 month skill roadmap + US/India/Remote compensation tables |
| 20 | 20-Topic Checklist & Top 15 Qs | [raw/screenshots/llm-handbook-50-concepts/19.jpg](../../raw/screenshots/llm-handbook-50-concepts/19.jpg) | Final mastery matrix and 15 top LLM interview questions |

---

## Synthesis Connections

- **Foundations**: Anchors [Transformer Architecture and Pre-training](../concepts/Transformer%20Architecture%20and%20Pre-training.md) and extends [Tokenization](../concepts/Tokenization.md) + [Prompt Engineering](../concepts/Prompt%20Engineering.md) (paired with equation-level study notes in [LLM Handwritten Study Guide 15 Pages](LLM%20Handwritten%20Study%20Guide%2015%20Pages.md) and [LLM Pretraining, Optimization and Decoding](../concepts/LLM%20Pretraining%2C%20Optimization%20and%20Decoding.md)).
- **Post-Training & Knowledge Retrieval**: Synthesized into [LLM Fine-Tuning and Alignment](../concepts/LLM%20Fine-Tuning%20and%20Alignment.md) and [Retrieval-Augmented Generation and Vector DBs](../concepts/Retrieval-Augmented%20Generation%20and%20Vector%20DBs.md) (complementing [Context Engineering Pipeline](../concepts/Context%20Engineering%20Pipeline.md)).
- **Production & Safety**: Synthesized into [LLM Inference Optimization and Security](../concepts/LLM%20Inference%20Optimization%20and%20Security.md), bridging [Inference Serving and Deployment Patterns](../concepts/Inference%20Serving%20and%20Deployment%20Patterns.md), [LLMOps & Inference](../topics/LLMOps%20%26%20Inference.md), [Cost Optimization](../concepts/Cost%20Optimization.md), [Closed-Loop Evals](../concepts/Closed-Loop%20Evals.md), and [Agent Skills Security Audit](../concepts/Agent%20Skills%20Security%20Audit.md).
