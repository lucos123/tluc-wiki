# Wiki Page Templates

Reference templates for creating consistent wiki pages. These are the canonical
structures — follow them when creating new pages during ingestion.

---

## Source Page Template

Location: `wiki/sources/<Source Title>.md`

```markdown
---
title: <Source Title>
date: YYYY-MM-DD
tags:
  - source
  - <topic-tag-1>
  - <topic-tag-2>
source: "raw/<filename>"
---

# <Source Title>

**Source File**: [raw/<filename>](../../raw/<filename>)

<1-2 sentence overview of the source and its significance.>

## Key Concepts

- **<Concept Name>**: <Explanation with [Markdown links](../concepts/Concept%20Name.md) to related pages.>
- **<Feature/Pattern Name>**: <Description, citing specific details.>

## Synthesis Notes

<Analytical commentary connecting this source to the broader knowledge base.
Note confirmations, contradictions, or gaps.>
```

---

## Entity Page Template

Location: `wiki/entities/<Entity Name>.md`

Use for: Named tools, products, organizations, people, AI systems.

```markdown
---
title: <Entity Name>
date: YYYY-MM-DD
tags:
  - entity
  - <type: tool|person|organization|product|ai-system>
  - <topic-tag>
---

# <Entity Name>

<1-2 sentence identification of the entity.>

## <Primary Section>
<Core details, features, or attributes. Use bullet lists for multiple items.
Link to related concepts and sources using [Markdown links](../concepts/Concept%20Name.md).>

## <Additional Section>
<Further details as needed. Keep sections focused on a single aspect.>

See [Related Source Page](../sources/Related%20Source%20Page.md) for detailed analysis.
```

---

## Concept Page Template

Location: `wiki/concepts/<Concept Name>.md`

Use for: Ideas, patterns, methodologies, frameworks, paradigms.

```markdown
---
title: <Concept Name>
date: YYYY-MM-DD
tags:
  - concept
  - <domain-tag>
---

# <Concept Name>

<1-2 sentence definition, citing the primary source: [Source Title](../sources/Source%20Title.md).>

## Definition
<Expanded explanation of the concept.>

## <Subtopic Section>
<Details, examples, or categorizations within the concept.>

## Relationship to <Other Concept>
<How this concept connects to other ideas in the knowledge base.
Use [Markdown links](Other%20Concept.md) extensively.>
```

---

## Analysis Page Template

Location: `wiki/analyses/<Analysis Title>.md`

Use for: Comparisons, cross-source synthesis, trend analysis.

```markdown
---
title: <Analysis Title>
date: YYYY-MM-DD
tags:
  - analysis
  - <topic-tag-1>
  - <topic-tag-2>
---

# <Analysis Title>

<Brief statement of the analysis question or comparison being made.>

## Background
<Context and motivation for this analysis.>

## Findings
<Structured findings. Use tables for comparisons, bullet lists for themes.>

## Conclusions
<What the analysis reveals. Note confidence levels and remaining gaps.>

## Sources
<List of wiki pages and raw sources used in this analysis.>
```

---

## Formatting Conventions

| Element             | Convention                                                |
|---------------------|-----------------------------------------------------------|
| Internal links      | `[Page Name](../concepts/Page%20Name.md)` or `[Display Text](../concepts/Page%20Name.md)` |
| Related Pages       | Nested sub-bullets for `>= 3` links under a category (`- **Concepts**:\n  - [Link](...)`) |
| Tags                | `kebab-case` for multi-word (e.g., `agentic-design`)     |
| Dates               | `YYYY-MM-DD` format (e.g., `2026-07-06`)                 |
| Headings            | `# Title`, `## Section`, `### Subsection`                 |
| Bold concepts       | `**Concept Name**:` at start of bullet point              |
| Contradictions      | Use `> ⚠️ **Evolving claim**: ...` blockquote             |
| Source attribution   | `**Source File**: [raw/<filename>](../../raw/<filename>)` after title heading |
