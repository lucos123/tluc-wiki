---
title: "Machine Learning Paradigms"
date: 2026-11-16
tags:
  - concept
  - machine-learning
  - llm-foundations
source: "[[Types of Machine Learning Handbook]]"
---

# Machine Learning Paradigms

**Machine Learning (ML)** enables computers to learn patterns from data and improve performance through **data, mathematical algorithms, and experience** without explicit rule-based programming for every task. As categorized in [[Types of Machine Learning Handbook]], ML spans five foundational learning paradigms alongside specialized training regimes.

---

## Core Learning Taxonomy

| Paradigm | Supervision Signal | Primary Goal | Representative Algorithms & Examples |
| :--- | :--- | :--- | :--- |
| **Supervised Learning** | Labeled `(input, output)` pairs | Map inputs to discrete labels or continuous numbers | [[Supervised Learning Algorithms]] (Spam detection, price prediction) |
| **Unsupervised Learning** | Unlabeled data only | Discover latent structures, clusters, or compressed projections | [[Unsupervised Learning and Dimensionality Reduction]] (Customer segmentation, anomaly detection) |
| **Semi-Supervised Learning** | Small labeled subset + large unlabeled pool | Improve generalization when labeling is expensive | Self-Training, Co-Training, Graph-based methods (Medical diagnostics, web/social analysis) |
| **Self-Supervised Learning** | Pseudo-labels auto-generated via **pretext tasks** | Learn reusable general-purpose **representations** (embeddings) | Masked LM (BERT), Next-Token Prediction (GPT), Contrastive Learning (CLIP), MAE, VideoGPT |
| **Reinforcement Learning (RL)** | Environment `State (s)` & scalar `Reward (r)` | Learn an optimal policy $\pi(a\|s)$ maximizing cumulative discounted reward | Q-Learning, DQN, Policy Gradient, Actor-Critic, PPO (Games, robotics, autonomous vehicles) |

---

## Deep Dive: Self-Supervised & Reinforcement Paradigms

### Self-Supervised Learning (Foundation of Modern LLMs)
- **Pipeline:** `Unlabeled Data (Text/Image/Video) → Pretext Task → Auto Pseudo-Labels → Train Representation → Downstream Tasks (Classification, Retrieval, Generation)`.
- **Why it dominates modern AI:** Eliminates manual annotation bottlenecks while scaling pretraining across web-scale corpora—powering transformer language models alongside [[Tokenization]].

### Reinforcement Learning (Sequential Decision Loop)
- **Objective Function:** Maximize expected cumulative discounted return:
  $$R = \sum_{t=0}^{\infty} \gamma^t r_t \quad (0 \le \gamma \le 1)$$
- **Core Tension:** Balancing **exploration** (trying unvisited actions) against **exploitation** (repeating highest-reward known actions)—structurally analogous to agent decision loops in [[Agent Loop Lifecycle]] and [[Control-Loop Engineering]].

---

## Adjacent & Specialized Paradigms

- **Online Learning:** Continuous incremental updates as streaming data arrives.
- **Transfer Learning:** Reusing representations learned on a source domain for a related target task.
- **Multi-Task Learning:** Joint optimization across multiple tasks simultaneously.
- **Few-Shot Learning:** Adapting from very few labeled demonstrations (conceptual precursor to in-context [[Few-Shot Prompting]]).
- **Active Learning:** Selectively querying human annotators for the highest-uncertainty examples.

---

## Related Pages
- **Sources**: [[Types of Machine Learning Handbook]], [[Prompt Engineering Handbook]]
- **Concepts**: [[Supervised Learning Algorithms]], [[Unsupervised Learning and Dimensionality Reduction]], [[Model Evaluation and Validation]], [[Few-Shot Prompting]], [[Agent Loop Lifecycle]]
