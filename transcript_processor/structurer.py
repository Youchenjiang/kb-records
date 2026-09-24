#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Narrative & Verbatim Document Structuring Module
Generates standardized proofread.md documents with YAML frontmatter,
standardized disclaimer blockquotes, and natural section structuring.
"""

from typing import List, Optional, Tuple, Union


class ProofreadBuilder:
    """
    Builder for 100% verbatim proofread markdown documents.
    """

    def __init__(
        self,
        title: str,
        event: str,
        talk_id: str,
        speakers: Union[str, List[str]],
        emoji: str = "🎙️",
    ):
        self.title = title
        self.event = event
        self.talk_id = talk_id
        if isinstance(speakers, str):
            self.speakers = [speakers]
        else:
            self.speakers = speakers
        self.emoji = emoji
        self.sections: List[Tuple[str, str]] = []

    def add_section(self, heading: str, content: str) -> "ProofreadBuilder":
        """
        Add a logical section with a Markdown heading and paragraph body.
        """
        clean_content = content.strip()
        self.sections.append((heading, clean_content))
        return self

    def render(self) -> str:
        """
        Render the complete Markdown document according to PROOFREAD_RULES.md.
        """
        speakers_str = ", ".join([f'"{s}"' for s in self.speakers])
        speaker_display = " / ".join(self.speakers)

        lines = [
            "---",
            f'title: "{self.title}"',
            f'event: "{self.event}"',
            f'talk_id: "{self.talk_id}"',
            f"speakers: [{speakers_str}]",
            'type: "verbatim-narrative-transcript"',
            "verbatim: true",
            "---",
            "",
            f"# {self.emoji} {self.talk_id} {self.title} ({speaker_display})",
            "",
            "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。"
            "保留講者所有原話發言、語意轉折、現場互動對話、幕後故事與問答，**未做任何刪減或摘要縮寫**；"
            "已全面修訂語音辨識錯字、同音字與專有名詞，並依演講敘事邏輯完成流暢的段落劃分與主題標題標註。",
            "",
            "---",
            "",
        ]

        for heading, body in self.sections:
            if not heading.startswith("#"):
                heading = f"## {heading}"
            lines.append(heading)
            lines.append("")
            lines.append(body)
            lines.append("")

        return "\n".join(lines).strip() + "\n"


def format_verbatim_document(
    title: str,
    event: str,
    talk_id: str,
    speakers: Union[str, List[str]],
    sections: List[Tuple[str, str]],
    emoji: str = "🎙️",
) -> str:
    """
    Convenience function to build a verbatim document in a single call.
    """
    builder = ProofreadBuilder(title, event, talk_id, speakers, emoji)
    for h, c in sections:
        builder.add_section(h, c)
    return builder.render()
