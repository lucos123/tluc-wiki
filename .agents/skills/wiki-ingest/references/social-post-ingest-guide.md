# Social Post & Visual Guide Ingest Guide

This reference documents the **Fast 2-Stage Pipeline** for capturing, downloading, and analyzing social media posts (Facebook, X/Twitter, LinkedIn, Instagram) and multi-slide visual handbooks/infographics into `tluc-wiki`.

---

## Why a 2-Stage Pipeline?

Having a browser subagent manually screenshot every slide **and** write a 20KB+ text transcription inside its own message causes two bottlenecks:
1. High step count and latency (~100+ browser turns).
2. Output truncation of the final slides in long multi-page decks.

Splitting **DOM Harvesting (Browser Subagent)** from **Parallel Download + Direct Multimodal Vision Analysis (Main Executor)** eliminates truncation, cuts browser execution time down dramatically, and preserves full original CDN image resolution (e.g., `1637×2048`).

---

## Stage 1 — Fast Browser Harvesting (Metadata + Text + Image URLs Only)

Invoke the `browser` subagent (`invoke_subagent` with `TypeName: "browser"`) using this prompt template:

```text
Navigate to: <POST_URL>

Execute fast harvesting only (target < 25 steps):
1. Dismiss any closeable login overlay/modal (`X`). If login strictly blocks all content with no close button, stop and report BLOCKED.
2. Click "See more" / "Xem thêm" if present to expand the full post text, and check top/author comments for pinned links.
3. Extract:
   - Author name & profile URL
   - Exact post date/timestamp
   - Complete verbatim post text and any author links/comments
4. Collect all ordered high-resolution image URLs (e.g., `scontent*.fbcdn.net`, `pbs.twimg.com`, `media.licdn.com`) by inspecting the gallery or querying DOM `img` URLs.
   - CRITICAL: Do NOT write full visual transcriptions inside your reply when direct high-res image URLs are extracted. Only return:
     (a) Ordered list of direct high-res image URLs
     (b) A 1-line title/topic for each image (if visible)
   - Only capture screenshots if direct image URLs cannot be extracted from the DOM.
```

### Chrome Remote Debugging Recovery
If the `browser` subagent reports `DevToolsActivePort (ENOENT)`:
1. Ask the user to open Chrome, enable remote debugging at `chrome://inspect/#remote-debugging`, and approve the prompt.
2. **Do not** spawn a duplicate subagent — reuse the existing `browser` subagent `conversationId` via `send_message`.

---

## Stage 2 — Parallel Asset Download & Direct Multimodal `read_file`

### 1. Choose Storage Mode & Run Downloader
| Content Type | `--mode` | Target Image Path | Target Raw Markdown |
| :--- | :--- | :--- | :--- |
| **Visual Guide / Carousel ($\ge 4$ slides)** | `screenshots` | `raw/screenshots/<slug>/00.<ext>` .. `NN.<ext>` | `raw/articles/ai-other/<slug>.md` |
| **Article / Post with 1–3 Diagrams** | `assets` | `raw/assets/<slug>-01.<ext>` .. | `raw/articles/<topic>/<slug>.md` |

Run the deterministic stdlib downloader script:
```powershell
python .agents\skills\wiki-ingest\scripts\download_post_assets.py `
  --slug "<clean-kebab-case-slug>" `
  --mode screenshots `
  --urls "<URL_0>" "<URL_1>" "<URL_2>"
```

If some URLs fail or require authenticated cookies, pass `--fallbacks "<SCREENSHOT_0>" ...` or a `--manifest path/to/manifest.json`:
```json
{
  "slug": "my-visual-guide",
  "mode": "screenshots",
  "start_index": 0,
  "items": [
    {"url": "https://...", "fallback": "C:/.../media_0.png"}
  ]
}
```

The script outputs structured JSON with `rel_path`, `wiki_link` (`[[raw/...]]`), `md_embed`, `format`, `dimensions`, and `bytes` for every saved image.

### 2. Direct Parallel Visual Reading
Call `read_file` directly on the downloaded local images in **parallel batches of 4–6 images per turn**:
- Read `00.jpg` .. `05.jpg` in one batch, then `06.jpg` .. `10.jpg` in the next batch.
- Because `read_file` inspects the full-resolution downloaded image natively, extract exact formulas, tables, diagrams, arrows, and Vietnamese/English text verbatim with zero loss or truncation.

---

## Stage 3 — Raw Documentation & Wiki Synthesis

1. **Save Raw Article (`raw/articles/<topic>/<slug>.md`):**
   - Include YAML frontmatter (`title`, `source`, `original_source` if cited, `author`, `published`, `created`, `description`, `tags`).
   - Include the complete verbatim post text, author links, relative image embeds (`![Page 00](../../screenshots/<slug>/00.jpg)`), and full slide-by-slide visual transcriptions.
2. **Execute Standard `wiki-ingest` Pipeline:**
   - Create `wiki/sources/<Source Title>.md` (`source_type: visual-notes`) linking the raw article and all `[[raw/screenshots/<slug>/...]]` files.
   - Create/update concept and entity pages in `wiki/concepts/` and `wiki/entities/`.
   - Update `index.md` (strict alphabetical order) and `wiki/log.md`.
   - Verify with `python .agents\skills\wiki-lint\scripts\lint_wiki.py`.
