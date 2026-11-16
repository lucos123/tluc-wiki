---
title: "Unsupervised Learning and Dimensionality Reduction"
date: 2026-11-16
tags:
  - concept
  - machine-learning
  - llm-foundations
source: "[[Types of Machine Learning Handbook]]"
---

# Unsupervised Learning and Dimensionality Reduction

**Unsupervised Learning** discovers hidden patterns, groupings, and compact structure in unlabeled data without predefined target labels—spanning **Clustering**, **Association Rules**, and **Dimensionality Reduction**. See [[Types of Machine Learning Handbook]].

---

## 1. Clustering Algorithms

| Algorithm | Grouping Mechanism | Cluster Shape & Key Trade-off |
| :--- | :--- | :--- |
| **K-Means Clustering** | Minimizes within-cluster sum-of-squares (inertia) around $K$ centroids | Fast on spherical clusters; requires choosing $K$ upfront; sensitive to initialization and outliers |
| **Hierarchical Clustering** | Builds nested **dendrogram** trees via agglomerative (bottom-up) or divisive (top-down) merging | No preset $K$ needed; exposes hierarchy; high compute cost on large datasets |
| **DBSCAN** | Groups points in dense neighborhoods (`Density-Based Spatial Clustering of Applications with Noise`) | Discovers arbitrary shapes and isolates noise/outliers automatically without $K$ |
| **Gaussian Mixture Models (GMM)** | Models data as a mixture of Gaussian distributions via Expectation-Maximization (EM) | Provides **soft clustering** (class probabilities) and captures elliptical clusters |

### Association Rule Mining
- **Apriori & Eclat:** Discover co-occurrence rules across transactional items (e.g., Market Basket Analysis: buying *Bread* predicts buying *Milk*).

---

## 2. Dimensionality Reduction & Feature Selection

Dimensionality reduction compresses high-dimensional features into low-dimensional representations while retaining essential signal—combating the **curse of dimensionality**, removing noise, cutting compute/storage costs, and reducing overfitting.

| Technique | Supervision | Core Behavior & Primary Use |
| :--- | :---: | :--- |
| **PCA (Principal Component Analysis)** | Unsupervised | Linearly projects data onto orthogonal principal components maximizing captured variance; general-purpose compression & visualization |
| **LDA (Linear Discriminant Analysis)** | Supervised | Uses class labels to project onto axes maximizing inter-class separability |
| **t-SNE** | Unsupervised | Non-linear embedding preserving local neighborhood structure for 2D/3D visualization (not suited as general downstream feature extractor) |
| **UMAP** | Unsupervised | Manifold projection preserving both local and broader structural relationships |
| **Feature Selection** | Mixed | Retains original features without transformation via **Filter** (variance threshold, correlation, mutual info), **Wrapper** (RFE), or **Embedded** (Lasso L1, tree feature importance) |

---

## Related Pages
- **Sources**: [[Types of Machine Learning Handbook]]
- **Concepts**: [[Machine Learning Paradigms]], [[Supervised Learning Algorithms]], [[Model Evaluation and Validation]]
