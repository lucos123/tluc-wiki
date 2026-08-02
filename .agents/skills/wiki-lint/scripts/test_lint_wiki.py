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


if __name__ == "__main__":
    unittest.main()
