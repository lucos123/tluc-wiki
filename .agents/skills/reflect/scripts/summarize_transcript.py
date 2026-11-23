#!/usr/bin/env python3
"""
Antigravity Session Transcript Indexer & Friction Extractor for reflect skill.

Reads Antigravity's transcript.jsonl cleanly and emits either structured JSON or a
compact Markdown digest showing user turns, tool stats, skills read, subagents invoked,
token/cache metrics, and exact 1-based line numbers for errors/non-zero exits.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

NONZERO_EXIT_RE = re.compile(r"Command exited with code ([1-9]\d*)")
USER_REQ_RE = re.compile(r"<USER_REQUEST>\s*([\s\S]*?)\s*</USER_REQUEST>", re.IGNORECASE)


def decode_arg_value(raw_val) -> str:
    """Decode Antigravity's JSON-quoted string arguments cleanly into plain strings."""
    if not isinstance(raw_val, str):
        return str(raw_val)
    text = raw_val.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        try:
            decoded = json.loads(text)
            if isinstance(decoded, str):
                return decoded
        except json.JSONDecodeError:
            return text[1:-1]
    return text


def clean_user_prompt(content: str, max_len: int = 160) -> str:
    """Extract concise readable request summary from USER_INPUT content."""
    text = (content or "").strip()
    m = USER_REQ_RE.search(text)
    if m:
        text = m.group(1).strip()
    one_line = re.sub(r"\s+", " ", text)
    if len(one_line) > max_len:
        return one_line[: max_len - 3].rstrip() + "..."
    return one_line


def resolve_transcript_path(transcript_arg: str | None, conversation_id: str | None, app_data_dir: str | None) -> Path:
    """Resolve explicit transcript path or construct it from conversation ID."""
    if transcript_arg:
        return Path(transcript_arg).expanduser()
    if conversation_id:
        base = Path(app_data_dir).expanduser() if app_data_dir else (Path.home() / ".gemini" / "antigravity")
        return base / "brain" / conversation_id / ".system_generated" / "logs" / "transcript.jsonl"
    raise ValueError("Provide either a transcript path or --conversation-id.")


def parse_transcript_records(transcript_path: Path) -> tuple[list[tuple[int, dict]], int]:
    """Parse JSONL preserving exact 1-based file line numbers; count malformed lines safely."""
    records = []
    parse_warnings = 0
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line_no, raw_line in enumerate(f, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError:
                parse_warnings += 1
                continue
            if isinstance(obj, dict):
                records.append((line_no, obj))
            else:
                parse_warnings += 1
    return records, parse_warnings


def analyze_transcript(
    transcript_path: Path,
    last_turns: int = 0,
    max_events: int = 40,
) -> dict:
    """Summarize transcript window, tool/skill/subagent usage, and friction line anchors."""
    records, parse_warnings = parse_transcript_records(transcript_path)
    total_file_records = len(records)

    user_positions = [idx for idx, (_ln, obj) in enumerate(records) if obj.get("type") == "USER_INPUT"]
    total_user_turns = len(user_positions)

    if last_turns and last_turns > 0 and len(user_positions) > last_turns:
        start_idx = user_positions[-last_turns]
        window_records = records[start_idx:]
    else:
        window_records = records

    start_line = window_records[0][0] if window_records else 1
    end_line = window_records[-1][0] if window_records else 0

    type_counts = Counter()
    model_counts = Counter()
    tool_counts = Counter()
    skills_read = []
    seen_skills = set()
    subagents = []
    user_turns = []
    friction_events = []

    input_tokens = 0
    cache_read_tokens = 0
    output_tokens = 0
    truncated_lines = 0

    for line_no, obj in window_records:
        rec_type = str(obj.get("type") or "UNKNOWN")
        type_counts[rec_type] += 1

        if obj.get("truncated_fields"):
            truncated_lines += 1

        if rec_type == "USER_INPUT":
            user_turns.append({
                "line": line_no,
                "step_index": obj.get("step_index"),
                "created_at": obj.get("created_at", ""),
                "preview": clean_user_prompt(str(obj.get("content", ""))),
                "truncated": bool(obj.get("truncated_fields")),
            })
        elif rec_type == "PLANNER_RESPONSE":
            input_tokens += int(obj.get("input_tokens") or 0)
            cache_read_tokens += int(obj.get("cache_read_tokens") or 0)
            output_tokens += int(obj.get("output_tokens") or 0)
            model = obj.get("model")
            if model:
                model_counts[str(model)] += 1
            for tc in obj.get("tool_calls") or []:
                if not isinstance(tc, dict):
                    continue
                tname = str(tc.get("name") or "unknown")
                tool_counts[tname] += 1
                args = tc.get("args") or {}
                if tname == "read_file" and isinstance(args, dict):
                    fpath = decode_arg_value(args.get("Path", ""))
                    if fpath.replace("\\", "/").endswith("/SKILL.md") or fpath.endswith("SKILL.md"):
                        norm = fpath.replace("\\", "/")
                        if norm not in seen_skills:
                            seen_skills.add(norm)
                            skills_read.append({"line": line_no, "path": norm})
                elif tname == "invoke_subagent" and isinstance(args, dict):
                    subagents.append({
                        "line": line_no,
                        "step_index": obj.get("step_index"),
                        "type_name": decode_arg_value(args.get("TypeName", "")),
                        "role": decode_arg_value(args.get("Role", "")),
                    })
        elif rec_type == "ERROR_MESSAGE":
            err_msg = re.sub(r"\s+", " ", str(obj.get("error") or obj.get("content") or "")).strip()
            friction_events.append({
                "line": line_no,
                "step_index": obj.get("step_index"),
                "kind": "api_error",
                "truncated": bool(obj.get("truncated_fields")),
                "snippet": err_msg[:180],
            })
        elif rec_type == "GENERIC":
            content = str(obj.get("content") or "")
            status = str(obj.get("status") or "")
            m_exit = NONZERO_EXIT_RE.search(content)
            is_tool_err = status == "ERROR" or "Encountered error" in content
            if m_exit or is_tool_err:
                one_line = re.sub(r"\s+", " ", content).strip()
                item = {
                    "line": line_no,
                    "step_index": obj.get("step_index"),
                    "kind": "nonzero_exit" if m_exit else "tool_error",
                    "truncated": bool(obj.get("truncated_fields")),
                    "snippet": one_line[:180],
                }
                if m_exit:
                    item["exit_code"] = int(m_exit.group(1))
                friction_events.append(item)

    total_friction = len(friction_events)
    if max_events > 0 and len(friction_events) > max_events:
        friction_events = friction_events[-max_events:]

    cache_hit_pct = round(cache_read_tokens / input_tokens * 100, 1) if input_tokens > 0 else 0.0
    full_path = transcript_path.with_name("transcript_full.jsonl")

    return {
        "status": "ok",
        "transcript_path": str(transcript_path),
        "full_transcript_path": str(full_path) if full_path.is_file() else None,
        "window": {
            "last_turns_requested": last_turns,
            "turns_in_window": len(user_turns),
            "total_user_turns_in_file": total_user_turns,
            "start_line": start_line,
            "end_line": end_line,
            "records_in_window": len(window_records),
            "total_records_in_file": total_file_records,
            "parse_warnings": parse_warnings,
        },
        "overview": {
            "record_types": dict(type_counts),
            "models": dict(model_counts.most_common()),
            "input_tokens": input_tokens,
            "cache_read_tokens": cache_read_tokens,
            "cache_hit_pct": cache_hit_pct,
            "output_tokens": output_tokens,
            "checkpoints": type_counts.get("CHECKPOINT", 0),
            "truncated_lines": truncated_lines,
            "total_tool_calls": sum(tool_counts.values()),
            "total_friction_events": total_friction,
        },
        "user_turns": user_turns,
        "tool_counts": dict(tool_counts.most_common()),
        "skills_read": skills_read,
        "subagents": subagents,
        "friction_events": friction_events,
    }


def render_markdown(report: dict) -> str:
    """Format compact, citation-ready Markdown digest for the 3-lens reflect panel."""
    w = report["window"]
    ov = report["overview"]
    lines = [
        "# Transcript Audit Digest",
        "",
        f"- **Transcript**: `{report['transcript_path']}`",
    ]
    if report["full_transcript_path"]:
        lines.append(f"- **Full Lines Fallback**: `{report['full_transcript_path']}` ({ov['truncated_lines']} truncated records in window)")
    lines.extend([
        f"- **Window**: Lines `L{w['start_line']}..L{w['end_line']}` ({w['turns_in_window']}/{w['total_user_turns_in_file']} user turns, {w['records_in_window']} records)",
        f"- **Tokens & Cache**: input `{ov['input_tokens']:,}` | cache read `{ov['cache_read_tokens']:,}` ({ov['cache_hit_pct']}%) | output `{ov['output_tokens']:,}` | checkpoints `{ov['checkpoints']}`",
        "",
        "## User Turns",
    ])
    for t in report["user_turns"]:
        lines.append(f"- `L{t['line']}` (step `{t['step_index']}`): {t['preview']}")

    lines.extend(["", "## Tool Usage"])
    if report["tool_counts"]:
        for name, cnt in report["tool_counts"].items():
            lines.append(f"- `{name}`: {cnt}")
    else:
        lines.append("- None")

    lines.extend(["", "## Skills Read & Subagents"])
    if report["skills_read"]:
        for s in report["skills_read"]:
            lines.append(f"- Skill `L{s['line']}`: `{s['path']}`")
    else:
        lines.append("- Skills read: None in window")
    if report["subagents"]:
        for sa in report["subagents"]:
            lines.append(f"- Subagent `L{sa['line']}`: `{sa['type_name']}` ({sa['role']})")
    else:
        lines.append("- Subagents invoked: None in window")

    lines.extend(["", f"## Friction & Error Hotspots ({len(report['friction_events'])}/{ov['total_friction_events']})"])
    if report["friction_events"]:
        for ev in report["friction_events"]:
            extra = f" exit={ev['exit_code']}" if "exit_code" in ev else ""
            trunc = " [truncated]" if ev.get("truncated") else ""
            lines.append(f"- `L{ev['line']}` (step `{ev['step_index']}`, `{ev['kind']}`{extra}{trunc}): {ev['snippet']}")
    else:
        lines.append("- None observed in window")

    return "\n".join(lines) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Summarize Antigravity transcript.jsonl for reflect audits.")
    parser.add_argument("transcript", nargs="?", help="Path to transcript.jsonl")
    parser.add_argument("--conversation-id", help="Conversation ID to resolve under --app-data-dir")
    parser.add_argument("--app-data-dir", default=None, help="Antigravity app data dir (default: ~/.gemini/antigravity)")
    parser.add_argument("--last-turns", type=int, default=0, help="Slice window to the most recent N user turns (0 = all)")
    parser.add_argument("--max-events", type=int, default=40, help="Maximum friction events to include (default: 40)")
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    args = parser.parse_args()

    try:
        tpath = resolve_transcript_path(args.transcript, args.conversation_id, args.app_data_dir)
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(2)

    if not tpath.is_file():
        print(json.dumps({"status": "error", "error": f"Transcript not found: {tpath}"}, ensure_ascii=False, indent=2))
        sys.exit(2)

    report = analyze_transcript(tpath, last_turns=args.last_turns, max_events=args.max_events)
    if args.format == "markdown":
        print(render_markdown(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
