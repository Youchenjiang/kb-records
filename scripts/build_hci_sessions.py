#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Human-Computer Interaction & UX Design course deliverables (HCI-01, HCI-02):
- Proofread verbatim transcription with speaker attributions
- Structured summary notes with Mermaid diagrams
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_undergrad_courses import clean_text, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2024-UndergraduateCourses"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_hci_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in HCI/UX lectures."""
    replacements = [
        ("Nolan", "Nielsen Norman Group (NN/g)"),
        ("使用本經驗", "使用者經驗 (User Experience)"),
        ("使用者 呃，什麼是使用者經驗呢", "什麼是使用者經驗呢"),
        ("e 收購了", "Google 收購了"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_hci_01():
    print("Building HCI-01 (週二 15點38分)...")
    raw_path = RAW_DIR / "週二 15點38分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_hci_typos(raw)

    title = "人機互動與 UX 設計 Lesson 01：行為動機模型、人境互動模式與使用者心智模型"
    talk_id = "HCI-01-MOTIVATION-ENVIRONMENT"
    event = "大學部人機互動與使用者經驗設計課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 設計心理學起點：內在動機探索、職涯抉擇與個人價值實現", sec1)
    builder.add_section("📊 人境互動與空間認知：生活與風景的視角翻轉、迷路意涵與環境互動映射", sec2)
    builder.add_section("💼 產品與使用者互動：複雜動機外化行為、防誤觸機制與抱枕遙控器案例", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部人機互動與使用者經驗設計課程"',
        'event: "大學部人機互動與使用者經驗設計課程"\ndate: "2024-11-12"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "人機互動與UX設計-01-行為動機與人境互動模式-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：設計心理學（Design Psychology）、行為動機、人境互動（Person-Environment Interaction）與心智模型（Mental Model）  
> **授課教授**：授課講師（人機互動與工業設計教授）  
> **核心模組**：Mental Models, Behavioral Motivation, Person-Environment Interaction, Affordance, Error Prevention  
> **學習目標**：理解使用者內在動機如何轉化為外在操作行為，掌握環境脈絡與人際互動如何塑造產品之直覺互動體驗  
> **關聯文件**：[📄 完整原話逐字稿 (人機互動與UX設計-01-行為動機與人境互動模式-proofread.md)](./人機互動與UX設計-01-行為動機與人境互動模式-proofread.md)

---

## 🏛️ 人機互動 (HCI) 心智模型與情境互動架構

```mermaid
flowchart TD
    User["使用者內在心理狀態<br/>(動機、目標、容忍度、過往經驗)"]
    Action["外在操作行為<br/>(點擊、滑動、手勢、語音)"]
    Product["產品 / 介面實體<br/>(回饋、預設提示、操作約束)"]
    Context["環境與物理脈絡<br/>(空間、干擾、社會場景)"]

    User --> Action
    Action --> Product
    Product -- "感官回饋與系統狀態" --> User
    Context -. "情境約束與干擾" .-> User
    Context -. "環境光線/空間限制" .-> Product
```

---

## 🛋️ 使用者行為驅動之產品創新模式 (以抱枕遙控器為例)

```mermaid
flowchart LR
    Pain["痛點洞察：使用者躺臥沙發時<br/>不願起身尋找傳統硬質遙控器"]
    Behavior["自然行為：雙手習慣抱持柔軟抱枕"]
    Integration["創新融合：將遙控電路軟性化<br/>嵌入日常抱枕織物中"]
    Constraint["防呆防誤觸機制：設置實體啟動按鈕<br/>避免隨意擠壓導致訊號誤發"]

    Pain --> Behavior
    Behavior --> Integration
    Integration --> Constraint
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 人與環境的互動哲學（生活 vs. 風景）
- **視角翻轉**：「對你來說是生活，對別人來說是風景」。互動設計必須跳脫設計師本位主義，深入使用者真實生活的日常脈絡（Context of Use）。
- **迷路的空間認知意涵**：迷路並非全然是負面的系統錯誤，而是人與空間環境在動態探索中重塑心智地圖（Cognitive Map）的過程。

### 2. 動機、行為與產品形式
- **複雜動機與外在行為**：人類的行為往往受多重複雜的內在動機驅動（例如省力、舒適、安全感）。優秀的設計順應人類自然的慵懶與直覺，而非強迫使用者適應生硬的機械結構。
- **操作約束與防呆設計（Error Prevention / Poka-Yoke）**：軟性互動介面（如織物或抱枕遙控）容易引發非意圖按壓，設計必須引入明確的確認動作或開關狀態約束，以消除誤操作。
"""
    summary_file = OUT_DIR / "人機互動與UX設計-01-行為動機與人境互動模式-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_hci_02():
    print("Building HCI-02 (週二 16點53分)...")
    raw_path = RAW_DIR / "週二 16點53分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_hci_typos(raw)

    title = "人機互動與 UX 設計 Lesson 02：使用者經驗完整定義、智慧產品易用性與美學平衡"
    talk_id = "HCI-02-UX-DEFINITION-USABILITY"
    event = "大學部人機互動與使用者經驗設計課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 學習契約與自主承諾：課堂紀律、容忍閥值設定與專業態度建立", sec1)
    builder.add_section("📊 NN/g 使用者經驗標準定義：涵蓋終端使用者與企業、服務與產品互動之全維度", sec2)
    builder.add_section("💼 智慧產品易用性與外觀美學：Nest 智慧溫控器收購與 AirPods 工業設計案例解析", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部人機互動與使用者經驗設計課程"',
        'event: "大學部人機互動與使用者經驗設計課程"\ndate: "2024-11-12"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "人機互動與UX設計-02-使用者經驗定義與智慧產品易用性-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：使用者經驗（User Experience, UX）、Nielsen Norman Group 權威定義、智慧硬體易用性（Usability）與工業美學平衡  
> **授課教授**：授課講師（人機互動與工業設計教授）  
> **核心模組**：NN/g UX Definition, Usability Heuristics, Industrial Design, Smart Home, Google Nest, Apple AirPods  
> **學習目標**：精熟 NN/g 對使用者經驗之全層面定義，理解使用者旅程中功能、易用性與審美價值的互補張力  
> **關聯文件**：[📄 完整原話逐字稿 (人機互動與UX設計-02-使用者經驗定義與智慧產品易用性-proofread.md)](./人機互動與UX設計-02-使用者經驗定義與智慧產品易用性-proofread.md)

---

## 🏛️ Nielsen Norman Group (NN/g) 使用者經驗全維度層級

```mermaid
flowchart TD
    UX["使用者經驗 (User Experience, UX)<br/>使用者與企業、服務及產品互動的『所有層面』"]
    
    Level1["層級一：實體與數位產品互動 (Product Interaction)<br/>介面清晰度、易用性、防呆、美感"]
    Level2["層級二：服務系統與支援流程 (Service Delivery)<br/>客服支援、配送物流、退換貨體驗"]
    Level3["層級三：企業品牌價值與信任 (Brand Perception)<br/>企業文化、隱私信任、長期情感連結"]

    UX --> Level1
    UX --> Level2
    UX --> Level3
```

---

## ⚖️ 智慧硬體設計張力：易用性 (Usability) vs. 工業美學 (Aesthetics)

```mermaid
flowchart LR
    subgraph ProductCases["指標性產品案例分析"]
        Nest["Google Nest 智慧溫控器<br/>- 突破傳統溫控器繁雜按鈕<br/>- 旋轉金屬外環直覺調節<br/>- 兼具極簡壁掛藝術品外觀"]
        AirPods["Apple AirPods 藍牙耳機<br/>- 開蓋即連無縫體驗<br/>- 造型標誌性與配戴舒適度<br/>- 消除藍牙配對複雜挫折感"]
    end

    Usability["易用性 (Usability)<br/>好用、直覺、低學習曲線"] <---> Aesthetics["外觀美學 (Aesthetics)<br/>吸引人、極簡、質感、品牌識別"]
    Usability --- Nest
    Aesthetics --- Nest
    Usability --- AirPods
    Aesthetics --- AirPods
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 使用者經驗 (User Experience, UX) 的標準定義
- **NN/g 權威詮釋**：使用者經驗「不僅僅是介面（UI）好不好看」，而是「終端使用者與公司、其服務以及其產品互動的所有層面（all aspects of the end-user's interaction with the company, its services, and its products）」。
- **整體旅程性**：包含購買前期待、拆箱體驗、初次設定挫折、日常使用流暢度乃至售後服務的全生命週期感受。

### 2. 易用性（Usability）與美學設計的相輔相成
- **美即好用效應（Aesthetic-Usability Effect）**：使用者傾向認為美觀的產品更容易使用，並對偶發的小瑕疵展現更高的容忍度。
- **直覺回饋與極簡架構**：以 Nest 智慧溫控器為例，傳統溫控器充斥晦澀的液晶按鈕與設定選單，Nest 透過精準旋轉外環與隨環境色變化的圓形螢幕，將複雜的物聯網溫控簡化為最原始直觀的物理操作。
"""
    summary_file = OUT_DIR / "人機互動與UX設計-02-使用者經驗定義與智慧產品易用性-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_hci_01()
    build_hci_02()
