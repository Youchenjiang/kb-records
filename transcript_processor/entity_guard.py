#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entity Guard & Proper Noun Verification Module
Provides candidate entity extraction, title/role association,
homophone clustering, and interactive verification table generation.
"""

from typing import Dict, List, Optional, Set, Tuple
import re
from collections import Counter


ROLE_PREFIX_PATTERNS = [
    r"(?:指導教授|口試委員|口試主持|口試主席|評審委員|大會司儀|發表者|報告者|報告人|發表人|主持人|引言人|主席)[\s：:、]*([^\s，。、！？\(\)（）\d:：]{2,3})(?=(?:教授|博士|老師|同學|學長|學姊|委員|[\s，。、！？]|$))",
    r"我是\s*([^\s，。、！？\(\)（）\d:：]{2,3})(?=(?:同學|[\s，。、！？]|$))",
    r"([^\s，。、！？\(\)（）\d:：]{2,3})(?:教授|博士|老師|學長|學姊|同學)",
]

TITLE_KEYWORDS = [
    "指導教授", "口試委員", "評審委員", "口試主持", "大會司儀",
    "發表者", "報告者", "報告人", "發表人", "主持人", "引言人",
    "教授", "博士", "老師", "學長", "學姊", "同學", "主席",
]

TITLE_AFFIX_CHARS = "教授博士老師同學學長學姊委員主席司儀"

INSTITUTION_PATTERNS = [
    r"[\u4e00-\u9fa5]{2,12}(?:大學|科技大學|技術學院|專科學校|研究所|學系|資訊工程系|資管系|電機系|研究中心|實驗室)",
]


class EntityCandidate:
    """
    Represents an extracted named entity candidate with context.
    """

    def __init__(self, raw_term: str, role_hint: str = "", count: int = 1, contexts: Optional[List[str]] = None):
        self.raw_term = raw_term
        self.role_hint = role_hint
        self.count = count
        self.contexts = contexts or []

    def add_occurrence(self, context: str):
        self.count += 1
        if len(self.contexts) < 3 and context not in self.contexts:
            self.contexts.append(context)

    def __repr__(self):
        return f"<EntityCandidate '{self.raw_term}' (hint='{self.role_hint}', count={self.count})>"


class EntityGuard:
    """
    Guards transcript pipelines against unverified proper nouns and speaker misattributions.
    """

    def __init__(self, confirmed_map: Optional[Dict[str, str]] = None):
        self.confirmed_map: Dict[str, str] = dict(confirmed_map) if confirmed_map else {}
        self.ignore_terms: Set[str] = {
            "大家", "各位", "我們", "你們", "他們", "這個", "那個",
            "現場", "問題", "報告", "時間", "研究", "簡報", "謝謝",
            "不好意思", "對不起", "稍微", "剛剛", "現在", "這裡",
            "部分", "方式", "內容", "結果", "模型", "架構", "資料",
            "天由", "由指", "導教",
        }

    def _clean_name(self, raw_name: str) -> str:
        name = raw_name.strip()
        # Strip known titles from suffix or prefix
        for kw in TITLE_KEYWORDS:
            if name.endswith(kw):
                name = name[:-len(kw)]
            if name.startswith(kw):
                name = name[len(kw):]
        # Strip single-character affixes if name has at least 3 chars
        while len(name) > 2 and name[-1] in TITLE_AFFIX_CHARS:
            name = name[:-1]
        while len(name) > 2 and name[0] in TITLE_AFFIX_CHARS:
            name = name[1:]
        # Strip common leading verbs like '由', '是', '為'
        if len(name) >= 3 and name[0] in "是由為在給與跟":
            name = name[1:]
        return name.strip()


    def register_confirmed(self, raw_term: str, confirmed_term: str):
        """
        Register a user-confirmed proper noun mapping.
        """
        self.confirmed_map[raw_term] = confirmed_term

    def register_confirmed_map(self, mapping: Dict[str, str]):
        """
        Batch register confirmed mappings.
        """
        self.confirmed_map.update(mapping)

    def extract_candidates(self, text: str) -> List[EntityCandidate]:
        """
        Scan text for candidate proper nouns based on academic & conference role patterns.
        """
        candidates: Dict[str, EntityCandidate] = {}
        matched_spans: Set[Tuple[int, int]] = set()

        for pattern in ROLE_PREFIX_PATTERNS:
            for match in re.finditer(pattern, text):
                raw_term = match.group(1).strip()
                term = self._clean_name(raw_term)

                if len(term) < 2 or len(term) > 4:
                    continue
                if term in self.ignore_terms or any(term == kw for kw in TITLE_KEYWORDS):
                    continue

                span = match.span(1)
                # Skip if this span overlaps with any previously recorded match
                if any(s[0] <= span[0] < s[1] or s[0] < span[1] <= s[1] for s in matched_spans):
                    continue
                matched_spans.add(span)

                start = max(0, match.start() - 25)
                end = min(len(text), match.end() + 25)
                context = text[start:end].replace("\n", " ").strip()

                # Infer role hint
                matched_str = match.group(0)
                role_hint = "講者/人物"
                for kw in TITLE_KEYWORDS:
                    if kw in matched_str:
                        role_hint = kw
                        break

                if term not in candidates:
                    candidates[term] = EntityCandidate(raw_term=term, role_hint=role_hint, count=1, contexts=[context])
                else:
                    candidates[term].add_occurrence(context)

        return sorted(candidates.values(), key=lambda c: c.count, reverse=True)



    def generate_verification_report(self, candidates: List[EntityCandidate]) -> str:
        """
        Generate a Markdown verification table for the user to review.
        """
        lines = [
            "### 🔍 專有名詞與人名候選清單（待使用者核對）",
            "",
            "以下為語音辨識文本中偵測到之潛在人名或職稱相關詞彙，請確認正確正名：",
            "",
            "| 候選原詞 | 角色線索 | 出現頻次 | 原始上下文範例 | 確認狀態 / 建議正名 |",
            "| :--- | :--- | :---: | :--- | :--- |",
        ]

        if not candidates:
            lines.append("| *(無偵測到疑似人名候選)* | - | - | - | - |")
            return "\n".join(lines)

        for c in candidates:
            ctx = c.contexts[0] if c.contexts else "-"
            # Truncate context if long
            if len(ctx) > 30:
                ctx = ctx[:28] + "..."
            status = f"✅ 已確認為 `{self.confirmed_map[c.raw_term]}`" if c.raw_term in self.confirmed_map else "⚠️ **待確認**"
            lines.append(f"| `{c.raw_term}` | {c.role_hint} | {c.count} | {ctx} | {status} |")

        lines.extend([
            "",
            "> **【規則提醒】**：根據 `PROOFREAD_RULES.md` 第 5 條，未經使用者確認之姓名嚴禁直接寫入最終交付文件。",
        ])
        return "\n".join(lines)

    def apply_confirmed_entities(self, text: str) -> str:
        """
        Substitute confirmed entities into text.
        """
        for raw, confirmed in self.confirmed_map.items():
            text = text.replace(raw, confirmed)
        return text

    def get_unconfirmed_candidates(self, text: str) -> List[EntityCandidate]:
        """
        Return candidates that have not been registered in confirmed_map.
        """
        all_candidates = self.extract_candidates(text)
        return [c for c in all_candidates if c.raw_term not in self.confirmed_map]

    @staticmethod
    def extract_institutional_entities(text: str) -> List[str]:
        """
        Extract institutional / departmental entities from text.
        """
        entities = set()
        for pat in INSTITUTION_PATTERNS:
            for match in re.finditer(pat, text):
                ent = match.group(0).strip()
                if len(ent) >= 4 and ent not in {"學術研討會", "論文研討會"}:
                    entities.add(ent)
        return sorted(list(entities))

    @staticmethod
    def verify_metadata_provenance(metadata: Dict, content_text: str) -> Tuple[bool, List[str]]:
        """
        Verify that all institutional and organizational entities claimed in metadata
        (event, title, speakers) have direct provenance in the transcript content text.
        Returns (is_valid, violations).
        """
        violations = []
        fields_to_check = [
            ("event", metadata.get("event", "")),
            ("title", metadata.get("title", "")),
        ]
        speakers = metadata.get("speakers", [])
        if isinstance(speakers, list):
            for spk in speakers:
                fields_to_check.append(("speaker", spk))
        elif isinstance(speakers, str):
            fields_to_check.append(("speakers", speakers))

        for field_name, field_val in fields_to_check:
            if not field_val or not isinstance(field_val, str):
                continue
            institutions = EntityGuard.extract_institutional_entities(field_val)
            for inst in institutions:
                aliases = [inst]
                if inst.startswith(("國立", "市立", "私立")):
                    aliases.append(inst[2:])
                if "臺灣科技大學" in inst or "台灣科技大學" in inst:
                    aliases.extend(["台科大", "台科", "NTUST"])
                elif "中央大學" in inst:
                    aliases.extend(["中央資管", "中央", "NCU"])
                elif "臺灣大學" in inst or "台灣大學" in inst:
                    aliases.extend(["台大", "NTU"])
                elif "清華大學" in inst:
                    aliases.extend(["清大", "NTHU"])
                elif "成功大學" in inst:
                    aliases.extend(["成大", "NCKU"])
                elif "交通大學" in inst or "陽明交通大學" in inst:
                    aliases.extend(["交大", "陽明交大", "NYCU"])
                elif "南洋大學" in inst or "南洋理工" in inst:
                    aliases.extend(["NTU", "南洋"])

                found = any(alias.lower() in content_text.lower() for alias in aliases)
                if not found:
                    violations.append(
                        f"Provenance violation in metadata['{field_name}']: '{inst}' has no mention in transcript text."
                    )

        return len(violations) == 0, violations

    @staticmethod
    def sanitize_metadata(metadata: Dict, content_text: str) -> Dict:
        """
        Sanitize metadata by replacing uncorroborated institutional entities with neutral terms.
        """
        sanitized = dict(metadata)
        is_valid, violations = EntityGuard.verify_metadata_provenance(sanitized, content_text)
        if not is_valid:
            event = str(sanitized.get("event", ""))
            for inst in EntityGuard.extract_institutional_entities(event):
                aliases = [inst, inst.replace("國立", "")]
                if not any(alias.lower() in content_text.lower() for alias in aliases):
                    if "碩士" in event and "口試" in event:
                        sanitized["event"] = "碩士學位論文口試審查會"
                    else:
                        sanitized["event"] = event.replace(inst, "").strip()
        return sanitized
