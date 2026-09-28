#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proofread Linter & Format Guard Test Suite
Validates all proofread.md documents across the repository to ensure strict compliance
with PROOFREAD_RULES.md (speaker attributions, clean headers, valid frontmatter, zero hallucinations).
"""

from pathlib import Path
import re
import sys
import unittest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from transcript_processor.structurer import ScenarioType, validate_transcript_structure

REPO_ROOT = Path(__file__).parent.parent


class TestProofreadLinter(unittest.TestCase):
    """
    Automated linting and format guard for all proofread documents.
    """

    def test_classroom_lecture_scenario_validation(self):
        """Test that classroom-lecture requires speaker attribution."""
        bad_text = (
            "---\n"
            'title: "測試課程"\n'
            'event: "教育訓練"\n'
            'speakers: ["授課講師"]\n'
            'type: "verbatim-narrative-transcript"\n'
            "verbatim: true\n"
            'scenario: "classroom-lecture"\n'
            "---\n\n"
            "# 🎙️ 測試課程 (授課講師)\n\n"
            "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。\n\n"
            "---\n\n"
            "## 🎯 模組介紹\n\n"
            "今天我們來上課。\n"
        )
        is_valid, errors = validate_transcript_structure(bad_text, scenario="classroom-lecture")
        self.assertFalse(is_valid)
        self.assertTrue(any("授課講師" in e for e in errors))

        good_text = (
            "---\n"
            'title: "測試課程"\n'
            'event: "教育訓練"\n'
            'speakers: ["授課講師"]\n'
            'type: "verbatim-narrative-transcript"\n'
            "verbatim: true\n"
            'scenario: "classroom-lecture"\n'
            "---\n\n"
            "# 🎙️ 測試課程 (授課講師)\n\n"
            "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。\n\n"
            "---\n\n"
            "## 🎯 模組介紹\n\n"
            "**【授課講師】**：今天我們來上課。\n"
        )
        is_valid, errors = validate_transcript_structure(good_text, scenario="classroom-lecture")
        self.assertTrue(is_valid, f"Validation failed with: {errors}")

    def test_no_artificial_heading_numbering(self):
        """Test that headings do not use artificial numbering like '一、', '二、'."""
        bad_heading = (
            "---\n"
            'title: "測試課程"\n'
            'event: "教育訓練"\n'
            'speakers: ["授課講師"]\n'
            'type: "verbatim-narrative-transcript"\n'
            "verbatim: true\n"
            'scenario: "classroom-lecture"\n'
            "---\n\n"
            "# 🎙️ 測試課程 (授課講師)\n\n"
            "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。\n\n"
            "---\n\n"
            "## 🎯 一、模組介紹\n\n"
            "**【授課講師】**：今天我們來上課。\n"
        )
        is_valid, errors = validate_transcript_structure(bad_heading, scenario="classroom-lecture")
        self.assertFalse(is_valid)
    def test_all_university_proofread_files(self):
        """Test that all 17 university proofread deliverables pass structure validation."""
        univ_files = list((REPO_ROOT / "4-University").glob("**/*-proofread.md"))
        self.assertEqual(len(univ_files), 17, f"Expected 17 university proofread files, found {len(univ_files)}")
        for f in univ_files:
            content = f.read_text(encoding="utf-8")
            is_valid, errors = validate_transcript_structure(content, scenario="classroom-lecture")
            self.assertTrue(is_valid, f"{f.name} failed structure validation: {errors}")


if __name__ == "__main__":
    unittest.main()

