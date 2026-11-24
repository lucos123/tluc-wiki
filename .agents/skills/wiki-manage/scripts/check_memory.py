#!/usr/bin/env python3
"""Deterministic hygiene, schema, secret, and link checker for mem/**/*.md."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import datetime
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import unquote

VALID_STATUSES = {"active", "completed", "paused", "planned"}

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("OpenAI-style secret key", re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{16,}")),
    ("GitHub token", re.compile(r"(?<![A-Za-z0-9_-])gh[pousr]_[A-Za-z0-9]{20,}")),
    ("Google API key", re.compile(r"(?<![A-Za-z0-9_-])AIza[0-9A-Za-z_-]{20,}")),
    ("AWS access key ID", re.compile(r"(?<![A-Za-z0-9_-])AKIA[0-9A-Z]{16}")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "Credential assignment",
        re.compile(
            r"""(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*["']?([A-Za-z0-9._/+=-]{12,})["']?"""
        ),
    ),
)

PLACEHOLDER_MARKERS = ("YOUR_", "EXAMPLE", "REDACTED", "DUMMY", "TEST_", "<", ">", "*", "{", "}")

WIKILINK_RE = re.compile(r"\[\[[^\]\n]+\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\n]+)\)")
INLINE_CODE_RE = re.compile(r"(``+)([^`\n]+?)\1|`([^`\n]+?)`")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
LIST_ITEM_RE = re.compile(r"^\s+-\s+(.+?)\s*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HYPOTHESIS_RE = re.compile(r"(?i)(?:\[\s*Hypothesis\s*\]|\bUnconfirmed\s*:|\bTBD\b|\bTODO\s*:)")

EXTERNAL_SCHEME_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "file://",
    "conversation://",
    "sidecar://",
    "tel:",
)


@dataclass(frozen=True)
class Finding:
    """Represents a single memory lint finding."""

    severity: str
    code: str
    file: str
    line: int
    message: str


@dataclass
class MemoryFrontmatter:
    """Parsed YAML frontmatter fields for a memory Markdown file."""

    fields: dict[str, Any]
    field_lines: dict[str, int]
    body_start_line: int


def _ensure_utf8_stdio() -> None:
    """Configure UTF-8 stdout/stderr on Windows consoles when available."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def _strip_inline_comment(value: str) -> str:
    """Strip unquoted trailing YAML # comment from a scalar value."""
    in_single = False
    in_double = False
    for idx, ch in enumerate(value):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if idx == 0 or value[idx - 1].isspace():
                return value[:idx].rstrip()
    return value.strip()


def _strip_quotes(value: str) -> str:
    """Strip matching surrounding single or double quotes after removing comments."""
    cleaned = _strip_inline_comment(value).strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in ("'", '"'):
        return cleaned[1:-1]
    return cleaned


def parse_frontmatter(lines: list[str]) -> MemoryFrontmatter | None:
    """Parse minimal YAML frontmatter from file lines. Return None if absent."""
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return None

    end_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() in ("---", "..."):
            end_idx = idx
            break
    if end_idx is None:
        return None

    fields: dict[str, Any] = {}
    field_lines: dict[str, int] = {}

    i = 1
    while i < end_idx:
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue

        match = TOP_KEY_RE.match(raw)
        if not match:
            i += 1
            continue

        key = match.group(1)
        val_raw = match.group(2).strip()
        field_lines[key] = i + 1

        if val_raw == "":
            list_items: list[str] = []
            i += 1
            while i < end_idx:
                nxt = lines[i]
                if not nxt.strip():
                    i += 1
                    continue
                item_match = LIST_ITEM_RE.match(nxt)
                if item_match:
                    item_val = _strip_quotes(item_match.group(1))
                    if item_val:
                        list_items.append(item_val)
                    i += 1
                    continue
                if nxt[0] in (" ", "\t"):
                    i += 1
                    continue
                break
            fields[key] = list_items
            continue

        cleaned_raw = _strip_inline_comment(val_raw)
        if cleaned_raw.startswith("[") and cleaned_raw.endswith("]"):
            fields[key] = [
                _strip_quotes(part)
                for part in cleaned_raw[1:-1].split(",")
                if _strip_quotes(part)
            ]
        else:
            fields[key] = _strip_quotes(val_raw)
        i += 1

    return MemoryFrontmatter(
        fields=fields,
        field_lines=field_lines,
        body_start_line=end_idx + 2,
    )


def _iter_non_code_lines(lines: list[str], start_line: int) -> list[tuple[int, str]]:
    """Return (1-based line_no, text_without_inline_code) outside fenced code blocks."""
    result: list[tuple[int, str]] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line_no in range(start_line, len(lines) + 1):
        line = lines[line_no - 1]
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0
                continue

        if in_fence:
            continue

        result.append((line_no, INLINE_CODE_RE.sub(" ", line)))

    return result


def _is_placeholder_secret(matched_text: str) -> bool:
    """Return True if a matched secret token is clearly a template placeholder."""
    upper = matched_text.upper()
    return any(marker in upper for marker in PLACEHOLDER_MARKERS)


def _is_external_or_placeholder(href: str) -> bool:
    """Return True if href points outside the workspace or uses template syntax."""
    lower = href.lower()
    if not href or href.startswith("#"):
        return True
    if any(lower.startswith(prefix) for prefix in EXTERNAL_SCHEME_PREFIXES):
        return True
    if any(ch in href for ch in ("<", ">", "{", "}", "*")):
        return True
    return False


def _clean_href_target(raw_href: str) -> str:
    """Extract normalized relative path from a Markdown link target."""
    href = raw_href.strip()
    if href.startswith("<") and ">" in href:
        href = href[1 : href.index(">")].strip()
    else:
        title_match = re.match(r'^(\S+)\s+["\'].*["\']$', href)
        if title_match:
            href = title_match.group(1)
    if "#" in href:
        href = href.split("#", 1)[0]
    return unquote(href)


def lint_memory_file(md_file: Path, project_root: Path) -> list[Finding]:
    """Audit one Markdown file in mem/ for schema, secrets, links, and hypotheses."""
    rel_file = md_file.relative_to(project_root).as_posix()
    lines = md_file.read_text(encoding="utf-8").splitlines()
    findings: list[Finding] = []

    for line_no, raw_line in enumerate(lines, 1):
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(raw_line):
                candidate = match.group(1) if match.lastindex else match.group(0)
                if _is_placeholder_secret(match.group(0)) or _is_placeholder_secret(candidate):
                    continue
                findings.append(
                    Finding(
                        severity="error",
                        code="secret-leak",
                        file=rel_file,
                        line=line_no,
                        message=f"Potential {label} detected; remove secrets/tokens from `mem/`.",
                    )
                )

    fm = parse_frontmatter(lines)
    if fm is None:
        findings.append(
            Finding(
                severity="error",
                code="missing-frontmatter",
                file=rel_file,
                line=1,
                message="Memory page must start with YAML frontmatter delimited by `---`.",
            )
        )
        body_start = 1
    else:
        body_start = fm.body_start_line
        for req in ("title", "date", "tags"):
            val = fm.fields.get(req)
            if val is None or (isinstance(val, str) and not val.strip()) or (isinstance(val, list) and not val):
                findings.append(
                    Finding(
                        severity="error",
                        code="missing-field",
                        file=rel_file,
                        line=fm.field_lines.get(req, 1),
                        message=f"Frontmatter is missing required field `{req}`.",
                    )
                )

        if "date" in fm.fields:
            date_val = str(fm.fields["date"]).strip()
            valid_date = bool(DATE_RE.match(date_val))
            if valid_date:
                try:
                    datetime.date.fromisoformat(date_val)
                except ValueError:
                    valid_date = False
            if date_val and not valid_date:
                findings.append(
                    Finding(
                        severity="error",
                        code="invalid-date",
                        file=rel_file,
                        line=fm.field_lines.get("date", 1),
                        message=f"Frontmatter `date` (`{date_val}`) must be a valid `YYYY-MM-DD` date.",
                    )
                )

        rel_parts = md_file.relative_to(project_root).parts
        if len(rel_parts) >= 2 and rel_parts[1] in ("projects", "goals") and "status" in fm.fields:
            status_val = str(fm.fields["status"]).strip().lower()
            if status_val not in VALID_STATUSES:
                findings.append(
                    Finding(
                        severity="error",
                        code="invalid-status",
                        file=rel_file,
                        line=fm.field_lines.get("status", 1),
                        message=(
                            f"Invalid `status` (`{status_val}`); expected one of "
                            f"{sorted(VALID_STATUSES)}."
                        ),
                    )
                )

    non_code = _iter_non_code_lines(lines, body_start)
    rel_parts = md_file.relative_to(project_root).parts
    is_preference_surface = rel_file == "mem/gemini.md" or (
        len(rel_parts) >= 2 and rel_parts[1] == "preferences"
    )

    for line_no, text in non_code:
        for match in WIKILINK_RE.finditer(text):
            findings.append(
                Finding(
                    severity="error",
                    code="legacy-wikilink",
                    file=rel_file,
                    line=line_no,
                    message=f"Found legacy wikilink `{match.group(0)}`; use Standard Relative Markdown Links.",
                )
            )

        for match in MD_LINK_RE.finditer(text):
            target = _clean_href_target(match.group(1))
            if _is_external_or_placeholder(target):
                continue
            if not (md_file.parent / target).exists():
                findings.append(
                    Finding(
                        severity="error",
                        code="broken-memory-link",
                        file=rel_file,
                        line=line_no,
                        message=f"Broken relative link `{match.group(1)}` (resolved target `{target}` not found).",
                    )
                )

        if is_preference_surface:
            hyp_match = HYPOTHESIS_RE.search(text)
            if hyp_match:
                findings.append(
                    Finding(
                        severity="warning",
                        code="unconfirmed-hypothesis-persisted",
                        file=rel_file,
                        line=line_no,
                        message=(
                            f"Found unconfirmed marker `{hyp_match.group(0)}` in `{rel_file}`; "
                            "confirm preference with the user or keep it out of durable memory."
                        ),
                    )
                )

    return findings


def lint_memory(project_root: Path) -> dict[str, Any]:
    """Lint all mem/**/*.md files under project_root."""
    mem_dir = project_root / "mem"
    findings: list[Finding] = []
    files_checked = 0

    if mem_dir.is_dir():
        for md_file in sorted(mem_dir.rglob("*.md")):
            files_checked += 1
            findings.extend(lint_memory_file(md_file, project_root))

    error_count = sum(1 for item in findings if item.severity == "error")
    warning_count = sum(1 for item in findings if item.severity == "warning")
    by_code: dict[str, int] = {}
    for item in findings:
        by_code[item.code] = by_code.get(item.code, 0) + 1

    if error_count > 0:
        status = "error"
    elif warning_count > 0:
        status = "warning"
    else:
        status = "ok"

    return {
        "status": status,
        "files_checked": files_checked,
        "summary": {
            "error": error_count,
            "warning": warning_count,
            "by_code": by_code,
        },
        "findings": [asdict(item) for item in findings],
    }


def _default_project_root() -> Path:
    """Resolve repository root automatically or fall back to cwd."""
    candidate = Path(__file__).resolve().parents[4]
    if (candidate / "mem").is_dir():
        return candidate
    return Path.cwd()


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for memory layer linting."""
    _ensure_utf8_stdio()
    parser = argparse.ArgumentParser(
        description="Validate mem/**/*.md schema, secret safety, links, and preference confirmation."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_default_project_root(),
        help="Path to the tluc-wiki root directory.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 1 if any error OR warning finding exists.",
    )
    args = parser.parse_args(argv)

    root = args.project_root.resolve()
    report = lint_memory(root)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    error_count = report["summary"]["error"]
    warning_count = report["summary"]["warning"]
    if error_count > 0 or (args.strict and warning_count > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
