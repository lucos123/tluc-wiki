---
title: "Data Preprocessing and Feature Engineering"
date: 2026-11-22
tags:
  - concept
  - machine-learning
  - data-engineering
  - python
source: "[[Machine Learning Basics Notes]]"
---

# Data Preprocessing and Feature Engineering

The upstream data preparation, feature construction, fit-diagnostic, and hyperparameter tuning workflow that transforms raw data into clean model signals (*"Better Data -> Better Model -> Better Decisions"*). Synthesized from [[Machine Learning Basics Notes]] (Pages 2, 7–9) and connected to [[Types of Machine Learning Handbook]].

---

## 1. Raw Data Taxonomies

Before selecting algorithms, ML pipelines classify raw inputs into three structural tiers:
- **Structured Data**: Fixed tabular schema (rows & columns in CSVs, relational databases).
- **Unstructured Data**: No fixed schema (free text, images, audio, video).
- **Semi-Structured Data**: Partially structured with schema tags/markers (`JSON`, `XML`).

---

## 2. Five-Step Data Preprocessing Pipeline

Raw datasets contain missing values, duplicates, incompatible scales, and non-numeric categories. Standard preprocessing executes five ordered transformations (`Clean Data = Better Model`):

1. **Missing Value Imputation**: Drop unusable rows/columns, fill with statistical estimators (**mean / median / mode**), or apply **KNN / interpolation** imputation.
2. **Deduplication**: Strip duplicate records that bias loss optimization and contaminate train/test splits.
3. **Feature Scaling (`Standardization` / `Min-Max`)**: Rescale numeric ranges so distance- and gradient-based models (`KNN`, `SVM`, `Linear/Logistic Regression`, neural networks) do not overweight high-magnitude columns:
   - **Standardization (Z-score)**: $z = \frac{x - \mu}{\sigma}$
   - **Min-Max Scaling**: $x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$
4. **Categorical Encoding**: Match encoding to category order:
   - **Label Encoding** for **ordinal** categories with meaningful order (e.g., `Low -> 0, Medium -> 1, High -> 2`).
   - **One-Hot Encoding** for **nominal** categories with no inherent order.
5. **Dataset Splitting (`Train / Validation / Test`)**: Partition clean data into isolated subsets (common splits `70/15/15` or `80/10/10`, plus K-Fold CV on small datasets)—fit on Train, tune hyperparameters on Validation, and reserve the **holdout Test set for one final evaluation** while strictly preventing **Data Leakage** *(never expose future/post-prediction info or target leakage into training/eval features)*.

![Data Preprocessing and Model Evaluation Overview](../../raw/screenshots/machine-learning-basics-notes/06.jpg)

---

## 3. Feature Engineering & Model Selection Pipeline

**Feature Engineering** constructs, selects, or transforms input variables to expose underlying domain structure to learning algorithms:
- **Feature Selection**: Prune redundant/noisy columns (`Filter`, `Wrapper RFE`, `Embedded Lasso/Tree` — see [[Unsupervised Learning and Dimensionality Reduction]]).
- **Feature Extraction**: Synthesize high-signal derived features from raw fields (e.g., computing *Age* from *Date of Birth*, or *Total Price* = *Quantity × Unit Price*).
- **Feature Transformation & Class Imbalance**: Non-linear transforms, scaling adjustments, and handling skewed label distributions via **resampling, class weights, and imbalance-aware metrics** (`Precision`, `Recall`, `F1` instead of raw Accuracy).

### Overfitting vs. Underfitting Diagnostics & Hyperparameters

| Fit Regime | Training Performance | Test Performance | Root Cause |
| :--- | :--- | :--- | :--- |
| **Underfitting (High Bias)** | Low (High error) | Low (High error) | Model too simple to capture data patterns |
| **Good Fit** | High (Low error) | High (Low error) | Captures generalizable signal without memorizing noise |
| **Overfitting (High Variance)** | **Very High (Low error)** | **Low (High error)** | Memorizes training noise/outliers; model overly complex |

**Seven-Stage Tuning Loop**: `Problem -> Data Prep -> Feature Engineering -> Model Selection -> Hyperparameter Tuning -> Validation (K-Fold CV) -> Final Model`. Key external hyperparameters governed before/during training include **`Learning rate`**, **`Number of trees`** (Random Forest), **`K`** (KNN/K-Means), **`Max depth`** (Decision Trees), **batch size / epochs**, and **regularization strength $\lambda$**.

![Feature Engineering, Overfitting Curves, Cross-Validation & Hyperparameters](../../raw/screenshots/machine-learning-basics-notes/07.jpg)

---

## 4. Foundational Python ML Library Stack

Practical implementation leverages six core Python packages (built on [[Python Core Syntax and Control Flow]] and [[Python Collections and File Handling]]):
- **Data Wrangling & Math**: **`NumPy`** (vectorized numerical arrays) & **`Pandas`** (tabular DataFrames & analysis).
- **Classical ML**: **`Scikit-learn`** (preprocessing transformers, classification, regression, clustering, cross-validation).
- **Deep Learning**: **`PyTorch`** (flexible research & neural training), **`TensorFlow`** (scalable neural networks), and **`Keras`** (high-level DL API).

---

## Related Pages
- **Sources**: [[Machine Learning Basics Notes]], [[Types of Machine Learning Handbook]], [[Machine Learning and Deep Learning Cheat Sheets]]
- **Entities**: [[Viet Nguyen AI]]
- **Concepts**: [[Model Evaluation and Validation]], [[Machine Learning Paradigms]], [[Supervised Learning Algorithms]], [[Unsupervised Learning and Dimensionality Reduction]], [[Neural Networks and Deep Learning Foundations]], [[Python Core Syntax and Control Flow]]
