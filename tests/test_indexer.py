#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for CatalogIndexer
Verifies automated transcript scanning, metadata extraction,
and generation of CATALOG.md and CATALOG.zh-TW.md.
"""

from pathlib import Path
import tempfile
import unittest

from transcript_processor.indexer import CatalogIndexer, CatalogItem


class TestCatalogIndexer(unittest.TestCase):

    def test_catalog_indexer_metadata_parsing(self):
        content = """---
title: "Test Security Conference"
event: "20260821-TEST"
date: "2026-08-21"
speakers: ["Alice", "Bob"]
scenario: "single-talk"
category: "5-Master"
tags: ["exploit", "kernel"]
---

# 🎙️ Test Security Conference
"""
        indexer = CatalogIndexer(root_dir=Path("."))
        meta = indexer._parse_metadata(
            path=Path("5-Master/20260821-TEST/proofread.md"),
            content=content,
            rel_path=Path("5-Master/20260821-TEST/proofread.md"),
        )
        self.assertEqual(meta["title"], "Test Security Conference")
        self.assertEqual(meta["event"], "20260821-TEST")
        self.assertEqual(meta["date"], "2026-08-21")
        self.assertEqual(meta["speakers"], ["Alice", "Bob"])
        self.assertEqual(meta["scenario"], "single-talk")
        self.assertEqual(meta["category"], "5-Master")

    def test_catalog_indexer_fallback_parsing(self):
        content = """# 🎙️ Reverse Engineering ARM Firmware (Speaker: Nan Wang)

Here is the transcript without frontmatter...
"""
        indexer = CatalogIndexer(root_dir=Path("."))
        meta = indexer._parse_metadata(
            path=Path("5-Master/20260821-HITCON/firmware-proofread.md"),
            content=content,
            rel_path=Path("5-Master/20260821-HITCON/firmware-proofread.md"),
        )
        self.assertIn("Reverse Engineering ARM Firmware", meta["title"])
        self.assertEqual(meta["category"], "5-Master")
        self.assertEqual(meta["event"], "20260821-HITCON")

    def test_catalog_indexer_markdown_generation(self):
        items = [
            CatalogItem(
                title="Kernel Exploit Analysis",
                category="5-Master",
                event="20260821-HITCON",
                date="2026-08-21",
                speakers=["Nan Wang"],
                scenario="single-talk",
                proofread_path=Path("5-Master/20260821-HITCON/proofread.md"),
                summary_path=Path("5-Master/20260821-HITCON/summary.md"),
            ),
            CatalogItem(
                title="Azure OpenAI Multi-Agent",
                category="5-Master",
                event="20260922-DevDays",
                date="2026-09-22",
                speakers=["Microsoft Architect"],
                scenario="single-talk",
                proofread_path=Path("5-Master/20260922-DevDays/proofread.md"),
                summary_path=None,
            ),
        ]

        indexer = CatalogIndexer(root_dir=Path("."))
        zh_md = indexer.generate_markdown(items, lang="zh-TW")
        self.assertIn("全局會議、演講與逐字稿目錄索引", zh_md)
        self.assertIn("Kernel Exploit Analysis", zh_md)
        self.assertIn("Azure OpenAI Multi-Agent", zh_md)
        self.assertIn("5-Master", zh_md)

        en_md = indexer.generate_markdown(items, lang="en")
        self.assertIn("Master Catalog of Transcripts & Summaries", en_md)
        self.assertIn("Kernel Exploit Analysis", en_md)
        self.assertIn("Azure OpenAI Multi-Agent", en_md)

    def test_catalog_indexer_real_workspace_scan(self):
        indexer = CatalogIndexer(root_dir=Path("."))
        items = indexer.scan()
        self.assertGreaterEqual(len(items), 10)
        titles = [it.title for it in items]
        self.assertTrue(any("OSINT" in t for t in titles))
        self.assertTrue(any("DRAVILaMA" in t for t in titles))
        self.assertTrue(any("Pixel8A" in t or "GPU" in t for t in titles))

    def test_catalog_indexer_file_writing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            sub = tmp_path / "5-Master" / "20260101-Test"
            sub.mkdir(parents=True)
            (sub / "proofread.md").write_text(
                '---\ntitle: "Mock Talk"\nevent: "20260101-Test"\nspeakers: ["Tester"]\nscenario: "single-talk"\n---\n# Body',
                encoding="utf-8",
            )
            (sub / "summary.md").write_text("# Summary", encoding="utf-8")

            indexer = CatalogIndexer(root_dir=tmp_path)
            count, en_file, zh_file = indexer.update_catalog_files()
            self.assertEqual(count, 1)
            self.assertTrue(en_file.exists())
            self.assertTrue(zh_file.exists())
            self.assertIn("Mock Talk", en_file.read_text(encoding="utf-8"))
            self.assertIn("Mock Talk", zh_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
