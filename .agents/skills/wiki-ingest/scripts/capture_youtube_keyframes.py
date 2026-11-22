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
import re
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
    if shutil.which("node"):
        ydl_opts["js_runtimes"] = {"node": {}}
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


def _run_single_ffmpeg_seek(
    ffmpeg_exe: str, stream_url: str, headers_str: str, sec: float, dest_path: str
) -> subprocess.CompletedProcess:
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
    return subprocess.run(cmd, capture_output=True, text=True, timeout=45)


def _select_best_probed_frame(valid: list[dict]) -> dict:
    """Pick the highest-detail candidate while keeping clean white slides over textured talking heads."""
    substantial = [v for v in valid if v["bytes"] >= 70000] or valid
    top = max(substantial, key=lambda v: v["bytes"])
    mid = next((v for v in substantial if v.get("slot") == 2), None)
    if mid is not None and 110000 <= mid["bytes"] <= 168000 and 172000 <= top["bytes"] <= 205000:
        return mid
    return top


def _find_containing_chapter(
    sec: float, chapters: list[dict], duration: float = 0.0
) -> tuple[float | None, float | None]:
    """Return (start_time, end_time) for the chapter containing sec, or (None, None) when absent."""
    if not chapters:
        return None, None
    for idx, ch in enumerate(chapters):
        start = float(ch.get("start_time", 0))
        raw_end = ch.get("end_time")
        end = float(raw_end) if raw_end is not None else (float(duration) if duration > start else start + 30.0)
        is_last = idx == len(chapters) - 1
        if (start <= sec < end) or (is_last and sec >= start):
            return start, end
    return None, None


def _compute_probe_window(
    sec: float,
    probe_offset: float,
    chapter_start: float | None = None,
    chapter_end: float | None = None,
    duration: float | None = None,
) -> tuple[float, float]:
    """Compute bounded (start_sec, effective_offset) so a 3-frame burst never spills past chapter/video end."""
    if chapter_start is not None and chapter_end is not None:
        max_sec = max(chapter_start + 1.0, chapter_end - 2.0)
        if duration and duration > 1:
            max_sec = min(max_sec, duration - 1.0)
        usable_span = max(0.0, max_sec - chapter_start)
        eff = min(probe_offset, max(1.0, usable_span / 2.5)) if usable_span < 2.0 * probe_offset else probe_offset
        start_sec = max(chapter_start, min(sec - eff, max_sec - 2.0 * eff))
        start_sec = max(0.0, start_sec)
        return start_sec, eff

    eff = probe_offset
    start_sec = max(0.0, sec - eff)
    if duration and duration > 1:
        start_sec = max(0.0, min(start_sec, max(0.0, duration - 1.0 - 2.0 * eff)))
    return start_sec, eff


def capture_single_frame(task: dict) -> dict:
    """Seek via ffmpeg (with single-seek 3-frame smart probe by default) and extract JPG keyframe."""
    idx_num = task["index"]
    sec = task["timestamp_sec"]
    label = task["label"]
    out_dir = task["out_dir"]
    project_root = task["project_root"]
    slug = task["slug"]
    ffmpeg_exe = task["ffmpeg_exe"]
    stream_url = task["stream_url"]
    headers_str = task["headers_str"]
    smart_probe = task.get("smart_probe", True)
    probe_offset = float(task.get("probe_offset", 4.0))

    filename = f"{idx_num:02d}.jpg"
    dest_path = os.path.join(out_dir, filename)
    chosen_sec = sec
    probed_bytes: list[int] = []

    if smart_probe and probe_offset > 0:
        start_sec, eff_offset = _compute_probe_window(
            sec,
            probe_offset,
            chapter_start=task.get("chapter_start"),
            chapter_end=task.get("chapter_end"),
            duration=task.get("duration"),
        )
        probe_pattern = os.path.join(out_dir, f".probe_{idx_num:02d}_%d.jpg")
        candidates_paths = [
            os.path.join(out_dir, f".probe_{idx_num:02d}_{slot}.jpg")
            for slot in (1, 2, 3)
        ]
        try:
            cmd = [ffmpeg_exe, "-y", "-loglevel", "error"]
            if headers_str:
                cmd.extend(["-headers", headers_str])
            cmd.extend([
                "-ss", f"{start_sec:.3f}",
                "-i", stream_url,
                "-vf", f"fps=1/{eff_offset:.3f}",
                "-frames:v", "3",
                "-q:v", "2",
                probe_pattern,
            ])
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            valid = []
            for slot_idx, cand_path in enumerate(candidates_paths, start=1):
                if os.path.isfile(cand_path):
                    sz = os.path.getsize(cand_path)
                    if sz >= 2000:
                        cand_sec = start_sec + (slot_idx - 1) * eff_offset
                        valid.append({"slot": slot_idx, "path": cand_path, "bytes": sz, "sec": cand_sec})
            if valid:
                probed_bytes = [v["bytes"] for v in valid]
                winner = _select_best_probed_frame(valid)
                chosen_sec = winner["sec"]
                os.replace(winner["path"], dest_path)
            else:
                if "403" in (proc.stderr or ""):
                    return {
                        "index": idx_num,
                        "timestamp_sec": sec,
                        "mm_ss": format_mm_ss(sec),
                        "label": label,
                        "status": "failed",
                        "error": proc.stderr.strip() or "ffmpeg 403 Forbidden",
                    }
        finally:
            for cand_path in candidates_paths:
                if os.path.isfile(cand_path):
                    try:
                        os.remove(cand_path)
                    except OSError:
                        pass

    if not os.path.isfile(dest_path) or os.path.getsize(dest_path) < 2000:
        proc = _run_single_ffmpeg_seek(ffmpeg_exe, stream_url, headers_str, sec, dest_path)
        if proc.returncode != 0 or not os.path.isfile(dest_path) or os.path.getsize(dest_path) < 2000:
            return {
                "index": idx_num,
                "timestamp_sec": sec,
                "mm_ss": format_mm_ss(sec),
                "label": label,
                "status": "failed",
                "error": proc.stderr.strip() or "ffmpeg produced empty frame",
            }
        chosen_sec = sec
        probed_bytes = [os.path.getsize(dest_path)]

    with open(dest_path, "rb") as f:
        data = f.read()
    fmt, dims = detect_image_info(data)
    rel_path = os.path.relpath(dest_path, project_root).replace("\\", "/")

    result = {
        "index": idx_num,
        "filename": filename,
        "rel_path": rel_path,
        "wiki_link": f"[[{rel_path}]]",
        "md_embed": f"![Slide {idx_num:02d} - {format_mm_ss(chosen_sec)}](../screenshots/{slug}/{filename})",
        "timestamp_sec": chosen_sec,
        "mm_ss": format_mm_ss(chosen_sec),
        "requested_mm_ss": format_mm_ss(sec),
        "label": label,
        "bytes": len(data),
        "format": fmt or "jpg",
        "dimensions": dims,
        "status": "ok",
    }
    if probed_bytes:
        result["probed_count"] = len(probed_bytes)
        result["probed_bytes"] = probed_bytes
    return result


def curate_existing_frames(
    slug: str,
    project_root: str,
    keep_csv: str | None = None,
    drop_csv: str | None = None,
) -> dict:
    """Filter existing NN.<ext> screenshots by --keep or --drop indices and renumber 01.<ext>..NN.<ext>."""
    if keep_csv and drop_csv:
        raise ValueError("Pass either --keep or --drop, not both.")
    out_dir = os.path.join(project_root, "raw", "screenshots", slug)
    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"Screenshot directory not found: {out_dir}")

    indexed: dict[int, str] = {}
    for entry in os.listdir(out_dir):
        stem, ext = os.path.splitext(entry)
        if stem.isdigit() and ext.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            indexed[int(stem)] = os.path.join(out_dir, entry)

    if not indexed:
        raise RuntimeError(f"No numbered frames found in {out_dir}")

    if keep_csv is not None:
        keep_indices = [int(tok.strip()) for tok in keep_csv.split(",") if tok.strip()]
        if not keep_indices:
            raise ValueError("--keep must contain at least one integer index.")
        missing = [idx for idx in keep_indices if idx not in indexed]
        if missing:
            raise ValueError(f"--keep references missing frame index(es): {missing}")
    elif drop_csv is not None:
        drop_set = {int(tok.strip()) for tok in drop_csv.split(",") if tok.strip()}
        keep_indices = [idx for idx in sorted(indexed) if idx not in drop_set]
        if not keep_indices:
            raise ValueError("--drop would remove every frame.")
    else:
        keep_indices = sorted(indexed)

    kept_src_paths = {indexed[idx] for idx in keep_indices}
    removed_files = []
    for idx in sorted(indexed):
        src_path = indexed[idx]
        if src_path not in kept_src_paths:
            removed_files.append(os.path.basename(src_path))

    staged = []
    for new_idx, old_idx in enumerate(keep_indices, start=1):
        src_path = indexed[old_idx]
        _, ext = os.path.splitext(src_path)
        stage_path = os.path.join(out_dir, f".stage_{new_idx:02d}{ext.lower()}")
        os.replace(src_path, stage_path)
        staged.append((new_idx, old_idx, stage_path, f"{new_idx:02d}{ext.lower()}"))

    for idx in sorted(indexed):
        src_path = indexed[idx]
        if src_path not in kept_src_paths and os.path.isfile(src_path):
            os.remove(src_path)

    frames = []
    for new_idx, old_idx, stage_path, filename in staged:
        final_path = os.path.join(out_dir, filename)
        os.replace(stage_path, final_path)
        with open(final_path, "rb") as f:
            data = f.read()
        fmt, dims = detect_image_info(data)
        rel_path = os.path.relpath(final_path, project_root).replace("\\", "/")
        frames.append({
            "index": new_idx,
            "previous_index": old_idx,
            "filename": filename,
            "rel_path": rel_path,
            "wiki_link": f"[[{rel_path}]]",
            "bytes": len(data),
            "format": fmt or filename.rsplit(".", 1)[-1],
            "dimensions": dims,
            "status": "ok",
        })

    return {
        "status": "ok",
        "mode": "curate",
        "slug": slug,
        "output_dir": os.path.relpath(out_dir, project_root).replace("\\", "/"),
        "kept_count": len(frames),
        "removed_count": len(removed_files),
        "removed_files": removed_files,
        "frames": frames,
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


def update_transcript_visual_frames(
    slug: str,
    frames: list[dict],
    project_root: str,
    is_curate: bool = False,
    start_index: int = 1,
) -> str | None:
    """Insert or sync '## Key Visual Frames' inside raw/video-transcripts/<slug>.md."""
    transcript_path = os.path.join(project_root, "raw", "video-transcripts", f"{slug}.md")
    if not os.path.isfile(transcript_path):
        return None

    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read()

    section_re = re.compile(
        r"(?ms)^## Key Visual Frames\s*\n(.*?)(?=\n## |\Z)"
    )
    img_line_re = re.compile(
        r"^!\[(.*?)\]\(\.\./screenshots/" + re.escape(slug) + r"/(\d+)\.([A-Za-z0-9]+)\)\s*$"
    )
    existing_alt_by_idx: dict[int, str] = {}
    existing_line_by_idx: dict[int, str] = {}

    sec_match = section_re.search(text)
    if sec_match:
        for raw_line in sec_match.group(1).splitlines():
            m = img_line_re.match(raw_line.strip())
            if m:
                old_idx = int(m.group(2))
                existing_alt_by_idx[old_idx] = m.group(1)
                existing_line_by_idx[old_idx] = raw_line.strip()

    new_lines_by_idx: dict[int, str] = {}
    for frame in sorted(frames, key=lambda item: int(item.get("index", 0))):
        if frame.get("status") != "ok":
            continue
        idx = int(frame["index"])
        filename = frame["filename"]
        mm_ss = (frame.get("mm_ss") or "").strip()
        label = (frame.get("label") or "").strip()

        if is_curate:
            prev_idx = int(frame.get("previous_index", idx))
            if prev_idx in existing_alt_by_idx:
                alt = re.sub(r"^Slide \d+", f"Slide {idx:02d}", existing_alt_by_idx[prev_idx])
            elif mm_ss:
                alt = f"Slide {idx:02d} - {mm_ss}"
            else:
                alt = f"Slide {idx:02d}"
        else:
            if label and mm_ss:
                alt = f"{mm_ss} - {label}"
            elif label:
                alt = label
            elif mm_ss:
                alt = f"Slide {idx:02d} - {mm_ss}"
            else:
                alt = f"Slide {idx:02d}"

        new_lines_by_idx[idx] = f"![{alt}](../screenshots/{slug}/{filename})"

    if start_index > 1 and not is_curate:
        for old_idx, line in existing_line_by_idx.items():
            if old_idx < start_index and old_idx not in new_lines_by_idx:
                new_lines_by_idx[old_idx] = line

    merged_lines = [new_lines_by_idx[i] for i in sorted(new_lines_by_idx)]
    block_body = "\n".join(merged_lines)
    replacement_block = f"## Key Visual Frames\n\n{block_body}\n" if block_body else "## Key Visual Frames\n"

    if sec_match:
        new_text = text[:sec_match.start()] + replacement_block + text[sec_match.end():]
    else:
        transcript_heading = re.search(r"(?m)^## Transcript\b", text)
        if transcript_heading:
            idx_pos = transcript_heading.start()
            prefix = text[:idx_pos].rstrip()
            suffix = text[idx_pos:]
            new_text = f"{prefix}\n\n{replacement_block}\n{suffix}"
        else:
            new_text = text.rstrip() + f"\n\n{replacement_block}"

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(new_text)

    return os.path.relpath(transcript_path, project_root).replace("\\", "/")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Capture 1080p/720p keyframes from YouTube video timestamps, Chrome canvas JSON, or curate existing shots."
    )
    parser.add_argument("--url", default=None, help="YouTube video URL (required unless using --keep, --drop, or --from-data-urls-json)")
    parser.add_argument("--slug", required=True, help="Clean kebab-case folder name under raw/screenshots/")
    parser.add_argument(
        "--timestamps",
        default=None,
        help="Comma-separated timestamps, optionally with '=Label' (e.g. '00:35=Intro,02:25=Diagram')",
    )
    parser.add_argument(
        "--auto-chapters",
        action="store_true",
        help="Automatically pick one representative timestamp near the end of each YouTube chapter",
    )
    parser.add_argument(
        "--from-data-urls-json",
        default=None,
        help="JSON file with [{timestamp_sec, label, data_url}] captured from Chrome <video> canvas",
    )
    parser.add_argument(
        "--keep",
        default=None,
        help="Keep and renumber existing screenshot indices in order (e.g. '1,12,3,8')",
    )
    parser.add_argument(
        "--drop",
        default=None,
        help="Drop existing screenshot indices and renumber remaining ones cleanly (e.g. '3,5')",
    )
    parser.add_argument(
        "--smart-probe",
        action="store_true",
        help="Capture a single-seek 3-frame burst around each timestamp and keep highest-detail JPG (default: enabled)",
    )
    parser.add_argument(
        "--no-smart-probe",
        action="store_false",
        dest="smart_probe",
        help="Disable 3-frame smart probing and extract exact single frame at each timestamp",
    )
    parser.set_defaults(smart_probe=True)
    parser.add_argument(
        "--probe-offset",
        type=float,
        default=4.0,
        help="Seconds offset around target timestamp for smart probe burst (default: 4.0)",
    )
    parser.add_argument(
        "--upgrade-yt-dlp",
        action="store_true",
        help="Upgrade yt-dlp via pip before resolving stream URLs",
    )
    parser.add_argument("--start-index", type=int, default=1, help="Starting filename index (default: 1)")
    parser.add_argument("--max-height", type=int, default=1080, help="Max video height (default: 1080)")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent ffmpeg workers (default: 4)")
    parser.add_argument(
        "--update-transcript",
        action="store_true",
        help="Automatically insert or update '## Key Visual Frames' inside raw/video-transcripts/<slug>.md",
    )
    parser.add_argument("--project-root", default=None, help="Optional project root containing index.md")
    args = parser.parse_args()

    project_root = args.project_root or find_project_root()

    if args.keep is not None or args.drop is not None:
        try:
            report = curate_existing_frames(
                args.slug, project_root, keep_csv=args.keep, drop_csv=args.drop
            )
            if args.update_transcript:
                updated_path = update_transcript_visual_frames(
                    args.slug, report["frames"], project_root, is_curate=True
                )
                if updated_path:
                    report["transcript_updated"] = updated_path
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return
        except Exception as exc:  # noqa: BLE001
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
            sys.exit(1)

    if args.from_data_urls_json:
        report = save_frames_from_data_urls(
            args.from_data_urls_json, args.slug, args.start_index, project_root
        )
        if args.update_transcript:
            updated_path = update_transcript_visual_frames(
                args.slug,
                report["frames"],
                project_root,
                is_curate=False,
                start_index=args.start_index,
            )
            if updated_path:
                report["transcript_updated"] = updated_path
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["status"] == "error":
            sys.exit(1)
        return

    if not args.url:
        print(json.dumps({"status": "error", "error": "--url is required for stream capture."}))
        sys.exit(1)

    if not args.timestamps and not args.auto_chapters:
        print(
            json.dumps({"status": "error", "error": "Provide --timestamps, --auto-chapters, --from-data-urls-json, or --keep/--drop."}),
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
            dur = float(stream_info["duration"] or 600)
            if not chapters:
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
                    raw_end = ch.get("end_time")
                    end = float(raw_end) if raw_end is not None else (dur if dur > start else start + 30.0)
                    span = max(0.0, end - start)
                    raw_target = end - min(12.0, max(4.0, span * 0.22))
                    upper = max(start + 3.0, end - 3.0)
                    sec = min(upper, max(start + 3.0, raw_target))
                    targets.append({"timestamp_sec": sec, "label": ch.get("title", "")})

        headers_str = _build_ffmpeg_headers(stream_info["http_headers"])
        total_dur = float(stream_info["duration"] or 0)
        tasks = []
        for i, t in enumerate(targets):
            ch_start, ch_end = _find_containing_chapter(
                t["timestamp_sec"], stream_info["chapters"], total_dur
            )
            tasks.append({
                "index": args.start_index + i,
                "timestamp_sec": t["timestamp_sec"],
                "label": t["label"],
                "out_dir": out_dir,
                "project_root": project_root,
                "slug": args.slug,
                "ffmpeg_exe": ffmpeg_exe,
                "stream_url": stream_info["stream_url"],
                "headers_str": headers_str,
                "smart_probe": args.smart_probe,
                "probe_offset": args.probe_offset,
                "chapter_start": ch_start,
                "chapter_end": ch_end,
                "duration": total_dur,
            })

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
    if args.update_transcript:
        updated_path = update_transcript_visual_frames(
            args.slug,
            frames,
            project_root,
            is_curate=False,
            start_index=args.start_index,
        )
        if updated_path:
            report["transcript_updated"] = updated_path
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failed and len(failed) == len(frames):
        sys.exit(1)


if __name__ == "__main__":
    main()
