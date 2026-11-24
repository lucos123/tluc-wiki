#!/usr/bin/env python3
"""Deterministic linter for .agents/skills/*/SKILL.md and ctx/rules/*.md."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import unquote

MAX_DESCRIPTION_LEN = 1024
MAX_SKILL_LINES = 500

DEPRECATED_TOOLS = (
    "view_file",
    "write_to_file",
    "replace_file_content",
    "multi_replace_file_content",
    "grep_search",
)

DEPRECATED_TOOL_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(tool) for tool in DEPRECATED_TOOLS) + r")\b"
)

STALE_RUNTIME_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("`.omc/` runtime path", re.compile(r"(?<![A-Za-z0-9_-])\.omc/")),
    ("`/oh-my-claudecode:` command", re.compile(r"/oh-my-claudecode:")),
    ("`CLAUDE_PLUGIN_ROOT` env var", re.compile(r"\bCLAUDE_PLUGIN_ROOT\b")),
    ("`Task(...)` call", re.compile(r"\bTask\(")),
)

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\n]+)\)")
BACKTICK_SUBPATH_RE = re.compile(
    r"`((?:references|scripts|examples|resources)/[A-Za-z0-9_./<>*{}-]+)`"
)
WIKILINK_RE = re.compile(r"\[\[[^\]\n]+\]\]")
INLINE_CODE_RE = re.compile(r"(``+)([^`\n]+?)\1|`([^`\n]+?)`")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
LIST_ITEM_RE = re.compile(r"^\s+-\s+(.+?)\s*$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

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
    """Represents a single lint finding."""

    severity: str
    code: str
    file: str
    line: int
    message: str


@dataclass
class FrontmatterData:
    """Parsed YAML frontmatter fields needed by the skill linter."""

    fields: dict[str, Any]
    field_lines: dict[str, int]
    allowed_tools: list[tuple[str, int]]
    body_start_line: int


def _ensure_utf8_stdio() -> None:
    """Configure UTF-8 stdout/stderr on Windows consoles when available."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def _strip_quotes(value: str) -> str:
    """Strip matching surrounding single or double quotes from a YAML scalar."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _fold_block_scalar(lines: list[str], folded: bool, strip_trailing: bool) -> str:
    """Join YAML literal (|) or folded (>) block scalar lines."""
    non_empty = [line for line in lines if line.strip()]
    if not non_empty:
        return ""
    min_indent = min(len(line) - len(line.lstrip(" ")) for line in non_empty)
    stripped = [line[min_indent:] if len(line) >= min_indent else "" for line in lines]

    if not folded:
        text = "\n".join(stripped)
    else:
        paragraphs: list[str] = []
        current: list[str] = []
        for line in stripped:
            if not line.strip():
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
                else:
                    paragraphs.append("")
            else:
                current.append(line.strip())
        if current:
            paragraphs.append(" ".join(current))
        text = "\n".join(paragraphs)

    return text.rstrip("\n") if strip_trailing else text


def parse_frontmatter(lines: list[str]) -> FrontmatterData | None:
    """Parse minimal YAML frontmatter from file lines. Return None if missing."""
    if not lines:
        return None
    first = lines[0].lstrip("\ufeff").strip()
    if first != "---":
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
    allowed_tools: list[tuple[str, int]] = []

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

        if val_raw in (">", ">-", "|", "|-"):
            folded = val_raw.startswith(">")
            strip_trailing = val_raw.endswith("-")
            block_lines: list[str] = []
            i += 1
            while i < end_idx:
                nxt = lines[i]
                if nxt.strip() == "":
                    block_lines.append("")
                    i += 1
                    continue
                if nxt[0] in (" ", "\t"):
                    block_lines.append(nxt)
                    i += 1
                    continue
                break
            fields[key] = _fold_block_scalar(block_lines, folded, strip_trailing)
            continue

        if key == "allowed-tools" and val_raw == "":
            tools_collected: list[str] = []
            i += 1
            while i < end_idx:
                nxt = lines[i]
                if not nxt.strip():
                    i += 1
                    continue
                item_match = LIST_ITEM_RE.match(nxt)
                if item_match:
                    tool_name = _strip_quotes(item_match.group(1))
                    tools_collected.append(tool_name)
                    allowed_tools.append((tool_name, i + 1))
                    i += 1
                    continue
                if nxt[0] in (" ", "\t"):
                    i += 1
                    continue
                break
            fields[key] = tools_collected
            continue

        if key == "allowed-tools" and val_raw.startswith("[") and val_raw.endswith("]"):
            items = [
                _strip_quotes(part)
                for part in val_raw[1:-1].split(",")
                if part.strip()
            ]
            fields[key] = items
            for item in items:
                allowed_tools.append((item, i + 1))
            i += 1
            continue

        # Plain scalar (possibly with indented continuation lines)
        scalar_parts = [_strip_quotes(val_raw)] if val_raw else []
        i += 1
        while i < end_idx:
            nxt = lines[i]
            if nxt.strip() and nxt[0] in (" ", "\t") and not LIST_ITEM_RE.match(nxt):
                scalar_parts.append(nxt.strip())
                i += 1
                continue
            break
        fields[key] = " ".join(part for part in scalar_parts if part)

    return FrontmatterData(
        fields=fields,
        field_lines=field_lines,
        allowed_tools=allowed_tools,
        body_start_line=end_idx + 2,
    )


def extract_non_code_lines(
    lines: list[str], start_line: int = 1
) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """Return (non_fence_lines, non_code_lines) preserving 1-based line numbers.

    `non_fence_lines` omits fenced code block contents (used for checking backticked
    local subpaths in prose). `non_code_lines` also replaces inline backtick spans
    with spaces (used for links, wikilinks, and un-backticked tool names).
    """
    non_fence: list[tuple[int, str]] = []
    non_code: list[tuple[int, str]] = []
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

        non_fence.append((line_no, line))
        stripped_inline = INLINE_CODE_RE.sub(" ", line)
        non_code.append((line_no, stripped_inline))

    return non_fence, non_code


def _is_external_or_placeholder(href: str) -> bool:
    """Return True if href is an external URI, anchor, or template placeholder."""
    lower = href.lower()
    if not href or href.startswith("#"):
        return True
    if any(lower.startswith(prefix) for prefix in EXTERNAL_SCHEME_PREFIXES):
        return True
    if any(ch in href for ch in ("<", ">", "{", "}", "*")):
        return True
    return False


def _clean_href_target(raw_href: str) -> str:
    """Extract clean path portion from a Markdown link target."""
    href = raw_href.strip()
    if href.startswith("<") and ">" in href:
        href = href[1 : href.index(">")].strip()
    else:
        # Strip optional Markdown link title: path "title" or path 'title'
        title_match = re.match(r'^(\S+)\s+["\'].*["\']$', href)
        if title_match:
            href = title_match.group(1)
    if "#" in href:
        href = href.split("#", 1)[0]
    return unquote(href)


def _check_broken_links(
    file_path: Path,
    rel_file: str,
    non_fence_lines: list[tuple[int, str]],
    non_code_lines: list[tuple[int, str]],
) -> list[Finding]:
    """Validate local Markdown links and backticked subpath references in SKILL.md."""
    findings: list[Finding] = []
    base_dir = file_path.parent

    for line_no, text in non_code_lines:
        for match in MD_LINK_RE.finditer(text):
            target = _clean_href_target(match.group(1))
            if _is_external_or_placeholder(target):
                continue
            resolved = base_dir / target
            if not resolved.exists():
                findings.append(
                    Finding(
                        severity="error",
                        code="broken-skill-link",
                        file=rel_file,
                        line=line_no,
                        message=f"Broken relative link `{match.group(1)}` (resolved target `{target}` not found).",
                    )
                )

    for line_no, text in non_fence_lines:
        for match in BACKTICK_SUBPATH_RE.finditer(text):
            subpath = match.group(1).strip()
            if _is_external_or_placeholder(subpath):
                continue
            if not re.search(r"\.[A-Za-z0-9]{1,8}$", subpath):
                continue
            if not (base_dir / subpath).exists():
                findings.append(
                    Finding(
                        severity="error",
                        code="broken-skill-link",
                        file=rel_file,
                        line=line_no,
                        message=f"Broken skill subpath reference `{subpath}` (file does not exist).",
                    )
                )

    return findings


def _check_runtime_and_wikilinks(
    rel_file: str,
    lines: list[str],
    non_code_lines: list[tuple[int, str]],
    start_line: int = 1,
) -> list[Finding]:
    """Scan lines for leaked external runtime artifacts and legacy [[wikilinks]]."""
    findings: list[Finding] = []

    for line_no in range(start_line, len(lines) + 1):
        raw_line = lines[line_no - 1]
        for label, pattern in STALE_RUNTIME_PATTERNS:
            if pattern.search(raw_line):
                findings.append(
                    Finding(
                        severity="error",
                        code="stale-external-runtime",
                        file=rel_file,
                        line=line_no,
                        message=f"Found leaked external runtime reference ({label}); adapt cleanly for Antigravity.",
                    )
                )

    for line_no, text in non_code_lines:
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

    return findings


def lint_skill_file(skill_md: Path, project_root: Path) -> list[Finding]:
    """Lint a single .agents/skills/<name>/SKILL.md file."""
    rel_file = skill_md.relative_to(project_root).as_posix()
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    findings: list[Finding] = []

    fm = parse_frontmatter(lines)
    if fm is None:
        findings.append(
            Finding(
                severity="error",
                code="missing-frontmatter",
                file=rel_file,
                line=1,
                message="SKILL.md must begin with valid YAML frontmatter delimited by `---`.",
            )
        )
        non_fence, non_code = extract_non_code_lines(lines, 1)
        findings.extend(_check_broken_links(skill_md, rel_file, non_fence, non_code))
        findings.extend(_check_runtime_and_wikilinks(rel_file, lines, non_code, 1))
        return findings

    expected_name = skill_md.parent.name
    actual_name = str(fm.fields.get("name", "")).strip()
    name_line = fm.field_lines.get("name", 1)
    if not actual_name or actual_name != expected_name or not SKILL_NAME_RE.match(actual_name):
        findings.append(
            Finding(
                severity="error",
                code="invalid-skill-name",
                file=rel_file,
                line=name_line,
                message=(
                    f"Frontmatter `name` (`{actual_name or '<missing>'}`) must match directory name "
                    f"`{expected_name}` using lowercase letters, digits, and hyphens."
                ),
            )
        )

    description = str(fm.fields.get("description", "")).strip()
    desc_line = fm.field_lines.get("description", 1)
    if not description or len(description) > MAX_DESCRIPTION_LEN:
        findings.append(
            Finding(
                severity="error",
                code="invalid-skill-description",
                file=rel_file,
                line=desc_line,
                message=(
                    f"Frontmatter `description` must be non-empty and <= {MAX_DESCRIPTION_LEN} characters "
                    f"(found {len(description)})."
                ),
            )
        )

    if len(lines) > MAX_SKILL_LINES:
        findings.append(
            Finding(
                severity="warning",
                code="oversized-skill-md",
                file=rel_file,
                line=MAX_SKILL_LINES + 1,
                message=(
                    f"SKILL.md has {len(lines)} lines (limit {MAX_SKILL_LINES}); move extended reference "
                    "material into `references/`."
                ),
            )
        )

    for tool_name, line_no in fm.allowed_tools:
        if tool_name in DEPRECATED_TOOLS:
            findings.append(
                Finding(
                    severity="error",
                    code="stale-tool-name",
                    file=rel_file,
                    line=line_no,
                    message=(
                        f"Deprecated tool `{tool_name}` in `allowed-tools`; replace with Antigravity "
                        "tools (`read_file`, `write_file`, `edit_file`, `run_command`)."
                    ),
                )
            )

    non_fence, non_code = extract_non_code_lines(lines, fm.body_start_line)
    for line_no, text_line in non_code:
        for match in DEPRECATED_TOOL_RE.finditer(text_line):
            findings.append(
                Finding(
                    severity="error",
                    code="stale-tool-name",
                    file=rel_file,
                    line=line_no,
                    message=(
                        f"Deprecated tool name `{match.group(0)}` in SKILL.md prose; replace with "
                        "Antigravity tool names (`read_file`, `write_file`, `edit_file`, `run_command`)."
                    ),
                )
            )

    findings.extend(_check_broken_links(skill_md, rel_file, non_fence, non_code))
    findings.extend(_check_runtime_and_wikilinks(rel_file, lines, non_code, 1))
    return findings


def lint_rule_file(rule_md: Path, project_root: Path) -> list[Finding]:
    """Lint a single ctx/rules/*.md file for legacy wikilinks and external runtime leaks."""
    rel_file = rule_md.relative_to(project_root).as_posix()
    lines = rule_md.read_text(encoding="utf-8").splitlines()
    _, non_code = extract_non_code_lines(lines, 1)
    return _check_runtime_and_wikilinks(rel_file, lines, non_code, 1)


def lint_workspace(project_root: Path) -> dict[str, Any]:
    """Lint all .agents/skills/*/SKILL.md and ctx/rules/*.md files under project_root."""
    skills_dir = project_root / ".agents" / "skills"
    rules_dir = project_root / "ctx" / "rules"

    findings: list[Finding] = []
    skills_checked = 0
    rules_checked = 0

    if skills_dir.is_dir():
        for entry in sorted(skills_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith((".", "_")):
                continue
            skill_md = entry / "SKILL.md"
            if skill_md.is_file():
                skills_checked += 1
                findings.extend(lint_skill_file(skill_md, project_root))
            else:
                rel_dir = entry.relative_to(project_root).as_posix()
                findings.append(
                    Finding(
                        severity="error",
                        code="missing-frontmatter",
                        file=f"{rel_dir}/SKILL.md",
                        line=1,
                        message=f"Skill directory `{rel_dir}` is missing `SKILL.md`.",
                    )
                )

    if rules_dir.is_dir():
        for rule_md in sorted(rules_dir.glob("*.md")):
            rules_checked += 1
            findings.extend(lint_rule_file(rule_md, project_root))

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
        "skills_checked": skills_checked,
        "rules_checked": rules_checked,
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
    if (candidate / ".agents" / "skills").is_dir():
        return candidate
    return Path.cwd()


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for skill and rule linting."""
    _ensure_utf8_stdio()
    parser = argparse.ArgumentParser(
        description="Lint .agents/skills/*/SKILL.md and ctx/rules/*.md for structural discipline."
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
    report = lint_workspace(root)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    error_count = report["summary"]["error"]
    warning_count = report["summary"]["warning"]
    if error_count > 0 or (args.strict and warning_count > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
