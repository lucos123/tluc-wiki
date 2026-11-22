"""
Deterministic Social & Web Asset Downloader for wiki-ingest (v4.4).

Concurrently downloads high-resolution post/article images (or archives local/uploaded
images with SHA-256 duplicate detection) into raw/screenshots/<slug>/ or raw/assets/
using pure Python standard library modules (zero external dependencies like PIL/requests).

Supports Zero-URL-Relay parsing from Chrome DevTools `steps/<N>/output.txt`
(`--from-harvest-file`), Local/Uploaded image ingestion (`--local-files`),
Cover-First probing (`--probe-cover`), Auto storage routing
(`--mode auto`: 1-3 -> assets, >=4 -> screenshots), non-AVIF content negotiation,
automatic domain-matched Referer fallback on HTTP 401/403, paywall metadata capture,
and multi-author YAML normalization.

Usage:
    python .agents/skills/wiki-ingest/scripts/download_post_assets.py \
        --slug transformers-detailed-notes --mode auto \
        --from-harvest-file "C:\\...\\steps\\6\\output.txt"
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import struct
import sys
import time
import urllib.error
import urllib.request
from datetime import date as dt_date
from urllib.parse import urlparse


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
# Explicitly request formats supported by pure-Python header detection & multimodal read_file
# (avoids Cloudflare/Substack/IG CDNs negotiating image/avif).
ACCEPT_IMAGE_HEADER = "image/webp,image/png,image/jpeg,image/gif;q=0.9,*/*;q=0.1"
STDOUT_TEXT_PREVIEW_LIMIT = 1200


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


def _infer_referer(url):
    """Return a domain-matched Referer header to satisfy CDN anti-hotlink checks."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    # Check Instagram before fbcdn.net because IG CDN URLs use *.fna.fbcdn.net
    if "instagram" in host or "cdninstagram" in host:
        return "https://www.instagram.com/"
    if "fbcdn" in host or "facebook" in host or "fbsbx" in host:
        return "https://www.facebook.com/"
    if "licdn" in host or "linkedin" in host:
        return "https://www.linkedin.com/"
    if "twimg" in host or "twitter" in host or host == "x.com" or host.endswith(".x.com"):
        return "https://x.com/"
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}/"
    return None


def _safe_relpath(path, base_dir):
    """Compute forward-slash relative path, falling back to absolute path across drives."""
    try:
        return os.path.relpath(path, base_dir).replace("\\", "/")
    except ValueError:
        return os.path.abspath(path).replace("\\", "/")


def fetch_url_bytes(url, retries=2, timeout=20):
    """Download URL bytes with retry/backoff, non-AVIF Accept header, and 401/403 Referer fallback."""
    last_err = None
    headers = {"User-Agent": USER_AGENT, "Accept": ACCEPT_IMAGE_HEADER}
    referer_tried = False
    attempt = 0
    while attempt <= retries:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), None
        except urllib.error.HTTPError as exc:
            last_err = str(exc)
            if exc.code in (401, 403) and not referer_tried:
                referer = _infer_referer(url)
                if referer:
                    headers["Referer"] = referer
                    referer_tried = True
                    continue
            if attempt < retries:
                time.sleep(0.8 * (attempt + 1))
            attempt += 1
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
            if attempt < retries:
                time.sleep(0.8 * (attempt + 1))
            attempt += 1
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


def _find_existing_raw_image_by_sha256(digest, project_root):
    """Return relative path of first byte-identical image in raw/assets/ or raw/screenshots/, or None."""
    if not digest or not project_root:
        return None
    for sub in ("assets", "screenshots"):
        base_dir = os.path.join(project_root, "raw", sub)
        if not os.path.isdir(base_dir):
            continue
        for root_dir, _, filenames in os.walk(base_dir):
            for fname in sorted(filenames):
                fpath = os.path.join(root_dir, fname)
                try:
                    h = hashlib.sha256()
                    with open(fpath, "rb") as f:
                        for chunk in iter(lambda: f.read(65536), b""):
                            h.update(chunk)
                    if h.hexdigest() == digest:
                        return _safe_relpath(fpath, project_root)
                except OSError:
                    continue
    return None


def _build_item_result(
    task,
    filename,
    dest_path,
    byte_count,
    ext,
    dims,
    source_used,
    url_error=None,
    sha256=None,
    duplicate_of=None,
):
    """Build normalized metadata dict for a successfully acquired asset."""
    rel_path = _safe_relpath(dest_path, task["project_root"])
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
    if sha256:
        result["sha256"] = sha256[:12]
    if duplicate_of:
        result["duplicate_existing_path"] = duplicate_of
    if url_error is not None:
        result["url_error"] = url_error
    if task.get("note"):
        result["note"] = task["note"]
    return result


def process_item(task):
    """Download or copy a single asset and return structured metadata."""
    idx_num = task["index"]
    local_file = task.get("local_file")
    url = task.get("url")
    fallback = task.get("fallback")
    mode = task["mode"]
    slug = task["slug"]
    out_dir = task["out_dir"]
    min_bytes = task["min_bytes"]
    explicit_dest = task.get("explicit_dest_path")

    def resolve_dest(ext_val):
        if explicit_dest:
            os.makedirs(os.path.dirname(os.path.abspath(explicit_dest)), exist_ok=True)
            return os.path.basename(explicit_dest), os.path.abspath(explicit_dest)
        fname = build_target_filename(mode, slug, idx_num, ext_val)
        return fname, os.path.join(out_dir, fname)

    if local_file:
        if os.path.isfile(local_file):
            with open(local_file, "rb") as f:
                local_data = f.read()
            digest = hashlib.sha256(local_data).hexdigest()
            ext, dims = detect_image_info(local_data)
            ext = ext or os.path.splitext(local_file)[1].lstrip(".").lower() or "png"
            dup = (
                None
                if task.get("skip_dup_check")
                else _find_existing_raw_image_by_sha256(digest, task["project_root"])
            )
            filename, dest_path = resolve_dest(ext)
            if os.path.abspath(local_file) != os.path.abspath(dest_path):
                shutil.copy2(local_file, dest_path)
            return _build_item_result(
                task,
                filename,
                dest_path,
                len(local_data),
                ext,
                dims,
                "local",
                sha256=digest,
                duplicate_of=dup,
            )
        return {
            "index": idx_num,
            "source_used": "failed",
            "error": f"Local image file not found: {local_file}",
        }

    err_msg = None
    if url:
        data, err_msg = fetch_url_bytes(url)
        if data is not None:
            ext, dims = detect_image_info(data)
            if ext and len(data) >= min_bytes:
                filename, dest_path = resolve_dest(ext)
                with open(dest_path, "wb") as f:
                    f.write(data)
                return _build_item_result(task, filename, dest_path, len(data), ext, dims, "url")
            err_msg = f"Invalid or tiny payload ({len(data)} bytes, ext={ext})"

    if fallback and os.path.isfile(fallback):
        with open(fallback, "rb") as f:
            fb_data = f.read()
        ext, dims = detect_image_info(fb_data)
        ext = ext or os.path.splitext(fallback)[1].lstrip(".").lower() or "png"
        filename, dest_path = resolve_dest(ext)
        shutil.copy2(fallback, dest_path)
        return _build_item_result(
            task, filename, dest_path, len(fb_data), ext, dims, "fallback", url_error=err_msg
        )

    return {
        "index": idx_num,
        "source_used": "failed",
        "error": err_msg or "No valid URL or fallback file provided",
    }


def _extract_json_payload(raw_text):
    """Extract JSON dict/list from raw JSON or Chrome DevTools evaluate_script output.txt."""
    text = raw_text.strip()
    if not text:
        raise ValueError("Harvest file is empty")

    fences = re.findall(r"```(?:json)?\s*([\s\S]*?)\s*```", text, flags=re.IGNORECASE)
    for block in reversed(fences):
        candidate = block.strip()
        if candidate.startswith(("{", "[")):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

    if text.startswith(("{", "[")):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch in ("{", "["):
            try:
                obj, _ = decoder.raw_decode(text, i)
                return obj
            except json.JSONDecodeError:
                continue

    raise ValueError("Could not locate valid JSON payload in harvest file")


def parse_harvest_file(path):
    """Load Chrome DevTools steps/<N>/output.txt or JSON harvest payload and full metadata."""
    with open(path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    payload = _extract_json_payload(raw_text)
    if isinstance(payload, list):
        payload = {"slides": payload}
    elif not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in harvest file, got {type(payload).__name__}")

    meta = {
        "platform": payload.get("platform"),
        "status": payload.get("status"),
        "paywalled": True if payload.get("paywalled") else None,
        "title": payload.get("title"),
        "url": payload.get("canonical_url") or payload.get("url"),
        "author": payload.get("author"),
        "author_headline": payload.get("author_headline"),
        "handle": payload.get("handle"),
        "co_authors": payload.get("co_authors") or [],
        "published": payload.get("published"),
        "text": payload.get("text") or payload.get("sidebar_text") or "",
        "comments": payload.get("comments") or [],
        "external_links": payload.get("external_links") or [],
        "videos_found": payload.get("videos_found") or [],
        "document_iframe_url": payload.get("document_iframe_url"),
        "first_photo_href": payload.get("first_photo_href"),
        "engagement": payload.get("engagement"),
    }
    clean_meta = {k: v for k, v in meta.items() if v not in (None, [], "", {})}
    return payload, clean_meta


def summarize_harvest_meta_for_stdout(harvest_meta, full_meta=False):
    """Keep CLI stdout token-efficient by truncating very long article bodies unless --full-meta is set."""
    if not harvest_meta:
        return None
    out = dict(harvest_meta)
    text = out.get("text")
    if isinstance(text, str) and not full_meta and len(text) > STDOUT_TEXT_PREVIEW_LIMIT + 300:
        out["text_length"] = len(text)
        out["text_truncated"] = True
        out["text_preview"] = text[:STDOUT_TEXT_PREVIEW_LIMIT].rstrip() + "..."
        del out["text"]
    return out


def resolve_storage_mode(requested_mode, item_count):
    """Resolve 'auto' storage mode (1-3 -> assets, >=4 -> screenshots)."""
    mode = (requested_mode or "screenshots").lower()
    if mode == "auto":
        return "assets" if 1 <= item_count <= 3 else "screenshots"
    if mode not in ("screenshots", "assets"):
        raise ValueError("--mode must be 'screenshots', 'assets', or 'auto'")
    return mode


def _normalize_manifest_items(manifest):
    """Normalize 'items', 'slides', 'results', or flat 'urls'/'fallbacks'/'local_files' arrays into item dicts."""
    raw_items_in = manifest.get("items") or manifest.get("slides") or manifest.get("results")
    if raw_items_in:
        normalized = []
        for entry in raw_items_in:
            if isinstance(entry, str) and entry.strip():
                normalized.append({"url": entry.strip()})
            elif isinstance(entry, dict):
                url = entry.get("url") or entry.get("src")
                fallback = entry.get("fallback")
                local_file = entry.get("local_file")
                if not url and not fallback and not local_file:
                    continue
                item = {
                    "url": url,
                    "fallback": fallback,
                }
                if local_file:
                    item["local_file"] = local_file
                note = entry.get("note") or entry.get("transcription")
                if note:
                    item["note"] = note
                normalized.append(item)
        return normalized

    local_files = manifest.get("local_files") or []
    if local_files:
        notes = manifest.get("notes") or []
        normalized = []
        for i, lf in enumerate(local_files):
            if not lf:
                continue
            item = {"local_file": lf}
            if isinstance(notes, list) and i < len(notes) and notes[i]:
                item["note"] = notes[i]
            normalized.append(item)
        return normalized

    urls = manifest.get("urls") or []
    fallbacks = manifest.get("fallbacks") or []
    notes = manifest.get("notes") or []
    count = max(len(urls), len(fallbacks))
    normalized = []
    for i in range(count):
        url = urls[i] if i < len(urls) else None
        fallback = fallbacks[i] if i < len(fallbacks) else None
        if not url and not fallback:
            continue
        item = {
            "url": url,
            "fallback": fallback,
        }
        if isinstance(notes, list) and i < len(notes) and notes[i]:
            item["note"] = notes[i]
        normalized.append(item)
    return normalized


def load_manifest_or_args(args):
    """Build normalized configuration and item list from --from-harvest-file, --manifest, or CLI flags."""
    harvest_file = getattr(args, "from_harvest_file", None)
    probe_cover = getattr(args, "probe_cover", None)
    requested_mode = getattr(args, "mode", None)
    manifest_file = getattr(args, "manifest", None)
    allow_empty = False

    if harvest_file or manifest_file:
        if harvest_file:
            config, _ = parse_harvest_file(harvest_file)
            default_mode = "auto"
            allow_empty = not bool(probe_cover)
        else:
            with open(manifest_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            default_mode = "auto" if config.get("local_files") else "screenshots"
        raw_items = _normalize_manifest_items(config)
        slug = args.slug or config.get("slug") or ("probe-cover" if probe_cover else None)
        mode = resolve_storage_mode(requested_mode or config.get("mode") or default_mode, len(raw_items))
        start_index = (
            args.start_index
            if args.start_index is not None
            else config.get("start_index", 0 if mode == "screenshots" else 1)
        )
    else:
        slug = args.slug or ("probe-cover" if probe_cover else None)
        local_files = getattr(args, "local_files", None) or []
        if local_files:
            raw_items = [{"local_file": p} for p in local_files if p]
            default_cli_mode = "auto"
        else:
            urls = args.urls or []
            fallbacks = args.fallbacks or []
            count = max(len(urls), len(fallbacks))
            raw_items = [
                {
                    "url": urls[i] if i < len(urls) else None,
                    "fallback": fallbacks[i] if i < len(fallbacks) else None,
                }
                for i in range(count)
                if (urls[i] if i < len(urls) else None) or (fallbacks[i] if i < len(fallbacks) else None)
            ]
            default_cli_mode = "screenshots"
        mode = resolve_storage_mode(requested_mode or default_cli_mode, len(raw_items))
        start_index = (
            args.start_index
            if args.start_index is not None
            else (0 if mode == "screenshots" else 1)
        )

    if not slug:
        raise ValueError("--slug is required (either via CLI or inside --manifest)")
    if not raw_items and not allow_empty:
        raise ValueError(
            "Provide at least one image via --urls, --fallbacks, --local-files, --manifest, or --from-harvest-file"
        )

    return slug, mode, start_index, raw_items


def _yaml_escape(text):
    """Escape double quotes and collapse newlines for single-line YAML string values."""
    return str(text).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def _format_yaml_published(published_val):
    """Normalize ISO timestamps to YYYY-MM-DD and safely quote non-ISO published strings."""
    s = str(published_val).strip()
    iso_match = re.match(r"^(\d{4}-\d{2}-\d{2})(?:[T\s].*)?$", s)
    if iso_match:
        return iso_match.group(1)
    return f'"{_yaml_escape(s)}"'


def _format_display_published(published_val):
    """Normalize ISO timestamps to YYYY-MM-DD for body display while preserving non-ISO strings."""
    s = str(published_val).strip()
    iso_match = re.match(r"^(\d{4}-\d{2}-\d{2})(?:[T\s].*)?$", s)
    return iso_match.group(1) if iso_match else s


def _strip_duplicate_leading_h1(post_text, title):
    """Drop a leading '# <heading>' from web_article text when it duplicates the top-level title."""
    lines = post_text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith("# "):
        heading = lines[i].lstrip()[2:].strip()
        norm_h = re.sub(r"\s+", " ", heading).lower()
        norm_t = re.sub(r"\s+", " ", str(title or "")).strip().lower()
        if norm_h == norm_t or (norm_t and norm_t.startswith(norm_h)):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            return "\n".join(lines[i:]).strip()
    return post_text


def extract_raw_meta(args, harvest_meta=None):
    """Merge --raw-* CLI flags, --manifest metadata, and --from-harvest-file metadata."""
    manifest = {}
    if getattr(args, "manifest", None):
        with open(args.manifest, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    hmeta = harvest_meta or {}

    return {
        "init_raw": bool(getattr(args, "init_raw", False) or manifest.get("init_raw", False)),
        "platform": (
            getattr(args, "platform", None)
            or manifest.get("platform")
            or hmeta.get("platform")
            or ("local_image" if getattr(args, "local_files", None) else None)
        ),
        "raw_subdir": getattr(args, "raw_subdir", None) or manifest.get("raw_subdir") or "ai-other",
        "title": getattr(args, "raw_title", None) or manifest.get("raw_title") or hmeta.get("title"),
        "source": getattr(args, "raw_source", None) or manifest.get("raw_source") or hmeta.get("url"),
        "original_source": getattr(args, "raw_original_source", None) or manifest.get("raw_original_source"),
        "author": getattr(args, "raw_author", None) or manifest.get("raw_author") or hmeta.get("author"),
        "published": getattr(args, "raw_published", None) or manifest.get("raw_published") or hmeta.get("published"),
        "created": getattr(args, "raw_created", None) or manifest.get("raw_created") or dt_date.today().strftime("%Y-%m-%d"),
        "description": getattr(args, "raw_description", None) or manifest.get("raw_description"),
        "text": getattr(args, "raw_text", None) or manifest.get("raw_text") or hmeta.get("text"),
        "external_links": manifest.get("external_links") or hmeta.get("external_links") or [],
        "tags": manifest.get("raw_tags") or None,
        "notes": manifest.get("raw_notes") or manifest.get("notes") or [],
        "paywalled": bool(manifest.get("paywalled") or hmeta.get("paywalled")),
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


def _normalize_authors(author):
    """Normalize single/multi-author string or list into deduplicated [[Wiki Link]] entries."""
    if not author:
        return []
    if isinstance(author, (list, tuple)):
        raw_items = []
        for entry in author:
            if entry:
                raw_items.extend(_normalize_authors(str(entry)))
        seen = set()
        out = []
        for item in raw_items:
            if item.lower() not in seen:
                seen.add(item.lower())
                out.append(item)
        return out

    text = str(author).strip()
    if not text:
        return []

    parts = re.split(
        r"(?:\s*;\s*|\s*,\s+(?!(?:Inc\.?|LLC|Ltd\.?|Corp\.?|Jr\.?|Sr\.?|II|III|Ph\.?D\.?|M\.?D\.?)(?:\b|$)))(?![^\[]*\]\])",
        text,
    )
    seen = set()
    out = []
    for part in parts:
        cleaned = part.strip().strip('"').strip("'")
        if not cleaned:
            continue
        val = cleaned if cleaned.startswith("[[") and cleaned.endswith("]]") else f"[[{cleaned}]]"
        key = val.lower()
        if key not in seen:
            seen.add(key)
            out.append(val)
    return out


def scaffold_raw_article(slug, files, project_root, meta):
    """Create raw/articles/<subdir>/<slug>.md with frontmatter, text, and slide/asset embeds if not already present."""
    subdir = (meta.get("raw_subdir") or "ai-other").strip().strip("/\\")
    raw_dir = os.path.join(project_root, "raw", "articles", subdir)
    raw_path = os.path.join(raw_dir, f"{slug}.md")
    rel_path = _safe_relpath(raw_path, project_root)

    if os.path.isfile(raw_path):
        return rel_path, "skipped_existing"

    os.makedirs(raw_dir, exist_ok=True)

    platform = (meta.get("platform") or "").lower()
    title = meta.get("title") or slug.replace("-", " ").title()
    source_url = meta.get("source") or ""
    original_source = meta.get("original_source") or ""
    author = meta.get("author") or ""
    published = meta.get("published") or ""
    created = meta.get("created") or dt_date.today().strftime("%Y-%m-%d")
    ok_files = [f for f in files if f.get("source_used") != "failed"]
    is_assets_mode = bool(
        ok_files
        and (
            str(ok_files[0].get("rel_path", "")).startswith("raw/assets/")
            or str(ok_files[0].get("md_embed", "")).startswith("![Asset")
        )
    )
    if platform == "web_article":
        default_desc = (
            f"Captured web article and diagrams for {title}."
            if ok_files
            else f"Captured web article for {title}."
        )
    elif platform == "local_image":
        default_desc = f"Collected visual reference and infographic notes for {title}."
    else:
        default_desc = f"Visual guide and captured slides for {title}."
    description = meta.get("description") or default_desc
    post_text = (meta.get("text") or "").strip()
    if platform == "web_article" and post_text:
        post_text = _strip_duplicate_leading_h1(post_text, title)
    external_links = meta.get("external_links") or []
    if meta.get("tags"):
        tags = meta["tags"]
    elif platform == "web_article":
        tags = ["clippings", "web-article"]
    elif platform == "local_image":
        tags = ["clippings", "visual-guide", "infographic"]
    else:
        tags = ["clippings", "visual-guide"]
    meta_notes = meta.get("notes") or []

    lines = [
        "---",
        f'title: "{_yaml_escape(title)}"',
    ]
    if source_url:
        lines.append(f'source: "{_yaml_escape(source_url)}"')
    if original_source:
        lines.append(f'original_source: "{_yaml_escape(original_source)}"')
    authors = _normalize_authors(author)
    if authors:
        lines.append("author:")
        for author_val in authors:
            lines.append(f'  - "{_yaml_escape(author_val)}"')
    if published:
        lines.append(f"published: {_format_yaml_published(published)}")
    lines.append(f"created: {created}")
    if meta.get("paywalled"):
        lines.append("paywalled: true")
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
    elif platform == "local_image":
        lines.append("- **Nguồn lưu trữ:** Hình ảnh sưu tầm cục bộ (Local / Uploaded Image)")
    if published:
        lines.append(f"- **Thời gian đăng:** {_format_display_published(published)}")
    if meta.get("paywalled"):
        lines.append("- **Trạng thái paywall:** Partial preview (phần cuối bài nằm sau paywall)")
    if original_source:
        lines.append(f"- **Nguồn gốc tiếng Anh được tác giả trích dẫn:** {original_source}")

    if ok_files:
        if is_assets_mode:
            lines.append(f"- **Hình ảnh đính kèm ({len(ok_files)} ảnh):** `raw/assets/`")
        else:
            lines.append(f"- **Thư mục hình ảnh gốc ({len(ok_files)} trang):** `raw/screenshots/{slug}/`")
    lines.extend(["", "---", ""])

    if post_text:
        if platform == "web_article":
            lines.append("## Nội Dung Nguyên Văn Bài Viết")
            lines.append("")
            lines.append(post_text)
        else:
            lines.append("## Nội Dung Nguyên Văn Bài Đăng")
            lines.append("")
            for p_line in post_text.splitlines():
                lines.append(f"> {p_line}" if p_line.strip() else ">")
        lines.extend(["", "---", ""])

    if ok_files:
        has_custom_notes = bool(meta_notes or any(f.get("note") or f.get("transcription") for f in ok_files))
        if has_custom_notes:
            section_heading = f"## Chi Tiết {len(ok_files)} Trang Hình Ảnh Đính Kèm (Visual Transcription)"
            item_prefix = "Trang"
        elif platform == "web_article":
            section_heading = f"## Hình Ảnh & Sơ Đồ Đính Kèm ({len(ok_files)} ảnh)"
            item_prefix = "Hình"
        else:
            section_heading = f"## Thư Viện {len(ok_files)} Trang Hình Ảnh Đính Kèm"
            item_prefix = "Trang"
        lines.append(section_heading)
        lines.append("")
        for i, item in enumerate(ok_files):
            filename = item["filename"]
            dims = item.get("dimensions", "")
            dims_note = f" *({dims})*" if dims and dims != "unknown" else ""
            if item.get("md_embed") and str(item["md_embed"]).startswith("![Asset"):
                embed = item["md_embed"]
            else:
                embed = f"![{item_prefix} {i + 1}](../../screenshots/{slug}/{filename})"
            lines.extend([
                f"### {item_prefix} {i + 1} / {len(ok_files)}{dims_note}",
                embed,
                "",
            ])
            note_text = _resolve_slide_note(item, i, meta_notes)
            if note_text:
                lines.extend([note_text, ""])

    if external_links:
        lines.extend(["## Liên Kết Tham Khảo", ""])
        for link in external_links[:20]:
            lines.append(f"- {link}")
        lines.append("")

    with open(raw_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return rel_path, "created"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Download social/web post images concurrently into raw/screenshots or raw/assets."
    )
    parser.add_argument("--slug", help="Clean kebab-case slug (e.g. transformers-detailed-notes)")
    parser.add_argument(
        "--mode",
        choices=["screenshots", "assets", "auto"],
        default=None,
        help="Target storage mode: 'screenshots', 'assets', or 'auto' (1-3 -> assets, >=4 -> screenshots)",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=None,
        help="Starting index number (default: 0 for screenshots, 1 for assets)",
    )
    parser.add_argument("--urls", nargs="*", help="Ordered list of direct image URLs")
    parser.add_argument("--fallbacks", nargs="*", help="Ordered list of local screenshot fallback paths")
    parser.add_argument(
        "--local-files",
        nargs="*",
        help="Ordered list of local/uploaded image files to archive into raw/assets/ or raw/screenshots/",
    )
    parser.add_argument(
        "--platform",
        default=None,
        help="Optional platform override (auto-set to 'local_image' when --local-files is used)",
    )
    parser.add_argument("--manifest", help="Optional JSON manifest file defining slug, mode, and items")
    parser.add_argument(
        "--from-harvest-file",
        help="Zero-URL-Relay path to Chrome DevTools steps/<N>/output.txt or harvester JSON file",
    )
    parser.add_argument(
        "--probe-cover",
        help="Download ONLY slide 1 directly to this local file path (e.g. scratch/cover.webp) to determine topic/slug",
    )
    parser.add_argument(
        "--full-meta",
        action="store_true",
        help="Print full untruncated harvest_meta.text on stdout (default truncates text >1500 chars to save tokens)",
    )
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
        harvest_meta = None
        if args.from_harvest_file:
            _, harvest_meta = parse_harvest_file(args.from_harvest_file)
        slug, mode, start_index, raw_items = load_manifest_or_args(args)
        raw_meta = extract_raw_meta(args, harvest_meta=harvest_meta)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    project_root = args.project_root or find_project_root()

    if args.probe_cover:
        probe_abs = os.path.abspath(args.probe_cover)
        out_dir = os.path.dirname(probe_abs)
        raw_items = raw_items[:1]
        tasks = [
            {
                "index": start_index,
                "url": raw_items[0].get("url"),
                "fallback": raw_items[0].get("fallback"),
                "local_file": raw_items[0].get("local_file"),
                "note": raw_items[0].get("note"),
                "mode": mode,
                "slug": slug,
                "out_dir": out_dir,
                "explicit_dest_path": probe_abs,
                "project_root": project_root,
                "min_bytes": args.min_bytes,
            }
        ]
    else:
        if mode == "screenshots":
            out_dir = os.path.join(project_root, "raw", "screenshots", slug)
        else:
            out_dir = os.path.join(project_root, "raw", "assets")
        if raw_items:
            os.makedirs(out_dir, exist_ok=True)
        tasks = [
            {
                "index": start_index + i,
                "url": item.get("url"),
                "fallback": item.get("fallback"),
                "local_file": item.get("local_file"),
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
    if tasks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            for res in pool.map(process_item, tasks):
                results.append(res)
        results.sort(key=lambda r: r["index"])

    failed = [r for r in results if r["source_used"] == "failed"]

    report = {
        "status": "ok" if not failed else "partial",
        "slug": slug,
        "mode": mode,
        "output_dir": _safe_relpath(out_dir, project_root),
        "total_requested": len(tasks),
        "succeeded_count": len(tasks) - len(failed),
        "failed_count": len(failed),
        "files": results,
    }
    if args.probe_cover:
        report["probe_cover"] = os.path.abspath(args.probe_cover).replace("\\", "/")
    if harvest_meta:
        report["harvest_meta"] = summarize_harvest_meta_for_stdout(harvest_meta, full_meta=args.full_meta)
    if raw_meta.get("init_raw") and not args.probe_cover and (not tasks or len(failed) < len(tasks)):
        scaffold_path, scaffold_status = scaffold_raw_article(slug, results, project_root, raw_meta)
        report["raw_scaffold_path"] = scaffold_path
        report["raw_scaffold_status"] = scaffold_status
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if tasks and failed and len(failed) == len(tasks):
        sys.exit(1)


if __name__ == "__main__":
    main()
