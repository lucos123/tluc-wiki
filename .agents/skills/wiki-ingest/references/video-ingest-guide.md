# Video Ingest Guide (Multimodal Transcript + 1080p Keyframe Pipeline)

This reference covers how to ingest video content (YouTube, Vimeo, conference talks, technical walkthroughs) into `tluc-wiki` by combining **chaptered, timestamped transcripts** with **targeted 1080p keyframe screenshots** of critical slides, diagrams, and charts.

---

## 3-Stage Multimodal Video Ingestion Pipeline

### Stage 1 — Extract Chaptered, Timestamped Transcript & Link Context
Run `extract_youtube_transcript.py` to fetch video metadata, chapters, `[MM:SS]`-marked transcript blocks, late-chapter keyframe suggestions, and matching `index.md` wiki links in **one single call**:

```powershell
# English transcript (default) with structured JSON (timestamps, safe filename, related wiki links)
python .agents\skills\wiki-ingest\scripts\extract_youtube_transcript.py "<VIDEO_URL>" --lang en --json

# Prefer Vietnamese, fallback to English
python .agents\skills\wiki-ingest\scripts\extract_youtube_transcript.py "<VIDEO_URL>" --lang vi,en --json
```

Read the generated `.md` transcript file to refine the timestamp list (`suggested_timestamps_arg` samples late-chapter 78%–85% completion moments by default, automatically adds a 48% mid-chapter marker for long chapters $\ge 150\text{s}$, and scans expanded `VISUAL_CUE_RE` phrases), using `related_wiki_pages` and `safe_source_page_name` directly when drafting wiki pages without running extra directory scans.

### Stage 2 — Capture (Smart-Probe) & Curate 1080p Keyframe Slides
Run `capture_youtube_keyframes.py` (uses `yt-dlp` + standalone `ffmpeg` via `imageio-ffmpeg` HTTP range-seeking — **no full video download needed**). By default, **3-frame single-seek smart probing** (`--smart-probe`, `--probe-offset 4.0`) extracts 3 frames around each timestamp in one seek and uses `_select_best_probed_frame()` to filter low-byte fade/cut frames (`<70KB`) while keeping crisp white/Excalidraw slides (`110–168KB`) from being overridden by textured full-screen webcam cuts (`172–205KB`). Pass **`--update-transcript`** to insert/sync `## Key Visual Frames` inside `raw/video-transcripts/<slug>.md` automatically without extra manual `edit_file` calls:

```powershell
# Capture targeted timestamps and auto-embed ## Key Visual Frames in the transcript
python .agents\skills\wiki-ingest\scripts\capture_youtube_keyframes.py `
  --url "<VIDEO_URL>" `
  --slug "<clean-kebab-case-slug>" `
  --timestamps "01:38=Architecture,04:14=Threats,08:05=Four-Pillars" `
  --update-transcript

# Or auto-sample representative chapter keyframes directly
python .agents\skills\wiki-ingest\scripts\capture_youtube_keyframes.py `
  --url "<VIDEO_URL>" `
  --slug "<clean-kebab-case-slug>" `
  --auto-chapters --update-transcript
```

Inspect all captured frames in `raw/screenshots/<slug>/` using parallel `read_file` batches (6–7 images/turn):
- **Atomic Curation & Renumbering (`--keep` / `--drop` + `--update-transcript`):** If any frame is still redundant or low-value (or after capturing supplemental `--start-index` frames), prune, renumber `01.jpg..NN.jpg`, and re-sync the transcript embeds in 1 deterministic command without manual PowerShell move chains:
  ```powershell
  # Keep specific indices in exact chronological order, renumber, and update transcript links
  python .agents\skills\wiki-ingest\scripts\capture_youtube_keyframes.py --slug "<slug>" --keep "1,12,3,8" --update-transcript

  # Or drop weak/duplicate indices and sync remaining links
  python .agents\skills\wiki-ingest\scripts\capture_youtube_keyframes.py --slug "<slug>" --drop "2,5" --update-transcript
  ```

### Stage 3 — Embed Visual Transcriptions, Synthesize Wiki & Register
1. Verify that `raw/video-transcripts/<slug>.md` contains the curated `## Key Visual Frames` links (`![MM:SS - <Label>](../screenshots/<slug>/NN.jpg)`), adding any concise visual transcriptions if needed (or omit manual `edit_file` entirely when `--update-transcript` already synced them cleanly).
2. Create `wiki/sources/<safe_source_page_name>.md` (`source_type: video`) linking both the raw transcript (`[raw/video-transcripts/<slug>.md](../../raw/video-transcripts/<slug>.md)`) and all kept `[raw/screenshots/<slug>/NN.jpg](../../raw/screenshots/<slug>/NN.jpg)` slides via Standard Relative Markdown Links, plus entity/concept pages in `wiki/entities/` and `wiki/concepts/`. To search `index.md` for additional candidate links by keyword, run:
   ```powershell
   python .agents\skills\wiki-ingest\scripts\register_ingest.py --suggest-links "supply chain security sbom"
   ```
3. Register all new pages into `index.md`, append `wiki/log.md`, and run `lint_wiki.py` in **1 command**:
   ```powershell
   python .agents\skills\wiki-ingest\scripts\register_ingest.py `
     --date YYYY-MM-DD `
     --log-type ingest `
     --source-title "<Video Title>" `
     --entry "Entities|..." `
     --entry "Concepts|..." `
     --entry "Sources|<safe_source_page_name>|..."
   ```

---

## How the Scripts Work

1. **`extract_youtube_transcript.py`**:
   - Auto-installs `yt-dlp` if missing and fetches metadata + direct caption tracks in a single pass (preferring untranslated `en-orig`/`en` tracks to avoid HTTP 429 limits).
   - Parses cue start times (`parse_vtt_cues`), deduplicates rolling auto-captions without discarding timestamps, groups under `### [MM:SS - MM:SS] <Chapter>` sections, emits `**[MM:SS]**` markers every ~18s, and writes directly to `raw/video-transcripts/<kebab-case-title>.md`.
   - With `--json`, emits `safe_source_page_name`, multi-point chapter suggestions (adding a `48%` midpoint candidate for chapters $\ge 150\text{s}$), expanded `VISUAL_CUE_RE` markers, and top `related_wiki_pages` ranked from `index.md`.
2. **`capture_youtube_keyframes.py`**:
   - Enables Node.js `js_runtimes` automatically for `yt-dlp` when present, auto-installs `imageio-ffmpeg` if system `ffmpeg` is not on PATH, and auto-upgrades `yt-dlp` on HTTP 403 retry.
   - Selects the highest-resolution direct HTTPS stream ($\le 1080\text{p}$) and seeks concurrently (`ThreadPoolExecutor`) with **chapter-bounded** single-seek 3-frame smart probing (`--smart-probe`, clamping the burst inside `[chapter_start, chapter_end - 2s]` via `_compute_probe_window()` so short chapters never drift past transitions into the next chapter; `--no-smart-probe` extracts the exact timestamp frame).
   - Verifies saved JPG dimensions via pure-Python binary header inspection, supports atomic `--keep` / `--drop` curation and renumbering (`01.jpg .. NN.jpg`), and syncs `## Key Visual Frames` inside `raw/video-transcripts/<slug>.md` when passed `--update-transcript`.

---

## Language Selection

| Scenario | `--lang` flag |
|----------|--------------|
| English video (default) | *(omit flag)* |
| Vietnamese video | `--lang vi,en` |
| Auto-detect best available | `--lang en,vi,zh,ja,ko` |

---

## Fallback: Manual Transcript Extraction

If the script fails (video has no captions, private video, geo-blocked, etc.):

### Option A — YouTube built-in transcript viewer
1. Open the video in Chrome/Edge
2. Click `...` (more options) $\rightarrow$ **Open transcript**
3. Select language in the transcript panel and copy text into `raw/video-transcripts/`

### Option B — yt-dlp direct download (command line)
```powershell
yt-dlp --write-subs --write-auto-subs --skip-download --sub-format vtt <URL>
yt-dlp --list-subs <URL>
```

---

## Source Page Template for Videos

```markdown
---
title: "<Video Title>"
date: <YYYY-MM-DD>
tags:
  - source
  - <topic-tag-1>
  - <topic-tag-2>
source: "raw/video-transcripts/<slug>.md"
source_type: video
url: "<YouTube URL>"
channel: "<Channel Name>"
speaker: "<Speaker Name>"
duration: "<e.g., 24m 38s>"
---

# <Video Title>

**Channel**: <Channel Name>
**Speaker**: <Speaker Name>
**URL**: <YouTube URL>
**Duration**: <duration>
**Transcript**: [raw/video-transcripts/<slug>.md](../../raw/video-transcripts/<slug>.md)
**Key Slides**: [raw/screenshots/<slug>/01.jpg](../../raw/screenshots/<slug>/01.jpg), ...

<1-2 sentence overview: what this video is about and why it matters.>

## Key Concepts

- **<Concept Name>**: <Explanation with [Markdown links](../concepts/Concept%20Name.md)>

## Synthesis Notes

<Analytical commentary. How does this video connect to the knowledge base?>
```

---

## Known Limitations & Zero-403 Canvas Fallback

| Issue | Cause | Workaround |
|-------|-------|------------|
| `No transcript available` | Video has no captions enabled | Manual fallback |
| Garbled text | Auto-captions with heavy accent | Use manual subtitles `--lang en` |
| Stream `ffmpeg` seek returns `403 Forbidden` | YouTube PO-token enforcement blocks CLI stream URLs | Run the **1-Call Chrome `<video>` + `<canvas>` Keyframe Harvester** below via the `browser` subagent, then pass `--from-data-urls-json` |
| Short transcript | Only intro captured | Check if video is private or age-gated |

### Fallback: 1-Call Chrome HTML5 `<video>` + `<canvas>` Keyframe Harvester
When `ffmpeg` receives `403 Forbidden`, invoke the `browser` subagent to open `<VIDEO_URL>`, skip any pre-roll ad, and execute this `mcp_chrome_devtools_evaluate_script` function (captures raw HD frames directly from the `<video>` element with zero YouTube player chrome):

```javascript
async () => {
  const targets = [
    { sec: 82, label: "Factory Line Shaft" },
    // ... { sec: <seconds>, label: "<label>" }
  ];
  const video = document.querySelector("video.html5-main-video");
  if (!video) return { error: "No html5-main-video element found" };
  video.pause();
  video.muted = true;
  const player = document.getElementById("movie_player");
  if (player?.setPlaybackQualityRange) {
    try { player.setPlaybackQualityRange("hd1080", "hd1080"); } catch {}
  }
  const waitSeek = (t) =>
    new Promise((resolve) => {
      let done = false;
      const finish = () => {
        if (done) return;
        done = true;
        video.removeEventListener("seeked", onSeek);
        setTimeout(resolve, 180);
      };
      const onSeek = () => finish();
      video.addEventListener("seeked", onSeek, { once: true });
      video.currentTime = t;
      setTimeout(finish, 3000);
    });

  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  const out = [];
  for (const item of targets) {
    await waitSeek(item.sec);
    const w = Math.min(1280, video.videoWidth || 1280);
    const h = Math.round((w * (video.videoHeight || 720)) / (video.videoWidth || 1280));
    canvas.width = w;
    canvas.height = h;
    ctx.drawImage(video, 0, 0, w, h);
    out.push({
      timestamp_sec: item.sec,
      label: item.label,
      dims: `${w}x${h}`,
      data_url: canvas.toDataURL("image/jpeg", 0.82),
    });
  }
  return out;
}
```

Save the returned JSON array to a scratch file and decode it via:
```powershell
python .agents\skills\wiki-ingest\scripts\capture_youtube_keyframes.py `
  --url "<VIDEO_URL>" `
  --slug "<clean-kebab-case-slug>" `
  --from-data-urls-json path\to\frames.json
```
