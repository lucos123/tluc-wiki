"""
Deterministic Index, Log & Lint Registrar for wiki-ingest.

Atomically inserts/updates entries in index.md (sorted alphabetically within
each updated section), appends an entry to wiki/log.md, and runs lint_wiki.py
in a single command.

Usage:
    python .agents/skills/wiki-ingest/scripts/register_ingest.py \
        --date 2026-11-16 \
        --log-type ingest \
        --source-title "Prompt Engineering Handbook" \
        --entry "Entities|Viet Nguyen AI|Vietnamese AI practitioner..." \
        --entry "Concepts|Prompt Engineering|Foundational discipline..." \
        --entry "Sources|Prompt Engineering Handbook|11-page visual guide..."
"""

import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import date as dt_date


SECTION_ALIASES = {
    "entities": "Entities",
    "entity": "Entities",
    "concepts": "Concepts",
    "concept": "Concepts",
    "sources": "Sources",
    "source": "Sources",
    "mem": "Personal Memory & Projects (mem/)",
    "memory": "Personal Memory & Projects (mem/)",
    "personal memory & projects (mem/)": "Personal Memory & Projects (mem/)",
    "analyses": "Analyses",
    "analysis": "Analyses",
    "output": "Generated Deliverables (output/)",
    "deliverables": "Generated Deliverables (output/)",
    "generated deliverables (output/)": "Generated Deliverables (output/)",
}

ENTRY_LINE_RE = re.compile(r"^\s*-\s*\[\[(.*?)\]\]\s*:\s*(.*)$")


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


def normalize_section(raw_section):
    """Map section names or aliases to canonical index.md H2 headings."""
    key = raw_section.strip().lower()
    if key in SECTION_ALIASES:
        return SECTION_ALIASES[key]
    return raw_section.strip()


def parse_entry_arg(raw_entry):
    """Parse 'Section|Page Name|One-line summary' into a structured dict."""
    parts = [p.strip() for p in raw_entry.split("|", 2)]
    if len(parts) != 3 or not all(parts):
        raise ValueError(
            f"Invalid --entry '{raw_entry}'. Expected 'Section|Page Name|One-line summary'."
        )
    return {
        "section": normalize_section(parts[0]),
        "page": parts[1],
        "summary": parts[2],
    }


def load_lint_module(project_root):
    """Dynamically import lint_wiki.py from .agents/skills/wiki-lint/scripts/."""
    lint_path = os.path.join(
        project_root, ".agents", "skills", "wiki-lint", "scripts", "lint_wiki.py"
    )
    if not os.path.isfile(lint_path):
        raise FileNotFoundError(f"Cannot locate lint_wiki.py at {lint_path}")
    spec = importlib.util.spec_from_file_location("lint_wiki", lint_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sort_key_from_bullet(line):
    """Return case-insensitive sort key for a '- [[Page]]: Summary' bullet line."""
    m = ENTRY_LINE_RE.match(line)
    if m:
        return m.group(1).split("|")[0].strip().lower()
    return line.strip().lower()


def update_index_content(content, entries):
    """Insert or update entries inside target ## sections and sort bullets alphabetically."""
    if not entries:
        return content, []

    lines = content.splitlines()
    preamble = []
    sections = []
    current_name = None
    current_lines = []

    for line in lines:
        if line.startswith("## "):
            if current_name is None:
                pass
            else:
                sections.append({"name": current_name, "lines": current_lines})
            current_name = line[3:].strip()
            current_lines = []
        else:
            if current_name is None:
                preamble.append(line)
            else:
                current_lines.append(line)

    if current_name is not None:
        sections.append({"name": current_name, "lines": current_lines})

    section_map = {s["name"].lower(): s for s in sections}
    grouped = {}
    for e in entries:
        grouped.setdefault(e["section"], []).append(e)

    updated = []
    for sec_name, sec_entries in grouped.items():
        sec_obj = section_map.get(sec_name.lower())
        if sec_obj is None:
            sec_obj = {"name": sec_name, "lines": []}
            sections.append(sec_obj)
            section_map[sec_name.lower()] = sec_obj

        bullets = []
        other_lines = []
        for l in sec_obj["lines"]:
            if ENTRY_LINE_RE.match(l):
                bullets.append(l)
            elif l.strip():
                other_lines.append(l)

        bullet_by_page = {}
        for b in bullets:
            m = ENTRY_LINE_RE.match(b)
            page_key = m.group(1).split("|")[0].strip().lower()
            bullet_by_page[page_key] = b

        for e in sec_entries:
            new_line = f"- [[{e['page']}]]: {e['summary']}"
            bullet_by_page[e["page"].lower()] = new_line
            updated.append({"section": sec_obj["name"], "page": e["page"], "line": new_line})

        sorted_bullets = sorted(bullet_by_page.values(), key=sort_key_from_bullet)
        sec_obj["lines"] = other_lines + sorted_bullets

    rebuilt = list(preamble)
    while rebuilt and not rebuilt[-1].strip():
        rebuilt.pop()

    for sec in sections:
        if rebuilt:
            rebuilt.append("")
        rebuilt.append(f"## {sec['name']}")
        for l in sec["lines"]:
            rebuilt.append(l)

    return "\n".join(rebuilt) + "\n", updated


def update_log_content(content, log_line):
    """Append log_line to wiki/log.md if not already present."""
    existing_lines = [l.rstrip() for l in content.splitlines()]
    while existing_lines and not existing_lines[-1].strip():
        existing_lines.pop()

    if log_line in existing_lines:
        return "\n".join(existing_lines) + "\n", False

    existing_lines.append(log_line)
    return "\n".join(existing_lines) + "\n", True


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Atomically update index.md, append wiki/log.md, and run lint_wiki.py."
    )
    parser.add_argument("--source-title", help="Source/operation title for wiki/log.md")
    parser.add_argument(
        "--log-type",
        default="ingest",
        help="Operation tag in wiki/log.md (default: ingest)",
    )
    parser.add_argument(
        "--date",
        default=dt_date.today().strftime("%Y-%m-%d"),
        help="YYYY-MM-DD date string (default: today)",
    )
    parser.add_argument(
        "--entry",
        action="append",
        default=[],
        help="Entry formatted as 'Section|Page Name|One-line summary' (repeatable)",
    )
    parser.add_argument(
        "--manifest",
        help="Optional JSON manifest file with source_title, log_type, date, entries",
    )
    parser.add_argument("--project-root", help="Optional project root containing index.md")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview updates and run lint without writing files",
    )
    parser.add_argument(
        "--suggest-links",
        default=None,
        help="Search index.md for existing wiki pages matching comma/space-separated keywords and print JSON matches",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=25,
        help="Maximum matches returned with --suggest-links (default: 25)",
    )
    args = parser.parse_args()

    project_root = args.project_root or find_project_root()
    index_path = os.path.join(project_root, "index.md")

    if args.suggest_links is not None:
        query_tokens = [t for t in re.findall(r"[^\W_]+", args.suggest_links.lower()) if len(t) >= 2]
        matches = []
        current_section = ""
        if os.path.isfile(index_path):
            with open(index_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if line.startswith("## "):
                        current_section = line[3:].strip()
                        continue
                    m = ENTRY_LINE_RE.match(line)
                    if not m:
                        continue
                    page = m.group(1).split("|")[0].strip()
                    summary = m.group(2).strip()
                    haystack_page = page.lower()
                    haystack_sum = summary.lower()
                    score = sum(
                        (4 if t in haystack_page else 0) + (1 if t in haystack_sum else 0)
                        for t in query_tokens
                    )
                    if score > 0:
                        matches.append((score, current_section, page, line.strip()))
        matches.sort(key=lambda item: (-item[0], item[2].lower()))
        print(
            json.dumps(
                {
                    "status": "ok",
                    "query": args.suggest_links,
                    "matches": [
                        {"section": sec, "page": page, "line": line}
                        for _, sec, page, line in matches[: args.top_k]
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    try:
        entries = [parse_entry_arg(e) for e in args.entry]
        source_title = args.source_title
        log_type = args.log_type
        date_str = args.date

        if args.manifest:
            with open(args.manifest, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            source_title = source_title or manifest.get("source_title")
            log_type = manifest.get("log_type", log_type)
            date_str = manifest.get("date", date_str)
            for m_entry in manifest.get("entries", []):
                entries.append(
                    {
                        "section": normalize_section(m_entry["section"]),
                        "page": m_entry["page"].strip(),
                        "summary": m_entry["summary"].strip(),
                    }
                )

        if not source_title:
            raise ValueError("--source-title is required (via CLI or --manifest)")
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    log_path = os.path.join(project_root, "wiki", "log.md")

    with open(index_path, "r", encoding="utf-8", errors="replace") as f:
        index_content = f.read()
    new_index_content, updated_entries = update_index_content(index_content, entries)

    log_line = f"## [{date_str}] {log_type} | {source_title}"
    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        log_content = f.read()
    new_log_content, log_appended = update_log_content(log_content, log_line)

    if not args.dry_run:
        if entries:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(new_index_content)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(new_log_content)

    lint_mod = load_lint_module(project_root)
    lint_report = lint_mod.lint_wiki(project_root, index_path)

    error_keys = [
        "orphan_pages",
        "missing_pages",
        "broken_links",
        "missing_frontmatter",
        "missing_fields",
        "duplicate_titles",
        "date_format_errors",
    ]
    errors = {k: lint_report.get(k, []) for k in error_keys}
    has_errors = any(bool(v) for v in errors.values())

    output = {
        "status": "error" if has_errors else "ok",
        "dry_run": args.dry_run,
        "updated_entries": updated_entries,
        "log_entry": log_line,
        "log_appended": log_appended,
        "stats": lint_report.get("stats", {}),
        "errors": errors,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if has_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
