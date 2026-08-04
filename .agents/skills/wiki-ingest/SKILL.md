---
name: wiki-ingest
description: >
  Ingest a new raw source document (web article, PDF whitepaper, YouTube video URL,
  work note, or transcript) into the wiki. Triggers when the user asks to ingest,
  add, import, process, or summarize a raw source or URL via /wiki-ingest or natural language.
when_to_use: >
  Use whenever a new article, URL, video, PDF, or work note needs to be processed, summarized,
  and integrated into the tluc-wiki knowledge graph.
argument-hint: "<url | path-to-raw-file>"
allowed-tools:
  - run_command
  - view_file
  - write_to_file
  - replace_file_content
  - read_url_content
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
| **PDF Whitepaper / Book** | `raw/pdfs/` | Read PDF content, save to `raw/pdfs/`, then Step 1 |
| **YouTube / Video URL** | `raw/video-transcripts/` | Run `python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py <URL>`, then Step 1 |
| **Work Notes & Drafts** | `raw/notes/<category>/` | Read note file in `raw/notes/`, then Step 1 |
| **Attachments / Images** | `raw/assets/` | Store visual media for referencing |

## 2. Ingest Pipeline (Capture $\rightarrow$ Extract $\rightarrow$ Add to Wiki)

### Step 1 — Pre-Flight Check
1. Verify the source file `$ARGUMENTS` exists in `raw/` (or fetch URL if HTTP/HTTPS).
2. Check `wiki/log.md` to prevent duplicate ingestion.
3. Read `index.md` to map existing concepts/entities.

### Step 2 — Read & Analyze Source
Read the source document thoroughly. Identify:
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
   - Assets/Images: `raw/assets/<descriptive-kebab-case-name>.<ext>` (e.g., `raw/assets/metacode-scattered-to-agent-ready.png`)
2. **Link Synchronization**: Update `wiki/sources/<Source Title>.md` YAML frontmatter `source:` field and body `**Source File**:` link to point to the newly renamed kebab-case raw path.

### Step 4 — Update / Create Entity & Concept Pages
- Create new page in `wiki/entities/` or `wiki/concepts/` if a topic is covered substantively.
- Update existing pages if new information or trade-offs are introduced.
- Note evolving claims explicitly (`⚠️ Evolving claim: [[Source A]] states X, while [[Source B]] states Y.`).

### Step 5 — Update Index & Log
1. Update `index.md` in strict alphabetical order.
2. Append exactly one line to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Source Title>`

### Step 6 — Embedded Verification Loop (Self-Linting Gate)
Run the automated structural health check to verify 0 broken links and 100% index coverage:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```
Confirm the output returns `"total_broken_links": 0` before reporting completion to the user.
