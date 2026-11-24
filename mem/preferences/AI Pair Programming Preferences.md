---
title: "AI Pair Programming Preferences"
date: 2026-11-24
tags:
  - preference
  - memory
---

# AI Pair Programming Preferences

Operating preferences for pair programming with Gemini AI in `tluc-wiki`.

## Core Guidelines

- **Analytical Depth**: Provide thorough, structured breakdowns with clear section headings, comparison tables, and Standard Relative Markdown Links.
- **Language**: Interaction in Vietnamese; technical terms and schemas in English.
- **Verification Gate (Session-Based, No Git `pre-commit` Hooks)**: Run deterministic session verification after major edits (`lint_wiki.py`, `lint_skills.py --strict`, `check_memory.py --strict`, and `python -W error .agents/skills/run_all_tests.py`) to guarantee 0 broken links and 0 schema/test regressions; do not install Git `pre-commit` hooks so commits remain manual and unblocked (Evidence: explicit user directive 2026-11-24).
- **Continuous Skill Improvement Reflection**: After completing each source ingest (or multi-step workflow), surface actionable observations and upgrade proposals across `SKILL.md`, helper scripts, and tests in a dedicated final section for explicit user approval before modifying skills (aligns with the human-gated pattern in [Self-Improving Agents](../../wiki/concepts/Self-Improving%20Agents.md) and CLI evolution in [Home Repo Pattern](../../wiki/concepts/Home%20Repo%20Pattern.md)).
