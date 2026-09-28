#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Lifecycle Manager for Transcript Processor Toolkit
Manages the staging and lifecycle of audio files between pending and processed states.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

AUDIO_EXTENSIONS = {
    ".aac", ".mp3", ".m4a", ".wav", ".flac", ".ogg", ".opus", ".wma", ".mp4", ".mkv"
}


class AudioManager:
    """
    Manages audio files lifecycle:
    - pending: unprocessed or currently running ASR
    - processed: finished transcription & proofreading (safe to delete)
    """

    def __init__(self, root_dir: Optional[Union[str, Path]] = None):
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()
        self.audio_dir = self.root_dir / "audio"
        self.pending_dir = self.audio_dir / "pending"
        self.processed_dir = self.audio_dir / "processed"

        # Ensure directories exist
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def _get_audio_files(self, target_dir: Path) -> List[Path]:
        """List all media files with recognized extensions in the directory."""
        if not target_dir.exists():
            return []
        files = [
            f for f in target_dir.iterdir()
            if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
        ]
        files.sort(key=lambda x: x.name)
        return files

    def get_status(self) -> Dict:
        """
        Inspect pending and processed audio directories.
        Returns details of file counts and disk usage.
        """
        pending_files = self._get_audio_files(self.pending_dir)
        processed_files = self._get_audio_files(self.processed_dir)

        def _stats(files: List[Path]):
            total_bytes = sum(f.stat().st_size for f in files)
            return {
                "count": len(files),
                "total_bytes": total_bytes,
                "total_mb": round(total_bytes / (1024 * 1024), 2),
                "files": [
                    {"name": f.name, "size_mb": round(f.stat().st_size / (1024 * 1024), 2)}
                    for f in files
                ],
            }

        return {
            "pending": _stats(pending_files),
            "processed": _stats(processed_files),
        }

    def import_to_pending(self, source_path: Union[str, Path]) -> Optional[Path]:
        """
        Move or stage an audio file into audio/pending/.
        """
        src = Path(source_path)
        if not src.is_absolute():
            src = self.root_dir / src

        if not src.exists() or not src.is_file():
            raise FileNotFoundError(f"Source audio file not found: {src}")

        dest = self.pending_dir / src.name
        if src.resolve() == dest.resolve():
            return dest

        shutil.move(str(src), str(dest))
        return dest

    def mark_as_processed(self, filename_or_pattern: str) -> List[Path]:
        """
        Move audio file(s) from pending (or root) to audio/processed/.
        """
        moved = []
        target_name = Path(filename_or_pattern).name

        # Check pending dir first
        cand_in_pending = self.pending_dir / target_name
        if cand_in_pending.exists():
            dest = self.processed_dir / target_name
            shutil.move(str(cand_in_pending), str(dest))
            moved.append(dest)
            return moved

        # Check root dir fallback
        cand_in_root = self.root_dir / target_name
        if cand_in_root.exists():
            dest = self.processed_dir / target_name
            shutil.move(str(cand_in_root), str(dest))
            moved.append(dest)
            return moved

        # Glob search in pending
        for match in self.pending_dir.glob(filename_or_pattern):
            if match.is_file() and match.suffix.lower() in AUDIO_EXTENSIONS:
                dest = self.processed_dir / match.name
                shutil.move(str(match), str(dest))
                moved.append(dest)

        # Glob search in root
        for match in self.root_dir.glob(filename_or_pattern):
            if match.is_file() and match.suffix.lower() in AUDIO_EXTENSIONS:
                dest = self.processed_dir / match.name
                shutil.move(str(match), str(dest))
                moved.append(dest)

        return moved

    def clean_processed(self, dry_run: bool = False) -> Tuple[int, float]:
        """
        Delete all audio media files in audio/processed/ to reclaim disk space.
        Leaves .gitkeep and README.md intact.
        Returns (deleted_count, freed_mb).
        """
        files = self._get_audio_files(self.processed_dir)
        total_bytes = sum(f.stat().st_size for f in files)
        freed_mb = round(total_bytes / (1024 * 1024), 2)

        if not dry_run:
            for f in files:
                f.unlink()

        return len(files), freed_mb
