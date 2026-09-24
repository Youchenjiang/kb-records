#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Transcript Pipeline Module
Coordinates cleaning, correction, proofreading, and summary generation.
"""

from typing import List, Optional, Tuple, Union
from pathlib import Path

from .cleaner import clean_transcript
from .corrector import CorrectionEngine
from .structurer import ProofreadBuilder
from .summarizer import SummaryBuilder


class TranscriptPipeline:
    """
    End-to-end pipeline coordinator.
    """

    def __init__(self, base_dir: Optional[Union[str, Path]] = None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.corrector = CorrectionEngine()

    def set_target_directory(self, category: str, event_folder: str) -> Path:
        """
        Resolve and ensure target directory: {base_dir}/{category}/{event_folder}
        """
        target = self.base_dir / category / event_folder
        target.mkdir(parents=True, exist_ok=True)
        return target

    def sanitize(self, raw_text: str, domains: Optional[List[str]] = None) -> str:
        """
        Step 1 & 2: Clean spaces and punctuation, then apply domain corrections.
        """
        cleaned = clean_transcript(raw_text)
        corrected = self.corrector.correct(cleaned, domains=domains)
        return corrected

    def export_proofread(
        self,
        output_dir: Path,
        talk_id: str,
        short_title: str,
        title: str,
        event: str,
        speakers: Union[str, List[str]],
        sections: List[Tuple[str, str]],
        emoji: str = "🎙️",
    ) -> Path:
        """
        Generate and save {ID}-{ShortTitle}-proofread.md
        """
        builder = ProofreadBuilder(
            title=title,
            event=event,
            talk_id=talk_id,
            speakers=speakers,
            emoji=emoji,
        )
        for heading, body in sections:
            builder.add_section(heading, body)

        content = builder.render()
        file_path = output_dir / f"{talk_id}-{short_title}-proofread.md"
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def export_summary(
        self,
        output_dir: Path,
        talk_id: str,
        short_title: str,
        summary_builder: SummaryBuilder,
    ) -> Path:
        """
        Generate and save {ID}-{ShortTitle}-summary.md
        """
        content = summary_builder.render()
        file_path = output_dir / f"{talk_id}-{short_title}-summary.md"
        file_path.write_text(content, encoding="utf-8")
        return file_path
