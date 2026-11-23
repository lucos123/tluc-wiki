#!/usr/bin/env python3
"""
Deterministic Workspace & Session Status Collector for ketchup skill.

Aggregates:
  - Recent entries from wiki/log.md with exact 1-based line numbers
  - Current git branch and changed/untracked files bucketed by tluc-wiki area
  - Optional Antigravity transcript summary (reusing reflect/scripts/summarize_transcript.py)
"""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def find_project_root(start_dir=None) -> str | None:
    """Walk upward from script or CWD to locate repository root containing index.md."""
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


def read_recent_log_entries(project_root: str, limit: int = 8) -> list[dict]:
    """Return the most recent N '## [...]' entries from wiki/log.md with 1-based line numbers."""
    log_path = Path(project_root) / "wiki" / "log.md"
    if not log_path.is_file():
        return []
    entries = []
    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        for line_no, raw_line in enumerate(f, start=1):
            stripped = raw_line.strip()
            if stripped.startswith("## "):
                entries.append({"line": line_no, "text": stripped})
    return entries[-limit:] if limit > 0 else entries


def parse_git_status_output(stdout_text: str) -> dict:
    """Parse 'git status --short --branch' output and bucket files by tluc-wiki top folder."""
    branch = ""
    buckets = {"wiki": [], "mem": [], "output": [], ".agents": [], "other": []}
    total_changed = 0

    for line in stdout_text.splitlines():
        if not line.strip():
            continue
        if line.startswith("## "):
            branch = line[3:].strip()
            continue
        code = line[:2]
        raw_path = line[3:].strip()
        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1].strip()
        if raw_path.startswith('"') and raw_path.endswith('"') and len(raw_path) >= 2:
            raw_path = raw_path[1:-1]
        norm = raw_path.replace("\\", "/")
        total_changed += 1
        top = norm.split("/", 1)[0]
        target_bucket = top if top in ("wiki", "mem", "output", ".agents") else "other"
        buckets[target_bucket].append({"status": code, "path": norm})

    return {
        "git_available": True,
        "branch": branch,
        "total_changed": total_changed,
        "by_bucket": buckets,
    }


def collect_git_status(project_root: str) -> dict:
    """Safely invoke 'git status --short --branch', degrading cleanly outside git repos."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(project_root), "status", "--short", "--branch"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return {"git_available": False, "error": str(exc), "branch": "", "total_changed": 0, "by_bucket": {}}

    if proc.returncode != 0:
        return {
            "git_available": False,
            "error": (proc.stderr or "").strip() or f"git exited with code {proc.returncode}",
            "branch": "",
            "total_changed": 0,
            "by_bucket": {},
        }
    return parse_git_status_output(proc.stdout)


def load_transcript_summary(transcript_path: str, last_turns: int = 5) -> dict:
    """Reuse reflect/scripts/summarize_transcript.py to summarize recent session turns."""
    tpath = Path(transcript_path).expanduser()
    if not tpath.is_file():
        return {"available": False, "error": f"Transcript not found: {tpath}"}

    summarizer_path = Path(__file__).resolve().parents[2] / "reflect" / "scripts" / "summarize_transcript.py"
    if not summarizer_path.is_file():
        return {"available": False, "error": f"Missing summarize_transcript.py at {summarizer_path}"}

    spec = importlib.util.spec_from_file_location("summarize_transcript", str(summarizer_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rep = mod.analyze_transcript(tpath, last_turns=last_turns, max_events=10)
    return {
        "available": True,
        "window": rep["window"],
        "user_turns": rep["user_turns"],
        "total_friction_events": rep["overview"]["total_friction_events"],
        "recent_friction": rep["friction_events"][-5:],
    }


def render_markdown(report: dict) -> str:
    """Render compact Markdown status digest for ketchup catch-up reporting."""
    lines = [
        "# Workspace Catch-Up Snapshot",
        "",
        f"- **Project Root**: `{report['project_root']}`",
    ]
    gs = report["git"]
    if gs.get("git_available"):
        lines.append(f"- **Git Branch**: `{gs['branch']}` (`{gs['total_changed']}` changed/untracked paths)")
        for bname, items in gs["by_bucket"].items():
            if items:
                preview = ", ".join(f"`{it['path']}` ({it['status'].strip() or '?'})" for it in items[:8])
                extra = f" ... (+{len(items) - 8})" if len(items) > 8 else ""
                lines.append(f"  - **{bname} ({len(items)})**: {preview}{extra}")
    else:
        lines.append(f"- **Git**: unavailable ({gs.get('error', 'not a git repo')})")

    lines.extend(["", f"## Recent `wiki/log.md` Entries ({len(report['recent_log_entries'])})"])
    if report["recent_log_entries"]:
        for entry in report["recent_log_entries"]:
            lines.append(f"- `wiki/log.md#L{entry['line']}`: {entry['text']}")
    else:
        lines.append("- None")

    ts = report.get("transcript")
    if ts:
        lines.extend(["", "## Recent Session Transcript Window"])
        if ts.get("available"):
            w = ts["window"]
            lines.append(
                f"- Lines `L{w['start_line']}..L{w['end_line']}` ({w['turns_in_window']}/{w['total_user_turns_in_file']} turns), friction events: `{ts['total_friction_events']}`"
            )
            for ut in ts["user_turns"]:
                lines.append(f"  - Turn `L{ut['line']}`: {ut['preview']}")
        else:
            lines.append(f"- Unavailable: {ts.get('error')}")

    return "\n".join(lines) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Gather workspace git, wiki/log.md, and optional transcript status for ketchup.")
    parser.add_argument("--project-root", default=None, help="Project root containing index.md")
    parser.add_argument("--log-lines", type=int, default=8, help="Number of recent wiki/log.md entries to include (default: 8)")
    parser.add_argument("--transcript", default=None, help="Optional path to Antigravity transcript.jsonl")
    parser.add_argument("--last-turns", type=int, default=5, help="Number of recent user turns when --transcript is passed")
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    args = parser.parse_args()

    project_root = args.project_root or find_project_root()
    if not project_root:
        print(json.dumps({"status": "error", "error": "Could not locate project root (index.md)."}, indent=2))
        sys.exit(2)

    report = {
        "status": "ok",
        "project_root": project_root.replace("\\", "/"),
        "git": collect_git_status(project_root),
        "recent_log_entries": read_recent_log_entries(project_root, limit=args.log_lines),
    }
    if args.transcript:
        report["transcript"] = load_transcript_summary(args.transcript, last_turns=args.last_turns)

    if args.format == "markdown":
        print(render_markdown(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
