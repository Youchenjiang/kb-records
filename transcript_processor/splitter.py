#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript Splitter Module
Provides automated, lossless splitting of mixed-scenario transcripts and summary notes
into standardized Option 3-A dual-tier deliverables (.full.md and .md).
"""

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union


@dataclass
class SplitSegmentConfig:
    """
    Configuration specification for a single split segment.
    """
    filename_base: str
    output_dir: Union[str, Path]
    title: str
    event: str
    scenario: str
    speakers: List[str]
    talk_id: str
    start_line: Optional[int] = None  # 1-indexed, inclusive
    end_line: Optional[int] = None    # 1-indexed, inclusive
    start_pattern: Optional[str] = None  # Regex pattern matching beginning header
    end_pattern: Optional[str] = None    # Regex pattern matching end boundary
    summary_start_line: Optional[int] = None
    summary_end_line: Optional[int] = None
    summary_key_takeaways: Optional[List[str]] = None


class TranscriptSplitter:
    """
    Splits multi-agenda or mixed-scenario transcripts into clean, independent deliverables.
    """

    def __init__(self, root_dir: Optional[Union[str, Path]] = None):
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()

    def parse_frontmatter_and_body(self, content: str) -> Tuple[Dict, str]:
        """
        Extracts YAML frontmatter dict and raw body text from markdown.
        """
        metadata = {}
        body = content
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            body = fm_match.group(2)
            for line in fm_text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key in ("speakers", "speaker"):
                        if val.startswith("[") and val.endswith("]"):
                            raw = val[1:-1].split(",")
                            metadata[key] = [s.strip().strip('"').strip("'") for s in raw if s.strip()]
                        elif val:
                            metadata[key] = [val]
                    else:
                        metadata[key] = val
        return metadata, body

    def inspect_sections(self, file_path: Union[str, Path]) -> List[Dict]:
        """
        Inspects headers (## ) and line ranges in a transcript to help users determine split points.
        """
        p = Path(file_path)
        content = p.read_text(encoding="utf-8")
        lines = content.splitlines()
        sections = []

        for i, line in enumerate(lines, start=1):
            if re.match(r"^##\s+(.*)$", line.strip()):
                sections.append({
                    "line": i,
                    "header": line.strip(),
                })
        return sections

    def split_transcript(
        self,
        full_md_path: Union[str, Path],
        segments: List[SplitSegmentConfig],
        summary_md_path: Optional[Union[str, Path]] = None,
    ) -> List[Tuple[Path, Optional[Path]]]:
        """
        Executes lossless splitting of full transcript and optional summary notes into segment deliverables.
        Returns list of (created_full_path, created_summary_path) pairs.
        """
        full_p = Path(full_md_path)
        if not full_p.exists():
            raise FileNotFoundError(f"Transcript file not found: {full_p}")

        full_content = full_p.read_text(encoding="utf-8")
        parent_meta, full_body = self.parse_frontmatter_and_body(full_content)
        full_lines = full_content.splitlines()

        summary_lines = []
        if summary_md_path:
            sum_p = Path(summary_md_path)
            if sum_p.exists():
                summary_lines = sum_p.read_text(encoding="utf-8").splitlines()

        created_files = []

        for seg in segments:
            # Determine content line range
            start_idx = 0
            end_idx = len(full_lines)

            if seg.start_line is not None:
                start_idx = seg.start_line - 1
            elif seg.start_pattern:
                for idx, line in enumerate(full_lines):
                    if re.search(seg.start_pattern, line):
                        start_idx = idx
                        break

            if seg.end_line is not None:
                end_idx = seg.end_line
            elif seg.end_pattern:
                for idx in range(start_idx + 1, len(full_lines)):
                    if re.search(seg.end_pattern, full_lines[idx]):
                        end_idx = idx
                        break

            # Extract segment content
            seg_body_lines = full_lines[start_idx:end_idx]

            # Filter out top-level parent headers if accidentally captured in body
            clean_body_lines = []
            for bl in seg_body_lines:
                if bl.startswith("# ") and "🎙️" in bl:
                    continue
                if bl.startswith("> **【排版與校對說明】**"):
                    continue
                clean_body_lines.append(bl)

            # Strip leading/trailing empty lines
            seg_body_text = "\n".join(clean_body_lines).strip()

            # Build YAML frontmatter
            date_val = parent_meta.get("date", "2026-01-01")
            speakers_repr = json.dumps(seg.speakers, ensure_ascii=False)
            speakers_str = " / ".join(seg.speakers)

            frontmatter = (
                f"---\n"
                f'title: "{seg.title}"\n'
                f'event: "{seg.event}"\n'
                f'date: "{date_val}"\n'
                f'talk_id: "{seg.talk_id}"\n'
                f"speakers: {speakers_repr}\n"
                f'type: "verbatim-narrative-transcript"\n'
                f"verbatim: true\n"
                f'scenario: "{seg.scenario}"\n'
                f"---\n\n"
            )

            header_block = (
                f"# 🎙️ {seg.talk_id} {seg.title} ({speakers_str})\n\n"
                f"> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。"
                f"本文件由混合錄音依研討脈絡精準獨立拆分，保留現場講者所有原話發言、語意轉折、現場問答與互動對話，**未做任何刪減或摘要縮寫**；"
                f"已全面修訂語音辨識錯字、專有名詞，並依演講敘事邏輯維持流暢之段落劃分。\n\n"
                f"---\n\n"
            )

            full_file_content = frontmatter + header_block + seg_body_text + "\n"

            # Destination paths
            out_dir = Path(seg.output_dir)
            if not out_dir.is_absolute():
                out_dir = self.root_dir / out_dir
            out_dir.mkdir(parents=True, exist_ok=True)

            target_full_path = out_dir / f"{seg.filename_base}.full.md"
            target_full_path.write_text(full_file_content, encoding="utf-8")

            # Handle summary note (.md)
            target_summary_path = None
            summary_content_text = ""

            if seg.summary_start_line is not None and seg.summary_end_line is not None and summary_lines:
                s_lines = summary_lines[seg.summary_start_line - 1 : seg.summary_end_line]
                summary_content_text = "\n".join(s_lines).strip()
            elif seg.summary_key_takeaways:
                takeaways_str = "\n".join(f"- {t}" for t in seg.summary_key_takeaways)
                summary_content_text = f"## 🎯 核心重點整理 (Key Takeaways)\n\n{takeaways_str}"

            if summary_content_text or summary_md_path:
                target_summary_path = out_dir / f"{seg.filename_base}.md"
                summary_header = (
                    f"# 🛡️ {seg.talk_id} {seg.title}\n\n\n"
                    f"> **研討主題**：{seg.title}  \n"
                    f"> **主講與對談**：{speakers_str}  \n"
                    f"> **所屬場合**：{seg.event}  \n"
                    f"> **關聯文件**：[📄 完整原話逐字稿 ({seg.filename_base}.full.md)](./{seg.filename_base}.full.md)\n\n"
                    f"---\n\n"
                )
                if not summary_content_text:
                    summary_content_text = (
                        f"## 🎯 研討核心摘述\n\n"
                        f"- 本章節自原始錄音場次獨立拆分，完整收錄針對「{seg.title}」之深度技術研析與討論。\n"
                        f"- 完整細節與原話問答請參閱同目錄對應逐字稿文件。\n"
                    )
                sum_full_content = summary_header + summary_content_text + "\n"
                target_summary_path.write_text(sum_full_content, encoding="utf-8")

            created_files.append((target_full_path, target_summary_path))

        return created_files
