"""
Unit Test Suite for query_wiki.py
"""

import os
import sys
import unittest
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import query_wiki


class TestQueryWiki(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        # Create index.md
        self.index_path = os.path.join(self.temp_dir, "index.md")
        with open(self.index_path, "w", encoding="utf-8") as f:
            f.write("# Index\n- [[Harness Engineering]]: Scaffolding around model.\n- [[Loop Engineering]]: Agent loops.")

        # Create wiki/concepts/
        self.concepts_dir = os.path.join(self.temp_dir, "wiki", "concepts")
        os.makedirs(self.concepts_dir)

        self.harness_file = os.path.join(self.concepts_dir, "Harness Engineering.md")
        with open(self.harness_file, "w", encoding="utf-8") as f:
            f.write("---\ntitle: Harness Engineering\n---\n# Harness Engineering\nOuter execution layer.")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_search_index(self):
        matches = query_wiki.search_index(self.index_path, "Harness")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["page_name"], "Harness Engineering")

    def test_search_content_files(self):
        matches = query_wiki.search_content_files(self.temp_dir, "Outer execution")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["page_name"], "Harness Engineering")
        self.assertEqual(matches[0]["match_count"], 1)

    def test_search_no_match(self):
        matches = query_wiki.search_content_files(self.temp_dir, "NonExistentKeyword")
        self.assertEqual(len(matches), 0)

    def test_search_index_standard_markdown_links(self):
        with open(self.index_path, "w", encoding="utf-8") as f:
            f.write(
                "# Index\n"
                "- [Harness Engineering](wiki/concepts/Harness%20Engineering.md): Scaffolding around model.\n"
                "- [Loop Engineering](wiki/concepts/Loop%20Engineering.md): Agent loops.\n"
            )
        matches = query_wiki.search_index(self.index_path, "Harness")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["page_name"], "Harness Engineering")
        self.assertEqual(matches[0]["rel_path"], "wiki/concepts/Harness Engineering.md")


if __name__ == "__main__":
    unittest.main()
