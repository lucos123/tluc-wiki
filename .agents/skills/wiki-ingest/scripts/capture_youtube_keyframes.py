#!/usr/bin/env python3
"""
capture_youtube_keyframes.py
────────────────────────────
Captures native 1080p/720p video keyframes at specified timestamps (or chapter
midpoints) directly from a YouTube stream using HTTP range-seeking via ffmpeg,
with automatic yt-dlp upgrade retry on 403 and a --from-data-urls-json mode
for decoding raw frames captured via Chrome HTML5 <video> + <canvas>.

Usage:
    python .agents/skills/wiki-ingest/scripts/capture_youtube_keyframes.py \
        --url "https://www.youtube.com/watch?v=..." \
        --slug "video-slug" \
        --timestamps "00:35=Intro,02:25=Architecture,05:10=Benchmarks"

    python .agents/skills/wiki-ingest/scripts/capture_youtube_keyframes.py \
        --url "https://www.youtube.com/watch?v=..." \
        --slug "video-slug" \
        --from-data-urls-json path/to/frames.json

Requirements:
    yt-dlp, imageio-ffmpeg (or system ffmpeg on PATH; auto-installed if missing)
"""

import argparse
import base64
import concurrent.futures
import importlib
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_post_assets import detect_image_info, find_project_root


def ensure_package(import_name: str, pip_name: str) -> bool:
    """Import a package or attempt silent pip installation if missing."""
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        pass
    print(f"[INFO] {pip_name} not found. Installing via pip ...", file=sys.stderr)
    res = subprocess.run(
        [sys.executable, "-m", "pip", "install", pip_name, "--quiet"],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        print(f"[ERROR] Failed to install {pip_name}:\n{res.stderr}", file=sys.stderr)
        return False
    return True


def upgrade_yt_dlp() -> bool:
    """Upgrade yt-dlp in place and reload module to handle YouTube 403 changes."""
    print("[INFO] Attempting yt-dlp upgrade via pip ...", file=sys.stderr)
    res = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-U", "yt-dlp", "--quiet"],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        print(f"[WARN] yt-dlp upgrade failed:\n{res.stderr}", file=sys.stderr)
        return False
    for name in list(sys.modules):
        if name == "yt_dlp" or name.startswith("yt_dlp."):
            sys.modules.pop(name, None)
    importlib.invalidate_caches()
    return True


def resolve_ffmpeg_exe() -> str:
    """Locate system ffmpeg or imageio-ffmpeg standalone binary."""
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg
    if not ensure_package("imageio_ffmpeg", "imageio-ffmpeg"):
        raise RuntimeError("Could not find system ffmpeg or install imageio-ffmpeg.")
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def parse_timestamp_token(token: str) -> tuple[float, str]:
    """Parse 'MM:SS=Label', 'H:MM:SS', or '125' into (seconds, label)."""
    if "=" in token:
        raw_ts, label = token.split("=", 1)
        label = label.strip()
    else:
        raw_ts, label = token, ""
    raw_ts = raw_ts.strip()
    parts = raw_ts.split(":")
    if len(parts) == 3:
        sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        sec = int(parts[0]) * 60 + float(parts[1])
    else:
        sec = float(raw_ts)
    return max(0.0, sec), label


def format_mm_ss(seconds: float) -> str:
    total = max(0, int(round(seconds)))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def extract_stream_and_chapters(url: str, max_height: int = 1080) -> dict:
    """Fetch direct HTTPS video stream URL and chapter metadata via yt-dlp."""
    import yt_dlp

    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = [
        f
        for f in (info.get("formats") or [])
        if f.get("vcodec") not in (None, "none")
        and f.get("url")
        and f.get("protocol") in ("https", "http")
        and (f.get("height") or 0) <= max_height
    ]
    if not formats:
        formats = [
            f
            for f in (info.get("formats") or [])
            if f.get("vcodec") not in (None, "none") and f.get("url")
        ]
    if not formats:
        raise RuntimeError("No downloadable video stream format found via yt-dlp.")

    def score_format(f):
        height = f.get("height") or 0
        ext_bonus = 2 if f.get("ext") == "mp4" else (1 if f.get("ext") == "webm" else 0)
        proto_bonus = 2 if f.get("protocol") in ("https", "http") else 0
        tbr = f.get("tbr") or 0
        return (proto_bonus, height, ext_bonus, tbr)

    best = max(formats, key=score_format)
    return {
        "stream_url": best["url"],
        "stream_height": best.get("height") or 0,
        "stream_ext": best.get("ext") or "unknown",
        "http_headers": best.get("http_headers") or info.get("http_headers") or {},
        "chapters": info.get("chapters") or [],
        "duration": info.get("duration") or 0,
        "title": info.get("title") or "",
    }


def _build_ffmpeg_headers(http_headers: dict) -> str:
    lines = [f"{k}: {v}" for k, v in http_headers.items() if k and v]
    return "\r\n".join(lines) + "\r\n" if lines else ""


def capture_single_frame(task: dict) -> dict:
    """Seek via ffmpeg and extract a single high-quality JPG keyframe."""
    idx_num = task["index"]
    sec = task["timestamp_sec"]
    label = task["label"]
    out_dir = task["out_dir"]
    project_root = task["project_root"]
    slug = task["slug"]
    ffmpeg_exe = task["ffmpeg_exe"]
    stream_url = task["stream_url"]
    headers_str = task["headers_str"]

    filename = f"{idx_num:02d}.jpg"
    dest_path = os.path.join(out_dir, filename)

    cmd = [ffmpeg_exe, "-y", "-loglevel", "error"]
    if headers_str:
        cmd.extend(["-headers", headers_str])
    cmd.extend([
        "-ss", f"{sec:.3f}",
        "-i", stream_url,
        "-frames:v", "1",
        "-q:v", "2",
        dest_path,
    ])

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    if proc.returncode != 0 or not os.path.isfile(dest_path) or os.path.getsize(dest_path) < 2000:
        return {
            "index": idx_num,
            "timestamp_sec": sec,
            "mm_ss": format_mm_ss(sec),
            "label": label,
            "status": "failed",
            "error": proc.stderr.strip() or "ffmpeg produced empty frame",
        }

    with open(dest_path, "rb") as f:
        data = f.read()
    fmt, dims = detect_image_info(data)
    rel_path = os.path.relpath(dest_path, project_root).replace("\\", "/")

    return {
        "index": idx_num,
        "filename": filename,
        "rel_path": rel_path,
        "wiki_link": f"[[{rel_path}]]",
        "md_embed": f"![Slide {idx_num:02d} - {format_mm_ss(sec)}](../screenshots/{slug}/{filename})",
        "timestamp_sec": sec,
        "mm_ss": format_mm_ss(sec),
        "label": label,
        "bytes": len(data),
        "format": fmt or "jpg",
        "dimensions": dims,
        "status": "ok",
    }


def save_frames_from_data_urls(
    json_path: str,
    slug: str,
    start_index: int,
    project_root: str,
) -> dict:
    """Decode base64 data URLs captured via Chrome <video> + <canvas> into raw/screenshots/<slug>/."""
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    out_dir = os.path.join(project_root, "raw", "screenshots", slug)
    os.makedirs(out_dir, exist_ok=True)

    frames = []
    for i, item in enumerate(items):
        idx_num = start_index + i
        sec = float(item.get("timestamp_sec", 0))
        label = item.get("label", "")
        data_url = item.get("data_url", "")
        if "," not in data_url:
            frames.append({
                "index": idx_num,
                "timestamp_sec": sec,
                "mm_ss": format_mm_ss(sec),
                "label": label,
                "status": "failed",
                "error": "Missing base64 comma separator in data_url",
            })
            continue
        raw_bytes = base64.b64decode(data_url.split(",", 1)[1])
        fmt, dims = detect_image_info(raw_bytes)
        ext = fmt or "jpg"
        filename = f"{idx_num:02d}.{ext}"
        dest_path = os.path.join(out_dir, filename)
        with open(dest_path, "wb") as out_f:
            out_f.write(raw_bytes)
        rel_path = os.path.relpath(dest_path, project_root).replace("\\", "/")
        frames.append({
            "index": idx_num,
            "filename": filename,
            "rel_path": rel_path,
            "wiki_link": f"[[{rel_path}]]",
            "md_embed": f"![Slide {idx_num:02d} - {format_mm_ss(sec)}](../screenshots/{slug}/{filename})",
            "timestamp_sec": sec,
            "mm_ss": format_mm_ss(sec),
            "label": label,
            "bytes": len(raw_bytes),
            "format": ext,
            "dimensions": dims,
            "status": "ok",
        })

    failed = [r for r in frames if r["status"] != "ok"]
    return {
        "status": "ok" if not failed else ("partial" if len(failed) < len(frames) else "error"),
        "mode": "data-urls-json",
        "slug": slug,
        "output_dir": os.path.relpath(out_dir, project_root).replace("\\", "/"),
        "total_requested": len(frames),
        "succeeded_count": len(frames) - len(failed),
        "failed_count": len(failed),
        "frames": frames,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Capture 1080p/720p keyframes from YouTube video timestamps or Chrome canvas JSON."
    )
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--slug", required=True, help="Clean kebab-case folder name under raw/screenshots/")
    parser.add_argument(
        "--timestamps",
        default=None,
        help="Comma-separated timestamps, optionally with '=Label' (e.g. '00:35=Intro,02:25=Diagram')",
    )
    parser.add_argument(
        "--auto-chapters",
        action="store_true",
        help="Automatically pick one representative timestamp inside each YouTube chapter",
    )
    parser.add_argument(
        "--from-data-urls-json",
        default=None,
        help="JSON file with [{timestamp_sec, label, data_url}] captured from Chrome <video> canvas",
    )
    parser.add_argument(
        "--upgrade-yt-dlp",
        action="store_true",
        help="Upgrade yt-dlp via pip before resolving stream URLs",
    )
    parser.add_argument("--start-index", type=int, default=1, help="Starting filename index (default: 1)")
    parser.add_argument("--max-height", type=int, default=1080, help="Max video height (default: 1080)")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent ffmpeg workers (default: 4)")
    parser.add_argument("--project-root", default=None, help="Optional project root containing index.md")
    args = parser.parse_args()

    project_root = args.project_root or find_project_root()

    if args.from_data_urls_json:
        report = save_frames_from_data_urls(
            args.from_data_urls_json, args.slug, args.start_index, project_root
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["status"] == "error":
            sys.exit(1)
        return

    if not args.timestamps and not args.auto_chapters:
        print(
            json.dumps({"status": "error", "error": "Provide --timestamps, --auto-chapters, or --from-data-urls-json."}),
            file=sys.stdout,
        )
        sys.exit(1)

    if args.upgrade_yt_dlp:
        upgrade_yt_dlp()
    if not ensure_package("yt_dlp", "yt-dlp"):
        sys.exit(1)
    try:
        ffmpeg_exe = resolve_ffmpeg_exe()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}))
        sys.exit(1)

    out_dir = os.path.join(project_root, "raw", "screenshots", args.slug)
    os.makedirs(out_dir, exist_ok=True)

    def run_stream_attempt():
        print("[1/2] Resolving direct stream & chapters via yt-dlp ...", file=sys.stderr)
        stream_info = extract_stream_and_chapters(args.url, max_height=args.max_height)

        targets = []
        if args.timestamps:
            for raw_tok in args.timestamps.split(","):
                tok = raw_tok.strip()
                if not tok:
                    continue
                sec, label = parse_timestamp_token(tok)
                targets.append({"timestamp_sec": sec, "label": label})
        elif args.auto_chapters:
            chapters = stream_info["chapters"]
            if not chapters:
                dur = float(stream_info["duration"] or 600)
                step = max(30.0, dur / 8.0)
                t = 10.0
                idx = 1
                while t < dur - 5:
                    targets.append({"timestamp_sec": t, "label": f"Sample {idx}"})
                    t += step
                    idx += 1
            else:
                for ch in chapters:
                    start = float(ch.get("start_time", 0))
                    end = float(ch.get("end_time", start + 30))
                    span = max(0.0, end - start)
                    sec = start + min(12.0, max(3.0, span * 0.25))
                    targets.append({"timestamp_sec": sec, "label": ch.get("title", "")})

        headers_str = _build_ffmpeg_headers(stream_info["http_headers"])
        tasks = [
            {
                "index": args.start_index + i,
                "timestamp_sec": t["timestamp_sec"],
                "label": t["label"],
                "out_dir": out_dir,
                "project_root": project_root,
                "slug": args.slug,
                "ffmpeg_exe": ffmpeg_exe,
                "stream_url": stream_info["stream_url"],
                "headers_str": headers_str,
            }
            for i, t in enumerate(targets)
        ]

        print(
            f"[2/2] Capturing {len(tasks)} keyframes at {stream_info['stream_height']}p ({stream_info['stream_ext']}) ...",
            file=sys.stderr,
        )
        probe_first = capture_single_frame(tasks[0])
        frames = [probe_first]
        if probe_first["status"] != "ok" and "403" in probe_first.get("error", ""):
            return stream_info, frames, True

        if len(tasks) > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                for res in pool.map(capture_single_frame, tasks[1:]):
                    frames.append(res)
        return stream_info, frames, False

    stream_info, frames, hit_403 = run_stream_attempt()
    if hit_403 and not args.upgrade_yt_dlp:
        print("[WARN] Hit 403 Forbidden on stream seek; upgrading yt-dlp and retrying once ...", file=sys.stderr)
        if upgrade_yt_dlp():
            stream_info, frames, _ = run_stream_attempt()

    frames.sort(key=lambda r: r["index"])
    failed = [f for f in frames if f["status"] != "ok"]

    report = {
        "status": "ok" if not failed else ("partial" if len(failed) < len(frames) else "error"),
        "mode": "ffmpeg-stream",
        "slug": args.slug,
        "output_dir": os.path.relpath(out_dir, project_root).replace("\\", "/"),
        "stream_height": stream_info["stream_height"],
        "stream_ext": stream_info["stream_ext"],
        "total_requested": len(frames),
        "succeeded_count": len(frames) - len(failed),
        "failed_count": len(failed),
        "frames": frames,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failed and len(failed) == len(frames):
        sys.exit(1)


if __name__ == "__main__":
    main()
