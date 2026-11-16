---
title: "Types of Machine Learning Handbook"
date: 2026-11-16
tags:
  - source
  - machine-learning
  - visual-guide
  - llm-foundations
  - verification
source: "[[raw/articles/ai-other/types-of-machine-learning-handbook.md]]"
source_type: visual-notes
---

# Các Loại Machine Learning Bằng Tiếng Việt — Hướng Dẫn Toàn Diện (13 Trang)

**Source Files**:
- [[raw/articles/ai-other/types-of-machine-learning-handbook.md]] *(Bài đăng Facebook gốc của [[Viet Nguyen AI]], 2026-11-16)*
- [[raw/screenshots/types-of-machine-learning-handbook/00.jpg]] *(Cover: Tổng quan 6 nhánh Machine Learning)*
- [[raw/screenshots/types-of-machine-learning-handbook/01.jpg]] *(1: Cơ bản về ML & Phân loại 4 nhóm chính)*
- [[raw/screenshots/types-of-machine-learning-handbook/02.jpg]] *(2: Supervised Learning — Classification & Regression)*
- [[raw/screenshots/types-of-machine-learning-handbook/03.jpg]] *(3: Unsupervised Learning — Clustering, Giảm chiều, Luật kết hợp)*
- [[raw/screenshots/types-of-machine-learning-handbook/04.jpg]] *(4: Semi-Supervised Learning — Quy trình, Ứng dụng, Ưu/Nhược điểm)*
- [[raw/screenshots/types-of-machine-learning-handbook/05.jpg]] *(5: Self-Supervised Learning — Pretext Tasks, Pseudo-Labels & AI hiện đại)*
- [[raw/screenshots/types-of-machine-learning-handbook/06.jpg]] *(6: Reinforcement Learning — Agent-Environment Loop & Thuật toán RL)*
- [[raw/screenshots/types-of-machine-learning-handbook/07.jpg]] *(7: Các thuật toán Regression — Linear, Polynomial, Ridge, Lasso, Elastic Net)*
- [[raw/screenshots/types-of-machine-learning-handbook/08.jpg]] *(8: Các thuật toán Classification — Logistic, KNN, Decision Tree, Random Forest, SVM, Naive Bayes)*
- [[raw/screenshots/types-of-machine-learning-handbook/09.jpg]] *(9: Các thuật toán Clustering — K-Means, Hierarchical, DBSCAN, GMM)*
- [[raw/screenshots/types-of-machine-learning-handbook/10.jpg]] *(10: Dimensionality Reduction — PCA, LDA, t-SNE & Feature Selection)*
- [[raw/screenshots/types-of-machine-learning-handbook/11.jpg]] *(11: Đánh giá & So sánh mô hình — Confusion Matrix, ROC-AUC, K-Fold Cross-Validation)*
- [[raw/screenshots/types-of-machine-learning-handbook/12.jpg]] *(12: Cheat Sheet tổng hợp & Top 100 câu hỏi phỏng vấn ML)*

---

## Tổng Quan Bộ Tài Liệu

Bộ tài liệu infographic 13 trang do [[Viet Nguyen AI]] chuyển ngữ sang tiếng Việt từ ấn phẩm tiếng Anh gốc (`instagram.com/p/Dddnl_eDcj6`), hệ thống hóa toàn diện kiến thức nền tảng Machine Learning từ các mô hình học tập ([[Machine Learning Paradigms]]), thuật toán kinh điển ([[Supervised Learning Algorithms]], [[Unsupervised Learning and Dimensionality Reduction]]), đến phương pháp đánh giá mô hình ([[Model Evaluation and Validation]]) và ma trận ôn tập phỏng vấn.

Triết lý cốt lõi:
$$\text{Dữ liệu học pattern, không phải quy tắc} \longrightarrow \text{Feature tốt} > \text{Mô hình phức tạp}$$

---

## Tổng Hợp 5 Khối Kiến Thức Trọng Tâm

### 1. Hệ Sinh Thái Các Phương Pháp Học ([[Machine Learning Paradigms]]) — Trang 00–06
- **Supervised Learning:** Học ánh xạ từ dữ liệu có nhãn cho Classification (nhãn rời rạc) và Regression (giá trị liên tục).
- **Unsupervised Learning:** Khai phá cấu trúc ẩn trong dữ liệu không nhãn qua Clustering, Dimensionality Reduction và Association Rules.
- **Semi-Supervised Learning:** Kết hợp ít dữ liệu có nhãn + nhiều dữ liệu không nhãn (Self-Training, Co-Training, Graph-based); tiết kiệm chi phí gán nhãn nhưng nhạy cảm với nhiễu lan truyền nhãn sai.
- **Self-Supervised Learning:** Tự tạo pseudo-labels qua **pretext tasks** (Masked LM cho BERT, Next Token Prediction cho GPT, Contrastive Learning cho CLIP, MAE cho ảnh, VideoGPT) để học representation tổng quát.
- **Reinforcement Learning:** Agent tương tác với Environment theo chu trình State ($s$), Action ($a$), Reward ($r$) để tìm optimal policy $\pi(a|s)$ tối đa hóa $\sum_{t=0}^\infty \gamma^t r_t$ qua Q-Learning, DQN, Policy Gradient, Actor-Critic và PPO.
- **Paradigm bổ trợ:** Online Learning, Transfer Learning, Multi-Task Learning, Few-Shot Learning, Active Learning.

### 2. Nhóm Thuật Toán Có Giám Sát ([[Supervised Learning Algorithms]]) — Trang 07–08
- **5 thuật toán Regression:** Linear Regression (OLS), Polynomial Regression, Ridge (L2 thu nhỏ hệ số), Lasso (L1 chọn feature đưa hệ số về 0), Elastic Net (L1 + L2).
- **6 thuật toán Classification:** Logistic Regression (Sigmoid), KNN (lân cận $k$ theo khoảng cách), Decision Tree (Gini / Information Gain), Random Forest (ensemble bagging + majority voting), SVM (maximum margin hyperplane + kernel trick RBF), Naive Bayes (Bayes' Theorem).

### 3. Nhóm Thuật Toán Không Giám Sát & Giảm Chiều ([[Unsupervised Learning and Dimensionality Reduction]]) — Trang 09–10
- **4 thuật toán Clustering:** K-Means (centroid/inertia), Hierarchical (dendrogram bottom-up/top-down), DBSCAN (mật độ, xử lý tốt hình dạng bất kỳ & outlier), GMM (soft clustering dùng phân phối Gaussian + thuật toán EM).
- **Giảm chiều dữ liệu & Chọn đặc trưng:** PCA (unsupervised, giữ phương sai lớn nhất), LDA (supervised, tối đa hóa phân tách lớp), t-SNE (trực quan hóa cấu trúc cục bộ 2D/3D), và Feature Selection (Filter, Wrapper RFE, Embedded Lasso/Tree).

### 4. Đánh Giá & Kiểm Định Mô Hình ([[Model Evaluation and Validation]]) — Trang 11
- **Classification:** Accuracy, Precision, Recall, F1 Score (từ Confusion Matrix TP/FN/FP/TN), đường cong ROC và diện tích AUC.
- **Regression:** MAE (ít nhạy outlier), MSE (phạt nặng sai số lớn), RMSE (cùng đơn vị mục tiêu), và $R^2$ Score.
- **K-Fold Cross-Validation ($K = 5, 10$):** Chia đều $K$ fold huấn luyện trên $K-1$ fold và kiểm thử lặp lại để so sánh mô hình công bằng cùng chi phí thời gian và khả năng diễn giải.

### 5. Ma Trận Chọn Thuật Toán & Chuẩn Bị Phỏng Vấn — Trang 12
- Tổng hợp bảng tra cứu nhanh thuật toán theo loại bài toán, các công thức cốt lõi, 11 khái niệm nền tảng (Bias-Variance Tradeoff, Feature Scaling, Hyperparameter Tuning, Imbalanced Datasets...) và 10 chủ đề / 9 câu hỏi phỏng vấn mẫu.

---

## Synthesis Notes

- **Cầu nối từ ML cổ điển sang LLM & Agentic Systems:** Trang 05 làm rõ cách **Self-Supervised Learning** (Next Token Prediction & Contrastive Learning) đóng vai trò động cơ pretraining phía sau mọi LLM hiện đại trước khi kết hợp [[Tokenization]], [[Prompt Engineering]] và [[Few-Shot Prompting]].
- **Cấu trúc vòng lặp điều khiển:** Vòng lặp **Reinforcement Learning** (`Agent → Action → Environment → State/Reward`) là nguyên mẫu toán học cho các vòng lặp agent hiện đại trong [[Agent Loop Lifecycle]] và [[Control-Loop Engineering]], còn các metric định lượng trong [[Model Evaluation and Validation]] nối trực tiếp lên tầng đánh giá tự động [[Closed-Loop Evals]].

---

## Related Knowledge Nodes

- **Entities**: [[Viet Nguyen AI]]
- **Concepts**: [[Machine Learning Paradigms]], [[Supervised Learning Algorithms]], [[Unsupervised Learning and Dimensionality Reduction]], [[Model Evaluation and Validation]], [[Prompt Engineering]], [[Few-Shot Prompting]], [[Tokenization]], [[Agent Loop Lifecycle]], [[Control-Loop Engineering]], [[Closed-Loop Evals]]
- **Sources**: [[Prompt Engineering Handbook]], [[Token and API Price Guide]], [[Building Closed-Loop Evals for a Multimodal Agent at Scale]]
