#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Scenario Profiles and Transcript Structure Validation
"""

from pathlib import Path
import sys
import unittest

# Add record-list directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from transcript_processor import (
    ProofreadBuilder,
    ScenarioType,
    validate_transcript_structure,
)


class TestScenarioValidation(unittest.TestCase):

    def test_proofread_builder_scenarios(self):
        # 1. Single Talk
        builder_st = ProofreadBuilder(
            title="GPU 漏洞挖掘",
            event="HITCON 2026",
            talk_id="91",
            speakers="PK",
            scenario=ScenarioType.SINGLE_TALK,
        )
        builder_st.add_section("研究目標", "目標受害者的手機上面裝了 App。")
        doc_st = builder_st.render()
        self.assertIn('title: "GPU 漏洞挖掘"', doc_st)
        self.assertIn("未做任何刪減或摘要縮寫", doc_st)

        # 2. Multi Paper
        builder_mp = ProofreadBuilder(
            title="研討會 Session G",
            event="研討會",
            scenario=ScenarioType.MULTI_PAPER,
        )
        builder_mp.add_section("論文一：語篇命題 (戴文芳)", "這是第一篇內容。")
        builder_mp.add_section("論文一評審講評與 Q&A 交流", "這是講評內容。")
        builder_mp.add_section("論文二：序列推薦 (林之璇)", "這是第二篇內容。")
        doc_mp = builder_mp.render()
        self.assertIn("未做任何刪減、摘要或人工造假注入", doc_mp)
        self.assertIn("明確標註發言角色（口試委員／指導教授／研究生／發表人／大會司儀）", doc_mp)

    def test_validate_single_talk(self):
        builder = ProofreadBuilder(
            title="Android Mali Driver",
            event="HITCON 2026",
            talk_id="91",
            speakers="PK",
            scenario=ScenarioType.SINGLE_TALK,
        )
        builder.add_section("技術架構", "核心結構是 kbase_context。")
        builder.add_section("現場 Q&A 問答交流", "**【現場會眾】**：請問這個漏洞是否修補？")
        doc = builder.render()

        is_valid, errors = validate_transcript_structure(doc, ScenarioType.SINGLE_TALK)
        self.assertTrue(is_valid, f"Validation failed: {errors}")
        self.assertEqual(len(errors), 0)

    def test_validate_multi_paper_passes(self):
        builder = ProofreadBuilder(
            title="Session I 專題",
            event="研討會 Session I",
            scenario=ScenarioType.MULTI_PAPER,
        )
        builder.add_section("論文一：DRAVILaMA (沈柏寧)", "結合對比學習微調 CodeLlama。")
        builder.add_section("論文一評審講評與 Q&A 交流", "歐陽長龍教授講評。")
        builder.add_section("論文二：區塊鏈電力交易 (張玉瑤)", "零知識證明方案。")
        builder.add_section("論文二評審講評與 Q&A 交流", "歐陽長龍教授講評。")
        doc = builder.render()

        is_valid, errors = validate_transcript_structure(doc, ScenarioType.MULTI_PAPER)
        self.assertTrue(is_valid, f"Validation failed: {errors}")

    def test_validate_multi_paper_fails_when_truncated_to_one_paper(self):
        builder = ProofreadBuilder(
            title="Session G 殘缺版",
            event="研討會 Session G",
            scenario=ScenarioType.MULTI_PAPER,
        )
        builder.add_section("論文一：aMCI 語篇", "只有一篇論文，後面的論文全被吃掉了。")
        doc = builder.render()

        is_valid, errors = validate_transcript_structure(doc, ScenarioType.MULTI_PAPER)
        self.assertFalse(is_valid)
        self.assertTrue(any("at least 2 paper sections" in e for e in errors))

    def test_validate_detects_banned_hallucinations(self):
        builder = ProofreadBuilder(
            title="測試腦補字句",
            event="研討會",
            scenario=ScenarioType.SINGLE_TALK,
        )
        builder.add_section("開場", "呃呃呃！大家好，今天來到這裡。")
        doc = builder.render()

        is_valid, errors = validate_transcript_structure(doc, ScenarioType.SINGLE_TALK)
        self.assertFalse(is_valid)
        self.assertTrue(any("Found banned hallucinated artifact phrase" in e for e in errors))

    def test_validate_real_conference_deliverables(self):
        base_dir = Path(__file__).parent.parent / "5-Master" / "20260327-AcademicConference"
        session_files = [
            base_dir / "SessionG-aMCI語篇研究-proofread.md",
            base_dir / "SessionG-AI焦慮與語音偽造-proofread.md",
            base_dir / "SessionI-特邀專題與學生論文-proofread.md",
        ]

        for s_file in session_files:
            self.assertTrue(s_file.exists(), f"File does not exist: {s_file}")
            content = s_file.read_text(encoding="utf-8")
            is_valid, errors = validate_transcript_structure(content, ScenarioType.MULTI_PAPER)
            self.assertTrue(is_valid, f"{s_file.name} failed structure validation: {errors}")


if __name__ == "__main__":
    unittest.main()
