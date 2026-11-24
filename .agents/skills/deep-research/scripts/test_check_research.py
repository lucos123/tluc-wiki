"""
Unit Test Suite for deep-research skill & scripts/check_research.py.
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
import check_research


class TestCheckResearch(unittest.TestCase):

    def test_clean_bilingual_research_brief_passes_with_zero_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ref_doc = root / "source-note.md"
            ref_doc.write_text("# Source Note\nVerified spec.\n", encoding="utf-8")

            brief_text = """---
title: "Cache Investigation"
date: 2026-11-24
tags:
  - analysis
---

# Cache Investigation

## Executive Answer
Prompt prefix stability keeps cached token hits active per [Source Note](source-note.md).

## Findings by Confidence Tier
- **[Direct]**: System prompt edits invalidate cached prefixes ([Source Note](source-note.md)).
- **[Direct]**: Verified handler behavior in `src/cache.py:42`.
- **[Supported]**: External spec aligns with measured runs at https://example.com/spec and repeated benchmarks confirm the 42ms latency median across 5 trials.
- **[Inferred]**: Keeping volatile timestamps at the tail appears to preserve prefix reuse across turns.

## What Remains Unknown
- Tested server logs (`logs/cache.log`) and config (`config.yaml`); billing breakdown per tier was not recorded.
"""
            res = check_research.analyze_research_brief(brief_text, "brief.md", file_dir=root)
            self.assertTrue(res["has_unknowns_section"])
            self.assertGreaterEqual(res["tier_counts"]["direct"], 2)
            self.assertEqual(res["findings"], [])

    def test_weasel_words_flagged_outside_code_and_quotes(self):
        doc = """# Quick Check

> Verbatim quote: "Obviously, this legacy hook must stay."

```text
Obviously ignore fenced code blocks.
```

Inline example `of course` is fine.
Clearly the retry works and hiển nhiên là không cần kiểm tra thêm.
"""
        res = check_research.analyze_research_brief(doc, "weasel.md")
        weasels = [f for f in res["findings"] if f["rule"] == "forbidden-certainty-weasel"]
        self.assertEqual(len(weasels), 2)
        self.assertTrue(all(f["line"] == 10 for f in weasels))

    def test_uncited_direct_claims_detected_while_valid_citations_pass(self):
        doc = """# Findings

## Direct Evidence
- System drops idle connections after 30s with no source attached.
- Worker pool size defaults to 8 threads in `runtime/pool.py:19`.
- Spec published at https://example.com/docs/pool confirms backpressure queue limit.
- **[Direct]** This uncited claim should also trigger a warning.
"""
        res = check_research.analyze_research_brief(doc, "direct.md")
        uncited = [f for f in res["findings"] if f["rule"] == "uncited-direct-claim"]
        self.assertEqual([f["line"] for f in uncited], [4, 7])

    def test_broken_local_citation_and_legacy_wikilink_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "exists.md").write_text("# Exists\n", encoding="utf-8")

            doc = """# Citations

Valid link: [Existing](exists.md) and external [Docs](https://example.com).
Math array [[-1, 0, 1], [0, 1, 0]] stays untouched.
Broken local file: [Missing](missing%20file.md).
Legacy syntax: [[Harness Engineering]].
"""
            res = check_research.analyze_research_brief(doc, "citations.md", file_dir=root)
            errors = [f for f in res["findings"] if f["severity"] == "error"]
            self.assertEqual([f["rule"] for f in errors], ["broken-local-citation", "legacy-wikilink"])
            self.assertEqual([f["line"] for f in errors], [5, 6])

    def test_missing_unknowns_section_and_vietnamese_heading_support(self):
        filler_words = " ".join(["evidence"] * 105)
        bad_doc = f"# Long Brief\n\n- **[Direct]** Observed in `log.txt`.\n\n{filler_words}\n"
        res_bad = check_research.analyze_research_brief(bad_doc, "no-unknowns.md")
        self.assertFalse(res_bad["has_unknowns_section"])
        self.assertIn("missing-unknowns-section", [f["rule"] for f in res_bad["findings"]])

        good_doc = f"{bad_doc}\n## Chưa xác minh & Giới hạn\n- Đã kiểm tra `log.txt`, chưa có trace mạng.\n"
        res_good = check_research.analyze_research_brief(good_doc, "vi-unknowns.md")
        self.assertTrue(res_good["has_unknowns_section"])
        self.assertNotIn("missing-unknowns-section", [f["rule"] for f in res_good["findings"]])

    def test_cli_strict_and_stdin_utf8(self):
        script_path = Path(__file__).resolve().parent / "check_research.py"
        clean_stdin = (
            "# Kết quả kiểm tra\n\n"
            "- **[Direct]** Ghi nhận tại `scripts/lint_wiki.py:145`.\n\n"
            "## What Remains Unknown\n- Chưa đo thời gian chạy trên 10,000 file.\n"
        )
        proc_ok = subprocess.run(
            [sys.executable, str(script_path), "--stdin", "--strict"],
            input=clean_stdin,
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        out_ok = json.loads(proc_ok.stdout)
        self.assertEqual(out_ok["status"], "ok")

        warn_stdin = "- **[Direct]** Khẳng định không có nguồn trích dẫn.\n"
        proc_warn = subprocess.run(
            [sys.executable, str(script_path), "--stdin", "--strict"],
            input=warn_stdin,
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(proc_warn.returncode, 1)
        self.assertEqual(json.loads(proc_warn.stdout)["summary"]["warning"], 1)

    def test_skill_frontmatter_and_no_omc_artifacts(self):
        skill_dir = Path(__file__).resolve().parent.parent
        skill_md = skill_dir / "SKILL.md"
        ep_md = skill_dir / "references" / "epistemics.md"
        text = skill_md.read_text(encoding="utf-8")

        self.assertLess(len(text.splitlines()), 120)
        self.assertTrue(text.startswith("---\n"))
        fm = text.split("---", 2)[1]
        self.assertIn("name: deep-research", fm)
        self.assertTrue(ep_md.is_file())
        self.assertTrue((skill_dir / "scripts" / "check_research.py").is_file())

        for p in (skill_md, ep_md):
            content = p.read_text(encoding="utf-8")
            self.assertFalse(
                re.search(r"\.omc/|/oh-my-claudecode:|\bsciomc\b|\bdeep-dive\b|\bautoresearch\b|docs/CREDITS\.md|\bTask\(", content),
                f"Found stale OMC reference in {p.name}",
            )

    def test_unvetted_benchmark_claim_detection_and_valid_vetted_figures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bench.md").write_text("# Bench\nMedian 42ms.\n", encoding="utf-8")

            doc = """# Performance Notes

> Verbatim quote: "This mode is 3x faster under synthetic load."

| Metric | Value |
| --- | --- |
| Latency | 42ms |

- Caching makes retrieval 2.4x faster.
- Measured p95 latency 42ms across 5 runs.
- Measured p95 latency 42ms median across 5 warm runs ([Bench](bench.md)).
- Rough estimate: batching yields 2x faster ingest (unmeasured).
"""
            res = check_research.analyze_research_brief(doc, "bench-brief.md", file_dir=root)
            unvetted = [f for f in res["findings"] if f["rule"] == "unvetted-benchmark-claim"]
            self.assertEqual([f["line"] for f in unvetted], [9, 10])


if __name__ == "__main__":
    unittest.main()
