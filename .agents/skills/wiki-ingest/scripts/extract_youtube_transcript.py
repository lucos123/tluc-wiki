#!/usr/bin/env python3
"""
extract_youtube_transcript.py
─────────────────────────────
Extracts a transcript from a YouTube (or other yt-dlp-compatible) video URL
and saves it as a Markdown file in the wiki's raw/ directory.

Usage:
    python extract_youtube_transcript.py <VIDEO_URL> [--output-dir PATH] [--lang LANG]

Output:
    Prints the saved file path to stdout on success.
    Prints errors to stderr.

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
from datetime import datetime
from pathlib import Path


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


# ── VTT / SRT → clean text ────────────────────────────────────────────────────

def clean_vtt(content: str) -> str:
    """Convert WebVTT subtitle content to plain readable text."""
    lines = content.splitlines()
    seen = set()
    text_lines = []

    for line in lines:
        line = line.strip()
        # Skip headers, timestamps, cue settings, empty lines
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("NOTE"):
            continue
        # Skip VTT metadata lines like "Kind: captions", "Language: en"
        if re.match(r"^(Kind|Language):\s", line):
            continue
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*", line):
            continue
        if re.match(r"^\d+$", line):
            continue
        # Remove inline tags like <00:00:00.000>, <c>, </c>
        line = re.sub(r"<[^>]+>", "", line)
        # Decode HTML entities (&gt; &amp; &lt; etc.)
        line = html.unescape(line)
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            text_lines.append(line)

    return "\n".join(text_lines)


def clean_srt(content: str) -> str:
    """Convert SRT subtitle content to plain readable text."""
    # Remove sequence numbers and timestamps
    content = re.sub(r"^\d+\s*$", "", content, flags=re.MULTILINE)
    content = re.sub(
        r"\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}", "", content
    )
    # Remove HTML tags
    content = re.sub(r"<[^>]+>", "", content)
    # Decode HTML entities
    content = html.unescape(content)
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    # Deduplicate adjacent identical lines
    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return "\n".join(deduped)


# ── Metadata extraction ────────────────────────────────────────────────────────

def get_video_metadata(url: str) -> dict:
    """Fetch video metadata using yt-dlp --dump-json."""
    import yt_dlp  # noqa: F401 — already ensured above

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    try:
        with __import__("yt_dlp").YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "channel": info.get("channel") or info.get("uploader", "Unknown Channel"),
                "upload_date": info.get("upload_date", ""),  # YYYYMMDD
                "duration": info.get("duration", 0),         # seconds
                "url": url,
                "video_id": info.get("id", ""),
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

def download_transcript(url: str, lang_pref: list[str], out_dir: str) -> tuple[str, str]:
    """
    Download subtitles using yt-dlp.
    Returns (file_path, format) where format is 'vtt' or 'srt'.
    Raises RuntimeError if no transcript is available.
    """
    import yt_dlp

    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "transcript")

        # Try manual subtitles first, then auto-generated
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

            # Find any subtitle file that was written
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


# ── Sanitize filename ──────────────────────────────────────────────────────────

def sanitize_filename(title: str) -> str:
    """Convert a title to a safe filename."""
    title = re.sub(r'[\\/:*?"<>|]', "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title[:120]  # cap length


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Extract YouTube transcript and save as wiki-ready Markdown."
    )
    parser.add_argument("url", help="YouTube (or compatible) video URL")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory to save the output .md file (default: auto-detect raw/ from project root)",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Preferred transcript language code(s), comma-separated (default: en). "
             "Example: --lang en,vi",
    )
    args = parser.parse_args()

    # ── Ensure yt-dlp ──
    if not ensure_yt_dlp():
        print(
            "\n[ERROR] Could not install yt-dlp automatically.\n"
            "Please install it manually: pip install yt-dlp\n"
            "Then re-run this script.",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── Resolve output directory ──
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        # Walk up to find project root (where index.md lives)
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

    # ── Fetch metadata ──
    print(f"[1/3] Fetching video metadata ...", file=sys.stderr)
    meta = get_video_metadata(args.url)
    title = meta["title"]
    print(f"      Title   : {title}", file=sys.stderr)
    print(f"      Channel : {meta['channel']}", file=sys.stderr)
    print(f"      Duration: {format_duration(meta['duration'])}", file=sys.stderr)

    # ── Download transcript ──
    print(f"[2/3] Downloading transcript (lang pref: {lang_list}) ...", file=sys.stderr)
    try:
        raw_sub, fmt = download_transcript(args.url, lang_list, str(out_dir))
    except RuntimeError as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(2)

    # ── Clean transcript ──
    if fmt == "vtt":
        transcript_text = clean_vtt(raw_sub)
    else:
        transcript_text = clean_srt(raw_sub)

    if not transcript_text.strip():
        print("[ERROR] Transcript is empty after cleaning.", file=sys.stderr)
        sys.exit(3)

    # ── Build Markdown file ──
    upload_date = format_upload_date(meta.get("upload_date", ""))
    today = datetime.now().strftime("%Y-%m-%d")
    duration_str = format_duration(meta["duration"])
    channel = meta["channel"]
    video_url = meta["url"]

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

## Transcript

{transcript_text}
"""

    # ── Save file ──
    filename = sanitize_filename(title) + ".md"
    out_path = out_dir / filename
    out_path.write_text(md_content, encoding="utf-8")

    print(f"[3/3] Transcript saved.", file=sys.stderr)
    print(f"      Lines   : {len(transcript_text.splitlines())}", file=sys.stderr)
    print(f"      Words   : {len(transcript_text.split())}", file=sys.stderr)
    print(f"      File    : {out_path}", file=sys.stderr)

    # Print the path to stdout so SKILL.md workflow can capture it
    print(str(out_path))


if __name__ == "__main__":
    main()
