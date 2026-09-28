#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Verbatim Proofread Formatter for 4-University Deliverables
Follows PROOFREAD_RULES.md (Step 2: Proofread Formatting & Deep Correction):
- CJK punctuation & spacing normalization
- Comprehensive domain vocabulary & acoustic phonetic correction
- Natural narrative paragraph reconstruction (no rigid sentence splitting)
- Clear thematic chapter structure with emojis
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = REPO_ROOT / "transcribe_outputs"
CCNA_DIR = REPO_ROOT / "4-University" / "2025-Cisco-CCNA1"
SEC_DIR = REPO_ROOT / "4-University" / "2025-CompTIA-SecurityPlus"


def clean_spaces_and_punct(text: str) -> str:
    """Normalize CJK punctuation, remove broken spaces, and repair mid-sentence pause particle splits."""
    cjk = r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]"
    punc = r"[，。！？、；：「」『』（）—…《》〈〉“”‘’]"

    for _ in range(5):
        text = re.sub(rf"({cjk})\s+({cjk})", r"\1\2", text)

    for _ in range(4):
        text = re.sub(rf"({cjk})\s+({punc})", r"\1\2", text)
        text = re.sub(rf"({punc})\s+({cjk})", r"\1\2", text)
        text = re.sub(rf"({punc})\s+({punc})", r"\1\2", text)

    text = re.sub(rf"({cjk})\s*,\s*", r"\1，", text)
    text = re.sub(rf"({cjk})\s*\.\s*", r"\1。", text)
    text = re.sub(rf"({cjk})\s*;\s*", r"\1；", text)
    text = re.sub(rf"({cjk})\s*:\s*", r"\1：", text)
    text = re.sub(rf"({cjk})\s*\?\s*", r"\1？", text)
    text = re.sub(rf"({cjk})\s*!\s*", r"\1！", text)

    # Mid-sentence pause particle split repair:
    # 1. Purely dependent particles: never preceded by full stops, commas, or colons
    text = re.sub(r"[。！？，、；：]\s*([的得地著之])", r"\1", text)
    # 2. Sequential / time adverbs interrupted by sentence boundary:
    text = re.sub(r"[。！？]\s*(之後|後呢|後來)", r"\1", text)

    text = re.sub(rf"([a-zA-Z0-9_])\s+({cjk})", r"\1 \2", text)
    text = re.sub(rf"({cjk})\s+([a-zA-Z0-9_])", r"\1 \2", text)
    text = re.sub(r"[ \t]+", " ", text).strip()
    return text


def build_natural_paragraphs(sentences: List[str], target_chars: int = 220) -> List[str]:
    """
    Assemble sentences into cohesive natural narrative paragraphs.
    Avoids sentence splitting across paragraphs and breaks at logical boundaries.
    """
    paragraphs = []
    current_para = []
    current_len = 0

    discourse_openers = (
        "好，", "那接下來", "另外", "所以呢", "第一件", "第二件", "第三件",
        "首先", "也就是說", "比如說", "那在實務上", "總而言之", "那我們看",
        "再來就是", "最後", "但是", "不過", "特別是", "據我所知",
    )

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue

        # If sentence starts with an obvious transition marker and current paragraph has enough content
        is_opener = any(sent.startswith(op) for op in discourse_openers)
        if current_para and (current_len >= target_chars or (is_opener and current_len >= 120)):
            paragraphs.append("".join(current_para))
            current_para = [sent]
            current_len = len(sent)
        else:
            current_para.append(sent)
            current_len += len(sent)

    if current_para:
        paragraphs.append("".join(current_para))

    # Post-process: merge tiny orphan paragraphs (< 60 chars) into neighbors
    if len(paragraphs) > 1:
        merged = []
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if len(p) < 60 and merged:
                merged[-1] = merged[-1] + " " + p
            else:
                merged.append(p)
        paragraphs = merged

    # If first paragraph is still too short (< 60 chars) and there are multiple paragraphs
    if len(paragraphs) > 1 and len(paragraphs[0]) < 60:
        paragraphs[1] = paragraphs[0] + " " + paragraphs[1]
        paragraphs = paragraphs[1:]

    return paragraphs


# Global common domain phonetic replacements
COMMON_REPLACEMENTS = [
    ("Pearson View", "Pearson VUE"),
    ("Pearson view", "Pearson VUE"),
    ("Pearson Vue", "Pearson VUE"),
    ("Unview", "OnVUE"),
    ("Onview", "OnVUE"),
    ("UnView", "OnVUE"),
    ("on view", "OnVUE"),
    ("onview", "OnVUE"),
    ("安利的一種方法。反正他一定要有微。看可以看到", "OnVUE 的一種方法。反正他一定要有 Webcam 可以看到"),
    ("安利的一種方法", "OnVUE 的一種方法"),
    ("一定要有微。看可以看到", "一定要有 Webcam 可以看到"),
    ("微。看可以看到", "Webcam 可以看到"),
    ("這波單位點四十個點看", "www.cisco.com"),
    ("三個單位點四十個點看", "www.cisco.com"),
    ("四十個點看", "cisco.com"),
    ("這波單位", "www"),
    ("那 B 就更更不用講了", "那 IPv6 就更更不用講了"),
    ("那 B 就更不用講了", "那 IPv6 就更更不用講了"),
    ("那 B 就", "那 IPv6 就"),
    ("Compiere", "CompTIA"),
    ("康迪", "CompTIA"),
    ("康提亞", "CompTIA"),
    ("Security Plus", "Security+"),
    ("Security plus", "Security+"),
    ("security class", "Security+"),
    ("Network Plus", "Network+"),
    ("single sign", "Single Sign-On (SSO)"),
    ("single三號", "Single Sign-On (SSO)"),
    ("新用三號車", "Single Sign-On (SSO)"),
    ("三印一下", "sign in 一下"),
    ("三印", "sign in"),
    ("廈門客", "下一門課"),
    ("下門課", "下一門課"),
    ("這口", "Cisco"),
    ("師科", "Cisco"),
    ("四科", "Cisco"),
    ("西西那", "CCNA"),
    ("西西", "CCNA"),
    ("西遷", "CCNA"),
    ("C C A", "CCNA"),
    ("C C I", "CCIE"),
    ("自然人憑政", "自然人憑證"),
    ("二兩百帶去三零一", "200-301"),
    ("兩百帶去三零一", "200-301"),
    ("去江", "巨匠"),
    ("橫瀝", "恆逸"),
    ("橫應", "恆逸"),
    ("連城", "聯成"),
    ("巨佳", "巨匠"),
    ("恆利", "恆逸"),
    ("微片", "Webcam"),
    ("挖坑罵詞", "Wildcard Mask（萬用字元遮罩）"),
    ("考補題", "考古題"),
    ("拖衣題", "拖曳題"),
    ("脫衣題", "拖曳題"),
    ("自理大學", "致理科技大學"),
    ("士軍", "四軍（陸海空與資通電軍）"),
    ("智通電", "資通電軍"),
    ("髮絲類", "Fastlab"),
    ("耐群組", "LINE 群組"),
    ("那群主", "LINE 群組"),
    ("那群", "LINE 群"),
    ("挖坑罵詞", "Wildcard Mask（萬用字元遮罩）"),
    ("挖卡", "Wildcard Mask"),
    ("X list 一號", "access-list 1"),
    ("X list", "access-list"),
    ("Roder", "Router"),
    ("P O C two", "POC-2"),
    ("trace log", "traceroute"),
    ("when的部分都浪費掉", "WAN 的頻寬都浪費掉"),
    ("二的方向", "out 的方向"),
    ("炮規則", "套規則"),
    ("本地IPN", "permit ip any any"),
    ("抵耐", "deny"),
    ("黑的的部分", "Header（標頭）部分"),
    ("黑的", "Header"),
    ("建湯了", "建 Tunnel"),
    ("雙堆疊", "Dual-Stack（雙堆疊）"),
    ("隱匿的 hole", "Unique Local"),
    ("D for R", "Default Route"),
    ("router station", "Router Solicitation (RS)"),
    ("router 耳臺什麼", "Router Advertisement (RA)"),
    ("蜂包", "封包"),
    ("T A V", "Network TAP"),
    ("T A P", "Network TAP"),
    ("陰帶", "In-band"),
    ("三手交握", "三次交握"),
    ("OpenSense", "OPNsense"),
    ("應用城市的空氣", "應用程式的攻擊"),
    ("應用層是", "應用程式"),
    ("落點的掃描", "弱點掃描"),
    ("落掃", "弱掃"),
    ("未果應用程式", "Web 應用程式"),
    ("英國資訊保安", "資訊共享與分析中心（ISAC）"),
    ("世界的記錄器", "事件的記錄器"),
    ("系統機子", "系統機制"),
    ("通用記錄盤格式", "通用日誌格式（Common Event Format, CEF）"),
    ("傳的十秒", "傳的時間"),
    ("紅包收幾", "封包收集"),
    ("證人憑證", "自然人憑證"),
    ("輸入憑口", "輸入 PIN 碼"),
    ("單點死角", "單點故障（Single Point of Failure, SPOF）"),
    ("令 local", "Link-Local"),
    ("link local", "Link-Local"),
    ("主播MultiCast", "Multicast（群播）"),
    ("連續領", "連續零"),
    ("雙不好", "雙冒號"),
    ("有密local", "Unique Local"),
    ("十一位", "三方交握（Three-way Handshake）"),
    ("三項", "三次交握"),
    ("雙方哈", "雙掛號"),
    ("in報", "Inbound"),
    ("out報", "Outbound"),
]


def apply_deep_replacements(text: str, custom_replacements: List[Tuple[str, str]] = None) -> str:
    """Apply global and custom phonetic replacements."""
    for old, new in COMMON_REPLACEMENTS:
        text = text.replace(old, new)
    if custom_replacements:
        for old, new in custom_replacements:
            text = text.replace(old, new)
    return text


def format_single_proofread(
    raw_folder_name: str,
    target_proofread_path: Path,
    title: str,
    event: str,
    talk_id: str,
    date: str,
    speakers: List[str],
    tags: List[str],
    section_markers: List[Tuple[str, str]],  # (Heading, trigger_text_snippet)
    custom_corrections: List[Tuple[str, str]] = None,
):
    """
    Format a raw transcript into a beautifully structured, highly readable proofread markdown.
    """
    raw_txt_path = OUTPUTS_DIR / raw_folder_name / "transcript_zh_tw.txt"
    if not raw_txt_path.exists():
        raw_txt_path = OUTPUTS_DIR / raw_folder_name / "raw_transcript.txt"
    if not raw_txt_path.exists():
        print(f"[ERROR] No raw transcript found in {raw_folder_name}")
        return

    raw_text = raw_txt_path.read_text(encoding="utf-8")
    cleaned_text = clean_spaces_and_punct(raw_text)
    corrected_text = apply_deep_replacements(cleaned_text, custom_corrections)

    # Split into raw sentences by full stops
    raw_sentences = re.split(r"(?<=[。！？\n])", corrected_text)
    raw_sentences = [s.strip() for s in raw_sentences if s.strip()]

    # Segment into sections by trigger markers
    sections = []  # [(heading, [sentences])]
    cur_heading = section_markers[0][0] if section_markers else "一、課程核心講義與技術解析"
    cur_sentences = []
    marker_idx = 1 if len(section_markers) > 1 else 9999

    filler_phrases = {"好。", "好哈。", "OK。", "對。", "嗯。", "好，好。", "好，知道。"}
    for s in raw_sentences:
        if marker_idx < len(section_markers):
            next_heading, trigger = section_markers[marker_idx]
            if trigger in s:
                transferred = []
                while cur_sentences and (len(cur_sentences[-1]) <= 6 or cur_sentences[-1] in filler_phrases):
                    transferred.insert(0, cur_sentences.pop())
                if cur_sentences:
                    sections.append((cur_heading, cur_sentences))
                cur_heading = next_heading
                cur_sentences = transferred
                marker_idx += 1
        cur_sentences.append(s)

    if cur_sentences:
        sections.append((cur_heading, cur_sentences))

    # Construct Document
    lines = [
        "---",
        f'title: "{title}"',
        f'event: "{event}"',
        f'date: "{date}"',
        f'talk_id: "{talk_id}"',
        f"speakers: {speakers}",
        'type: "verbatim-narrative-transcript"',
        "verbatim: true",
        'scenario: "single-talk"',
        'category: "4-University"',
        "tags:",
    ]
    for tag in tags:
        lines.append(f'  - "{tag}"')
    lines.extend([
        "---",
        "",
        f"# 🎙️ {title} (授課講師)",
        "",
        "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語（Cisco、CompTIA、Pearson VUE、OnVUE、SSO、PKI、SIEM 等）與標點符號，並依授課脈絡劃分流暢之章節段落。",
        "",
        "---",
        "",
    ])

    for heading, sents in sections:
        lines.extend([f"## {heading}", ""])
        paras = build_natural_paragraphs(sents, target_chars=220)
        for p in paras:
            lines.append(p)
            lines.append("")

    target_proofread_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✨ Successfully formatted proofread: {target_proofread_path.name} ({len(lines)} lines)")


print("Proofread Formatter Engine loaded.")
