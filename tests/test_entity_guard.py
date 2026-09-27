#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for EntityGuard module
"""

import unittest
from pathlib import Path
import sys

# Add record-list directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from transcript_processor.entity_guard import EntityGuard, EntityCandidate


class TestEntityGuard(unittest.TestCase):

    def setUp(self):
        self.guard = EntityGuard()

    def test_extract_candidates(self):
        sample_text = (
            "各位好，我是沈國立同學。今天由指導教授陳一鳴博士指導我的碩士論文報告。"
            "另外感謝口試委員蔡志峰教授的提問。沈國立同學請繼續說明。"
        )
        candidates = self.guard.extract_candidates(sample_text)
        candidate_terms = [c.raw_term for c in candidates]

        self.assertIn("沈國立", candidate_terms)
        self.assertIn("陳一鳴", candidate_terms)
        self.assertIn("蔡志峰", candidate_terms)

        # Check frequency
        shen_candidate = next(c for c in candidates if c.raw_term == "沈國立")
        self.assertEqual(shen_candidate.count, 2)

    def test_generate_verification_report(self):
        sample_text = "指導教授陳一鳴博士與沈國立同學。"
        candidates = self.guard.extract_candidates(sample_text)
        report = self.guard.generate_verification_report(candidates)

        self.assertIn("專有名詞與人名候選清單", report)
        self.assertIn("陳一鳴", report)
        self.assertIn("待確認", report)

    def test_apply_confirmed_entities(self):
        self.guard.register_confirmed("沈國立", "沈柏寧")
        self.guard.register_confirmed("陳一鳴", "陳奕明")
        text = "我是沈國立，指導教授為陳一鳴博士。"
        result = self.guard.apply_confirmed_entities(text)
        self.assertEqual(result, "我是沈柏寧，指導教授為陳奕明博士。")

    def test_unconfirmed_filter(self):
        text = "指導教授陳一鳴博士與沈國立同學共同參與。"
        self.guard.register_confirmed("沈國立", "沈柏寧")
        unconfirmed = self.guard.get_unconfirmed_candidates(text)
        unconfirmed_terms = [c.raw_term for c in unconfirmed]

        self.assertNotIn("沈國立", unconfirmed_terms)
        self.assertIn("陳一鳴", unconfirmed_terms)


if __name__ == "__main__":
    unittest.main()
