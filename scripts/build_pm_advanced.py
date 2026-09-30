#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Advanced Project Management course deliverables (PM-05, PM-06, PM-07):
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


def fix_pm_advanced_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in Advanced PM lectures."""
    replacements = [
        ("專業管理", "專案管理"),
        ("專員管理", "專案管理"),
        ("W B的展開", "WBS 的展開"),
        ("高中低", "高／中／低風險級別"),
        ("利害關係又可以", "利害關係人又可以"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_pm_05():
    print("Building PM-05 (週二 上午09點47分)...")
    raw_path = RAW_DIR / "週二 上午09點047分".replace("047", "47") / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_advanced_typos(raw)

    title = "專案管理實務 Lesson 05：專案組織人力配置、職能矩陣與外包採購決策"
    talk_id = "PM-05-ORGANIZATION-OUTSOURCING"
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

    builder.add_section("🎯 專案組織架構評估：企業現有資源盤點與專案職能需求對稱性", sec1)
    builder.add_section("📊 專案人力聘僱之陷阱：專用型人力閒置成本與組織靈活度維持", sec2)
    builder.add_section("💼 內調 vs. 外包決策準則：採購策略、外包合約管理與課堂綜合討論", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-11-19"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-05-組織人力配置職能矩陣與外包採購決策-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：專案組織架構（Organizational Structure）、人力資源配置、自製或外購（Make-or-Buy Analysis）與外包採購管理  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Resource Allocation, Skills Matrix, Staffing Acquisition, Make-or-Buy Decision, Outsourcing Risk  
> **學習目標**：掌握專案組織與職能矩陣之匹配原則，精確評估專屬人力招聘之後續閒置風險，並建立理性外包決策架構  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-05-組織人力配置職能矩陣與外包採購決策-proofread.md)](./專案管理-05-組織人力配置職能矩陣與外包採購決策-proofread.md)

---

## 🏛️ 專案人力資源取得途徑決策樹 (Staffing Decision Tree)

```mermaid
flowchart TD
    Need["專案產生特定技術/職能需求"]
    CheckInternal{"公司內部現有團隊<br/>是否具備相應職能?"}
    
    InternalTransfer["內部借調 (Internal Transfer)<br/>跨部門協調、矩陣式支援"]
    CheckLongTerm{"該職能是否屬於<br/>公司長期核心業務?"}
    
    Hire["對外招聘正職員工 (Hire)<br/>長期核心研發專才"]
    Outsource["外包或顧問採購 (Outsource)<br/>專案結束後立即終止合約，無冗員負擔"]

    Need --> CheckInternal
    CheckInternal -- "是" --> InternalTransfer
    CheckInternal -- "否" --> CheckLongTerm
    CheckLongTerm -- "長期核心" --> Hire
    CheckLongTerm -- "專案性/短暫" --> Outsource
```

---

## ⚖️ 專案人員聘僱 vs. 外包採購權衡

```mermaid
flowchart LR
    subgraph DirectHire["專屬人力直接招聘 (Direct Hire)"]
        H1["優點：掌控度高、團隊凝聚力好"]
        H2["風險：專案結束後成為組織冗員，難以轉移至其他專案"]
    end

    subgraph Outsourcing["外包委外採購 (Outsourcing)"]
        O1["優點：彈性靈活、成本依產出結算、無長期負擔"]
        O2["風險：供應商交期風險、關鍵技術流失、溝通協調成本"]
    end

    DirectHire <--> Outsourcing
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 專案組織能力盤點與對稱性分析
- **職能落差識別**：在專案啟動時，必須比對 WBS 工作包所需的技術能力與現有成員的技能矩陣（Skills Matrix）。
- **組織靈活性優先**：現代敏捷型企業應避免因為單一專案的需求而盲目擴張編制，優先考慮組織內調（Staff Reallocation）。

### 2. 「專案專聘」的高昂隱形成本
- **專案專聘的後遺症**：若專門為某一案子聘請特定專家，一旦該專案結案，若公司後續缺乏同類型專案接續，此專案聘任人員將陷入無案可做的閒置窘境，企業甚至面臨遣散或冗員成本。
- **解決方案**：短中期或非核心專用技術，應優先採取外包（Outsourcing）或顧問合作模式。

### 3. 外包採購合約管理的關鍵
- **明確驗收標準（SOW: Statement of Work）**：委外案必須具備高度量化之交付物清單與驗收規範，避免履約爭議。
- **里程碑分期撥款**：將外包付款進度與實機驗收點（Milestones）緊密綁定，有效牽引供應商進度與品質。
"""
    summary_file = OUT_DIR / "專案管理-05-組織人力配置職能矩陣與外包採購決策-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_pm_06():
    print("Building PM-06 (週二 下午01點12分)...")
    raw_path = RAW_DIR / "週二 下午01點12分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_advanced_typos(raw)

    title = "專案管理實務 Lesson 06：極限專案成本模擬、風險矩陣與利害關係人管理"
    talk_id = "PM-06-SIMULATION-RISK-STAKEHOLDERS"
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

    builder.add_section("🎯 極限專案案例剖析：太空船高擬真模擬器造價與事前驗證成本哲學", sec1)
    builder.add_section("📊 風險管理遊戲規則：WBS 展開、高中低風險矩陣量化與對策制訂", sec2)
    builder.add_section("💼 利害關係人分析矩陣：內部與外部維度、支援與抗拒者化解策略", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-11-19"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-06-極限專案成本模擬風險矩陣與利害關係人管理-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：極限專案成本架構、高擬真模擬機事前驗證、風險評估矩陣（Risk Matrix）與利害關係人參與管理  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Extreme Project Management, Simulation Costs, Risk Matrix, Stakeholder Analysis, Resistance Handling  
> **學習目標**：理解極限專案中高昂驗證模擬的必要性，掌握風險發生機率與衝擊矩陣，並建立利害關係人抗拒之轉化機制  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-06-極限專案成本模擬風險矩陣與利害關係人管理-proofread.md)](./專案管理-06-極限專案成本模擬風險矩陣與利害關係人管理-proofread.md)

---

## 🏛️ 風險機率與衝擊量化矩陣 (Probability-Impact Matrix)

```mermaid
flowchart TD
    subgraph RiskMatrix["風險等級判定矩陣"]
        direction TB
        High["🔴 高風險 (High Risk)<br/>衝擊極大、機率高<br/>對策：規避 (Avoid) 或重點減緩 (Mitigate)"]
        Med["🟡 中風險 (Medium Risk)<br/>衝擊或機率中等<br/>對策：轉移 (Transfer) 或減緩 (Mitigate)"]
        Low["🟢 低風險 (Low Risk)<br/>衝擊小、機率低<br/>對策：接受 (Accept) 並列入觀察清單 (Watchlist)"]
    end
```

---

## 👥 利害關係人權力與利益矩陣 (Power-Interest Grid)

```mermaid
flowchart LR
    subgraph Grid["利害關係人分類管理策略"]
        direction TB
        P_High_I_High["權力高 / 利益高 (Key Players: 出資主管、主要客戶)<br/>👉 重點管理、緊密參與 (Manage Closely)"]
        P_High_I_Low["權力高 / 利益低 (監管機構、法規單位)<br/>👉 令其滿意 (Keep Satisfied)"]
        P_Low_I_High["權力低 / 利益高 (基層使用者、一般團隊成員)<br/>👉 隨時告知最新資訊 (Keep Informed)"]
        P_Low_I_Low["權力低 / 利益低 (外圍利害關係人)<br/>👉 最低限度監控 (Monitor with Minimal Effort)"]
    end
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 極限專案與高擬真模擬成本哲學
- **事前驗證的高昂代價**：以載人太空船專案為例，太空人訓練與極端情境模擬器的造價往往逼近甚至超越專案實體本體。然而相較於飛行發射失敗的全盤毀滅，事前的高額模擬投入是絕對必要且最合算的風險控制手段。
- **軟體專案借鏡**：在金融交易或核心伺服器專案中，打造高並發壓力測試環境與預發行環境（Staging Environment）即等同於「模擬機」，能防範災難性生產事故。

### 2. 風險管理遊戲規則先行
- **明確風險級別準則**：在團隊展開 WBS 與風險評估前，PM 必須預先定義何謂「高、中、低風險」（例如：延誤 1 週 vs. 1 個月；損失 10 萬 vs. 100 萬），避免團隊成員因個人主觀偏差而低估系統性風險。

### 3. 利害關係人抗拒應對之道
- **識別關鍵利害關係人**：分清「出資者（Sponsor）」、「核心團隊」、「審查主管」與「終端用戶」。
- **化解抗拒策略**：抗拒者通常源於對專案帶來改變的不安全感或利益受損。PM 應提早與抗拒者一對一溝通，探尋其根本顧慮，並在專案目標中融入對其有利的配套措施，將阻力化為助力。
"""
    summary_file = OUT_DIR / "專案管理-06-極限專案成本模擬風險矩陣與利害關係人管理-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_pm_07():
    print("Building PM-07 (週二 下午02點52分)...")
    raw_path = RAW_DIR / "週二 下午02點52分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_advanced_typos(raw)

    title = "專案管理實務 Lesson 07：跨世代研發團隊協作、專家整合與溝通領導實務"
    talk_id = "PM-07-CROSS-GEN-COLLABORATION"
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

    builder.add_section("🎯 專案團隊多元性：頂尖技術與充分協作的平衡、孤鳥型成員管理挑戰", sec1)
    builder.add_section("📊 跨世代研發團隊文化：新世代手遊軟體公司創新活力與管理思維革新", sec2)
    builder.add_section("💼 雙軌配置與團隊彈性：主副責任制、溝通障礙排除與期末實務綜合反思", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-11-19"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-07-跨世代研發團隊協作與領導溝通實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：專案團隊建立（Team Building）、跨世代協作、孤鳥型技術專家管理與雙軌主副責任制  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Team Dynamics, Cross-Generation Collaboration, Technical Lone Wolves, Pairing System  
> **學習目標**：掌握多樣化團隊動態管理心法，妥善調處技術天才與團隊溝通落差，並建立主副雙軌備援制確保專案永續交付  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-07-跨世代研發團隊協作與領導溝通實務-proofread.md)](./專案管理-07-跨世代研發團隊協作與領導溝通實務-proofread.md)

---

## 🏛️ 專案團隊協作雙軌制 (Primary-Secondary Pairing Model)

```mermaid
flowchart TD
    Task["關鍵專案模組任務"]
    
    subgraph Pairing["主副雙軌責任制 (Pairing Setup)"]
        Primary["主負責人 (Primary / 核心技術專家)<br/>負責核心演算法與架構突破"]
        Secondary["副手 / 協同者 (Secondary / 團隊橋樑)<br/>負責代碼審查、文件記錄與跨組協調"]
    end

    Task --> Primary
    Task --> Secondary
    Primary <--> Secondary
    Secondary -- "對外同步與跨部門交流" --> External["專案經理 (PM) 與其他模組"]
```

---

## ⚡ 「孤鳥型」技術天才之整合策略

```mermaid
flowchart LR
    subgraph Challenge["孤鳥型成員特質"]
        C1["個人技術能力極其頂尖"]
        C2["不屑或不善與團隊社交互動"]
        C3["容易成為專案單點故障 (SPOF)"]
    end

    subgraph Solution["PM 管理介入解方"]
        S1["不強求其承擔行政溝通，保留純粹技術戰場"]
        S2["指派高同理心副手進行緩衝式對接"]
        S3["定期要求輸出架構文檔或程式碼留痕"]
    end

    Challenge --> Solution
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 團隊協作重於個人英雄主義
- **孤鳥成員的專案風險**：部分技術能力頂尖的工程師習慣單打獨鬥、拒絕溝通，在專案管理中這類「孤鳥」若無良好機制包裝，將導致模組黑盒子化，一旦其離職或生病，整個專案將陷入停擺。
- **主副責任制（Primary-Secondary Setup）**：重要工作包指派一名主負責人與一名副手。主負責人主攻技術攻堅，副手協助溝通協調與知識備份，兼顧效率與專案風險分散。

### 2. 跨世代團隊的領導新思維
- **手遊與新創團隊生態**：以 30 歲以下年輕工程師為主體的研發團隊，思維跳躍、追求酷炫與自主性。傳統威權由上而下的命令式管理不再奏效，專案領導者需轉型為「教練與僕人式領導（Servant Leadership）」，營造彈性自主的氛圍以激發其創造力。
"""
    summary_file = OUT_DIR / "專案管理-07-跨世代研發團隊協作與領導溝通實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_pm_05()
    build_pm_06()
    build_pm_07()
