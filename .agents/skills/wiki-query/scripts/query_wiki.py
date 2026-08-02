"""
Wiki Query Helper Script — Fast Multi-Layer Search Utility.

Scans index.md, wiki/, mem/, and output/ for query keywords and outputs matching
page titles, paths, and relevant context snippets in a token-efficient JSON format.

Usage:
    python .agents/skills/wiki-query/scripts/query_wiki.py "<QUERY_STRING>" [--max-results 10]
"""

import os
import re
import json
import sys
import argparse


def find_project_root():
    """Walk up from this script's location to find the project root (where index.md lives)."""
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(10):
        if os.path.isfile(os.path.join(d, "index.md")):
            return d
        d = os.path.dirname(d)
    return None


def search_index(index_file, query):
    """Scan index.md for title or description matches."""
    matches = []
    if not os.path.isfile(index_file):
        return matches

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    with open(index_file, "r", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, 1):
            if pattern.search(line):
                link_match = re.search(r"\[\[(.*?)\]\]", line)
                page_name = link_match.group(1).split("|")[0] if link_match else None
                matches.append({
                    "type": "index_match",
                    "line_number": line_num,
                    "snippet": line.strip(),
                    "page_name": page_name,
                })
    return matches


def search_content_files(project_root, query, max_results=10):
    """Scan markdown files across wiki/, mem/, and output/ for keyword matches."""
    scan_dirs = ["wiki", "mem", "output"]
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    file_matches = []

    for s_dir in scan_dirs:
        dir_path = os.path.join(project_root, s_dir)
        if not os.path.isdir(dir_path):
            continue
        for root, _dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith(".md"):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, project_root)
                    page_name = f[:-3]

                    matched_lines = []
                    with open(full_path, "r", encoding="utf-8", errors="replace") as file_obj:
                        for line_num, line in enumerate(file_obj, 1):
                            if pattern.search(line):
                                matched_lines.append({
                                    "line": line_num,
                                    "content": line.strip()[:150]
                                })
                                if len(matched_lines) >= 3:
                                    break

                    if matched_lines:
                        file_matches.append({
                            "page_name": page_name,
                            "rel_path": rel_path,
                            "match_count": len(matched_lines),
                            "snippets": matched_lines,
                        })
                        if len(file_matches) >= max_results:
                            break
            if len(file_matches) >= max_results:
                break

    return file_matches


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Wiki Query Helper Script")
    parser.add_argument("query", help="Search query string or keywords")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum number of file matches")
    args = parser.parse_args()

    project_root = find_project_root()
    if not project_root:
        print(json.dumps({"error": "Could not locate project root containing index.md"}))
        sys.exit(1)

    index_file = os.path.join(project_root, "index.md")
    index_results = search_index(index_file, args.query)
    content_results = search_content_files(project_root, args.query, args.max_results)

    output = {
        "query": args.query,
        "index_matches_count": len(index_results),
        "index_matches": index_results,
        "content_matches_count": len(content_results),
        "content_matches": content_results,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
