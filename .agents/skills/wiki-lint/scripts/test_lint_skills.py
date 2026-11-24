#!/usr/bin/env python3
"""Unit tests for lint_skills.py."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_skills  # noqa: E402


class TestLintSkills(unittest.TestCase):
    """Test suite covering all checks in lint_skills.py."""

    def _make_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / ".agents" / "skills").mkdir(parents=True)
        (root / "ctx" / "rules").mkdir(parents=True)
        return tmp, root

    def _write(self, path: Path, content: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_compliant_skill_rule_and_credit_attribution_pass(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        skill_dir = root / ".agents" / "skills" / "demo-skill"
        self._write(skill_dir / "references" / "guide.md", "# Guide\n")
        self._write(skill_dir / "scripts" / "run.py", "print('ok')\n")
        self._write(
            skill_dir / "SKILL.md",
            (
                "---\n"
                "name: demo-skill\n"
                "description: >\n"
                "  Validate compliant multi-line YAML descriptions and relative links.\n"
                "allowed-tools:\n"
                "  - read_file\n"
                "  - write_file\n"
                "  - edit_file\n"
                "  - run_command\n"
                "---\n\n"
                "# Demo Skill\n\n"
                "Read [Guide](references/guide.md) and run `scripts/run.py`.\n"
                "Never write `[[Example Wikilink]]` or use `view_file` in new docs.\n\n"
                "```python\n"
                "matrix = [[1, 2], [3, 4]]\n"
                "```\n"
            ),
        )
        self._write(
            root / "ctx" / "rules" / "sample-rules.md",
            (
                "# Sample Rules\n\n"
                "> Adapted from oh-my-claudecode's `agent-doc-discipline` and `correct` concepts.\n\n"
                "- Avoid `[[Wikilink]]` syntax and replace `view_file` with `read_file`.\n"
            ),
        )

        report = lint_skills.lint_workspace(root)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["skills_checked"], 1)
        self.assertEqual(report["rules_checked"], 1)
        self.assertEqual(report["summary"], {"error": 0, "warning": 0, "by_code": {}})
        self.assertEqual(report["findings"], [])

    def test_missing_frontmatter_and_name_or_description_errors(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        self._write(
            root / ".agents" / "skills" / "no-fm" / "SKILL.md",
            "# No Frontmatter\n",
        )
        self._write(
            root / ".agents" / "skills" / "bad-meta" / "SKILL.md",
            (
                "---\n"
                "name: wrong-name\n"
                "description: \"\"\n"
                "---\n\n"
                "# Bad Meta\n"
            ),
        )
        too_long = "x" * 1025
        self._write(
            root / ".agents" / "skills" / "long-desc" / "SKILL.md",
            (
                "---\n"
                "name: long-desc\n"
                f"description: {too_long}\n"
                "---\n\n"
                "# Long Desc\n"
            ),
        )

        report = lint_skills.lint_workspace(root)
        self.assertEqual(report["status"], "error")
        codes = {item["file"]: [] for item in report["findings"]}
        for item in report["findings"]:
            codes[item["file"]].append(item["code"])

        self.assertIn("missing-frontmatter", codes[".agents/skills/no-fm/SKILL.md"])
        self.assertIn("invalid-skill-name", codes[".agents/skills/bad-meta/SKILL.md"])
        self.assertIn("invalid-skill-description", codes[".agents/skills/bad-meta/SKILL.md"])
        self.assertIn("invalid-skill-description", codes[".agents/skills/long-desc/SKILL.md"])

    def test_deprecated_allowed_tools_and_prose_detection(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        self._write(
            root / ".agents" / "skills" / "stale-tools" / "SKILL.md",
            (
                "---\n"
                "name: stale-tools\n"
                "description: Detects deprecated pre-Antigravity tool names.\n"
                "allowed-tools:\n"
                "  - run_command\n"
                "  - view_file\n"
                "  - write_to_file\n"
                "  - replace_file_content\n"
                "  - multi_replace_file_content\n"
                "  - grep_search\n"
                "---\n\n"
                "Call view_file directly to read.\n"
            ),
        )

        report = lint_skills.lint_workspace(root)
        stale_findings = [
            item for item in report["findings"] if item["code"] == "stale-tool-name"
        ]
        self.assertEqual(len(stale_findings), 6)
        self.assertEqual([item["line"] for item in stale_findings], [6, 7, 8, 9, 10, 13])

    def test_broken_links_and_backtick_subpaths_vs_placeholders_and_urls(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        skill_dir = root / ".agents" / "skills" / "link-check"
        self._write(skill_dir / "references" / "valid.md", "# Valid\n")
        self._write(
            skill_dir / "SKILL.md",
            (
                "---\n"
                "name: link-check\n"
                "description: Checks relative links and subpaths.\n"
                "---\n\n"
                "- Valid relative: [Valid](references/valid.md)\n"
                "- Broken relative: [Missing](references/missing.md)\n"
                "- External URL: [Docs](https://example.com/guide)\n"
                "- Anchor: [Top](#top)\n"
                "- Placeholder subpath: `references/<topic>.md` and `scripts/*.py`\n"
                "- Broken subpath: `scripts/missing_helper.py`\n"
            ),
        )

        report = lint_skills.lint_workspace(root)
        broken = [item for item in report["findings"] if item["code"] == "broken-skill-link"]
        self.assertEqual(len(broken), 2)
        self.assertEqual([item["line"] for item in broken], [7, 11])

    def test_leaked_external_runtime_and_wikilinks_vs_code_blocks(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        self._write(
            root / ".agents" / "skills" / "leaky-skill" / "SKILL.md",
            (
                "---\n"
                "name: leaky-skill\n"
                "description: Tests leaked external runtime detection.\n"
                "---\n\n"
                "Use [[Legacy Page]] in prose.\n\n"
                "```bash\n"
                "cat .omc/state/session.json\n"
                "echo ${CLAUDE_PLUGIN_ROOT}/run.sh\n"
                "```\n\n"
                "Invoke /oh-my-claudecode:autopilot or Task(subagent_type='x').\n\n"
                "```python\n"
                "nested = [[1, 2], [3, 4]]\n"
                "```\n"
            ),
        )
        self._write(
            root / "ctx" / "rules" / "bad-rule.md",
            (
                "# Bad Rule\n\n"
                "- Never keep .omc/config.json around.\n"
                "- Avoid [[Rule Wikilink]] here.\n"
                "- Keep `[[Backticked Array]]` ignored.\n"
            ),
        )

        report = lint_skills.lint_workspace(root)
        by_code = report["summary"]["by_code"]
        self.assertEqual(by_code.get("stale-external-runtime"), 5)
        self.assertEqual(by_code.get("legacy-wikilink"), 2)

    def test_oversized_skill_warning_and_strict_cli_exit_code(self) -> None:
        tmp, root = self._make_workspace()
        self.addCleanup(tmp.cleanup)

        filler_lines = "\n".join(f"Line {idx}" for idx in range(1, 497))
        skill_content = (
            "---\n"
            "name: large-skill\n"
            "description: Over 500 lines warning check.\n"
            "---\n\n"
            f"{filler_lines}\n"
        )
        self.assertEqual(len(skill_content.splitlines()), 501)
        self._write(root / ".agents" / "skills" / "large-skill" / "SKILL.md", skill_content)

        script_path = Path(__file__).resolve().parent / "lint_skills.py"

        non_strict = subprocess.run(
            [sys.executable, str(script_path), "--project-root", str(root)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(non_strict.returncode, 0, non_strict.stderr)
        non_strict_json = json.loads(non_strict.stdout)
        self.assertEqual(non_strict_json["status"], "warning")
        self.assertEqual(non_strict_json["summary"]["error"], 0)
        self.assertEqual(non_strict_json["summary"]["warning"], 1)
        self.assertEqual(non_strict_json["findings"][0]["code"], "oversized-skill-md")

        strict = subprocess.run(
            [sys.executable, str(script_path), "--project-root", str(root), "--strict"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(strict.returncode, 1, strict.stderr)


if __name__ == "__main__":
    unittest.main()
