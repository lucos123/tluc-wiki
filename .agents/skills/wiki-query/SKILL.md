---
name: wiki-query
description: >
  Answer questions using the wiki knowledge base. Use when the user asks a
  question, requests an explanation, comparison, or analysis of topics covered
  in the wiki. Searches the index, reads relevant pages, synthesizes an answer
  with citations, and optionally compounds valuable answers back into the wiki.
---

# Wiki Query Skill

You are answering a question using a personal knowledge base (the "wiki"). Your
goal is to provide a well-cited, synthesized answer — not just regurgitate page
content. Follow every step below precisely.

## Step 1 — Understand the Question

Before searching, classify the question type:

| Type            | Examples                                      | Strategy               |
|-----------------|-----------------------------------------------|------------------------|
| **Factual**     | "What is Neuralese?"                          | Find the page, cite it |
| **Comparative** | "How do Claude Code and Codex handle skills?" | Find multiple pages, compare |
| **Analytical**  | "Why is harness engineering important?"       | Synthesize across pages |
| **Gap-finding** | "What don't we know about Agent-4?"           | Identify missing info   |
| **Exploratory** | "What topics relate to context engineering?"  | Map connections         |

This classification guides how deep you search and how you structure the answer.

## Step 2 — Search the Wiki

Follow this multi-layer search strategy. Each layer builds on the previous one:

### Layer 1: Index Scan
Read `index.md` to get a bird's-eye view of all available pages. Identify
pages whose titles or descriptions are directly relevant to the question.

### Layer 2: Targeted Page Reads
Read the pages identified in Layer 1. As you read, note:
- Direct answers to the question
- Cross-references (`[[wiki links]]`) that point to additional relevant pages
- Contradictions or nuances that need to be surfaced

### Layer 3: Deep Search (if needed)
If Layers 1-2 don't fully answer the question, use `grep_search` to find
keyword matches across all wiki pages. Search for:
- Key terms from the question
- Synonyms and related jargon
- Named entities mentioned in the question

### Layer 4: Raw Source Consultation (if needed)
If wiki pages reference a raw source and the question requires detail beyond
what the wiki page captured, read the original `raw/` file for deeper context.
Always prefer the wiki synthesis, but use raw sources to fill gaps.

> **Rule**: Never fabricate information. If the wiki doesn't contain the answer,
> say so explicitly. Do not hallucinate content that isn't in the knowledge base.

## Step 3 — Synthesize the Answer

Structure your answer based on the question type:

### For Factual Questions
- Provide a clear, direct answer
- Cite the wiki page: "According to [[Page Name]], ..."
- Include relevant details from the page

### For Comparative Questions
- Use a structured format (table or side-by-side bullets)
- Cite each page being compared
- Highlight similarities, differences, and unique aspects
- Note if the comparison is incomplete due to missing information

### For Analytical Questions
- Start with a thesis/conclusion
- Support with evidence from multiple wiki pages
- Weave a narrative that connects the sources
- Acknowledge gaps or areas of uncertainty

### For Gap-Finding Questions
- State what IS known (with citations)
- Explicitly list what is NOT covered
- Suggest sources to ingest that might fill the gaps

### For Exploratory Questions
- Map the connections between related pages
- Use a structured format showing the relationship graph
- Highlight unexpected connections or contradictions

## Citation Protocol

Always cite wiki pages when making claims. Use these formats:

| Situation                  | Citation Format                                   |
|----------------------------|---------------------------------------------------|
| Direct reference           | `According to [[Page Name]], ...`                 |
| Paraphrasing               | `... (see [[Page Name]])`                         |
| Multiple sources           | `... ([[Source A]], [[Source B]])`                 |
| Contradictory sources      | `[[Source A]] states X, while [[Source B]] argues Y` |
| Raw source for detail      | `The original source ([[raw/file.md]]) elaborates...` |

### Citation Quality Rules
- **Every factual claim** must have at least one citation
- **Never cite a page you haven't read** in this session
- **Prefer wiki pages** over raw sources (wiki pages are synthesized)
- **Flag stale citations** if you notice a page's `date:` field is very old

## Step 4 — Assess Compounding Value

After answering, evaluate whether the answer should be filed back into the wiki.

### Compound if the answer:
- Introduces a **new comparison** not currently captured (e.g., "Claude Code vs
  Codex skill systems")
- Reveals a **new insight or pattern** connecting multiple sources
- Fills a **documented gap** in the wiki
- Is a **synthesis** the user explicitly asked for and approved

### Do NOT compound if the answer:
- Simply restates what's already on a single page
- Is a trivial factual lookup
- Is speculative or based on information outside the wiki

### Compounding Procedure
If compounding is warranted:
1. **Propose** the new page to the user: suggest a title, location
   (`wiki/analyses/` or `wiki/concepts/`), and brief outline
2. **Wait for approval** before creating the page
3. If approved, create the page following the templates in the wiki-ingest
   skill's reference materials
4. Update `index.md` with the new entry
5. Update `wiki/log.md`

## Step 5 — Update `wiki/log.md`

Append exactly one line at the end of `wiki/log.md`:

```
## [YYYY-MM-DD] query | <Short description of the question>
```

Use today's date. The description should be a brief summary of what was asked
(not the full question).

## Step 6 — Identify Follow-Up Opportunities

End your answer with (if applicable):
- **Missing sources**: "The wiki doesn't cover X. Consider ingesting a source
  about it."
- **Stale information**: "[[Page Name]] was last updated on YYYY-MM-DD and may
  need refreshing."
- **Suggested investigations**: "An interesting follow-up question would be..."
- **Related pages**: "You might also be interested in [[Page Name]]."

Only include these if they are genuinely useful — don't pad the response.

## Answer Quality Checklist

Before delivering your answer, verify:

- [ ] Every factual claim is cited with `[[wiki links]]`
- [ ] The answer directly addresses the user's question
- [ ] Contradictions between sources are noted, not hidden
- [ ] Gaps in wiki coverage are explicitly acknowledged
- [ ] The answer synthesizes rather than copy-pastes page content
- [ ] Compounding opportunity is assessed and proposed if warranted
- [ ] `wiki/log.md` is updated
