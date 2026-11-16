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
| **Pinecone** | Managed Cloud | Serverless scaling, low operational overhead, high throughput |
| **Weaviate** | Open Source | Hybrid vector + keyword search with GraphQL API |
| **FAISS** | Open Source Library (Meta AI) | Ultra-fast in-memory similarity search library (not a full database server) |
| **Qdrant** | Open Source (Rust) | High-speed filtering + low-latency production vector engine |
| **Milvus** | Open Source Distributed | Built for billion-scale enterprise vector collections |

---

## Orchestration Ecosystem

Modern RAG and tool-using [[Agent Loop Lifecycle|agents]] commonly leverage **LangChain** (`PromptTemplate`, `RecursiveCharacterTextSplitter`, `VectorStoreRetriever`), **LlamaIndex** (data-framework specialized for indexing and retrieval), **LangGraph** (stateful cyclic agent graphs), **Haystack**, and **Semantic Kernel**.

---

## Relationships

- **Memory & Context Layer**: Directly powers the retrieval tier of [[Context Engineering Pipeline]] and external memory for [[Agent Loop Lifecycle]].
- **Alternative to Weight Updates**: Contrasts cleanly against parameter modification in [[LLM Fine-Tuning and Alignment]].
- **Hallucination & Eval Mitigation**: Reduces extrinsic hallucinations measured in [[LLM Inference Optimization and Security]] and [[Model Evaluation and Validation]].
