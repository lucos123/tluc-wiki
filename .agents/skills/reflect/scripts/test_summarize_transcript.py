"""
Unit Test Suite for reflect skill & scripts/summarize_transcript.py.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import summarize_transcript


def _write_jsonl(path: Path, records: list[str | dict]):
    lines = []
    for rec in records:
        if isinstance(rec, dict):
            lines.append(json.dumps(rec, ensure_ascii=False))
        else:
            lines.append(rec)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


class TestSummarizeTranscript(unittest.TestCase):

    def _sample_records(self):
        return [
            {
                "type": "USER_INPUT",
                "step_index": 0,
                "created_at": "2026-11-24T00:00:00Z",
                "content": "<USER_REQUEST>\nIngest bài viết đầu tiên\n</USER_REQUEST>",
            },
            {
                "type": "PLANNER_RESPONSE",
                "step_index": 1,
                "model": "gemini-pro",
                "input_tokens": 1000,
                "cache_read_tokens": 500,
                "output_tokens": 200,
                "tool_calls": [
                    {
                        "name": "read_file",
                        "args": {"Path": r'"c:\\repo\\.agents\\skills\\wiki-ingest\\SKILL.md"'},
                    },
                    {
                        "name": "run_command",
                        "args": {"CommandLine": '"python bad.py"'},
                    },
                ],
            },
            {
                "type": "GENERIC",
                "step_index": 2,
                "status": "DONE",
                "content": "Command exited with code 1.\nTraceback...",
            },
            {
                "type": "USER_INPUT",
                "step_index": 3,
                "created_at": "2026-11-24T00:05:00Z",
                "content": "<USER_REQUEST>\nTiếp tục kiểm tra link\n</USER_REQUEST>",
            },
            {
                "type": "PLANNER_RESPONSE",
                "step_index": 4,
                "model": "gemini-flash",
                "input_tokens": 2000,
                "cache_read_tokens": 1500,
                "output_tokens": 300,
                "truncated_fields": ["thinking"],
                "tool_calls": [
                    {
                        "name": "invoke_subagent",
                        "args": {"TypeName": '"research"', "Role": '"Code Auditor"'},
                    },
                    {
                        "name": "edit_file",
                        "args": {"Path": '"notes.md"'},
                    },
                ],
            },
            {
                "type": "GENERIC",
                "step_index": 5,
                "status": "ERROR",
                "content": "Encountered error in step execution: Target not found",
            },
            {
                "type": "ERROR_MESSAGE",
                "step_index": 6,
                "error": "API error: stream timeout",
            },
            {
                "type": "CHECKPOINT",
                "step_index": 7,
                "content": "Summary checkpoint",
            },
            {
                "type": "USER_INPUT",
                "step_index": 8,
                "created_at": "2026-11-24T00:10:00Z",
                "content": "Chạy verification lần cuối",
            },
        ]

    def test_full_parse_extracts_turns_tools_skills_subagents_and_friction(self):
        with tempfile.TemporaryDirectory() as tmp:
            tpath = Path(tmp) / "transcript.jsonl"
            full_path = Path(tmp) / "transcript_full.jsonl"
            _write_jsonl(tpath, self._sample_records())
            full_path.write_text("", encoding="utf-8")

            rep = summarize_transcript.analyze_transcript(tpath)
            self.assertEqual(rep["status"], "ok")
            self.assertEqual(rep["full_transcript_path"], str(full_path))
            self.assertEqual(rep["window"]["total_user_turns_in_file"], 3)
            self.assertEqual(rep["overview"]["input_tokens"], 3000)
            self.assertEqual(rep["overview"]["cache_read_tokens"], 2000)
            self.assertEqual(rep["overview"]["output_tokens"], 500)
            self.assertEqual(rep["overview"]["checkpoints"], 1)
            self.assertEqual(rep["overview"]["truncated_lines"], 1)
            self.assertEqual(rep["tool_counts"], {"read_file": 1, "run_command": 1, "invoke_subagent": 1, "edit_file": 1})
            self.assertEqual(rep["skills_read"][0]["path"], "c:/repo/.agents/skills/wiki-ingest/SKILL.md")
            self.assertEqual(rep["subagents"][0]["type_name"], "research")
            self.assertEqual(rep["subagents"][0]["role"], "Code Auditor")
            self.assertEqual([e["kind"] for e in rep["friction_events"]], ["nonzero_exit", "tool_error", "api_error"])
            self.assertEqual([e["line"] for e in rep["friction_events"]], [3, 6, 7])

    def test_last_turns_slice_preserves_true_line_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            tpath = Path(tmp) / "transcript.jsonl"
            _write_jsonl(tpath, self._sample_records())

            rep = summarize_transcript.analyze_transcript(tpath, last_turns=2)
            self.assertEqual(rep["window"]["turns_in_window"], 2)
            self.assertEqual(rep["window"]["start_line"], 4)
            self.assertEqual(rep["window"]["end_line"], 9)
            self.assertEqual([t["line"] for t in rep["user_turns"]], [4, 9])
            self.assertEqual([e["line"] for e in rep["friction_events"]], [6, 7])

    def test_malformed_jsonl_lines_counted_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tpath = Path(tmp) / "transcript.jsonl"
            _write_jsonl(
                tpath,
                [
                    "",
                    "{not-valid-json",
                    "42",
                    self._sample_records()[0],
                ],
            )
            rep = summarize_transcript.analyze_transcript(tpath)
            self.assertEqual(rep["window"]["parse_warnings"], 2)
            self.assertEqual(rep["window"]["turns_in_window"], 1)
            self.assertEqual(rep["user_turns"][0]["line"], 4)

    def test_cli_json_markdown_and_missing_file_exit_code(self):
        script_path = Path(__file__).resolve().parent / "summarize_transcript.py"
        with tempfile.TemporaryDirectory() as tmp:
            tpath = Path(tmp) / "transcript.jsonl"
            _write_jsonl(tpath, self._sample_records())

            proc_md = subprocess.run(
                [sys.executable, str(script_path), str(tpath), "--last-turns", "2", "--format", "markdown"],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            self.assertIn("# Transcript Audit Digest", proc_md.stdout)
            self.assertIn("L4", proc_md.stdout)
            self.assertIn("Kiểm tra link".lower(), proc_md.stdout.lower())

            proc_missing = subprocess.run(
                [sys.executable, str(script_path), str(Path(tmp) / "missing.jsonl")],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertEqual(proc_missing.returncode, 2)
            self.assertEqual(json.loads(proc_missing.stdout)["status"], "error")

    def test_conversation_id_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            conv_id = "abc-123"
            logs_dir = Path(tmp) / "brain" / conv_id / ".system_generated" / "logs"
            logs_dir.mkdir(parents=True)
            tpath = logs_dir / "transcript.jsonl"
            _write_jsonl(tpath, [self._sample_records()[0]])

            resolved = summarize_transcript.resolve_transcript_path(None, conv_id, tmp)
            self.assertEqual(resolved, tpath)

    def test_skill_frontmatter_and_no_omc_artifacts(self):
        skill_dir = Path(__file__).resolve().parent.parent
        skill_md = skill_dir / "SKILL.md"
        lenses_md = skill_dir / "references" / "reviewer-lenses.md"
        text = skill_md.read_text(encoding="utf-8")

        self.assertLess(len(text.splitlines()), 120)
        self.assertTrue(text.startswith("---\n"))
        fm = text.split("---", 2)[1]
        self.assertIn("name: reflect", fm)
        self.assertTrue(lenses_md.is_file())
        self.assertTrue((skill_dir / "scripts" / "summarize_transcript.py").is_file())

        for p in (skill_md, lenses_md):
            content = p.read_text(encoding="utf-8")
            self.assertFalse(
                re.search(r"\.omc/|/oh-my-claudecode:|\.claude/skills|\bskillify\b|\bketchup\b|\bTask\(", content),
                f"Found stale OMC/Claude reference in {p.name}",
            )


if __name__ == "__main__":
    unittest.main()
