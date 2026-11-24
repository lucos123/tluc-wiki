---
title: "tluc-wiki 2nd Brain Architecture"
date: 2026-11-24
tags:
  - project
  - memory
status: active
---

# tluc-wiki 2nd Brain Architecture

Active engineering project upgrading `tluc-wiki` into a 5-tier persistent context Second Brain system (`raw/`, `wiki/`, `output/`, `ctx/`, `mem/`) with 15 Agent Skills, 4 operational rule files in `ctx/rules/`, and a 94-test deterministic verification suite (`run_all_tests.py`).

## Key Decisions

- **2026-08-02**: Adopted `2nd-brain.jpg` reference architecture.
- **2026-08-02**: Standardized 5 Agent Skills (`wiki-ingest`, `wiki-write`, `wiki-manage`, `wiki-query`, `wiki-lint`).
- **2026-08-02**: Added unit test suite `run_all_tests.py` with 13 unit tests.
- **2026-11-05**: Added domain operational skill `dental-consult-ops` for Nha Khoa 3C TVV workflows, SOPs, and KPI governance.
- **2026-11-15 to 2026-11-22**: Upgraded `wiki-ingest` through v4.2 (multi-domain JS harvesters A–E, Zero-URL-Relay `--from-harvest-file`, SHA-256 duplicate guards, chapter-clamped YouTube smart-probe keyframes, and atomic `register_ingest.py`).
- **2026-11-22**: Migrated the entire vault (`index.md`, `wiki/`, `mem/`) from legacy wikilinks to Standard Relative Markdown Links (`quote(rel_path, safe="/-._~")`) and nested `Related Pages` sub-bullets with 0 broken links.
- **2026-11-24**: Ported 7 Group A workflow skills (`technical-writing`, `diagram`, `reflect`, `deep-research`, `sharpen`, `bro`, `ketchup`), completed Group B governance & verification hardening (`ctx/rules/agent-doc-and-correction-rules.md`, `lint_skills.py`, `check_memory.py`, `unvetted-benchmark-claim` in `check_research.py`, and critical ingest of 24 `pstack`/OMC principles), and expanded `run_all_tests.py` to 94 passing unit tests.
- **2026-11-24**: Codified proactive session-based verification (`lint_wiki.py`, `lint_skills.py --strict`, `check_memory.py --strict`, `run_all_tests.py`) and explicitly declined Git `pre-commit` hook enforcement to keep manual commits unblocked.

## Related Pages

- **Concepts**:
  - [Memory Architecture](../../wiki/concepts/Memory%20Architecture.md)
  - [Harness Engineering](../../wiki/concepts/Harness%20Engineering.md)
  - [Context Engineering](../../wiki/concepts/Context%20Engineering.md)
  - [Agentic Engineering Principles](../../wiki/concepts/Agentic%20Engineering%20Principles.md)
  - [Poteto Trust Pyramid](../../wiki/concepts/Poteto%20Trust%20Pyramid.md)
  - [Verification Loop](../../wiki/concepts/Verification%20Loop.md)
  - [Self-Improving Agents](../../wiki/concepts/Self-Improving%20Agents.md)
- **History & Goals**:
  - [2026-Q3 Milestones](../history/2026-Q3-Milestones.md)
  - [2026-Q4 Milestones](../history/2026-Q4-Milestones.md)
  - [AI Engineering Mastery 2026](../goals/AI%20Engineering%20Mastery%202026.md)
