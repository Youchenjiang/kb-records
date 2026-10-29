#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Domain Terminology & ASR Misrecognition Guard Test Suite
Validates transcripts to ensure domain-specific terminology (Information Management,
Cybersecurity, Machine Learning) is preserved and common ASR phonetic misrecognitions are banned.
"""

from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from transcript_processor.structurer import BANNED_ASR_GARBLES, validate_banned_asr_garbles

REPO_ROOT = Path(__file__).parent.parent


class TestDomainTerminology(unittest.TestCase):
    """
    Test suite for domain terminology accuracy and ASR garble prevention.
    """

    def test_banned_garbles_detection_unit(self):
        """Verify detector catches all registered domain garbles."""
        sample_bad = (
            "這篇論文研究被他買技術，老師說我們缺乏良性，放那麼多鍵盤只是重版面。"
            "工具者去使用它，並品嚐我們的攻擊資料，我阿弟參考一下。"
        )
        errors = validate_banned_asr_garbles(sample_bad)
        self.assertTrue(any("被他買" in e for e in errors))
        self.assertTrue(any("缺乏良性" in e for e in errors))
        self.assertTrue(any("放那麼多鍵盤" in e for e in errors))
        self.assertTrue(any("重版面" in e for e in errors))
        self.assertTrue(any("工具者" in e for e in errors))
        self.assertTrue(any("品嚐我們的攻擊" in e for e in errors))
        self.assertTrue(any("我阿弟參考" in e for e in errors))

    def test_clean_technical_text_passes(self):
        """Verify proper technical terminology passes cleanly."""
        sample_good = (
            "這篇論文探討 Data Mining 資料探勘技術，中央大學應具備強烈狼性積極爭取資源。"
            "碩士論文切勿堆疊教科書內容刻意充版面。攻擊者透過混淆編碼繞過檢測，請各位參考。"
        )
        errors = validate_banned_asr_garbles(sample_good)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
