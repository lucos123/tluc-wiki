---
title: "Model Evaluation and Validation"
date: 2026-11-16
tags:
  - concept
  - machine-learning
  - verification
source: "[[Types of Machine Learning Handbook]]"
---

# Model Evaluation and Validation

**Model Evaluation and Validation** measures how accurately an ML model generalizes to unseen data, selects appropriate loss/business metrics across classification and regression, and prevents overfitting through resampling strategies such as K-Fold Cross-Validation. See [[Types of Machine Learning Handbook]].

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
| **$R^2$ Score** | $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | Proportion of target variance explained by the model | $(-\infty, 1]$ — Higher is better |

---

## 3. Validation, Trade-offs & Model Selection

- **K-Fold Cross-Validation:** Partitions training data into $K$ folds (commonly $K = 5$ or $10$), iteratively training on $K - 1$ folds and validating on the remaining fold, then averaging performance for fair model comparison.
- **Core Selection Principles:**
  - Account for **Bias–Variance Tradeoff**, **Feature Scaling** (Standardization/Normalization), **Hyperparameter Tuning** (Grid/Random Search), training latency, and interpretability alongside raw metric scores.
  - Heuristic from [[Types of Machine Learning Handbook]]: *"Better features > complex models."*
- **Agentic Connection:** Systematic evaluation gates and benchmark validation in classical ML extend into automated production loops in [[Closed-Loop Evals]].

---

## Related Pages
- **Sources**: [[Types of Machine Learning Handbook]], [[AI Eval Concepts Explained in 15 Minutes]]
- **Concepts**: [[Machine Learning Paradigms]], [[Supervised Learning Algorithms]], [[Unsupervised Learning and Dimensionality Reduction]], [[Closed-Loop Evals]], [[Product Evals and Error Analysis]], [[LLM-as-a-Judge and Eval Alignment]]
