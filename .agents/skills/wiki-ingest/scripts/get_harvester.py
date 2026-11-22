"""
Progressive-Disclosure Platform Harvester Dispatcher & Duplicate Checker for wiki-ingest (v4.3).

Routes any HTTP/HTTPS URL to its matching lightweight JS DOM harvester
(facebook, instagram, x_twitter, linkedin, or web_article), guards against
misrouting YouTube video or direct PDF URLs, checks raw/ + wiki/sources/ for
duplicate ingestion, and emits a compact Zero-URL-Relay browser prompt.

Usage:
    python .agents/skills/wiki-ingest/scripts/get_harvester.py --url "https://..."
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse


HARVESTERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harvesters")

SUPPORTED_PLATFORMS = ("facebook", "instagram", "x_twitter", "linkedin", "web_article")

PLATFORM_HINTS = {
    "facebook": (
        "1) Dismiss closeable login modal (`X`). If strictly gated with no close button, stop and report BLOCKED.\n"
        "2) Run the `facebook` JS harvester on the post page to capture verbatim post text/metadata.\n"
        "3) If `status === \"needs_gallery_open\"` and `first_photo_href` is present, click/open the first photo "
        "into `/photo?fbid=...` (or `/photos/...`) and run the SAME JS harvester once inside the photo viewer."
    ),
    "instagram": (
        "1) Dismiss any closeable popup (`Not now` / `X`). If blocked by mandatory login wall (`status === \"blocked\"`), "
        "stop and report BLOCKED.\n"
        "2) Run the `instagram` JS harvester ONCE on the post URL; it auto-rewinds to Slide 1, expands captions, "
        "excludes 'More posts' thumbnails, and clicks through all carousel slides automatically.\n"
        "3) Note: Captions are often short CTAs ('Comment PDF'), so let the coordinator probe Slide 1 to determine topic/slug."
    ),
    "x_twitter": (
        "1) Dismiss any non-blocking banner. If login blocks tweet view (`status === \"blocked\"`), report BLOCKED.\n"
        "2) Run the `x_twitter` JS harvester ONCE; it anchors on the exact focal status ID, expands long tweets, "
        "scrolls through connected same-author thread tweets or X Longform Articles, and upgrades `pbs.twimg.com/media` to `?name=orig`."
    ),
    "linkedin": (
        "1) If `/authwall` blocks the post (`status === \"blocked\"`), report BLOCKED.\n"
        "2) Run the `linkedin` JS harvester ONCE; it parses JSON-LD + logged-in/public DOM, expands `'see more'`, "
        "steps document carousels, and captures media/comments.\n"
        "3) If `document_iframe_url` is returned for a cross-origin PDF slide viewer, include it prominently in your reply."
    ),
    "web_article": (
        "1) Dismiss any closeable subscribe/sign-in modal (`Continue reading` / `No thanks` / `X`) and wait for main article content to settle.\n"
        "2) Scroll briefly down the article so lazy-loaded `<figure>` images load (`naturalWidth > 0`).\n"
        "3) Run the `web_article` JS harvester ONCE to extract JSON-LD (@graph-aware) / OG metadata, paywall flag, "
        "clean structured Markdown (headings, code blocks with language, GFM tables, nested lists), and high-res `<figure>` URLs."
    ),
}


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


def detect_platform(url):
    """Classify URL into one of the five harvester keys, or 'youtube'/'pdf' redirect guards."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path_lower = (parsed.path or "").lower()
    if host.startswith("www."):
        host = host[4:]

    if host in ("youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"):
        return "youtube"
    if path_lower.endswith(".pdf") or (host == "arxiv.org" and path_lower.startswith("/pdf/")):
        return "pdf"
    if host in ("facebook.com", "web.facebook.com", "m.facebook.com", "mbasic.facebook.com", "fb.com", "fb.watch"):
        return "facebook"
    if host in ("instagram.com", "instagr.am"):
        return "instagram"
    if host in ("x.com", "twitter.com", "mobile.twitter.com"):
        return "x_twitter"
    if host == "linkedin.com" or host.endswith(".linkedin.com"):
        return "linkedin"
    return "web_article"


GENERIC_QUERY_PATHS = {"/watch", "/photo", "/permalink.php", "/story.php", "/item"}


def extract_url_fingerprints(url):
    """Extract normalized URL, scheme/www-agnostic host+path, and canonical platform post IDs."""
    parsed = urlparse(url)
    clean_path = parsed.path.rstrip("/")
    clean_url = f"{parsed.scheme}://{parsed.netloc}{clean_path}" if parsed.scheme and parsed.netloc else url.strip()
    is_generic_query_endpoint = clean_path.lower() in GENERIC_QUERY_PATHS
    tokens = []

    host_no_www = (parsed.hostname or "").lower()
    if host_no_www.startswith("www."):
        host_no_www = host_no_www[4:]

    if not is_generic_query_endpoint:
        if clean_url:
            tokens.append(clean_url)
        # Add www- and scheme-agnostic host+path for articles/docs/posts with substantive paths
        if host_no_www and len(clean_path) >= 4:
            host_path = f"{host_no_www}{clean_path}"
            if host_path not in tokens:
                tokens.append(host_path)
    else:
        # Preserve identity query parameter for generic endpoints like HN /item?id=...
        id_m = re.search(r"[?&]id=(\d{5,})", url)
        if id_m and host_no_www:
            tokens.append(f"{host_no_www}{clean_path}?id={id_m.group(1)}")

    patterns = [
        r"(pfbid[A-Za-z0-9]{12,})",
        r"/(?:posts|permalink|videos)/(\d{8,})",
        r"/share/[pr]/([A-Za-z0-9]{8,})",
        r"[?&](?:story_fbid|fbid)=(\d{8,})",
        r"(?:instagram\.com|instagr\.am)/(?:[^/]+/)?(?:p|reels?|tv)/([A-Za-z0-9_-]{6,})",
        r"(?:x\.com|twitter\.com)/(?:[^/]+/)?(?:status|article)/(\d{8,})",
        r"(?:activity|ugcPost)[:-](\d{10,})",
        r"(?:youtube\.com/watch\?[^#\s]*v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pat in patterns:
        for m in re.finditer(pat, url):
            tok = m.group(1)
            if tok and len(tok) >= 6 and tok not in tokens:
                tokens.append(tok)
    return tokens


def _token_matches_text(token, text):
    """Match token with alphanumeric/slug boundaries so prefix paths never false-match longer slugs."""
    return bool(re.search(rf"(?<![A-Za-z0-9_-]){re.escape(token)}(?![A-Za-z0-9_-])", text))


def find_duplicate_ingestions(url, project_root):
    """Scan raw/articles/, raw/video-transcripts/, and wiki/sources/ for existing references."""
    tokens = extract_url_fingerprints(url)
    if not tokens:
        return []

    scan_dirs = [
        os.path.join(project_root, "raw", "articles"),
        os.path.join(project_root, "raw", "video-transcripts"),
        os.path.join(project_root, "wiki", "sources"),
    ]
    matches = []
    seen_paths = set()

    for base_dir in scan_dirs:
        if not os.path.isdir(base_dir):
            continue
        for root_dir, _, filenames in os.walk(base_dir):
            for fname in sorted(filenames):
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(root_dir, fname)
                rel = os.path.relpath(fpath, project_root).replace("\\", "/")
                if rel in seen_paths:
                    continue
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        head = f.read(6144)
                except OSError:
                    continue

                hit_token = None
                match_role = "reference"
                for tok in tokens:
                    if _token_matches_text(tok, head):
                        hit_token = tok
                        for line in head.splitlines()[:50]:
                            if _token_matches_text(tok, line):
                                stripped = line.strip()
                                if stripped.startswith(("original_source:", "original_url:")) or "Nguồn gốc" in stripped:
                                    match_role = "original_source"
                                    break
                                if stripped.startswith(("source:", "url:", "- **Nguồn", "**Source Post:**", "**URL**:")):
                                    match_role = "primary_source"
                                    break
                        break
                if hit_token:
                    seen_paths.add(rel)
                    matches.append({
                        "file": rel,
                        "match_role": match_role,
                        "matched_token": hit_token,
                    })
    return matches


def load_harvester_js(platform):
    """Read the JS snippet for the requested platform."""
    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform '{platform}'. Choose from: {', '.join(SUPPORTED_PLATFORMS)}")
    js_path = os.path.join(HARVESTERS_DIR, f"{platform}.js")
    if not os.path.isfile(js_path):
        raise FileNotFoundError(f"Missing harvester JS file: {js_path}")
    with open(js_path, "r", encoding="utf-8") as f:
        return f.read().strip(), js_path


def build_browser_prompt(url, platform, js_code):
    """Build a compact, Zero-URL-Relay prompt for the browser subagent."""
    guidance = PLATFORM_HINTS.get(platform, PLATFORM_HINTS["web_article"])
    return (
        f"Navigate to: {url}\n\n"
        f"Platform mode: `{platform}` — execute fast DOM harvesting ONLY (~2-4 browser tool calls):\n"
        f"{guidance}\n\n"
        f"ZERO-URL-RELAY RULE (Token Saving):\n"
        f"- If `mcp_chrome_devtools_evaluate_script` saves large output to a `steps/<N>/output.txt` file, "
        f"do NOT paste long CDN image URLs or 30KB article text into your text reply.\n"
        f"- Return cleanly:\n"
        f"  1) `status`, `author`, `handle`, `published`, `engagement`, `total_slides`, and `paywalled` (when true)\n"
        f"  2) Exact saved `steps/<N>/output.txt` path (or inline `text` / `slides` ONLY when small, e.g. <= 3 slides and <= 1500 chars)\n"
        f"  3) Brief non-image metadata (comments / external links / `document_iframe_url` / `videos_found` if any). Never transcribe slide text.\n\n"
        f"Run this exact JS snippet in `mcp_chrome_devtools_evaluate_script`:\n"
        f"```javascript\n{js_code}\n```"
    )


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Dispatch platform-specific wiki-ingest browser JS harvester and check duplicates."
    )
    parser.add_argument("--url", required=True, help="Target HTTP/HTTPS URL to inspect")
    parser.add_argument(
        "--platform",
        choices=list(SUPPORTED_PLATFORMS),
        default=None,
        help="Override auto-detected platform",
    )
    parser.add_argument(
        "--no-duplicate-check",
        action="store_true",
        help="Skip scanning raw/ and wiki/sources/ for duplicate URLs/IDs",
    )
    parser.add_argument(
        "--no-js",
        action="store_true",
        help="Omit browser_prompt from JSON output (useful for quick duplicate check)",
    )
    parser.add_argument(
        "--include-raw-js",
        action="store_true",
        help="Also emit standalone harvester_js field alongside browser_prompt (omitted by default to save tokens)",
    )
    parser.add_argument("--project-root", default=None, help="Optional vault root containing index.md")
    args = parser.parse_args()

    project_root = args.project_root or find_project_root()
    platform = args.platform or detect_platform(args.url)
    duplicates = [] if args.no_duplicate_check else find_duplicate_ingestions(args.url, project_root)

    out = {
        "status": "ok",
        "url": args.url,
        "platform": platform,
        "fingerprints": extract_url_fingerprints(args.url),
        "already_ingested": any(d["match_role"] == "primary_source" for d in duplicates),
        "has_original_source_overlap": any(d["match_role"] == "original_source" for d in duplicates),
        "duplicate_matches": duplicates,
    }

    if platform == "youtube":
        out["status"] = "redirect_video"
        out["recommended_command"] = (
            f'python .agents/skills/wiki-ingest/scripts/extract_youtube_transcript.py "{args.url}" --lang en --json'
        )
        out["note"] = "YouTube URL detected — use the 3-Stage Video Pipeline (references/video-ingest-guide.md) instead of web_article.js."
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if platform == "pdf":
        out["status"] = "redirect_pdf"
        out["note"] = "Direct PDF URL detected — download into raw/pdfs/<slug>.pdf and inspect via the pdf skill instead of web_article.js."
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if not args.no_js:
        js_code, js_path = load_harvester_js(platform)
        out["harvester_js_path"] = os.path.relpath(js_path, project_root).replace("\\", "/")
        if args.include_raw_js:
            out["harvester_js"] = js_code
        out["browser_prompt"] = build_browser_prompt(args.url, platform, js_code)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
