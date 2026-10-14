#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Narrative & Verbatim Document Structuring Module
Generates standardized proofread.md documents with YAML frontmatter,
standardized disclaimer blockquotes, natural section structuring,
and scenario-specific structure validation.
"""

from enum import Enum
from pathlib import Path
import re
from typing import List, Optional, Tuple, Union

try:
    import opencc
    _OPENCC_S2TW = opencc.OpenCC('s2tw')
except Exception:
    _OPENCC_S2TW = None

BANNED_ASR_GARBLES = [
    "巨就是巨無安",
    "巨無安",
    "局無安",
    "推算兩百",
    "A A P I推算兩百",
    "我是黑俠",
    "西萬",
    "C萬",
    "C庫",
    "加洛妥",
    "西派神",
    "一日你十六字格",
    "稀土伺服器",
    "稀土中繼",
]

STRICT_SIMPLIFIED_CHARS = set(
    "误进现说话样个为关时对应该经过题动机与双阶状态设验证测试简报决沟广图变点导实总数论专写历学网络软体资讯检规则权构结语义认识类记录单头长线条级别组织门闪电师训练项页码据库环节点标签优处错逻辑迟频谱传输协议连计弯让请谢"
)

ALLOWED_TRADITIONAL_VARIANTS = {
    '里', '台', '后', '面', '么', '只', '准', '划', '干', '余', '板', '杰', '范', '谷', '松',
    '钟', '周', '表', '志', '云', '胡', '适', '占', '采', '签', '姜', '借', '庄', '喂', '扣',
    '并', '升', '系', '致', '别', '布', '帘', '沈', '党', '涂', '咸', '游', '筑', '秋', '仆',
    '朴', '累', '辟', '脏', '摺', '巨', '覆', '愿', '据', '瞭', '克', '回', '托', '制',
    '了', '注', '局', '卷', '念', '合', '杆', '欲', '才', '吃', '核', '羣', '群'
}


class ScenarioType(str, Enum):
    """
    Standard Scenario Profiles defined in PROOFREAD_RULES.md
    """
    CLASSROOM_LECTURE = "classroom-lecture"
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
        if self.scenario == ScenarioType.CLASSROOM_LECTURE:
            return (
                "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。"
                "完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動問答，**未做任何刪減或摘要縮寫**；"
                "已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語與標點符號，"
                "明確標註發言角色（授課講師／學員），並依授課脈絡劃分流暢之主題章節。"
            )
        elif self.scenario == ScenarioType.MULTI_PAPER:
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
            f'scenario: "{self.scenario.value if isinstance(self.scenario, ScenarioType) else self.scenario}"',
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

    # Check for artificial numbering in headings (e.g., "## 🎯 一、...")
    for h in headings:
        if re.search(r"^[^\w\s]*\s*[一二三四五六七八九十百]+[、\.]", h):
            errors.append(f"Heading contains artificial numeric prefix: '{h}'")

    if scenario_enum == ScenarioType.CLASSROOM_LECTURE:
        # Classroom lecture requires speaker attribution (授課講師)
        if not re.search(r"\*\*【授課講師】\*\*：", markdown_text):
            errors.append("classroom-lecture scenario requires mandatory '**【授課講師】**：' speaker attribution")

    elif scenario_enum == ScenarioType.MULTI_PAPER:
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

    # 5. Banned ASR Phonetic Garbles Guard
    errors.extend(validate_banned_asr_garbles(markdown_text))

    # 6. Traditional Chinese Guard
    errors.extend(validate_traditional_chinese(markdown_text))

    # 7. Mermaid Block Syntax Guard
    errors.extend(validate_mermaid_blocks(markdown_text))

    # 8. Speaker Semantic Consistency Guard
    errors.extend(validate_speaker_semantic_consistency(markdown_text, scenario_enum))

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_mermaid_blocks(markdown_text: str) -> List[str]:
    """
    Validates Mermaid diagram blocks inside Markdown text.
    Catches syntax errors such as:
    1. Node ID colliding with Subgraph ID (fatal Mermaid syntax error).
    2. Subgraph and 'end' balance.
    3. Valid diagram type header.
    """
    errors: List[str] = []
    blocks = re.findall(r"```mermaid\s*\n(.*?)\n```", markdown_text, flags=re.DOTALL)
    valid_diagram_types = (
        "flowchart", "graph", "sequenceDiagram", "classDiagram",
        "stateDiagram", "stateDiagram-v2", "erDiagram", "journey",
        "gantt", "pie", "quadrantChart", "gitGraph", "mindmap", "timeline"
    )
    for idx, block in enumerate(blocks, 1):
        lines = [line.strip() for line in block.splitlines() if line.strip() and not line.strip().startswith("%%")]
        if not lines:
            errors.append(f"Mermaid block #{idx} is empty")
            continue
        first_line = lines[0]
        if not any(first_line.startswith(t) for t in valid_diagram_types):
            errors.append(f"Mermaid block #{idx} missing valid diagram type: '{first_line}'")
            continue

        is_flowchart = first_line.startswith("flowchart") or first_line.startswith("graph")
        if is_flowchart:
            subgraph_ids = set()
            subgraph_count = 0
            end_count = 0
            for line in lines:
                m_sub = re.match(r"^subgraph\s+([A-Za-z0-9_\-]+)", line)
                if m_sub:
                    subgraph_ids.add(m_sub.group(1))
                    subgraph_count += 1
                elif line == "end" or line.startswith("end "):
                    end_count += 1

            if subgraph_count != end_count:
                errors.append(
                    f"Mermaid block #{idx} has mismatched subgraph ({subgraph_count}) vs end ({end_count})"
                )

            # Check for node IDs colliding with subgraph IDs
            for line in lines:
                if re.match(r"^subgraph\s+", line):
                    continue
                node_refs = re.findall(r"\b([A-Za-z0-9_\-]+)(?=\s*(?:\[|\(|\{|\>))", line)
                for node_id in node_refs:
                    if node_id in subgraph_ids:
                        errors.append(
                            f"Mermaid block #{idx} syntax error: Node ID '{node_id}' collides with Subgraph ID"
                        )
    return errors


def is_simplified_char(ch: str) -> bool:
    """
    Checks if a character is strictly Simplified Chinese.
    """
    return ch in STRICT_SIMPLIFIED_CHARS


def validate_traditional_chinese(markdown_text: str) -> List[str]:
    """
    Validates that the markdown text is in Traditional Chinese (Taiwan standard)
    and does not contain strictly Simplified Chinese characters.
    """
    errors: List[str] = []
    # Strip code blocks, inline code, links
    clean_text = re.sub(r"```.*?```", "", markdown_text, flags=re.DOTALL)
    clean_text = re.sub(r"`.*?`", "", clean_text)
    clean_text = re.sub(r"https?://\S+", "", clean_text)

    for line_no, line in enumerate(clean_text.splitlines(), 1):
        for ch in line:
            if is_simplified_char(ch):
                if ch == '据' and '拮据' in line:
                    continue
                errors.append(f"Line {line_no} contains Simplified Chinese character '{ch}'")
    return errors


def validate_banned_asr_garbles(markdown_text: str) -> List[str]:
    """
    Ensures known high-frequency ASR phonetic garble artifacts are eliminated.
    """
    errors: List[str] = []
    for garble in BANNED_ASR_GARBLES:
        if garble in markdown_text:
            errors.append(f"Found banned ASR phonetic garble: '{garble}'")
    return errors


def validate_speaker_semantic_consistency(
    markdown_text: str,
    scenario: Union[str, ScenarioType] = ScenarioType.SINGLE_TALK,
) -> List[str]:
    """
    Guards against speaker diarization inversion or role semantic contradiction.
    """
    errors: List[str] = []
    turns = re.findall(r"\*\*【(.*?)】\*\*：(.*?)(?=\n\n\*\*【|\Z)", markdown_text, flags=re.DOTALL)
    for speaker, speech in turns:
        speaker = speaker.strip()
        speech_snippet = speech[:80].strip().replace("\n", " ")
        # Student speaking with professor addressing student
        if "侑宸" in speaker or "研究生" in speaker:
            if re.search(r"(?:好[，、\s]+侑宸|侑宸你的|侑宸你這|我是指導教授|作為指導教授|我先講評)", speech):
                errors.append(
                    f"Speaker '{speaker}' contains dialogue characteristic of professor addressing student: '{speech_snippet}'"
                )
        # Professor or committee claiming to be student defending
        if any(role in speaker for role in ["指導教授", "口試委員", "評審委員"]):
            if re.search(r"(?:我的碩士論文題目是|我是侑宸|接下來由我進行論文報告)", speech):
                errors.append(
                    f"Speaker '{speaker}' contains dialogue characteristic of student speaker: '{speech_snippet}'"
                )
    return errors


def validate_summary_document(
    markdown_text: str,
    file_path: Optional[str] = None,
) -> Tuple[bool, List[str]]:
    """
    Validates executive summary (.md) document structure, including:
    - Presence of companion .full.md link.
    - Valid Mermaid blocks.
    - Traditional Chinese compliance.
    - No banned ASR garbles.
    - For Thesis-Progress summaries: presence of comparison matrix table.
    """
    errors: List[str] = []

    # 1. Companion link check
    if file_path and not file_path.endswith(".full.md") and not file_path.endswith("README.md"):
        stem = Path(file_path).stem
        full_name = f"{stem}.full.md"
        if f"{full_name}" not in markdown_text and "pending" not in markdown_text.lower():
            errors.append(f"Summary missing relative link to companion transcript '{full_name}'")

    # 2. Mermaid validation
    errors.extend(validate_mermaid_blocks(markdown_text))

    # 3. Traditional Chinese
    errors.extend(validate_traditional_chinese(markdown_text))

    # 4. Banned ASR garbles
    errors.extend(validate_banned_asr_garbles(markdown_text))

    # 5. Thesis Progress comparison table check
    if file_path and "Thesis-Progress" in file_path:
        has_table = any(line.strip().startswith("|") for line in markdown_text.splitlines())
        if not has_table:
            errors.append("Thesis-Progress summary requires a comparison matrix table")

    is_valid = len(errors) == 0
    return is_valid, errors
