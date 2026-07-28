"""
Wiki Lint Script — Enhanced structural health checker.

Scans the wiki directory for structural issues and outputs a JSON report.
Designed to be run by the wiki-lint agent skill.

Usage:
    python .agents/skills/wiki-lint/scripts/lint_wiki.py [--wiki-dir PATH] [--index-file PATH]

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


def get_all_wiki_pages(wiki_dir):
    """Recursively find all .md files in the wiki directory."""
    pages = []
    for root, _dirs, files in os.walk(wiki_dir):
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, os.path.dirname(wiki_dir))
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

    # Simple YAML parsing for flat fields
    current_key = None
    current_list = None
    for line in fm_text.split("\n"):
        stripped = line.strip()

        # List item under a key
        if stripped.startswith("- ") and current_key:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            fields[current_key] = current_list
            continue

        # Key-value pair
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


def extract_wiki_links(content):
    """Extract all [[wiki links]] from markdown content."""
    links = re.findall(r"\[\[(.*?)\]\]", content)
    # Handle [[Page|Display Text]] — take the page part
    return [link.split("|")[0].strip() for link in links]


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


def lint_wiki(wiki_dir, index_file):
    """Run all structural checks and return a JSON-serializable report."""

    pages = get_all_wiki_pages(wiki_dir)
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

    # --- Check orphans and missing ---
    # Orphans: pages in wiki/ but not in index.md
    for p in pages:
        if p["name"] not in index_links:
            report["orphan_pages"].append({
                "name": p["name"],
                "path": p["rel_path"],
            })

    # Missing: referenced in index.md but no corresponding page
    # (Only check page names, not raw/ references)
    for link in index_links:
        if link.startswith("raw/"):
            continue
        if link not in page_names:
            report["missing_pages"].append(link)

    # --- Per-page checks ---
    all_tags = Counter()
    title_map = defaultdict(list)

    for p in pages:
        with open(p["path"], "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Frontmatter check
        fm = parse_frontmatter(content)
        if fm is None:
            report["missing_frontmatter"].append({
                "name": p["name"],
                "path": p["rel_path"],
            })
            report["stats"]["pages_without_frontmatter"] += 1
        else:
            report["stats"]["pages_with_frontmatter"] += 1

            # Required fields
            required = ["title", "date", "tags"]
            # source is only required for source pages
            if "sources" in p["rel_path"]:
                required.append("source")

            missing = [field for field in required if field not in fm or not fm[field]]
            if missing:
                report["missing_fields"].append({
                    "name": p["name"],
                    "path": p["rel_path"],
                    "missing": missing,
                })

            # Date format validation
            if "date" in fm:
                if not validate_date(fm["date"]):
                    report["date_format_errors"].append({
                        "name": p["name"],
                        "path": p["rel_path"],
                        "date_value": str(fm["date"]),
                    })

            # Title duplicate detection
            if "title" in fm:
                title_map[fm["title"]].append(p["rel_path"])

            # Tag collection
            if "tags" in fm and isinstance(fm["tags"], list):
                for tag in fm["tags"]:
                    all_tags[tag] += 1

        # Broken links check
        links = extract_wiki_links(content)
        report["stats"]["total_links"] += len(links)

        for link in links:
            # Skip raw/ references — those are file paths, not wiki pages
            if link.startswith("raw/"):
                continue
            # Strip heading anchors: [[Page Name#Section]] -> "Page Name"
            page_ref = link.split("#")[0].strip()
            if page_ref and page_ref not in page_names:
                report["broken_links"].append({
                    "page": p["name"],
                    "page_path": p["rel_path"],
                    "broken_link": link,
                })

    # --- Post-processing ---

    # Duplicate titles
    for title, paths in title_map.items():
        if len(paths) > 1:
            report["duplicate_titles"].append({
                "title": title,
                "pages": paths,
            })

    # Tag analysis
    report["tag_analysis"]["all_tags"] = dict(all_tags.most_common())
    report["tag_analysis"]["singleton_tags"] = [
        tag for tag, count in all_tags.items() if count == 1
    ]

    # Final stats
    report["stats"]["total_broken_links"] = len(report["broken_links"])
    if len(pages) > 0:
        coverage = (len(pages) - len(report["orphan_pages"])) / len(pages) * 100
        report["stats"]["index_coverage_pct"] = round(coverage, 1)
    else:
        report["stats"]["index_coverage_pct"] = 0

    return report


def main():
    parser = argparse.ArgumentParser(description="Wiki structural lint checker")
    parser.add_argument(
        "--wiki-dir",
        default=None,
        help="Path to the wiki/ directory (auto-detected if not provided)",
    )
    parser.add_argument(
        "--index-file",
        default=None,
        help="Path to index.md (auto-detected if not provided)",
    )
    args = parser.parse_args()

    # Auto-detect paths
    project_root = find_project_root()
    if project_root is None:
        print(json.dumps({"error": "Could not find project root (no index.md found)"}))
        sys.exit(1)

    wiki_dir = args.wiki_dir or os.path.join(project_root, "wiki")
    index_file = args.index_file or os.path.join(project_root, "index.md")

    if not os.path.isdir(wiki_dir):
        print(json.dumps({"error": f"Wiki directory not found: {wiki_dir}"}))
        sys.exit(1)

    if not os.path.isfile(index_file):
        print(json.dumps({"error": f"Index file not found: {index_file}"}))
        sys.exit(1)

    report = lint_wiki(wiki_dir, index_file)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
