---
title: Memory Architecture
date: 2026-08-02
tags:
  - concept
  - agentic-design
  - harness-engineering
  - context-engineering
source: "raw/assets/2nd-brain.jpg"
---

# Memory Architecture

**Memory Architecture** is the reference framework for persistent context management that extends the LLM context window indefinitely by structuring and persisting information outside the model's context window.

Original reference notes provided in [[raw/assets/2nd-brain.jpg]].

## Key Principles

1. **Persistent Memory**: Context survives across sessions and model context limits.
2. **Separation of Concerns**: Strict boundary between raw inputs (`raw/`), evergreen knowledge (`wiki/`), shareable deliverables (`output/`), context primitives (`ctx/`), and identity/memory (`mem/`).
3. **Connected Knowledge**: Everything is cross-referenced using Obsidian wiki links.
4. **Personalization**: The system records user preferences, goals, and project state (`mem/gemini.md`).
5. **Compounding Value**: Every interaction adds to the knowledge base, compounding value over time.

## Operational Flow

$$\text{RAW (Ground Truth)} \longrightarrow \text{WIKI (Evergreen Knowledge)} \longrightarrow \text{OUTPUT / CTX} \longleftrightarrow \text{MEM (Identity)} \longrightarrow \text{RE-COMPOUND}$$

See `GEMINI.md`, [[Harness Engineering]], and [[Context Engineering]].
