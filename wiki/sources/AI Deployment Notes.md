---
title: "AI Deployment Notes"
date: 2026-11-16
tags:
  - source
  - ai-deployment
  - llmops
  - visual-guide
  - inference-economics
source: "[[raw/articles/ai-other/ai-deployment-notes.md]]"
source_type: visual-notes
---

# Ghi Chú AI Deployment Bằng Tiếng Việt — Chương 1 (12 Trang)

**Source Files**:
- [[raw/articles/ai-other/ai-deployment-notes.md]] *(Bài đăng Facebook gốc của [[Viet Nguyen AI]], 2026-11-15)*
- [[raw/screenshots/ai-deployment-notes/00.jpg]] *(Cover: AI Deployment Architecture Ecosystem — Docker, Kubernetes, AWS, Terraform, CI/CD, Grafana, PostgreSQL, vLLM/TGI, ChromaDB)*
- [[raw/screenshots/ai-deployment-notes/01.jpg]] *(1: Giới thiệu về AI Deployment, 6-layer stack & khác biệt phần mềm truyền thống)*
- [[raw/screenshots/ai-deployment-notes/02.jpg]] *(2: Vòng đời 7 bước của ứng dụng AI/ML & vòng đời lồng nhau)*
- [[raw/screenshots/ai-deployment-notes/03.jpg]] *(3: AI Development vs AI Deployment)*
- [[raw/screenshots/ai-deployment-notes/04.jpg]] *(4: Model Training vs Model Inference)*
- [[raw/screenshots/ai-deployment-notes/05.jpg]] *(5: Môi trường Development, Staging và Production cho AI)*
- [[raw/screenshots/ai-deployment-notes/06.jpg]] *(6: Model Packaging, Registry & Versioning)*
- [[raw/screenshots/ai-deployment-notes/07.jpg]] *(7: Batch vs Real-Time vs Async Inference)*
- [[raw/screenshots/ai-deployment-notes/08.jpg]] *(8: Online vs Offline Predictions & Hybrid Pattern)*
- [[raw/screenshots/ai-deployment-notes/09.jpg]] *(9: Cloud vs Edge vs Hybrid Deployment)*
- [[raw/screenshots/ai-deployment-notes/10.jpg]] *(10: Kiến trúc End-to-End 6 tầng, Observability, Security & Reliability)*
- [[raw/screenshots/ai-deployment-notes/11.jpg]] *(11: Model Serving & Inference Servers — vLLM, Triton, Dynamic Batching, TTFT/TPS)*

---

## Tổng Quan Bộ Tài Liệu

Bộ tài liệu trực quan 12 trang do [[Viet Nguyen AI]] chuyển ngữ sang tiếng Việt từ ấn phẩm tiếng Anh gốc (`instagram.com/p/Ddkzwpmku1K`), giải đáp trọn vẹn bài toán *"sau khi train xong thì làm gì"* để đưa mô hình AI/ML từ môi trường thử nghiệm lên hệ thống production phục vụ người dùng thực tế ở quy mô lớn.

Chu trình cốt lõi:
$$\text{MODEL} \longrightarrow \text{SERVE} \longrightarrow \text{SCALE} \longrightarrow \text{OBSERVE}$$

---

## Tổng Hợp 3 Trụ Cột Kiến Thức

### 1. Vòng Đời, Môi Trường & Tách Biệt Vai Trò ([[AI Deployment Lifecycle and Environments]]) — Trang 01–05
- **Vòng đời ứng dụng AI/ML 7 giai đoạn:** `Define → Data & Discover → Build → Evaluate → Deploy → Operate → Learn & Improve`, trong đó vòng đời Model (`Data → Train → Evaluate → Version`) nằm lồng bên trong vòng đời Application.
- **Tách bạch Phát triển vs Triển khai & Training vs Inference:** *"Development / Training tạo ra trí thông minh; Deployment / Inference mang lại giá trị."* Hệ thống AI khác phần mềm truyền thống vì mang tính xác suất (probabilistic), tài sản gồm `Code + Model + Data + Prompt + Retrieval` và chịu tác động **data/model drift**.
- **Luồng promote môi trường:** `Development` (mock data, lặp nhanh) $\rightarrow$ `Staging` (cấu hình giống prod, data đại diện **không PII**, eval chất lượng & an toàn) $\rightarrow$ `Production` (traffic thật, hardened, rollback).

### 2. Đóng Gói, Registry & Quản Lý Phiên Bản ([[Model Packaging and Versioning]]) — Trang 06
- Đóng gói không chỉ là weights mà gồm: `Weights + Tokenizer + Inference Code + Dependencies + Config + Prompt Templates + Retrieval Config + Eval Results`.
- Phân biệt **Artifact/Container Registry** (Docker Hub, ECR, GCR, ACR) và **Model Registry** (MLflow, Hugging Face, SageMaker, Vertex AI) với vòng đời `Experiment → Validated → Registered → Staging → Approved → Production → Retired`.
- Thay đổi ở `prompt` hoặc `retrieval` tạo ra phiên bản ứng dụng mới ngay cả khi model weights giữ nguyên (`v1.0.0 → v1.1.0 → v1.2.0`).

### 3. Kiến Trúc Phục Vụ, Pattern Inference & Tối Ưu Serving ([[Inference Serving and Deployment Patterns]]) — Trang 00, 07–11
- **Batch vs Real-Time vs Async:** Chọn Batch để tối ưu throughput/chi phí (xử lý offline), Real-Time cho latency thấp, và Async queue cho tác vụ agent/media chạy lâu.
- **Offline vs Online Predictions & Hybrid:** Precompute candidates offline và re-rank online bằng ngữ cảnh real-time.
- **Cloud vs Edge vs Hybrid:** Đánh đổi giữa sức mạnh GPU tập trung trên Cloud và độ trễ thấp, hoạt động offline, giữ dữ liệu tại chỗ + model quantization trên Edge.
- **Model Serving & Inference Servers (`Model ≠ Model Server ≠ API`):** Sử dụng `vLLM`, `TGI`, `NVIDIA Triton`, `TorchServe`, `BentoML` hoặc Managed Inference (`SageMaker`, `Azure AI Foundry`, `Vertex AI`) trên Kubernetes; cân bằng **Dynamic Batching** (latency $\leftrightarrow$ throughput), áp dụng `Retry / Fallback model / Cache / Graceful degradation` và giám sát bộ chỉ số LLM (`TTFT`, `Tokens/s`, `Inter-token latency`, `Context length`, `GPU memory`).

---

## Synthesis Notes

- **Kết nối với Kinh tế Token & Lựa chọn Mô hình:** Quy trình serving LLM (`User Prompt → Tokenization → Prefill → Iterative Decode`) ở Trang 11 giải thích trực tiếp cơ chế hạ tầng đứng sau sự chênh lệch chi phí prefill vs decode trong [[Token and API Price Guide]] và [[Token Economics]], cũng như các quyết định cân bằng giữa chất lượng và tốc độ trong [[Inference Speed vs Intelligence Trade-off]].
- **Kết nối với Enterprise Stack & Vận hành Agent:** Yêu cầu về Data Lineage, Access Control, Guardrails, Staging Evals và Drift Monitoring trong [[AI Deployment Notes]] khớp chặt với kiến trúc production trong [[Enterprise Agent Stack]] và quy trình tự động hóa [[Closed-Loop Evals]].

---

## Related Knowledge Nodes

- **Entities**: [[Viet Nguyen AI]]
- **Concepts**: [[AI Deployment Lifecycle and Environments]], [[Model Packaging and Versioning]], [[Inference Serving and Deployment Patterns]], [[Inference Speed vs Intelligence Trade-off]], [[Tokenization]], [[Token Economics]], [[Closed-Loop Evals]], [[Enterprise Agent Stack]], [[Model Evaluation and Validation]], [[Context Engineering]]
- **Sources**: [[Types of Machine Learning Handbook]], [[Prompt Engineering Handbook]], [[Token and API Price Guide]], [[Why Your Enterprise Tech Stack Isn't Ready for AI Agents]]
