"""
Unit Test Suite for extract_youtube_transcript.py and capture_youtube_keyframes.py curation helpers
"""

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)
import capture_youtube_keyframes
import download_post_assets
import extract_youtube_transcript


def _load_lint_wiki():
    """Dynamically load lint_wiki.py from sibling wiki-lint skill scripts."""
    lint_path = os.path.abspath(
        os.path.join(SCRIPTS_DIR, "..", "..", "wiki-lint", "scripts", "lint_wiki.py")
    )
    spec = importlib.util.spec_from_file_location("lint_wiki", lint_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load lint_wiki module from {lint_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lint_wiki = _load_lint_wiki()


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

    def test_lint_wiki_ignores_nested_arrays_and_code_spans(self):
        sample_md = """---
title: "Sobel Filter Note"
date: 2026-11-19
tags:
  - concept
source: "[[Valid Source]]"
---

Inline nested array math `[[-1,0,1],[-2,0,2],[-1,0,1]]` and raw array [[-1,0,1],[0,1,0]] should be ignored.

```python
kernel = [[-1, 0, 1], [-2, 0, 2]]
comment = "ignore [[Fake Code Block Link]] here"
```

Meanwhile [[Real Concept|Alias]] and table-escaped [[Table Concept\\|Escaped Alias]] must still be extracted cleanly.
"""
        extracted = lint_wiki.extract_wiki_links(sample_md)
        self.assertIn("Valid Source", extracted)
        self.assertIn("Real Concept", extracted)
        self.assertIn("Table Concept", extracted)
        self.assertNotIn("Fake Code Block Link", extracted)
        self.assertFalse(any("-1,0,1" in item for item in extracted))

    def test_download_post_assets_scaffold_raw_article_immutability(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = [
                {
                    "index": 0,
                    "filename": "00.jpg",
                    "dimensions": "1536x2048",
                    "source_used": "url",
                },
                {
                    "index": 1,
                    "filename": "01.jpg",
                    "dimensions": "1536x2048",
                    "source_used": "url",
                },
            ]
            meta = {
                "raw_subdir": "ai-other",
                "title": "Sample Visual Guide",
                "source": "https://web.facebook.com/example/posts/123",
                "author": "Viet Nguyen AI",
                "published": "2026-11-19",
                "created": "2026-11-19",
                "text": "Line 1 of post.\nLine 2 of post.",
                "tags": ["clippings", "visual-guide"],
            }
            rel1, status1 = download_post_assets.scaffold_raw_article(
                "sample-visual-guide", files, tmp, meta
            )
            self.assertEqual(rel1, "raw/articles/ai-other/sample-visual-guide.md")
            self.assertEqual(status1, "created")

            raw_file = Path(tmp) / rel1
            content = raw_file.read_text(encoding="utf-8")
            self.assertIn('title: "Sample Visual Guide"', content)
            self.assertIn('> Line 1 of post.', content)
            self.assertIn('![Trang 1](../../screenshots/sample-visual-guide/00.jpg)', content)
            self.assertIn('![Trang 2](../../screenshots/sample-visual-guide/01.jpg)', content)
            self.assertNotIn('<!-- Điền nội dung', content)

            # Mutate file content manually and verify second call respects raw/ immutability
            raw_file.write_text("USER EDITED", encoding="utf-8")
            rel2, status2 = download_post_assets.scaffold_raw_article(
                "sample-visual-guide", files, tmp, meta
            )
            self.assertEqual(rel2, rel1)
            self.assertEqual(status2, "skipped_existing")
            self.assertEqual(raw_file.read_text(encoding="utf-8"), "USER EDITED")

            # Optional per-slide notes are rendered cleanly without placeholders
            meta_with_notes = dict(meta, raw_subdir="with-notes", notes=["Intro slide caption", "Second slide caption"])
            rel3, status3 = download_post_assets.scaffold_raw_article(
                "sample-with-notes", files, tmp, meta_with_notes
            )
            self.assertEqual(status3, "created")
            content3 = (Path(tmp) / rel3).read_text(encoding="utf-8")
            self.assertIn("Intro slide caption", content3)
            self.assertIn("Second slide caption", content3)
            self.assertNotIn('<!-- Điền nội dung', content3)

    def test_download_post_assets_manifest_urls_and_items_normalization(self):
        import argparse
        import json

        with tempfile.TemporaryDirectory() as tmp:
            m1_path = Path(tmp) / "m_urls.json"
            m1_path.write_text(
                json.dumps({
                    "slug": "flat-urls-deck",
                    "mode": "screenshots",
                    "urls": ["https://example.com/0.jpg", "https://example.com/1.jpg"],
                }),
                encoding="utf-8",
            )
            args1 = argparse.Namespace(
                manifest=str(m1_path), slug=None, mode=None, start_index=None, urls=None, fallbacks=None
            )
            slug1, mode1, start1, items1 = download_post_assets.load_manifest_or_args(args1)
            self.assertEqual(slug1, "flat-urls-deck")
            self.assertEqual(mode1, "screenshots")
            self.assertEqual(start1, 0)
            self.assertEqual(items1, [
                {"url": "https://example.com/0.jpg", "fallback": None},
                {"url": "https://example.com/1.jpg", "fallback": None},
            ])

            m2_path = Path(tmp) / "m_items.json"
            m2_path.write_text(
                json.dumps({
                    "slug": "mixed-items-deck",
                    "items": [
                        "https://example.com/str.jpg",
                        {"src": "https://example.com/obj.jpg", "note": "Slide 2 visual"},
                    ],
                }),
                encoding="utf-8",
            )
            args2 = argparse.Namespace(
                manifest=str(m2_path), slug=None, mode=None, start_index=None, urls=None, fallbacks=None
            )
            _, _, _, items2 = download_post_assets.load_manifest_or_args(args2)
            self.assertEqual(items2[0], {"url": "https://example.com/str.jpg"})
            self.assertEqual(items2[1], {
                "url": "https://example.com/obj.jpg",
                "fallback": None,
                "note": "Slide 2 visual",
            })


class TestMultiDomainV4Ingest(unittest.TestCase):
    def test_all_harvester_js_files_parse_and_are_async_callables(self):
        import json
        import shutil
        import subprocess

        harvesters_dir = Path(__file__).resolve().parent / "harvesters"
        expected = ["facebook.js", "instagram.js", "x_twitter.js", "linkedin.js", "web_article.js"]
        for fname in expected:
            self.assertTrue((harvesters_dir / fname).is_file(), f"Missing harvester JS: {fname}")

        node_bin = shutil.which("node")
        self.assertIsNotNone(node_bin, "Node.js is required to syntax-validate harvesters/*.js")
        js_check = (
            "const fs = require('fs'); const path = require('path'); "
            "const dir = process.argv[1]; "
            "for (const name of JSON.parse(process.argv[2])) { "
            "  const src = fs.readFileSync(path.join(dir, name), 'utf8').trim(); "
            "  const fn = new Function('return (' + src + ')')(); "
            "  if (typeof fn !== 'function') throw new Error(name + ' did not evaluate to function'); "
            "  if (fn.constructor.name !== 'AsyncFunction') throw new Error(name + ' is not async function'); "
            "}"
        )
        proc = subprocess.run(
            [node_bin, "-e", js_check, str(harvesters_dir), json.dumps(expected)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"JS validation failed: {proc.stderr or proc.stdout}")

    def test_web_article_and_x_harvester_real_js_behavior_in_node(self):
        import json
        import shutil
        import subprocess

        node_bin = shutil.which("node")
        self.assertIsNotNone(node_bin, "Node.js is required for JS behavior tests")
        harvesters_dir = Path(__file__).resolve().parent / "harvesters"

        # Lightweight DOM harness testing web_article.js (@graph JSON-LD, GFM table, code lang, comma-in-URL srcset)
        node_test = r"""
const fs = require('fs');
const path = require('path');
const dir = process.argv[1];

class FakeEl {
  constructor(tag, attrs = {}, text = '', children = []) {
    this.nodeType = 1;
    this.tagName = tag.toUpperCase();
    this.attrs = { ...attrs };
    this.className = attrs.class || '';
    const clsList = this.className.split(/\s+/).filter(Boolean);
    this.classList = { contains: (c) => clsList.includes(c) };
    this._text = text;
    this.children = [];
    this.parent = null;
    this.src = attrs.src || '';
    this.currentSrc = attrs.currentSrc || attrs.src || '';
    this.srcset = attrs.srcset || '';
    this.alt = attrs.alt || '';
    this.href = attrs.href || '';
    this.naturalWidth = attrs.naturalWidth || 0;
    this.naturalHeight = attrs.naturalHeight || 0;
    for (const c of children) this.appendChild(c);
  }
  appendChild(c) { c.parent = this; this.children.push(c); return c; }
  getAttribute(k) { return this.attrs[k] ?? null; }
  get textContent() { return this.children.length ? this._text + this.children.map(c => c.textContent).join('') : this._text; }
  get innerText() { return this.textContent; }
  getBoundingClientRect() { return { width: this.attrs._w ?? 800, height: this.attrs._h ?? 500, top: 20, bottom: 520, left: 0 }; }
  remove() { if (this.parent) this.parent.children = this.parent.children.filter(c => c !== this); }
  cloneNode() {
    const c = new FakeEl(this.tagName, { ...this.attrs }, this._text);
    c.children = this.children.map(ch => { const k = ch.cloneNode(true); k.parent = c; return k; });
    return c;
  }
  matchesOne(sel) {
    sel = sel.trim();
    if (sel.startsWith('.')) return this.classList.contains(sel.slice(1));
    if (sel === 'a.image-link') return this.tagName === 'A' && this.classList.contains('image-link');
    if (sel === 'article') return this.tagName === 'ARTICLE';
    if (sel === 'main article' || sel === '[role="main"] article') return this.tagName === 'ARTICLE' && !!this.closest('main');
    if (sel === 'main') return this.tagName === 'MAIN';
    if (sel === 'tr') return this.tagName === 'TR';
    if (sel === 'th') return this.tagName === 'TH';
    if (sel === 'td') return this.tagName === 'TD';
    if (sel === 'code') return this.tagName === 'CODE';
    if (sel === 'img') return this.tagName === 'IMG';
    if (sel === 'figure') return this.tagName === 'FIGURE';
    if (sel === 'figcaption') return this.tagName === 'FIGCAPTION';
    if (sel === 'nav') return this.tagName === 'NAV';
    if (sel === 'aside') return this.tagName === 'ASIDE';
    if (sel === 'footer') return this.tagName === 'FOOTER';
    if (sel === 'a[href^="http"]') return this.tagName === 'A' && this.href.startsWith('http');
    if (sel === 'script[type="application/ld+json"]') return this.tagName === 'SCRIPT' && this.attrs.type === 'application/ld+json';
    if (sel === 'link[rel="canonical"]') return this.tagName === 'LINK' && this.attrs.rel === 'canonical';
    if (sel === 'time[datetime]') return this.tagName === 'TIME' && !!this.attrs.datetime;
    if (sel.startsWith('meta[')) {
      const m = sel.match(/meta\[(property|name)="([^"]+)"\]/);
      return m ? (this.tagName === 'META' && this.attrs[m[1]] === m[2]) : false;
    }
    const dm = sel.match(/^\[data-testid=['"]([^'"]+)['"]\]$/);
    if (dm) return this.attrs['data-testid'] === dm[1];
    return false;
  }
  matches(selectorList) {
    return selectorList.split(',').some(s => this.matchesOne(s));
  }
  closest(selectorList) {
    let cur = this;
    while (cur) { if (cur.matches(selectorList)) return cur; cur = cur.parent; }
    return null;
  }
  querySelectorAll(selectorList) {
    const out = [];
    const walk = (n) => {
      for (const ch of n.children) {
        if (ch.matches(selectorList)) out.push(ch);
        walk(ch);
      }
    };
    walk(this);
    return out;
  }
  querySelector(selectorList) { return this.querySelectorAll(selectorList)[0] || null; }
}

(async () => {
  const ldScript = new FakeEl('script', { type: 'application/ld+json' }, JSON.stringify({
    '@context': 'https://schema.org',
    '@graph': [
      { '@type': 'WebSite', name: 'TestBlog' },
      { '@type': 'TechArticle', headline: 'Scaling Agents', datePublished: '2026-10-05T12:00:00Z', author: { name: 'Jane Doe' } }
    ]
  }));
  const table = new FakeEl('table', {}, '', [
    new FakeEl('tr', {}, '', [new FakeEl('th', {}, 'Model'), new FakeEl('th', {}, 'Score')]),
    new FakeEl('tr', {}, '', [new FakeEl('td', {}, 'Alpha'), new FakeEl('td', {}, '94.2')]),
  ]);
  const pre = new FakeEl('pre', {}, '', [new FakeEl('code', { class: 'language-python' }, 'print("hi")')]);
  const fig = new FakeEl('figure', {}, '', [
    new FakeEl('a', { class: 'image-link', href: 'https://substackcdn.com/image/fetch/full.png' }, '', [
      new FakeEl('img', {
        src: 'https://substackcdn.com/image/fetch/w_424,c_limit,f_auto/https%3A%2F%2Fimg.png',
        srcset: 'https://substackcdn.com/image/fetch/w_424,c_limit,f_auto/https%3A%2F%2Fimg.png 424w, https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto/https%3A%2F%2Fimg.png 1456w',
        naturalWidth: 1456, naturalHeight: 900, _w: 700, _h: 450,
      }),
    ]),
    new FakeEl('figcaption', {}, 'Agent Loop Architecture')
  ]);
  const article = new FakeEl('article', {}, '', [
    new FakeEl('nav', {}, 'Home About Pricing'),
    new FakeEl('div', { class: 'subscription-widget-wrap' }, '', [
      new FakeEl('p', {}, 'Subscribe now box'),
      new FakeEl('a', { href: 'https://substack.com/subscribe' }, 'Sub'),
    ]),
    new FakeEl('h1', {}, 'Scaling Agents'),
    new FakeEl('p', {}, 'A comprehensive architectural deep dive into autonomous agent loops and benchmark evaluations across production workloads. '.repeat(3)),
    new FakeEl('p', {}, 'Jam with AI is a reader-supported publication. To receive new posts and support my work, consider becoming a free or paid subscriber.'),
    new FakeEl('p', {}, 'Read the companion paper: ', [new FakeEl('a', { href: 'https://arxiv.org/abs/2401.00001' }, 'arXiv')]),
    new FakeEl('a', { href: 'https://substack.com/profile/123-user' }, 'Reader Profile'),
    new FakeEl('a', { href: 'https://substack.com/@shantanuladhwe' }, 'Co-Author'),
    new FakeEl('a', { href: 'https://substack.com/sign-in?redirect=%2Fp%2Fscaling-agents' }, 'Sign in'),
    new FakeEl('h2', {}, 'This post is for paid subscribers'),
    new FakeEl('div', { class: 'paywall', 'data-testid': 'paywall' }, '', [
      new FakeEl('p', {}, 'Upgrade to paid to continue reading.'),
      new FakeEl('a', { href: 'https://jamwithai.substack.com/subscribe?simple=true&utm_source=paywall' }, 'Upgrade'),
    ]),
    table,
    pre,
    fig,
  ]);
  const doc = new FakeEl('html', {}, '', [ldScript, new FakeEl('main', {}, '', [article])]);
  doc.body = doc;
  doc.title = 'Fallback Title';

  global.document = doc;
  global.location = new URL('https://newsletter.example.com/p/scaling-agents');
  global.window = { innerHeight: 900, scrollY: 0, scrollBy() {}, scrollTo() {} };

  const webFn = new Function('return (' + fs.readFileSync(path.join(dir, 'web_article.js'), 'utf8').trim() + ')')();
  const res = await webFn();
  console.log(JSON.stringify(res));
})();
"""
        proc = subprocess.run(
            [node_bin, "-e", node_test, str(harvesters_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"Node web_article behavior test failed: {proc.stderr or proc.stdout}")
        res = json.loads(proc.stdout)
        self.assertEqual(res["title"], "Scaling Agents")
        self.assertEqual(res["author"], "Jane Doe")
        self.assertEqual(res["published"], "2026-10-05T12:00:00Z")
        self.assertTrue(res["paywalled"])
        self.assertIn("| Model | Score |", res["text"])
        self.assertIn("| Alpha | 94.2 |", res["text"])
        self.assertIn("```python\nprint(\"hi\")\n```", res["text"])
        self.assertNotIn("Home About Pricing", res["text"])
        self.assertNotIn("Subscribe now box", res["text"])
        self.assertNotIn("reader-supported publication", res["text"])
        self.assertNotIn("paid subscribers", res["text"])
        self.assertNotIn("Upgrade to paid", res["text"])
        self.assertIn("https://arxiv.org/abs/2401.00001", res["external_links"])
        self.assertFalse(any("substackcdn.com/image/" in u for u in res["external_links"]))
        self.assertFalse(any("substack.com/profile/" in u for u in res["external_links"]))
        self.assertFalse(any("@shantanuladhwe" in u for u in res["external_links"]))
        self.assertFalse(any("utm_source=paywall" in u for u in res["external_links"]))
        self.assertFalse(any("substack.com/sign-in" in u for u in res["external_links"]))
        self.assertFalse(any("substack.com/subscribe" in u for u in res["external_links"]))
        self.assertEqual(res["total_slides"], 1)
        self.assertEqual(
            res["slides"][0]["src"],
            "https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto/https%3A%2F%2Fimg.png",
        )
        self.assertEqual(res["slides"][0]["note"], "Agent Loop Architecture")

    def test_get_harvester_platform_detection_guards_and_fingerprints(self):
        import get_harvester

        self.assertEqual(get_harvester.detect_platform("https://web.facebook.com/vietnh1009/posts/pfbid02tqE2H"), "facebook")
        self.assertEqual(get_harvester.detect_platform("https://fb.watch/abc123/"), "facebook")
        self.assertEqual(
            get_harvester.detect_platform("https://www.instagram.com/techyy_bandaa/p/DdQPCJoEuaU/?img_index=1"),
            "instagram",
        )
        self.assertEqual(get_harvester.detect_platform("https://instagr.am/reels/DdQPCJoEuaU/"), "instagram")
        self.assertEqual(get_harvester.detect_platform("https://x.com/karpathy/status/1890000000000000000"), "x_twitter")
        self.assertEqual(
            get_harvester.detect_platform("https://www.linkedin.com/posts/alex_ai-activity-7123456789012345678-AbCd"),
            "linkedin",
        )
        self.assertEqual(
            get_harvester.detect_platform("https://www.anthropic.com/engineering/building-effective-agents"),
            "web_article",
        )
        # Guard YouTube & PDF URLs from falling back to web_article
        self.assertEqual(get_harvester.detect_platform("https://www.youtube.com/watch?v=dQw4w9WgXcQ"), "youtube")
        self.assertEqual(get_harvester.detect_platform("https://youtu.be/dQw4w9WgXcQ"), "youtube")
        self.assertEqual(get_harvester.detect_platform("https://arxiv.org/pdf/2401.12345"), "pdf")
        self.assertEqual(get_harvester.detect_platform("https://example.com/whitepaper.pdf"), "pdf")

        ig_tokens = get_harvester.extract_url_fingerprints("https://instagr.am/reels/DdQPCJoEuaU/?img_index=1")
        self.assertIn("DdQPCJoEuaU", ig_tokens)

        fb_tokens = get_harvester.extract_url_fingerprints("https://www.facebook.com/share/p/1AbCdEfGhI/")
        self.assertIn("1AbCdEfGhI", fb_tokens)

        x_tokens = get_harvester.extract_url_fingerprints("https://x.com/user/article/1890000000000000000")
        self.assertIn("1890000000000000000", x_tokens)

        li_tokens = get_harvester.extract_url_fingerprints("https://www.linkedin.com/feed/update/urn:li:ugcPost:7123456789012345678/")
        self.assertIn("7123456789012345678", li_tokens)

        web_tokens = get_harvester.extract_url_fingerprints("https://www.anthropic.com/engineering/building-effective-agents/")
        self.assertIn("anthropic.com/engineering/building-effective-agents", web_tokens)

    def test_get_harvester_duplicate_detection_and_compact_cli_stdout(self):
        import json
        import subprocess
        import get_harvester

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text("# Index\n", encoding="utf-8")
            (root / "raw" / "articles" / "ai").mkdir(parents=True)
            (root / "wiki" / "sources").mkdir(parents=True)
            (root / "raw" / "articles" / "ai" / "transformers.md").write_text(
                '---\ntitle: "Transformers"\nsource: "https://www.instagram.com/techyy_bandaa/p/DdQPCJoEuaU/"\n---\n',
                encoding="utf-8",
            )
            (root / "wiki" / "sources" / "ref.md").write_text(
                '---\ntitle: "Ref"\noriginal_source: "https://www.instagram.com/p/DdQPCJoEuaU/"\n---\n',
                encoding="utf-8",
            )
            # Test www vs non-www match on web articles & ensure prefix slug does NOT false-match longer slug
            (root / "raw" / "articles" / "ai" / "agents.md").write_text(
                '---\ntitle: "Agents"\nsource: "https://anthropic.com/engineering/building-effective-agents"\n---\n',
                encoding="utf-8",
            )
            (root / "raw" / "articles" / "ai" / "agents-v2.md").write_text(
                '---\ntitle: "Agents v2"\nsource: "https://anthropic.com/engineering/building-effective-agents-part-2"\n---\n',
                encoding="utf-8",
            )
            (root / "raw" / "video-transcripts").mkdir(parents=True)
            (root / "raw" / "video-transcripts" / "other-video.md").write_text(
                '---\ntitle: "Other"\nurl: "https://www.youtube.com/watch?v=OTHER123456"\n---\n',
                encoding="utf-8",
            )

            matches = get_harvester.find_duplicate_ingestions(
                "https://www.instagram.com/techyy_bandaa/p/DdQPCJoEuaU/?img_index=1",
                str(root),
            )
            roles = {m["file"]: m["match_role"] for m in matches}
            self.assertEqual(roles.get("raw/articles/ai/transformers.md"), "primary_source")
            self.assertEqual(roles.get("wiki/sources/ref.md"), "original_source")

            web_matches = get_harvester.find_duplicate_ingestions(
                "https://www.anthropic.com/engineering/building-effective-agents/",
                str(root),
            )
            self.assertEqual(len(web_matches), 1)
            self.assertEqual(web_matches[0]["file"], "raw/articles/ai/agents.md")
            self.assertEqual(web_matches[0]["match_role"], "primary_source")

            # Generic query endpoint (/watch) MUST NOT false-match other YouTube videos
            yt_unseen = get_harvester.find_duplicate_ingestions(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                str(root),
            )
            self.assertEqual(yt_unseen, [])
            yt_seen = get_harvester.find_duplicate_ingestions(
                "https://youtu.be/OTHER123456",
                str(root),
            )
            self.assertEqual(len(yt_seen), 1)
            self.assertEqual(yt_seen[0]["file"], "raw/video-transcripts/other-video.md")

            # CLI verification: default output omits duplicate raw harvester_js, and redirects YouTube
            script_path = Path(__file__).resolve().parent / "get_harvester.py"
            p_ig = subprocess.run(
                [sys.executable, str(script_path), "--url", "https://www.instagram.com/techyy_bandaa/p/DdQPCJoEuaU/", "--project-root", str(root)],
                capture_output=True, text=True, check=True,
            )
            ig_out = json.loads(p_ig.stdout)
            self.assertTrue(ig_out["already_ingested"])
            self.assertTrue(ig_out["has_original_source_overlap"])
            self.assertIn("browser_prompt", ig_out)
            self.assertNotIn("harvester_js", ig_out)

            p_yt = subprocess.run(
                [sys.executable, str(script_path), "--url", "https://youtu.be/dQw4w9WgXcQ", "--project-root", str(root)],
                capture_output=True, text=True, check=True,
            )
            yt_out = json.loads(p_yt.stdout)
            self.assertEqual(yt_out["status"], "redirect_video")
            self.assertEqual(yt_out["platform"], "youtube")
            self.assertNotIn("browser_prompt", yt_out)

    def test_download_post_assets_parse_fenced_harvest_auto_mode_and_zero_relay_cli(self):
        import argparse
        import json
        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            tdir = Path(tmp)
            (tdir / "index.md").write_text("# Index\n", encoding="utf-8")
            fenced_2 = tdir / "ig_output.txt"
            payload_2 = {
                "platform": "instagram",
                "status": "ok",
                "url": "https://www.instagram.com/techyy_bandaa/p/DdQPCJoEuaU/?img_index=1",
                "canonical_url": "https://www.instagram.com/techyy_bandaa/p/DdQPCJoEuaU/",
                "author": "Techie",
                "published": "2025-08-12T08:00:00.000Z",
                "text": "Comment PDF",
                "slides": [
                    {"index": 1, "src": "https://instagram.fsgn8-4.fna.fbcdn.net/1.webp"},
                    {"index": 2, "src": "https://instagram.fsgn8-4.fna.fbcdn.net/2.webp"},
                ],
            }
            fenced_2.write_text(
                f"## Script output\n```json\n{json.dumps(payload_2)}\n```\nPage navigated to https://www.instagram.com/.\n",
                encoding="utf-8",
            )

            parsed, meta = download_post_assets.parse_harvest_file(str(fenced_2))
            self.assertEqual(parsed["platform"], "instagram")
            self.assertEqual(meta["author"], "Techie")
            self.assertEqual(meta["url"], "https://www.instagram.com/techyy_bandaa/p/DdQPCJoEuaU/")

            args_auto_assets = argparse.Namespace(
                from_harvest_file=str(fenced_2), manifest=None, slug="two-diagram-post",
                mode=None, start_index=None, urls=None, fallbacks=None, probe_cover=None,
            )
            slug_a, mode_a, start_a, items_a = download_post_assets.load_manifest_or_args(args_auto_assets)
            self.assertEqual((slug_a, mode_a, start_a, len(items_a)), ("two-diagram-post", "assets", 1, 2))

            fenced_5 = tdir / "deck_output.txt"
            fenced_5.write_text(
                json.dumps({"platform": "instagram", "slides": [{"src": f"https://example.com/{i}.webp"} for i in range(5)]}),
                encoding="utf-8",
            )
            args_auto_shots = argparse.Namespace(
                from_harvest_file=str(fenced_5), manifest=None, slug="five-slide-deck",
                mode="auto", start_index=None, urls=None, fallbacks=None, probe_cover=None,
            )
            slug_s, mode_s, start_s, items_s = download_post_assets.load_manifest_or_args(args_auto_shots)
            self.assertEqual((slug_s, mode_s, start_s, len(items_s)), ("five-slide-deck", "screenshots", 0, 5))

            # End-to-end CLI test on a 0-image long Web Article: stdout truncates preview, raw file gets full body & clean Markdown
            long_body = "# Architecture\n\n| Metric | Value |\n| --- | --- |\n| Latency | 12ms |\n\n" + ("Detailed paragraph content. " * 120)
            long_article = tdir / "web_output.txt"
            long_article.write_text(
                "```json\n" + json.dumps({
                    "platform": "web_article",
                    "status": "ok",
                    "title": "Deep Architecture Guide",
                    "canonical_url": "https://blog.example.com/deep-arch",
                    "author": "Jane Doe",
                    "published": "2026-10-05T14:30:00Z",
                    "text": long_body,
                    "external_links": ["https://arxiv.org/abs/2401.00001"],
                    "slides": [],
                }) + "\n```\n",
                encoding="utf-8",
            )
            script_path = Path(__file__).resolve().parent / "download_post_assets.py"
            proc = subprocess.run(
                [
                    sys.executable, str(script_path),
                    "--slug", "deep-architecture-guide",
                    "--mode", "auto",
                    "--from-harvest-file", str(long_article),
                    "--init-raw", "--raw-subdir", "ai-other",
                    "--project-root", str(tdir),
                ],
                capture_output=True, text=True, check=True,
            )
            cli_rep = json.loads(proc.stdout)
            self.assertEqual(cli_rep["status"], "ok")
            self.assertEqual(cli_rep["total_requested"], 0)
            self.assertTrue(cli_rep["harvest_meta"]["text_truncated"])
            self.assertIn("text_preview", cli_rep["harvest_meta"])
            self.assertNotIn("text", cli_rep["harvest_meta"])

            raw_md = (tdir / "raw" / "articles" / "ai-other" / "deep-architecture-guide.md").read_text(encoding="utf-8")
            self.assertIn("published: 2026-10-05", raw_md)
            self.assertIn("## Nội Dung Nguyên Văn Bài Viết", raw_md)
            self.assertIn("| Metric | Value |", raw_md)
            self.assertNotIn("> | Metric | Value |", raw_md)
            self.assertNotIn("raw/screenshots/deep-architecture-guide", raw_md)
            self.assertNotIn("Thư Viện 0 Trang", raw_md)
            self.assertIn("https://arxiv.org/abs/2401.00001", raw_md)
            self.assertGreater(len(raw_md), len(long_body))

    def test_download_post_assets_403_referer_retry_assets_scaffold_and_probe_cover(self):
        import urllib.error
        from unittest import mock

        self.assertEqual(
            download_post_assets._infer_referer("https://instagram.fsgn8-4.fna.fbcdn.net/v/t51.82787-15/1.webp"),
            "https://www.instagram.com/",
        )
        self.assertEqual(
            download_post_assets._infer_referer("https://scontent.fsgn5-2.fna.fbcdn.net/v/t39/2.jpg"),
            "https://www.facebook.com/",
        )
        self.assertEqual(
            download_post_assets._infer_referer("https://pbs.twimg.com/media/AbCdEf?format=jpg&name=orig"),
            "https://x.com/",
        )
        self.assertEqual(
            download_post_assets._infer_referer("https://media.licdn.com/dms/image/D4D22AQF/0"),
            "https://www.linkedin.com/",
        )

        # Verify fetch_url_bytes sends non-AVIF Accept header and retries 403 with Instagram Referer
        seen_headers = []

        class _FakeResp:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self): return b"OK_BYTES"

        def _fake_urlopen(req, timeout=20):
            hdrs = {k.lower(): v for k, v in req.header_items()}
            seen_headers.append(hdrs)
            if len(seen_headers) == 1:
                raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, None)
            return _FakeResp()

        with mock.patch("urllib.request.urlopen", side_effect=_fake_urlopen):
            data, err = download_post_assets.fetch_url_bytes(
                "https://instagram.fsgn8-4.fna.fbcdn.net/v/t51/img.webp", retries=0
            )
        self.assertEqual(data, b"OK_BYTES")
        self.assertIsNone(err)
        self.assertEqual(len(seen_headers), 2)
        self.assertNotIn("avif", seen_headers[0]["accept"].lower())
        self.assertNotIn("referer", seen_headers[0])
        self.assertEqual(seen_headers[1]["referer"], "https://www.instagram.com/")

        # Verify scaffold_raw_article assets mode + colon-containing published quoting + explicit probe_cover
        minimal_png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x03"
            b"\x08\x02\x00\x00\x00\x00\x00\x00\x00" + (b"\x00" * 32)
        )
        with tempfile.TemporaryDirectory() as tmp:
            tdir = Path(tmp)
            src_img = tdir / "src.png"
            src_img.write_bytes(minimal_png)
            probe_dest = tdir / "scratch" / "cover.png"

            res = download_post_assets.process_item({
                "index": 0,
                "url": None,
                "fallback": str(src_img),
                "mode": "screenshots",
                "slug": "probe-cover",
                "out_dir": str(probe_dest.parent),
                "explicit_dest_path": str(probe_dest),
                "project_root": str(tdir),
                "min_bytes": 10,
            })
            self.assertEqual(res["source_used"], "fallback")
            self.assertEqual(res["filename"], "cover.png")
            self.assertTrue(probe_dest.is_file())
            self.assertFalse((tdir / "raw").exists())

            rel_a, st_a = download_post_assets.scaffold_raw_article(
                "two-diagrams",
                [{
                    "index": 1,
                    "filename": "two-diagrams-01.png",
                    "rel_path": "raw/assets/two-diagrams-01.png",
                    "md_embed": "![Asset 01](../../assets/two-diagrams-01.png)",
                    "dimensions": "1200x800",
                    "source_used": "url",
                }],
                str(tdir),
                {
                    "platform": "facebook",
                    "raw_subdir": "ai-other",
                    "title": "Two Diagrams",
                    "published": "14 tháng 11 lúc 18:30",
                    "text": "Short caption",
                },
            )
            self.assertEqual(st_a, "created")
            assets_md = (tdir / rel_a).read_text(encoding="utf-8")
            self.assertIn('published: "14 tháng 11 lúc 18:30"', assets_md)
            self.assertIn("`raw/assets/`", assets_md)
            self.assertNotIn("raw/screenshots/two-diagrams", assets_md)

    def test_register_ingest_suggest_links_supports_vietnamese_unicode(self):
        import json
        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text(
                "# Index\n\n## Concepts\n- [[Quy Trình Tư Vấn Nha Khoa 3C]]: Quy trình tư vấn khách hàng nha khoa.\n",
                encoding="utf-8",
            )
            script_path = Path(__file__).resolve().parent / "register_ingest.py"
            proc = subprocess.run(
                [sys.executable, str(script_path), "--project-root", str(root), "--suggest-links", "tư vấn nha khoa"],
                capture_output=True, text=True, check=True,
            )
            out = json.loads(proc.stdout)
            self.assertEqual(len(out["matches"]), 1)
            self.assertEqual(out["matches"][0]["page"], "Quy Trình Tư Vấn Nha Khoa 3C")

    def test_compute_probe_window_clamps_inside_short_chapter_boundary(self):
        chapters = [
            {"start_time": 962, "end_time": 980, "title": "Metrics, Tracing, and AI Evaluations"},
            {"start_time": 100, "end_time": 108, "title": "Very Short Chapter"},
        ]
        # Chapter 12 (18s span): target 975 with offset 4.0 must not exceed 978.0 (chapter_end - 2)
        ch_start, ch_end = capture_youtube_keyframes._find_containing_chapter(975.0, chapters, duration=1031.0)
        self.assertEqual((ch_start, ch_end), (962.0, 980.0))
        start_sec, eff = capture_youtube_keyframes._compute_probe_window(975.0, 4.0, ch_start, ch_end, 1031.0)
        self.assertGreaterEqual(start_sec, 962.0)
        self.assertLessEqual(start_sec + 2.0 * eff, 978.0)

        # Very short 8s chapter (100..108): eff compresses cleanly so all 3 frames stay inside [100, 106]
        ch2_start, ch2_end = capture_youtube_keyframes._find_containing_chapter(105.0, chapters, duration=200.0)
        self.assertEqual((ch2_start, ch2_end), (100.0, 108.0))
        s2, eff2 = capture_youtube_keyframes._compute_probe_window(105.0, 4.0, ch2_start, ch2_end, 200.0)
        self.assertGreaterEqual(s2, 100.0)
        self.assertLessEqual(s2 + 2.0 * eff2, 106.0)
        self.assertLess(eff2, 4.0)

    def test_build_timestamps_arg_no_duplicate_chapter_mid(self):
        chapters = [{"start_time": 0, "end_time": 180, "title": "Long Section"}]
        cues = [{"start": 40.0, "text": "Here you can see the architecture diagram."}]
        suggested = extract_youtube_transcript.suggest_keyframe_timestamps(cues=cues, chapters=chapters, duration=180)
        ts_arg = extract_youtube_transcript.build_timestamps_arg(suggested, max_items=12)
        tokens = ts_arg.split(",")
        self.assertEqual(len(tokens), len(set(tokens)), f"Duplicate timestamp token generated: {tokens}")
        self.assertEqual(len(tokens), 3)

    def test_scaffold_raw_article_web_article_dedups_h1_and_formats_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            rel_w, status_w = download_post_assets.scaffold_raw_article(
                "system-design-guide",
                [{
                    "index": 0,
                    "filename": "00.png",
                    "rel_path": "raw/screenshots/system-design-guide/00.png",
                    "dimensions": "1440x606",
                    "source_used": "url",
                }],
                tmp,
                {
                    "platform": "web_article",
                    "raw_subdir": "ai-other",
                    "title": "System Design for AI Engineers: 7 patterns",
                    "source": "https://jamwithai.substack.com/p/system-design-for-ai-engineers-7",
                    "author": "Jam With AI",
                    "published": "2026-04-09T20:33:54+07:00",
                    "text": "# System Design for AI Engineers: 7 patterns\n\n## 1. API Gateway\n\nBody paragraph.",
                },
            )
            self.assertEqual(status_w, "created")
            content = (Path(tmp) / rel_w).read_text(encoding="utf-8")
            self.assertIn('  - "web-article"', content)
            self.assertNotIn('  - "visual-guide"', content)
            self.assertIn("Captured web article and diagrams for", content)
            self.assertIn("- **Thời gian đăng:** 2026-04-09", content)
            self.assertEqual(content.count("# System Design for AI Engineers: 7 patterns"), 1)
            self.assertIn("## Hình Ảnh & Sơ Đồ Đính Kèm (1 ảnh)", content)
            self.assertIn("### Hình 1 / 1 *(1440x606)*", content)

    def test_download_post_assets_multi_author_and_paywall_metadata(self):
        import argparse
        import json

        self.assertEqual(
            download_post_assets._normalize_authors("Shantanu Ladhwe, Shirin Khosravi Jam"),
            ["Shantanu Ladhwe", "Shirin Khosravi Jam"],
        )
        self.assertEqual(
            download_post_assets._normalize_authors("Acme, Inc."),
            ["Acme, Inc."],
        )
        self.assertEqual(
            download_post_assets._normalize_authors(["[[Alice]]", "Bob", "Alice"]),
            ["Alice", "Bob"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            harvest_path = Path(tmp) / "paywalled_harvest.txt"
            harvest_path.write_text(
                json.dumps({
                    "platform": "web_article",
                    "status": "ok",
                    "paywalled": True,
                    "title": "Paywalled Article",
                    "canonical_url": "https://jamwithai.substack.com/p/demo",
                    "author": "Shantanu Ladhwe, Shirin Khosravi Jam",
                    "published": "2026-07-01T16:41:23+07:00",
                    "text": "# Paywalled Article\n\nSection 1 content.",
                    "slides": [],
                }),
                encoding="utf-8",
            )
            _, hmeta = download_post_assets.parse_harvest_file(str(harvest_path))
            self.assertTrue(hmeta.get("paywalled"))

            args = argparse.Namespace(
                init_raw=True,
                manifest=None,
                raw_subdir="ai-other",
                raw_title=None,
                raw_source=None,
                raw_original_source=None,
                raw_author=None,
                raw_published=None,
                raw_created="2026-11-22",
                raw_description=None,
                raw_text=None,
            )
            rmeta = download_post_assets.extract_raw_meta(args, harvest_meta=hmeta)
            self.assertTrue(rmeta["paywalled"])

            rel_p, st_p = download_post_assets.scaffold_raw_article("paywalled-demo", [], tmp, rmeta)
            self.assertEqual(st_p, "created")
            content = (Path(tmp) / rel_p).read_text(encoding="utf-8")
            self.assertIn('  - "Shantanu Ladhwe"', content)
            self.assertIn('  - "Shirin Khosravi Jam"', content)
            self.assertNotIn("[[Shantanu Ladhwe]]", content)
            self.assertIn("paywalled: true", content)
            self.assertIn("- **Trạng thái paywall:**", content)

    def test_download_post_assets_local_files_auto_routing_dedup_and_scaffold(self):
        import argparse
        import json
        import subprocess

        minimal_png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x04\x00\x00\x00\x04"
            b"\x08\x02\x00\x00\x00\x00\x00\x00\x00" + (b"\x00" * 32)
        )
        with tempfile.TemporaryDirectory() as tmp:
            tdir = Path(tmp)
            (tdir / "index.md").write_text("# Index\n", encoding="utf-8")
            upload_dir = tdir / "uploads"
            upload_dir.mkdir(parents=True)
            img1 = upload_dir / "roadmap.png"
            img1.write_bytes(minimal_png)

            script_path = Path(__file__).resolve().parent / "download_post_assets.py"
            proc1 = subprocess.run(
                [
                    sys.executable, str(script_path),
                    "--slug", "ai-agents-roadmap",
                    "--mode", "auto",
                    "--local-files", str(img1),
                    "--init-raw",
                    "--raw-subdir", "ai-other",
                    "--raw-title", "AI Agents Roadmap Blueprint",
                    "--project-root", str(tdir),
                ],
                capture_output=True, text=True, check=True,
            )
            rep1 = json.loads(proc1.stdout)
            self.assertEqual(rep1["status"], "ok")
            self.assertEqual(rep1["mode"], "assets")
            self.assertEqual(rep1["files"][0]["source_used"], "local")
            self.assertEqual(rep1["files"][0]["rel_path"], "raw/assets/ai-agents-roadmap-01.png")
            self.assertEqual(len(rep1["files"][0]["sha256"]), 12)
            self.assertNotIn("duplicate_existing_path", rep1["files"][0])
            self.assertTrue((tdir / "raw" / "assets" / "ai-agents-roadmap-01.png").is_file())

            raw_md = (tdir / rep1["raw_scaffold_path"]).read_text(encoding="utf-8")
            self.assertIn('  - "infographic"', raw_md)
            self.assertIn("Collected visual reference and infographic notes for AI Agents Roadmap Blueprint.", raw_md)
            self.assertIn("- **Nguồn lưu trữ:**", raw_md)

            # Second archival with byte-identical file under a different slug reports duplicate_existing_path
            proc2 = subprocess.run(
                [
                    sys.executable, str(script_path),
                    "--slug", "ai-agents-roadmap-copy",
                    "--mode", "auto",
                    "--local-files", str(img1),
                    "--project-root", str(tdir),
                ],
                capture_output=True, text=True, check=True,
            )
            rep2 = json.loads(proc2.stdout)
            self.assertEqual(rep2["status"], "ok")
            self.assertEqual(rep2["files"][0]["duplicate_existing_path"], "raw/assets/ai-agents-roadmap-01.png")

            # 4 local files auto-route to screenshots mode starting at 0
            four_files = [str(img1)] * 4
            args_4 = argparse.Namespace(
                from_harvest_file=None, manifest=None, slug="four-local-deck",
                mode=None, start_index=None, urls=None, fallbacks=None,
                local_files=four_files, probe_cover=None,
            )
            slug4, mode4, start4, items4 = download_post_assets.load_manifest_or_args(args_4)
            self.assertEqual((slug4, mode4, start4, len(items4)), ("four-local-deck", "screenshots", 0, 4))

    def test_find_related_wiki_pages_supports_standard_markdown_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text(
                "\n".join([
                    "# Index",
                    "",
                    "## Entities",
                    "- [IBM Technology](wiki/entities/IBM%20Technology.md): Official IBM technical education channel.",
                    "- [Unrelated Lab](wiki/entities/Unrelated%20Lab.md): Something else.",
                    "",
                    "## Concepts",
                    "- [Loop Engineering](wiki/concepts/Loop%20Engineering.md): Agent loop patterns and safeguards.",
                    "- [raw ignored](raw/ignored.md): Raw should not appear.",
                    "",
                ]),
                encoding="utf-8",
            )
            matches = extract_youtube_transcript.find_related_wiki_pages(
                root,
                title="What Is Loop Engineering",
                chapters=[{"title": "Loop Engineering Deep Dive"}],
                channel="IBM Technology",
                top_k=5,
            )
            by_page = {m["page"]: m for m in matches}
            self.assertIn("IBM Technology", by_page)
            self.assertEqual(by_page["IBM Technology"]["path"], "wiki/entities/IBM Technology.md")
            self.assertIn("Loop Engineering", by_page)
            self.assertNotIn("Unrelated Lab", by_page)
            self.assertNotIn("raw ignored", by_page)

    def test_register_ingest_standard_markdown_links_and_duplicate_stems(self):
        import json
        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for sub in ("wiki/concepts", "wiki/sources", "wiki/entities", "raw"):
                (root / sub).mkdir(parents=True, exist_ok=True)
            (root / "raw" / "h.md").write_text("# Raw\n", encoding="utf-8")
            (root / "wiki" / "log.md").write_text("# Log\n", encoding="utf-8")
            (root / "index.md").write_text(
                "# Wiki Index\n\n## Entities\n\n## Concepts\n\n## Sources\n",
                encoding="utf-8",
            )
            (root / "wiki" / "concepts" / "Harness Engineering.md").write_text(
                "---\ntitle: Harness Concept\ndate: 2026-11-22\ntags:\n  - concept\n---\n# Harness\n",
                encoding="utf-8",
            )
            (root / "wiki" / "concepts" / "Amazon Web Services (AWS).md").write_text(
                "---\ntitle: AWS\ndate: 2026-11-22\ntags:\n  - concept\n---\n# AWS\n",
                encoding="utf-8",
            )
            (root / "wiki" / "sources" / "Harness Engineering.md").write_text(
                '---\ntitle: Harness Source\ndate: 2026-11-22\ntags:\n  - source\nsource: "raw/h.md"\n---\n# Src\n',
                encoding="utf-8",
            )

            script_path = Path(__file__).resolve().parent / "register_ingest.py"
            proc = subprocess.run(
                [
                    sys.executable, str(script_path),
                    "--project-root", str(root),
                    "--date", "2026-11-22",
                    "--log-type", "ingest",
                    "--source-title", "Harness Engineering",
                    "--entry", "Concepts|Harness Engineering|Concept definition.",
                    "--entry", "Concepts|Amazon Web Services (AWS)|Cloud architecture.",
                    "--entry", "Sources|Harness Engineering|Original essay summary.",
                ],
                capture_output=True, text=True, check=True,
            )
            out = json.loads(proc.stdout)
            self.assertEqual(out["status"], "ok")
            self.assertEqual(out["stats"]["total_broken_links"], 0)
            self.assertEqual(out["stats"]["total_legacy_wikilinks"], 0)
            self.assertEqual(out["stats"]["index_coverage_pct"], 100.0)

            idx_text = (root / "index.md").read_text(encoding="utf-8")
            self.assertIn(
                "- [Amazon Web Services (AWS)](wiki/concepts/Amazon%20Web%20Services%20%28AWS%29.md): Cloud architecture.",
                idx_text,
            )
            self.assertIn(
                "- [Harness Engineering](wiki/concepts/Harness%20Engineering.md): Concept definition.",
                idx_text,
            )
            self.assertIn(
                "- [Harness Engineering](wiki/sources/Harness%20Engineering.md): Original essay summary.",
                idx_text,
            )

            proc_sug = subprocess.run(
                [
                    sys.executable, str(script_path),
                    "--project-root", str(root),
                    "--suggest-links", "Amazon Services",
                ],
                capture_output=True, text=True, check=True,
            )
            sug_out = json.loads(proc_sug.stdout)
            self.assertEqual(len(sug_out["matches"]), 1)
            self.assertEqual(sug_out["matches"][0]["path"], "wiki/concepts/Amazon Web Services (AWS).md")


if __name__ == "__main__":
    unittest.main()
