#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Narrative & Verbatim Document Structuring Module
Generates standardized proofread.md documents with YAML frontmatter,
standardized disclaimer blockquotes, natural section structuring,
and scenario-specific structure validation.
"""

from enum import Enum
import re
from typing import List, Optional, Tuple, Union


class ScenarioType(str, Enum):
    """
    Standard Scenario Profiles defined in PROOFREAD_RULES.md
    """
    SINGLE_TALK = "single-talk"
    MULTI_PAPER = "multi-paper"
    THESIS_DEFENSE = "thesis-defense"
    LIGHTNING_TALKS = "lightning-talks"


class ProofreadBuilder:
    """
    Builder for 100% verbatim proofread markdown documents with scenario adaptation.
    """

    def __init__(
        self,
        title: str,
        event: str,
        talk_id: Optional[str] = None,
        speakers: Union[str, List[str]] = "講者",
        emoji: str = "🎙️",
        scenario: Union[str, ScenarioType] = ScenarioType.SINGLE_TALK,
    ):
        self.title = title
        self.event = event
        self.talk_id = talk_id or ""
        if isinstance(speakers, str):
            self.speakers = [speakers]
        else:
            self.speakers = speakers
        self.emoji = emoji
        if isinstance(scenario, str):
            try:
                self.scenario = ScenarioType(scenario)
            except ValueError:
                self.scenario = ScenarioType.SINGLE_TALK
        else:
            self.scenario = scenario
        self.sections: List[Tuple[str, str]] = []

    def add_section(self, heading: str, content: str) -> "ProofreadBuilder":
        """
        Add a logical section with a Markdown heading and paragraph body.
        """
        clean_content = content.strip()
        self.sections.append((heading, clean_content))
        return self

    def _get_disclaimer(self) -> str:
        """
        Return the standardized disclaimer blockquote adapted to the scenario profile.
        """
        if self.scenario == ScenarioType.MULTI_PAPER:
            return (
                "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。"
                "完整收錄現場所有講者原話發言、語意轉折、現場互動、提問質詢、答辯攻防與評定決議，**未做任何刪減、摘要或人工造假注入**；"
                "已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、術語縮寫與標點符號，"
                "明確標註發言角色（口試委員／指導教授／研究生／發表人／大會司儀），並完成舒適流暢的段落劃分與主題標題標註。"
            )
        elif self.scenario == ScenarioType.THESIS_DEFENSE:
            return (
                "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。"
                "完整收錄口試現場所有講者原話發言、語意轉折、現場互動、提問質詢、答辯攻防與評定決議，**未做任何刪減、摘要或人工造假注入**；"
                "已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、術語縮寫與標點符號，"
                "明確標註發言角色（召集人／指導教授／口試委員／研究生），並完成舒適流暢的段落劃分與主題標題標註。"
            )
        else:
            return (
                "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。"
                "保留講者所有原話發言、語意轉折、現場互動對話、幕後故事與問答，**未做任何刪減或摘要縮寫**；"
                "已全面修訂語音辨識錯字、同音字與專有名詞，並依演講敘事邏輯完成流暢的段落劃分與主題標題標註。"
            )

    def render(self) -> str:
        """
        Render the complete Markdown document according to PROOFREAD_RULES.md.
        """
        speakers_str = ", ".join([f'"{s}"' for s in self.speakers])
        speaker_display = " / ".join(self.speakers)
        header_title = f"{self.talk_id} {self.title}".strip()

        frontmatter_lines = [
            "---",
            f'title: "{self.title}"',
            f'event: "{self.event}"',
        ]
        if self.talk_id:
            frontmatter_lines.append(f'talk_id: "{self.talk_id}"')
        frontmatter_lines.extend([
            f"speakers: [{speakers_str}]",
            'type: "verbatim-narrative-transcript"',
            "verbatim: true",
            "---",
        ])

        lines = frontmatter_lines + [
            "",
            f"# {self.emoji} {header_title} ({speaker_display})",
            "",
            self._get_disclaimer(),
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
    scenario: Union[str, ScenarioType] = ScenarioType.SINGLE_TALK,
) -> str:
    """
    Convenience function to build a verbatim document in a single call.
    """
    builder = ProofreadBuilder(title, event, talk_id, speakers, emoji, scenario=scenario)
    for h, c in sections:
        builder.add_section(h, c)
    return builder.render()


def validate_transcript_structure(
    markdown_text: str,
    scenario: Union[str, ScenarioType] = ScenarioType.SINGLE_TALK,
) -> Tuple[bool, List[str]]:
    """
    Validate a proofread Markdown document against the rules in PROOFREAD_RULES.md.
    Returns (is_valid, list_of_errors).
    """
    errors: List[str] = []
    
    if isinstance(scenario, str):
        try:
            scenario_enum = ScenarioType(scenario)
        except ValueError:
            scenario_enum = ScenarioType.SINGLE_TALK
    else:
        scenario_enum = scenario

    # 1. Frontmatter Validation
    if not markdown_text.startswith("---"):
        errors.append("Missing opening YAML frontmatter delimiter '---'")
    else:
        fm_end = markdown_text.find("---", 3)
        if fm_end == -1:
            errors.append("Missing closing YAML frontmatter delimiter '---'")
        else:
            fm_content = markdown_text[3:fm_end]
            if "title:" not in fm_content:
                errors.append("YAML frontmatter missing 'title' field")
            if "event:" not in fm_content:
                errors.append("YAML frontmatter missing 'event' field")
            if "speakers:" not in fm_content:
                errors.append("YAML frontmatter missing 'speakers' field")
            if 'type: "verbatim-narrative-transcript"' not in fm_content and "type: 'verbatim-narrative-transcript'" not in fm_content:
                errors.append("YAML frontmatter missing or invalid 'type' field")
            if "verbatim: true" not in fm_content:
                errors.append("YAML frontmatter missing 'verbatim: true'")

    # 2. Disclaimer Blockquote
    if "> **【排版與校對說明】**" not in markdown_text:
        errors.append("Missing standardized disclaimer blockquote '> **【排版與校對說明】**'")

    # 3. Zero Hallucination Checks (Banned artifact phrases)
    banned_hallucinations = ["呃呃呃！", "假的Q&A", "（此處插入對話）"]
    for phrase in banned_hallucinations:
        if phrase in markdown_text:
            errors.append(f"Found banned hallucinated artifact phrase: '{phrase}'")

    # 4. Scenario-Specific Structure Checks
    headings = re.findall(r"^##\s+(.+)$", markdown_text, flags=re.MULTILINE)

    if scenario_enum == ScenarioType.MULTI_PAPER:
        # Check for multiple paper sections
        paper_headings = [h for h in headings if "論文" in h]
        if len(paper_headings) < 2:
            errors.append(f"multi-paper scenario requires at least 2 paper sections, found {len(paper_headings)}")
        # Check for Q&A / Reviewer comment sections
        qa_headings = [h for h in headings if any(k in h for k in ["講評", "Q&A", "問答", "質詢"])]
        if len(qa_headings) < 1:
            errors.append("multi-paper scenario requires Q&A or reviewer comment sections (講評/Q&A/問答)")

    elif scenario_enum == ScenarioType.THESIS_DEFENSE:
        # Check for committee / defense markers
        defense_markers = ["委員", "教授", "研究生", "答辯", "口試", "召集人"]
        has_defense_markers = any(m in markdown_text for m in defense_markers)
        if not has_defense_markers:
            errors.append("thesis-defense scenario requires defense dialogue/committee markers")

    elif scenario_enum == ScenarioType.LIGHTNING_TALKS:
        lightning_headings = [h for h in headings if "閃電秀" in h]
        if len(lightning_headings) < 2 and len(headings) < 2:
            errors.append("lightning-talks scenario requires multiple short talk sections")

    is_valid = len(errors) == 0
    return is_valid, errors
