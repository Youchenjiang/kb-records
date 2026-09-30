#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Final Project Management course deliverables (PM-08, PM-09, PM-10, PM-11):
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


def fix_pm_final_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in PM final lectures."""
    replacements = [
        ("專業管理", "專案管理"),
        ("專員管理", "專案管理"),
        ("PAC 是八百", "BAC 是 800 萬"),
        ("PAC", "BAC (完工總預算)"),
        ("絕英案", "捷運工程案"),
        ("高雄絕英案", "高雄捷運案"),
        ("臺北絕英案", "台北捷運案"),
        ("一零一大", "台北 101 大樓"),
        ("盈失", "品質規格"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_pm_08():
    print("Building PM-08 (週一 下午03點02分)...")
    raw_path = RAW_DIR / "週一 下午03點02分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_final_typos(raw)

    title = "專案管理實務 Lesson 08：專案角色授權、組織權責劃分與跨部門協調"
    talk_id = "PM-08-ROLE-DELEGATION-GOVERNANCE"
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

    builder.add_section("🎯 專案管理角色定義：機能主管 vs. 專案經理權責邊界與授權機制", sec1)
    builder.add_section("📊 組織內部跨部門協調挑戰：資源競爭、排程衝突與共識建立", sec2)
    builder.add_section("💼 專案治理落實：授權層級設計、審查機制與實作現場反思", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-11-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-08-專案角色授權與組織權責矩陣劃分-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：專案治理架構（Project Governance）、角色授權、矩陣型組織權責劃分與跨部門資源協調  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Project Governance, Authority Delegation, Matrix Organization, RACI Matrix, Resource Conflict  
> **學習目標**：釐清弱矩陣、平衡矩陣與強矩陣組織中 PM 之授權邊界，建立透明之決策升級與授權層級體系  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-08-專案角色授權與組織權責矩陣劃分-proofread.md)](./專案管理-08-專案角色授權與組織權責矩陣劃分-proofread.md)

---

## 🏛️ 矩陣型組織架構中專案經理與機能主管權責邊界

```mermaid
flowchart TD
    CEO["企業總經理 / 執行長"]
    
    subgraph FunctionalManagers["機能主管 (Functional Managers)"]
        FM1["研發部主管<br/>(掌握技術標準與考績)"]
        FM2["維運部主管<br/>(掌握硬體伺服器資源)"]
    end

    subgraph ProjectManagers["專案主管 (Project Managers)"]
        PM["專案經理 (Project Manager)<br/>(掌握專案時程、預算、交付範疇)"]
    end

    TeamMember["跨部門專案成員 (Project Staff)"]

    CEO --> FunctionalManagers
    CEO --> ProjectManagers
    FM1 -- "決定『由誰做』(Who) 與專業考核" --> TeamMember
    FM2 -- "調配設備資源" --> TeamMember
    PM -- "決定『做什麼』(What) 與『何時完成』(When)" --> TeamMember
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 專案角色的雙重報告線（Dual Reporting）
- **矩陣型組織挑戰**：專案成員同時向機能主管（Functional Manager）與專案經理（PM）報告，極易產生指令衝突。
- **權限清晰劃分**：PM 主掌專案工作範疇、時程與交付物；機能主管主掌人員專業訓練、薪酬考績與長期職涯分配。

### 2. 授權與責任落實
- **授權層級設計**：專案經理在預算與時程調整上應具備明確的自主核決權限，避免枝微末節的變更皆需向上請示而喪失專案敏捷度。
"""
    summary_file = OUT_DIR / "專案管理-08-專案角色授權與組織權責矩陣劃分-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_pm_09():
    print("Building PM-09 (週一 下午03點05分)...")
    raw_path = RAW_DIR / "週一 下午03點05分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_final_typos(raw)

    title = "專案管理實務 Lesson 09：專案團隊心理調適、聯考裝杯標哲學與成果驗收前瞻"
    talk_id = "PM-09-TEAM-PSYCHOLOGY-READINESS"
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

    builder.add_section("🎯 專案收尾心理調適：充足準備後的放鬆藝術與聯考裝杯標哲學", sec1)
    builder.add_section("📊 人才價值與職場多樣性：班級中段學生創業實務與學術專業分工反思", sec2)
    builder.add_section("💼 專案成果預備度檢核：上線前穩定度驗證、手環穿戴裝置與期末演練前瞻", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-11-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-09-專案團隊心理調適與成果驗收前瞻-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：專案團隊心理調適、驗收前壓力管理、個人專業適性發展與專案交付前預備度檢核  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Stress Management, Readiness Review, Career Diversity, Psychological Safety, Final Delivery  
> **學習目標**：掌握專案衝刺收尾期的團隊心理韌性建設，建立上線前的冷靜驗收心態並正確認知多元人才價值  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-09-專案團隊心理調適與成果驗收前瞻-proofread.md)](./專案管理-09-專案團隊心理調適與成果驗收前瞻-proofread.md)

---

## 🏛️ 專案收尾衝刺壓力與心理調適曲線 (Yerkes-Dodson 模型)

```mermaid
flowchart LR
    Low["壓力過低 (怠惰無目標)"] --> Optimal["最適壓力區 (充分準備 + 冷靜放鬆)<br/>👉 產出效率最高、系統錯誤最少"]
    Optimal --> High["壓力過高 (恐慌混亂、通宵返工)<br/>👉 疲倦導致重大生產事故"]
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 充足準備後的「放鬆哲學」
- **聯考裝杯標比喻**：專案上線前最後關頭，最重要的不再是臨時盲目寫新功能，而是「放鬆心情、檢查清單、確保既有架構穩定運作」。慌亂改動往往是生產事故的元凶。
- **心理韌性**：專案經理的從容定見是穩定整個團隊軍心的核心錨點。

### 2. 人才多樣性與實務生存力
- **學業成績 vs. 商業實踐**：會讀書的人適合走純學術或研究型道路；而能在複雜商業環境中賺錢破局的，往往是具備高情商、人脈整合與業務膽識的成員。專案團隊必須包容各具所長的多元人才。
"""
    summary_file = OUT_DIR / "專案管理-09-專案團隊心理調適與成果驗收前瞻-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_pm_10():
    print("Building PM-10 (週三 下午01點05分)...")
    raw_path = RAW_DIR / "週三 下午01點05分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_final_typos(raw)

    title = "專案管理實務 Lesson 10：專案衝突解決矩陣、強勢成員處置與實獲值 EVM 控制"
    talk_id = "PM-10-CONFLICT-RESOLUTION-EVM"
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

    builder.add_section("🎯 溝通模式與事實導向：直球溝通、事實證據展現與迂迴鋪陳之利弊剖析", sec1)
    builder.add_section("📊 團隊衝突解決五大策略：強迫破壞性、強勢核心專家風險隔離與備援培訓", sec2)
    builder.add_section("💼 實獲值管理 EVM 動態策略調整：時程超前與成本落後之動態平衡修正", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-11-27"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-10-專案衝突解決矩陣與實獲值EVM動態控制-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：專案溝通衝突解決模式（Thomas-Kilmann 模型）、破壞性強勢成員處置、事實證據導向與實獲值管理（EVM）動態策略校準  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Conflict Resolution, Toxic Experts Handling, Fact-Based Communication, EVM Dynamic Control  
> **學習目標**：精熟專案衝突之五種應對手法，掌握強勢破壞型技術專家之風險隔離備援方案，並透過 EVM 動態調整時程與預算  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-10-專案衝突解決矩陣與實獲值EVM動態控制-proofread.md)](./專案管理-10-專案衝突解決矩陣與實獲值EVM動態控制-proofread.md)

---

## 🏛️ 專案衝突解決五大模式 (Thomas-Kilmann Conflict Mode)

```mermaid
flowchart TD
    subgraph TKI["衝突處置風格矩陣"]
        direction TB
        Collab["🤝 合作 (Collaborating / Problem Solving)<br/>雙贏最佳解，尋找整合方案"]
        Force["⚡ 強迫 (Forcing / Competing)<br/>單方強推，易造成兩敗俱傷與團隊怨懟"]
        Compromise["⚖️ 妥協 (Compromising)<br/>雙方各退一步，折衷方案"]
        Smooth["🕊️ 安撫/包容 (Accommodating)<br/>強調共識，暫時擱置爭議"]
        Avoid["🏃 迴避 (Avoiding / Withdrawal)<br/>拖延逃避，未真正解決根本問題"]
    end
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 事實與證據導向溝通（Fact-Based）
- **避免情緒化爭執**：專案出現爭議時，PM 應要求雙方拿出客觀數據、測試報告與系統 Log 說話，以事實證據（Evidence）為決策基準，杜絕主觀臆測。

### 2. 強勢破壞型專家的風險處置
- **兩敗俱傷的強迫風格**：部分核心成員雖具技術能力，但處處強推己見、霸凌隊友。
- **風險防禦對策**：PM 必須在不激化衝突的前提下，私下培訓備援人選（Shadowing / Backup），逐步降低專案對單一破壞型人員的依賴，最終在適當時機將其移出團隊。

### 3. EVM 動態調整循環
- **持續修正策略**：若專案呈現「時程超前但成本超支」，應評估是否投入過多加班費用；若「成本節省但進度落後」，需評估是否需適度增補外包資源以追回進度。
"""
    summary_file = OUT_DIR / "專案管理-10-專案衝突解決矩陣與實獲值EVM動態控制-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_pm_11():
    print("Building PM-11 (週三 下午03點04分)...")
    raw_path = RAW_DIR / "週三 下午03點04分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_pm_final_typos(raw)

    title = "專案管理實務 Lesson 11：專案品質度量、EVM 指標精確計算與大型工程驗收"
    talk_id = "PM-11-QUALITY-EVM-LARGE-PROJECTS"
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

    builder.add_section("🎯 實獲值 EVM 量化實例：BAC 800 萬、PV 400 萬、EV 100 萬與 AC 200 萬指標剖析", sec1)
    builder.add_section("📊 專案評估四要點：範疇、成本、時程與規格，大型工程外部專家驗收機制", sec2)
    builder.add_section("💼 實務落實哲學：專案管理落實執行重於空談、期末實作筆記表總結", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部專案管理實務課程"',
        'event: "大學部專案管理實務課程"\ndate: "2024-11-27"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "專案管理-11-專案品質度量EVM指標計算與大型工程驗收-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：專案品質管理（Quality Management）、實獲值（EVM）核心公式計算、三重限制與大型標竿工程驗收評估  
> **授課教授**：授課講師（專案管理授課教授）  
> **核心模組**：Earned Value Management, EVM Metrics, BAC, PV, EV, AC, Triple Constraints, Large-Scale Projects  
> **學習目標**：精熟 EVM 成本與時程變異數及績效指標（CV, SV, CPI, SPI）之計算，掌握大型工程（如 101 大樓、捷運）評估驗收標準  
> **關聯文件**：[📄 完整原話逐字稿 (專案管理-11-專案品質度量EVM指標計算與大型工程驗收-proofread.md)](./專案管理-11-專案品質度量EVM指標計算與大型工程驗收-proofread.md)

---

## 🏛️ 實獲值管理 (EVM) 核心四大基礎變數

```mermaid
flowchart TD
    BAC["BAC (完工總預算: Budget at Completion)<br/>專案核准之總預算基準 (本例: 800 萬)"]
    PV["PV (計畫價值: Planned Value)<br/>截至當前預計應完成之預算 (本例: 400 萬)"]
    EV["EV (實獲價值: Earned Value)<br/>實際已完成工作之核定價值 (本例: 100 萬)"]
    AC["AC (實際成本: Actual Cost)<br/>完成目前工作所實際耗費的成本 (本例: 200 萬)"]

    BAC --> PV
    PV --> EV
    EV --> Variance["計算變異數與績效指數"]
    AC --> Variance
```

---

## 📊 課堂 EVM 算例深度解析 (截至第二年底)

| 指標代號 | 指標名稱 | 計算公式 | 數值計算 | 狀態解讀 |
| :--- | :--- | :--- | :--- | :--- |
| **CV** | 成本差異 (Cost Variance) | $EV - AC$ | $100 - 200 = -100$ 萬 | **🔴 成本嚴重超支 (Over Budget)** |
| **SV** | 時程差異 (Schedule Variance) | $EV - PV$ | $100 - 400 = -300$ 萬 | **🔴 進度嚴重落後 (Behind Schedule)** |
| **CPI** | 成本績效指標 (Cost Performance Index) | $EV / AC$ | $100 / 200 = 0.5$ | **每花 1 元僅產生 0.5 元價值** |
| **SPI** | 時程績效指標 (Schedule Performance Index) | $EV / PV$ | $100 / 400 = 0.25$ | **實際進度僅為預期之 25%** |

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. EVM 指標判讀心法
- **變異數小於 0 為警訊**：$CV < 0$ 代表成本超支；$SV < 0$ 代表進度落後。
- **指標小於 1.0 為劣質**：$CPI < 1.0$ 代表花錢效率不佳；$SPI < 1.0$ 代表執行進度落後。本課堂算例中 $CPI=0.5, SPI=0.25$，顯示該專案處於極端危機狀態，必須進行全面範疇縮減或重組。

### 2. 大型專案的獨立評估機制
- **台北 101 與捷運工程案例**：大型公共或高階建築專案，驗收階段必須委託獨立公正的第三方外部評估專家，依據範疇、時間、成本與技術規格四大要點出具正式評估報告書。

### 3. 「落實執行」高於一切
- 專案管理並非僅是繪製美觀甘特圖或填寫表格，最關鍵的核心在於「落實執行（Execution & Implementation）」。
"""
    summary_file = OUT_DIR / "專案管理-11-專案品質度量EVM指標計算與大型工程驗收-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_pm_08()
    build_pm_09()
    build_pm_10()
    build_pm_11()
