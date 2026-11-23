"""
Unit Test Suite for ketchup + bro skills & scripts/gather_status.py.
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
import gather_status


class TestGatherStatus(unittest.TestCase):

    def test_read_recent_log_entries_preserves_line_numbers_and_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "wiki").mkdir(parents=True)
            (root / "wiki" / "log.md").write_text(
                "\n".join([
                    "# Wiki Log",
                    "",
                    "## [2026-11-20] ingest | First Entry",
                    "Some detail line",
                    "## [2026-11-21] write | Báo cáo Tiếng Việt",
                    "## [2026-11-22] maintain | Final Entry",
                ]) + "\n",
                encoding="utf-8",
            )
            entries = gather_status.read_recent_log_entries(str(root), limit=2)
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0]["line"], 5)
            self.assertIn("Báo cáo Tiếng Việt", entries[0]["text"])
            self.assertEqual(entries[1]["line"], 6)

    def test_parse_git_status_output_buckets_tluc_wiki_areas(self):
        sample = "\n".join([
            "## main...origin/main",
            " M GEMINI.md",
            "?? .agents/skills/bro/SKILL.md",
            " M wiki/concepts/Harness Engineering.md",
            "?? output/reports/summary.md",
            " M mem/goals/AI Engineering Mastery 2026.md",
        ])
        parsed = gather_status.parse_git_status_output(sample)
        self.assertTrue(parsed["git_available"])
        self.assertEqual(parsed["branch"], "main...origin/main")
        self.assertEqual(parsed["total_changed"], 5)
        self.assertEqual(len(parsed["by_bucket"][".agents"]), 1)
        self.assertEqual(len(parsed["by_bucket"]["wiki"]), 1)
        self.assertEqual(len(parsed["by_bucket"]["output"]), 1)
        self.assertEqual(len(parsed["by_bucket"]["mem"]), 1)
        self.assertEqual(len(parsed["by_bucket"]["other"]), 1)

    def test_collect_git_status_handles_non_git_dir_gracefully(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = gather_status.collect_git_status(tmp)
            self.assertFalse(res["git_available"])
            self.assertEqual(res["total_changed"], 0)

    def test_optional_transcript_integration_reuses_reflect_summarizer(self):
        with tempfile.TemporaryDirectory() as tmp:
            tpath = Path(tmp) / "transcript.jsonl"
            tpath.write_text(
                "\n".join([
                    json.dumps({"type": "USER_INPUT", "step_index": 0, "content": "<USER_REQUEST>\nTóm tắt tình hình\n</USER_REQUEST>"}),
                    json.dumps({"type": "GENERIC", "step_index": 1, "status": "ERROR", "content": "Encountered error in step execution: Missing file"}),
                ]) + "\n",
                encoding="utf-8",
            )
            summary = gather_status.load_transcript_summary(str(tpath), last_turns=5)
            self.assertTrue(summary["available"])
            self.assertEqual(summary["window"]["turns_in_window"], 1)
            self.assertEqual(summary["total_friction_events"], 1)
            self.assertIn("Tóm tắt tình hình", summary["user_turns"][0]["preview"])

    def test_cli_json_and_markdown_modes(self):
        script_path = Path(__file__).resolve().parent / "gather_status.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text("# Index\n", encoding="utf-8")
            (root / "wiki").mkdir(parents=True)
            (root / "wiki" / "log.md").write_text("## [2026-11-24] test | Kiểm thử\n", encoding="utf-8")

            proc_json = subprocess.run(
                [sys.executable, str(script_path), "--project-root", str(root), "--format", "json"],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            out = json.loads(proc_json.stdout)
            self.assertEqual(out["status"], "ok")
            self.assertEqual(len(out["recent_log_entries"]), 1)

            proc_md = subprocess.run(
                [sys.executable, str(script_path), "--project-root", str(root), "--format", "markdown"],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            self.assertIn("# Workspace Catch-Up Snapshot", proc_md.stdout)
            self.assertIn("Kiểm thử", proc_md.stdout)

    def test_bro_and_ketchup_skill_frontmatter_and_no_omc_artifacts(self):
        skills_root = Path(__file__).resolve().parents[2]
        for skill_name in ("bro", "ketchup"):
            skill_md = skills_root / skill_name / "SKILL.md"
            self.assertTrue(skill_md.is_file())
            text = skill_md.read_text(encoding="utf-8")
            self.assertLess(len(text.splitlines()), 80)
            self.assertTrue(text.startswith("---\n"))
            fm = text.split("---", 2)[1]
            self.assertIn(f"name: {skill_name}", fm)
            self.assertFalse(
                re.search(r"\.omc/|/oh-my-claudecode:|ledger row|\bTask\(", text),
                f"Found stale OMC reference in {skill_name}/SKILL.md",
            )


if __name__ == "__main__":
    unittest.main()
