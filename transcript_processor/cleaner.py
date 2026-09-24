#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Normalization & Sanitization Module
Cleans CJK whitespace anomalies, normalizes punctuation, and preserves code/alphanumeric tokens.
"""

import re

CJK_REGEX = r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]"
CJK_PUNC_REGEX = r"[，。！？、；：「」『』（）—…《》〈〉“”‘’]"


def clean_cjk_spaces(text: str) -> str:
    """
    Remove spurious spaces between CJK characters and between CJK characters and CJK punctuation,
    while carefully preserving single spaces between alphanumeric words.
    """
    # Collapse multiple spaces between CJK characters
    for _ in range(8):
        text = re.sub(rf"({CJK_REGEX})\s+({CJK_REGEX})", r"\1\2", text)

    # Collapse spaces between CJK characters and punctuation
    for _ in range(4):
        text = re.sub(rf"({CJK_REGEX})\s+({CJK_PUNC_REGEX})", r"\1\2", text)
        text = re.sub(rf"({CJK_PUNC_REGEX})\s+({CJK_REGEX})", r"\1\2", text)
        text = re.sub(rf"({CJK_PUNC_REGEX})\s+({CJK_PUNC_REGEX})", r"\1\2", text)

    # Normalize spacing between Alphanumeric and CJK
    text = re.sub(rf"([a-zA-Z0-9_])\s+({CJK_REGEX})", r"\1 \2", text)
    text = re.sub(rf"({CJK_REGEX})\s+([a-zA-Z0-9_])", r"\1 \2", text)

    # Collapse consecutive whitespace
    text = re.sub(r"[ \t]+", " ", text).strip()
    return text


def normalize_punctuation(text: str) -> str:
    """
    Convert half-width punctuation attached to CJK characters into standardized full-width forms.
    """
    text = re.sub(rf"({CJK_REGEX})\s*,\s*", r"\1，", text)
    text = re.sub(rf"({CJK_REGEX})\s*\.\s*", r"\1。", text)
    text = re.sub(rf"({CJK_REGEX})\s*;\s*", r"\1；", text)
    text = re.sub(rf"({CJK_REGEX})\s*:\s*", r"\1：", text)
    text = re.sub(rf"({CJK_REGEX})\s*\?\s*", r"\1？", text)
    text = re.sub(rf"({CJK_REGEX})\s*!\s*", r"\1！", text)
    return text


def clean_transcript(text: str) -> str:
    """
    Complete sanitization pipeline for raw ASR text.
    """
    cleaned = clean_cjk_spaces(text)
    normalized = normalize_punctuation(cleaned)
    return clean_cjk_spaces(normalized)
