"""
Unit Test Suite for technical-writing skill & scripts/check_prose.py.
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
import check_prose


class TestCheckProse(unittest.TestCase):

    def test_clean_bilingual_document_passes_with_zero_findings(self):
        doc = """---
title: "Benchmark Summary"
date: 2026-11-24
tags:
  - report
---

# Benchmark Summary

Migration cut test suite runtime from 12.4s to 0.8s (`7/7` pass in [test_lint_wiki.py](test_lint_wiki.py)).

## Findings
- Batching edits reduced round-trips by 4x at \\$0.20 input vs \\$1.20 output per 1M tokens.
- KaTeX inline formula $z = w^T x + b$ and $10^{28}$ FLOP stay untouched.

## Related Pages
- **Concepts**:
  - [Harness Engineering](../wiki/concepts/Harness%20Engineering.md)
  - [Loop Engineering](../wiki/concepts/Loop%20Engineering.md)
  - [Context Engineering](../wiki/concepts/Context%20Engineering.md)
"""
        report = check_prose.analyze_markdown(doc, "clean.md")
        self.assertEqual(report["findings"], [])

    def test_ai_filler_detected_outside_code_and_blockquotes(self):
        doc = """---
title: "Draft"
date: 2026-11-24
---

# Draft

> Quote: In today's fast-paced world, it is important to note that verbatim quotes stay intact.

```markdown
In today's fast-paced world, code fences also stay intact.
```

Inline example `delve into` should be ignored.
Trong thời đại công nghệ phát triển nhanh chóng, hệ thống đóng vai trò vô cùng quan trọng.
"""
        report = check_prose.analyze_markdown(doc, "filler.md")
        rules = [f["rule"] for f in report["findings"]]
        self.assertEqual(rules.count("ai-filler-phrase"), 2)
        self.assertTrue(all(f["line"] == 15 for f in report["findings"]))

    def test_vague_unquantified_claims_require_numbers_or_citations(self):
        doc = """# Performance Note

The new parser is significantly faster and cải thiện đáng kể.
The cached parser is significantly faster (42ms vs 310ms).
The indexed lookup is significantly faster per [Benchmark Report](bench.md).
"""
        report = check_prose.analyze_markdown(doc, "claims.md")
        vague = [f for f in report["findings"] if f["rule"] == "vague-unquantified-claim"]
        self.assertEqual(len(vague), 2)
        self.assertTrue(all(f["line"] == 3 for f in vague))

    def test_legacy_wikilink_detected_while_arrays_ignored(self):
        doc = """# Links

Nested convolution array [[-1, 0, 1], [-2, 0, 2]] is math, not a link.
Broken legacy [[Harness Engineering]] should fail.
"""
        report = check_prose.analyze_markdown(doc, "links.md")
        errs = [f for f in report["findings"] if f["rule"] == "legacy-wikilink"]
        self.assertEqual(len(errs), 1)
        self.assertEqual(errs[0]["severity"], "error")
        self.assertEqual(errs[0]["line"], 4)

    def test_katex_currency_collision_detection(self):
        doc = """# Pricing

Bad pricing: costs $5.00 input and $30.00 output per million tokens.
Good pricing: costs \\$5.00 input and \\$30.00 output per million tokens.
Single price: flat $5.00 tier has only one dollar sign.
Math formula: $x_1 + x_2 = y$ stays clean.
"""
        report = check_prose.analyze_markdown(doc, "pricing.md")
        hits = [f for f in report["findings"] if f["rule"] == "katex-currency-collision"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["line"], 3)

    def test_dense_related_links_detected(self):
        doc = """# Page

## Related Pages
- **Concepts**: [A](a.md), [B](b.md), [C](c.md)
- **Entities**: [E1](e1.md), [E2](e2.md)
"""
        report = check_prose.analyze_markdown(doc, "related.md")
        dense = [f for f in report["findings"] if f["rule"] == "dense-related-links"]
        self.assertEqual(len(dense), 1)
        self.assertEqual(dense[0]["line"], 4)

    def test_cli_strict_mode_and_utf8_support(self):
        script_path = Path(__file__).resolve().parent / "check_prose.py"
        with tempfile.TemporaryDirectory() as tmp:
            warn_file = Path(tmp) / "nháp-báo-cáo.md"
            warn_file.write_text("# Nháp\n\nNhư chúng ta đã biết, tool chạy tốt.\n", encoding="utf-8")

            proc_default = subprocess.run(
                [sys.executable, str(script_path), str(warn_file)],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            out_default = json.loads(proc_default.stdout)
            self.assertEqual(out_default["status"], "warn")
            self.assertEqual(out_default["summary"]["warning"], 1)

            proc_strict = subprocess.run(
                [sys.executable, str(script_path), str(warn_file), "--strict"],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertEqual(proc_strict.returncode, 1)

    def test_skill_frontmatter_and_no_omc_artifacts(self):
        skill_dir = Path(__file__).resolve().parent.parent
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        lines = text.splitlines()

        self.assertLess(len(lines), 500)
        self.assertTrue(text.startswith("---\n"))
        fm_block = text.split("---", 2)[1]
        self.assertIn("name: technical-writing", fm_block)
        self.assertIn("description:", fm_block)

        # Linked companion files must exist
        self.assertTrue((skill_dir / "references" / "minimal-prose-discipline.md").is_file())
        self.assertTrue((skill_dir / "scripts" / "check_prose.py").is_file())

        # Ensure clean Antigravity port (no leftover Claude Code / OMC runtime references)
        for p in (skill_md, skill_dir / "references" / "minimal-prose-discipline.md"):
            content = p.read_text(encoding="utf-8")
            self.assertFalse(re.search(r"\.omc/|/oh-my-claudecode:|CLAUDE_PLUGIN_ROOT|\bTask\(", content), f"Found stale OMC reference in {p.name}")


if __name__ == "__main__":
    unittest.main()
