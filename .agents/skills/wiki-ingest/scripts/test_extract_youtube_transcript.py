"""
Unit Test Suite for extract_youtube_transcript.py
"""

import os
import sys
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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


if __name__ == "__main__":
    unittest.main()
