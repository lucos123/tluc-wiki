---
title: "Supervised Learning Algorithms"
date: 2026-11-16
tags:
  - concept
  - machine-learning
  - llm-foundations
source: "[[Types of Machine Learning Handbook]]"
---

# Supervised Learning Algorithms

**Supervised Learning** trains models on labeled `(input, ground-truth output)` pairs via a 5-stage pipeline (`Labeled Data → Data Preprocessing → Model Training → Testing/Evaluation → Inference`) to generalize onto unseen data across **Regression** (continuous outputs) and **Classification** (discrete classes). See [[Types of Machine Learning Handbook]].

---

## 1. Regression Algorithms (Continuous Target)

| Algorithm | Mathematical Formulation / Objective | Key Strength & Trade-off |
| :--- | :--- | :--- |
| **Linear Regression (OLS)** | $y = \theta_0 + \theta_1 x_1 + \dots + \theta_n x_n$ | Fast, highly interpretable; assumes linear relationships |
| **Polynomial Regression** | $y = \theta_0 + \theta_1 x + \theta_2 x^2 + \theta_3 x^3 + \dots$ | Captures non-linear curves using polynomial feature transforms |
| **Ridge Regression (L2)** | $J(\theta) = \frac{1}{2m}\sum (y - \hat{y})^2 + \lambda \sum \theta_j^2$ | Shrinks correlated coefficients to curb overfitting without zeroing them out |
| **Lasso Regression (L1)** | $J(\theta) = \frac{1}{2m}\sum (y - \hat{y})^2 + \lambda \sum \|\theta_j\|$ | Drives weak coefficients strictly to zero (embedded feature selection) |
| **Elastic Net (L1 + L2)** | $J(\theta) = \frac{1}{2m}\sum (y - \hat{y})^2 + \lambda_1 \sum \|\theta_j\| + \lambda_2 \sum \theta_j^2$ | Balances L1 sparsity and L2 stability across correlated features |

> *Implementation note*: L1 and L2 penalties typically apply strictly to **model weights** $w_j$ and exclude the bias/intercept term $b$ ([[Machine Learning and Deep Learning Cheat Sheets]]).

---

## 2. Classification Algorithms (Discrete Class)

| Algorithm | Core Mechanism | When to Choose |
| :--- | :--- | :--- |
| **Logistic Regression** | Linear logits passed through sigmoid: $P(y=1) = \frac{1}{1 + e^{-(w^T x + b)}}$ | Fast baseline for binary classification and calibrated probabilities |
| **K-Nearest Neighbors (KNN)** | Non-parametric instance lookup voting over $k$ closest neighbors (e.g., Euclidean distance) | Small datasets with simple local decision boundaries |
| **Decision Tree** | Recursive feature splits maximizing Gini impurity reduction or Information Gain | High interpretability; prone to overfitting without pruning |
| **Random Forest** | Bagging ensemble of trees trained on bootstrap data & random feature subsets via majority voting | Large tabular/high-dimensional datasets requiring strong accuracy and variance reduction |
| **Support Vector Machine (SVM)** | Finds maximum-margin separating hyperplane; uses kernel trick (e.g., RBF) for non-linear boundaries | High-dimensional spaces and sharp margin boundaries |
| **Naive Bayes** | Bayes' theorem $P(y \mid X) = \frac{P(X \mid y)P(y)}{P(X)}$ assuming conditional feature independence (Gaussian, Multinomial, Bernoulli) | Very fast training/inference on small datasets or high-dimensional text |

---

## Related Pages
- **Sources**: [[Types of Machine Learning Handbook]], [[Machine Learning and Deep Learning Cheat Sheets]]
- **Concepts**: [[Machine Learning Paradigms]], [[Unsupervised Learning and Dimensionality Reduction]], [[Model Evaluation and Validation]], [[Neural Networks and Deep Learning Foundations]]
