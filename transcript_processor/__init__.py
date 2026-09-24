"""
Transcript Processor Toolkit
A modular, extensible pipeline for processing speech-to-text (ASR) transcripts
into verbatim proofread documents and executive summaries.
"""

from .cleaner import clean_cjk_spaces, normalize_punctuation, clean_transcript
from .corrector import CorrectionEngine, DomainDict
from .structurer import ProofreadBuilder, format_verbatim_document
from .summarizer import SummaryBuilder, MermaidDiagram
from .pipeline import TranscriptPipeline

__all__ = [
    "clean_cjk_spaces",
    "normalize_punctuation",
    "clean_transcript",
    "CorrectionEngine",
    "DomainDict",
    "ProofreadBuilder",
    "format_verbatim_document",
    "SummaryBuilder",
    "MermaidDiagram",
    "TranscriptPipeline",
]
