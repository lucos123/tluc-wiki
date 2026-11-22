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
