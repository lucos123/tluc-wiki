---
name: wiki-ingest
description: >
  Ingest a new raw source document (web article, social media post on Facebook/X/LinkedIn/Instagram,
  visual slide deck/infographic, uploaded or local image, PDF whitepaper, YouTube video URL, work note, or transcript)
  into the wiki. Triggers when the user asks to ingest, add, import, collect, download images,
  process, or summarize a source, uploaded image, or URL via /wiki-ingest or natural language.
when_to_use: >
  Use whenever an article, social media post, visual slide deck, uploaded infographic, URL, video, PDF, or work note
  needs to be captured into raw/, summarized, and integrated into the tluc-wiki knowledge graph.
argument-hint: "<url | path-to-raw-file | uploaded-image>"
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
| **Web Article / Docs (HTTP URL)** | `raw/articles/<topic>/` + `raw/assets/` | Follow `references/social-post-ingest-guide.md` v4.3: 1) `get_harvester.py --url <URL>` (`web_article.js` clean Markdown + GFM tables + figure URLs), 2) `download_post_assets.py --from-harvest-file <steps/N/output.txt> --slug <slug> --mode auto --init-raw` (writes full text directly to `raw/` without context bloat), then Step 2 |
| **Social Post / Visual Deck (FB, IG, X, LinkedIn)** | `raw/screenshots/<slug>/` or `raw/assets/` + `raw/articles/<topic>/<slug>.md` | Follow `references/social-post-ingest-guide.md` v4.3: 1) `get_harvester.py --url <URL>` (duplicate check + YouTube/PDF guard + single `harvesters/<platform>.js` prompt + **Zero-URL-Relay**), 2) `download_post_assets.py --from-harvest-file` (`--probe-cover` + `--mode auto`), 3) Batch `read_file` (5–7 images/turn) |
| **Collected / Uploaded Images & Infographics (1–N local files)** | `raw/assets/` (`1–3`) or `raw/screenshots/<slug>/` (`>= 4`) | Follow `references/local-image-ingest-guide.md` v4.4: 1) Visually inspect uploaded/local image(s) via `read_file`, 2) Archive cleanly with `download_post_assets.py --slug <slug> --mode auto --local-files <paths...>` (SHA-256 dedup check; add `--init-raw` if multi-page deck/notes), 3) Transcribe & compound into `wiki/` |
| **PDF Whitepaper / Book** | `raw/pdfs/` | Read PDF content, save to `raw/pdfs/`, then Step 1 |
| **YouTube / Video URL** | `raw/video-transcripts/` + `raw/screenshots/<slug>/` | Follow `references/video-ingest-guide.md`: 1) `extract_youtube_transcript.py <URL> --json` (chapters + `[MM:SS]` cues + `related_wiki_pages`), 2) `capture_youtube_keyframes.py` (1080p smart-probed slides + `--keep/--drop` curation), 3) Batch `read_file` to verify & synthesize slides |
| **Work Notes & Drafts** | `raw/notes/<category>/` | Read note file in `raw/notes/`, then Step 1 |

## 2. Ingest Pipeline (Capture $\rightarrow$ Extract $\rightarrow$ Add to Wiki)

### Step 1 — Pre-Flight Check & Capture
1. Verify the source file `$ARGUMENTS` exists in `raw/` (or capture HTTP/HTTPS URL or uploaded image into `raw/` first):
   - For **YouTube/Video**, follow the **3-Stage Multimodal Pipeline** in `references/video-ingest-guide.md` (`extract_youtube_transcript.py --json` for chaptered `[MM:SS]` transcript + `related_wiki_pages` + `safe_source_page_name` $\rightarrow$ `capture_youtube_keyframes.py` with 3-frame smart probing & `--keep/--drop` curation $\rightarrow$ batch `read_file` to verify visual slides).
   - For **Facebook / Instagram / X / LinkedIn posts & Web Articles**, follow the **v4.3 Multi-Domain Pipeline** in `references/social-post-ingest-guide.md`: run `python .agents/skills/wiki-ingest/scripts/get_harvester.py --url "<URL>"` to verify non-duplication and fetch the single platform-matched JS snippet prompt (`Snippets A–E`) with **Zero-URL-Relay** (`steps/<N>/output.txt` $\rightarrow$ `download_post_assets.py --from-harvest-file` + `--mode auto`), then read native `.jpg`/`.png`/`.webp` images in parallel `read_file` batches of **5–7 images per turn**.
   - For **Uploaded / Local Collected Images & Infographics**, follow `references/local-image-ingest-guide.md`: inspect images with `read_file`, archive into `raw/assets/` or `raw/screenshots/<slug>/` via `download_post_assets.py --local-files --mode auto` (with automatic SHA-256 duplicate detection), and transcribe into `wiki/`.
   - **Language Policy**: Keep native-language visual assets unmodified in `raw/screenshots/` or `raw/assets/`; write `raw/articles/` notes cleanly in Vietnamese paired with verbatim English terminology/formulas, and write `wiki/` pages in the matching canonical language (primarily English with bilingual notes where appropriate).
2. Check `wiki/log.md` to prevent duplicate ingestion.
3. Map existing concepts/entities without wasting extra file scans: use `related_wiki_pages` returned by `extract_youtube_transcript.py --json`, run `python .agents/skills/wiki-ingest/scripts/register_ingest.py --suggest-links "<keywords>"`, or inspect `index.md` directly only when broad manual lookup is needed.

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
- Note evolving claims explicitly (`⚠️ Evolving claim: [Source A](Source%20A.md) states X, while [Source B](Source%20B.md) states Y.`).
- **Mandatory `lint_wiki.py` Rules**:
  1. Always format `tags:` as a **multiline YAML list** (`tags:\n  - concept\n  - ...`), NEVER inline `tags: [a, b]`.
  2. Include required frontmatter fields (`title`, `date` in `YYYY-MM-DD`, `tags`, plus `source` on all `wiki/sources/` files formatted as plain repo-relative paths like `"raw/articles/<topic>/<slug>.md"`).
  3. Every cross-reference inside `wiki/` MUST use **Standard Relative Markdown Links** (`[Display Name](../concepts/Page%20Name.md)`, RFC 3986 percent-encoded via `quote(rel_path, safe="/-._~")`) pointing to an actual existing `.md` page or `raw/` asset — **NEVER** `[[Wiki Links]]`. Format `## Related Pages` groups with `>= 3` links as nested sub-bullets (`- **Concepts**:\n  - [Page A](...)`) instead of single comma-separated lines.

### Step 5 — Atomic Index, Log & Verification Gate (1-Command Finish)
Instead of editing `index.md` and `wiki/log.md` manually across multiple calls, run `register_ingest.py` to atomically insert/sort all new `index.md` entries, append `wiki/log.md`, and execute `lint_wiki.py` in **1 single command** *(uses `--date`, `--log-type`, `--source-title`, and repeatable `--entry "Section|Page|Summary"` — no `--summary` flag)*:
```powershell
python .agents/skills/wiki-ingest/scripts/register_ingest.py `
  --date YYYY-MM-DD `
  --log-type ingest `
  --source-title "<Source Title>" `
  --entry "Entities|<Entity Name>|<One-line summary>" `
  --entry "Concepts|<Concept Name>|<One-line summary>" `
  --entry "Sources|<Source Title>|<One-line summary>"
```
*(Or pass `--manifest path/to/entries.json`.)* Confirm the output returns `"status": "ok"`, `"total_broken_links": 0`, and `"index_coverage_pct": 100.0` before reporting completion to the user.

For standalone structural checks without modifying `index.md` or `wiki/log.md`, run:
```powershell
python .agents/skills/wiki-lint/scripts/lint_wiki.py
```

### Step 6 — Post-Ingest Reflection & Skill Improvement Proposal (Human-Gated)
At the end of every ingestion run—especially after extracting complex videos, social carousels, or dense technical docs—perform a brief pipeline retrospective covering:
- **Execution Friction & Token Efficiency**: Extra tool calls, manual formatting edits, browser retries, or redundant context reads that could be automated.
- **Script & Extraction Quality**: Visual keyframe probing accuracy (`--smart-probe` false positives, missed mid-chapter slides), transcript formatting gaps, or `register_ingest.py` edge cases.
- **Test & Verification Coverage**: Missing unit tests for newly discovered edge cases (`test_extract_youtube_transcript.py`, downloader, or lint checks).

Append a concise final section (`### 💡 Nhận xét & Đề xuất Cải thiện Skill / Pipeline`) to your reply to the user:
- If concrete improvements were spotted, list 1–3 prioritized, actionable proposals (file/script, problem observed, proposed fix) and ask for the user's approval before editing any skill files (**human-gated self-improvement**: never modify `.agents/skills/` scripts silently during an ingest turn without explicit user sign-off).
- If the run executed cleanly with zero friction, confirm briefly that the current skill pipeline operated smoothly with no new gaps observed.
