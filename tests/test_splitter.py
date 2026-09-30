#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for TranscriptSplitter
Verifies lossless splitting, frontmatter parsing, section inspection,
and generation of Option 3-A dual-tier deliverables.
"""

from pathlib import Path
import tempfile
import unittest

from transcript_processor.splitter import TranscriptSplitter, SplitSegmentConfig


class TestTranscriptSplitter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        self.splitter = TranscriptSplitter(root_dir=self.root_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_frontmatter_and_body(self):
        sample = """---
title: "Parent Recording"
event: "20260226-Lab"
date: "2026-02-26"
speakers: ["Alice", "Bob"]
scenario: "lab-meeting"
---

# 🎙️ Parent Recording Header

## 01. Topic A
Content A line 1
Content A line 2

## 02. Topic B
Content B line 1
"""
        meta, body = self.splitter.parse_frontmatter_and_body(sample)
        self.assertEqual(meta["title"], "Parent Recording")
        self.assertEqual(meta["event"], "20260226-Lab")
        self.assertEqual(meta["date"], "2026-02-26")
        self.assertEqual(meta["speakers"], ["Alice", "Bob"])
        self.assertIn("## 01. Topic A", body)

    def test_inspect_sections(self):
        file_path = self.root_path / "sample.md"
        content = """# Title
> intro
## 01. First Section
details
## 02. Second Section
more details
"""
        file_path.write_text(content, encoding="utf-8")
        sections = self.splitter.inspect_sections(file_path)
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["line"], 3)
        self.assertEqual(sections[0]["header"], "## 01. First Section")
        self.assertEqual(sections[1]["line"], 5)
        self.assertEqual(sections[1]["header"], "## 02. Second Section")

    def test_split_transcript_lossless(self):
        full_path = self.root_path / "mixed.full.md"
        full_content = """---
title: "Mixed Session"
event: "Mixed-Event"
date: "2026-04-30"
speakers: ["George", "Student"]
scenario: "classroom-lecture"
---

# 🎙️ Mixed Session

## 01. Anime Popularity Prediction
Anime line 1
Anime line 2

## 02. Fault-Tolerant VPS Testing
VPS line 1
VPS line 2
"""
        full_path.write_text(full_content, encoding="utf-8")

        summary_path = self.root_path / "mixed.md"
        summary_content = """# 🛡️ Mixed Session Summary
> Summary intro

### 1. Anime Summary
Key points on anime

### 2. VPS Summary
Key points on VPS
"""
        summary_path.write_text(summary_content, encoding="utf-8")

        segments = [
            SplitSegmentConfig(
                filename_base="20260430-Anime-Model",
                output_dir="Course/AdvAI",
                title="Anime Model Presentation",
                event="AdvancedAI-Optimization",
                scenario="classroom-lecture",
                speakers=["George", "Student"],
                talk_id="20260430-01",
                start_line=10,
                end_line=13,
                summary_start_line=4,
                summary_end_line=5,
            ),
            SplitSegmentConfig(
                filename_base="20260430-VPS-Evaluation",
                output_dir="Lab/Project-Meeting",
                title="Fault-Tolerant VPS Evaluation",
                event="Project-Meeting",
                scenario="lab-meeting",
                speakers=["Student", "Professor Wang"],
                talk_id="20260430-02",
                start_line=14,
                end_line=17,
                summary_start_line=7,
                summary_end_line=8,
            ),
        ]

        created = self.splitter.split_transcript(
            full_md_path=full_path,
            segments=segments,
            summary_md_path=summary_path,
        )

        self.assertEqual(len(created), 2)

        # Check segment 1
        seg1_full, seg1_sum = created[0]
        self.assertTrue(seg1_full.exists())
        self.assertTrue(seg1_sum.exists())
        seg1_full_text = seg1_full.read_text(encoding="utf-8")
        self.assertIn("Anime line 1", seg1_full_text)
        self.assertIn("Anime line 2", seg1_full_text)
        self.assertNotIn("VPS line 1", seg1_full_text)
        self.assertIn('scenario: "classroom-lecture"', seg1_full_text)

        seg1_sum_text = seg1_sum.read_text(encoding="utf-8")
        self.assertIn("Key points on anime", seg1_sum_text)
        self.assertIn("[📄 完整原話逐字稿 (20260430-Anime-Model.full.md)](./20260430-Anime-Model.full.md)", seg1_sum_text)

        # Check segment 2
        seg2_full, seg2_sum = created[1]
        self.assertTrue(seg2_full.exists())
        self.assertTrue(seg2_sum.exists())
        seg2_full_text = seg2_full.read_text(encoding="utf-8")
        self.assertIn("VPS line 1", seg2_full_text)
        self.assertIn("VPS line 2", seg2_full_text)
        self.assertNotIn("Anime line 1", seg2_full_text)
        self.assertIn('scenario: "lab-meeting"', seg2_full_text)


if __name__ == "__main__":
    unittest.main()
