#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repetition Loop & Hallucination Guard Test Suite
Guards against ASR repetition loops, decoder stutter artifacts, and consecutive duplicate sentences.
"""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from transcript_processor.structurer import validate_no_repetition_loops

REPO_ROOT = Path(__file__).parent.parent


class TestRepetitionAndHallucination(unittest.TestCase):
    """
    Automated guard against ASR hallucination loops and repetition artifacts.
    """

    def test_phrase_repetition_loop_detection(self):
        """Test catching short repeating phrase loops like '少少少' or '推論資料'."""
        bad_loop = "我們先少編一點預算。少少少，少少少，少少少，少少少。然後下個月再看。"
        errors = validate_no_repetition_loops(bad_loop)
        self.assertTrue(any("少少少" in e for e in errors))

    def test_consecutive_duplicate_sentences_detection(self):
        """Test catching identical consecutive sentence loops."""
        bad_sentences = (
            "那我們就是要假設我們是攻擊者，然後去使用這個系統去抽取到這個站點的權限資料。\n\n"
            "那我們就是要假設我們是攻擊者，然後去使用這個系統去抽取到這個站點的權限資料。\n\n"
            "那我們就是要假設我們是攻擊者，然後去使用這個系統去抽取到這個站點的權限資料。\n\n"
            "接下來我們看第四個部分。"
        )
        errors = validate_no_repetition_loops(bad_sentences)
        self.assertTrue(any("consecutive identical sentences" in e for e in errors))

    def test_natural_conversational_repetition_allowed(self):
        """Test that natural conversational spoken expressions up to reasonable limits pass."""
        good_speech = "對啊，對啊，對啊，我們下週會針對這個題目進行專題報告。"
        errors = validate_no_repetition_loops(good_speech)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
