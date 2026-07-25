---
title: Vibe Coding vs Agentic Engineering
date: 2026-06-28
tags:
  - concept
  - ai_sdlc
  - engineering_practice
---

# Vibe Coding vs. Agentic Engineering

A spectrum of AI-assisted development paradigms introduced in [[The New SDLC With Vibe Coding]].

## Vibe Coding
- **Definition**: Casual natural language prompting where the developer accepts the AI's output and fixes errors by pasting tracebacks back into the prompt.
- **Characteristics**: Fast, unstructured, relies entirely on the model's baseline capabilities.
- **Risk**: High operational expenditure (OpEx) due to token burn, maintenance debt, and security vulnerabilities ("spaghetti code"). Best for prototypes and scripts.

## Agentic Engineering
- **Definition**: Structured, disciplined AI implementation governed by formal specs, deterministic tests, and feedback loops.
- **Characteristics**: High upfront capital expenditure (CapEx) to build the scaffolding, but low OpEx for maintenance and execution.
- **Requirements**: Requires evaluating trajectories and outputs, setting up CI/CD gates, and establishing firm architectural guardrails. Best for production systems.
- **Implementation**: Also referred to as "AI-assisted engineering" by [[Addy Osmani]], who stresses that relying on LLMs requires strict planning (specs before code), iterative chunking, extensive context packing, and continuous testing to avoid a "jumbled mess" of code (see [[My LLM coding workflow going into 2026]]).
