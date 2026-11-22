# Compounding Rules & Schema Guide

This guide outlines when and how synthesized answers should be compounded back into `wiki/analyses/` or `output/reports/`.

---

## 1. When to Compound

Compound an answer if:
1. It introduces a **new multi-source comparison** (e.g. `GPT-5.6 vs Kimi K3`).
2. It synthesizes a **new architectural pattern** or trade-off evaluation connecting multiple concepts.
3. The user explicitly asks to "file this answer back to the wiki" or generate a report deliverable.

Do NOT compound if:
1. The query is a simple factual lookup on a single page.
2. The information is speculative or not grounded in source files.

---

## 2. Compounding Target Locations

- **`wiki/analyses/<Title>.md`**: For cross-source technical evaluations, comparisons, and architecture syntheses.
- **`output/reports/<Title>.md`**: For formal deliverables requested by the user.

---

## 3. Page Schema for `wiki/analyses/`

```markdown
---
title: "<Analysis Title>"
date: YYYY-MM-DD
tags:
  - analysis
  - concept
  - <topic-tag>
---

# <Analysis Title>

<Executive Summary>

## Comparison & Evaluation

| Dimension | Subject A | Subject B |
|-----------|-----------|-----------|
| ...       | ...       | ...       |

## Deep Synthesis

<Detailed text citing [Entity A](../entities/Entity%20A.md) and [Entity B](../entities/Entity%20B.md).>

See [index.md](../../index.md).
```
