---
title: "Path-Scoped Rules"
date: 2026-08-10
tags:
  - concept
  - context-engineering
  - harness-engineering
  - claude-code
source: "[[How Claude remembers your project]]"
---

# Path-Scoped Rules

**Path-Scoped Rules** are conditional instruction files stored in `.claude/rules/` that load into context *only when matching files are accessed* by the agent.

---

## Configuration & Glob Matching

Path-scoped rules use YAML frontmatter with glob patterns in the `paths` field:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "lib/**/*.{ts,tsx}"
---
# API Guidelines
- Require input validation for all endpoints
```

## Benefits for Context Engineering

1. **Context Window Optimization**: Unconditional rules bloat session startup context. Path-scoped rules load lazily, preserving context tokens.
2. **Modular Architecture**: Teams can organize rules by domain (`frontend/`, `backend/`, `security.md`) without cluttering main root instruction files.
3. **Symlink Support**: Rules in `.claude/rules/` support symlinks, allowing shared rule repositories to be linked across projects.

See [[How Claude remembers your project]] and [[Progressive Disclosure]].
