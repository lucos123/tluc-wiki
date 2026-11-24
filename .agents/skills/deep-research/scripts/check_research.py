#!/usr/bin/env python3
"""
Deterministic Epistemic & Citation Hygiene Checker for deep-research.

Audits Markdown research briefs (or stdin) for:
  - legacy-wikilink (error): stray [[...]] outside code blocks/spans
  - broken-local-citation (error): relative Markdown links resolving to missing files on disk
  - forbidden-certainty-weasel (warning): epistemics-banned weasel words outside blockquotes/code
  - uncited-direct-claim (warning): [Direct] / Direct Evidence bullets lacking any link or file citation
  - unvetted-benchmark-claim (warning): comparative speedup/latency/throughput/eval figures lacking provenance labels or citations
  - missing-unknowns-section (warning): briefs >= 100 words missing a What Remains Unknown section
  - missing-confidence-tiers (info): briefs >= 150 words without explicit epistemic tier labels
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

WIKILINK_RE = re.compile(r"\[\[([^\[\]\n]+)\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[([^\[\]\n]+)\]\(([^)\n]+)\)")
EXTERNAL_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
BACKTICK_FILE_RE = re.compile(r"`([^`\n]*(?:[\\/]|:\d+|\.(?:md|py|js|ts|tsx|json|yaml|yml|csv|pdf|jpg|png|webp))[^`\n]*)`")

WEASEL_PATTERNS = [
    r"\bobviously\b",
    r"\bclearly\b",
    r"\bof course\b",
    r"\bundoubtedly\b",
    r"\bi think\b",
    r"\bi believe\b",
    r"\bhiển nhiên là\b",
    r"\brõ ràng là\b",
    r"\btất nhiên là\b",
    r"\btôi nghĩ rằng\b",
    r"\btôi tin rằng\b",
]
WEASEL_RE = re.compile("|".join(WEASEL_PATTERNS), re.IGNORECASE)

BENCHMARK_CLAIM_RE = re.compile(
    r"(?:"
    r"\b\d+(?:\.\d+)?\s*[x×]\s*(?:faster|slower|speedup|higher\s+throughput|lower\s+latency|cheaper|more\s+efficient)\b"
    r"|\b\d+(?:\.\d+)?\s*%\s*(?:faster|slower|speedup|lower\s+latency|higher\s+throughput|regression|improvement|reduction\s+in\s+(?:latency|cost|tokens?))\b"
    r"|\b(?:speedup|p50|p95|p99|ttft|tps|throughput|latency|eval\s+score|benchmark\s+score)\b[^.\n]{0,40}\b\d+(?:\.\d+)?\s*(?:%|×(?=\W|$)|(?:ms|us|µs|s|x|pts?|req/s|tokens?/s)\b)"
    r")",
    re.IGNORECASE,
)
NON_MEASURED_LABEL_RE = re.compile(
    r"\b(?:estimate|estimated|inferred|unmeasured|speculative|ước\s+tính|ước\s+lượng|suy\s+luận|chưa\s+đo)\b",
    re.IGNORECASE,
)
MEASURED_LABEL_RE = re.compile(
    r"\b(?:measured|median|trials?|runs?|đo\s+thực\s+tế|trung\s+vị)\b",
    re.IGNORECASE,
)

DIRECT_TAG_RE = re.compile(r"(?:\[\s*Direct\s*\]|\*\*\s*Direct\s*\*\*\s*:?)", re.IGNORECASE)
DIRECT_SECTION_RE = re.compile(r"^#{2,3}\s+.*\b(Direct Evidence|Verified Findings|Direct Findings)\b", re.IGNORECASE)
UNKNOWNS_HEADING_RE = re.compile(
    r"^#{2,3}\s+.*(?:unknown|uncertaint|gap|limitation|open question|chưa xác minh|còn bỏ ngỏ|giới hạn)",
    re.IGNORECASE,
)
TIER_LABEL_RE = re.compile(r"\b(Direct|Supported|Inferred|Speculative|Unknown)\b", re.IGNORECASE)


def split_frontmatter(text: str) -> tuple[int, str]:
    """Return (body_start_line_1based, body_text)."""
    m = re.match(r"^---\r?\n.*?\r?\n---\r?\n?", text, re.S)
    if not m:
        return 1, text
    return m.group(0).count("\n") + 1, text[m.end():]


def strip_inline_code(line: str) -> str:
    """Replace inline code spans with spaces while preserving line layout."""
    return re.sub(r"`+[^`\n]+`+", lambda m: " " * len(m.group(0)), line)


def iter_non_code_lines(body: str, start_line: int):
    """Yield (line_no, raw_line, cleaned_no_inline_code, is_blockquote) outside fenced code blocks."""
    in_fence = False
    fence_char = ""
    fence_len = 0

    for offset, raw_line in enumerate(body.splitlines()):
        line_no = start_line + offset
        stripped = raw_line.lstrip(" \t")
        m_fence = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)

        if not in_fence:
            if m_fence:
                ch = m_fence.group(1)[0]
                rest = m_fence.group(2)
                if ch == "~" or "`" not in rest:
                    in_fence = True
                    fence_char = ch
                    fence_len = len(m_fence.group(1))
                    continue
        else:
            if re.match(rf"^{re.escape(fence_char)}{{{fence_len},}}[ \t]*$", stripped):
                in_fence = False
                continue
            continue

        yield line_no, raw_line, strip_inline_code(raw_line), stripped.startswith(">")


def has_citation(raw_line: str) -> bool:
    """Check whether a line includes a Markdown link, external URL, or backticked file/line reference."""
    if MD_LINK_RE.search(raw_line):
        return True
    if EXTERNAL_URL_RE.search(raw_line):
        return True
    if BACKTICK_FILE_RE.search(raw_line):
        return True
    return False


def _clean_local_target(raw_href: str) -> str | None:
    href = raw_href.strip()
    if href.startswith("<") and href.endswith(">"):
        href = href[1:-1].strip()
    if not href or href.startswith("#"):
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*:", href.lower()):
        return None
    path_part = href.partition("#")[0].strip()
    if not path_part:
        return None
    return unquote(path_part)


def analyze_research_brief(text: str, filename: str = "<stdin>", file_dir: Path | None = None) -> dict:
    """Audit one research brief for citation integrity, epistemic tiers, and phrasing discipline."""
    start_line, body = split_frontmatter(text)
    findings = []
    tier_counts = {"direct": 0, "supported": 0, "inferred": 0, "speculative": 0, "unknown": 0}
    has_unknowns_section = False
    in_direct_section = False
    total_words = 0

    for line_no, raw_line, cleaned, is_quote in iter_non_code_lines(body, start_line):
        total_words += len(re.findall(r"[^\W_]+", cleaned))
        stripped = raw_line.strip()

        if re.match(r"^#{2,3}\s+", stripped):
            in_direct_section = bool(DIRECT_SECTION_RE.match(stripped))
            if UNKNOWNS_HEADING_RE.match(stripped):
                has_unknowns_section = True

        # Track confidence tiers mentioned
        for tm in TIER_LABEL_RE.finditer(cleaned):
            tier_counts[tm.group(1).lower()] += 1

        # 1. Legacy wikilink check (error)
        for wm in WIKILINK_RE.finditer(cleaned):
            inner = wm.group(1)
            if "[" in inner or "]" in inner:
                continue
            findings.append({
                "line": line_no,
                "severity": "error",
                "rule": "legacy-wikilink",
                "message": f"Replace legacy wikilink '[[{inner}]]' with a Standard Relative Markdown Link.",
                "snippet": stripped[:140],
            })

        # 2. Broken relative Markdown citation check (error, when file_dir is known)
        if file_dir is not None:
            for lm in MD_LINK_RE.finditer(cleaned):
                target = _clean_local_target(lm.group(2))
                if target is None:
                    continue
                resolved = (file_dir / target).resolve()
                if not resolved.is_file():
                    findings.append({
                        "line": line_no,
                        "severity": "error",
                        "rule": "broken-local-citation",
                        "message": f"Citation target does not exist: '{lm.group(2).strip()}'.",
                        "snippet": stripped[:140],
                    })

        # 3. Certainty weasel words (warning, ignore verbatim blockquotes)
        if not is_quote:
            for wz in WEASEL_RE.finditer(cleaned):
                findings.append({
                    "line": line_no,
                    "severity": "warning",
                    "rule": "forbidden-certainty-weasel",
                    "message": f"Remove certainty/opinion phrase '{wz.group(0)}' and cite direct evidence or hedge explicitly.",
                    "snippet": stripped[:140],
                })

        # 4. Uncited [Direct] claims or bullets inside Direct Evidence sections (warning)
        if not is_quote and stripped and not stripped.startswith("#"):
            is_direct_claim = bool(DIRECT_TAG_RE.search(cleaned)) or (in_direct_section and stripped.startswith(("-", "*")))
            if is_direct_claim and not has_citation(raw_line):
                findings.append({
                    "line": line_no,
                    "severity": "warning",
                    "rule": "uncited-direct-claim",
                    "message": "Direct claim has no inline link, URL, or backticked file:line citation.",
                    "snippet": stripped[:140],
                })

        # 5. Unvetted benchmark / performance claims (warning)
        if not is_quote and stripped and not stripped.startswith(("#", "|")) and BENCHMARK_CLAIM_RE.search(cleaned):
            has_unmeasured_label = bool(NON_MEASURED_LABEL_RE.search(cleaned))
            has_vetted_measured = bool(MEASURED_LABEL_RE.search(cleaned)) and has_citation(raw_line)
            if not (has_unmeasured_label or has_vetted_measured):
                findings.append({
                    "line": line_no,
                    "severity": "warning",
                    "rule": "unvetted-benchmark-claim",
                    "message": "Benchmark claim lacks provenance or uncertainty label; attach 'measured' + source citation after vetting (limiter, repeats, variance) or mark as estimate/inferred/unmeasured per epistemics.md.",
                    "snippet": stripped[:140],
                })

    if total_words >= 100 and not has_unknowns_section:
        findings.append({
            "line": start_line,
            "severity": "warning",
            "rule": "missing-unknowns-section",
            "message": "Research brief >= 100 words lacks an explicit 'What Remains Unknown' / gaps section.",
            "snippet": f"Document ({total_words} words)",
        })

    if total_words >= 150 and sum(tier_counts.values()) == 0:
        findings.append({
            "line": start_line,
            "severity": "info",
            "rule": "missing-confidence-tiers",
            "message": "Research brief >= 150 words has no epistemic confidence tier labels (Direct/Supported/Inferred/Speculative/Unknown).",
            "snippet": f"Document ({total_words} words)",
        })

    return {
        "file": filename,
        "word_count": total_words,
        "tier_counts": tier_counts,
        "has_unknowns_section": has_unknowns_section,
        "findings": findings,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Validate epistemic rigor and citations in Markdown research briefs.")
    parser.add_argument("files", nargs="*", help="Markdown file paths to inspect")
    parser.add_argument("--stdin", action="store_true", help="Read Markdown content from stdin")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any error or warning findings")
    args = parser.parse_args()

    if not args.files and not args.stdin:
        parser.error("Provide at least one file path or pass --stdin.")

    results = []
    summary = {"error": 0, "warning": 0, "info": 0}

    if args.stdin:
        results.append(analyze_research_brief(sys.stdin.read(), filename="<stdin>", file_dir=None))

    for raw_path in args.files:
        p = Path(raw_path)
        if not p.is_file():
            print(json.dumps({"status": "error", "error": f"File not found: {raw_path}"}, ensure_ascii=False, indent=2))
            sys.exit(2)
        text = p.read_text(encoding="utf-8", errors="replace")
        results.append(analyze_research_brief(text, filename=raw_path.replace("\\", "/"), file_dir=p.resolve().parent))

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
        "files_checked": len(results),
        "summary": summary,
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if summary["error"] > 0 or (args.strict and summary["warning"] > 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
