# Source Ingest Document Templates

This reference guide provides standardized frontmatter, body templates, and raw file naming guidelines for ingesting different source types into `wiki/sources/`.

---

## 0. Raw File Naming Standard (Kebab-Case)

All raw files in `raw/` must be renamed to lower-case kebab-case filenames upon ingestion:
- **Articles**: `raw/articles/<category>/<clean-kebab-case-title>.<ext>`
- **PDFs**: `raw/pdfs/<clean-kebab-case-title>.pdf`
- **Video Transcripts**: `raw/video-transcripts/<clean-kebab-case-title>.md`
- **Notes**: `raw/notes/<category>/<clean-kebab-case-title>.<ext>`
- **Visual Assets**: `raw/assets/<descriptive-kebab-case-name>.<ext>`
- **Social Screenshots / Slide Decks**: `raw/screenshots/<clean-kebab-case-slug>/00.<ext>` (00-indexed for cover + numbered pages, or `raw/assets/<slug>-01.<ext>` for 1–3 standalone diagrams)

Always strip trailing browser artifacts (`  Claude`, `  OpenAI API`, ` copy`, ` copy 2`), special characters, and convert spaces to hyphens. Update the `source:` frontmatter link in `wiki/sources/` accordingly.

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
source: "raw/articles/<category>/<filename>"
---

# <Article Title>

**Source File**: [raw/articles/<category>/<filename>](../../raw/articles/<category>/<filename>)

<1-2 sentence overview summarizing what this article covers and why it is significant.>

## Key Concepts

- **<Concept Name>**: <Concise explanation with [Markdown links](../concepts/Concept%20Name.md) to related concept/entity pages.>
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
source: "raw/pdfs/<filename>"
---

# <Book or Paper Title>

**Source File**: [raw/pdfs/<filename>](../../raw/pdfs/<filename>)

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
source: "raw/notes/<category>/<filename>"
---

# <Note Title>

**Source File**: [raw/notes/<category>/<filename>](../../raw/notes/<category>/<filename>)

<Context of user notes, meeting takeaways, or training material.>

## Key Insights & Action Items

- **<Key Takeaway>**: <Description>

## Integration with Personal Memory

<Cross-references to [Project Name](../../mem/projects/Project%20Name.md) or [Goal Name](../../mem/goals/Goal%20Name.md) if applicable.>
```

---

## 4. Social Post & Visual Guide Deck Template (`raw/articles/` + `raw/screenshots/`)

### A. Raw Markdown Post (`raw/articles/<category>/<slug>.md`)

```markdown
---
title: "<Post Title>"
source: "<Post URL>"
original_source: "<Optional English/upstream source URL if cited>"
author:
  - "<Author Entity Name>"
published: YYYY-MM-DD
created: YYYY-MM-DD
description: "<1-2 sentence summary of the post and attached visual slides>"
tags:
  - "clippings"
  - "<topic-tag>"
  - "visual-guide"
---

# <Post Title>

- **Source URL:** <Post URL>
- **Published:** YYYY-MM-DD
- **Visual Assets Folder:** `raw/screenshots/<slug>/`

## Verbatim Post Content

> <Complete verbatim text from social post>

## Visual Slide Transcriptions

### Page 00 — <Cover / Slide Title>
![Page 00](../../screenshots/<slug>/00.jpg)

<Detailed transcription of diagrams, tables, formulas, and key points.>
```

### B. Wiki Source Page (`wiki/sources/<Source Title>.md`)

```markdown
---
title: "<Source Title>"
date: YYYY-MM-DD
tags:
  - source
  - <topic-tag>
  - visual-guide
source: "raw/articles/<category>/<slug>.md"
source_type: visual-notes
---

# <Source Title>

**Source Files**:
- [raw/articles/<category>/<slug>.md](../../raw/articles/<category>/<slug>.md) *(Original post & visual transcriptions)*
- [raw/screenshots/<slug>/00.jpg](../../raw/screenshots/<slug>/00.jpg) *(Page 00 description)*
- [raw/screenshots/<slug>/01.jpg](../../raw/screenshots/<slug>/01.jpg) *(Page 01 description)*

<1-2 sentence overview summarizing the visual handbook and its significance.>

## Synthesized Knowledge Blocks

- **<Block / Slide Theme>**: <Analytical synthesis with [Markdown links](../concepts/Concept%20Name.md) to concepts/entities.>

## Synthesis Notes

<Cross-source connections, trade-offs, and updates relative to existing wiki pages.>

## Related Pages

- **Entities**: [Author Entity](../entities/Author%20Entity.md)
- **Concepts**:
  - [Concept 1](../concepts/Concept%201.md)
  - [Concept 2](../concepts/Concept%202.md)
  - [Concept 3](../concepts/Concept%203.md)
- **Sources**: [Related Source](Related%20Source.md)
```
