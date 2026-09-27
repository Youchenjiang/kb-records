#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for SafeASREngine module
"""

import unittest
from pathlib import Path
import sys

# Add record-list directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from transcript_processor.asr import SafeASREngine


class TestSafeASREngine(unittest.TestCase):

    def setUp(self):
        self.engine = SafeASREngine(max_vram_fraction=0.60, chunk_duration_sec=30.0, overlap_sec=2.0, device="cpu")

    def test_interval_computation_short(self):
        intervals = self.engine.compute_chunk_intervals(total_duration_sec=20.0)
        self.assertEqual(intervals, [(0.0, 20.0)])

    def test_interval_computation_overlapping(self):
        intervals = self.engine.compute_chunk_intervals(total_duration_sec=70.0, chunk_duration=30.0, overlap=5.0)
        # step = 25.0
        # 0: 0.0 to 30.0
        # 1: 25.0 to 55.0
        # 2: 50.0 to 70.0
        expected = [(0.0, 30.0), (25.0, 55.0), (50.0, 70.0)]
        self.assertEqual(intervals, expected)

    def test_vram_fraction_clamping(self):
        low_engine = SafeASREngine(max_vram_fraction=0.01, device="cpu")
        self.assertEqual(low_engine.max_vram_fraction, 0.1)

        high_engine = SafeASREngine(max_vram_fraction=0.99, device="cpu")
        self.assertEqual(high_engine.max_vram_fraction, 0.9)


    def test_vram_info(self):
        info = self.engine.get_vram_info()
        self.assertIn("device", info)
        self.assertIn("max_fraction", info)
        self.assertEqual(info["max_fraction"], 0.60)

    def test_cleanup_memory(self):
        # Should execute cleanly without throwing errors
        self.engine.cleanup_memory()


if __name__ == "__main__":
    unittest.main()
