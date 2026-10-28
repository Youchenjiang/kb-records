#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language-Agnostic QA Dialogue Turn & Critique Coverage Guard
Validates that ALL substantial advisor / questioner interventions in verbatim transcripts (.full.md)
are faithfully covered in executive summaries (.md), completely independent of language (English, Chinese, bilingual).
"""

from collections import Counter
from pathlib import Path
import re
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Universal stop words / noise across English & Chinese
COMMON_STOP_WORDS = {
    # English filler & functional words
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with",
    "by", "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "from", "up", "down", "in", "out", "off", "over",
    "under", "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "s", "t", "can", "will", "just", "don", "should", "now", "i", "you",
    "he", "she", "it", "we", "they", "this", "that", "these", "those", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
    "does", "did", "doing", "would", "could", "my", "your", "our", "their", "what",
    "which", "who", "whom", "whose", "if", "because", "as", "until", "while", "of",
    "um", "uh", "yeah", "yes", "okay", "sorry", "thank", "thanks", "well", "think",
    "know", "said", "say", "saying", "see", "look", "like", "one", "two", "three",
    "first", "second", "third", "page", "slide", "presentation", "question",
    # Traditional Chinese filler words
    "的", "了", "和", "是", "就", "都", "而", "及", "與", "著", "或", "一個", "沒有",
    "我們", "你們", "他們", "這個", "那個", "這些", "那些", "因為", "所以", "如果",
    "但是", "然後", "那麼", "自己", "什麼", "怎麼", "這樣", "那樣", "也是", "就是",
    "還是", "可以", "覺得", "應該", "可能", "大家", "老師", "同學", "今天", "現在",
    "一下", "一些", "好的", "對啊", "嗯", "呃", "啊", "吧", "呢", "啦", "哦"
}

def extract_qa_interaction_blocks(text: str):
    """
    Extracts QA interaction blocks using pure speaker turn structure.
    No language keywords required.
    An interaction block occurs when a non-presenter (Advisor, Committee, Reviewer, Teacher, Peer)
    intervenes and speaks with substantive length (>15 words or >30 chars).
    """
    turns = re.findall(r"\*\*【(.*?)】\*\*：(.*?)(?=\n\n\*\*【|\Z)", text, flags=re.DOTALL)
    if not turns:
        return []

    # Identify primary presenter(s) vs questioners/advisors
    # In master thesis/project meetings, questioners are typically 指導教授, 口委, 審查委員, 評審, etc.
    questioner_roles = ["指導教授", "教授", "口委", "審查委員", "評審委員", "口試委員", "評審", "委員會", "教師", "老師"]
    
    qa_blocks = []
    for idx, (speaker, speech) in enumerate(turns):
        speech_clean = speech.strip()
        is_questioner = any(role in speaker for role in questioner_roles)
        
        # Check if this turn is a substantive intervention/question
        if is_questioner and len(speech_clean) >= 30:
            qa_blocks.append({
                "turn_index": idx + 1,
                "speaker": speaker.strip(),
                "speech": speech_clean
            })
    return qa_blocks

def extract_salient_concepts(speech: str, top_n: int = 5):
    """
    Extracts salient topic concepts (words/terms) from a speech segment.
    Works for English (case-insensitive words >= 4 letters) and Chinese (2-4 char n-grams).
    """
    concepts = []
    
    # 1. English words
    en_words = re.findall(r"[A-Za-z]{4,}", speech.lower())
    filtered_en = [w for w in en_words if w not in COMMON_STOP_WORDS]
    en_counts = Counter(filtered_en)
    for w, count in en_counts.most_common(top_n):
        concepts.append(w)
        
    # 2. Chinese technical phrases / terms (e.g. 2-4 hanzi)
    # Extract hanzi sequences
    hanzi_seqs = re.findall(r"[\u4e00-\u9fff]+", speech)
    zh_words = []
    for seq in hanzi_seqs:
        if len(seq) in (2, 3, 4) and seq not in COMMON_STOP_WORDS:
            zh_words.append(seq)
        elif len(seq) > 4:
            for i in range(len(seq) - 1):
                sub = seq[i:i+2]
                if sub not in COMMON_STOP_WORDS:
                    zh_words.append(sub)
    zh_counts = Counter(zh_words)
    for w, count in zh_counts.most_common(top_n):
        concepts.append(w)
        
    return list(dict.fromkeys(concepts))  # preserve order, unique

def verify_critique_coverage(full_path: Path, summary_path: Path):
    """
    Checks if substantial critique/QA interactions in full transcript are reflected in summary.
    Returns (covered_ratio, list_of_uncovered_issues).
    """
    full_text = full_path.read_text(encoding="utf-8")
    summary_text = summary_path.read_text(encoding="utf-8").lower()
    
    blocks = extract_qa_interaction_blocks(full_text)
    if not blocks:
        return 1.0, []
        
    uncovered = []
    for b in blocks:
        concepts = extract_salient_concepts(b["speech"])
        if not concepts:
            continue
            
        # Check if ANY of the top salient concepts from the advisor's question appear in summary
        # If it's an English term (e.g. 'drift'), we check if 'drift' or its Chinese counterpart '漂移' appears
        matched = False
        concept_matches = []
        for c in concepts:
            # Direct match
            if c in summary_text:
                matched = True
                concept_matches.append(c)
                break
            # Bilingual synonyms fallback
            bilingual_map = {
                "drift": "漂移", "drifting": "漂移", "hiding": "隱藏",
                "transfer": "轉移", "gradient": "梯度", "sensor": "感測器",
                "surrogate": "替代模型", "boundary": "邊界", "perturbation": "擾動",
                "incremental": "增量", "continual": "持續"
            }
            if c in bilingual_map and bilingual_map[c] in summary_text:
                matched = True
                concept_matches.append(f"{c}->{bilingual_map[c]}")
                break
                
        if not matched:
            uncovered.append({
                "turn": b["turn_index"],
                "speaker": b["speaker"],
                "snippet": b["speech"][:70].replace("\n", " "),
                "missing_concepts": concepts[:4]
            })
            
    coverage_ratio = (len(blocks) - len(uncovered)) / len(blocks)
    return coverage_ratio, uncovered

class TestLanguageAgnosticQACoverage(unittest.TestCase):
    """
    Enforces that advisor questions in any language are reflected in summaries.
    """
    def test_20261008_english_proposal_drift_question_coverage(self):
        """
        Targeted test on 20261008-01 English proposal:
        Ensures the advisor's behavior drift / continual learning question is faithfully recorded.
        """
        p_full = REPO_ROOT / "5-Master/Laboratory/Project-Meeting/20261008-01-全英語三年期研究計畫Proposal提案發表與攻防答辯.full.md"
        p_sum = REPO_ROOT / "5-Master/Laboratory/Project-Meeting/20261008-01-全英語三年期研究計畫Proposal提案發表與攻防答辯.md"
        
        ratio, uncovered = verify_critique_coverage(p_full, p_sum)
        print(f"\n[Test Result] 20261008-01 Coverage Ratio: {ratio:.1%}")
        if uncovered:
            print("Uncovered QA interactions:")
            for item in uncovered:
                print(f"  - Turn #{item['turn']} [{item['speaker']}]: '{item['snippet']}...' (Expected concepts: {item['missing_concepts']})")
                
        self.assertGreaterEqual(
            ratio, 0.85,
            f"Summary covers only {ratio:.1%} of advisor critique turns! Missing: {uncovered}"
        )

    def test_20261020_project_meeting_qa_coverage(self):
        """
        Targeted test on 20261020 R&D Administrative AI transformation matching:
        Ensures the advisor's AI coding / routine workflow questions and interventions are faithfully recorded.
        """
        p_full = REPO_ROOT / "5-Master/Laboratory/Project-Meeting/20261020-研發處行政業務AI轉型媒合與出國報告自動回填需求研討.full.md"
        p_sum = REPO_ROOT / "5-Master/Laboratory/Project-Meeting/20261020-研發處行政業務AI轉型媒合與出國報告自動回填需求研討.md"

        ratio, uncovered = verify_critique_coverage(p_full, p_sum)
        print(f"\n[Test Result] 20261020 Coverage Ratio: {ratio:.1%}")
        if uncovered:
            print("Uncovered QA interactions:")
            for item in uncovered:
                print(f"  - Turn #{item['turn']} [{item['speaker']}]: '{item['snippet']}...' (Expected concepts: {item['missing_concepts']})")

        self.assertGreaterEqual(
            ratio, 0.85,
            f"Summary covers only {ratio:.1%} of advisor critique turns! Missing: {uncovered}"
        )

    def test_batch41_laboratory_sessions_critique_coverage(self):
        """
        Targeted regression test on audited Batch 41 laboratory sessions (201-213).
        Validates that advisor critique coverage meets or exceeds 85% threshold.
        """
        audited_sessions = [
            ("201", "5-Master/Laboratory/Project-Meeting/20260716-實驗室暑期例會-新進碩一生AI開發實作與研究交接"),
            ("203", "5-Master/Laboratory/Project-Meeting/20260226-01-對抗性模仿學習與感測器模型防禦"),
            ("204", "5-Master/Laboratory/Project-Meeting/20260226-02-APK免疫疫苗與程式碼自動修補"),
            ("205", "5-Master/Laboratory/Project-Meeting/20260430-整合型計畫-容錯系統VPS評測與進度研討"),
            ("206", "5-Master/Laboratory/Project-Meeting/20260617-平台前端資料庫整合與API錯誤處理測試研討"),
            ("207", "5-Master/Laboratory/Project-Meeting/20260720-實驗室AI文獻管理與知識圖譜系統架構設計"),
            ("208", "5-Master/Laboratory/Project-Meeting/20260723-產學合作專案成本核銷與AI開發工具補助協調"),
            ("209", "5-Master/Laboratory/Security-News/20260720-Cursor-IDE惡意工作區路徑劫持與Git執行檔注入漏洞研討"),
            ("210", "5-Master/Laboratory/Security-News/20260914-PostgreSQL複寫協議提權漏洞"),
            ("211", "5-Master/Laboratory/Seminar/20260723-軟體工程論文研討-Kernel-Multi-Hunk-Features與跨檔案漏洞修補"),
            ("212", "5-Master/Laboratory/Seminar/20260914-自動化漏洞修復APR根因分析與兩階段驗證"),
            ("213", "5-Master/Laboratory/Thesis-Progress/20260226-Android惡意程式行為子圖與抗混淆GNN檢測"),
        ]

        for no, stem in audited_sessions:
            p_full = REPO_ROOT / f"{stem}.full.md"
            p_sum = REPO_ROOT / f"{stem}.md"
            ratio, uncovered = verify_critique_coverage(p_full, p_sum)
            print(f"\n[Test Result] Session #{no} Coverage Ratio: {ratio:.1%}")
            self.assertGreaterEqual(
                ratio, 0.85,
                f"Session #{no} covers only {ratio:.1%} of advisor critique turns! Missing: {uncovered}"
            )


if __name__ == "__main__":
    unittest.main()
