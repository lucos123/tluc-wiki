# Video Ingest Guide (Multimodal Transcript + 1080p Keyframe Pipeline)

This reference covers how to ingest video content (YouTube, Vimeo, conference talks, technical walkthroughs) into `tluc-wiki` by combining **chaptered, timestamped transcripts** with **targeted 1080p keyframe screenshots** of critical slides, diagrams, and charts.

---

## 3-Stage Multimodal Video Ingestion Pipeline

### Stage 1 — Extract Chaptered, Timestamped Transcript
Run `extract_youtube_transcript.py` to fetch video metadata, chapters, `[MM:SS]`-marked transcript blocks, and suggested keyframe timestamps into `raw/video-transcripts/<clean-kebab-case-slug>.md`:

```powershell
# English transcript (default) with JSON metadata output
python .agents\skills\wiki-ingest\scripts\extract_youtube_transcript.py "<VIDEO_URL>" --lang en --json

# Prefer Vietnamese, fallback to English
python .agents\skills\wiki-ingest\scripts\extract_youtube_transcript.py "<VIDEO_URL>" --lang vi,en
```

Read the generated `.md` transcript file to inspect all **Chapters**, **Suggested Keyframe Timestamps**, and `[MM:SS]` cues so you can pinpoint the exact 8–12 moments where slides, diagrams, formulas, or architectural comparisons appear.

### Stage 2 — Capture & Visually Verify 1080p Keyframe Slides
Run `capture_youtube_keyframes.py` (uses `yt-dlp` + standalone `ffmpeg` via `imageio-ffmpeg` HTTP range-seeking — **no full video download needed**):

```powershell
# Capture targeted timestamps identified from the transcript
python .agents\skills\wiki-ingest\scripts\capture_youtube_keyframes.py `
  --url "<VIDEO_URL>" `
  --slug "<clean-kebab-case-slug>" `
  --timestamps "00:35=Intro,02:25=Line Shaft Era,04:10=Architecture"

# Or auto-sample one representative frame per YouTube chapter
python .agents\skills\wiki-ingest\scripts\capture_youtube_keyframes.py `
  --url "<VIDEO_URL>" `
  --slug "<clean-kebab-case-slug>" `
  --auto-chapters
```

Inspect all captured frames in `raw/screenshots/<slug>/` using parallel `read_file` batches (6–7 images/turn):
- **Filter pure talking-head frames:** If a frame only shows the speaker without a slide, diagram, or visual card, either re-seek to the exact timestamp inside that chapter where the slide appears, or delete uninformative duplicates and re-index so `raw/screenshots/<slug>/` contains only high-value visual frames.

### Stage 3 — Embed Visual Transcriptions, Synthesize Wiki & Register
1. Embed the verified keyframe screenshots (`![Slide NN - MM:SS](../screenshots/<slug>/NN.jpg)`) and concise visual transcriptions into the raw transcript (`raw/video-transcripts/<slug>.md`).
2. Create `wiki/sources/<Video Title>.md` (`source_type: video`) linking both the raw transcript and all kept `[[raw/screenshots/<slug>/NN.jpg]]` slides, plus entity/concept pages in `wiki/entities/` and `wiki/concepts/`.
3. Register all new pages into `index.md`, append `wiki/log.md`, and run `lint_wiki.py` in **1 command**:
   ```powershell
   python .agents\skills\wiki-ingest\scripts\register_ingest.py `
     --date YYYY-MM-DD `
     --log-type ingest `
     --source-title "<Video Title>" `
     --entry "Entities|..." `
     --entry "Concepts|..." `
     --entry "Sources|<Video Title>|..."
   ```

---

## How the Scripts Work

1. **`extract_youtube_transcript.py`**:
   - Auto-installs `yt-dlp` if missing.
   - Extracts metadata, `chapters`, and manual/auto VTT captions.
   - Parses cue start times (`parse_vtt_cues`), deduplicates rolling auto-captions without discarding timestamps, groups under `### [MM:SS - MM:SS] <Chapter>` sections, emits `**[MM:SS]**` markers every ~18s, and writes directly to `raw/video-transcripts/<kebab-case-title>.md`.
2. **`capture_youtube_keyframes.py`**:
   - Auto-installs `imageio-ffmpeg` if system `ffmpeg` is not on PATH.
   - Selects the highest-resolution direct HTTPS stream ($\le 1080\text{p}$) and seeks concurrently (`ThreadPoolExecutor`) with `ffmpeg -ss <sec> -i <stream_url> -frames:v 1 -q:v 2`.
   - Verifies saved JPG dimensions via pure-Python binary header inspection and outputs JSON containing `rel_path`, `wiki_link`, `md_embed`, `timestamp_sec`, `mm_ss`, and `dimensions`.

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
source: "[[raw/video-transcripts/<slug>.md]]"
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
**Transcript**: [[raw/video-transcripts/<slug>.md]]
**Key Slides**: [[raw/screenshots/<slug>/01.jpg]], ...

<1-2 sentence overview: what this video is about and why it matters.>

## Key Concepts

- **<Concept Name>**: <Explanation with [[wiki links]]>

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
