#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Semester Courses deliverables (MATH-02, MATH-03, BIO-01):
- MATH-02: Polynomial Variable Substitution & Exam Review
- MATH-03: Factor Theorem & Higher-Degree Polynomial Decomposition
- BIO-01: Optical Microscopy Cell Observation Lab & Midterm Exam Protocol
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_undergrad_courses import clean_text, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2024-Fall-SemesterCourses"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_batch3_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in semester course lectures."""
    replacements = [
        ("變數變快", "變數變換 (Variable Substitution)"),
        ("簡討過", "檢討過"),
        ("焦根", "根號"),
        ("a 減 a a 減 b", "(x - a) 與 (x - b)"),
        ("療法", "實驗記錄簿"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_math_02():
    print("Building MATH-02 (10月19日 下午4點24分)...")
    raw_path = RAW_DIR / "10月19日 下午4點24分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_batch3_typos(raw)

    title = "基礎數學與先修代數 Lesson 02：多項式變數代換法、方根整數小數化簡與段考檢討"
    talk_id = "MATH-02-EXAM-REVIEW-VARIABLE-SUBSTITUTION"
    event = "大學部基礎數學與微積分先修課程"

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

    builder.add_section("🎯 班級日常事務與常規提醒：戶外課門窗巡檢、活動紀錄影片與秩序要求", sec1)
    builder.add_section("📊 段考數學重點試題檢討：方根整數小數拆解與令 t 等於 x 平方加 3x 變數代換技巧", sec2)
    builder.add_section("💼 運動會活動籌備與公差紀律：外掃區清潔標準與值日幹部集合宣達", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部基礎數學與微積分先修課程"',
        'event: "大學部基礎數學與微積分先修課程"\ndate: "2024-10-19"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "基礎數學-02-多項式變數代換法與段考綜合試題檢討-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：基礎數學段考核心難題檢討、多項式高次式變數代換技巧、無理數方根整數與純小數部分拆解  
> **授課教授**：授課講師（應用數學授課教授）  
> **核心模組**：Algebraic Substitution, Radical Simplification, Integer and Fractional Parts, Exam Review  
> **學習目標**：精熟令 $t = x^2 + 3x$ 之降次代換策略化簡複雜高次多項式，掌握無理數方根取整數與小數之代數操作  
> **關聯文件**：[📄 完整原話逐字稿 (基礎數學-02-多項式變數代換法與段考綜合試題檢討-proofread.md)](./基礎數學-02-多項式變數代換法與段考綜合試題檢討-proofread.md)

---

## 🏛️ 高次多項式「變數代換法」解題思維模型

```mermaid
flowchart TD
    Complex["高次複雜代數方程式<br/>(例如: (x^2 + 3x + 1)(x^2 + 3x + 2) = 3(x^2 + 3x) + 8)"]
    Pattern["識別共同重複結構塊: (x^2 + 3x)"]
    Substitution["令新變數 t = x^2 + 3x"]
    Simple["降次化簡為二次方程式: (t + 1)(t + 2) = 3t + 8<br/>👉 展開求解 t"]
    BackSub["回代求得 x: x^2 + 3x = t^*<br/>👉 解出原始方程式所有實數根"]

    Complex --> Pattern
    Pattern --> Substitution
    Substitution --> Simple
    Simple --> BackSub
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 變數代換法 (Variable Substitution) 降次心法
- **難題破局點**：若直接將四次多項式暴力展開，極易產生高階繁瑣計算與符號錯誤。透過觀察對稱結構，令 $t = x^2 + 3x$，可將四次方程式立即降解為一元二次方程式。
- **回代檢驗**：求出 $t$ 之後，務必回代二次方程式 $x^2 + 3x - t = 0$，並透過判別式 $D = b^2 - 4ac$ 檢驗是否有實數解。

### 2. 無理數方根的「整數部分」與「小數部分」
- 設 $\sqrt{N}$ 介於兩相鄰正整數之間 $k < \sqrt{N} < k+1$：
  - **整數部分（Integer Part）**：$a = \lfloor \sqrt{N} \rfloor = k$。
  - **小數部分（Fractional Part）**：$b = \sqrt{N} - k \in (0, 1)$。
"""
    summary_file = OUT_DIR / "基礎數學-02-多項式變數代換法與段考綜合試題檢討-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_math_03():
    print("Building MATH-03 (10月22日 下午3點16分)...")
    raw_path = RAW_DIR / "10月22日 下午3點16分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_batch3_typos(raw)

    title = "基礎數學與先修代數 Lesson 03：多項式因式定理、餘式定理與高次代數分解實務"
    talk_id = "MATH-03-FACTOR-THEOREM-POLYNOMIALS"
    event = "大學部基礎數學與微積分先修課程"

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

    builder.add_section("🎯 課堂開場與專注力凝聚：時間價值認知、學習態度建立與師生互動", sec1)
    builder.add_section("📊 因式定理核心架構：主題八因式定理推導、分配律逆推與雙根一次因式判定", sec2)
    builder.add_section("💼 高次多項式分解實戰：綜合除法輔助、常見計算盲點與課後演練總結", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部基礎數學與微積分先修課程"',
        'event: "大學部基礎數學與微積分先修課程"\ndate: "2024-10-22"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "基礎數學-03-多項式因式定理與高次代數分解實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：多項式餘式定理（Remainder Theorem）、因式定理（Factor Theorem）、高次多項式整係數因式分解與分配律逆推  
> **授課教授**：授課講師（應用數學授課教授）  
> **核心模組**：Remainder Theorem, Factor Theorem, Polynomial Factorization, Synthetic Division  
> **學習目標**：精熟 $f(a)=0 \iff (x-a) \mid f(x)$ 之因式定理雙向推論，掌握高次多項式一次因式檢驗法與分配律逆向因式提取  
> **關聯文件**：[📄 完整原話逐字稿 (基礎數學-03-多項式因式定理與高次代數分解實務-proofread.md)](./基礎數學-03-多項式因式定理與高次代數分解實務-proofread.md)

---

## 🏛️ 多項式除法原理與餘式／因式定理推論脈絡

```mermaid
flowchart TD
    DivAlg["多項式除法原理: f(x) = (x - a) q(x) + r<br/>(其中商式 q(x)，餘式 r 為常數)"]
    Sub["代入 x = a 求值"]
    Remainder["餘式定理 (Remainder Theorem):<br/>f(a) = (a - a) q(a) + r = r<br/>👉 多項式值即為除以 (x - a) 之餘式"]
    FactorCheck{"若餘式 r = f(a) = 0 ?"}
    Factor["因式定理 (Factor Theorem):<br/>f(x) = (x - a) q(x)<br/>👉 (x - a) 為 f(x) 之因式"]

    DivAlg --> Sub
    Sub --> Remainder
    Remainder --> FactorCheck
    FactorCheck -- "餘式為 0" --> Factor
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 因式定理 (Factor Theorem) 核心判據
- 若多項式 $f(x)$ 滿足 $f(a) = 0$，則 $(x - a)$ 必為 $f(x)$ 之一階一次因式。
- **多根因式推廣**：若 $a, b$ 為兩相異實數，且 $f(a) = 0, f(b) = 0$，則 $f(x)$ 必同時含有 $(x - a)$ 與 $(x - b)$ 因式，即 $(x - a)(x - b) \mid f(x)$。

### 2. 分配律逆推與因式分解
- 高次多項式因式分解本質上為乘法分配律的逆向操作：
  $$a \cdot c + b \cdot c = (a + b) \cdot c$$
- 透過一次因式檢驗法猜根（可能的根必在最高次係數因數與常數項因數之商），結合綜合除法降次，逐階抽離線性因子。
"""
    summary_file = OUT_DIR / "基礎數學-03-多項式因式定理與高次代數分解實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_bio_01():
    print("Building BIO-01 (10月24日 下午1點24分)...")
    raw_path = RAW_DIR / "10月24日 下午1點24分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_batch3_typos(raw)

    title = "普通生物學實驗 Lesson 01：光學顯微鏡細胞觀察實作與期中考操作規範"
    talk_id = "BIO-01-LAB-MICROSCOPY-EXAM-GUIDELINES"
    event = "大學部普通生物學核心課程"

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

    builder.add_section("🎯 實驗室集合紀律與期中操作考時程：科學館二樓準時抵達與用具清單", sec1)
    builder.add_section("📊 複式光學顯微鏡調焦操作：低倍鏡找尋目標、細調節輪微調與玻片標本製作", sec2)
    builder.add_section("💼 細胞形態觀察記錄與課堂常規：十項全能趣味分享、實驗室安全與下課叮嚀", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部普通生物學核心課程"',
        'event: "大學部普通生物學核心課程"\ndate: "2024-10-24"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "普通生物學實驗-01-光學顯微鏡細胞觀察實作與期中考操作規範-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **實驗課程主題**：普通生物學實驗、複式光學顯微鏡標準操作流程（SOP）、暫時玻片標本製作與期中操作考評量規範  
> **授課教授**：授課講師（普通生物學實驗教授）  
> **核心模組**：Optical Microscopy, Specimen Preparation, Focus Adjustment, Cytological Observation, Lab Safety  
> **學習目標**：精熟光學顯微鏡由低倍鏡至高倍鏡之對焦操作程序，掌握動植物細胞切片觀察重點並嚴格恪遵實驗室安全紀律  
> **關聯文件**：[📄 完整原話逐字稿 (普通生物學實驗-01-光學顯微鏡細胞觀察實作與期中考操作規範-proofread.md)](./普通生物學實驗-01-光學顯微鏡細胞觀察實作與期中考操作規範-proofread.md)

---

## 🏛️ 複式光學顯微鏡標準對焦與操作工作流程 (Microscopy SOP)

```mermaid
flowchart TD
    Start["檢查顯微鏡外觀與接通光源"]
    LowPower["1. 旋轉物鏡轉盤至『最低倍率物鏡』(4x / 10x)"]
    Mount["2. 將載玻片置於載物台，標本對準中央通光孔"]
    Coarse["3. 眼睛由側面觀察，轉動粗調節輪使載物台上升至近距離"]
    Look["4. 雙眼由目鏡觀察，緩慢向下轉動粗調節輪直至見到模糊影像"]
    Fine["5. 轉動細調節輪 (微調輪)，直到細胞輪廓清晰對焦"]
    SwitchHigh["6. 如需高倍觀察，直接切換高倍物鏡，『僅使用細調節輪』微調"]

    Start --> LowPower
    LowPower --> Mount
    Mount --> Coarse
    Coarse --> Look
    Look --> Fine
    Fine --> SwitchHigh
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 光學顯微鏡對焦黃金原則
- **先低倍後高倍**：尋找視野目標物必須始終從最低倍率物鏡開始，不可直接跳用高倍物鏡，以防視野過小迷失或物鏡直接碰撞壓破蓋玻片。
- **高倍鏡下嚴禁粗調節輪**：切換至高倍物鏡（40x/100x）後，物鏡前端與載玻片距離極短，**僅能轉動細調節輪（Fine Focus）**，否則極易壓碎玻片標本並刮傷高精密透鏡。

### 2. 期中實驗操作考注意事項
- **準時與紀律**：操作考設有嚴格的跑站計時，遲到將直接扣減該站測驗時間。
- **標本真實記錄**：依據目鏡視野下實際觀察到的細胞壁、細胞核與葉綠體形態繪製紀錄，切忌抄襲教科書示意圖。
"""
    summary_file = OUT_DIR / "普通生物學實驗-01-光學顯微鏡細胞觀察實作與期中考操作規範-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_math_02()
    build_math_03()
    build_bio_01()
