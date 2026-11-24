#!/usr/bin/env python3
"""Unit tests for check_memory.py and wiki-manage documentation hygiene."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_memory  # noqa: E402


class TestCheckMemory(unittest.TestCase):
    """Test suite covering all checks in check_memory.py."""

    def _make_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "mem" / "preferences").mkdir(parents=True)
        (root / "mem" / "projects").mkdir(parents=True)
        (root / "mem" / "goals").mkdir(parents=True)
        (root / "mem" / "people").mkdir(parents=True)
        (root / "mem" / "history").mkdir(parents=True)
        (root / "wiki" / "concepts").mkdir(parents=True)
        return tmp, root

    def _write(self, path: Path, content: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_compliant_mem_hierarchy_passes(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        self._write(root / "wiki" / "concepts" / "Harness Engineering.md", "# Harness\n")
        self._write(
            root / "mem" / "gemini.md",
            (
                "---\n"
                "title: \"Identity\"\n"
                "date: 2026-11-24\n"
                "tags:\n"
                "  - identity\n"
                "  - memory\n"
                "---\n\n"
                "- Linked [Harness Engineering](../wiki/concepts/Harness%20Engineering.md).\n"
            ),
        )
        self._write(
            root / "mem" / "preferences" / "Coding Style.md",
            (
                "---\n"
                "title: \"Coding Style\"\n"
                "date: 2026-11-24\n"
                "tags:\n"
                "  - preference\n"
                "---\n\n"
                "- **Run tests**: Always pass `--strict`. (Evidence: 2026-11-24 directive)\n"
            ),
        )
        self._write(
            root / "mem" / "projects" / "Brain.md",
            (
                "---\n"
                "title: \"Brain\"\n"
                "date: 2026-11-24\n"
                "tags:\n"
                "  - project\n"
                "status: active # active | completed\n"
                "---\n\n"
                "Uses [Harness Engineering](../../wiki/concepts/Harness%20Engineering.md).\n"
            ),
        )
        self._write(
            root / "mem" / "goals" / "2026 Goal.md",
            (
                "---\n"
                "title: \"2026 Goal\"\n"
                "date: 2026-11-24\n"
                "tags: [goal, career]\n"
                "status: planned\n"
                "---\n\n"
                "Goal body.\n"
            ),
        )
        self._write(
            root / "mem" / "people" / "Alex.md",
            "---\ntitle: \"Alex\"\ndate: 2026-11-24\ntags:\n  - person\n---\n\nColleague.\n",
        )
        self._write(
            root / "mem" / "history" / "Q4.md",
            "---\ntitle: \"Q4\"\ndate: 2026-11-24\ntags:\n  - history\n---\n\nMilestone.\n",
        )

        report = check_memory.lint_memory(root)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["files_checked"], 6)
        self.assertEqual(report["summary"], {"error": 0, "warning": 0, "by_code": {}})

    def test_missing_frontmatter_fields_invalid_date_and_status(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        self._write(root / "mem" / "history" / "no-fm.md", "# Plain file\n")
        self._write(
            root / "mem" / "projects" / "bad-meta.md",
            (
                "---\n"
                "title: \"Bad Project\"\n"
                "date: 2026/11/24\n"
                "status: archived\n"
                "---\n\n"
                "Body.\n"
            ),
        )

        report = check_memory.lint_memory(root)
        by_code = report["summary"]["by_code"]
        self.assertEqual(report["status"], "error")
        self.assertEqual(by_code.get("missing-frontmatter"), 1)
        self.assertEqual(by_code.get("missing-field"), 1)
        self.assertEqual(by_code.get("invalid-date"), 1)
        self.assertEqual(by_code.get("invalid-status"), 1)

    def test_secret_leak_detection_vs_placeholders(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        leaked_openai = "sk-" + "AbCdEfGhIjKlMnOpQrSt1234"
        leaked_gh = "ghp_" + "1234567890abcdefghij1234567890"
        leaked_google = "AIza" + "SyNotARealGoogleKey1234567890"
        private_header = "-----BEGIN RSA " + "PRIVATE KEY-----"

        self._write(
            root / "mem" / "preferences" / "Secrets.md",
            (
                "---\ntitle: \"Secrets\"\ndate: 2026-11-24\ntags:\n  - preference\n---\n\n"
                f"- OpenAI: `{leaked_openai}`\n"
                f"- GitHub: {leaked_gh}\n"
                f"- Google: {leaked_google}\n"
                f"- {private_header}\n"
                "- api_key=\"real_secret_token_value_99\"\n"
                "- Safe placeholder: api_key=\"YOUR_EXAMPLE_KEY_12345\"\n"
                "- Safe placeholder 2: `api_key=<REDACTED_VALUE>`\n"
            ),
        )

        report = check_memory.lint_memory(root)
        secret_findings = [item for item in report["findings"] if item["code"] == "secret-leak"]
        self.assertEqual([item["line"] for item in secret_findings], [8, 9, 10, 11, 12])

    def test_legacy_wikilink_and_broken_links_vs_code_fences(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        self._write(root / "wiki" / "concepts" / "Valid.md", "# Valid\n")
        self._write(
            root / "mem" / "projects" / "Links.md",
            (
                "---\ntitle: \"Links\"\ndate: 2026-11-24\ntags:\n  - project\nstatus: active\n---\n\n"
                "- Good: [Valid](../../wiki/concepts/Valid.md) and [URL](https://example.com)\n"
                "- Broken: [Missing](../../wiki/concepts/Missing.md)\n"
                "- Legacy: [[Old Concept]] and inline `[[Code Example]]`\n\n"
                "```python\n"
                "arr = [[1, 2], [3, 4]]\n"
                "```\n"
            ),
        )

        report = check_memory.lint_memory(root)
        codes = [(item["code"], item["line"]) for item in report["findings"]]
        self.assertEqual(codes, [("broken-memory-link", 10), ("legacy-wikilink", 11)])

    def test_unconfirmed_hypothesis_warning_and_cli_strict(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        self._write(
            root / "mem" / "preferences" / "DraftPrefs.md",
            (
                "---\ntitle: \"Draft\"\ndate: 2026-11-24\ntags:\n  - preference\n---\n\n"
                "- [Hypothesis] Prefers short answers.\n"
                "- Unconfirmed: Avoid tables in summaries.\n"
                "- Example marker in code `TBD` stays ignored.\n"
            ),
        )

        script_path = Path(__file__).resolve().parent / "check_memory.py"
        non_strict = subprocess.run(
            [sys.executable, str(script_path), "--project-root", str(root)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(non_strict.returncode, 0, non_strict.stderr)
        data = json.loads(non_strict.stdout)
        self.assertEqual(data["status"], "warning")
        self.assertEqual(data["summary"]["warning"], 2)
        self.assertEqual(data["summary"]["error"], 0)

        strict = subprocess.run(
            [sys.executable, str(script_path), "--project-root", str(root), "--strict"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(strict.returncode, 1, strict.stderr)

    def test_wiki_manage_skill_and_guide_no_stale_artifacts(self) -> None:
        skill_dir = Path(__file__).resolve().parent.parent
        skill_md = skill_dir / "SKILL.md"
        guide_md = skill_dir / "references" / "memory-management-guide.md"

        for doc in (skill_md, guide_md):
            content = doc.read_text(encoding="utf-8")
            self.assertFalse(
                re.search(
                    r"\.omc/|/oh-my-claudecode:|\bCLAUDE_PLUGIN_ROOT\b|\bTask\(|\bview_file\b|\bwrite_to_file\b|\bgrep_search\b",
                    content,
                ),
                f"Found stale artifact or deprecated tool name in {doc.name}",
            )


if __name__ == "__main__":
    unittest.main()
