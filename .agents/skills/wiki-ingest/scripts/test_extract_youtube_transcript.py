"""
Unit Test Suite for extract_youtube_transcript.py and capture_youtube_keyframes.py curation helpers
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capture_youtube_keyframes
import extract_youtube_transcript


class TestExtractYoutubeTranscript(unittest.TestCase):

    def test_clean_vtt(self):
        vtt_content = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:04.000
<c>Hello</c> and welcome to

00:00:04.000 --> 00:00:06.000
this AI &amp; LLM tutorial.
"""
        cleaned = extract_youtube_transcript.clean_vtt(vtt_content)
        self.assertNotIn("WEBVTT", cleaned)
        self.assertNotIn("-->", cleaned)
        self.assertIn("Hello and welcome to", cleaned)
        self.assertIn("this AI & LLM tutorial.", cleaned)

    def test_clean_srt(self):
        srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello and welcome to

2
00:00:04,000 --> 00:00:06,000
this AI tutorial.
"""
        cleaned = extract_youtube_transcript.clean_srt(srt_content)
        self.assertNotIn("-->", cleaned)
        self.assertIn("Hello and welcome to", cleaned)
        self.assertIn("this AI tutorial.", cleaned)

    def test_format_duration(self):
        self.assertEqual(extract_youtube_transcript.format_duration(3665), "1h 1m 5s")
        self.assertEqual(extract_youtube_transcript.format_duration(125), "2m 5s")
        self.assertEqual(extract_youtube_transcript.format_duration(0), "Unknown")

    def test_format_upload_date(self):
        self.assertEqual(extract_youtube_transcript.format_upload_date("20260802"), "2026-08-02")
        self.assertEqual(extract_youtube_transcript.format_upload_date("invalid"), "invalid")

    def test_sanitize_filename(self):
        raw_title = 'What is "Harness Engineering"? <Part 1>'
        sanitized = extract_youtube_transcript.sanitize_filename(raw_title)
        self.assertNotIn('"', sanitized)
        self.assertNotIn('<', sanitized)
        self.assertNotIn('>', sanitized)
        self.assertEqual(sanitized, "What is Harness Engineering Part 1")

    def test_suggest_keyframe_timestamps_late_chapter_and_builder(self):
        chapters = [
            {"start_time": 0, "end_time": 100, "title": "Understand Loop Engineering? Yes!"},
            {"start_time": 100, "end_time": 120, "title": "Short Demo"},
        ]
        suggested = extract_youtube_transcript.suggest_keyframe_timestamps(
            cues=[], chapters=chapters, duration=120
        )
        self.assertEqual(len(suggested), 2)
        self.assertEqual(suggested[0]["timestamp_sec"], 88)
        self.assertEqual(suggested[1]["timestamp_sec"], 116)
        ts_arg = extract_youtube_transcript.build_timestamps_arg(suggested)
        self.assertEqual(
            ts_arg,
            "01:28=Understand-Loop-Engineering-Yes,01:56=Short-Demo",
        )

    def test_find_related_wiki_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text(
                "\n".join([
                    "# Index",
                    "",
                    "## Entities",
                    "- [[IBM Technology]]: Official IBM technical education channel.",
                    "- [[Unrelated Lab]]: Something else.",
                    "",
                    "## Concepts",
                    "- [[Loop Engineering]]: Agent loop patterns and safeguards.",
                    "- [[Prompt Engineering]]: Single-turn prompting technique.",
                    "- [[raw/ignored]]: Raw should not appear.",
                    "",
                ]),
                encoding="utf-8",
            )
            matches = extract_youtube_transcript.find_related_wiki_pages(
                root,
                title="What Is Loop Engineering? Building Better AI Agents",
                chapters=[{"title": "Compare Prompt vs Loop Engineering"}],
                channel="IBM Technology",
                top_k=5,
            )
            pages = [m["page"] for m in matches]
            self.assertIn("IBM Technology", pages)
            self.assertIn("Loop Engineering", pages)
            self.assertIn("Prompt Engineering", pages)
            self.assertNotIn("Unrelated Lab", pages)
            self.assertNotIn("raw/ignored", pages)

    def test_curate_existing_frames_keep_and_drop(self):
        # Minimal valid JPEG bytes (SOI + SOF0 16x16 + EOI)
        minimal_jpg = (
            b"\xff\xd8\xff\xc0\x00\x11\x08\x00\x10\x00\x10\x03\x01\x11\x00"
        )
        with tempfile.TemporaryDirectory() as tmp:
            slug_dir = Path(tmp) / "raw" / "screenshots" / "demo-video"
            slug_dir.mkdir(parents=True)
            for idx, payload in [(1, b"A"), (2, b"BB"), (3, b"CCC"), (4, b"DDDD")]:
                (slug_dir / f"{idx:02d}.jpg").write_bytes(minimal_jpg + payload)

            report = capture_youtube_keyframes.curate_existing_frames(
                "demo-video", tmp, keep_csv="1,4,2"
            )
            self.assertEqual(report["kept_count"], 3)
            self.assertEqual(report["removed_count"], 1)
            self.assertEqual(report["removed_files"], ["03.jpg"])
            self.assertTrue((slug_dir / "01.jpg").read_bytes().endswith(b"A"))
            self.assertTrue((slug_dir / "02.jpg").read_bytes().endswith(b"DDDD"))
            self.assertTrue((slug_dir / "03.jpg").read_bytes().endswith(b"BB"))
            self.assertFalse((slug_dir / "04.jpg").exists())

            report2 = capture_youtube_keyframes.curate_existing_frames(
                "demo-video", tmp, drop_csv="2"
            )
            self.assertEqual(report2["kept_count"], 2)
            self.assertEqual(report2["removed_files"], ["02.jpg"])
            self.assertTrue((slug_dir / "01.jpg").read_bytes().endswith(b"A"))
            self.assertTrue((slug_dir / "02.jpg").read_bytes().endswith(b"BB"))
            self.assertFalse((slug_dir / "03.jpg").exists())


if __name__ == "__main__":
    unittest.main()
