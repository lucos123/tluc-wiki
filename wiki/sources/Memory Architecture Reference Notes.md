---
title: "Memory Architecture Reference Notes"
date: 2026-08-02
tags:
  - source
  - harness-engineering
  - context-engineering
source: "raw/assets/2nd-brain.jpg"
---

# Memory Architecture Reference Notes

**Source File**: [raw/assets/2nd-brain.jpg](../../raw/assets/2nd-brain.jpg)

Reference architecture diagram (Version 1.0, 2025-05-12) defining persistent context management, a 5-tier directory structure (`raw/`, `wiki/`, `output/`, `ctx/`, `mem/`), and a knowledge compounding feedback loop.

## Key Concepts

- **Core Goal**: Extends the model context window indefinitely by persisting and structuring information outside the model.
- **5-Tier Separation**:
  - `raw/`: Immutable ground truth inputs (articles, pdfs, screenshots, transcripts, notes).
  - `wiki/`: Evergreen structured knowledge (concepts, entities, topics, sources, analyses, references).
  - `output/`: Shareable, versioned deliverables (reports, documents, summaries, posts, visuals).
  - `ctx/`: Context primitives (prompts, templates, rules, snippets).
  - `mem/`: Identity and personal memory (`gemini.md`, preferences, goals, projects, people, history).
- **Knowledge Compounding Feedback Loop**:
  $$\text{Source} \longrightarrow \text{Knowledge} \longrightarrow \text{Context} \longrightarrow \text{Output} \longrightarrow \text{Memory} \longrightarrow \text{Source/Knowledge}$$

See [Memory Architecture](../concepts/Memory%20Architecture.md), `GEMINI.md`, [Harness Engineering](../concepts/Harness%20Engineering.md), and [Context Engineering](../concepts/Context%20Engineering.md).
