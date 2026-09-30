#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 4-University Undergraduate Professional Courses Deliverables:
- 專案管理實務 (週二 上午10點50分)
- 電腦網路實習：UTP 跳線製作 (週二 16點05分)
- 雲端運算導論 (週四 下午02點03分)
Follows PROOFREAD_RULES.md, ScenarioType.CLASSROOM_LECTURE, and tests/test_proofread_linter.py.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2024-UndergraduateCourses"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"

REPLACEMENTS = [
    (r"UTP", "UTP（無遮蔽雙絞線）"),
    (r"STP", "STP（遮蔽雙絞線）"),
    (r"FTP", "FTP（鋁箔遮蔽雙絞線）"),
    (r"雙絞線", "雙絞線 (Twisted Pair)"),
    (r"虛運化", "虛擬化"),
    (r"毛利", "毛利 (Gross Margin)"),
    (r"直接成本", "直接成本 (Direct Cost)"),
    (r"間接成本", "間接成本 (Indirect Cost)"),
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
        if current_len >= 220 or s.endswith("好。") or s.endswith("OK。"):
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
        student_triggers = ["大家好，我們是第四組", "這是我們的組員", "老師請問", "是這樣嗎？"]
        if any(trig in p_clean for trig in student_triggers):
            formatted_paras.append(f"**【學員】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_pm():
    print("Building Project Management Deliverable...")
    raw = (RAW_DIR / "週二 上午10點50分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "專案管理實務 Lesson 01：專案成本管理、直接成本 vs. 間接成本與預算編列技術"
    talk_id = "PM-01-COST-BUDGETING"
    event = "大學部專案管理實務課程"

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

    builder.add_section("🎯 專案財務結構核心：總合約收入、直接成本與代理商毛利率解析", sec1)
    builder.add_section("📊 間接成本分攤機制：辦公行政、水電折舊與專案不可預見準備金", sec2)
    builder.add_section("💼 企業接案成本模型建立：WBS 工作分解結構與工時單價精確預估", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2025-12-09"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-01-專案直接成本與預算編列實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：專案成本管理（Cost Management）、直接成本／間接成本拆解、毛利率計算與預算編列  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Project Cost Estimation, Direct & Indirect Costs, Gross Margin, WBS Costing  
> **學習目標**：理解專案損益結構、精準拆解執行團隊直接成本與企業營運管銷費用  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-01-專案直接成本與預算編列實務-proofread.md)](./專案管理-01-專案直接成本與預算編列實務-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Revenue["專案合約總收入 (Total Revenue)"] --> DC["直接成本 (Direct Cost: 研發工時、專屬軟硬體、專用伺服器)"]
    Revenue --> GM["毛利 (Gross Margin = 營收 - 直接成本)"]
    GM --> IC["間接成本 / 營業費用 (Indirect Cost: 房租、水電、法務人資攤提)"]
    GM --> NP["淨利 (Net Profit = 毛利 - 間接成本 - 稅賦)"]
    DC --> Budget["依 WBS 工作項目編列專案基線預算 (Cost Baseline)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **直接成本 vs. 間接成本**：直接成本是專案不接就不會發生的成本（如專案外包費、專案成員工時）；間接成本是公司日常維持必須分攤的管銷費用。
2. **毛利是專案存亡關鍵**：報價時若只估算直接成本而忽略間接成本分攤與風險準備金，接案愈多虧損愈大。
"""
    summary_file = OUT_DIR / "專案管理-01-專案直接成本與預算編列實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_cabling():
    print("Building UTP Cabling Lab Deliverable...")
    raw = (RAW_DIR / "週二 16點05分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "電腦網路實習 Lesson 01：UTP 雙絞線製作、T568A/B 跳線標準與傳輸衰減量測"
    talk_id = "NET-LAB-01"
    event = "大學部電腦網路實驗課程"

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

    builder.add_section("🎯 實體層傳輸媒介剖析：UTP、STP 與 FTP 遮蔽結構特性比較", sec1)
    builder.add_section("🔌 T568A 與 T568B 腳位對應色碼標準：平行線 vs. 跳線（Crossover）製作", sec2)
    builder.add_section("⚡ 壓線鉗實作步驟、RJ-45 接頭壓接技巧與測線器傳輸連通性驗證", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部電腦網路實驗課程"',
        'event: "大學部電腦網路實驗課程"\ndate: "2025-12-09"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "電腦網路實驗-01-UTP雙絞線跳線製作與衰減標準-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：實體層網路線材、UTP/STP 結構比較、T568A/B 色碼標準與 RJ-45 壓接實務  
> **指導評審**：授課講師（網路實驗授課教師）  
> **發表團隊**：實習第四組學員群  
> **核心模組**：Physical Layer Cabling, UTP vs. STP, T568A/T568B Wiring, Cable Continuity Testing  
> **學習目標**：理解雙絞抗電磁干擾原理、親手壓接標準 RJ-45 網路線並通過測線器驗證  
> **關聯文件**：[📄 完整原話逐字稿 (電腦網路實驗-01-UTP雙絞線跳線製作與衰減標準-proofread.md)](./電腦網路實驗-01-UTP雙絞線跳線製作與衰減標準-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Cable["網路傳輸線材"] --> UTP["UTP (非遮蔽: 成本低、柔軟度佳、最普及)"]
    Cable --> STP["STP / FTP (金屬箔/編織網遮蔽: 抗強電磁干擾機房環境)"]
    UTP --> Wiring{"接頭線序標準 (TIA/EIA)"}
    Wiring --> B["T568B: 白橙、橙、白綠、藍、白藍、綠、白棕、棕"]
    Wiring --> A["T568A: 白綠、綠、白橙、藍、白藍、橙、白棕、棕"]
    B --> Type1["兩端皆為 T568B: 平行線 (Straight-through: 接 PC 到 Switch)"]
    A & B --> Type2["一端 A、一端 B: 跳線 (Crossover: 接同質設備 PC 到 PC)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **雙絞（Twist）抗干擾原理**：藉由兩條絕緣銅線緊密纏繞，使外部噪聲在相鄰半周上感應出大小相等、方向相反的噪聲電流相互抵消。
2. **現代 Auto-MDIX 普及**：現代交換器與網卡普遍內建 Auto-MDIX 自動翻轉功能，但掌握 T568A/B 規範與實體壓接仍為網路工程師必備基本功。
"""
    summary_file = OUT_DIR / "電腦網路實驗-01-UTP雙絞線跳線製作與衰減標準-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_cloud():
    print("Building Cloud Virtualization Deliverable...")
    raw = (RAW_DIR / "週四 下午02點03分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "雲端運算導論 Lesson 01：雲端本質剖析、伺服器虛擬化與現代資料中心集中運算"
    talk_id = "CLOUD-01"
    event = "大學部雲端運算架構課程"

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

    builder.add_section("🎯 雲端運算本質剖析：從實體水蒸氣比喻看電腦硬體架構解耦與數位化", sec1)
    builder.add_section("💻 伺服器虛擬化核心：Hypervisor 抽象化層、虛擬機器與資源彈性池化（Pooling）", sec2)
    builder.add_section("🏢 集中式現代資料中心演進：自建地端主機 vs. 公有雲出租經濟效益權衡", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部雲端運算架構課程"',
        'event: "大學部雲端運算架構課程"\ndate: "2024-10-17"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "雲端運算-01-虛擬化架構與資料中心運算基礎-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：雲端運算導論、電腦硬體虛擬化本質、資源彈性調度與現代資料中心  
> **授課教授**：授課講師（資管系雲端架構授課教授）  
> **核心模組**：Cloud Computing Fundamentals, Hardware Decoupling, Virtualization & Hypervisor  
> **學習目標**：釐清「雲」背後的物理實體主機本質、理解虛擬化抽象層如何實現資源池化  
> **關聯文件**：[📄 完整原話逐字稿 (雲端運算-01-虛擬化架構與資料中心運算基礎-proofread.md)](./雲端運算-01-虛擬化架構與資料中心運算基礎-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Physical["實體資料中心硬體 (CPU, RAM, Storage, Network)"] --> Hypervisor["虛擬化管理層 (Hypervisor / 抽象化層)"]
    Hypervisor --> Pool["多租戶資源池 (Resource Pooling)"]
    Pool --> VM1["虛擬機器 1 (Tenant A)"]
    Pool --> VM2["虛擬機器 2 (Tenant B)"]
    Pool --> VM3["虛擬機器 3 (Tenant C)"]
    Pool --> Elastic["彈性自動擴展 (Rapid Elasticity: 隨負載動態增減)"]
    Elastic --> Meter["按用量計費 (Measured Service: 隨用隨付)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **雲端的真實本質**：雲端並非虛無飄渺，而是「別人的電腦」——透過高度自動化與虛擬化軟體，將集中在超大型資料中心的實體硬體切分為彈性運算單元。
2. **虛擬化（Virtualization）價值**：傳統單一主機運載率僅 10%~15%；透過虛擬化可將單一伺服器利用率提升至 70%~80%，大幅降低硬體與機房能耗成本。
"""
    summary_file = OUT_DIR / "雲端運算-01-虛擬化架構與資料中心運算基礎-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_pm()
    build_cabling()
    build_cloud()
