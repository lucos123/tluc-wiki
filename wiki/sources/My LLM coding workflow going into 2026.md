---
title: "Summary: My LLM coding workflow going into 2026"
date: 2026-06-28
tags:
  - workflow
  - best-practices
source: "[[raw/My LLM coding workflow going into 2026.md]]"
---

# My LLM coding workflow going into 2026

## Summary
[[Addy Osmani]] outlines a disciplined "AI-assisted engineering" approach for 2026. He emphasizes that while AI coding assistants are powerful, they require clear direction, context, and oversight. The developer remains the accountable director, avoiding the pitfalls of unstructured prompt-and-pray coding.

## Key Workflow Steps
1. **Plan first (Specs before code)**: Brainstorm a detailed specification (`spec.md`) and project plan with the AI before writing code.
2. **Break work into small chunks**: Avoid monolithic requests. Tackle features step-by-step or ticket-by-ticket to prevent the code from becoming a jumbled mess.
3. **Provide extensive context**: Feed the AI all necessary code, docs, and constraints. Use tools like `gitingest` or Claude Skills for context packing.
4. **Choose the right model**: Swap between models (e.g., Claude, Gemini) when one gets stuck. 
5. **Leverage AI across the SDLC**: Use CLI tools (Claude Code, Gemini CLI) and asynchronous agents (Jules, Copilot Agent) for repetitive tasks. 
6. **Human in the loop**: Verify, test, and review everything. Treat AI like an over-confident junior developer. 
7. **Commit often**: Use granular version control as a safety net to undo AI missteps and document the process. Worktrees and branches isolate parallel AI experiments.
8. **Customize AI behavior**: Use `CLAUDE.md` or system prompts to align the AI with project style and rules.
9. **Embrace automation**: CI/CD, linters, and review bots catch mistakes automatically, allowing the AI to learn and fix them.

## Associated Entities & Concepts
- [[Addy Osmani]]
- [[Vibe Coding vs Agentic Engineering]]: This workflow strongly advocates for structured Agentic Engineering over naive Vibe Coding.
- [[Conductor vs Orchestrator]]: Mentions orchestration tools like "Conductor" for running multiple agents asynchronously.
