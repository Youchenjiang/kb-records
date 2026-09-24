#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for transcript_processor toolkit
"""

import unittest
from pathlib import Path
import sys

# Add record-list directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from transcript_processor import (
    clean_cjk_spaces,
    normalize_punctuation,
    clean_transcript,
    CorrectionEngine,
    ProofreadBuilder,
    SummaryBuilder,
    MermaidDiagram,
)


class TestTranscriptProcessor(unittest.TestCase):

    def test_cleaner_spaces(self):
        raw = "你 可 以 去 把 它 做 這 些 分 類"
        cleaned = clean_cjk_spaces(raw)
        self.assertEqual(cleaned, "你可以去把它做這些分類")

    def test_cleaner_mixed_english(self):
        raw = "使 用 60 比 較 多 ， 跑 在 x8664"
        cleaned = clean_cjk_spaces(raw)
        self.assertEqual(cleaned, "使用 60 比較多，跑在 x8664")

    def test_punctuation_normalization(self):
        raw = "分類,然後一步.測試;問號?驚嘆!冒號:"
        norm = normalize_punctuation(raw)
        self.assertEqual(norm, "分類，然後一步。測試；問號？驚嘆！冒號：")

    def test_corrector_engine(self):
        engine = CorrectionEngine()
        raw = "在 dpend cloud 和 admin security 中發現 M GPQ driver 漏洞"
        corrected = engine.correct(raw)
        self.assertIn("Defender for Cloud", corrected)
        self.assertIn("Advanced Security", corrected)
        self.assertIn("Mali GPU driver", corrected)

    def test_custom_domain_rule(self):
        engine = CorrectionEngine()
        engine.register_rule("custom", "舊測試名", "新測試名")
        res = engine.correct("這是一個舊測試名的字串", domains=["custom"])
        self.assertEqual(res, "這是一個新測試名的字串")

    def test_proofread_builder(self):
        builder = ProofreadBuilder(
            title="測試演講",
            event="HITCON-2026",
            talk_id="99",
            speakers=["講者A", "講者B"],
        )
        builder.add_section("開場", "這是測試段落一。")
        rendered = builder.render()
        self.assertIn('title: "測試演講"', rendered)
        self.assertIn('talk_id: "99"', rendered)
        self.assertIn("## 開場", rendered)
        self.assertIn("這是測試段落一。", rendered)

    def test_summary_builder(self):
        builder = SummaryBuilder(
            talk_id="99",
            title="測試演講",
            speaker="講者A",
            topic="測試主題",
            tech_stack="Python, LLM",
            outcome="提升100%",
        )
        diagram = MermaidDiagram()
        diagram.add("A[輸入] --> B[輸出]")
        builder.set_diagram(diagram)
        builder.add_section("技術剖析", "架構說明。")
        builder.add_takeaway("核心要點一。")
        rendered = builder.render()
        self.assertIn("# 📑 99 測試演講 (講者A)", rendered)
        self.assertIn("```flowchart TD", rendered)
        self.assertIn("A[輸入] --> B[輸出]", rendered)
        self.assertIn("1. 核心要點一。", rendered)


if __name__ == "__main__":
    unittest.main()
