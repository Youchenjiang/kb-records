#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Project Management course deliverables (PM-02, PM-03, PM-04):
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


def fix_pm_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in Project Management lectures."""
    replacements = [
        ("專業管理", "專案管理"),
        ("專員管理", "專案管理"),
        ("底區間去", "決策樹"),
        ("路子裡面", "Root 根節點裡面"),
        ("early finish", "Early Finish (最早完成時間)"),
        ("later start", "Late Start (最晚開始時間)"),
        ("later finish", "Late Finish (最晚完成時間)"),
        ("early early finish", "Early Finish"),
        ("early and later finish", "Late Finish"),
        ("六G", "生成式 AI"),
        ("茶點", "查核點 (Checkpoint)"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_pm_02():
    print("Building PM-02 (週一 上午09點02分)...")
    raw_path = RAW_DIR / "週一 上午09點02分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_typos(raw)

    title = "專案管理實務 Lesson 02：專案生命週期五大流程組、十大知識體系與工作分解結構 WBS"
    talk_id = "PM-02-LIFECYCLE-WBS"
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
    s1 = int(total_len * 0.18)
    s2 = int(total_len * 0.36)
    s3 = int(total_len * 0.54)
    s4 = int(total_len * 0.72)
    s5 = int(total_len * 0.88)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:s3])
    sec4 = segment_into_dialogue_paragraphs(cleaned[s3:s4])
    sec5 = segment_into_dialogue_paragraphs(cleaned[s4:s5])
    sec6 = segment_into_dialogue_paragraphs(cleaned[s5:])

    builder.add_section("🎯 專案管理導論：組織扁平化浪潮、知識提升與生成式 AI 工具整合實務", sec1)
    builder.add_section("📊 專案生命週期五大流程組：啟動、規劃、執行、監控與收尾循環", sec2)
    builder.add_section("💼 跨領域專案思維：職涯探索、動機激勵與利害關係人期望管理", sec3)
    builder.add_section("🛡️ 數位資產與專案備份：儲存介質管理、資訊安全與敏捷專案驅動力", sec4)
    builder.add_section("🏗️ 工作分解結構 WBS 核心架構：母項展開、工作包定義與產出物界定", sec5)
    builder.add_section("📝 專案收尾與驗收防禦：期中審查機制、變更防範與期末實作要求", sec6)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-10-21"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-02-專案生命週期與工作分解結構WBS-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    # Build Summary
    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：專案生命週期五大流程組、十大知識領域、工作分解結構（WBS）拆解原則與產出物驗收  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Project Life Cycle, WBS Work Breakdown, 100% Rule, Scope Management, Milestone Review  
> **學習目標**：掌握專案五大流程組與工作分解結構（WBS）之 100% 拆解原則，有效預防範疇蔓延與收尾驗收爭議  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-02-專案生命週期與工作分解結構WBS-proofread.md)](./專案管理-02-專案生命週期與工作分解結構WBS-proofread.md)

---

## 🏛️ 專案生命週期與五大流程組循環

```mermaid
flowchart LR
    subgraph PLC["專案管理五大流程組 (Project Life Cycle)"]
        Init["1. 啟動流程組 (Initiating)<br/>專案章程、利害關係人識別"]
        Plan["2. 規劃流程組 (Planning)<br/>範疇定義、WBS拆解、時程預算"]
        Exec["3. 執行流程組 (Executing)<br/>團隊指派、資源調度、產出交付"]
        Mon["4. 監控流程組 (Monitoring & Controlling)<br/>績效度量、偏差分析、變更控制"]
        Close["5. 收尾流程組 (Closing)<br/>成果驗收、經驗學習、專案結案"]
    end

    Init --> Plan
    Plan --> Exec
    Exec <--> Mon
    Mon --> Plan
    Mon --> Close
```

---

## 📊 工作分解結構 (WBS) 階層展開

```mermaid
flowchart TD
    Project["專案最高目標 (Level 0: 專案專案總目標)"]
    PhaseA["階段一 (Level 1: 需求分析與系統規格)"]
    PhaseB["階段二 (Level 1: 核心開發與模組建置)"]
    PhaseC["階段三 (Level 1: 整合測試與上線驗收)"]

    WP_A1["工作包 1.1: 訪談利害關係人與產出需求書"]
    WP_A2["工作包 1.2: 系統架構評估與規格審查"]

    WP_B1["工作包 2.1: 資料庫與後端 API 開發"]
    WP_B2["工作包 2.2: 前端使用者介面實作"]

    WP_C1["工作包 3.1: 單元與高並發壓力測試"]
    WP_C2["工作包 3.2: 使用者驗收測試 (UAT) 與結案報告"]

    Project --> PhaseA
    Project --> PhaseB
    Project --> PhaseC

    PhaseA --> WP_A1
    PhaseA --> WP_A2

    PhaseB --> WP_B1
    PhaseB --> WP_B2

    PhaseC --> WP_C1
    PhaseC --> WP_C2
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 專案的本質與組織變革
- **專案 vs. 常態營運**：專案具備「獨特性（Uniqueness）」與「暫時性（Temporary）」，目標達成後即解散交付；常態營運則具備重複性與持續性。
- **組織扁平化與知識爆炸**：現代企業因應快速變革，傳統科層式管理弱化，各項任務轉化為專案導向運作，仰賴專案經理統籌跨部門資源。

### 2. 工作分解結構 (WBS) 之 100% 原則
- **100% 原則 (100% Rule)**：WBS 樹狀圖所涵蓋的子工作包總和，必須 100% 等於母項任務的範疇，既無遺漏（Omission），亦不可衍生範疇蔓延（Scope Creep）。
- **工作包 (Work Package) 定義準則**：
  - 獨立性高、界面清晰。
  - 工時可精確預估（通常介於 8 到 80 小時之間）。
  - 單一負責人（Single Point of Contact, SPOC）。

### 3. 利害關係人溝通與收尾驗收防禦
- **專案收尾的非典型困難**：軟體專案常因前期未確立清晰「驗收標準（Acceptance Criteria）」，導致客戶在收尾階段提出大幅度介面或功能變更要求。
- **漸進明細（Progressive Elaboration）與期中審查**：在各個關鍵里程碑邀請客戶實機驗收（Milestone Review），提早暴露出落差，避免最終驗收時推倒重來。
"""
    summary_file = OUT_DIR / "專案管理-02-專案生命週期與工作分解結構WBS-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_pm_03():
    print("Building PM-03 (週三 上午09點09分)...")
    raw_path = RAW_DIR / "週三 上午09點09分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_typos(raw)

    title = "專案管理實務 Lesson 03：專案進度查核點設計、團隊溝通管理計畫與雙表追蹤機制"
    talk_id = "PM-03-CHECKPOINTS-COMMUNICATION"
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
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 專案營運模式、利潤評估與溝通管理規則設定", sec1)
    builder.add_section("📊 專案里程碑查核點管理表與跨部門問題解決機制", sec2)
    builder.add_section("💼 專案團隊有效傾聽、全員參與感與同理心激勵", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-10-23"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-03-專案進度查核點與團隊溝通管理實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：專案溝通管理計畫（Communication Plan）、查核點（Checkpoints）雙表追蹤與團隊同理激勵  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Communication Management, Checkpoint Design, Issue Tracking, Active Listening  
> **學習目標**：建立專案透明升級管道與節奏化會議制度，運用進度與障礙雙表確保專案交付無死角  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-03-專案進度查核點與團隊溝通管理實務-proofread.md)](./專案管理-03-專案進度查核點與團隊溝通管理實務-proofread.md)

---

## 🏛️ 專案溝通與問題升級機制 (Escalation Path)

```mermaid
flowchart TD
    Issue["成員執行過程中遭遇技術/資源瓶頸"]
    CheckSelf["能否內部協調解決?"]
    Immediate["即刻回報專案經理 (PM)<br/>（不等待定期週報）"]
    Resolve["共同評估處置對策<br/>調度支援資源"]
    Document["記錄於問題追蹤表<br/>（建立組織知識庫）"]
    Regular["常態進度於每週週報同步<br/>月度審查會回顧"]

    Issue --> CheckSelf
    CheckSelf -- "是" --> Regular
    CheckSelf -- "否" --> Immediate
    Immediate --> Resolve
    Resolve --> Document
    Document --> Regular
```

---

## 📋 專案進度與問題查核雙表運作模型

```mermaid
flowchart LR
    subgraph Table1["表一：里程碑與查核點管理表 (Milestone & Checkpoint Table)"]
        T1_A["項目代號與查核階段 (Phase)"]
        T1_B["明確應交付成果 (Deliverables)"]
        T1_C["指派負責人員 (Owner)"]
        T1_D["預定 vs. 實際完成日期 (Variance)"]
    end

    subgraph Table2["表二：障礙與解決方案追蹤表 (Issue & Resolution Log)"]
        T2_A["遭遇困難具體現象 (Problem Statement)"]
        T2_B["根因分析 (Root Cause)"]
        T2_C["採行之應對措施 (Action Plan)"]
        T2_D["經驗沉澱與團隊共享 (Lessons Learned)"]
    end

    Table1 <--> Table2
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 溝通管理計畫的遊戲規則制定
- **即時回報原則**：專案遭遇卡點時，應主動向 PM 尋求協調，嚴禁將問題壓箱至例行會議才揭露，避免損失黃金應對時效。
- **節奏化會議**：
  - **每週週報**：回顧上週完成事項、本週規劃、現存阻礙。
  - **月度審查會議**：針對關鍵里程碑進行整體預算、進度與範疇對齊。

### 2. 查核點 (Checkpoint) 的設計哲學
- **明確產出物判定**：查核點不可流於抽象趴數（如「完成 80%」），必須有清晰的交付物判定依據（如「規格書簽署完成」、「第一版 API 測試通過」）。
- **知識資產沉澱**：記錄成員解決問題之歷程，供團隊其他專案或後續人員借鑑，降低重複試錯成本。

### 3. 軟性管理：傾聽與全員參與感
- **同理心傾聽**：專案經理若一味強推決策，易導致沉默或消極抗拒；多方傾聽沉默成員的想法，能提高團隊向心力與認同感。
- **激勵團隊自驅力**：當團隊成員提出的回饋在專案中被具體採納時，能極大化其成就感與責任擔當。
"""
    summary_file = OUT_DIR / "專案管理-03-專案進度查核點與團隊溝通管理實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_pm_04():
    print("Building PM-04 (週三 上午10點12分)...")
    raw_path = RAW_DIR / "週三 上午10點12分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_typos(raw)

    title = "專案管理實務 Lesson 04：關鍵路徑法 CPM、PERT 三點時程估算、快速跟進風險與變更控制"
    talk_id = "PM-04-CPM-PERT-CHANGE-CONTROL"
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
    s1 = int(total_len * 0.40)
    s2 = int(total_len * 0.75)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 關鍵路徑法 CPM、最早最晚時間計算與 PERT 三點估算法", sec1)
    builder.add_section("📊 專案趕工、快速跟進 Fast Tracking 風險與變更管理控制", sec2)
    builder.add_section("💼 專案職場人際溝通障礙排解與實務綜合回顧", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-10-23"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-04-關鍵路徑法CPM時程估算與專案變更控制-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """

> **課程主題**：關鍵路徑法（CPM）、PERT 三點估算、時程壓縮（Crashing vs. Fast Tracking）與變更控制程序  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Critical Path Method, PERT Estimation, Float/Slack, Schedule Compression, Change Control  
> **學習目標**：精熟正推法與逆推法計算活動最早／最晚起訖時間，評估快速跟進返工風險並建立變更控制基準線  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-04-關鍵路徑法CPM時程估算與專案變更控制-proofread.md)](./專案管理-04-關鍵路徑法CPM時程估算與專案變更控制-proofread.md)

---

## 🏛️ 關鍵路徑法 (CPM) 時間計算與浮動時間結構

```mermaid
flowchart LR
    A["活動 A<br/>ES:0, D:3, EF:3"] --> B["活動 B<br/>ES:3, D:4, EF:7"]
    A --> C["活動 C<br/>ES:3, D:2, EF:5"]
    B --> D["活動 D (關鍵路徑)<br/>ES:7, D:5, EF:12"]
    C --> D
    
    style D fill:#ffdddd,stroke:#ff0000,stroke-width:2px
    style B fill:#ffdddd,stroke:#ff0000,stroke-width:2px
    style A fill:#ffdddd,stroke:#ff0000,stroke-width:2px
```

---

## ⚡ 時程壓縮技術比較：趕工 (Crashing) vs. 快速跟進 (Fast Tracking)

```mermaid
flowchart TD
    ScheduleCompression["專案時程壓縮策略"]
    
    Crashing["趕工 (Crashing)<br/>- 投入額外資源/加班<br/>- 代價：成本直接上升<br/>- 風險：邊際效應遞減、疲乏"]
    FastTracking["快速跟進 (Fast Tracking)<br/>- 將原本循序的活動改為並行<br/>- 例：未完成架構即開始寫扣<br/>- 代價：高額返工 (Rework) 風險"]

    ScheduleCompression --> Crashing
    ScheduleCompression --> FastTracking
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. CPM 關鍵路徑演算法核心公式
- **正推法 (Forward Pass)**：計算最早時間
  - $EF = ES + \\text{Duration}$
  - 當後續活動有多個前置活動時，取最大值：$ES = \\max(EF_\\text{predecessors})$。
- **逆推法 (Backward Pass)**：計算最晚時間
  - $LS = LF - \\text{Duration}$
  - 當前置活動有多個後續活動時，取最小值：$LF = \\min(LS_\\text{successors})$。
- **總浮動時間 (Total Float / Slack)**：
  - $\\text{Float} = LS - ES = LF - EF$
  - **關鍵路徑 (Critical Path)** 即為總浮動時間為 0（或最小）之活動路徑，決定了整個專案的最短完工時間。任何關鍵路徑上的延誤都將直接導致專案完工日推遲。

### 2. PERT 三點時程估算 (Three-Point Estimating)
- **貝他分佈 (Beta Distribution) 加權平均公式**：
  - $T_e = \\frac{O + 4M + P}{6}$
  - 其中 $O$ 為最樂觀時間（Optimistic）、$M$ 為最可能時間（Most Likely）、$P$ 為最悲觀時間（Pessimistic）。
- 適用於具備不確定性或創新性的研發專案，能有效平滑樂觀偏差。

### 3. 專案變更控制程序 (Change Control)
- **凡是專案必有變更**：任何範疇、時程、預算之變更請求（Change Request），均需評估其對專案三大限制（三重限制：範疇、時間、成本）之連鎖衝擊。
- **變更控制委員會 (CCB)**：經由正式審查、量化衝擊分析與客戶書面確認後，始得修改專案基準線（Baseline）。
"""
    summary_file = OUT_DIR / "專案管理-04-關鍵路徑法CPM時程估算與專案變更控制-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_pm_02()
    build_pm_03()
    build_pm_04()
