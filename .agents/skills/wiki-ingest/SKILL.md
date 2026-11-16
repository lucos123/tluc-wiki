---
name: wiki-ingest
description: >
  Ingest a new raw source document (web article, social media post on Facebook/X/LinkedIn/Instagram,
  visual slide deck/infographic, PDF whitepaper, YouTube video URL, work note, or transcript)
  into the wiki. Triggers when the user asks to ingest, add, import, collect, download images,
  process, or summarize a source or URL via /wiki-ingest or natural language.
when_to_use: >
  Use whenever an article, social media post, visual slide deck, URL, video, PDF, or work note
  needs to be captured into raw/, summarized, and integrated into the tluc-wiki knowledge graph.
argument-hint: "<url | path-to-raw-file>"
allowed-tools:
  - run_command
  - read_file
  - write_file
  - edit_file
  - invoke_subagent
  - send_message
  - search_web
---

# Wiki Ingest Skill

Target Source: `$ARGUMENTS`

You are operating the persistent Second Brain (`tluc-wiki`). Your task is to ingest a raw source document, extract core concepts and entities, create a source summary page in `wiki/sources/`, update or create entity and concept pages in `wiki/entities/` and `wiki/concepts/`, and update `index.md` and `wiki/log.md`.

Refer to `examples/ingest-workflow-example.md` for a complete execution walkthrough.

## 1. Source Classification & Subfolder Routing

All raw files must reside in structured subfolders under `raw/`:

| Source Type | Subfolder Target | Extraction Protocol |
|-------------|------------------|---------------------|
| **Web Article / Docs** | `raw/articles/<topic>/` | Save markdown/text file, then Step 1 |
| **Social Post / Multi-Slide Visual Deck** | `raw/screenshots/<slug>/` + `raw/articles/<topic>/<slug>.md` | Follow `references/social-post-ingest-guide.md`: 1) Fast browser harvest (text + direct CDN URLs only), 2) `python .agents/skills/wiki-ingest/scripts/download_post_assets.py`, 3) Batch `read_file` on local images |
| **PDF Whitepaper / Book** | `raw/pdfs/` | Read PDF content, save to `raw/pdfs/`, then Step 1 |
| **YouTube / Video URL** | `raw/video-transcripts/` | Follow `references/video-ingest-guide.md`: Run `python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py <URL>`, then Step 1 |
| **Work Notes & Drafts** | `raw/notes/<category>/` | Read note file in `raw/notes/`, then Step 1 |
| **Standalone Attachments / Images (1–3)** | `raw/assets/` | Download via `download_post_assets.py --mode assets` or store for referencing |

## 2. Ingest Pipeline (Capture $\rightarrow$ Extract $\rightarrow$ Add to Wiki)

### Step 1 — Pre-Flight Check & Capture
1. Verify the source file `$ARGUMENTS` exists in `raw/` (or capture HTTP/HTTPS URL into `raw/` first):
   - For **YouTube/Video**, follow `references/video-ingest-guide.md`.
   - For **Facebook / X / LinkedIn / Instagram posts & visual decks**, follow the **2-Stage Social & Visual Pipeline** in `references/social-post-ingest-guide.md` (`browser` subagent harvests text + ordered high-res image URLs without writing full image transcriptions; then download via `scripts/download_post_assets.py` and inspect local images directly with parallel `read_file` batches).
2. Check `wiki/log.md` to prevent duplicate ingestion.
3. Read `index.md` to map existing concepts/entities.

### Step 2 — Read & Analyze Source
Read the source document and any downloaded visual slides thoroughly. Identify:
- **Entities**: Named tools, platforms, organizations, people (`wiki/entities/`).
- **Concepts**: Frameworks, patterns, architectures, methodologies (`wiki/concepts/`).
- **Synthesis Connections**: How this source relates to existing pages in `wiki/`, `mem/`, and `output/`.

### Step 3 — Create Source Summary Page (`wiki/sources/`)
Create a new file `wiki/sources/<Source Title>.md`.
Follow templates in `references/ingest-templates.md` or `references/video-ingest-guide.md`.

### Step 3.5 — Standardize Raw Filename (Kebab-Case) & Synchronize Links
1. **Raw File Kebab-Case Renaming**: Rename the raw input file in `raw/` to a clean, lower-case kebab-case filename based on the document's canonical title (removing trailing browser artifacts like `  Claude`, ` copy`, ` copy 2`, punctuation, and converting spaces to hyphens):
   - Articles/Notes: `raw/<subfolder>/<clean-kebab-case-title>.<ext>` (e.g., `raw/articles/ai-other/emerging-markdown-formats-that-shape-coding-agent-behavior.md`)
   - Video Transcripts: `raw/video-transcripts/<clean-kebab-case-title>.md` (e.g., `raw/video-transcripts/why-graph-engineering-will-10x-your-claude-codex.md`)
   - Visual Decks: `raw/screenshots/<clean-kebab-case-slug>/00.<ext> .. NN.<ext>` (e.g., `raw/screenshots/prompt-engineering-handbook/00.jpg`)
   - Assets/Images: `raw/assets/<descriptive-kebab-case-name>.<ext>` (e.g., `raw/assets/metacode-scattered-to-agent-ready.png`)
2. **Link Synchronization**: Update `wiki/sources/<Source Title>.md` YAML frontmatter `source:` field and body `**Source File**:` link to point to the newly renamed kebab-case raw path.

### Step 4 — Update / Create Entity & Concept Pages (Strict Lint Compliance)
- Create new page in `wiki/entities/` or `wiki/concepts/` if a topic is covered substantively.
- Update existing pages if new information or trade-offs are introduced.
- Note evolving claims explicitly (`⚠️ Evolving claim: [[Source A]] states X, while [[Source B]] states Y.`).
- **Mandatory `lint_wiki.py` Rules**:
  1. Always format `tags:` as a **multiline YAML list** (`tags:\n  - concept\n  - ...`), NEVER inline `tags: [a, b]`.
  2. Include required frontmatter fields (`title`, `date` in `YYYY-MM-DD`, `tags`, plus `source` on all `wiki/sources/` files).
  3. Every `[[Wiki Link]]` inside `wiki/` (unless prefixed with `raw/`) MUST match the exact filename (without `.md`) of an existing page in `wiki/`, `mem/`, or `output/`.

### Step 5 — Update Index & Log
1. Insert every newly created entity, concept, and source page into `index.md` in **strict alphabetical order** under `## Entities`, `## Concepts`, or `## Sources`.
2. Append exactly one line to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Source Title>`

### Step 6 — Embedded Verification Loop (Self-Linting Gate)
Run the automated structural health check to verify 0 broken links and 100% index coverage:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```
Confirm the output returns `"total_broken_links": 0` and `"index_coverage_pct": 100.0` before reporting completion to the user.
