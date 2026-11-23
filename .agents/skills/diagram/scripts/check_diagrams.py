#!/usr/bin/env python3
"""
Deterministic Mermaid Diagram Validator for diagram skill & tluc-wiki.

Checks Markdown files (or stdin, or --vault across wiki/, mem/, output/) for:
  - empty-mermaid-block (error): Mermaid code fence has no diagram content
  - unsupported-mermaid-type (error): Diagram header outside Antigravity-safe subset
  - unbalanced-subgraph (error): Unmatched subgraph / end inside flowchart or graph blocks
  - unquoted-special-label (warning): Unquoted parentheses inside rectangular [Label (Info)] nodes
  - html-tag-in-mermaid (warning): Raw HTML tags (<br>, <b>, etc.) inside Mermaid blocks
  - oversized-mermaid-diagram (info): Diagram exceeds 45 non-comment lines
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SUPPORTED_TYPES = frozenset({
    "flowchart",
    "graph",
    "sequenceDiagram",
    "stateDiagram-v2",
    "stateDiagram",
    "classDiagram",
    "erDiagram",
    "xychart-beta",
})

UNQUOTED_PAREN_NODE_RE = re.compile(
    r'(?<!\[)\b[A-Za-z0-9_-]+\[(?![("\[/\\])[^"\]\n]*[()][^"\]\n]*\]'
)
HTML_TAG_RE = re.compile(
    r"<\s*/?\s*(?:br|b|i|u|span|div|font|small|strong|em)\b[^>]*>",
    re.IGNORECASE,
)


def find_project_root(start_dir=None):
    """Walk upward from script or CWD to find repository root containing index.md."""
    candidates = [Path(start_dir or __file__).resolve(), Path.cwd().resolve()]
    for base in candidates:
        probe = base if base.is_dir() else base.parent
        for _ in range(10):
            if (probe / "index.md").is_file():
                return str(probe)
            if probe.parent == probe:
                break
            probe = probe.parent
    return None


def extract_mermaid_blocks(text: str) -> list[dict]:
    """
    Extract top-level ```mermaid or ~~~mermaid blocks with exact 1-based line numbers.
    Ignores nested ```mermaid examples inside 4+ backtick outer documentation fences.
    """
    blocks = []
    lines = text.splitlines()
    in_outer = False
    outer_char = ""
    outer_len = 0

    in_mermaid = False
    mermaid_char = ""
    mermaid_len = 0
    mermaid_start_line = 0
    mermaid_buf = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.lstrip(" \t")
        m_fence = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)

        if in_mermaid:
            if m_fence and m_fence.group(1)[0] == mermaid_char and len(m_fence.group(1)) >= mermaid_len and not m_fence.group(2).strip():
                blocks.append({
                    "start_line": mermaid_start_line,
                    "content": "\n".join(mermaid_buf),
                })
                in_mermaid = False
                mermaid_buf = []
            else:
                mermaid_buf.append(line)
            continue

        if in_outer:
            if m_fence and m_fence.group(1)[0] == outer_char and len(m_fence.group(1)) >= outer_len and not m_fence.group(2).strip():
                in_outer = False
            continue

        if m_fence:
            ch = m_fence.group(1)[0]
            flen = len(m_fence.group(1))
            info = m_fence.group(2).strip()
            if ch == "~" or "`" not in info:
                if info.lower().split()[0:1] == ["mermaid"]:
                    in_mermaid = True
                    mermaid_char = ch
                    mermaid_len = flen
                    mermaid_start_line = idx
                    mermaid_buf = []
                else:
                    in_outer = True
                    outer_char = ch
                    outer_len = flen

    return blocks


def _strip_mermaid_frontmatter(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Strip optional leading YAML frontmatter block (`--- ... ---`) inside Mermaid."""
    i = 0
    while i < len(lines) and not lines[i][1].strip():
        i += 1
    if i < len(lines) and lines[i][1].strip() == "---":
        for j in range(i + 1, len(lines)):
            if lines[j][1].strip() == "---":
                return lines[j + 1:]
    return lines


def validate_mermaid_block(content: str, block_start_line: int) -> tuple[str | None, list[dict]]:
    """Validate one Mermaid block and return (diagram_type, findings)."""
    findings = []
    numbered_lines = [
        (block_start_line + offset + 1, raw)
        for offset, raw in enumerate(content.splitlines())
    ]
    numbered_lines = _strip_mermaid_frontmatter(numbered_lines)

    meaningful = [
        (ln, raw) for ln, raw in numbered_lines
        if raw.strip() and not raw.lstrip().startswith("%%")
    ]
    if not meaningful:
        findings.append({
            "line": block_start_line,
            "severity": "error",
            "rule": "empty-mermaid-block",
            "message": "Mermaid block contains no diagram definition.",
            "snippet": "```mermaid",
        })
        return None, findings

    header_ln, header_raw = meaningful[0]
    header_tok = header_raw.strip().split()[0]
    if header_tok not in SUPPORTED_TYPES:
        findings.append({
            "line": header_ln,
            "severity": "error",
            "rule": "unsupported-mermaid-type",
            "message": f"Unsupported Mermaid type '{header_tok}'; use flowchart, graph, sequenceDiagram, stateDiagram-v2, classDiagram, erDiagram, or xychart-beta.",
            "snippet": header_raw.strip()[:120],
        })

    if len(meaningful) > 45:
        findings.append({
            "line": header_ln,
            "severity": "info",
            "rule": "oversized-mermaid-diagram",
            "message": f"Mermaid block has {len(meaningful)} content lines (>45); split into smaller views or escalate to generative_ui.",
            "snippet": f"{header_raw.strip()[:80]} ({len(meaningful)} lines)",
        })

    is_flow = header_tok in ("flowchart", "graph")
    subgraph_depth = 0
    unbalanced_reported = False

    for ln, raw in meaningful:
        st = raw.strip()

        if HTML_TAG_RE.search(raw):
            findings.append({
                "line": ln,
                "severity": "warning",
                "rule": "html-tag-in-mermaid",
                "message": "Avoid HTML tags (<br>, <b>, etc.) inside Mermaid labels; use plain text or quoted lines.",
                "snippet": st[:120],
            })

        if is_flow:
            if UNQUOTED_PAREN_NODE_RE.search(raw):
                findings.append({
                    "line": ln,
                    "severity": "warning",
                    "rule": "unquoted-special-label",
                    "message": "Quote node labels containing parentheses as id[\"Label (Info)\"] to avoid Mermaid parse errors.",
                    "snippet": st[:120],
                })
            if re.match(r"^subgraph\b", st):
                subgraph_depth += 1
            elif re.match(r"^end\s*$", st):
                subgraph_depth -= 1
                if subgraph_depth < 0 and not unbalanced_reported:
                    unbalanced_reported = True
                    findings.append({
                        "line": ln,
                        "severity": "error",
                        "rule": "unbalanced-subgraph",
                        "message": "Unexpected 'end' without matching 'subgraph'.",
                        "snippet": st[:120],
                    })

    if is_flow and subgraph_depth > 0 and not unbalanced_reported:
        findings.append({
            "line": meaningful[-1][0],
            "severity": "error",
            "rule": "unbalanced-subgraph",
            "message": f"Unclosed Mermaid subgraph block ({subgraph_depth} missing 'end').",
            "snippet": meaningful[-1][1].strip()[:120],
        })

    return header_tok, findings


def analyze_markdown_diagrams(text: str, filename: str = "<stdin>") -> dict:
    """Validate all Mermaid blocks inside a Markdown document."""
    blocks = extract_mermaid_blocks(text)
    all_findings = []
    diagram_types = []

    for blk in blocks:
        dtype, b_findings = validate_mermaid_block(blk["content"], blk["start_line"])
        if dtype:
            diagram_types.append(dtype)
        all_findings.extend(b_findings)

    return {
        "file": filename,
        "diagrams_count": len(blocks),
        "diagram_types": diagram_types,
        "findings": all_findings,
    }


def collect_vault_markdown_files(project_root: str) -> list[str]:
    """Gather all .md files across wiki/, mem/, and output/ sorted deterministically."""
    files = []
    for top in ("wiki", "mem", "output"):
        top_dir = Path(project_root) / top
        if top_dir.is_dir():
            for p in sorted(top_dir.rglob("*.md")):
                files.append(str(p))
    return files


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Validate Mermaid diagrams across Markdown files or the tluc-wiki vault.")
    parser.add_argument("files", nargs="*", help="Markdown file paths to inspect")
    parser.add_argument("--stdin", action="store_true", help="Read Markdown content from stdin")
    parser.add_argument("--vault", action="store_true", help="Audit all .md files under wiki/, mem/, and output/")
    parser.add_argument("--project-root", default=None, help="Optional project root containing index.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any error or warning findings")
    parser.add_argument("--only-issues", action="store_true", help="Include only files with findings in results[]")
    args = parser.parse_args()

    if not args.files and not args.stdin and not args.vault:
        parser.error("Provide file path(s), --stdin, or --vault.")

    results = []
    summary = {"error": 0, "warning": 0, "info": 0}
    diagrams_checked = 0
    files_checked = 0

    if args.stdin:
        files_checked += 1
        res = analyze_markdown_diagrams(sys.stdin.read(), filename="<stdin>")
        diagrams_checked += res["diagrams_count"]
        if not args.only_issues or res["findings"]:
            results.append(res)

    target_paths = list(args.files)
    if args.vault:
        root = args.project_root or find_project_root()
        if not root:
            print(json.dumps({"status": "error", "error": "Could not locate project root (index.md)."}, indent=2))
            sys.exit(2)
        target_paths.extend(collect_vault_markdown_files(root))

    for path in target_paths:
        if not os.path.isfile(path):
            print(json.dumps({"status": "error", "error": f"File not found: {path}"}, ensure_ascii=False, indent=2))
            sys.exit(2)
        files_checked += 1
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        disp = path.replace("\\", "/")
        if args.vault:
            try:
                disp = Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
            except ValueError:
                pass
        res = analyze_markdown_diagrams(content, filename=disp)
        diagrams_checked += res["diagrams_count"]
        for finding in res["findings"]:
            summary[finding["severity"]] += 1
        if (not args.only_issues and res["diagrams_count"] > 0) or res["findings"]:
            results.append(res)

    if args.stdin:
        for finding in results[0]["findings"] if results else []:
            pass  # already counted below if needed; let's count cleanly
    if args.stdin:
        # Count stdin findings without double counting file findings
        summary = {"error": 0, "warning": 0, "info": 0}
        for res in results:
            for finding in res["findings"]:
                summary[finding["severity"]] += 1

    if summary["error"] > 0:
        status = "error"
    elif summary["warning"] > 0:
        status = "warn"
    else:
        status = "ok"

    report = {
        "status": status,
        "files_checked": files_checked,
        "diagrams_checked": diagrams_checked,
        "summary": summary,
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if summary["error"] > 0 or (args.strict and summary["warning"] > 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
