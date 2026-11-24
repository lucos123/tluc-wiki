# Personal Memory Management Guide

This reference guide provides standardized schemas for managing personal identity, projects, goals, preferences, and people in `mem/`.

---

## 1. Active Project Page Schema (`mem/projects/`)

```markdown
---
title: "<Project Name>"
date: YYYY-MM-DD
tags:
  - project
  - <domain-tag>
status: active # active | completed | paused | planned
---

# <Project Name>

<1-2 sentence overview of the project, mission, and scope.>

## Objectives & Key Results (OKRs)

- [ ] Milestone 1
- [ ] Milestone 2

## Decision Log

- **YYYY-MM-DD**: <Key decision made, rationale, and consequences.>

## Related Wiki Concepts

- Cross-reference relevant technical pages: [Concept Name](../../wiki/concepts/Concept%20Name.md), [Entity Name](../../wiki/entities/Entity%20Name.md).
```

---

## 2. Career & Personal Goal Schema (`mem/goals/`)

```markdown
---
title: "<Goal Name>"
date: YYYY-MM-DD
tags:
  - goal
  - <career|technical|life>
status: active
target_date: YYYY-MM-DD
---

# <Goal Name>

<Goal description and target outcomes.>

## Target Milestones

1. **Phase 1**: ...
2. **Phase 2**: ...

## Knowledge Assets Required

- Cites wiki concepts: [Concept Name](../../wiki/concepts/Concept%20Name.md).
```

---

## 3. Person & Collaborator Schema (`mem/people/`)

```markdown
---
title: "<Person Name>"
date: YYYY-MM-DD
tags:
  - person
  - collaborator
role: "<Title / Role>"
organization: "<Organization / Company>"
---

# <Person Name>

<Role, background, and key topics of collaboration.>

## Projects & Interactions

- [Project Name](../projects/Project%20Name.md): Collaboration context.
```

---

## 4. User Preference Profile Schema (`mem/preferences/`)

```markdown
---
title: "<Preference Profile Title>"
date: YYYY-MM-DD
tags:
  - preference
  - memory
---

# <Preference Profile Title>

Standing working-style rules grounded in repeated session evidence.

## Standing Preferences

- **<Rule Lead>**: <Checkable rule statement.> (Evidence: <transcript path or dated user directive>)
```

- **Precedence**: `mem/preferences/` and `mem/gemini.md` layer underneath repository rules (`GEMINI.md`, `ctx/rules/*.md`); project rules win on conflict.
- **Secret Hygiene**: Never store API keys, tokens, passwords, or private credentials in `mem/`.

---

## 5. Memory Surface Routing, Evidence Extraction & Diff Confirmation Protocol

### Memory Surface Routing Table

| Signal Type | Destination | Routing Rule |
| :--- | :--- | :--- |
| Cross-session working style (repeated evidence) | `mem/gemini.md` or `mem/preferences/` | Cite explicit directive or repeated transcript pattern |
| Active project scope, OKRs, dated decisions | `mem/projects/` or `mem/goals/` | Cross-link related `wiki/` concepts and entities |
| Private collaborators & contacts | `mem/people/` | Private contacts only (public figures go in `wiki/entities/`) |
| Completed milestones & closed phases | `mem/history/` | Archival milestone record with completion date |
| Repo-wide AI conventions & enforcement rules | `ctx/rules/` or `.agents/skills/` | Route out of `mem/` |
| Objective technical concepts & benchmarks | `wiki/` | Route out of `mem/` |
| Transient single-turn scratch context | Do not persist in `mem/` | Keep ephemeral outside durable memory |

### Evidence-First Extraction

- Anchor every standing preference in `mem/preferences/` or `mem/gemini.md` to explicit user instructions or repeated session patterns (optionally indexed via [summarize_transcript.py](../../reflect/scripts/summarize_transcript.py)).
- Treat any signal seen only once as an **Unconfirmed Hypothesis** and ask the user instead of persisting it as a standing rule.

### Duplicate & Conflict Audit

- Read existing files in `mem/` before drafting edits.
- Flag overlapping, stale, or conflicting rules explicitly rather than silently appending contradictory lines.

### Mandatory Diff Confirmation Gate

- Present the proposed additions, modifications, removals, and unconfirmed hypotheses before writing to existing `mem/` files.
- Never silently overwrite existing memory files without explicit user sign-off.
