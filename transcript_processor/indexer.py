#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Catalog Indexer Module
Scans the repository for proofread.md and summary.md transcripts,
extracts metadata, and generates unified, auto-updated CATALOG.md and CATALOG.zh-TW.md files.
"""

from dataclasses import dataclass, field
from datetime import datetime
import os
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union


@dataclass
class CatalogItem:
    """
    Metadata representation of an indexed transcript session.
    """
    title: str
    category: str
    event: str
    date: str
    speakers: List[str]
    scenario: str
    proofread_path: Path
    summary_path: Optional[Path] = None
    tags: List[str] = field(default_factory=list)


class CatalogIndexer:
    """
    Automated scanner and markdown catalog generator.
    """

    EXCLUDED_DIRS = {
        ".git",
        ".github",
        ".vscode",
        ".idea",
        ".pytest_cache",
        "__pycache__",
        "venv",
        ".venv",
        "node_modules",
        "transcribe_outputs",
        "tests",
    }

    def __init__(self, root_dir: Optional[Union[str, Path]] = None):
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()

    def scan(self) -> List[CatalogItem]:
        """
        Scan repository directory tree for all proofread.md files and match summaries.
        """
        items: List[CatalogItem] = []

        for p_file in self.root_dir.glob("**/*proofread*.md"):
            # Check exclusions
            parts = p_file.parts
            if any(excluded in parts for excluded in self.EXCLUDED_DIRS):
                continue
            if p_file.name == "PROOFREAD_RULES.md":
                continue

            rel_p = p_file.relative_to(self.root_dir)
            content = p_file.read_text(encoding="utf-8")
            metadata = self._parse_metadata(p_file, content, rel_p)

            # Match summary
            summary_path = None
            if p_file.name == "proofread.md":
                cand = p_file.parent / "summary.md"
                if cand.exists():
                    summary_path = cand.relative_to(self.root_dir)
            elif p_file.name.endswith("-proofread.md"):
                prefix = p_file.name[:-len("-proofread.md")]
                cand = p_file.parent / f"{prefix}-summary.md"
                if cand.exists():
                    summary_path = cand.relative_to(self.root_dir)

            item = CatalogItem(
                title=metadata["title"],
                category=metadata["category"],
                event=metadata["event"],
                date=metadata["date"],
                speakers=metadata["speakers"],
                scenario=metadata["scenario"],
                proofread_path=rel_p,
                summary_path=summary_path,
                tags=metadata["tags"],
            )
            items.append(item)

        # Sort items by category, event, and title
        items.sort(key=lambda x: (x.category, x.event, x.title))
        return items

    def _parse_metadata(self, path: Path, content: str, rel_path: Path) -> Dict:
        """
        Extract metadata from YAML frontmatter or fallback to heuristic parsing.
        """
        data = {
            "title": "",
            "category": "Uncategorized",
            "event": "Unknown",
            "date": "",
            "speakers": ["講者"],
            "scenario": "single-talk",
            "tags": [],
        }

        # Determine category from first path component
        parts = rel_path.parts
        if len(parts) > 1:
            data["category"] = parts[0]
            if len(parts) > 2:
                data["event"] = parts[1]

        # Extract YAML Frontmatter
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            for line in fm_text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key == "title":
                        data["title"] = val
                    elif key == "event":
                        data["event"] = val
                    elif key == "date":
                        data["date"] = val
                    elif key == "category":
                        data["category"] = val
                    elif key == "scenario":
                        data["scenario"] = val
                    elif key in ("speakers", "speaker"):
                        # Support [A, B] or single
                        if val.startswith("[") and val.endswith("]"):
                            raw_speakers = val[1:-1].split(",")
                            data["speakers"] = [s.strip().strip('"').strip("'") for s in raw_speakers if s.strip()]
                        elif val:
                            data["speakers"] = [val]

        # Fallback for title and speaker
        h1_line_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
        if h1_line_match:
            full_h1 = h1_line_match.group(1).strip()
            # Check for parenthesized speaker at the end
            paren_match = re.search(r"\(([^)]+)\)\s*$", full_h1)
            if paren_match and (not data["speakers"] or data["speakers"] == ["講者"]):
                spk_cand = paren_match.group(1).strip()
                if not any(spk_cand.startswith(p) for p in ["指導", "中央", "錄音"]):
                    data["speakers"] = [spk_cand]

            if not data["title"]:
                # Clean title
                clean_title = re.sub(r"^(?:🎙️|🔬|🛡️|📑|\d+)\s*", "", full_h1)
                clean_title = re.sub(r"\([^)]+\)\s*$", "", clean_title).strip()
                data["title"] = clean_title or full_h1

        if not data["title"]:
            data["title"] = path.stem.replace("-proofread", "")

        # Fallback date from event or path
        if not data["date"]:
            date_match = re.search(r"(\d{4}[-_]?\d{2}[-_]?\d{2})", str(rel_path))
            if date_match:
                raw_d = date_match.group(1).replace("_", "-")
                if len(raw_d) == 8 and raw_d.isdigit():
                    data["date"] = f"{raw_d[:4]}-{raw_d[4:6]}-{raw_d[6:8]}"
                else:
                    data["date"] = raw_d

        # Fallback scenario inference if not explicitly provided in frontmatter
        fm_has_scenario = fm_match and ("scenario:" in fm_match.group(1))
        if not fm_has_scenario:
            search_str = f"{rel_path} {data['title']} {data['event']}"
            if any(k in search_str for k in ["MasterDefense", "口試", "碩士學位", "審查質詢", "thesis-defense"]):
                data["scenario"] = "thesis-defense"
            elif any(k in search_str for k in ["AcademicConference", "研討會", "Session G", "Session H", "Session I", "multi-paper"]):
                data["scenario"] = "multi-paper"
            elif any(k in search_str for k in ["閃電秀", "lightning"]):
                data["scenario"] = "lightning-talks"
            else:
                data["scenario"] = "single-talk"

        # Entity Provenance Sanity Check
        from .entity_guard import EntityGuard
        data = EntityGuard.sanitize_metadata(data, content)

        return data


    def generate_markdown(self, items: List[CatalogItem], lang: str = "zh-TW") -> str:
        """
        Render a structured markdown catalog document.
        """
        is_zh = (lang == "zh-TW")
        today = datetime.now().strftime("%Y-%m-%d")

        if is_zh:
            title = "# 📑 Record List 全局會議、演講與逐字稿目錄索引"
            banner = f"> **自動化索引聲明**：本目錄由 `transcript_processor.indexer` 於 `{today}` 自動掃描產生，收錄全庫已完成之雙交付版本文件。"
            col_no = "序號"
            col_topic = "演講主題 / 論文名稱"
            col_speakers = "講者 / 發表人"
            col_scenario = "場景規範"
            col_links = "雙版本連結"
            toc_title = "## 🧭 分類快速導航"
        else:
            title = "# 📑 Record List - Master Catalog of Transcripts & Summaries"
            banner = f"> **Auto-Generated Index**: Automatically generated by `transcript_processor.indexer` on `{today}`. Indexes all production-grade proofread & summary deliverables across the repository."
            col_no = "No."
            col_topic = "Session Topic / Paper Title"
            col_speakers = "Speaker(s)"
            col_scenario = "Scenario"
            col_links = "Deliverable Links"
            toc_title = "## 🧭 Quick Category Navigation"

        # Group by category then event
        categories: Dict[str, Dict[str, List[CatalogItem]]] = {}
        for item in items:
            cat = item.category
            ev = item.event
            if cat not in categories:
                categories[cat] = {}
            if ev not in categories[cat]:
                categories[cat][ev] = []
            categories[cat][ev].append(item)

        lines = [
            title,
            "",
            banner,
            "",
            toc_title,
            "",
        ]

        # TOC
        for cat in categories.keys():
            lines.append(f"- [{cat}](#{cat.lower()})")
            for ev in categories[cat].keys():
                lines.append(f"  - [{ev}](#{ev.lower()})")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Content
        global_idx = 1
        for cat, events in categories.items():
            lines.append(f"## 🗂️ {cat}")
            lines.append("")

            for ev, ev_items in events.items():
                lines.append(f"### 📅 {ev}")
                lines.append("")
                lines.append(f"| {col_no} | {col_topic} | {col_speakers} | {col_scenario} | {col_links} |")
                lines.append("| :--- | :--- | :--- | :--- | :--- |")

                for it in ev_items:
                    speakers_str = ", ".join(it.speakers)
                    proofread_rel = str(it.proofread_path).replace("\\", "/")
                    proof_link = f"[📄 Proofread](./{proofread_rel})"
                    summary_link = ""
                    if it.summary_path:
                        sum_rel = str(it.summary_path).replace("\\", "/")
                        summary_link = f" · [📑 Summary](./{sum_rel})"

                    links_col = f"{proof_link}{summary_link}"
                    lines.append(f"| {global_idx} | **{it.title}** | {speakers_str} | `{it.scenario}` | {links_col} |")
                    global_idx += 1

                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines).strip() + "\n"

    def update_catalog_files(
        self,
        output_en: Path = Path("CATALOG.md"),
        output_zh: Path = Path("CATALOG.zh-TW.md"),
    ) -> Tuple[int, Path, Path]:
        """
        Scan repository and update both CATALOG.md and CATALOG.zh-TW.md.
        """
        items = self.scan()
        zh_content = self.generate_markdown(items, lang="zh-TW")
        en_content = self.generate_markdown(items, lang="en")

        out_zh_path = self.root_dir / output_zh
        out_en_path = self.root_dir / output_en

        out_zh_path.write_text(zh_content, encoding="utf-8")
        out_en_path.write_text(en_content, encoding="utf-8")

        return len(items), out_en_path, out_zh_path

