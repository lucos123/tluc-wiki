# Social Post & Multi-Domain Web Ingest Guide (v4.1 — Progressive Disclosure & Zero-URL-Relay)

This reference defines the **v4.1 Multi-Domain Ingest Pipeline** for capturing visual decks, social threads, PDF slides, and technical web articles across **Facebook, Instagram, X/Twitter, LinkedIn, and arbitrary Web Articles (Substack, Medium, blogs, docs)** into `tluc-wiki`.

---

## Key Architecture Pillars

1. **Progressive Disclosure & Redirect Guards via `get_harvester.py`:** Never inline bulky JS harvesters inside prompts upfront. Run `get_harvester.py --url "<URL>"` first—it checks `raw/articles/`, `raw/video-transcripts/`, and `wiki/sources/` for duplicate ingestion (`primary_source` vs `original_source`), guards against accidentally routing YouTube or `.pdf` URLs to `web_article.js`, classifies the platform, and emits **only** the matching `.js` prompt (without duplicating a second raw JS field).
2. **Zero-URL-Relay & Zero-Article-Relay (`steps/<N>/output.txt` $\rightarrow$ `--from-harvest-file`):** When `mcp_chrome_devtools_evaluate_script` writes large output to `steps/<N>/output.txt`, the `browser` subagent **never copies 10–20 signed CDN URLs or 35KB article bodies back into chat**. Instead, it returns ONLY compact metadata + the exact `steps/<N>/output.txt` path. `download_post_assets.py --from-harvest-file ... --init-raw` parses it natively, writes full untruncated text straight to `raw/articles/<topic>/<slug>.md`, and returns a compact stdout summary (`text_preview` for bodies `> 1500` chars unless `--full-meta` is passed).
3. **Cover-First Slug Resolution (`--probe-cover`):** On platforms with short CTA-only captions (`"Comment PDF"` on Instagram/LinkedIn), download only Slide 1 via `--probe-cover scratch/cover.webp` and read it first to determine the exact canonical title and `<slug>` before writing to `raw/`.
4. **Auto Storage Routing (`--mode auto`) & Reliable CDN Downloads:** Automatically routes `1–3` diagrams to `raw/assets/<slug>-01.<ext>` (`assets` mode) and `>= 4` visual slides to `raw/screenshots/<slug>/00.<ext>..NN.<ext>` (`screenshots` mode). Sends explicit non-AVIF `Accept: image/webp,image/png,image/jpeg,image/gif;q=0.9,*/*;q=0.1` headers and automatically retries HTTP `401`/`403` once with a domain-matched `Referer` (checking `instagram`/`cdninstagram` before `fbcdn.net`).
5. **Bilingual Layer Separation:** Always keep visual assets in their **native original language** (English `.webp`/`.jpg` or Vietnamese `.jpg`); write `raw/articles/...` in Vietnamese + verbatim English terms/formulas, and maintain `wiki/` concepts/entities in canonical English (or matching language per target page).

---

## Supported Platforms & Harvesters (`Snippets A–E`)

| Platform | Script (`scripts/harvesters/`) | How It Extracts Accurately & Saves Tokens | Auth / Special Caveats |
| :--- | :--- | :--- | :--- |
| **Facebook** | `facebook.js` *(Snippet A)* | Auto-detects post view vs `/photo?fbid=...` & `/photos/...` Page albums; supports English + Vietnamese login/UI labels; filters comment photos; steps Visible-Stage `rect > 200` carousel (`80ms` poll, `fbid` + `pathname` dedup) | Works on most public posts; if `status === "needs_gallery_open"`, open `first_photo_href` and run `facebook.js` once inside photo viewer |
| **Instagram** | `instagram.js` *(Snippet B)* | Auto-rewinds `?img_index=K` to Slide 1; expands captions; scopes strictly to post carousel & excludes `"More posts from @author"` thumbnails; comma-safe `srcset` max-res picker; ISO `<time datetime>`, co-authors, `videos_found` | **Requires logged-in Chrome session** for full carousels (`status: "blocked"` otherwise); native `.webp` renders cleanly via `read_file`; probe Slide 1 to name `<slug>` |
| **X / Twitter** | `x_twitter.js` *(Snippet C)* | Anchors strictly on focal `/status/<id>` tweet; expands in-tweet `"Show more"`; scrolls virtualized timeline to capture full same-author threads (stopping at other-author replies) + X Longform Articles; upgrades `pbs.twimg.com/media` to **`?name=orig`** | Check `videos_found` / external paper links if tweet quotes an external article |
| **LinkedIn** | `linkedin.js` *(Snippet D)* | Supports both logged-in feed DOM & public post DOM + `SocialMediaPosting` JSON-LD (exact ISO `datePublished`); separates `author_headline` from `published`; steps `.ssplayer-carousel` / `.carousel-next-btn` with stale-stop guard | Checks `/authwall`; if slide deck renders inside a cross-origin PDF iframe, use returned `document_iframe_url` |
| **Web Articles** *(Substack, Medium, Blogs, Docs)* | `web_article.js` *(Snippet E)* | Parses `@graph`-aware JSON-LD + OpenGraph; selects largest text-rich article container; strips nav/aside/footer/comments and Substack subscribe/promo CTAs + lightbox/profile links; converts headings (auto-deduping leading H1), language-tagged `<pre>` code fences, **GFM `<table>`s**, and nested lists (capped 45K chars) + comma-safe `srcset` `<figure>`s | Zero screenshot overhead for text-first articles; pass `--from-harvest-file ... --init-raw` to write clean Markdown directly to `raw/articles/` |

---

## End-to-End 3-Stage Workflow

### Stage 1 — Duplicate Pre-Check & Dispatch (`get_harvester.py`)
```powershell
python .agents/skills/wiki-ingest/scripts/get_harvester.py --url "<TARGET_URL>"
```
1. Check `"status"` (`redirect_video` $\rightarrow$ `video-ingest-guide.md`; `redirect_pdf` $\rightarrow$ `raw/pdfs/`) and inspect `"already_ingested"`, `"has_original_source_overlap"`, and `"duplicate_matches"`.
2. Invoke the `browser` subagent (`TypeName: "browser"`) using the generated `"browser_prompt"` field directly.
3. If the subagent reports `DevToolsActivePort (ENOENT)`: ask the user to enable remote debugging at `chrome://inspect/#remote-debugging`, then reuse the **same** subagent `conversationId` via `send_message`.

### Stage 2 — Cover Probe (If CTA-Only Caption) & Concurrent Download / Zero-Relay Scaffold
- **Optional Slide-1 Probe** (for Instagram/LinkedIn posts without descriptive captions):
  ```powershell
  python .agents\skills\wiki-ingest\scripts\download_post_assets.py `
    --from-harvest-file "C:\...\steps\6\output.txt" `
    --probe-cover "C:\...\scratch\cover.webp"
  ```
  Inspect `cover.webp` with `read_file` to establish `<slug>` cleanly.
- **Full Concurrent Download (`--mode auto`) & Optional Raw Scaffolding (`--init-raw`)**:
  ```powershell
  python .agents\skills\wiki-ingest\scripts\download_post_assets.py `
    --slug "<slug>" --mode auto `
    --from-harvest-file "C:\...\steps\6\output.txt"
  ```
  *(For long Web Articles, add `--init-raw --raw-subdir "<topic>"` to write the full Markdown + figure embeds straight into `raw/articles/<topic>/<slug>.md` with zero context bloat, then read `raw/articles/<topic>/<slug>.md` directly.)*

### Stage 3 — Parallel `read_file`, Immutable `raw/`, Wiki Synthesis & 1-Command Registration
1. Call `read_file` on downloaded local images (`.jpg`, `.png`, `.webp`) in **parallel batches of 5–7 images per turn**.
2. Finalize `raw/articles/<topic>/<slug>.md` **once** (immutable: YAML frontmatter + verbatim post/article content + full bilingual visual transcription with `![Page XX](../../screenshots/<slug>/XX.<ext>)` or `![Asset XX](../../assets/<slug>-XX.<ext>)`).
3. Run `python .agents\skills\wiki-ingest\scripts\register_ingest.py --suggest-links "<keywords>"` (supports both English and Vietnamese Unicode keywords) and create/update `wiki/entities/`, `wiki/sources/`, and `wiki/concepts/` pages with multiline YAML `tags:` lists and zero broken links.
4. Register atomically in **1 command**:
   ```powershell
   python .agents\skills\wiki-ingest\scripts\register_ingest.py `
     --date YYYY-MM-DD `
     --log-type ingest `
     --source-title "<Source Title>" `
     --entry "Entities|<Entity Name>|<One-line summary>" `
     --entry "Concepts|<Concept Name>|<One-line summary>" `
     --entry "Sources|<Source Title>|<One-line summary>"
   ```
   Confirm `"status": "ok"`, `"total_broken_links": 0`, and `"index_coverage_pct": 100.0`.
