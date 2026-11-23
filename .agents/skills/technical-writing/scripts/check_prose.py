#!/usr/bin/env python3
"""
Deterministic Prose & Markdown Hygiene Checker for technical-writing.

Audits Markdown files (or stdin) against tluc-wiki's technical-writing rules:
  - legacy-wikilink (error): stray [[...]] outside code spans/fences
  - ai-filler-phrase (warning): EN/VI AI throat-clearing & cliché phrasing
  - vague-unquantified-claim (warning): unquantified comparatives without digits or citations
  - katex-currency-collision (warning): unescaped currency $ pairs risking KaTeX math rendering
  - dense-related-links (warning): >= 3 links packed onto one bullet inside ## Related* sections
  - long-intro-wall (info): opening prose > 140 words before first heading/list/table
"""

import argparse
import json
import os
import re
import sys


AI_FILLER_PATTERNS = [
    r"\bin today'?s fast-paced\b",
    r"\bit is important to note that\b",
    r"\bit(?:'s| is) worth noting\b",
    r"\bdelve into\b",
    r"\bleverage the power of\b",
    r"\bgame[- ]changer\b",
    r"\bseamless(?:ly)?\b",
    r"\btapestry\b",
    r"\bneedless to say\b",
    r"\bcomprehensive overview\b",
    r"\btrong thời đại công nghệ phát triển nhanh chóng\b",
    r"\bkhông thể phủ nhận rằng\b",
    r"\bđóng vai trò vô cùng quan trọng\b",
    r"\bnhư chúng ta đã biết\b",
    r"\btổng kết lại có thể thấy\b",
]
AI_FILLER_RE = re.compile("|".join(AI_FILLER_PATTERNS), re.IGNORECASE)

VAGUE_CLAIM_RE = re.compile(
    r"\b(?:"
    r"significantly\s+(?:faster|slower|better|worse|improved|reduces?|increases?)"
    r"|much\s+(?:faster|slower|better|worse)"
    r"|blazingly\s+fast"
    r"|vastly\s+improved"
    r"|dramatically\s+(?:reduces?|improves?|faster|better)"
    r"|nhanh\s+hơn\s+rất\s+nhiều"
    r"|cải\s+thiện\s+đáng\s+kể"
    r"|tối\s+ưu\s+vượt\s+trội"
    r")\b",
    re.IGNORECASE,
)

WIKILINK_RE = re.compile(r"\[\[([^\[\]\n]+)\]\]")
MD_LINK_RE = re.compile(r"\[[^\[\]\n]+\]\([^)\n]+\)")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")
CURRENCY_RE = re.compile(
    r"(?<!\\)\$\d+(?:[.,]\d+)*(?:[KMBTkmbt](?![\w\^_{}\\])|(?![\d.,A-Za-z\^_{}\\+\-*=<>]))"
)


def split_frontmatter(text: str) -> tuple[str, int, str]:
    """Return (frontmatter_text, body_start_line_1based, body_text)."""
    m = re.match(r"^---\r?\n.*?\r?\n---\r?\n?", text, re.S)
    if not m:
        return "", 1, text
    fm_block = m.group(0)
    body = text[m.end():]
    start_line = fm_block.count("\n") + 1
    return fm_block, start_line, body


def strip_inline_code(line: str) -> str:
    """Replace inline code spans with spaces of equal length to preserve column context cleanly."""
    return re.sub(r"`+[^`\n]+`+", lambda m: " " * len(m.group(0)), line)


def iter_non_code_lines(body: str, start_line: int):
    """Yield (line_no, raw_line, cleaned_no_inline_code, is_blockquote) skipping fenced code blocks."""
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

        is_quote = stripped.startswith(">")
        cleaned = strip_inline_code(raw_line)
        yield line_no, raw_line, cleaned, is_quote


def add_finding(findings: list, line_no: int, severity: str, rule: str, message: str, snippet: str):
    findings.append({
        "line": line_no,
        "severity": severity,
        "rule": rule,
        "message": message,
        "snippet": snippet.strip()[:140],
    })


def _check_currency_line(line_no: int, raw_line: str, cleaned: str, findings: list):
    """Flag lines with >=2 unescaped single $ where currency syntax risks KaTeX math capture."""
    if "$$" in cleaned:
        no_display = re.sub(r"\$\$[^$]*\$\$", "", cleaned)
    else:
        no_display = cleaned

    unescaped_dollars = re.findall(r"(?<!\\)\$", no_display)
    if len(unescaped_dollars) < 2:
        return
    if not CURRENCY_RE.search(no_display):
        return
    add_finding(
        findings,
        line_no,
        "warning",
        "katex-currency-collision",
        "Multiple unescaped '$' with currency value may cause KaTeX to render intervening prose as math; escape as '\\$' or wrap in backticks.",
        raw_line,
    )


def _check_vague_claims_on_line(line_no: int, raw_line: str, cleaned: str, is_quote: bool, findings: list):
    """Flag unquantified vague comparative claims lacking digits or Markdown link citations."""
    if is_quote:
        return
    for seg in SENTENCE_SPLIT_RE.split(cleaned):
        if not seg.strip():
            continue
        matches = list(VAGUE_CLAIM_RE.finditer(seg))
        if not matches:
            continue
        has_number = bool(re.search(r"\d", seg))
        has_citation = bool(MD_LINK_RE.search(seg))
        if not has_number and not has_citation:
            for m in matches:
                add_finding(
                    findings,
                    line_no,
                    "warning",
                    "vague-unquantified-claim",
                    f"Replace unquantified claim '{m.group(0)}' with a concrete metric (number/unit) or cited link.",
                    seg,
                )


def _check_long_intro(body: str, start_line: int, findings: list):
    """Emit info finding if opening prose before the first H2/list/table exceeds 140 words."""
    intro_words = 0
    intro_line = start_line
    saw_h1 = False
    in_prose = False

    for line_no, raw_line, cleaned, is_quote in iter_non_code_lines(body, start_line):
        st = raw_line.strip()
        if not st:
            continue
        if st.startswith("# ") and not saw_h1:
            saw_h1 = True
            continue
        if st.startswith(("## ", "### ", "- ", "* ", "|", "---")):
            break
        if re.match(r"^\d+\.\s", st):
            break
        if not in_prose:
            in_prose = True
            intro_line = line_no
        if not is_quote:
            intro_words += len(re.findall(r"[^\W_]+", cleaned))

    if intro_words > 140:
        add_finding(
            findings,
            intro_line,
            "info",
            "long-intro-wall",
            f"Opening prose before first section/list/table is {intro_words} words (>140); tighten into outcome-first layered summary.",
            f"Intro block ({intro_words} words)",
        )


def analyze_markdown(text: str, filename: str = "<stdin>") -> dict:
    """Analyze one Markdown document and return structured hygiene report."""
    _fm, start_line, body = split_frontmatter(text)
    findings = []
    in_related = False
    total_words = 0

    for line_no, raw_line, cleaned, is_quote in iter_non_code_lines(body, start_line):
        total_words += len(re.findall(r"[^\W_]+", cleaned))
        stripped = raw_line.strip()

        if re.match(r"^##\s+Related\b", stripped):
            in_related = True
        elif re.match(r"^##\s+", stripped):
            in_related = False

        # 1. Legacy wikilink check (error)
        for m in WIKILINK_RE.finditer(cleaned):
            inner = m.group(1)
            if "[" in inner or "]" in inner:
                continue
            add_finding(
                findings,
                line_no,
                "error",
                "legacy-wikilink",
                f"Legacy wikilink '[[{inner}]]' violates Standard Relative Markdown Link convention.",
                raw_line,
            )

        # 2. AI filler phrase check (warning, ignore blockquotes so verbatim quotes pass cleanly)
        if not is_quote:
            for m_filler in AI_FILLER_RE.finditer(cleaned):
                add_finding(
                    findings,
                    line_no,
                    "warning",
                    "ai-filler-phrase",
                    f"Remove AI filler/throat-clearing phrase '{m_filler.group(0)}'.",
                    raw_line,
                )

        # 3. Vague unquantified comparative claims (warning)
        _check_vague_claims_on_line(line_no, raw_line, cleaned, is_quote, findings)

        # 4. Unescaped currency $ KaTeX collision check (warning)
        _check_currency_line(line_no, raw_line, cleaned, findings)

        # 5. Dense >=3-link line inside ## Related* sections (warning)
        if in_related and stripped.startswith(("-", "*")):
            link_count = len(MD_LINK_RE.findall(cleaned))
            if link_count >= 3:
                add_finding(
                    findings,
                    line_no,
                    "warning",
                    "dense-related-links",
                    f"Related section bullet packs {link_count} links on one line; expand into nested sub-bullets.",
                    raw_line,
                )

    # 6. Oversized opening wall check (info)
    _check_long_intro(body, start_line, findings)

    return {
        "file": filename,
        "word_count": total_words,
        "findings": findings,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Check Markdown prose quality and tluc-wiki formatting conventions.")
    parser.add_argument("files", nargs="*", help="Markdown file paths to check")
    parser.add_argument("--stdin", action="store_true", help="Read Markdown content from stdin")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any error or warning findings exist")
    args = parser.parse_args()

    if not args.files and not args.stdin:
        parser.error("Provide at least one file path or pass --stdin.")

    results = []
    summary = {"error": 0, "warning": 0, "info": 0}

    if args.stdin:
        content = sys.stdin.read()
        res = analyze_markdown(content, filename="<stdin>")
        results.append(res)

    for path in args.files:
        if not os.path.isfile(path):
            print(json.dumps({"status": "error", "error": f"File not found: {path}"}, ensure_ascii=False, indent=2))
            sys.exit(2)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        results.append(analyze_markdown(content, filename=path.replace("\\", "/")))

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
