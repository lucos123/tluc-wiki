# Social Post & Visual Guide Ingest Guide (v3 — Token- & Speed-Optimized)

This reference documents the **Fast 2-Stage Pipeline** for capturing, downloading, and analyzing social media posts (Facebook, X/Twitter, LinkedIn, Instagram) and multi-slide visual handbooks/infographics into `tluc-wiki`.

---

## Why This Architecture?

1. **Zero 60s Timeouts & Zero Manual `press_key` Loops:** Running an exact, visible-DOM-aware JS gallery harvester inside `mcp_chrome_devtools_evaluate_script` extracts 13–20 high-res CDN URLs in **1 tool call (~4–6s)** instead of 13+ LLM `press_key("ArrowRight")` round trips (~400K–500K wasted tokens).
2. **Zero Output Truncation:** The `browser` subagent returns **only** metadata, verbatim post text, links/comments, and ordered CDN URLs—never writing slide transcriptions inside its reply.
3. **2-Turn Vision + 1-Command Registration:** `download_post_assets.py` pulls all images concurrently in seconds, parallel `read_file` batches (6–7 images/turn) inspect full-res slides in 2 turns, and `register_ingest.py` atomically updates `index.md`, `wiki/log.md`, and runs `lint_wiki.py` in 1 command.

---

## Stage 1 — Fast Browser Harvesting (~5 Browser Tool Calls Total)

Invoke the `browser` subagent (`invoke_subagent` with `TypeName: "browser"`) using this prompt template:

```text
Navigate to: <POST_URL>

Execute fast DOM harvesting ONLY (target ~5 tool calls total):
1. Dismiss any closeable login modal (`X`). If login strictly blocks all content with no close button, stop and report BLOCKED.
2. Click "See more" / "Xem thêm" if truncated, and extract post metadata (author, exact timestamp, engagement), verbatim post text, and author comments/links via 1 `evaluate_script` call.
3. For multi-image posts (Facebook gallery/carousel):
   - Click the first photo thumbnail to enter the photo viewer (`/photo?fbid=...`).
   - Run the 1-Call Gallery Harvester JS snippet below in a SINGLE `evaluate_script` call (targets ONLY the visible stage `<img>` with `rect.width > 200 && rect.height > 200`, `80ms` poll, `1500ms` per-slide cap, `40000ms` total cap):
     * CRITICAL: Do NOT use `document.querySelector('[role="main"] img[src*="scontent"]')` (matches hidden preloaded images and triggers 60s timeouts).
     * CRITICAL: Do NOT iterate slide-by-slide using repeated `press_key("ArrowRight")` LLM turns unless the 1-call JS snippet fails twice.
4. Return ONLY:
   (a) Author, profile URL, exact timestamp, engagement
   (b) Complete verbatim post text & comments/external links
   (c) Ordered list of direct high-resolution CDN image URLs (`fbid`, dimensions, `src`)
   - Do NOT transcribe image text in your reply.
```

### Reference JS Snippets for Facebook (`mcp_chrome_devtools_evaluate_script`)

#### Snippet A — Visible-Stage 1-Call Gallery Harvester (Run once inside `/photo?fbid=...`)
```javascript
async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const startedAt = Date.now();
  const MAX_TOTAL_MS = 40000;
  const PER_SLIDE_MS = 1500;

  const getVisibleStageImg = () => {
    const candidates = Array.from(
      document.querySelectorAll('img[data-visualcompletion="media-vc-image"], [role="main"] img[src*="scontent"], img[src*="scontent"]')
    ).filter((el) => {
      const r = el.getBoundingClientRect();
      const st = getComputedStyle(el);
      return r.width > 200 && r.height > 200 && st.display !== "none" && st.visibility !== "hidden" && st.opacity !== "0";
    });
    candidates.sort((a, b) => {
      const ra = a.getBoundingClientRect();
      const rb = b.getBoundingClientRect();
      return rb.width * rb.height - ra.width * ra.height;
    });
    return candidates[0] || null;
  };

  const snap = () => {
    const fbid = new URL(location.href).searchParams.get("fbid");
    const img = getVisibleStageImg();
    return {
      fbid,
      src: img ? img.src : null,
      dims: img ? `${img.naturalWidth}x${img.naturalHeight}` : null,
    };
  };

  const results = [];
  const seen = new Set();
  let cur = snap();
  if (!cur.fbid || !cur.src) return { error: "Stage image or fbid not found", cur };
  seen.add(cur.fbid);
  results.push({ index: 1, ...cur });

  while (Date.now() - startedAt < MAX_TOTAL_MS && results.length < 40) {
    const prevFbid = cur.fbid;
    const prevSrc = cur.src;
    const nextBtn = document.querySelector('[aria-label="Next photo"], [aria-label="Ảnh tiếp theo"]');
    if (!nextBtn) break;
    nextBtn.click();

    const stepStart = Date.now();
    let updated = null;
    while (Date.now() - stepStart < PER_SLIDE_MS) {
      await sleep(80);
      const probe = snap();
      if (probe.fbid && probe.fbid !== prevFbid && probe.src && probe.src !== prevSrc) {
        updated = probe;
        break;
      }
    }
    if (!updated) updated = snap();
    if (!updated.fbid || seen.has(updated.fbid)) break;
    seen.add(updated.fbid);
    cur = updated;
    results.push({ index: results.length + 1, ...cur });
  }

  return { total: results.length, elapsedMs: Date.now() - startedAt, results };
}
```

### Chrome Remote Debugging Recovery
If the `browser` subagent reports `DevToolsActivePort (ENOENT)`:
1. Ask the user to open Chrome, enable remote debugging at `chrome://inspect/#remote-debugging`, and approve the prompt.
2. **Do not** spawn a duplicate subagent — reuse the existing `browser` subagent `conversationId` via `send_message`.

---

## Stage 2 — Parallel Asset Download & 2-Turn Multimodal `read_file`

### 1. Choose Storage Mode & Run Downloader
| Content Type | `--mode` | Target Image Path | Target Raw Markdown |
| :--- | :--- | :--- | :--- |
| **Visual Guide / Carousel ($\ge 4$ slides)** | `screenshots` | `raw/screenshots/<slug>/00.<ext>` .. `NN.<ext>` | `raw/articles/ai-other/<slug>.md` |
| **Article / Post with 1–3 Diagrams** | `assets` | `raw/assets/<slug>-01.<ext>` .. | `raw/articles/<topic>/<slug>.md` |

Write a scratch manifest JSON file (cleanest for long CDN query strings) and run:
```powershell
python .agents\skills\wiki-ingest\scripts\download_post_assets.py --manifest path\to\manifest.json
```

### 2. Batch Parallel Visual Reading (6–7 Images/Turn)
Call `read_file` directly on the downloaded local images in **parallel batches of 6–7 images per turn**:
- For an 11–14 slide deck, read slides `00..06` in Turn 1 and `07..13` in Turn 2 (**2 turns total**).
- Extract exact formulas, tables, diagrams, arrows, and Vietnamese/English text verbatim at native CDN resolution.

---

## Stage 3 — Raw Documentation, Wiki Synthesis & 1-Command Registration

1. **Save Raw Article (`raw/articles/<topic>/<slug>.md`):**
   - Write YAML frontmatter (`title`, `source`, `original_source` if cited, `author`, `published`, `created`, `description`, `tags`).
   - Include verbatim post text, author links/comments, relative image embeds (`![Page 00](../../screenshots/<slug>/00.jpg)`), and slide-by-slide transcriptions.
2. **Create/Update Wiki Pages (`wiki/sources/`, `wiki/concepts/`, `wiki/entities/`):**
   - Create `wiki/sources/<Source Title>.md` (`source_type: visual-notes`), entity/concept pages with multiline YAML `tags:` lists and verified `[[Wiki Links]]`.
3. **Register Index, Log & Lint in 1 Single Command:**
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
