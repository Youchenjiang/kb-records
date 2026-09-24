#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executive Summary & Technical Digest Generator Module
Produces structured summary.md documents adhering to PROOFREAD_RULES.md,
including Mermaid flowcharts, metadata blocks, and technical deep-dives.
"""

from typing import List, Optional, Tuple, Union


class MermaidDiagram:
    """
    Helper for assembling valid Mermaid code blocks.
    """

    def __init__(self, chart_type: str = "flowchart TD"):
        self.chart_type = chart_type
        self.statements: List[str] = []

    def add(self, statement: str) -> "MermaidDiagram":
        self.statements.append(statement)
        return self

    def render(self) -> str:
        lines = [f"```{self.chart_type}"]
        for stmt in self.statements:
            lines.append(f"    {stmt}")
        lines.append("```")
        return "\n".join(lines)


class SummaryBuilder:
    """
    Builder for structured technical summary documents.
    """

    def __init__(
        self,
        talk_id: str,
        title: str,
        speaker: str,
        topic: str,
        tech_stack: str,
        outcome: str,
        emoji: str = "📑",
    ):
        self.talk_id = talk_id
        self.title = title
        self.speaker = speaker
        self.topic = topic
        self.tech_stack = tech_stack
        self.outcome = outcome
        self.emoji = emoji
        self.mermaid_diagram: Optional[str] = None
        self.overview_content: Optional[str] = None
        self.sections: List[Tuple[str, str]] = []
        self.takeaways: List[str] = []

    def set_diagram(self, diagram: Union[str, MermaidDiagram], section_title: str = "🎯 核心概念與技術架構") -> "SummaryBuilder":
        if isinstance(diagram, MermaidDiagram):
            self.mermaid_diagram = diagram.render()
        else:
            self.mermaid_diagram = diagram.strip()
        self.overview_heading = section_title
        return self

    def set_overview(self, text: str) -> "SummaryBuilder":
        self.overview_content = text.strip()
        return self

    def add_section(self, heading: str, body: str) -> "SummaryBuilder":
        self.sections.append((heading, body.strip()))
        return self

    def add_takeaway(self, takeaway: str) -> "SummaryBuilder":
        self.takeaways.append(takeaway.strip())
        return self

    def render(self) -> str:
        lines = [
            f"# {self.emoji} {self.talk_id} {self.title} ({self.speaker})",
            "",
            f"> **演講主題**：{self.topic}  ",
            f"> **講者**：{self.speaker}  ",
            f"> **關鍵技術**：{self.tech_stack}  ",
            f"> **核心成果 / 價值**：{self.outcome}",
            "",
            "---",
            "",
        ]

        if self.mermaid_diagram or self.overview_content:
            heading = getattr(self, "overview_heading", "🎯 核心概念與技術架構")
            if not heading.startswith("#"):
                heading = f"## {heading}"
            lines.append(heading)
            lines.append("")
            if self.mermaid_diagram:
                lines.append(self.mermaid_diagram)
                lines.append("")
            if self.overview_content:
                lines.append(self.overview_content)
                lines.append("")
            lines.append("---")
            lines.append("")

        for heading, body in self.sections:
            if not heading.startswith("#"):
                heading = f"## {heading}"
            lines.append(heading)
            lines.append("")
            lines.append(body)
            lines.append("")
            lines.append("---")
            lines.append("")

        if self.takeaways:
            lines.append("## 💡 關鍵總結與啟示")
            lines.append("")
            for idx, item in enumerate(self.takeaways, start=1):
                lines.append(f"{idx}. {item}")
            lines.append("")

        return "\n".join(lines).strip() + "\n"
