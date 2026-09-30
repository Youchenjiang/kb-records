#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 5-Master Research Methodology Deliverables:
- 資訊管理研究方法論 Part 1 & Part 2 (週三 14點00分 & 週三 15點42分)
Follows PROOFREAD_RULES.md, ScenarioType.CLASSROOM_LECTURE, and repository linters.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "5-Master" / "2025-ResearchMethodology"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"

REPLACEMENTS = [
    (r"validity", "效度（Validity）"),
    (r"hypothesis", "假說（Hypothesis）"),
    (r"framework", "研究架構（Research Framework）"),
    (r"organize", "組織（Organize）"),
    (r"conclusion", "結論（Conclusion）"),
    (r"discrete", "離散變數（Discrete）"),
    (r"aspect background", "背景變數（Demographics）"),
    (r"操作化", "操作化（Operationalization）"),
    (r"治安", "資安"),
]


def clean_text(text: str) -> str:
    res = text
    for pat, rep in REPLACEMENTS:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def segment_into_dialogue_paragraphs(text: str, default_speaker="授課講師") -> str:
    sentences = re.split(r"(?<=[。！？])", text)
    paragraphs = []
    current_para = []
    current_len = 0

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        current_para.append(s)
        current_len += len(s)
        if current_len >= 220 or s.endswith("好。") or s.endswith("OK。") or s.endswith("下週繼續。"):
            paragraphs.append("".join(current_para))
            current_para = []
            current_len = 0

    if current_para:
        paragraphs.append("".join(current_para))

    formatted_paras = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        student_triggers = ["老師請問", "所以操作化是", "是這樣嗎？"]
        if any(trig in p_clean for trig in student_triggers):
            formatted_paras.append(f"**【學員】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_part1():
    print("Building Research Methodology Part 1...")
    raw = (RAW_DIR / "週三 14點00分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "資訊管理研究方法論 Lesson 01：基礎研究 vs. 應用研究、概念層次與變數操作化"
    talk_id = "RES-METH-01"
    event = "資訊管理研究所研究方法論課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.33)
    s2 = int(total_len * 0.66)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 基礎研究（Basic Research） vs. 應用研究（Applied Research）本質差異與研究動機", sec1)
    builder.add_section("📐 概念層次（Conceptual Level）到操作層次（Operational Level）之「操作化（Operationalization）」", sec2)
    builder.add_section("🧪 研究效度（Validity）、測量誤差與多元變數關係架構圖繪製", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "資訊管理研究所研究方法論課程"',
        'event: "資訊管理研究所研究方法論課程"\ndate: "2026-03-04"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "研究方法-01-概念層次操作化與變數定義-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：資訊管理研究方法論、基礎與應用研究分野、概念操作化與變數定義  
> **授課教授**：授課講師（資管所資深講座教授）  
> **核心模組**：Research Methodology, Basic vs. Applied Research, Conceptualization & Operationalization  
> **學習目標**：理解學術研究三大領域（實務、理論、方法），掌握將抽象概念轉換為可測量變數之操作化技巧  
> **關聯文件**：[📄 完整原話逐字稿 (研究方法-01-概念層次操作化與變數定義-proofread.md)](./研究方法-01-概念層次操作化與變數定義-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["現實世界現象與實務痛點"] --> B["概念層次 (Conceptual Level)"]
    B --> C["抽象構念 (Constructs / 如資安意識、滿意度)"]
    C -->|操作化程序 (Operationalization)| D["操作層次 (Operational Level)"]
    D --> E["可測量變數 (Variables / 如問卷題項、日誌登入次數)"]
    E --> F["資料收集與統計分析 (Data Collection & Analysis)"]
    F --> G["效度檢驗 (Validity & Reliability)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **基礎研究 vs. 應用研究**：基礎研究旨在探索宇宙與社會現象之普遍規律、拓展知識邊界；應用研究則側重解決特定組織或產業的具體實務問題。資管研究往往兼具兩者特徵。
2. **操作化（Operationalization）核心價值**：抽象概念（如「系統安全性」）無法直接測量，必須透過操作化轉譯為具體可觀察、可量化的變數（如未修補 CVE 數量、帳號密碼強度分數）。
3. **效度（Validity）之挑戰**：實驗與問卷設計永遠存在測量誤差（Measurement Error），研究者必須在研究架構中嚴格論證指標的建構效度、收斂效度與區別效度。
"""
    summary_file = OUT_DIR / "研究方法-01-概念層次操作化與變數定義-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_part2():
    print("Building Research Methodology Part 2...")
    raw = (RAW_DIR / "週三 15點42分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "資訊管理研究方法論 Lesson 02：概念界定、離散與連續變數、假說建立與理論架構檢證"
    talk_id = "RES-METH-02"
    event = "資訊管理研究所研究方法論課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.33)
    s2 = int(total_len * 0.66)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 概念（Concepts）作為學術溝通與思考基石之重要性", sec1)
    builder.add_section("📊 變數類型分類：離散變數（Discrete） vs. 連續變數（Continuous）之統計特性", sec2)
    builder.add_section("🧭 假說建立（Hypothesis Formulation）、理論框架（Theoretical Framework）與實證支援", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "資訊管理研究所研究方法論課程"',
        'event: "資訊管理研究所研究方法論課程"\ndate: "2026-03-04"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "研究方法-02-假說建立與理論框架實證檢驗-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：學術概念思考邊界、變數尺度分類（離散 vs. 連續）、研究假說擬定與理論框架  
> **授課教授**：授課講師（資管所資深講座教授）  
> **核心模組**：Research Concepts, Discrete vs. Continuous Variables, Hypothesis Formulation  
> **學習目標**：掌握嚴謹概念界定、區分名目/順序/等距/等比尺度，建立可被實證檢驗之具體假說  
> **關聯文件**：[📄 完整原話逐字稿 (研究方法-02-假說建立與理論框架實證檢驗-proofread.md)](./研究方法-02-假說建立與理論框架實證檢驗-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Theory["理論文獻基礎 (Theoretical Foundation)"] --> Framework["建立研究理論架構 (Research Framework)"]
    Framework --> Scope["限制研究邊界 (Boundary of Scope)"]
    Scope --> H["提出具體檢定假說 (Hypothesis H1, H2, H3...)"]
    H --> VarType{"界定自變數與因變數之尺度"}
    VarType --> Disc["離散變數 (Discrete: 類別、二元、人口統計)"]
    VarType --> Cont["連續變數 (Continuous: 等距、比率尺度、使用時數)"]
    Disc & Cont --> EmpTest["實證數據檢驗與假說支持判定 (Supported / Rejected)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **概念是思考與溝通的基石**：學術研究最忌「頭腦簡單」，所謂深刻思考即在於大腦中具備足夠豐富、邊界精準的專用概念，能向同行精確傳遞邏輯。
2. **變數尺度的統計意義**：離散變數（如性別、部門、是否採用某技術）與連續變數（如系統反應時間、月交易量）適用完全不同的統計檢定模型（卡方檢定 vs. 回歸分析/結構方程模型）。
3. **假說（Hypothesis）的邊界效應**：提出明確的假說能防止研究發散，為論文明確劃定「要包含什麼、不包含什麼」的嚴密範疇。
"""
    summary_file = OUT_DIR / "研究方法-02-假說建立與理論框架實證檢驗-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_part1()
    build_part2()
