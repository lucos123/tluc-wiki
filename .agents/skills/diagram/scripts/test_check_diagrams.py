"""
Unit Test Suite for diagram skill & scripts/check_diagrams.py.
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
import check_diagrams


class TestCheckDiagrams(unittest.TestCase):

    def test_valid_supported_mermaid_types_and_shapes_pass_cleanly(self):
        doc = """# Valid Diagrams

```mermaid
---
title: Architecture Flow
---
%% Leading comment
flowchart LR
    Start(["User Request"]) --> Safe["Parse (UTF-8 Input)"]
    Safe --> Store[("SQLite DB")]
    Safe --> Sub[["Run Helper"]]
    subgraph GroupA["Execution Layer"]
        Safe --> Done["End State"]
    end
```

```mermaid
sequenceDiagram
    Agent->>DB: queryItems(filter)
    DB-->>Agent: rows
```

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> [*]
```

```mermaid
xychart-beta
    x-axis ["A", "B"]
    y-axis "Score" 0 --> 10
    bar [6, 9]
```
"""
        res = check_diagrams.analyze_markdown_diagrams(doc, "valid.md")
        self.assertEqual(res["diagrams_count"], 4)
        self.assertEqual(res["diagram_types"], ["flowchart", "sequenceDiagram", "stateDiagram-v2", "xychart-beta"])
        self.assertEqual(res["findings"], [])

    def test_unsupported_mermaid_types_fail_with_error(self):
        for bad_type in ("gantt", "mindmap", "timeline", "pie"):
            doc = f"```mermaid\n{bad_type}\n    title Demo\n```\n"
            res = check_diagrams.analyze_markdown_diagrams(doc, f"{bad_type}.md")
            rules = [f["rule"] for f in res["findings"]]
            self.assertIn("unsupported-mermaid-type", rules)
            self.assertEqual(res["findings"][0]["severity"], "error")

    def test_unquoted_parentheses_label_warning_only_in_flowchart_or_graph(self):
        doc = """# Labels

```mermaid
graph TD
    A[Worker (Async)] --> B["Proper (Quoted)"]
```

```mermaid
sequenceDiagram
    Client->>Server: fetchData(id)
```
"""
        res = check_diagrams.analyze_markdown_diagrams(doc, "labels.md")
        warnings = [f for f in res["findings"] if f["rule"] == "unquoted-special-label"]
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]["severity"], "warning")
        self.assertEqual(warnings[0]["line"], 5)

    def test_html_tags_detected_in_mermaid(self):
        doc = """```mermaid
flowchart TD
    A["Line 1<br/>Line 2"] --> B["<b>Bold</b>"]
```
"""
        res = check_diagrams.analyze_markdown_diagrams(doc, "html.md")
        html_warns = [f for f in res["findings"] if f["rule"] == "html-tag-in-mermaid"]
        self.assertEqual(len(html_warns), 1)
        self.assertEqual(html_warns[0]["severity"], "warning")

    def test_unbalanced_subgraph_detected_while_end_in_label_ignored(self):
        bad_doc = """```mermaid
flowchart TD
    subgraph Outer
        A["Start"] --> B["End of phase"]
```
"""
        res_bad = check_diagrams.analyze_markdown_diagrams(bad_doc, "unclosed.md")
        self.assertEqual([f["rule"] for f in res_bad["findings"]], ["unbalanced-subgraph"])
        self.assertEqual(res_bad["findings"][0]["severity"], "error")

        good_doc = """```mermaid
flowchart TD
    subgraph Outer
        A["End state"] --> B["Next"]
    end
```
"""
        res_good = check_diagrams.analyze_markdown_diagrams(good_doc, "closed.md")
        self.assertEqual(res_good["findings"], [])

    def test_empty_oversized_and_nested_documentation_fence_handling(self):
        many_edges = "\n".join(f"    N{i} --> N{i + 1}" for i in range(47))
        doc = (
            "````markdown\n"
            "Example inside 4-backtick outer fence should be ignored:\n"
            "```mermaid\n"
            "pie\n"
            "```\n"
            "````\n\n"
            "```mermaid\n"
            "%% empty\n"
            "```\n\n"
            "```mermaid\n"
            "flowchart TD\n"
            f"{many_edges}\n"
            "```\n"
        )
        res = check_diagrams.analyze_markdown_diagrams(doc, "edge.md")
        self.assertEqual(res["diagrams_count"], 2)
        rules = [f["rule"] for f in res["findings"]]
        self.assertEqual(rules, ["empty-mermaid-block", "oversized-mermaid-diagram"])

    def test_cli_strict_and_vault_mode_utf8(self):
        script_path = Path(__file__).resolve().parent / "check_diagrams.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text("# Index\n", encoding="utf-8")
            concepts = root / "wiki" / "concepts"
            concepts.mkdir(parents=True)
            (concepts / "Quy Trình.md").write_text(
                "# Quy Trình\n\n```mermaid\nflowchart LR\n    A[\"Bước 1 (Khởi tạo)\"] --> B[\"Bước 2\"]\n```\n",
                encoding="utf-8",
            )
            proc_ok = subprocess.run(
                [sys.executable, str(script_path), "--vault", "--project-root", str(root), "--strict"],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            out_ok = json.loads(proc_ok.stdout)
            self.assertEqual(out_ok["status"], "ok")
            self.assertEqual(out_ok["diagrams_checked"], 1)

            warn_file = concepts / "Lỗi Nhãn.md"
            warn_file.write_text(
                "```mermaid\ngraph TD\n    X[Node (Unquoted)] --> Y[OK]\n```\n",
                encoding="utf-8",
            )
            proc_strict = subprocess.run(
                [sys.executable, str(script_path), str(warn_file), "--strict"],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertEqual(proc_strict.returncode, 1)
            out_warn = json.loads(proc_strict.stdout)
            self.assertEqual(out_warn["summary"]["warning"], 1)

    def test_skill_frontmatter_cleanliness_and_vocabulary_diagrams_pass(self):
        skill_dir = Path(__file__).resolve().parent.parent
        skill_md = skill_dir / "SKILL.md"
        vocab_md = skill_dir / "references" / "visual-vocabulary.md"
        text = skill_md.read_text(encoding="utf-8")

        self.assertLess(len(text.splitlines()), 120)
        self.assertTrue(text.startswith("---\n"))
        fm_block = text.split("---", 2)[1]
        self.assertIn("name: diagram", fm_block)
        self.assertIn("description:", fm_block)
        self.assertTrue(vocab_md.is_file())
        self.assertTrue((skill_dir / "scripts" / "check_diagrams.py").is_file())

        # Zero OMC / Claude Code runtime artifacts
        for p in (skill_md, vocab_md):
            content = p.read_text(encoding="utf-8")
            self.assertFalse(
                re.search(r"\.omc/|/oh-my-claudecode:|OMC_WORKFLOW_REGISTRY|xdg-open|\bTask\(", content),
                f"Found stale OMC reference in {p.name}",
            )

        # Every Mermaid diagram inside visual-vocabulary.md must pass cleanly
        vocab_report = check_diagrams.analyze_markdown_diagrams(vocab_md.read_text(encoding="utf-8"), vocab_md.name)
        self.assertGreaterEqual(vocab_report["diagrams_count"], 4)
        self.assertEqual(vocab_report["findings"], [])


if __name__ == "__main__":
    unittest.main()
