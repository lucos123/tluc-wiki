#!/usr/bin/env python3
"""
extract_youtube_transcript.py
─────────────────────────────
Extracts a chaptered, timestamped transcript and keyframe slide timestamp
suggestions from a YouTube (or other yt-dlp-compatible) video URL and saves
it as a kebab-case Markdown file in raw/video-transcripts/.

Usage:
    python extract_youtube_transcript.py <VIDEO_URL> [--output-dir PATH] [--lang LANG] [--json]

Output:
    Prints the saved file path (or JSON metadata with --json) to stdout on success.
    Prints progress and errors to stderr.

Requirements:
    yt-dlp  (auto-installed if missing)
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from collections import deque
from datetime import datetime
from pathlib import Path


VISUAL_CUE_RE = re.compile(
    r"\b(slide|diagram|chart|graph|figure|table|architecture|screenshot|"
    r"on the screen|here you can see|you can see here|look at this|"
    r"as you can see|on this slide|next slide|let's look at)\b",
    re.IGNORECASE,
)


# ── Auto-install yt-dlp if missing ────────────────────────────────────────────

def ensure_yt_dlp() -> bool:
    """Check if yt-dlp is available; install it if not. Returns True on success."""
    try:
        import importlib
        importlib.import_module("yt_dlp")
        return True
    except ImportError:
        pass

    print("[INFO] yt-dlp not found. Attempting auto-install via pip ...", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "yt-dlp", "--quiet"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[ERROR] pip install failed:\n{result.stderr}", file=sys.stderr)
        return False

    print("[INFO] yt-dlp installed successfully.", file=sys.stderr)
    return True


# ── Timestamp & text helpers ──────────────────────────────────────────────────

def parse_timestamp_sec(ts_str: str) -> float:
    """Convert 'HH:MM:SS.mmm' or 'MM:SS.mmm' into float seconds."""
    ts_str = ts_str.strip().replace(",", ".")
    parts = ts_str.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return float(ts_str)


def format_mm_ss(seconds: float) -> str:
    """Format seconds as MM:SS (or H:MM:SS if >= 1 hour)."""
    total = max(0, int(round(seconds)))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def _clean_caption_line(line: str) -> str:
    line = re.sub(r"<[^>]+>", "", line)
    line = html.unescape(line)
    return re.sub(r"\s+", " ", line).strip()


# ── Legacy plain cleaners (preserved for unit-test compatibility) ─────────────

def clean_vtt(content: str) -> str:
    """Convert WebVTT subtitle content to plain readable text."""
    lines = content.splitlines()
    seen = set()
    text_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("NOTE"):
            continue
        if re.match(r"^(Kind|Language):\s", line):
            continue
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*", line):
            continue
        if re.match(r"^\d+$", line):
            continue
        line = _clean_caption_line(line)
        if line and line not in seen:
            seen.add(line)
            text_lines.append(line)

    return "\n".join(text_lines)


def clean_srt(content: str) -> str:
    """Convert SRT subtitle content to plain readable text."""
    content = re.sub(r"^\d+\s*$", "", content, flags=re.MULTILINE)
    content = re.sub(
        r"\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}", "", content
    )
    content = re.sub(r"<[^>]+>", "", content)
    content = html.unescape(content)
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return "\n".join(deduped)


# ── Cue-level parsers preserving timestamps ───────────────────────────────────

VTT_TIMING_RE = re.compile(
    r"^(\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s*-->\s*(\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})"
)


def parse_vtt_cues(content: str) -> list[dict]:
    """Parse VTT subtitles into deduplicated timestamped cues [{'start', 'text'}]."""
    cues = []
    recent = deque(maxlen=6)
    current_start = None
    buffer_lines = []

    def flush_cue():
        nonlocal current_start, buffer_lines
        if current_start is None or not buffer_lines:
            buffer_lines = []
            return
        new_parts = []
        for raw_line in buffer_lines:
            cleaned = _clean_caption_line(raw_line)
            if not cleaned or cleaned in recent:
                continue
            recent.append(cleaned)
            new_parts.append(cleaned)
        if new_parts:
            cues.append({"start": current_start, "text": " ".join(new_parts)})
        buffer_lines = []

    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            flush_cue()
            current_start = None
            continue
        if line.startswith(("WEBVTT", "NOTE")) or re.match(r"^(Kind|Language):\s", line):
            continue
        m = VTT_TIMING_RE.match(line)
        if m:
            flush_cue()
            current_start = parse_timestamp_sec(m.group(1))
            continue
        if current_start is None and re.match(r"^\d+$", line):
            continue
        if current_start is not None:
            buffer_lines.append(line)

    flush_cue()
    return cues


def parse_srt_cues(content: str) -> list[dict]:
    """Parse SRT subtitles into deduplicated timestamped cues [{'start', 'text'}]."""
    return parse_vtt_cues(content)


def format_timestamped_transcript(
    cues: list[dict],
    chapters: list[dict] | None = None,
    duration: int = 0,
    block_seconds: int = 18,
    section_seconds: int = 150,
) -> str:
    """Render cues grouped by chapters (or time blocks) with periodic [MM:SS] markers."""
    if not cues:
        return ""

    if chapters:
        sections = [
            {
                "start": float(ch.get("start_time", 0)),
                "end": float(ch.get("end_time", duration or 999999)),
                "title": ch.get("title", f"Chapter {idx + 1}"),
            }
            for idx, ch in enumerate(chapters)
        ]
    else:
        max_t = float(duration or cues[-1]["start"] + 1)
        sections = []
        t = 0.0
        idx = 1
        while t < max_t:
            end_t = min(max_t, t + section_seconds)
            sections.append({"start": t, "end": end_t, "title": f"Section {idx}"})
            t = end_t
            idx += 1

    out_blocks = []
    for sec in sections:
        sec_cues = [
            c for c in cues
            if sec["start"] <= c["start"] < sec["end"]
            or (sec == sections[-1] and c["start"] >= sec["end"])
        ]
        if not sec_cues:
            continue
        header = f"### [{format_mm_ss(sec['start'])} - {format_mm_ss(sec['end'])}] {sec['title']}"
        out_blocks.append(header)

        para_start = sec_cues[0]["start"]
        para_parts = []
        for cue in sec_cues:
            if para_parts and (cue["start"] - para_start) >= block_seconds:
                out_blocks.append(f"**[{format_mm_ss(para_start)}]** {' '.join(para_parts)}")
                para_start = cue["start"]
                para_parts = [cue["text"]]
            else:
                para_parts.append(cue["text"])
        if para_parts:
            out_blocks.append(f"**[{format_mm_ss(para_start)}]** {' '.join(para_parts)}")
        out_blocks.append("")

    return "\n".join(out_blocks).strip()


def suggest_keyframe_timestamps(
    cues: list[dict],
    chapters: list[dict] | None = None,
    duration: int = 0,
) -> list[dict]:
    """Identify candidate keyframe timestamps from chapters and visual cue phrases."""
    candidates = []
    if chapters:
        for ch in chapters:
            start = float(ch.get("start_time", 0))
            end = float(ch.get("end_time", start + 30))
            span = max(0.0, end - start)
            target = start + min(12.0, max(3.0, span * 0.25))
            candidates.append(
                {
                    "timestamp_sec": int(round(target)),
                    "mm_ss": format_mm_ss(target),
                    "reason": "chapter",
                    "label": ch.get("title", "Chapter"),
                }
            )

    for cue in cues:
        if VISUAL_CUE_RE.search(cue["text"]):
            t = int(round(cue["start"]))
            if not any(abs(c["timestamp_sec"] - t) < 20 for c in candidates):
                candidates.append(
                    {
                        "timestamp_sec": t,
                        "mm_ss": format_mm_ss(t),
                        "reason": "visual_cue",
                        "label": cue["text"][:80],
                    }
                )

    candidates.sort(key=lambda c: c["timestamp_sec"])
    return candidates


# ── Metadata extraction ────────────────────────────────────────────────────────

def get_video_metadata(url: str) -> dict:
    """Fetch video metadata and chapters using yt-dlp."""
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "channel": info.get("channel") or info.get("uploader", "Unknown Channel"),
                "upload_date": info.get("upload_date", ""),
                "duration": info.get("duration", 0),
                "url": url,
                "video_id": info.get("id", ""),
                "chapters": info.get("chapters") or [],
                "description": info.get("description", ""),
                "subtitles": info.get("subtitles") or {},
                "automatic_captions": info.get("automatic_captions") or {},
            }
    except Exception as e:
        print(f"[WARN] Could not fetch metadata: {e}", file=sys.stderr)
        return {
            "title": "Unknown Title",
            "channel": "Unknown Channel",
            "upload_date": "",
            "duration": 0,
            "url": url,
            "video_id": "",
            "chapters": [],
            "description": "",
            "subtitles": {},
            "automatic_captions": {},
        }


def format_duration(seconds: int) -> str:
    if not seconds:
        return "Unknown"
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"


def format_upload_date(raw: str) -> str:
    """Convert YYYYMMDD to YYYY-MM-DD."""
    if len(raw) == 8:
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    return raw


# ── Transcript download ────────────────────────────────────────────────────────

def _fetch_direct_caption_track(meta: dict, lang_pref: list[str]) -> tuple[str, str] | None:
    """Fetch subtitle directly from yt-dlp info tracks, preferring untranslated tracks."""
    expanded_langs = []
    for lang in lang_pref:
        for candidate_lang in (f"{lang}-orig", lang):
            if candidate_lang not in expanded_langs:
                expanded_langs.append(candidate_lang)

    for track_source in (meta.get("subtitles") or {}, meta.get("automatic_captions") or {}):
        for lang_code in expanded_langs:
            entries = track_source.get(lang_code) or []
            candidates = [e for e in entries if e.get("ext") in ("vtt", "srt") and e.get("url")]
            candidates.sort(
                key=lambda e: (
                    1 if "tlang=" in e["url"] else 0,
                    0 if e["ext"] == "vtt" else 1,
                )
            )
            for cand in candidates[:3]:
                try:
                    req = urllib.request.Request(
                        cand["url"], headers={"User-Agent": "Mozilla/5.0"}
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        text = resp.read().decode("utf-8", errors="replace")
                    if text.strip():
                        return text, cand["ext"]
                except Exception:
                    continue
    return None


def download_transcript(
    url: str,
    lang_pref: list[str],
    out_dir: str,
    meta: dict | None = None,
) -> tuple[str, str]:
    """
    Download subtitles using single-pass info URLs (avoiding tlang= 429 rate limits),
    falling back to yt-dlp subtitle download if needed.
    Returns (subtitle_text, format) where format is 'vtt' or 'srt'.
    """
    if meta:
        direct = _fetch_direct_caption_track(meta, lang_pref)
        if direct is not None:
            return direct

    import yt_dlp

    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "transcript")

        for auto in (False, True):
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "writesubtitles": not auto,
                "writeautomaticsub": auto,
                "subtitleslangs": lang_pref,
                "subtitlesformat": "vtt",
                "outtmpl": base,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                except Exception:
                    pass

            for f in Path(tmp).glob("transcript.*"):
                suffix = f.suffix.lstrip(".")
                if suffix in ("vtt", "srt"):
                    content = f.read_text(encoding="utf-8", errors="replace")
                    return content, suffix

    raise RuntimeError(
        "No transcript available for this video. "
        "The video may have subtitles disabled or no auto-generated captions.\n"
        "See references/video-ingest-guide.md for manual fallback options."
    )


# ── Filename helpers ──────────────────────────────────────────────────────────

def sanitize_filename(title: str) -> str:
    """Convert a title to a safe filename (preserved for backward compatibility)."""
    title = re.sub(r'[\\/:*?"<>|]', "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title[:120]


def to_kebab_case(title: str, max_len: int = 100) -> str:
    """Convert a title into a clean lower-case kebab-case slug."""
    cleaned = title.lower().replace("&", " and ")
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len].rsplit("-", 1)[0]
    return cleaned or "video-transcript"


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Extract chaptered, timestamped YouTube transcript into raw/video-transcripts/."
    )
    parser.add_argument("url", help="YouTube (or compatible) video URL")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory to save the output .md file (default: auto-detect raw/video-transcripts/)",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Preferred transcript language code(s), comma-separated (default: en)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON metadata to stdout instead of only file path",
    )
    args = parser.parse_args()

    if not ensure_yt_dlp():
        print(
            "\n[ERROR] Could not install yt-dlp automatically.\n"
            "Please install it manually: pip install yt-dlp",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        script_dir = Path(__file__).resolve().parent
        candidate = script_dir
        for _ in range(10):
            if (candidate / "index.md").exists():
                out_dir = candidate / "raw" / "video-transcripts"
                break
            candidate = candidate.parent
        else:
            out_dir = Path.cwd() / "raw" / "video-transcripts"

    out_dir.mkdir(parents=True, exist_ok=True)
    lang_list = [l.strip() for l in args.lang.split(",") if l.strip()]

    print("[1/3] Fetching video metadata & chapters ...", file=sys.stderr)
    meta = get_video_metadata(args.url)
    title = meta["title"]
    chapters = meta.get("chapters", [])
    print(f"      Title    : {title}", file=sys.stderr)
    print(f"      Channel  : {meta['channel']}", file=sys.stderr)
    print(f"      Duration : {format_duration(meta['duration'])}", file=sys.stderr)
    print(f"      Chapters : {len(chapters)}", file=sys.stderr)

    print(f"[2/3] Downloading transcript (lang pref: {lang_list}) ...", file=sys.stderr)
    try:
        raw_sub, fmt = download_transcript(args.url, lang_list, str(out_dir), meta=meta)
    except RuntimeError as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(2)

    cues = parse_vtt_cues(raw_sub) if fmt == "vtt" else parse_srt_cues(raw_sub)
    transcript_text = format_timestamped_transcript(
        cues, chapters=chapters, duration=meta["duration"]
    )
    if not transcript_text.strip():
        print("[ERROR] Transcript is empty after cleaning.", file=sys.stderr)
        sys.exit(3)

    suggested_keyframes = suggest_keyframe_timestamps(
        cues, chapters=chapters, duration=meta["duration"]
    )

    upload_date = format_upload_date(meta.get("upload_date", ""))
    today = datetime.now().strftime("%Y-%m-%d")
    duration_str = format_duration(meta["duration"])
    channel = meta["channel"]
    video_url = meta["url"]
    slug = to_kebab_case(title)

    chapters_md = ""
    if chapters:
        rows = [
            f"| {idx + 1} | `{format_mm_ss(ch.get('start_time', 0))} - {format_mm_ss(ch.get('end_time', 0))}` | {ch.get('title', '')} |"
            for idx, ch in enumerate(chapters)
        ]
        chapters_md = (
            "\n## Chapters\n\n"
            "| # | Timestamp | Chapter |\n"
            "| :--- | :--- | :--- |\n"
            + "\n".join(rows)
            + "\n"
        )

    keyframes_md = ""
    if suggested_keyframes:
        kf_lines = [
            f"- `{k['mm_ss']}` ({k['timestamp_sec']}s, `{k['reason']}`): {k['label']}"
            for k in suggested_keyframes
        ]
        keyframes_md = "\n## Suggested Keyframe Timestamps\n\n" + "\n".join(kf_lines) + "\n"

    frontmatter = f"""---
title: "{title}"
date: {today}
tags:
  - raw
  - video-transcript
source_type: video
url: "{video_url}"
channel: "{channel}"
upload_date: "{upload_date}"
duration: "{duration_str}"
---"""

    md_content = f"""{frontmatter}

# {title}

**Channel**: {channel}
**URL**: {video_url}
**Upload Date**: {upload_date}
**Duration**: {duration_str}
**Transcript extracted**: {today}

---
{chapters_md}{keyframes_md}
## Transcript

{transcript_text}
"""

    out_path = out_dir / f"{slug}.md"
    out_path.write_text(md_content, encoding="utf-8")

    print("[3/3] Timestamped transcript saved.", file=sys.stderr)
    print(f"      Cues    : {len(cues)}", file=sys.stderr)
    print(f"      Words   : {len(transcript_text.split())}", file=sys.stderr)
    print(f"      File    : {out_path}", file=sys.stderr)

    if args.json:
        print(
            json.dumps(
                {
                    "file_path": str(out_path),
                    "slug": slug,
                    "title": title,
                    "channel": channel,
                    "upload_date": upload_date,
                    "duration": duration_str,
                    "duration_sec": meta["duration"],
                    "chapters": chapters,
                    "suggested_keyframes": suggested_keyframes,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(str(out_path))


if __name__ == "__main__":
    main()
