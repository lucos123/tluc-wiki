---
title: "Model Evaluation and Validation"
date: 2026-11-16
tags:
  - concept
  - machine-learning
  - verification
source: "wiki/sources/Types of Machine Learning Handbook.md"
---

# Model Evaluation and Validation

**Model Evaluation and Validation** measures how accurately an ML model generalizes to unseen data, selects appropriate loss/business metrics across classification and regression, and prevents overfitting through resampling strategies such as K-Fold Cross-Validation. See [Types of Machine Learning Handbook](../sources/Types%20of%20Machine%20Learning%20Handbook.md).

---

## 1. Classification Metrics (From the Confusion Matrix)

Given `TP` (True Positive), `TN` (True Negative), `FP` (False Positive), and `FN` (False Negative):

- **Accuracy:** $\frac{TP + TN}{TP + TN + FP + FN}$ — overall correctness; misleading on imbalanced datasets.
- **Precision:** $\frac{TP}{TP + FP}$ — fraction of positive predictions that are truly positive (critical when false positives are costly).
- **Recall (TPR):** $\frac{TP}{TP + FN}$ — fraction of actual positives successfully captured (critical in medical diagnosis or fraud screening).
- **F1 Score:** $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ — harmonic mean balancing Precision and Recall.
- **ROC Curve & AUC:** Plots True Positive Rate (Recall) against False Positive Rate across classification thresholds; $\text{AUC} \in [0, 1]$ measures class-separation ranking quality ($0.5 =$ random guessing; curves bowing toward top-left indicate strong separation).

---

## 2. Regression Metrics

| Metric | Formula | Sensitivity & Interpretation | Range & Direction |
| :--- | :--- | :--- | :--- |
| **MAE** | $\frac{1}{n}\sum_{i=1}^n \|y_i - \hat{y}_i\|$ | Average absolute error; robust against extreme outliers | $[0, \infty)$ — Lower is better |
| **MSE** | $\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2$ | Penalizes large errors quadratically | $[0, \infty)$ — Lower is better |
| **RMSE** | $\sqrt{\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2}$ | Preserves original target units while penalizing large errors | $[0, \infty)$ — Lower is better |
| **$R^2$ Score** | $1 - \frac{SSE}{SST} = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | Proportion of target variance explained by the model | $(-\infty, 1]$ — Higher is better |

---

## 3. Validation, Trade-offs & Model Selection

- **K-Fold Cross-Validation:** Partitions training data into $K$ folds (commonly $K = 5$ or $10$), iteratively training on $K - 1$ folds and validating on the remaining fold, then averaging performance for fair model comparison.
- **Fit Diagnostics (`Train` vs. `Test`):**
  - **Underfitting:** Low Train / Low Test (model overly simple).
  - **Good Fit:** High Train / High Test (captures signal without noise).
  - **Overfitting:** Very High Train / Low Test (memorizes noise — also requires external hyperparameter tuning such as `learning rate`, `max depth`, or ensemble size; see [Data Preprocessing and Feature Engineering](Data%20Preprocessing%20and%20Feature%20Engineering.md)).
- **Core Selection Principles:**
  - Account for **Bias–Variance Tradeoff**, **Feature Scaling** (Standardization/Normalization), **Hyperparameter Tuning** (Grid/Random Search), training latency, and interpretability alongside raw metric scores.
  - Heuristic from [Types of Machine Learning Handbook](../sources/Types%20of%20Machine%20Learning%20Handbook.md): *"Better features > complex models."*
- **Agentic Connection:** Systematic evaluation gates and benchmark validation in classical ML extend into automated production loops in [Closed-Loop Evals](Closed-Loop%20Evals.md) and [LLM-as-a-Judge and Eval Alignment](LLM-as-a-Judge%20and%20Eval%20Alignment.md).

---

## Related Pages
- **Sources**:
  - [Types of Machine Learning Handbook](../sources/Types%20of%20Machine%20Learning%20Handbook.md)
  - [AI Eval Concepts Explained in 15 Minutes](../sources/AI%20Eval%20Concepts%20Explained%20in%2015%20Minutes.md)
  - [Machine Learning Basics Notes](../sources/Machine%20Learning%20Basics%20Notes.md)
  - [Machine Learning and Deep Learning Cheat Sheets](../sources/Machine%20Learning%20and%20Deep%20Learning%20Cheat%20Sheets.md)
- **Concepts**:
  - [Machine Learning Paradigms](Machine%20Learning%20Paradigms.md)
  - [Supervised Learning Algorithms](Supervised%20Learning%20Algorithms.md)
  - [Unsupervised Learning and Dimensionality Reduction](Unsupervised%20Learning%20and%20Dimensionality%20Reduction.md)
  - [Data Preprocessing and Feature Engineering](Data%20Preprocessing%20and%20Feature%20Engineering.md)
  - [Neural Networks and Deep Learning Foundations](Neural%20Networks%20and%20Deep%20Learning%20Foundations.md)
  - [Closed-Loop Evals](Closed-Loop%20Evals.md)
  - [Product Evals and Error Analysis](Product%20Evals%20and%20Error%20Analysis.md)
  - [LLM-as-a-Judge and Eval Alignment](LLM-as-a-Judge%20and%20Eval%20Alignment.md)
