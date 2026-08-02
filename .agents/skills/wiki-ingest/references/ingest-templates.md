# Source Ingest Document Templates

This reference guide provides standardized frontmatter and body templates for ingesting different source types into `wiki/sources/`.

---

## 1. Web Article & Documentation Template (`raw/articles/`)

```markdown
---
title: "<Article Title>"
date: YYYY-MM-DD
tags:
  - source
  - <topic-tag-1>
  - <topic-tag-2>
source: "[[raw/articles/<category>/<filename>]]"
---

# <Article Title>

**Source File**: [[raw/articles/<category>/<filename>]]

<1-2 sentence overview summarizing what this article covers and why it is significant.>

## Key Concepts

- **<Concept Name>**: <Concise explanation with [[wiki links]] to related concept/entity pages.>
- **<Feature/Architecture>**: <Analytical breakdown with key specifications.>

## Synthesis Notes

<Analytical commentary connecting this source to broader AI engineering frameworks, trade-offs, or contradictions with existing wiki content.>
```

---

## 2. Book & PDF Whitepaper Template (`raw/pdfs/`)

```markdown
---
title: "<Book or Paper Title>"
date: YYYY-MM-DD
tags:
  - source
  - pdf
  - <topic-tag>
source: "[[raw/pdfs/<filename>]]"
---

# <Book or Paper Title>

**Source File**: [[raw/pdfs/<filename>]]

<Executive summary of the whitepaper/book, main thesis, and scope.>

## Core Architecture & Frameworks

- **<Section/Chapter Theme>**: <Key takeaways and formulas/specifications.>

## Practical Applications & Trade-offs

<How this whitepaper applies to production agent systems or LLMOps.>
```

---

## 3. Work Notes & Drafts Template (`raw/notes/`)

```markdown
---
title: "<Note Title>"
date: YYYY-MM-DD
tags:
  - source
  - notes
  - <topic-tag>
source: "[[raw/notes/<category>/<filename>]]"
---

# <Note Title>

**Source File**: [[raw/notes/<category>/<filename>]]

<Context of user notes, meeting takeaways, or training material.>

## Key Insights & Action Items

- **<Key Takeaway>**: <Description>

## Integration with Personal Memory

<Cross-references to [[mem/projects/]] or [[mem/goals/]] if applicable.>
```
