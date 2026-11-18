---
title: "AI Engineer Interview Notes (by Koteswara · koteswar.AI)"
source: "https://web.facebook.com/vietnh1009/posts/pfbid02fLqtSEEF2VCZd8iEGMLNxH8H3yg9zh9wH8bsrCfR9681kgUar2hTvCJst6pTJgKQl"
author:
  - "[[Koteswara]]"
  - "[[Viet Nguyen AI]]"
published: 2026-10-30
created: 2026-11-19
description: "Tài liệu ôn phỏng vấn AI Engineer 17 trang (All in One Place — by Koteswara, koteswar.AI) được Việt Nguyễn AI chia sẻ: LLM Fundamentals, Prompt Engineering & Systematic Debugging, RAG & Evaluation, AI Agents & Guardrails, Fine-tuning vs RAG vs Prompting, LLM-as-Judge & Production Cost/Latency, AI System Design (10M users Support AI), The Meta Pattern, 30-Day Prep Checklist và A-Z Quick Glossary."
tags:
  - "clippings"
  - "ai-engineering"
  - "interview-prep"
  - "system-design"
---

# AI Engineer Interview Notes

- **Nguồn chia sẻ:** [Facebook — Việt Nguyễn AI](https://web.facebook.com/vietnh1009/posts/pfbid02fLqtSEEF2VCZd8iEGMLNxH8H3yg9zh9wH8bsrCfR9681kgUar2hTvCJst6pTJgKQl)
- **Tác giả gốc (hiển thị trong tài liệu):** Koteswara (`koteswar.AI`)
- **Thời gian đăng bài Facebook:** 30 October 2026 at 14:00 (UTC+7)
- **Tương tác tại thời điểm thu thập:** 269 reactions (252 Like, 17 Love), 3 bình luận (chủ yếu tag bạn bè), 391 lượt chia sẻ
- **Thư mục hình ảnh gốc (17 trang):** `raw/screenshots/ai-engineer-interview-notes/` (`00.jpg` – `16.jpg`, kích thước đồng nhất `1241x1754`)

---

## Nội Dung Nguyên Văn Bài Đăng Facebook

> AI Engineer Interview Notes 🔥
> Nội dung chính trong bản notes này bao gồm:
> 🔹 LLM Fundamentals: giải thích attention, temperature vs top-p, vì sao model hallucinate
> 🔹 Prompt Engineering: zero-shot, few-shot, CoT, cách debug prompt có hệ thống, phòng thủ prompt injection
> 🔹 RAG: từ chunking, hybrid search, reranking đến câu hỏi "làm sao biết RAG của bạn chạy tốt?"
> 🔹 AI Agents: ReAct, tool calling, khi nào nên dùng multi-agent
> 🔹 Fine-tuning vs RAG vs Prompting: bảng quyết định rõ ràng
> 🔹 Evaluation & System Design: LLM-as-judge, tối ưu latency/chi phí, khung 5 bước để trả lời bài thiết kế hệ thống

---

## Chi Tiết 17 Trang Tài Liệu (Full Visual Transcription)

### Page 1 / 17 — Cover, TOC & 1. LLM Fundamentals *(1241x1754)*
![Trang 1](../../screenshots/ai-engineer-interview-notes/00.jpg)

- **Header:** *AI Engineer Interview Notes — All in One Place — by Koteswara · koteswar.AI*
- **Premise:** *"Practical, interview-first notes from going through AI Engineer interviews in 2026. Not a textbook — these are the topics interviewers actually test, the questions they ask, and how to answer them crisply."*
- **Table of Contents (10 Sections):** `1. LLM Fundamentals`, `2. Prompt Engineering`, `3. RAG Systems`, `4. AI Agents`, `5. Fine-tuning vs RAG vs Prompting`, `6. Evaluation & Production`, `7. AI System Design`, `8. The Meta Pattern`, `9. 30-Day Prep Checklist`, `10. A-Z Quick Glossary`.
- **What interviewers test (Section 1):** Explain transformer architecture (attention, tokenization, embeddings) in 2 minutes; sampling parameters (`temperature`, `top-k`, `top-p`); context windows, cost/latency implications & workarounds; hallucination causes & mitigations.
- **Transformer (2-min version):** `tokens -> embeddings -> attention layers -> feed-forward network -> logits -> next-token probabilities`. Autoregressive **Decoders** (GPT-style: 1 token at a time) vs bidirectional **Encoders** (BERT-style: embeddings/classification/NER, not generation).
- **Attention formula:** `Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V`. Scaled by $\sqrt{d_k}$ for numerical stability; Multi-head attention runs parallel heads tracking syntax, coreference, etc.
- **Tokenization:** `1 token ≈ 0.75 English words`; model-specific (GPT BPE `tiktoken`); multilingual text & code cost more tokens.

---

### Page 2 / 17 — Embeddings, Sampling, Context Windows, Hallucination & LLM Q&As *(1241x1754)*
![Trang 2](../../screenshots/ai-engineer-interview-notes/01.jpg)

- **Embeddings:** Dense vectors (`768–3072 dims`), similarity via **cosine similarity**.
- **Sampling parameters:**
  - `Temperature`: Scales logits before softmax (`0–0.3` deterministic extraction/classification/factual; `0.7–1.2` brainstorming/creative).
  - `Top-k`: Keeps k most likely tokens (mostly legacy control).
  - `Top-p (nucleus)`: Smallest token set whose cumulative probability $\ge p$ (`0.9–0.95` balanced default). **Rule of thumb: change temperature OR top-p, not both at once.**
- **Context windows & Cost:** Implications: (1) cost scales with tokens (`150K` input on `200K` context is expensive); (2) latency grows with input length; (3) **Lost in the middle** degrades center recall. Workarounds: conversation summarization, RAG over raw doc dumps, sliding windows, routing retrieval steps to smaller models.
- **Hallucination (causes & fixes):** Causes: (1) noisy training data; (2) next-token fluency objective vs truth; (3) missing grounding. Fixes: RAG citations, structured decoding, low temperature, verification step, HITL.
- **5 Sample Q&As:** Explains self-attention in 1 min; Temperature `0` vs `1`; Why long contexts degrade; How embeddings enable semantic search (`"car breakdown"` retrieves `"vehicle malfunction"`); Fixing fabricated paper citations in production.

---

### Page 3 / 17 — LLM Cheat Sheet, Common Mistakes & 2. Prompt Engineering *(1241x1754)*
![Trang 3](../../screenshots/ai-engineer-interview-notes/02.jpg)

- **LLM Q&A (cont.):** Autoregressive decoders vs encoder-only models (encoder for RAG retrieval embeddings, decoder for generation).
- **LLM Cheat Sheet & Common Mistakes:**
  - Never say *"the model understands"* — it predicts tokens.
  - Don't tune `temperature` and `top-p` together.
  - Don't dump everything into context instead of retrieving.
  - Low temperature reduces randomness, NOT hallucination.
- **2. Prompt Engineering:** Tests zero-shot vs few-shot vs CoT; systematic debugging framework (not trial-and-error); prompt injection attacks & defenses.
- **Key concepts:** `Zero-shot` (cheapest), `Few-shot` (`2–5` examples when output schema/tone matters; watch example selection bias), `Chain-of-thought (CoT)` (zero-shot CoT *"Let's think step by step"*, few-shot CoT, self-consistency majority voting).

---

### Page 4 / 17 — Prompt Debugging, Prompt Injection Defenses & Prompt Q&As *(1241x1754)*
![Trang 4](../../screenshots/ai-engineer-interview-notes/03.jpg)

- **Decision Rule:** Start `Zero-shot` $\rightarrow$ add `Few-shot` only if format/tone breaks $\rightarrow$ add `CoT` only if reasoning breaks.
- **6-Step Systematic Prompt Debugging Framework:**
  1. `Reproduce` (pin exact input & output)
  2. `Isolate` (test instruction alone vs retrieved context vs examples)
  3. `Inspect` (factual error $\implies$ grounding/RAG bug; task misunderstanding $\implies$ instruction rewrite)
  4. `Change one thing` (never tweak instruction + examples + temperature simultaneously)
  5. `Build a regression set` (`10–20` eval cases)
  6. `Version the prompt` (in code/config, never chat logs)
- **Prompt Injection & Defense-in-Depth:** Treat retrieved/user text as untrusted data (`<user_content>...</user_content>`), least-privilege tools, input/output filtering, HITL for irreversible actions (send email, delete, purchase), anomalous tool-call monitoring.
- **6 Sample Q&As + Start of Cheat Sheet (`Zero-shot`).** *(Includes example of prompt failure that is actually a retrieval/data bug.)*

---

### Page 5 / 17 — Prompt Cheat Sheet & 3. RAG Systems *(1241x1754)*
![Trang 5](../../screenshots/ai-engineer-interview-notes/04.jpg)

- **Prompt Cheat Sheet (`Few-shot`, `Zero-shot CoT`, `Few-shot CoT`, `Self-consistency` `N × reasoning tokens`) & Common Mistakes** (prompt-tweaking by vibes; using few-shot to fix a CoT reasoning issue; trusting retrieved content; giant unversioned system prompts).
- **3. RAG Systems:** Pipeline: `Ingest -> chunk -> embed -> vector DB -> embed query -> retrieve top-k -> (rerank) -> stuff into prompt -> generate with citations`.
- **4 Chunking Strategies:**
  - `Fixed-size` (e.g., `512 tokens, overlap 50`): Easy baseline, splits mid-thought.
  - `Semantic chunking`: Split on topic/embedding shifts.
  - `Hierarchical`: Retrieve small child chunk, return large parent chunk.
  - `Document-structure-aware`: Split on headings/sections/tables (**never split tables or code blocks across chunks**).

---

### Page 6 / 17 — Embeddings, Vector DBs, Hybrid Search, Reranking & RAG Evaluation *(1241x1754)*
![Trang 6](../../screenshots/ai-engineer-interview-notes/05.jpg)

- **Embeddings:** OpenAI API (fast dev, cost per token, leaves VPC) vs Open-source (`BGE`, `E5`, `Nomic` — free local inference, privacy/scale). **Hard rule:** Index and query embedding models MUST match.
- **Vector Databases:** `Pinecone` (managed, check scaling cost), `Weaviate` (open-source + managed, built-in hybrid search), `Qdrant` (Rust, fast self-host), `pgvector` (Postgres extension, best simple choice at moderate scale when already running Postgres).
- **Retrieval Quality Techniques:**
  - `Hybrid search`: Dense semantic + sparse `BM25` keyword scores (fixes exact-term failures on SKUs, error codes, proper nouns).
  - `Reranking`: Retrieve top-50 cheaply $\rightarrow$ cross-encoder rerank to top-5.
  - `Query expansion / HyDE`: Embed a hypothetical answer to bridge vocabulary gap.
  - `Metadata filtering`: Pre-filter by date, source, and **ACL permissions** before vector search.
- **Senior RAG Evaluation Answer:** Retrieval metrics (`recall@k` / hit rate on golden pairs) + Generation metrics (`faithfulness`, answer relevance, citation accuracy) via LLM-as-judge + human spot-checks + A/B tests.
- **Sample Q&As (Pipeline walk-through, Hybrid vs Pure vector, OpenAI vs BGE embeddings, Debugging hallucinating RAG).**

---

### Page 7 / 17 — RAG ACLs, Decision Cheat Sheet & 4. AI Agents *(1241x1754)*
![Trang 7](../../screenshots/ai-engineer-interview-notes/06.jpg)

- **RAG Q&As (cont.):** Pre-retrieval ACL metadata filtering (never ask the LLM to *"ignore"* unauthorized chunks—never retrieve them); Junior vs Senior RAG answer; When RAG is wrong (static small facts $\rightarrow$ prompt; style/behavior change $\rightarrow$ fine-tuning; tight latency budget).
- **RAG Cheat Sheet & Common Mistakes.**
- **4. AI Agents:** Tests `ReAct (Thought -> Action -> Observation)` loop, termination (`final answer`, max-iteration cap, stop condition), Tool schemas, Single vs Multi-agent, Memory, Guardrails.

---

### Page 8 / 17 — Tool Calling, Single vs Multi-Agent, Memory & Agent Guardrails *(1241x1754)*
![Trang 8](../../screenshots/ai-engineer-interview-notes/07.jpg)

- **Tool Calling:** Precise JSON schemas (`descriptions`, `required` fields, `enums`); return actionable error strings as observations (not raw stack traces); cap retries; design **idempotent** reads vs human-gated destructive writes; least-privilege capabilities.
- **Single vs Multi-Agent:** Default to single agent; pay multi-agent orchestration cost only when distinct roles + clean handoffs (`researcher -> writer -> critic`) justify parallelism & context separation.
- **Memory:** `Short-term (working)` = context-window management problem (summarization, sliding windows); `Long-term` = data problem (persistent store/vector DB + write/retrieval/forgetting policies because **stale facts are worse than no facts**).
- **Production Guardrails:** Max iteration cap, tool-call budgets per run, treat tool outputs as untrusted data, human approval gates, per-run cost budgets + kill switches, full trajectory logging & trajectory evals.
- **Sample Q&As (5 Q&As).**

---

### Page 9 / 17 — Agent Q&As/Cheat Sheet & 5. Fine-Tuning vs RAG vs Prompting *(1241x1754)*
![Trang 9](../../screenshots/ai-engineer-interview-notes/08.jpg)

- **Agent Q&As (Indirect prompt injection on `delete database` tool; Agent vs Chain)** + **Agent Cheat Sheet & Common Mistakes** (`"query: string"` vague schemas!).
- **5. Fine-tuning vs RAG vs Prompting:** Comparison matrix starts (`Prompting` changes nothing in model; `RAG` injects retrieved knowledge per-call; `Fine-tuning` updates model weights).

---

### Page 10 / 17 — Fine-Tuning vs RAG Matrix, LoRA & Decision Framework *(1241x1754)*
![Trang 10](../../screenshots/ai-engineer-interview-notes/09.jpg)

- **Comparison Matrix (cont.):** Knowledge cutoff, Cost profile, Latency, Risk (`Prompt brittleness`, `Retrieval quality`, `Overfitting / catastrophic forgetting`).
- **Verbatim 3-Step Decision Framework:** (1) Start with **Prompting**; (2) Move to **RAG** for large/changing/proprietary facts & citations; (3) Use **Fine-tuning** (`LoRA` adapter matrices / `distillation` with 100s+ high-quality examples) for consistent style/behavior or shrinking to a faster/cheaper model — **never to inject new facts** (`RLHF`/`DPO` as post-training preference alignment).
- **Signature Tradeoff Quote:** *"Prompting is cheapest to change but weakest at knowledge; RAG grounds answers in fresh data at the cost of retrieval latency and pipeline complexity; fine-tuning bakes in behavior at the cost of upfront data and training effort — and none of them fixes a bad problem definition."*
- **Sample Q&As (5 Q&As).**

---

### Page 11 / 17 — Build-vs-Train Matrix & 6. Evaluation & Production *(1241x1754)*
![Trang 11](../../screenshots/ai-engineer-interview-notes/10.jpg)

- **Decision Matrix Cheat Sheet & Common Mistakes.**
- **6. Evaluation & Production:**
  - **LLM-as-a-Judge & 4 Biases:** `Verbosity bias` (prefers longer answers), `Position bias` (prefers first option), `Self-preference` (favors same-model style), `Leniency drift`. Mitigations: pairwise comparison with position swapping, reference-based rubrics, human calibration, **never judge a model's own outputs uncritically**.
  - **Human Evaluation:** Non-negotiable for high-stakes medical/legal/financial domains, subjective brand tone, and calibrating judges (inter-rater agreement).
  - **Latency Optimization Levers:** Streaming (`TTFT`), Exact prompt caching + Semantic caching, Small-model routing, Concurrency/batching, Shorter contexts (faster prefill), knowing `TTFT` and `tokens/sec`.
  - **Cost Management:** Token budgets (request/user/day), small-by-default routing, context right-sizing (5 chunks vs 50), aggressive caching, **track unit economics (`cost per query/task`)**.

---

### Page 12 / 17 — Production Monitoring, Q&As & Latency/Cost Cheat Sheet *(1241x1754)*
![Trang 12](../../screenshots/ai-engineer-interview-notes/11.jpg)

- **Production Monitoring Signals:** `p50/p95 TTFT` & total latency, cost per query, error rates, per-tool success rates, user signals (thumbs/reformulations/abandonment), live eval faithfulness/relevance, query/data drift, rate limits, PII/secret leakage detection.
- **6 Production Q&As + Latency/Cost Lever Cheat Sheet + Start of Common Mistakes.**

---

### Page 13 / 17 — 7. AI System Design (5-Step Framework & 10M-User Support AI) *(1241x1754)*
![Trang 13](../../screenshots/ai-engineer-interview-notes/12.jpg)

- **The 5-Step AI System Design Framework:**
  1. `Requirements & clarifying questions` (users, scale, latency, quality bar, constraints)
  2. `Architecture` (boxes, data flow)
  3. `Deep dive` (pick 2–3 hardest components: retrieval, eval, agent loop)
  4. `Tradeoffs` (name explicit latency/cost/quality price)
  5. `Monitoring & iteration`
- **Worked Case Study — "Design a customer support AI for 10M users" (`<2s` chat first response, `~5%` peak concurrency):**
  - **Architecture:** `User -> Chat API -> Orchestrator -> Intent/Complexity Router (<300ms small model)` routing `Simple/FAQ -> RAG pipeline` OR `Complex -> Tool-using Agent (order lookup, ticket create, KB search)`, wrapped by `Guardrails (PII redact, injection filter)` and `Escalation -> Human agent queue (full transcript + AI summary)`.
  - **Deep Dive:** Retrieval (`hybrid search`, `top-50 -> top-5` rerank, `product version/locale` metadata filter, golden `recall@k` + `faithfulness`), Router (`<300ms` bypasses agent loop for FAQ volume), Escalation (confidence/frustration/out-of-scope triggers).
  - **Tradeoffs:** Automation rate (`60% -> 80%`) vs wrong-answer risk; `per-query cost × 10M` drives small-model routing + caching as primary architecture, not micro-optimization.

---

### Page 14 / 17 — Support AI Iteration, Design Q&As & Checklist *(1241x1754)*
![Trang 14](../../screenshots/ai-engineer-interview-notes/13.jpg)

- **Step 5 Monitoring & Close:** Track auto-resolution rate, escalation rate, CSAT, faithfulness, `p95` latency, cost/conversation. Ship FAQ RAG path first; weekly triage of human escalations feeds the eval loop (`retrieval`, `reasoning`, `missing knowledge`, `policy gap`).
- **6 System Design Q&As + Design Phase Checklist.**

---

### Page 15 / 17 — System Design Mistakes, 8. The Meta Pattern & 9. 30-Day Prep Checklist *(1241x1754)*
![Trang 15](../../screenshots/ai-engineer-interview-notes/14.jpg)

- **System Design Mistakes:** Jumping into components without requirements; over/under-scaling; `"we'll use GPT-4 for everything"`; omitting escalation/guardrails/monitoring; failing to state tradeoffs.
- **8. The Meta Pattern:** Strongest candidates tie every technical choice to **business impact + measurement** (`cost/1M queries`, `latency percentiles`, `eval scores`): *"Build systems, measure them, understand tradeoffs. That's what gets offers."*
- **9. 30-Day Prep Checklist (1–2h/day):**
  - `Week 1`: Foundations & Prompting (Attention whiteboard, sampling, CoT/few-shot, debugging & injection defense)
  - `Week 2`: RAG (Minimal `pgvector`/`Qdrant` RAG, semantic re-chunking, hybrid + rerank 20 questions, golden `recall@k` + `faithfulness`)
  - `Week 3`: Agents & Build-vs-Train (ReAct with 2–3 tools + caps, schema/injection validation, Single vs Multi-agent sketch, Decision Matrix + LoRA)
  - `Week 4`: Production & System Design (`LLM-as-judge`, latency/cost calcs, agent monitoring dashboard, 3 timed System Design mocks, weak-spot review)
- **10. A-Z Quick Glossary begins (`Agent`).**

---

### Page 16 / 17 — A-Z Quick Glossary (`Attention` – `RLHF/DPO`) *(1241x1754)*
![Trang 16](../../screenshots/ai-engineer-interview-notes/15.jpg)

Concise one-line definitions for 26 terms: `Attention`, `BM25`, `Chain-of-thought (CoT)`, `Chunking`, `Context window`, `Cosine similarity`, `Cross-encoder (reranker)`, `Embeddings`, `Evals`, `Faithfulness`, `Few-shot`, `Fine-tuning`, `Guardrails`, `Hallucination`, `Hybrid search`, `HyDE`, `LLM-as-judge`, `LoRA`, `Lost in the middle`, `PGVector`, `Prompt injection`, `RAG`, `ReAct`, `Recall@k`, `Reranking`, `RLHF / DPO`.

---

### Page 17 / 17 — A-Z Quick Glossary (`Self-consistency` – `Zero-shot`) *(1241x1754)*
![Trang 17](../../screenshots/ai-engineer-interview-notes/16.jpg)

Concise one-line definitions for final 11 terms: `Self-consistency`, `Streaming`, `System prompt`, `Temperature`, `Token`, `Tokenization`, `Tool calling`, `Top-p (nucleus)`, `TTFT`, `Vector DB`, `Zero-shot`. Sign-off: *"Prepared by Koteswara — documenting the AI Engineer journey in real time. More practical AI engineering notes at koteswar.AI."*
