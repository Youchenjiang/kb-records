#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for AudioManager (audio staging lifecycle and safety)
"""

import tempfile
from pathlib import Path
import unittest

from transcript_processor import AudioManager


class TestAudioManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.manager = AudioManager(root_dir=self.root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_directory_initialization(self):
        self.assertTrue(self.manager.pending_dir.exists())
        self.assertTrue(self.manager.processed_dir.exists())
        self.assertTrue(self.manager.preserved_dir.exists())
        status = self.manager.get_status()
        self.assertEqual(status["pending"]["count"], 0)
        self.assertEqual(status["processed"]["count"], 0)
        self.assertEqual(status["preserved"]["count"], 0)

    def test_import_and_lifecycle(self):
        # Create a mock audio file in root
        dummy_audio = self.root / "sample_audio.mp3"
        dummy_audio.write_bytes(b"dummy audio binary data")

        # 1. Import to pending
        dest = self.manager.import_to_pending(dummy_audio)
        self.assertTrue(dest.exists())
        self.assertEqual(dest.parent, self.manager.pending_dir)

        status_pending = self.manager.get_status()
        self.assertEqual(status_pending["pending"]["count"], 1)
        self.assertEqual(status_pending["processed"]["count"], 0)
        self.assertEqual(status_pending["preserved"]["count"], 0)

        # 2. Mark as processed (finish)
        moved = self.manager.mark_as_processed("sample_audio.mp3")
        self.assertEqual(len(moved), 1)
        self.assertTrue(moved[0].exists())
        self.assertEqual(moved[0].parent, self.manager.processed_dir)

        status_proc = self.manager.get_status()
        self.assertEqual(status_proc["pending"]["count"], 0)
        self.assertEqual(status_proc["processed"]["count"], 1)
        self.assertEqual(status_proc["preserved"]["count"], 0)

    def test_preserve_non_speech_audio(self):
        # Create dummy music audio in pending
        music_file = self.manager.pending_dir / "piano_melody.mp3"
        music_file.write_bytes(b"piano music binary data")

        # Preserve with reason
        quarantined = self.manager.preserve_audio("piano_melody.mp3", reason="純鋼琴曲/非課堂研討")
        self.assertEqual(len(quarantined), 1)
        self.assertTrue(quarantined[0].exists())
        self.assertEqual(quarantined[0].parent, self.manager.preserved_dir)
        self.assertFalse(music_file.exists())

        # Check status
        status = self.manager.get_status()
        self.assertEqual(status["preserved"]["count"], 1)
        self.assertEqual(status["pending"]["count"], 0)

        # Check manifest
        manifest = self.manager.preserved_dir / "MANIFEST.md"
        self.assertTrue(manifest.exists())
        self.assertIn("piano_melody.mp3", manifest.read_text(encoding="utf-8"))
        self.assertIn("純鋼琴曲/非課堂研討", manifest.read_text(encoding="utf-8"))

    def test_clean_processed_protects_gitkeep_readme_and_preserved(self):
        # Create .gitkeep and README.md in processed
        gitkeep = self.manager.processed_dir / ".gitkeep"
        gitkeep.write_text("keep", encoding="utf-8")
        readme = self.manager.processed_dir / "README.md"
        readme.write_text("# Processed", encoding="utf-8")

        # Create dummy audio files in processed
        a1 = self.manager.processed_dir / "test1.aac"
        a1.write_bytes(b"data" * 1000)
        a2 = self.manager.processed_dir / "test2.wav"
        a2.write_bytes(b"data" * 1000)

        # Create dummy preserved file in preserved
        p1 = self.manager.preserved_dir / "quarantined_song.mp3"
        p1.write_bytes(b"music" * 1000)

        # Dry run
        count, freed = self.manager.clean_processed(dry_run=True)
        self.assertEqual(count, 2)
        self.assertTrue(a1.exists())
        self.assertTrue(a2.exists())
        self.assertTrue(p1.exists())

        # Actual clean
        count, freed = self.manager.clean_processed(dry_run=False)
        self.assertEqual(count, 2)
        self.assertFalse(a1.exists())
        self.assertFalse(a2.exists())

        # Crucial check: .gitkeep and README.md in processed MUST survive!
        self.assertTrue(gitkeep.exists())
        self.assertTrue(readme.exists())

        # Crucial check: preserved files MUST NEVER be deleted by clean_processed!
        self.assertTrue(p1.exists())


if __name__ == "__main__":
    unittest.main()
