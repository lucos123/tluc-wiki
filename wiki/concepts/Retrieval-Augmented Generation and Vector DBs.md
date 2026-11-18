---
title: "Retrieval-Augmented Generation and Vector DBs"
date: 2026-11-17
tags:
  - concept
  - context-engineering
  - llm-foundations
  - architecture
source: "[[LLM Handbook 50 Concepts]]"
---

# Retrieval-Augmented Generation and Vector DBs

**Retrieval-Augmented Generation (RAG)** anchors LLM responses in external, verifiable knowledge retrieved at query time rather than relying exclusively on static parametric memory from pre-training. Paired with **Vector Databases** and dense semantic **Embeddings**, RAG overcomes model knowledge cutoffs, protects private data boundaries, enables source citations, and suppresses hallucinations ([[LLM Handbook 50 Concepts]]).

---

## Standard vs. Advanced RAG Pipeline

```
Ingestion:  Documents ─▶ Chunking ─▶ Embeddings ─▶ Vector DB (HNSW Index)
                                                         │
Query Time: User Query ─▶ Query Embedding ───────────────┴─▶ Top-k Retrieval (k=3..5)
                                                                     │
                                                                     ▼
                                          Augment (Prompt + Context) ─▶ LLM + Citations
```

### Advanced RAG Patterns
When naive single-pass chunk retrieval misses nuanced queries, production pipelines layer:
- **Query Rewriting**: Re-formulate ambiguous user questions before vector search.
- **HyDE (Hypothetical Document Embeddings)**: Generate a synthetic ideal answer first and embed *it* to improve document-to-document similarity matching.
- **Re-ranking**: Re-score initial Top-K candidates with a higher-precision cross-encoder before prompt insertion.
- **Parent Document Retriever**: Match against small, focused child chunks (`100–200` tokens) for precision, then pass the larger parent window to the generator for complete context.
- **Self-RAG**: Let the LLM dynamically decide when retrieval is needed and verify retrieved support before answering.

---

## Embeddings, Chunking & Indexing

| Component | Standard Choices & Parameters | Engineering Trade-offs |
| :--- | :--- | :--- |
| **Embedding Models** | `text-embedding-ada-002` ([[OpenAI]], `1536 dims`), `all-mpnet-base-v2` (`768 dims`, open), `all-MiniLM-L6-v2` (`384 dims`, lightweight/free) | Higher dimensions capture richer nuance; small open models slash cost & latency |
| **Chunking Strategy** | **Fixed** (`500` / overlap `50`), **Recursive** (`500–1000` / overlap `50–100`), **Semantic** (split on similarity drop) | **Recursive chunking** (respecting paragraphs/sentences) is the recommended default |
| **Similarity Metrics** | **Cosine Similarity** ($\frac{A \cdot B}{\|A\|\|B\|} \in [-1, 1]$), Dot Product, Euclidean | Cosine similarity is magnitude-invariant and standard for text embeddings |
| **ANN Indexing** | **HNSW** (*Hierarchical Navigable Small World*) | Fast approximate nearest-neighbor graph traversal trading tiny recall loss for low latency |

---

## Vector Database Ecosystem Comparison

| Store / Library | Deployment Model | Key Characteristics |
| :--- | :--- | :--- |
| **Chroma** | Open Source (Local / Client) | Python-native (`chroma.Client()`), ideal for prototyping & local RAG |
| **pgvector** | Postgres Extension | Zero-new-infra SQL + vector search; strong default when already running PostgreSQL at moderate scale ([[AI Engineer Interview Notes]]) |
| **Pinecone** | Managed Cloud | Serverless scaling, low operational overhead, high throughput |
| **Weaviate** | Open Source | Hybrid vector + keyword search with GraphQL API |
| **FAISS** | Open Source Library (Meta AI) | Ultra-fast in-memory similarity search library (not a full database server) |
| **Qdrant** | Open Source (Rust) | High-speed filtering + low-latency production vector engine |
| **Milvus** | Open Source Distributed | Built for billion-scale enterprise vector collections |

---

## Production Quality, Security & RAG Evaluation (Senior Signals)

Synthesized from [[AI Engineer Interview Notes]]:
- **Embedding Parity & Privacy**: Choose API embeddings to ship fast, or self-hosted open weights (`BGE`, `E5`, `Nomic`) for zero per-token inference cost and strict VPC data boundaries—and **always keep index-time and query-time embedding models identical**.
- **Hybrid Search + Cross-Encoder Reranking**: Combine dense vector similarity with sparse **`BM25`** keyword scoring whenever queries involve SKUs, error codes, version numbers, or proper nouns; fetch `Top-50` cheaply and cross-encoder rerank to `Top-5`.
- **Pre-Retrieval ACL Metadata Filtering**: Enforce document permissions via chunk metadata filters **before** vector similarity search runs—never rely on prompting an LLM to withhold unauthorized chunks already stuffed into context.
- **Document-Structure Chunking Rule**: Never split markdown tables or code blocks across chunk boundaries; escalate from `512`-token overlap baselines to semantic/hierarchical chunking only when `recall@k` metrics diagnose context fragmentation.
- **RAG Evaluation Triad**: Measure retrieval independently (**`Recall@k`** / hit rate on a golden question $\rightarrow$ expected-chunk dataset) alongside generation (**Faithfulness**, answer relevance, and source citation accuracy) to isolate retrieval bugs from prompt bugs.

---

## Orchestration Ecosystem

Modern RAG and tool-using [[Agent Loop Lifecycle|agents]] commonly leverage **LangChain** (`PromptTemplate`, `RecursiveCharacterTextSplitter`, `VectorStoreRetriever`), **LlamaIndex** (data-framework specialized for indexing and retrieval), **LangGraph** (stateful cyclic agent graphs), **Haystack**, and **Semantic Kernel**.

---

## Relationships

- **Sources**: [[LLM Handbook 50 Concepts]], [[AI Engineer Interview Notes]], [[AI Complete Handbook]]
- **Memory & Context Layer**: Directly powers the retrieval tier of [[Context Engineering Pipeline]], [[AI System Design and Production Architecture]], and external memory for [[Agent Loop Lifecycle]].
- **Alternative to Weight Updates**: Contrasts cleanly against parameter modification in [[LLM Fine-Tuning and Alignment]].
- **Hallucination & Eval Mitigation**: Reduces extrinsic hallucinations measured in [[LLM Inference Optimization and Security]], [[Product Evals and Error Analysis]], and [[Model Evaluation and Validation]].
