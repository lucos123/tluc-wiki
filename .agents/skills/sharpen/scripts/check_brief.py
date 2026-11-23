#!/usr/bin/env python3
"""
Deterministic Brief & Playback Hygiene Validator for sharpen skill.

Checks written task briefs (`--mode brief`) or goal playbacks (`--mode playback`) for:
  - legacy-wikilink (error): stray [[...]] outside code blocks/spans
  - missing-required-element (warning): missing Consumer/Goal/Done-Check/Non-Goals (brief)
    or Goal/Problem-or-Assumptions/Success-Check (playback)
  - missing-observable-check (warning): Done-Check uses subjective words only or lacks observable check
  - echo-copy-detected (warning): Playback echoes --original prompt too closely without paraphrasing
  - brief-overspecified (info): Concise brief exceeds 250 words
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\[\]\n]+)\]\]")
MD_LINK_RE = re.compile(r"\[[^\[\]\n]+\]\([^)\n]+\)")

ELEMENT_PATTERNS = {
    "consumer": re.compile(
        r"\b(?:consumer|audience|reader|target\s+user|beneficiary|người\s+dùng|đối\s+tượng|người\s+đọc|người\s+hưởng\s+lợi)\b",
        re.IGNORECASE,
    ),
    "goal": re.compile(
        r"\b(?:goal|outcome|objective|deliverable|observable\s+change|mục\s+tiêu|kết\s+quả)\b",
        re.IGNORECASE,
    ),
    "problem_or_assumptions": re.compile(
        r"\b(?:problem|blocker|obstacle|assumption|assumptions|vấn\s+đề|giả\s+định|trở\s+ngại|rào\s+cản)\b",
        re.IGNORECASE,
    ),
    "done_check": re.compile(
        r"\b(?:done[- ]check|success\s+check|verification|acceptance|outside\s+check|tiêu\s+chí\s+hoàn\s+thành|kiểm\s+chứng|điều\s+kiện\s+xong)\b",
        re.IGNORECASE,
    ),
    "non_goals": re.compile(
        r"\b(?:non[- ]goals?|out\s+of\s+scope|explicitly\s+excluded|không\s+làm|ngoài\s+phạm\s+vi)\b",
        re.IGNORECASE,
    ),
}

SUBJECTIVE_ONLY_RE = re.compile(
    r"\b(?:looks?\s+good|high\s+quality|works?\s+well|clean(?:er)?|nice|better|hoàn\s+hảo|tốt\s+hơn|đẹp\s+hơn|ổn\s+áp)\b",
    re.IGNORECASE,
)
OBSERVABLE_SIGNAL_RE = re.compile(
    r"(?:\d|`[^`\n]+`|\[[^\[\]\n]+\]\([^)\n]+\)|\b(?:pass|passes|fail|fails|exit|exits|render|renders|click|return|returns|count|diff|test|tests|lint|build|verify|check|chạy|trả\s+về|khớp|mở\s+được|kiểm\s+tra|đạt)\b)",
    re.IGNORECASE,
)


def split_frontmatter(text: str) -> tuple[int, str]:
    """Return (body_start_line_1based, body_text)."""
    m = re.match(r"^---\r?\n.*?\r?\n---\r?\n?", text, re.S)
    if not m:
        return 1, text
    return m.group(0).count("\n") + 1, text[m.end():]


def strip_inline_code(line: str) -> str:
    return re.sub(r"`+[^`\n]+`+", lambda m: " " * len(m.group(0)), line)


def iter_non_code_lines(body: str, start_line: int):
    """Yield (line_no, raw_line, cleaned_no_inline_code) skipping fenced code blocks."""
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

        yield line_no, raw_line, strip_inline_code(raw_line)


def _is_labeled_element(raw_line: str, pattern: re.Pattern) -> bool:
    stripped = raw_line.strip()
    if re.match(r"^#{1,3}\s+", stripped):
        return bool(pattern.search(stripped))
    if re.match(r"^(?:[-*]|\d+\.)\s+\*\*[^*]+\*\*", stripped) or re.match(r"^(?:[-*]|\d+\.)\s+[^:]+:", stripped) or re.match(r"^[A-Za-zÀ-ỹ\s/_-]+:", stripped):
        head = stripped.split(":", 1)[0]
        return bool(pattern.search(head))
    return False


def _extract_done_check_spans(lines_list: list[tuple[int, str, str]]) -> list[tuple[int, str]]:
    """Collect (line_no, full_done_check_text) spans from labeled lines or headings."""
    spans = []
    i = 0
    while i < len(lines_list):
        ln, raw, _cleaned = lines_list[i]
        st = raw.strip()
        if _is_labeled_element(raw, ELEMENT_PATTERNS["done_check"]):
            parts = []
            if ":" in st and not st.startswith("#"):
                parts.append(st.split(":", 1)[1].strip())
            j = i + 1
            while j < len(lines_list):
                nxt_raw = lines_list[j][1]
                nxt_st = nxt_raw.strip()
                if not nxt_st:
                    j += 1
                    continue
                if re.match(r"^#{1,3}\s+", nxt_st):
                    break
                if any(_is_labeled_element(nxt_raw, pat) for pat in ELEMENT_PATTERNS.values()):
                    break
                if not st.startswith("#") and re.match(r"^(?:[-*]|\d+\.)\s+\*\*", nxt_st):
                    break
                parts.append(nxt_st)
                j += 1
            spans.append((ln, " ".join(p for p in parts if p)))
            i = j
            continue
        i += 1
    return spans


def _token_set(text: str) -> set[str]:
    return {t for t in re.findall(r"[^\W_]+", text.lower()) if len(t) >= 2}


def analyze_brief(
    text: str,
    filename: str = "<stdin>",
    mode: str = "brief",
    original_prompt: str | None = None,
) -> dict:
    """Validate sharpened brief or goal playback against sharpen criteria."""
    start_line, body = split_frontmatter(text)
    lines_list = list(iter_non_code_lines(body, start_line))
    findings = []

    required_keys = (
        ["consumer", "goal", "done_check", "non_goals"]
        if mode == "brief"
        else ["goal", "problem_or_assumptions", "done_check"]
    )
    elements_found = {k: False for k in required_keys}
    total_words = 0

    for line_no, raw_line, cleaned in lines_list:
        total_words += len(re.findall(r"[^\W_]+", cleaned))

        # 1. Legacy wikilink check (error)
        for wm in WIKILINK_RE.finditer(cleaned):
            inner = wm.group(1)
            if "[" in inner or "]" in inner or re.fullmatch(r"[\d\s,.\-+*/eE;]+", inner):
                continue
            findings.append({
                "line": line_no,
                "severity": "error",
                "rule": "legacy-wikilink",
                "message": f"Replace legacy wikilink '[[{inner}]]' with a Standard Relative Markdown Link.",
                "snippet": raw_line.strip()[:140],
            })

        # Track labeled elements
        for key in required_keys:
            if _is_labeled_element(raw_line, ELEMENT_PATTERNS[key]):
                elements_found[key] = True

    # 2. Required elements check (warning)
    for key in required_keys:
        if not elements_found[key]:
            findings.append({
                "line": start_line,
                "severity": "warning",
                "rule": "missing-required-element",
                "message": f"Missing '{key}' label/section required for {mode} mode.",
                "snippet": f"Missing element: {key}",
            })

    # 3. Observable done-check check (warning)
    done_spans = _extract_done_check_spans(lines_list)
    for ln, span_text in done_spans:
        if not span_text.strip():
            findings.append({
                "line": ln,
                "severity": "warning",
                "rule": "missing-observable-check",
                "message": "Done-check/Success-check is empty; name a concrete command, count, test, or observable outcome.",
                "snippet": "Empty done-check",
            })
            continue
        has_obs = bool(OBSERVABLE_SIGNAL_RE.search(span_text))
        is_subjective = bool(SUBJECTIVE_ONLY_RE.search(span_text)) and not re.search(r"\d|`[^`\n]+`", span_text)
        if not has_obs or is_subjective:
            findings.append({
                "line": ln,
                "severity": "warning",
                "rule": "missing-observable-check",
                "message": "Done-check lacks an observable pass condition (command, digit/metric, test, or render check).",
                "snippet": span_text[:140],
            })

    # 4. Paraphrase vs verbatim echo check (warning when --original provided)
    if original_prompt:
        orig_tokens = _token_set(original_prompt)
        body_tokens = _token_set(body)
        if len(orig_tokens) >= 6:
            union = orig_tokens | body_tokens
            jaccard = len(orig_tokens & body_tokens) / len(union) if union else 0.0
            norm_orig = re.sub(r"\s+", " ", original_prompt.strip().lower())
            norm_body = re.sub(r"\s+", " ", body.strip().lower())
            verbatim_contained = len(norm_orig) >= 24 and norm_orig in norm_body
            goal_lines = [
                raw.split(":", 1)[1] if ":" in raw else raw
                for _ln, raw, _cl in lines_list
                if _is_labeled_element(raw, ELEMENT_PATTERNS["goal"])
            ]
            goal_tokens = _token_set(" ".join(goal_lines))
            goal_overlap = len(orig_tokens & goal_tokens) / len(orig_tokens) if orig_tokens else 0.0
            if jaccard >= 0.85 or verbatim_contained or goal_overlap >= 0.85:
                findings.append({
                    "line": start_line,
                    "severity": "warning",
                    "rule": "echo-copy-detected",
                    "message": "Text closely echoes the original prompt instead of paraphrasing into concrete consumer/goal/check terms.",
                    "snippet": body.strip()[:140],
                })

    # 5. Conciseness check (info)
    if total_words > 250:
        findings.append({
            "line": start_line,
            "severity": "info",
            "rule": "brief-overspecified",
            "message": f"Brief has {total_words} words (>250); trim implementation details and keep focus on target/check.",
            "snippet": f"Brief ({total_words} words)",
        })

    return {
        "file": filename,
        "word_count": total_words,
        "elements_found": elements_found,
        "findings": findings,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Validate sharpened task briefs and goal playbacks.")
    parser.add_argument("files", nargs="*", help="Markdown brief file(s) to check")
    parser.add_argument("--stdin", action="store_true", help="Read brief content from stdin")
    parser.add_argument("--mode", choices=("brief", "playback"), default="brief", help="Validation schema mode")
    parser.add_argument("--original", default=None, help="Optional original request text to detect verbatim echoes")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any error or warning findings")
    args = parser.parse_args()

    if not args.files and not args.stdin:
        parser.error("Provide at least one file path or pass --stdin.")

    results = []
    summary = {"error": 0, "warning": 0, "info": 0}

    if args.stdin:
        results.append(analyze_brief(sys.stdin.read(), filename="<stdin>", mode=args.mode, original_prompt=args.original))

    for raw_path in args.files:
        p = Path(raw_path)
        if not p.is_file():
            print(json.dumps({"status": "error", "error": f"File not found: {raw_path}"}, ensure_ascii=False, indent=2))
            sys.exit(2)
        text = p.read_text(encoding="utf-8", errors="replace")
        results.append(analyze_brief(text, filename=raw_path.replace("\\", "/"), mode=args.mode, original_prompt=args.original))

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
        "mode": args.mode,
        "files_checked": len(results),
        "summary": summary,
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if summary["error"] > 0 or (args.strict and summary["warning"] > 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
