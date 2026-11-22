"""
Unit Test Suite for lint_wiki.py
"""

import os
import sys
import unittest
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_wiki


class TestLintWiki(unittest.TestCase):

    def test_parse_frontmatter_valid(self):
        content = """---
title: "Test Page"
date: 2026-08-02
tags:
  - test
  - unit
source: "[[raw/test.md]]"
---
# Content Header
"""
        fm = lint_wiki.parse_frontmatter(content)
        self.assertIsNotNone(fm)
        self.assertEqual(fm["title"], "Test Page")
        self.assertEqual(fm["date"], "2026-08-02")
        self.assertEqual(fm["tags"], ["test", "unit"])
        self.assertEqual(fm["source"], "[[raw/test.md]]")

    def test_parse_frontmatter_missing(self):
        content = "# Just Header\nNo frontmatter here."
        fm = lint_wiki.parse_frontmatter(content)
        self.assertIsNone(fm)

    def test_extract_wiki_links(self):
        content = "Link to [[Page A]] and [[Page B|Display Name]] and [[Page C#Section]]"
        links = lint_wiki.extract_wiki_links(content)
        self.assertEqual(links, ["Page A", "Page B", "Page C#Section"])

    def test_extract_wiki_links_table_escaped_pipe(self):
        content = (
            "| Target | Link |\n"
            "| :--- | :--- |\n"
            r"| Cell 1 | [[Page A\|Alias A]] and [[Page B#Section\|Alias B]] |"
            "\n"
            r"| Cell 2 | [[Page C \| Alias C]] |"
        )
        links = lint_wiki.extract_wiki_links(content)
        self.assertEqual(links, ["Page A", "Page B#Section", "Page C"])

        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = os.path.join(tmp_dir, "index.md")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write("# Index\n- [[Page A]]\n- [[Page B]]\n")
            wiki_dir = os.path.join(tmp_dir, "wiki")
            os.makedirs(wiki_dir)
            with open(os.path.join(wiki_dir, "Page A.md"), "w", encoding="utf-8") as f:
                f.write(
                    "---\ntitle: Page A\ndate: 2026-11-22\ntags:\n  - test\n---\n\n"
                    "| Col | Ref |\n| :--- | :--- |\n"
                    r"| Row | [[Page B\|Display]] |"
                )
            with open(os.path.join(wiki_dir, "Page B.md"), "w", encoding="utf-8") as f:
                f.write("---\ntitle: Page B\ndate: 2026-11-22\ntags:\n  - test\n---\n# Page B\n")
            report = lint_wiki.lint_wiki(tmp_dir, index_path)
            self.assertEqual(report["stats"]["total_broken_links"], 0)
            self.assertEqual(report["broken_links"], [])

    def test_validate_date(self):
        self.assertTrue(lint_wiki.validate_date("2026-08-02"))
        self.assertFalse(lint_wiki.validate_date("02-08-2026"))
        self.assertFalse(lint_wiki.validate_date("2026/08/02"))
        self.assertFalse(lint_wiki.validate_date("invalid-date"))

    def test_lint_wiki_engine(self):
        """End-to-end test of lint_wiki engine on temporary mock project."""
        temp_dir = tempfile.mkdtemp()
        try:
            # Create index.md
            index_path = os.path.join(temp_dir, "index.md")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write("# Index\n- [[Page A]]\n- [[Broken Page]]")

            # Create wiki/
            wiki_dir = os.path.join(temp_dir, "wiki")
            os.makedirs(wiki_dir)

            # Create page_a.md
            page_a_path = os.path.join(wiki_dir, "Page A.md")
            with open(page_a_path, "w", encoding="utf-8") as f:
                f.write("---\ntitle: Page A\ndate: 2026-08-02\ntags:\n  - test\n---\n# Page A\nSee [[Page B]]")

            # Create orphan page_b.md (not in index)
            page_b_path = os.path.join(wiki_dir, "Page B.md")
            with open(page_b_path, "w", encoding="utf-8") as f:
                f.write("---\ntitle: Page B\ndate: 2026-08-02\ntags:\n  - test\n---\n# Page B")

            # Run lint engine
            report = lint_wiki.lint_wiki(temp_dir, index_path)

            self.assertEqual(report["stats"]["total_wiki_pages"], 2)
            self.assertEqual(len(report["orphan_pages"]), 1)
            self.assertEqual(report["orphan_pages"][0]["name"], "Page B")
            self.assertEqual(report["missing_pages"], ["Broken Page"])
            self.assertEqual(len(report["broken_links"]), 0)

        finally:
            shutil.rmtree(temp_dir)

    def test_standard_markdown_links_special_chars_duplicate_stems_and_broken_detection(self):
        """Verify Standard Relative Markdown Links with RFC 3986 encoding, anchors, raw paths, and duplicate stems."""
        with tempfile.TemporaryDirectory() as tmp:
            index_path = os.path.join(tmp, "index.md")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(
                    "# Wiki Index\n\n"
                    "## Concepts\n"
                    "- [Amazon Web Services (AWS)](wiki/concepts/Amazon%20Web%20Services%20%28AWS%29.md): AWS note.\n"
                    "- [Harness Engineering](wiki/concepts/Harness%20Engineering.md): Concept page.\n\n"
                    "## Sources\n"
                    "- [Harness Engineering](wiki/sources/Harness%20Engineering.md): Source summary.\n"
                    "- [OpenAI's $10B Bet](wiki/sources/OpenAI%27s%20%2410B%20Bet.md): Market note.\n"
                )

            for sub in ("wiki/concepts", "wiki/sources", "raw/articles"):
                os.makedirs(os.path.join(tmp, sub), exist_ok=True)

            with open(os.path.join(tmp, "raw", "articles", "harness.md"), "w", encoding="utf-8") as f:
                f.write("# Raw Harness\n")

            with open(os.path.join(tmp, "wiki", "concepts", "Amazon Web Services (AWS).md"), "w", encoding="utf-8") as f:
                f.write(
                    "---\n"
                    'title: "Amazon Web Services (AWS)"\n'
                    "date: 2026-11-22\n"
                    "tags:\n  - concept\n"
                    "---\n\n"
                    "See [Harness Concept](Harness%20Engineering.md#definition) and "
                    "[AWS $10B Source](../sources/OpenAI%27s%20%2410B%20Bet.md).\n"
                    "Also check external https link `[not checked](https://example.com)` and ```[[Ignored]]```.\n"
                )

            with open(os.path.join(tmp, "wiki", "concepts", "Harness Engineering.md"), "w", encoding="utf-8") as f:
                f.write(
                    "---\n"
                    'title: "Harness Concept"\n'
                    "date: 2026-11-22\n"
                    "tags:\n  - concept\n"
                    "---\n\n"
                    "## Definition\nCore concept referencing [Harness Source](../sources/Harness%20Engineering.md).\n"
                )

            with open(os.path.join(tmp, "wiki", "sources", "Harness Engineering.md"), "w", encoding="utf-8") as f:
                f.write(
                    "---\n"
                    'title: "Harness Source"\n'
                    "date: 2026-11-22\n"
                    "tags:\n  - source\n"
                    'source: "raw/articles/harness.md"\n'
                    "---\n\n"
                    "**Source File**: [raw/articles/harness.md](../../raw/articles/harness.md)\n"
                )

            with open(os.path.join(tmp, "wiki", "sources", "OpenAI's $10B Bet.md"), "w", encoding="utf-8") as f:
                f.write(
                    "---\n"
                    "title: \"OpenAI's $10B Bet\"\n"
                    "date: 2026-11-22\n"
                    "tags:\n  - source\n"
                    'source: "raw/articles/harness.md"\n'
                    "---\n\n"
                    "Valid backlink to [AWS](../../wiki/concepts/Amazon%20Web%20Services%20%28AWS%29.md).\n"
                )

            report = lint_wiki.lint_wiki(tmp, index_path)
            self.assertEqual(report["orphan_pages"], [])
            self.assertEqual(report["missing_pages"], [])
            self.assertEqual(report["broken_links"], [])
            self.assertEqual(report["legacy_wikilinks"], [])
            self.assertEqual(report["stats"]["total_markdown_links"], 5)
            self.assertEqual(report["stats"]["index_coverage_pct"], 100.0)

            # Now introduce a broken relative link + a legacy wikilink to confirm detection
            with open(os.path.join(tmp, "wiki", "concepts", "Harness Engineering.md"), "a", encoding="utf-8") as f:
                f.write("\nBroken [Missing Target](Does%20Not%20Exist.md) and legacy [[Amazon Web Services (AWS)]].\n")

            bad_report = lint_wiki.lint_wiki(tmp, index_path)
            self.assertEqual(len(bad_report["broken_links"]), 1)
            self.assertEqual(bad_report["broken_links"][0]["broken_link"], "Does%20Not%20Exist.md")
            self.assertEqual(bad_report["stats"]["total_legacy_wikilinks"], 1)
            self.assertEqual(bad_report["legacy_wikilinks"][0]["wikilink"], "[[Amazon Web Services (AWS)]]")


if __name__ == "__main__":
    unittest.main()
