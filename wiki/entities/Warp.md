---
title: Warp
date: 2026-08-30
tags:
  - entity
  - tool
  - ai_company
  - developer-tools
---

# Warp

**Warp** is a modern, AI-powered terminal and agentic development environment designed to accelerate developer productivity through integrated AI workflows, intelligent subagents, and collaborative developer tooling.

---

## Overview & Corporate Facts

- **Founded**: 2020
- **Founders**: Zach Lloyd (CEO, former Google Principal Engineer)
- **Funding**: $73M+ raised
- **Core Technology Stack**: Rust (native client), Golang (backend services), GitHub Actions, **Oz** (internal agent orchestration engine), [[Anthropic]] Claude Platform.
- **Scale**: Over 800,000 monthly active developers; used by 56% of the Fortune 500; hosts >10M [[Claude Code]] sessions (400K+/week) and >40M total Warp Agent interactions.

---

## Key Products & Architectural Innovations

### 1. The Warp Terminal & Agentic IDE
Warp reimagines the terminal as a collaborative code editor and AI workspace with native block-based input, graphical shell outputs, and integrated AI agent commands.

### 2. Oz Agent Orchestration Platform
Oz is Warp's scheduled and event-driven orchestration system for executing autonomous background agents, scheduled observer loops, and repository maintenance workflows.

### 3. Dual-Skill Self-Improving Agent Framework
As documented in [[How Warp Builds Self-Improving Agents on Claude]], Warp pioneered an open-source framework for autonomous agent self-improvement:
- **Base Skills**: Domain-specific instruction files (`SKILL.md`) executing triage, code reviews, and spec generation.
- **Improver Skills**: Observer agents running on Oz that collect in-situ human feedback from PR comments, compute minimal skill adjustments, and open Git pull requests for maintainer review.

---

## Related Knowledge Nodes

- **Concepts**: [[Self-Improving Agents]], [[Agent Skills Architecture]], [[Loop Engineering]], [[Verification Loop]], [[Harness Engineering]].
- **Entities**: [[Anthropic]], [[Claude Code]], [[OpenAI]].
- **Sources**: [[How Warp Builds Self-Improving Agents on Claude]], [[5 Best Practices for Building AI Agent Skills]].
