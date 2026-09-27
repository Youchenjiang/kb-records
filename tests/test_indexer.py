#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for CatalogIndexer
Verifies automated transcript scanning, metadata extraction,
and generation of CATALOG.md and CATALOG.zh-TW.md.
"""

from pathlib import Path
import tempfile
import pytest

from transcript_processor.indexer import CatalogIndexer, CatalogItem


def test_catalog_indexer_metadata_parsing():
    content = """---
title: "Test Security Conference"
event: "20260821-TEST"
date: "2026-08-21"
speakers: ["Alice", "Bob"]
scenario: "single-talk"
category: "1-Security"
tags: ["exploit", "kernel"]
---

# 🎙️ Test Security Conference
"""
    indexer = CatalogIndexer(root_dir=Path("."))
    meta = indexer._parse_metadata(
        path=Path("1-Security/20260821-TEST/proofread.md"),
        content=content,
        rel_path=Path("1-Security/20260821-TEST/proofread.md"),
    )
    assert meta["title"] == "Test Security Conference"
    assert meta["event"] == "20260821-TEST"
    assert meta["date"] == "2026-08-21"
    assert meta["speakers"] == ["Alice", "Bob"]
    assert meta["scenario"] == "single-talk"
    assert meta["category"] == "1-Security"


def test_catalog_indexer_fallback_parsing():
    content = """# 🎙️ Reverse Engineering ARM Firmware (Speaker: Nan Wang)

Here is the transcript without frontmatter...
"""
    indexer = CatalogIndexer(root_dir=Path("."))
    meta = indexer._parse_metadata(
        path=Path("1-Security/20260821-HITCON/firmware-proofread.md"),
        content=content,
        rel_path=Path("1-Security/20260821-HITCON/firmware-proofread.md"),
    )
    assert "Reverse Engineering ARM Firmware" in meta["title"]
    assert meta["category"] == "1-Security"
    assert meta["event"] == "20260821-HITCON"


def test_catalog_indexer_markdown_generation():
    items = [
        CatalogItem(
            title="Kernel Exploit Analysis",
            category="1-Security",
            event="20260821-HITCON",
            date="2026-08-21",
            speakers=["Nan Wang"],
            scenario="single-talk",
            proofread_path=Path("1-Security/20260821-HITCON/proofread.md"),
            summary_path=Path("1-Security/20260821-HITCON/summary.md"),
        ),
        CatalogItem(
            title="Azure OpenAI Multi-Agent",
            category="2-Cloud-AI",
            event="20260922-DevDays",
            date="2026-09-22",
            speakers=["Microsoft Architect"],
            scenario="single-talk",
            proofread_path=Path("2-Cloud-AI/20260922-DevDays/proofread.md"),
            summary_path=None,
        ),
    ]

    indexer = CatalogIndexer(root_dir=Path("."))
    zh_md = indexer.generate_markdown(items, lang="zh-TW")
    assert "全局會議、演講與逐字稿目錄索引" in zh_md
    assert "Kernel Exploit Analysis" in zh_md
    assert "Azure OpenAI Multi-Agent" in zh_md
    assert "1-Security" in zh_md
    assert "2-Cloud-AI" in zh_md

    en_md = indexer.generate_markdown(items, lang="en")
    assert "Master Catalog of Transcripts & Summaries" in en_md
    assert "Kernel Exploit Analysis" in en_md
    assert "Azure OpenAI Multi-Agent" in en_md


def test_catalog_indexer_real_workspace_scan():
    indexer = CatalogIndexer(root_dir=Path("."))
    items = indexer.scan()
    # Repository has multiple transcripts across 1-Security and 5-Master
    assert len(items) >= 10
    titles = [it.title for it in items]
    # Check that known items are detected
    assert any("OSINT" in t for t in titles)
    assert any("DRAVILaMA" in t for t in titles)
    assert any("Pixel8A" in t or "GPU" in t for t in titles)


def test_catalog_indexer_file_writing():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        sub = tmp_path / "1-Security" / "20260101-Test"
        sub.mkdir(parents=True)
        (sub / "proofread.md").write_text(
            '---\ntitle: "Mock Talk"\nevent: "20260101-Test"\nspeakers: ["Tester"]\nscenario: "single-talk"\n---\n# Body',
            encoding="utf-8",
        )
        (sub / "summary.md").write_text("# Summary", encoding="utf-8")

        indexer = CatalogIndexer(root_dir=tmp_path)
        count, en_file, zh_file = indexer.update_catalog_files()
        assert count == 1
        assert en_file.exists()
        assert zh_file.exists()
        assert "Mock Talk" in en_file.read_text(encoding="utf-8")
        assert "Mock Talk" in zh_file.read_text(encoding="utf-8")
