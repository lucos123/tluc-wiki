---
title: "Context Selection and Sequencing"
date: 2026-08-12
tags:
  - concept
  - context-engineering
  - harness-engineering
source: "[[What Is Context Engineering]]"
---

# Context Selection and Sequencing

**Context Selection and Sequencing** is the structural optimization phase in [[Context Engineering]] governing *what* data enters the LLM context window (Selection) and *where* each layer is ordered in the prompt payload (Sequencing).

---

## 1. Context Selection

Selection filters raw retrieved information down to task-relevant data while protecting the inference window:
- **Noise Filtering & Reranking**: Stripping redundant boilerplate text and ranking search results by semantic utility.
- **Context Poisoning Prevention**: Guarding against malicious, untrusted, or corrupted external data inputs.

---

## 2. Context Sequencing (Ordering Rule)

```mermaid
graph TD
    Layer1["1. System Prompt Layer (Instructions, Rules, Constraints)"] --> Layer2["2. High-Relevance Context Layer (Retrieved Data, RAG Reranked)"]
    Layer2 --> Layer3["3. History & Background Layer (Prior Turn Summaries, Logs)"]
```

Because LLMs pay uneven attention to tokens across long payloads, optimal payload sequencing dictates:
1. **Instructions & Rules First**: Place core system prompts and behavioral guardrails at the top of the prompt.
2. **Most Relevant Context Second**: Position primary RAG retrievals and tool results immediately below system rules.
3. **Historical / Background Data Last**: Place older conversation history and lower-priority details further back.

See [[What Is Context Engineering]], [[Context Engineering]], [[Context Processing and Management]], and [[System Prompt Caching Optimization]].
