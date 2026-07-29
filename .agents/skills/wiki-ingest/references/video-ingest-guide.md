# Video Ingest Guide

This reference covers how to ingest video content (YouTube, Vimeo, etc.) into the wiki
using the automated extraction script. Read this when `SKILL.md` directs you here.

---

## Quick Start

### Step 1 — Run the extraction script

```powershell
python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py <VIDEO_URL>
```

**Examples:**
```powershell
# English transcript (default)
python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py https://www.youtube.com/watch?v=abc123

# Prefer Vietnamese, fallback to English
python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py https://www.youtube.com/watch?v=abc123 --lang vi,en

# Save to a specific directory
python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py https://www.youtube.com/watch?v=abc123 --output-dir raw/claude-code
```

### Step 2 — Use the output path

The script prints the saved file path to **stdout**. Use that path as the source for the
normal wiki-ingest Step 1 (Read & Analyze).

```
raw/video-transcripts/The Art of Loop Engineering.md  ← use this path
```

### Step 3 — Proceed with normal ingest

Continue from **Step 1** of `SKILL.md` using the extracted `.md` file as your source.

---

## Installation

`yt-dlp` is auto-installed by the script if missing. If auto-install fails:

```powershell
pip install yt-dlp
```

Or with uv:
```powershell
uv pip install yt-dlp
```

---

## How the Script Works

1. **Metadata fetch**: Retrieves title, channel, upload date, duration using `yt-dlp --dump-json`
2. **Transcript download**: Tries manual subtitles first, then auto-generated captions
3. **Cleaning**: Strips timestamps, sequence numbers, HTML tags, and deduplicates overlapping caption lines
4. **Output**: Saves a `.md` file with YAML frontmatter (title, url, channel, duration, date)

---

## Language Selection

| Scenario | `--lang` flag |
|----------|--------------|
| English video (default) | *(omit flag)* |
| Vietnamese video | `--lang vi,en` |
| Auto-detect best available | `--lang en,vi,zh,ja,ko` |

The script tries each language in order and uses the first one available.

---

## Fallback: Manual Transcript Extraction

If the script fails (video has no captions, private video, geo-blocked, etc.):

### Option A — YouTube built-in transcript viewer
1. Open the video in Chrome/Edge
2. Click `...` (more options) → **Open transcript**
3. Select language in the transcript panel
4. Open browser DevTools Console (`F12`)
5. Run this JS snippet to extract all text:
```javascript
(() => {
  const segments = document.querySelectorAll('ytd-transcript-segment-renderer');
  const lines = Array.from(segments).map(s => s.querySelector('.segment-text').textContent.trim());
  copy(lines.join('\n'));
  console.log(`Copied ${lines.length} lines to clipboard.`);
})();
```
6. Paste into a new file in `raw/video-transcripts/`

### Option B — yt-dlp direct download (command line)
```powershell
# Download all available subtitles
yt-dlp --write-subs --write-auto-subs --skip-download --sub-format vtt <URL>

# List available subtitle tracks
yt-dlp --list-subs <URL>
```

---

## Source Page Template for Videos

When creating the `wiki/sources/` page for a video, use this extended template that
includes video-specific fields:

```markdown
---
title: <Video Title>
date: <YYYY-MM-DD of today>
tags:
  - source
  - <topic-tag-1>
  - <topic-tag-2>
source: raw/video-transcripts/<filename>.md
source_type: video
url: "<YouTube URL>"
channel: "<Channel Name>"
speaker: "<Speaker Name (if known)>"
duration: "<e.g., 32m 15s>"
---

# <Video Title>

**Channel**: <Channel Name>
**Speaker**: <Speaker Name>
**URL**: <YouTube URL>
**Duration**: <duration>
**Transcript**: [[raw/video-transcripts/<filename>.md]]

<1-2 sentence overview: what this video is about and why it matters.>

## Key Concepts

- **<Concept Name>**: <Explanation with [[wiki links]]>

## Synthesis Notes

<Analytical commentary. How does this video connect to the knowledge base? 
What does it add, confirm, or contradict?>
```

---

## Quality Checklist for Video Ingestion

Before proceeding to wiki page creation, verify the extracted transcript is usable:

- [ ] Transcript has at least 200 lines (thin transcripts = auto-captions may have failed)
- [ ] Text is readable (not garbled Unicode or repeated artifacts)
- [ ] Speaker names or sections are identifiable in the content
- [ ] No major gaps (check if the transcript covers the whole video)

If the transcript quality is poor, switch to the manual fallback (Option A or B above).

---

## Known Limitations

| Issue | Cause | Workaround |
|-------|-------|------------|
| `No transcript available` | Video has no captions enabled | Manual fallback |
| Garbled text | Auto-captions with heavy accent | Use manual subtitles `--lang en` |
| Script hangs | Network timeout | Re-run; check VPN/firewall |
| Short transcript | Only intro captured | Check if video is private or age-gated |
