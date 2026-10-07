#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reformat all 6 deliverables to paragraph-by-paragraph bilingual alignment:
Combines consecutive turns by the same speaker into cohesive natural paragraphs (3-6 sentences),
followed by a full, fluent Traditional Chinese translated paragraph.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import validate_transcript_structure

TARGET_FILES = [
    (REPO_ROOT / "5-Master/2-Second-Year/Fall-Semester/20260912-AWS-CloudTrail-DuckDB-Detection/20260912-AWS-CloudTrail偵測工程與DuckDB-SigmaHQ本地威脅狩獵.full.md", "single-talk"),
    (REPO_ROOT / "5-Master/2-Second-Year/Fall-Semester/20260912-SNES-Mario-ACE-Exploit/20260912-超級瑪利歐世界-SNES任意代碼執行ACE記憶體漏洞逆向解析.full.md", "single-talk"),
    (REPO_ROOT / "5-Master/2-Second-Year/Fall-Semester/2026-Managerial-Communication/20260910-管理溝通-Week01-課程導論與組織管理溝通.full.md", "classroom-lecture"),
    (REPO_ROOT / "5-Master/2-Second-Year/Fall-Semester/2026-Managerial-Communication/20260917-管理溝通-Week02-專業定位與學員英語自介發表.full.md", "classroom-lecture"),
    (REPO_ROOT / "5-Master/2-Second-Year/Fall-Semester/2026-Managerial-Communication/20260924-管理溝通-Week03-科技與商務決策溝通.full.md", "classroom-lecture"),
    (REPO_ROOT / "5-Master/2-Second-Year/Fall-Semester/2026-Managerial-Communication/20261001-管理溝通-Week04-受眾分析與簡報結構設計.full.md", "classroom-lecture"),
]


def clean_zh_join(sentences):
    text = " ".join([s.strip() for s in sentences if s.strip()])
    # Remove spaces between Chinese characters and punctuation, but preserve around ASCII
    text = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', text)
    return text


def consolidate_section_turns(body_text, scenario="single-talk", min_chars=320):
    """
    Parse existing turns in body_text and merge into rich paragraphs.
    """
    # Pattern to match: **[【]Speaker[】]**[:：] English \n\n> **繁中翻譯**： Chinese
    turn_pattern = re.compile(
        r'\*\*【?([^\*【】]+)】?\*\*[:：]\s*(.*?)\n\n>\s*\*\*繁中翻譯\*\*：\s*(.*?)(?=\n\n\*\*|\n\n##|$)',
        re.DOTALL
    )
    matches = list(turn_pattern.finditer(body_text))
    if not matches:
        return body_text

    turns = []
    for m in matches:
        spk = m.group(1).strip()
        en = m.group(2).strip()
        zh = m.group(3).strip()
        turns.append((spk, en, zh))

    consolidated = []
    curr_speaker = None
    curr_en = []
    curr_zh = []
    curr_en_len = 0

    for spk, en, zh in turns:
        # If speaker changed, flush
        if curr_speaker is not None and spk != curr_speaker:
            en_p = " ".join(curr_en)
            zh_p = clean_zh_join(curr_zh)
            consolidated.append((curr_speaker, en_p, zh_p))
            curr_speaker = spk
            curr_en = [en]
            curr_zh = [zh]
            curr_en_len = len(en)
            continue

        if curr_speaker is None:
            curr_speaker = spk

        curr_en.append(en)
        curr_zh.append(zh)
        curr_en_len += len(en)

        # Flush if paragraph has reached substantive length and ends with punctuation
        if curr_en_len >= min_chars and en.rstrip().endswith(('.', '?', '!', '。', '？', '！')):
            en_p = " ".join(curr_en)
            zh_p = clean_zh_join(curr_zh)
            consolidated.append((curr_speaker, en_p, zh_p))
            curr_speaker = None
            curr_en = []
            curr_zh = []
            curr_en_len = 0

    if curr_en:
        en_p = " ".join(curr_en)
        zh_p = clean_zh_join(curr_zh)
        consolidated.append((curr_speaker, en_p, zh_p))

    # Reformat into markdown
    formatted_paras = []
    for spk, en_p, zh_p in consolidated:
        if scenario == "classroom-lecture":
            prefix = f"**【{spk}】**："
        else:
            prefix = f"**{spk}**:"
        para_md = f"{prefix} {en_p}\n\n> **繁中翻譯**：{zh_p}"
        formatted_paras.append(para_md)

    return "\n\n".join(formatted_paras)


def process_file(file_path: Path, scenario: str):
    print(f"Processing {file_path.name} ({scenario})...")
    content = file_path.read_text(encoding="utf-8")

    # Split header part and section parts
    # Sections start with '## '
    parts = re.split(r'\n(?=## )', content)
    header_part = parts[0]
    section_parts = parts[1:]

    new_sections = []
    for sec in section_parts:
        lines = sec.split("\n", 1)
        heading = lines[0]
        body = lines[1] if len(lines) > 1 else ""

        reformatted_body = consolidate_section_turns(body, scenario=scenario)
        new_sec_text = f"{heading}\n\n{reformatted_body.strip()}\n"
        new_sections.append(new_sec_text)

    new_full_content = header_part.rstrip() + "\n\n" + "\n".join(new_sections).strip() + "\n"

    # Validate structure
    is_valid, errors = validate_transcript_structure(new_full_content, scenario=scenario)
    if not is_valid:
        raise ValueError(f"Validation failed for {file_path.name}: {errors}")

    file_path.write_text(new_full_content, encoding="utf-8")
    print(f"  [OK] Successfully reformatted and validated {file_path.name}")


if __name__ == "__main__":
    for fpath, sc in TARGET_FILES:
        process_file(fpath, sc)
    print("\n🎉 All target transcripts reformatted to paragraph-by-paragraph bilingual alignment!")
