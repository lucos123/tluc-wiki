---
name: wiki-ingest
description: >
  Ingest a new source document into the wiki knowledge base. Use when the user
  asks to add, process, ingest, import, or summarize a new raw source document
  (article, paper, notes, transcript, or video URL) into the wiki. Handles
  reading the source, creating wiki pages, updating the index, and maintaining
  the operation log. Supports automatic YouTube transcript extraction via a
  bundled script — no browser interaction needed.
---

# Wiki Ingest Skill

You are operating a personal knowledge base (the "wiki"). Your job is to read a
raw source document and distill it into structured, cross-referenced wiki pages.
Follow every step below precisely.

## Pre-Flight Checks

Before doing any writing, complete these checks:

1. **Locate the source file.** The user will reference a file in `raw/` or
   provide content directly. Confirm the file exists and is readable.
2. **Check for prior ingestion.** Read `wiki/log.md` and search for the source title.
   If it has already been ingested, inform the user and ask whether to
   re-ingest (update) or skip.
3. **Read `index.md`** to understand what pages already exist and how they are
   organized. This prevents duplicate page creation.

## Source Type Detection

Before reading the source, identify its type and follow the matching protocol:

| Source Type | Indicator | Protocol |
|-------------|-----------|----------|
| **File** | Path to `.md`, `.pdf`, `.docx`, `.txt` in `raw/` | Proceed directly to Step 1 |
| **Article URL** | HTTP/HTTPS link to a blog post, paper, or doc page | Fetch the page content (use browser or `read_url_content`), save to `raw/`, then Step 1 |
| **Video URL** | YouTube, Vimeo, or other video platform link | Run **Video Extraction Protocol** below |

### Video Extraction Protocol

This replaces manual browser-based transcript extraction. It is faster, token-free,
and produces a clean, structured file.

**Step V1 — Run the extraction script:**
```powershell
python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py <VIDEO_URL>
```

The script will:
- Auto-install `yt-dlp` if not present
- Fetch video metadata (title, channel, duration, upload date)
- Download and clean the transcript (manual captions preferred, auto-captions as fallback)
- Save a `.md` file to `raw/video-transcripts/` with full YAML frontmatter
- **Print the saved file path to stdout**

**Step V2 — Note the output path** (printed to stdout by the script).

**Step V3 — Proceed to Step 1** using the saved `.md` file as your source.

**If the script fails** (no captions available, geo-blocked, private video):
Read `references/video-ingest-guide.md` for manual fallback options and the
video-specific source page template.

> **Token efficiency**: The extraction script does all the heavy lifting outside
> the LLM context. The model only reads the final clean transcript, not the raw
> VTT/SRT format with timestamps.

## Step 1 — Read & Analyze the Source

Read the entire source document carefully. As you read, identify and mentally
categorize:

| Category       | What to look for                                       |
|----------------|--------------------------------------------------------|
| **Entities**   | Named tools, products, organizations, people           |
| **Concepts**   | Ideas, patterns, methodologies, frameworks             |
| **Claims**     | Factual statements, predictions, statistics            |
| **Connections**| References to topics already covered in the wiki       |

> **Important**: Do NOT skim. For long documents (>200 lines), read in chunks
> but ensure full coverage. The quality of the wiki page depends on thorough
> reading.

## Step 2 — Discuss with the User (If Requested)

If the user asks for discussion before writing, provide:
- A 3–5 bullet summary of key takeaways
- Notable new entities or concepts not yet in the wiki
- Contradictions or tensions with existing wiki content
- Your proposed page creation/update plan

Wait for user feedback before proceeding to Step 3.

If the user did NOT request discussion, proceed directly to Step 3.

## Step 3 — Create the Source Summary Page

Create a new page at `wiki/sources/<Source Title>.md`. Follow this structure
exactly:

```markdown
---
title: <Source Title>
date: <YYYY-MM-DD of today>
tags:
  - source
  - <topic-tag-1>
  - <topic-tag-2>
source: "[[raw/<filename>]]"
---

# <Source Title>

**Source File**: [[raw/<filename>]]

<1-2 sentence overview: what this source is and why it matters.>

## Key Concepts

- **<Concept/Feature Name>**: <Concise explanation with [[wiki links]] to
  related pages where they exist.>
- ...repeat for each major point...

## Synthesis Notes
<Your analytical commentary. What does this source add to the overall knowledge
base? How does it connect to, support, or contradict existing pages? Note any
tensions or evolving claims.>
```

> **For Video Sources**: Use the extended template in
> `references/video-ingest-guide.md` which includes `source_type`, `url`,
> `channel`, `speaker`, and `duration` fields in the frontmatter.

### Source Page Quality Rules

- **Tags**: Always include `source` as the first tag. Add 2-4 topic tags using
  `kebab-case` (e.g., `agentic-design`, `ai_sdlc`). Reuse existing tags from
  the wiki when possible — check other source pages for consistency.
- **Key Concepts**: Aim for 4-8 bullet points. Each should be a self-contained
  insight, not a sentence fragment. Use `**bold**` for the concept name.
- **Wiki Links**: Aggressively link to existing pages using `[[Page Name]]`
  syntax. If a concept SHOULD exist as its own page but doesn't yet, still
  create the link — you'll create the page in the next step.
- **Synthesis Notes**: This is the most valuable section. Don't just summarize —
  analyze. Connect this source to the broader knowledge graph. Note if it
  confirms, extends, or contradicts existing wiki content.

## Step 4 — Update Entity & Concept Pages

For each entity or concept identified in Step 1:

### Decision: Create New Page or Update Existing?

- **Create a new page** if:
  - The entity/concept does NOT already exist in the wiki
  - AND it is mentioned substantively (not just in passing)
  - AND it is likely to be referenced by future sources

- **Update an existing page** if:
  - The entity/concept already has a wiki page
  - AND the new source adds meaningful information (a new fact, feature,
    relationship, or perspective)

- **Skip** if:
  - The entity/concept is only mentioned in passing with no new information
  - OR it is too granular to warrant its own page (e.g., a single CLI flag)

### Creating a New Entity Page (`wiki/entities/`)

```markdown
---
title: <Entity Name>
date: <YYYY-MM-DD>
tags:
  - entity
  - <type: tool|person|organization|product>
  - <topic-tag>
---

# <Entity Name>

<1-2 sentence definition/description.>

## <Relevant Section Heading>
<Details organized by topic. Use [[wiki links]] liberally.>
```

### Creating a New Concept Page (`wiki/concepts/`)

```markdown
---
title: <Concept Name>
date: <YYYY-MM-DD>
tags:
  - concept
  - <domain-tag>
---

# <Concept Name>

<1-2 sentence definition, citing the source where it was introduced:
[[Source Title]].>

## Definition
<Expanded explanation.>

## <Additional Sections as Needed>
<Examples, implementations, relationships to other concepts.>
```

### Updating an Existing Page

When adding information to an existing page:
1. Add new content under the most appropriate existing section heading, or
   create a new section if no existing section fits.
2. Update the `date:` field in the frontmatter to today's date.
3. Add any new wiki links that connect to the source page.
4. If the new information contradicts existing content, **do not silently
   overwrite**. Instead, note the contradiction explicitly:
   > ⚠️ **Evolving claim**: [[Source A]] states X, while [[Source B]] states Y.

## Step 5 — Update `index.md`

Add entries for every new wiki page created. Follow the existing format:

- **Entities** go under `## Entities`, alphabetically sorted
- **Concepts** go under `## Concepts`, alphabetically sorted
- **Sources** go under `## Sources`, alphabetically sorted

Entry format: `- [[Page Title]]: <Brief one-line description.>`

If you only updated existing pages (no new pages created), no index changes are
needed.

## Step 6 — Update `wiki/log.md`

Append exactly one line at the end of `wiki/log.md`:

```
## [YYYY-MM-DD] ingest | <Source Title>
```

Use today's date. The source title should match the `title:` field from the
source page frontmatter.

## Step 7 — Post-Ingest Self-Review

Before reporting completion to the user, mentally verify:

- [ ] Source page exists in `wiki/sources/` with correct frontmatter
- [ ] All `[[wiki links]]` in the source page point to real pages (or pages
      you just created)
- [ ] Entity/concept pages were created or updated as needed
- [ ] New pages have complete frontmatter (title, date, tags)
- [ ] `index.md` includes entries for all new pages, alphabetically sorted
- [ ] `wiki/log.md` has the new ingest entry appended
- [ ] No existing content was silently overwritten — contradictions are noted
- [ ] Cross-references flow both ways (new pages link back to the source page,
      and existing pages updated to reference new content where relevant)

## Final Report

After completing all steps, report to the user:
- Pages created (list with paths)
- Pages updated (list with what changed)
- Any contradictions or tensions discovered
- Suggested follow-up actions (e.g., "Consider ingesting source X for more
  context on concept Y")
