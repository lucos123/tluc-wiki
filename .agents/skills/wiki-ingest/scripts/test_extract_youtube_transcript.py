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

    def test_suggest_keyframe_timestamps_long_chapter_and_visual_cues(self):
        chapters = [
            {"start_time": 0, "end_time": 180, "title": "Safety and Environment"},
        ]
        cues = [
            {"start": 10.0, "text": "Here is what a failure can look like this on prod."},
            {"start": 45.0, "text": "In a study published back in August we tested this."},
        ]
        suggested = extract_youtube_transcript.suggest_keyframe_timestamps(
            cues=cues, chapters=chapters, duration=180
        )
        reasons = [item["reason"] for item in suggested]
        self.assertIn("chapter_mid", reasons)
        self.assertIn("chapter", reasons)
        self.assertIn("visual_cue", reasons)
        mid_item = next(item for item in suggested if item["reason"] == "chapter_mid")
        self.assertEqual(mid_item["label"], "Safety and Environment (Mid)")
        self.assertEqual(mid_item["timestamp_sec"], 86)

        ts_arg = extract_youtube_transcript.build_timestamps_arg(suggested)
        self.assertIn("Safety-and-Environment-Mid", ts_arg)
        self.assertIn("=Safety-and-Environment", ts_arg)

    def test_select_best_probed_frame_avoids_textured_talking_head_over_white_slide(self):
        # Filters <70KB fade-in frames, picks high-detail IDE screen (>205KB)
        ide_candidates = [
            {"slot": 1, "bytes": 62000, "sec": 10.0},
            {"slot": 2, "bytes": 140000, "sec": 14.0},
            {"slot": 3, "bytes": 245000, "sec": 18.0},
        ]
        self.assertEqual(
            capture_youtube_keyframes._select_best_probed_frame(ide_candidates)["slot"],
            3,
        )

        # Preserves crisp white/Excalidraw slide at slot 2 (110KB-168KB) over adjacent 185KB webcam cut
        white_slide_vs_webcam = [
            {"slot": 1, "bytes": 185000, "sec": 276.0},
            {"slot": 2, "bytes": 125000, "sec": 280.0},
            {"slot": 3, "bytes": 135000, "sec": 284.0},
        ]
        self.assertEqual(
            capture_youtube_keyframes._select_best_probed_frame(white_slide_vs_webcam)["slot"],
            2,
        )

    def test_update_transcript_visual_frames_and_curate_sync(self):
        minimal_jpg = (
            b"\xff\xd8\xff\xc0\x00\x11\x08\x00\x10\x00\x10\x03\x01\x11\x00"
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            transcript_dir = root / "raw" / "video-transcripts"
            slug_dir = root / "raw" / "screenshots" / "demo-talk"
            transcript_dir.mkdir(parents=True)
            slug_dir.mkdir(parents=True)

            transcript_file = transcript_dir / "demo-talk.md"
            transcript_file.write_text(
                "# Demo Talk\n\n## Transcript\n\n**[00:01]** Hello world.\n",
                encoding="utf-8",
            )

            for idx, label_byte in [(1, b"1"), (2, b"2"), (3, b"3")]:
                (slug_dir / f"{idx:02d}.jpg").write_bytes(minimal_jpg + label_byte)

            initial_frames = [
                {"index": 1, "filename": "01.jpg", "mm_ss": "00:30", "label": "Intro", "status": "ok"},
                {"index": 2, "filename": "02.jpg", "mm_ss": "01:15", "label": "Webcam Cut", "status": "ok"},
                {"index": 3, "filename": "03.jpg", "mm_ss": "02:00", "label": "Architecture", "status": "ok"},
            ]
            rel_updated = capture_youtube_keyframes.update_transcript_visual_frames(
                "demo-talk", initial_frames, str(root), is_curate=False, start_index=1
            )
            self.assertEqual(rel_updated, "raw/video-transcripts/demo-talk.md")
            body = transcript_file.read_text(encoding="utf-8")
            self.assertIn("## Key Visual Frames", body)
            self.assertIn("![00:30 - Intro](../screenshots/demo-talk/01.jpg)", body)
            self.assertIn("![02:00 - Architecture](../screenshots/demo-talk/03.jpg)", body)
            self.assertLess(body.index("## Key Visual Frames"), body.index("## Transcript"))

            # Append supplemental frame via start_index=4 and verify preservation of 1..3
            (slug_dir / "04.jpg").write_bytes(minimal_jpg + b"4")
            capture_youtube_keyframes.update_transcript_visual_frames(
                "demo-talk",
                [{"index": 4, "filename": "04.jpg", "mm_ss": "03:00", "label": "Summary", "status": "ok"}],
                str(root),
                is_curate=False,
                start_index=4,
            )
            body2 = transcript_file.read_text(encoding="utf-8")
            self.assertIn("![00:30 - Intro](../screenshots/demo-talk/01.jpg)", body2)
            self.assertIn("![03:00 - Summary](../screenshots/demo-talk/04.jpg)", body2)

            # Curate with --keep "1,4,3" -> drops 2 and syncs descriptive alt text
            curated = capture_youtube_keyframes.curate_existing_frames(
                "demo-talk", str(root), keep_csv="1,4,3"
            )
            capture_youtube_keyframes.update_transcript_visual_frames(
                "demo-talk", curated["frames"], str(root), is_curate=True
            )
            body3 = transcript_file.read_text(encoding="utf-8")
            self.assertIn("![00:30 - Intro](../screenshots/demo-talk/01.jpg)", body3)
            self.assertIn("![03:00 - Summary](../screenshots/demo-talk/02.jpg)", body3)
            self.assertIn("![02:00 - Architecture](../screenshots/demo-talk/03.jpg)", body3)
            self.assertNotIn("Webcam Cut", body3)
            self.assertNotIn("04.jpg", body3)


if __name__ == "__main__":
    unittest.main()
