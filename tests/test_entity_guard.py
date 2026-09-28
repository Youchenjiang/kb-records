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

    def test_verify_metadata_provenance_valid(self):
        meta = {
            "title": "碩士論文口試簡報：DRAVILaMA 惡意程式抗混淆偵測",
            "event": "碩士學位論文口試審查會",
            "speakers": ["沈柏寧", "陳奕明"],
        }
        text = "我是沈柏寧，今天向各位委員報告碩士學位論文..."
        is_valid, violations = EntityGuard.verify_metadata_provenance(meta, text)
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)

    def test_verify_metadata_provenance_hallucination_detected(self):
        meta = {
            "title": "碩士論文口試簡報",
            "event": "國立臺灣科技大學資訊工程系 碩士學位論文口試",
            "speakers": ["沈柏寧"],
        }
        text = "各位口試委員好，今天報告題目是惡意程式防護..."
        is_valid, violations = EntityGuard.verify_metadata_provenance(meta, text)
        self.assertFalse(is_valid)
        self.assertEqual(len(violations), 1)
        self.assertIn("國立臺灣科技大學資訊工程系", violations[0])

    def test_sanitize_metadata(self):
        meta = {
            "title": "碩士論文口試簡報",
            "event": "國立臺灣科技大學資訊工程系 碩士學位論文口試",
        }
        text = "各位口試委員好，今天報告題目是惡意程式防護..."
        sanitized = EntityGuard.sanitize_metadata(meta, text)
        self.assertEqual(sanitized["event"], "碩士學位論文口試審查會")

    def test_repository_all_metadata_provenance(self):
        """
        Anti-Hallucination Regression Linter:
        Asserts that every single proofread in 5-Master/ has valid provenance without hallucinated institutions.
        """
        repo_root = Path(__file__).parent.parent
        master_dir = repo_root / "5-Master"
        if not master_dir.exists():
            return

        import re
        total_checked = 0
        violations_all = []

        for p_file in master_dir.glob("**/*proofread*.md"):
            content = p_file.read_text(encoding="utf-8")
            fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if not fm_match:
                continue

            metadata = {}
            for line in fm_match.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip()] = v.strip().strip('"').strip("'")

            is_valid, violations = EntityGuard.verify_metadata_provenance(metadata, content)
            total_checked += 1
            if not is_valid:
                violations_all.extend([f"[{p_file.name}] {v}" for v in violations])

        self.assertGreater(total_checked, 0, "Should have checked at least one file")
        self.assertEqual(violations_all, [], f"Hallucination / provenance violations detected: {violations_all}")


if __name__ == "__main__":
    unittest.main()
