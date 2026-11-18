"""
Deterministic Social & Visual Asset Downloader for wiki-ingest.

Concurrently downloads high-resolution post images (or falls back to local
screenshots) into raw/screenshots/<slug>/ or raw/assets/ using pure Python
standard library modules (zero external dependencies like PIL/requests).

Usage:
    python .agents/skills/wiki-ingest/scripts/download_post_assets.py \
        --slug prompt-engineering-handbook --mode screenshots \
        --urls "https://..." "https://..."
"""

import argparse
import concurrent.futures
import json
import os
import shutil
import struct
import sys
import time
import urllib.request
from datetime import date as dt_date


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def find_project_root(start_dir=None):
    """Walk upward to locate the repository root containing index.md."""
    d = os.path.abspath(start_dir or os.path.dirname(__file__))
    for _ in range(10):
        if os.path.isfile(os.path.join(d, "index.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.getcwd()


def _parse_jpeg_dimensions(data):
    """Scan JPEG SOF markers to extract (width, height) without PIL."""
    idx = 2
    n = len(data)
    sof_markers = {
        0xC0, 0xC1, 0xC2, 0xC3,
        0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB,
        0xCD, 0xCE, 0xCF,
    }
    while idx + 4 < n:
        if data[idx] != 0xFF:
            idx += 1
            continue
        while idx < n and data[idx] == 0xFF:
            idx += 1
        if idx >= n:
            break
        marker = data[idx]
        idx += 1
        if marker in (0xD8, 0xD9, 0x00) or (0xD0 <= marker <= 0xD7):
            continue
        if idx + 2 > n:
            break
        seg_len = struct.unpack(">H", data[idx:idx + 2])[0]
        if marker in sof_markers and idx + 7 <= n:
            height, width = struct.unpack(">HH", data[idx + 3:idx + 7])
            return f"{width}x{height}"
        if seg_len < 2:
            break
        idx += seg_len
    return "unknown"


def _parse_webp_dimensions(data):
    """Extract (width, height) from RIFF WEBP VP8/VP8L/VP8X chunks."""
    if len(data) < 30:
        return "unknown"
    chunk = data[12:16]
    if chunk == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
        w, h = struct.unpack("<HH", data[26:30])
        return f"{w & 0x3FFF}x{h & 0x3FFF}"
    if chunk == b"VP8L" and data[20] == 0x2F:
        bits = struct.unpack("<I", data[21:25])[0]
        w = (bits & 0x3FFF) + 1
        h = ((bits >> 14) & 0x3FFF) + 1
        return f"{w}x{h}"
    if chunk == b"VP8X":
        w = int.from_bytes(data[24:27], "little") + 1
        h = int.from_bytes(data[27:30], "little") + 1
        return f"{w}x{h}"
    return "unknown"


def detect_image_info(data):
    """Detect image format and resolution from raw file header bytes."""
    if len(data) < 12:
        return None, "unknown"
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        w, h = struct.unpack(">II", data[16:24])
        return "png", f"{w}x{h}"
    if data[:3] == b"\xff\xd8\xff":
        return "jpg", _parse_jpeg_dimensions(data)
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        w, h = struct.unpack("<HH", data[6:10])
        return "gif", f"{w}x{h}"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp", _parse_webp_dimensions(data)
    return None, "unknown"


def fetch_url_bytes(url, retries=2, timeout=20):
    """Download URL bytes with retry/backoff and browser User-Agent."""
    last_err = None
    headers = {"User-Agent": USER_AGENT, "Accept": "image/*,*/*;q=0.8"}
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), None
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
            if attempt < retries:
                time.sleep(0.8 * (attempt + 1))
    return None, last_err


def build_target_filename(mode, slug, idx_num, ext):
    """Construct canonical kebab-case filename for screenshots or assets."""
    idx_str = f"{idx_num:02d}"
    if mode == "screenshots":
        return f"{idx_str}.{ext}"
    return f"{slug}-{idx_str}.{ext}"


def build_md_embed(mode, slug, filename, idx_num):
    """Return relative Markdown embed path from raw/articles/<topic>/<slug>.md."""
    if mode == "screenshots":
        return f"![Page {idx_num:02d}](../../screenshots/{slug}/{filename})"
    return f"![Asset {idx_num:02d}](../../assets/{filename})"


def _build_item_result(task, filename, dest_path, byte_count, ext, dims, source_used, url_error=None):
    """Build normalized metadata dict for a successfully acquired asset."""
    rel_path = os.path.relpath(dest_path, task["project_root"]).replace("\\", "/")
    result = {
        "index": task["index"],
        "filename": filename,
        "rel_path": rel_path,
        "wiki_link": f"[[{rel_path}]]",
        "md_embed": build_md_embed(task["mode"], task["slug"], filename, task["index"]),
        "bytes": byte_count,
        "format": ext,
        "dimensions": dims,
        "source_used": source_used,
    }
    if url_error is not None:
        result["url_error"] = url_error
    if task.get("note"):
        result["note"] = task["note"]
    return result


def process_item(task):
    """Download or copy a single asset and return structured metadata."""
    idx_num = task["index"]
    url = task.get("url")
    fallback = task.get("fallback")
    mode = task["mode"]
    slug = task["slug"]
    out_dir = task["out_dir"]
    min_bytes = task["min_bytes"]

    err_msg = None
    if url:
        data, err_msg = fetch_url_bytes(url)
        if data is not None:
            ext, dims = detect_image_info(data)
            if ext and len(data) >= min_bytes:
                filename = build_target_filename(mode, slug, idx_num, ext)
                dest_path = os.path.join(out_dir, filename)
                with open(dest_path, "wb") as f:
                    f.write(data)
                return _build_item_result(task, filename, dest_path, len(data), ext, dims, "url")
            err_msg = f"Invalid or tiny payload ({len(data)} bytes, ext={ext})"

    if fallback and os.path.isfile(fallback):
        with open(fallback, "rb") as f:
            fb_data = f.read()
        ext, dims = detect_image_info(fb_data)
        ext = ext or os.path.splitext(fallback)[1].lstrip(".").lower() or "png"
        filename = build_target_filename(mode, slug, idx_num, ext)
        dest_path = os.path.join(out_dir, filename)
        shutil.copy2(fallback, dest_path)
        return _build_item_result(
            task, filename, dest_path, len(fb_data), ext, dims, "fallback", url_error=err_msg
        )

    return {
        "index": idx_num,
        "source_used": "failed",
        "error": err_msg or "No valid URL or fallback file provided",
    }


def _normalize_manifest_items(manifest):
    """Normalize 'items' (dict or URL string) or flat 'urls'/'fallbacks' arrays into item dicts."""
    raw_items_in = manifest.get("items")
    if raw_items_in:
        normalized = []
        for entry in raw_items_in:
            if isinstance(entry, str):
                normalized.append({"url": entry})
            elif isinstance(entry, dict):
                item = {
                    "url": entry.get("url") or entry.get("src"),
                    "fallback": entry.get("fallback"),
                }
                note = entry.get("note") or entry.get("transcription")
                if note:
                    item["note"] = note
                normalized.append(item)
        return normalized

    urls = manifest.get("urls") or []
    fallbacks = manifest.get("fallbacks") or []
    notes = manifest.get("notes") or []
    count = max(len(urls), len(fallbacks))
    normalized = []
    for i in range(count):
        item = {
            "url": urls[i] if i < len(urls) else None,
            "fallback": fallbacks[i] if i < len(fallbacks) else None,
        }
        if isinstance(notes, list) and i < len(notes) and notes[i]:
            item["note"] = notes[i]
        normalized.append(item)
    return normalized


def load_manifest_or_args(args):
    """Build normalized configuration and item list from --manifest or CLI flags."""
    if args.manifest:
        with open(args.manifest, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        slug = args.slug or manifest.get("slug")
        mode = args.mode or manifest.get("mode", "screenshots")
        start_index = (
            args.start_index
            if args.start_index is not None
            else manifest.get("start_index", 0 if mode == "screenshots" else 1)
        )
        raw_items = _normalize_manifest_items(manifest)
    else:
        slug = args.slug
        mode = args.mode or "screenshots"
        start_index = (
            args.start_index
            if args.start_index is not None
            else (0 if mode == "screenshots" else 1)
        )
        urls = args.urls or []
        fallbacks = args.fallbacks or []
        count = max(len(urls), len(fallbacks))
        raw_items = [
            {
                "url": urls[i] if i < len(urls) else None,
                "fallback": fallbacks[i] if i < len(fallbacks) else None,
            }
            for i in range(count)
        ]

    if not slug:
        raise ValueError("--slug is required (either via CLI or inside --manifest)")
    if mode not in ("screenshots", "assets"):
        raise ValueError("--mode must be 'screenshots' or 'assets'")
    if not raw_items:
        raise ValueError("Provide at least one image via --urls, --fallbacks, or --manifest")

    return slug, mode, start_index, raw_items


def _yaml_escape(text):
    """Escape double quotes and collapse newlines for single-line YAML string values."""
    return str(text).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def extract_raw_meta(args):
    """Merge --raw-* CLI flags and optional --manifest metadata into a raw scaffolding dict."""
    manifest = {}
    if getattr(args, "manifest", None):
        with open(args.manifest, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    return {
        "init_raw": bool(getattr(args, "init_raw", False) or manifest.get("init_raw", False)),
        "raw_subdir": getattr(args, "raw_subdir", None) or manifest.get("raw_subdir") or "ai-other",
        "title": getattr(args, "raw_title", None) or manifest.get("raw_title"),
        "source": getattr(args, "raw_source", None) or manifest.get("raw_source"),
        "original_source": getattr(args, "raw_original_source", None) or manifest.get("raw_original_source"),
        "author": getattr(args, "raw_author", None) or manifest.get("raw_author"),
        "published": getattr(args, "raw_published", None) or manifest.get("raw_published"),
        "created": getattr(args, "raw_created", None) or manifest.get("raw_created") or dt_date.today().strftime("%Y-%m-%d"),
        "description": getattr(args, "raw_description", None) or manifest.get("raw_description"),
        "text": getattr(args, "raw_text", None) or manifest.get("raw_text"),
        "tags": manifest.get("raw_tags") or ["clippings", "visual-guide"],
        "notes": manifest.get("raw_notes") or manifest.get("notes") or [],
    }


def _resolve_slide_note(item, idx, meta_notes):
    """Resolve optional transcription/note text for slide idx without emitting placeholder comments."""
    if item.get("note"):
        return str(item["note"]).strip()
    if item.get("transcription"):
        return str(item["transcription"]).strip()
    if isinstance(meta_notes, list) and idx < len(meta_notes) and meta_notes[idx]:
        return str(meta_notes[idx]).strip()
    if isinstance(meta_notes, dict):
        fname = item.get("filename")
        val = meta_notes.get(fname) or meta_notes.get(str(idx))
        if val:
            return str(val).strip()
    return ""


def scaffold_raw_article(slug, files, project_root, meta):
    """Create raw/articles/<subdir>/<slug>.md with frontmatter, post text, and slide embeds if not already present."""
    subdir = (meta.get("raw_subdir") or "ai-other").strip().strip("/\\")
    raw_dir = os.path.join(project_root, "raw", "articles", subdir)
    raw_path = os.path.join(raw_dir, f"{slug}.md")
    rel_path = os.path.relpath(raw_path, project_root).replace("\\", "/")

    if os.path.isfile(raw_path):
        return rel_path, "skipped_existing"

    os.makedirs(raw_dir, exist_ok=True)

    title = meta.get("title") or slug.replace("-", " ").title()
    source_url = meta.get("source") or ""
    original_source = meta.get("original_source") or ""
    author = meta.get("author") or ""
    published = meta.get("published") or ""
    created = meta.get("created") or dt_date.today().strftime("%Y-%m-%d")
    description = meta.get("description") or f"Visual guide and captured slides for {title}."
    post_text = (meta.get("text") or "").strip()
    tags = meta.get("tags") or ["clippings", "visual-guide"]
    meta_notes = meta.get("notes") or []

    lines = [
        "---",
        f'title: "{_yaml_escape(title)}"',
    ]
    if source_url:
        lines.append(f'source: "{_yaml_escape(source_url)}"')
    if original_source:
        lines.append(f'original_source: "{_yaml_escape(original_source)}"')
    if author:
        author_val = author if author.startswith("[[") else f"[[{author}]]"
        lines.append("author:")
        lines.append(f'  - "{_yaml_escape(author_val)}"')
    if published:
        lines.append(f"published: {published}")
    lines.append(f"created: {created}")
    lines.append(f'description: "{_yaml_escape(description)}"')
    lines.append("tags:")
    for t in tags:
        lines.append(f'  - "{_yaml_escape(t)}"')
    lines.extend([
        "---",
        "",
        f"# {title}",
        "",
    ])
    if source_url:
        lines.append(f"- **Nguồn bài viết:** {source_url}")
    if published:
        lines.append(f"- **Thời gian đăng:** {published}")
    if original_source:
        lines.append(f"- **Nguồn gốc tiếng Anh được tác giả trích dẫn:** {original_source}")

    ok_files = [f for f in files if f.get("source_used") != "failed"]
    lines.append(f"- **Thư mục hình ảnh gốc ({len(ok_files)} trang):** `raw/screenshots/{slug}/`")
    lines.extend(["", "---", ""])

    if post_text:
        lines.append("## Nội Dung Nguyên Văn Bài Đăng")
        lines.append("")
        for p_line in post_text.splitlines():
            lines.append(f"> {p_line}" if p_line.strip() else ">")
        lines.extend(["", "---", ""])

    section_heading = (
        f"## Thư Viện {len(ok_files)} Trang Hình Ảnh Đính Kèm"
        if not meta_notes and not any(f.get("note") or f.get("transcription") for f in ok_files)
        else f"## Chi Tiết {len(ok_files)} Trang Hình Ảnh Đính Kèm (Visual Transcription)"
    )
    lines.append(section_heading)
    lines.append("")
    for i, item in enumerate(ok_files):
        filename = item["filename"]
        dims = item.get("dimensions", "")
        dims_note = f" *({dims})*" if dims and dims != "unknown" else ""
        if item.get("md_embed") and str(item["md_embed"]).startswith("![Asset"):
            embed = item["md_embed"]
        else:
            embed = f"![Trang {i + 1}](../../screenshots/{slug}/{filename})"
        lines.extend([
            f"### Trang {i + 1} / {len(ok_files)}{dims_note}",
            embed,
            "",
        ])
        note_text = _resolve_slide_note(item, i, meta_notes)
        if note_text:
            lines.extend([note_text, ""])

    with open(raw_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return rel_path, "created"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Download social post images concurrently into raw/screenshots or raw/assets."
    )
    parser.add_argument("--slug", help="Clean kebab-case slug (e.g. prompt-engineering-handbook)")
    parser.add_argument(
        "--mode",
        choices=["screenshots", "assets"],
        default=None,
        help="Target storage mode: 'screenshots' (default) or 'assets'",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=None,
        help="Starting index number (default: 0 for screenshots, 1 for assets)",
    )
    parser.add_argument("--urls", nargs="*", help="Ordered list of direct image URLs")
    parser.add_argument("--fallbacks", nargs="*", help="Ordered list of local screenshot fallback paths")
    parser.add_argument("--manifest", help="Optional JSON manifest file defining slug, mode, and items")
    parser.add_argument("--project-root", help="Optional project root path containing index.md")
    parser.add_argument("--min-bytes", type=int, default=5000, help="Minimum valid image payload bytes")
    parser.add_argument("--workers", type=int, default=6, help="Concurrent download worker count")
    parser.add_argument("--init-raw", action="store_true", help="Scaffold raw/articles/<subdir>/<slug>.md if not yet created")
    parser.add_argument("--raw-subdir", default=None, help="Subdirectory under raw/articles/ for --init-raw (default: ai-other)")
    parser.add_argument("--raw-title", default=None, help="Title for scaffolded raw article")
    parser.add_argument("--raw-source", default=None, help="Source URL for scaffolded raw article")
    parser.add_argument("--raw-original-source", default=None, help="Original cited URL for scaffolded raw article")
    parser.add_argument("--raw-author", default=None, help="Author entity name for scaffolded raw article")
    parser.add_argument("--raw-published", default=None, help="Published date/timestamp string for scaffolded raw article")
    parser.add_argument("--raw-created", default=None, help="YYYY-MM-DD creation date (default: today)")
    parser.add_argument("--raw-description", default=None, help="Description field for scaffolded raw article")
    parser.add_argument("--raw-text", default=None, help="Verbatim post text for scaffolded raw article")
    args = parser.parse_args()

    try:
        slug, mode, start_index, raw_items = load_manifest_or_args(args)
        raw_meta = extract_raw_meta(args)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    project_root = args.project_root or find_project_root()
    if mode == "screenshots":
        out_dir = os.path.join(project_root, "raw", "screenshots", slug)
    else:
        out_dir = os.path.join(project_root, "raw", "assets")
    os.makedirs(out_dir, exist_ok=True)

    tasks = [
        {
            "index": start_index + i,
            "url": item.get("url"),
            "fallback": item.get("fallback"),
            "note": item.get("note"),
            "mode": mode,
            "slug": slug,
            "out_dir": out_dir,
            "project_root": project_root,
            "min_bytes": args.min_bytes,
        }
        for i, item in enumerate(raw_items)
    ]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for res in pool.map(process_item, tasks):
            results.append(res)

    results.sort(key=lambda r: r["index"])
    failed = [r for r in results if r["source_used"] == "failed"]

    report = {
        "status": "ok" if not failed else "partial",
        "slug": slug,
        "mode": mode,
        "output_dir": os.path.relpath(out_dir, project_root).replace("\\", "/"),
        "total_requested": len(tasks),
        "succeeded_count": len(tasks) - len(failed),
        "failed_count": len(failed),
        "files": results,
    }
    if raw_meta.get("init_raw") and len(failed) < len(tasks):
        scaffold_path, scaffold_status = scaffold_raw_article(slug, results, project_root, raw_meta)
        report["raw_scaffold_path"] = scaffold_path
        report["raw_scaffold_status"] = scaffold_status
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failed and len(failed) == len(tasks):
        sys.exit(1)


if __name__ == "__main__":
    main()
