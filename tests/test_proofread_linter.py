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
    def test_mermaid_block_validation(self):
        """Test Mermaid validation: detects node/subgraph collision and syntax errors."""
        from transcript_processor.structurer import validate_mermaid_blocks

        bad_mermaid = (
            "```mermaid\n"
            "flowchart TD\n"
            '    subgraph CoreEngine["核心引擎"]\n'
            '        CoreEngine["引擎節點"] --> Output\n'
            "    end\n"
            "```"
        )
        errs = validate_mermaid_blocks(bad_mermaid)
        self.assertTrue(any("syntax error" in e and "CoreEngine" in e for e in errs), f"Expected collision error, got: {errs}")

        good_mermaid = (
            "```mermaid\n"
            "flowchart TD\n"
            '    subgraph CoreEngine["核心引擎"]\n'
            '        Node1["引擎節點"] --> Output\n'
            "    end\n"
            "```"
        )
        errs_good = validate_mermaid_blocks(good_mermaid)
        self.assertEqual(errs_good, [])

    def test_traditional_chinese_validation(self):
        """Test Traditional Chinese guard: catches strictly Simplified Chinese characters."""
        from transcript_processor.structurer import validate_traditional_chinese

        bad_tc = "這是一個包含误報率與改进方向的句子。"
        errs = validate_traditional_chinese(bad_tc)
        self.assertTrue(len(errs) >= 2, f"Expected simplified Chinese errors, got: {errs}")

        good_tc = "這是一個包含誤報率與改進方向的繁體中文句子。"
        errs_good = validate_traditional_chinese(good_tc)
        self.assertEqual(errs_good, [])

    def test_banned_asr_garbles(self):
        """Test detection of banned ASR phonetic garble artifacts."""
        from transcript_processor.structurer import validate_banned_asr_garbles

        bad_asr = "我們透過巨就是巨無安直接操作，然後A A P I推算兩百。"
        errs = validate_banned_asr_garbles(bad_asr)
        self.assertTrue(any("巨就是巨無安" in e for e in errs))
        self.assertTrue(any("推算兩百" in e for e in errs))

        good_asr = "我們透過 GUI 介面直接操作，然後 API 回傳 200。"
        errs_good = validate_banned_asr_garbles(good_asr)
        self.assertEqual(errs_good, [])

    def test_speaker_semantic_consistency(self):
        """Test detection of inverted speaker attributions and semantic role mismatch."""
        from transcript_processor.structurer import validate_speaker_semantic_consistency

        inverted_dialogue = (
            "**【侑宸】**：好，那侑宸你的簡報時間到了，我先講評。\n\n"
            "**【指導教授】**：我的碩士論文題目是黑箱漏洞探索，接下來由我報告第四章。"
        )
        errs = validate_speaker_semantic_consistency(inverted_dialogue)
        self.assertTrue(any("侑宸" in e for e in errs))
        self.assertTrue(any("指導教授" in e for e in errs))

        consistent_dialogue = (
            "**【侑宸】**：各位委員好，我的碩士論文題目是黑箱漏洞探索，接下來由我報告第四章。\n\n"
            "**【指導教授】**：好，那侑宸你的簡報時間到了，接下來請口試委員提問。"
        )
        errs_good = validate_speaker_semantic_consistency(consistent_dialogue)
        self.assertEqual(errs_good, [])

    def test_heading_attribution_validation(self):
        """Test heading attribution guard: ensures external research datasets are explicitly attributed."""
        from transcript_processor.structurer import validate_heading_attribution

        bad_heading = "## 📊 基準論文資料集剖析：16 位學生手工標註 47 個真實商業邏輯漏洞案例"
        errs = validate_heading_attribution(bad_heading)
        self.assertTrue(len(errs) > 0, f"Expected attribution error, got: {errs}")

        good_heading = "## 📊 外部基準文獻對標：借鑑經典研究（外部學者與 16 位學生標註之 47 個漏洞資料集）與消融實驗設計"
        errs_good = validate_heading_attribution(good_heading)
        self.assertEqual(errs_good, [])

    def test_all_proofread_deliverables_structure(self):
        """Test that ALL proofread deliverables across University and Master pass structure validation."""
        all_full_files = sorted(
            list((REPO_ROOT / "4-University").glob("**/*.full.md")) +
            list((REPO_ROOT / "5-Master").glob("**/*.full.md"))
        )
        self.assertGreaterEqual(len(all_full_files), 220, f"Expected at least 220 proofread files, found {len(all_full_files)}")
        failed_files = []
        for f in all_full_files:
            content = f.read_text(encoding="utf-8")
            m = re.search(r'scenario:\s*["\']?([a-zA-Z0-9_-]+)["\']?', content)
            scenario = m.group(1) if m else "classroom-lecture"
            is_valid, errors = validate_transcript_structure(content, scenario=scenario)
            if not is_valid:
                failed_files.append((f.relative_to(REPO_ROOT), errors))
        self.assertEqual(failed_files, [], f"Deliverables failed structure validation:\n" + "\n".join(f"{f}: {errs}" for f, errs in failed_files))

    def test_all_executive_summaries_validation(self):
        """Test that ALL executive summaries (.md) pass summary validation."""
        from transcript_processor.structurer import validate_summary_document

        all_summaries = sorted([
            f for f in (list((REPO_ROOT / "4-University").glob("**/*.md")) + list((REPO_ROOT / "5-Master").glob("**/*.md")))
            if not f.name.endswith(".full.md") and f.name != "README.md"
        ])
        self.assertGreaterEqual(len(all_summaries), 220, f"Expected at least 220 summaries, found {len(all_summaries)}")
        failed = []
        for f in all_summaries:
            content = f.read_text(encoding="utf-8")
            is_valid, errors = validate_summary_document(content, file_path=str(f.relative_to(REPO_ROOT)))
            if not is_valid:
                failed.append((f.relative_to(REPO_ROOT), errors))
        self.assertEqual(failed, [], f"Summaries failed validation:\n" + "\n".join(f"{f}: {errs}" for f, errs in failed))


if __name__ == "__main__":
    unittest.main()

