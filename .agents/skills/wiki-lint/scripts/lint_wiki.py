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


def _strip_code_and_math_spans(content):
    """Strip fenced code blocks and inline code spans in the Markdown body while preserving frontmatter."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            fm_header = f"---{parts[1]}---"
            body = parts[2]
        else:
            fm_header, body = "", content
    else:
        fm_header, body = "", content

    body = re.sub(r"````.*?````|```.*?```|~~~.*?~~~", "", body, flags=re.S)
    body = re.sub(r"`[^`\n]+`", "", body)
    return fm_header + body


def extract_wiki_links(content):
    """Extract all [[wiki links]] from markdown content, ignoring code spans and nested arrays."""
    cleaned = _strip_code_and_math_spans(content)
    links = re.findall(r"\[\[(.*?)\]\]", cleaned)
    results = []
    for link in links:
        target = link.split("|")[0].strip()
        if not target or "[" in target or "]" in target or "\n" in target:
            continue
        results.append(target)
    return results


def read_index_links(index_file):
    """Extract all [[wiki links]] referenced in index.md."""
    with open(index_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    return set(extract_wiki_links(content))


def validate_date(date_str):
    """Check if a date string matches YYYY-MM-DD format."""
    if not isinstance(date_str, str):
        date_str = str(date_str)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def lint_wiki(project_root, index_file):
    """Run all structural checks across wiki/, mem/, output/ and return a JSON report."""

    pages = get_all_wiki_pages(project_root)
    page_names = {p["name"] for p in pages}
    index_links = read_index_links(index_file)

    report = {
        "orphan_pages": [],
        "missing_pages": [],
        "broken_links": [],
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
            "total_index_entries": len(index_links),
            "total_links": 0,
            "total_broken_links": 0,
            "pages_with_frontmatter": 0,
            "pages_without_frontmatter": 0,
        },
    }

    # Orphans: pages in wiki/ (excluding log.md) not in index.md
    for p in pages:
        if p["name"] == "log":
            continue
        if p["name"] not in index_links:
            report["orphan_pages"].append({
                "name": p["name"],
                "path": p["rel_path"],
            })

    # Missing: referenced in index.md but no corresponding page
    for link in index_links:
        if link.startswith("raw/"):
            continue
        if link not in page_names:
            report["missing_pages"].append(link)

    # Per-page checks
    all_tags = Counter()
    title_map = defaultdict(list)

    for p in pages:
        # Ignore log.md for frontmatter checks
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

        # Broken links check
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
