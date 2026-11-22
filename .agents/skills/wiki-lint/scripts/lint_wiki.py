"""
Wiki Lint Script — Enhanced structural health checker for Second Brain Architecture.

Scans the wiki/, mem/, and output/ directories for structural issues and outputs a JSON report.
Designed to be run by the wiki-lint agent skill.

Usage:
    python .agents/skills/wiki-lint/scripts/lint_wiki.py [--project-root PATH]

Output: JSON to stdout with categories:
    - orphan_pages, missing_pages, broken_links, missing_frontmatter,
      missing_fields, duplicate_titles, date_format_errors, stats
"""

import os
import re
import json
import sys
import argparse
from collections import Counter, defaultdict
from datetime import datetime
from urllib.parse import unquote


def find_project_root():
    """Walk up from this script's location to find the project root (where index.md lives)."""
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(10):
        if os.path.isfile(os.path.join(d, "index.md")):
            return d
        d = os.path.dirname(d)
    return None


def get_all_wiki_pages(project_root):
    """Recursively find all .md files in wiki/, mem/, and output/ directories."""
    scan_dirs = ["wiki", "mem", "output"]
    pages = []
    for s_dir in scan_dirs:
        dir_path = os.path.join(project_root, s_dir)
        if not os.path.isdir(dir_path):
            continue
        for root, _dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith(".md"):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, project_root)
                    page_name = f[:-3]  # strip .md
                    pages.append({
                        "name": page_name,
                        "path": full_path,
                        "rel_path": rel_path,
                    })
    return pages


def parse_frontmatter(content):
    """Extract YAML frontmatter fields from markdown content."""
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    fm_text = parts[1].strip()
    fields = {}

    current_key = None
    current_list = None
    for line in fm_text.split("\n"):
        stripped = line.strip()

        if stripped.startswith("- ") and current_key:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            fields[current_key] = current_list
            continue

        if ":" in stripped:
            if current_list is not None:
                current_list = None
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value:
                fields[key] = value
                current_list = None
            else:
                current_list = []
                fields[key] = current_list

    return fields


def _split_frontmatter_and_body(content):
    """Split optional YAML frontmatter block from the Markdown body."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            return f"---{parts[1]}---", parts[2]
    return "", content


def _strip_body_code_spans(body):
    """Strip fenced code blocks and inline code spans from a Markdown body."""
    stripped = re.sub(r"````.*?````|```.*?```|~~~.*?~~~", "", body, flags=re.S)
    return re.sub(r"`[^`\n]+`", "", stripped)


def _strip_code_and_math_spans(content):
    """Strip fenced code blocks and inline code spans in the Markdown body while preserving frontmatter."""
    fm_header, body = _split_frontmatter_and_body(content)
    return fm_header + _strip_body_code_spans(body)


def _clean_markdown_href(raw_href):
    """Normalize a Markdown link destination, returning (decoded_path, anchor) or (None, '') if non-local."""
    href = raw_href.strip()
    if href.startswith("<") and href.endswith(">"):
        href = href[1:-1].strip()
    else:
        title_match = re.match(r'^(\S+(?:\s+\S+)*?)\s+(?:"[^"]*"|\'[^\']*\')\s*$', href)
        if title_match and not href.endswith(")"):
            href = title_match.group(1).strip()

    if not href or href.startswith("#"):
        return None, ""
    lower = href.lower()
    if re.match(r"^[a-z][a-z0-9+.-]*:", lower):
        return None, ""

    path_part, _, anchor = href.partition("#")
    decoded_path = unquote(path_part.strip())
    if not decoded_path:
        return None, anchor
    return decoded_path, anchor


def extract_markdown_links(content):
    """Extract local Standard Markdown links [label](path) from body, ignoring images, URLs, and code."""
    _fm, body = _split_frontmatter_and_body(content)
    cleaned_body = _strip_body_code_spans(body)
    results = []
    for label, raw_href in re.findall(r"(?<!!)\[([^\[\]\n]+)\]\(([^)\n]+)\)", cleaned_body):
        decoded_path, anchor = _clean_markdown_href(raw_href)
        if decoded_path is None:
            continue
        results.append({
            "label": label.strip(),
            "raw_href": raw_href.strip(),
            "path": decoded_path,
            "anchor": anchor,
        })
    return results


def extract_wiki_links(content):
    """Extract all [[wiki links]] from markdown content, ignoring code spans and nested arrays."""
    cleaned = _strip_code_and_math_spans(content)
    links = re.findall(r"\[\[(.*?)\]\]", cleaned)
    results = []
    for link in links:
        target = re.split(r"\\?\|", link, maxsplit=1)[0].strip()
        if not target or "[" in target or "]" in target or "\n" in target:
            continue
        results.append(target)
    return results


def extract_legacy_wikilinks(content):
    """Return raw [[target]] matches remaining outside code blocks/inline code (for migration checks)."""
    cleaned = _strip_code_and_math_spans(content)
    results = []
    for raw in re.findall(r"\[\[(.*?)\]\]", cleaned):
        target = re.split(r"\\?\|", raw, maxsplit=1)[0].strip()
        if not target or "[" in target or "]" in target or "\n" in target:
            continue
        results.append(f"[[{raw}]]")
    return results


_INDEX_MD_BULLET_RE = re.compile(r"^\s*-\s*\[([^\[\]\n]+)\]\(([^)\n]+)\)(?:\s*:\s*(.*))?$")
_INDEX_WIKI_BULLET_RE = re.compile(r"^\s*-\s*\[\[(.*?)\]\](?:\s*:\s*(.*))?$")


def read_index_entries(index_file, project_root=None):
    """Read both Standard Markdown links and legacy [[wiki links]] from index.md."""
    with open(index_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    md_entries = []
    md_paths = set()
    md_paths_lower = set()
    legacy_entries = []
    legacy_stems = set()

    for line in content.splitlines():
        m_md = _INDEX_MD_BULLET_RE.match(line)
        if m_md:
            label = m_md.group(1).strip()
            raw_href = m_md.group(2).strip()
            decoded_path, _anchor = _clean_markdown_href(raw_href)
            if decoded_path:
                norm_posix = os.path.normpath(decoded_path).replace("\\", "/")
                if norm_posix.startswith("./"):
                    norm_posix = norm_posix[2:]
                md_entries.append({
                    "label": label,
                    "raw_href": raw_href,
                    "path": norm_posix,
                })
                md_paths.add(norm_posix)
                md_paths_lower.add(norm_posix.lower())
            continue

        m_wk = _INDEX_WIKI_BULLET_RE.match(line)
        if m_wk:
            target = re.split(r"\\?\|", m_wk.group(1), maxsplit=1)[0].strip()
            if target and "[" not in target and "]" not in target:
                legacy_entries.append(target)
                legacy_stems.add(target)

    return {
        "md_entries": md_entries,
        "md_paths": md_paths,
        "md_paths_lower": md_paths_lower,
        "legacy_entries": legacy_entries,
        "legacy_stems": legacy_stems,
    }


def read_index_links(index_file):
    """Extract all indexed page labels/names referenced in index.md (Markdown + legacy)."""
    data = read_index_entries(index_file)
    names = set(data["legacy_stems"])
    for entry in data["md_entries"]:
        names.add(entry["label"])
    return names


def validate_date(date_str):
    """Check if a date string matches YYYY-MM-DD format."""
    if not isinstance(date_str, str):
        date_str = str(date_str)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _is_within_root(resolved_path, abs_root):
    return resolved_path == abs_root or resolved_path.startswith(abs_root + os.sep)


def lint_wiki(project_root, index_file):
    """Run all structural checks across wiki/, mem/, output/ and return a JSON report."""
    abs_root = os.path.abspath(project_root)
    pages = get_all_wiki_pages(abs_root)
    page_names = {p["name"] for p in pages}
    idx_data = read_index_entries(index_file, abs_root)
    with open(index_file, "r", encoding="utf-8", errors="replace") as f:
        index_content = f.read()

    report = {
        "orphan_pages": [],
        "missing_pages": [],
        "broken_links": [],
        "legacy_wikilinks": [],
        "missing_frontmatter": [],
        "missing_fields": [],
        "duplicate_titles": [],
        "date_format_errors": [],
        "tag_analysis": {
            "all_tags": {},
            "singleton_tags": [],
        },
        "stats": {
            "total_wiki_pages": len(pages),
            "total_index_entries": len(idx_data["md_entries"]) + len(idx_data["legacy_entries"]),
            "total_links": 0,
            "total_markdown_links": 0,
            "total_legacy_wikilinks": 0,
            "total_broken_links": 0,
            "pages_with_frontmatter": 0,
            "pages_without_frontmatter": 0,
        },
    }

    for wl in extract_legacy_wikilinks(index_content):
        report["legacy_wikilinks"].append({
            "page": "index",
            "page_path": "index.md",
            "wikilink": wl,
        })

    # Orphans: pages in wiki/mem/output (excluding log.md) not in index.md
    for p in pages:
        if p["name"] == "log":
            continue
        rel_posix = p["rel_path"].replace("\\", "/")
        if rel_posix.lower() not in idx_data["md_paths_lower"] and p["name"] not in idx_data["legacy_stems"]:
            report["orphan_pages"].append({
                "name": p["name"],
                "path": p["rel_path"],
            })

    # Missing: referenced in index.md but target file missing
    for entry in idx_data["md_entries"]:
        resolved = os.path.normpath(os.path.join(abs_root, entry["path"]))
        if not (_is_within_root(resolved, abs_root) and os.path.isfile(resolved)):
            report["missing_pages"].append(entry["path"])

    for link in idx_data["legacy_entries"]:
        if link.startswith("raw/"):
            continue
        if link not in page_names:
            report["missing_pages"].append(link)

    # Per-page checks
    all_tags = Counter()
    title_map = defaultdict(list)

    for p in pages:
        # Ignore log.md checks
        if p["name"] == "log":
            continue

        with open(p["path"], "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        fm = parse_frontmatter(content)
        if fm is None:
            report["missing_frontmatter"].append({
                "name": p["name"],
                "path": p["rel_path"],
            })
            report["stats"]["pages_without_frontmatter"] += 1
        else:
            report["stats"]["pages_with_frontmatter"] += 1

            required = ["title", "date", "tags"]
            if "sources" in p["rel_path"]:
                required.append("source")

            missing = [field for field in required if field not in fm or not fm[field]]
            if missing:
                report["missing_fields"].append({
                    "name": p["name"],
                    "path": p["rel_path"],
                    "missing": missing,
                })

            if "date" in fm:
                if not validate_date(fm["date"]):
                    report["date_format_errors"].append({
                        "name": p["name"],
                        "path": p["rel_path"],
                        "date_value": str(fm["date"]),
                    })

            if "title" in fm:
                title_map[fm["title"]].append(p["rel_path"])

            if "tags" in fm and isinstance(fm["tags"], list):
                for tag in fm["tags"]:
                    all_tags[tag] += 1

            if "source" in fm and fm["source"]:
                raw_sources = fm["source"] if isinstance(fm["source"], list) else [fm["source"]]
                fm_items = []
                for entry in raw_sources:
                    s_val = str(entry).strip()
                    if "[[" in s_val:
                        continue
                    for part in re.split(r"\s*,\s*(?=(?:wiki|mem|output|raw)/)", s_val):
                        part = part.strip()
                        if part:
                            fm_items.append(part)
                for src_path in fm_items:
                    if re.match(r"^(?:wiki|mem|output|raw)/", src_path):
                        resolved = os.path.normpath(os.path.join(abs_root, src_path))
                        if not (_is_within_root(resolved, abs_root) and os.path.isfile(resolved)):
                            report["broken_links"].append({
                                "page": p["name"],
                                "page_path": p["rel_path"],
                                "broken_link": src_path,
                                "link_type": "frontmatter_source",
                            })

        # Markdown links check (relative filesystem resolution)
        md_links = extract_markdown_links(content)
        report["stats"]["total_markdown_links"] += len(md_links)
        report["stats"]["total_links"] += len(md_links)
        page_dir = os.path.dirname(os.path.abspath(p["path"]))
        for ml in md_links:
            resolved = os.path.normpath(os.path.join(page_dir, ml["path"]))
            if not (_is_within_root(resolved, abs_root) and os.path.isfile(resolved)):
                report["broken_links"].append({
                    "page": p["name"],
                    "page_path": p["rel_path"],
                    "broken_link": ml["raw_href"],
                    "link_type": "markdown",
                })

        # Legacy [[wiki links]] backward-compatible check & deprecation tracker
        legacy_raw = extract_legacy_wikilinks(content)
        for wl in legacy_raw:
            report["legacy_wikilinks"].append({
                "page": p["name"],
                "page_path": p["rel_path"],
                "wikilink": wl,
            })

        links = extract_wiki_links(content)
        report["stats"]["total_links"] += len(links)

        for link in links:
            if link.startswith("raw/"):
                continue
            page_ref = link.split("#")[0].strip()
            if page_ref and page_ref not in page_names:
                report["broken_links"].append({
                    "page": p["name"],
                    "page_path": p["rel_path"],
                    "broken_link": link,
                    "link_type": "wikilink",
                })

    for title, paths in title_map.items():
        if len(paths) > 1:
            report["duplicate_titles"].append({
                "title": title,
                "pages": paths,
            })

    report["tag_analysis"]["all_tags"] = dict(all_tags.most_common())
    report["tag_analysis"]["singleton_tags"] = [
        tag for tag, count in all_tags.items() if count == 1
    ]

    report["stats"]["total_broken_links"] = len(report["broken_links"])
    report["stats"]["total_legacy_wikilinks"] = len(report["legacy_wikilinks"])
    if len(pages) > 0:
        coverage = (len(pages) - len(report["orphan_pages"])) / len(pages) * 100
        report["stats"]["index_coverage_pct"] = round(coverage, 1)
    else:
        report["stats"]["index_coverage_pct"] = 0

    return report


def main():
    parser = argparse.ArgumentParser(description="Second Brain structural lint checker")
    parser.add_argument(
        "--project-root",
        default=None,
        help="Path to project root (auto-detected if not provided)",
    )
    args = parser.parse_args()

    project_root = args.project_root or find_project_root()
    if project_root is None:
        print(json.dumps({"error": "Could not find project root (no index.md found)"}))
        sys.exit(1)

    index_file = os.path.join(project_root, "index.md")
    if not os.path.isfile(index_file):
        print(json.dumps({"error": f"Index file not found: {index_file}"}))
        sys.exit(1)

    report = lint_wiki(project_root, index_file)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
