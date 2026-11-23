"""
Unit Test Suite for sharpen skill & scripts/check_brief.py.
"""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_brief


class TestCheckBrief(unittest.TestCase):

    def test_clean_english_and_vietnamese_briefs_pass_zero_findings(self):
        en_brief = """# Task Brief
- **Consumer**: Wiki maintainers running weekly health audits.
- **Goal**: Produce a cross-source trade-off report linking [Memory Architecture](wiki/concepts/Memory%20Architecture.md).
- **Done-Check**: `check_research.py --strict` and `lint_wiki.py` pass with 0 broken links.
- **Non-Goals**: No edits inside `raw/` or database deployment.
"""
        vi_brief = """# Phạm vi nhiệm vụ
- **Đối tượng hưởng lợi**: Đội ngũ TVV Nha khoa 3C tư vấn khách Implant qua tin nhắn.
- **Mục tiêu**: Chuẩn hóa 3 kịch bản phản hồi kèm ngưỡng chuyển ca bác sĩ.
- **Tiêu chí hoàn thành**: Quản lý TVV chạy thử 3 ca giả lập khớp checklist trong `< 5` phút.
- **Ngoài phạm vi**: Không thay đổi bảng giá niêm yết.
"""
        res_en = check_brief.analyze_brief(en_brief, "en.md", mode="brief")
        res_vi = check_brief.analyze_brief(vi_brief, "vi.md", mode="brief")
        self.assertEqual(res_en["findings"], [])
        self.assertEqual(res_vi["findings"], [])

    def test_missing_required_elements_detected_in_brief_mode(self):
        incomplete = """- **Goal**: Write an analysis doc.
- **Done-Check**: `lint_wiki.py` returns 0 errors.
"""
        res = check_brief.analyze_brief(incomplete, "incomplete.md", mode="brief")
        missing_msgs = [f["message"] for f in res["findings"] if f["rule"] == "missing-required-element"]
        self.assertEqual(len(missing_msgs), 2)
        self.assertFalse(res["elements_found"]["consumer"])
        self.assertFalse(res["elements_found"]["non_goals"])

    def test_playback_mode_and_echo_detection(self):
        orig = "Please build a clean Python script that checks all mermaid diagrams across the entire wiki vault quickly."
        echo_playback = (
            "- **Goal**: Please build a clean Python script that checks all mermaid diagrams across the entire wiki vault quickly.\n"
            "- **Assumptions**: Assuming `wiki/` only.\n"
            "- **Success Check**: `check_diagrams.py --vault --strict` returns 0 errors.\n"
        )
        good_playback = (
            "- **Goal**: Implement an AST/regex CLI linter auditing Mermaid fences across `wiki/`, `mem/`, and `output/`.\n"
            "- **Problem & Assumptions**: IDE preview breaks on `pie` charts and unquoted parentheses; assuming Python stdlib only.\n"
            "- **Success Check**: Unit test suite passes 8/8 cases and `--vault --strict` exits 0.\n"
        )
        res_echo = check_brief.analyze_brief(echo_playback, "echo.md", mode="playback", original_prompt=orig)
        self.assertIn("echo-copy-detected", [f["rule"] for f in res_echo["findings"]])

        res_good = check_brief.analyze_brief(good_playback, "good.md", mode="playback", original_prompt=orig)
        self.assertEqual(res_good["findings"], [])

    def test_subjective_done_check_flagged_while_observable_passes(self):
        bad_brief = """- **Consumer**: Repo developers.
- **Goal**: Improve prompt formatting docs.
- **Done-Check**: Output looks good and high quality.
- **Non-Goals**: No code edits.
"""
        res = check_brief.analyze_brief(bad_brief, "subj.md", mode="brief")
        self.assertIn("missing-observable-check", [f["rule"] for f in res["findings"]])

        multiline_ok = """## Consumer
Future readers.
## Goal
Document cache behavior.
## Done-Check
- All 5 tests in `test_cache.py` pass without errors.
## Non-Goals
- No production config changes.
"""
        res_multi = check_brief.analyze_brief(multiline_ok, "multi.md", mode="brief")
        self.assertEqual(res_multi["findings"], [])

    def test_legacy_wikilink_and_overspecified_word_limit(self):
        filler = " ".join(["detail"] * 255)
        doc = (
            "- **Consumer**: [Harness Engineering](wiki/concepts/Harness%20Engineering.md) readers and [[Legacy Link]].\n"
            "- **Goal**: Summarize matrix [[-1, 0, 1]].\n"
            "- **Done-Check**: `lint_wiki.py` exits 0.\n"
            f"- **Non-Goals**: Keep scope small. {filler}\n"
        )
        res = check_brief.analyze_brief(doc, "over.md", mode="brief")
        rules = [f["rule"] for f in res["findings"]]
        self.assertEqual(rules, ["legacy-wikilink", "brief-overspecified"])
        self.assertEqual(res["findings"][0]["severity"], "error")
        self.assertEqual(res["findings"][1]["severity"], "info")

    def test_cli_stdin_strict_utf8_exit_codes(self):
        script_path = Path(__file__).resolve().parent / "check_brief.py"
        clean_vi = (
            "- **Đối tượng hưởng lợi**: Người đọc `tluc-wiki`.\n"
            "- **Mục tiêu**: Bổ sung sơ đồ kiến trúc cho bài ghi chú GPU.\n"
            "- **Tiêu chí hoàn thành**: Chạy `check_diagrams.py --vault --strict` đạt 0 lỗi.\n"
            "- **Ngoài phạm vi**: Không sửa file gốc trong `raw/`.\n"
        )
        proc_ok = subprocess.run(
            [sys.executable, str(script_path), "--stdin", "--strict"],
            input=clean_vi,
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(proc_ok.stdout)["status"], "ok")

        proc_bad = subprocess.run(
            [sys.executable, str(script_path), "--stdin", "--strict"],
            input="- **Goal**: Làm cho đẹp hơn.\n",
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(proc_bad.returncode, 1)
        self.assertGreater(json.loads(proc_bad.stdout)["summary"]["warning"], 0)

    def test_skill_frontmatter_and_no_omc_artifacts(self):
        skill_dir = Path(__file__).resolve().parent.parent
        skill_md = skill_dir / "SKILL.md"
        ref_md = skill_dir / "references" / "playback-and-examples.md"
        text = skill_md.read_text(encoding="utf-8")

        self.assertLess(len(text.splitlines()), 120)
        self.assertTrue(text.startswith("---\n"))
        fm = text.split("---", 2)[1]
        self.assertIn("name: sharpen", fm)
        self.assertTrue(ref_md.is_file())
        self.assertTrue((skill_dir / "scripts" / "check_brief.py").is_file())

        for p in (skill_md, ref_md):
            content = p.read_text(encoding="utf-8")
            self.assertFalse(
                re.search(r"\.omc/|/oh-my-claudecode:|\bdeep-interview\b|\bAskUserQuestion\b|\bTask\(", content),
                f"Found stale OMC/Claude reference in {p.name}",
            )


if __name__ == "__main__":
    unittest.main()
