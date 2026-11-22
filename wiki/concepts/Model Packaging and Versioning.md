---
title: "Model Packaging and Versioning"
date: 2026-11-16
tags:
  - concept
  - ai-deployment
  - llmops
  - verification
source: "wiki/sources/AI Deployment Notes.md"
---

# Model Packaging and Versioning

**Model Packaging and Versioning** ensures AI systems are reproducible, auditable, and safely rollbackable in production by bundling and tracking not only trained model weights, but every runtime, prompt, retrieval, and configuration dependency that determines system behavior. See [AI Deployment Notes](../sources/AI%20Deployment%20Notes.md).

---

## 1. Beyond Model Weights: What Must Be Packaged & Versioned

A serialized weights file alone cannot run reliably in production. Deployable AI artifacts bundle:
- **Model weights & Tokenizer** (critical for LLMs; see [Tokenization](Tokenization.md))
- **Inference code & model runtime** + pinned library/framework dependencies
- **Configuration** (environment variables, serving & batching parameters)
- **LLM/Agent Application Artifacts:** **Prompt templates** and **Retrieval / RAG configuration** (vector store index, embedding model, chunking settings)
- **Data Version, Evaluation Results & Metadata** (owner, timestamp, changelog)

> **Multi-Component Versioning Example:** Bumping an application from `v1.0.0` (`Llama-3-8B` + `prompt: v1` $\rightarrow$ `72%`) to `v1.1.0` (`Llama-3-8B` + `prompt: v2` $\rightarrow$ `78%`) changes system behavior and score **without** retraining model weights; `v1.2.0` may upgrade both `Llama-3-70B` and `retrieval: v2` (`82%`).

---

## 2. Container/Artifact Registry vs. Model Registry

| Registry Type | Primary Responsibility | Representative Tools |
| :--- | :--- | :--- |
| **Artifact / Container Registry** | Stores immutable deployable packages and container images | Docker Hub, AWS ECR, Google GCR/Artifact Registry, Azure ACR |
| **Model Registry** | Tracks model versions, lineage metadata, evaluation scores, and promotion lifecycle states | MLflow, Hugging Face Hub, AWS SageMaker Model Registry, Google Vertex AI |

---

## 3. Promotion Pipeline, Lifecycle States & Challenges

- **Promotion Flow:** `Build & Package → Register → Staging (Evaluate) → Approve (Quality Gate) → Production (Deploy) → Monitor` (with fast **Rollback** to a previously tagged version if metrics regress).
- **Typical Model States:** `Experiment → Validated → Registered → Staging → Approved → Production → Retired` (*not every trained model should become production-ready*).
- **Operational Challenges:** Huge model artifact sizes (storage & download latency), training–serving dependency skew, **version sprawl** across prompts/models/configs, **data lineage** tracking, evaluation drift, and access control—paralleling the immutable action and provenance requirements in [Enterprise Agent Stack](Enterprise%20Agent%20Stack.md).

---

## Related Pages
- **Sources**: [AI Deployment Notes](../sources/AI%20Deployment%20Notes.md)
- **Concepts**:
  - [AI Deployment Lifecycle and Environments](AI%20Deployment%20Lifecycle%20and%20Environments.md)
  - [Inference Serving and Deployment Patterns](Inference%20Serving%20and%20Deployment%20Patterns.md)
  - [Tokenization](Tokenization.md)
  - [Context Engineering](Context%20Engineering.md)
  - [Enterprise Agent Stack](Enterprise%20Agent%20Stack.md)
