#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Career Development & Job Hunting deliverables (CAREER-01, CAREER-02, CAREER-03):
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


def fix_career_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in Career Development lectures."""
    replacements = [
        ("一零四", "104 人力銀行"),
        ("收餘利", "收履歷"),
        ("小資樣", "小國家"),
        ("全面積", "前幾碼"),
        ("能力拿當", "人力資源顧問"),
        ("定增項", "應徵項目"),
        ("定增裝置", "應徵職位"),
        ("中科產", "中科院或科技產業"),
        ("市值來回答", "實質事實來回答"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_career_01():
    print("Building CAREER-01 (週一 上午09點09分)...")
    raw_path = RAW_DIR / "週一 上午09點09分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_career_typos(raw)

    title = "職涯發展與就業輔導 Lesson 01：求職自我優勢定位、人脈推薦與海外求職防詐實務"
    talk_id = "CAREER-01-POSITIONING-NETWORKING-SAFETY"
    event = "大學部職涯發展與求職就業輔導工作坊"

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

    builder.add_section("🎯 求職自我定位與非你莫屬核心價值：履歷媒合、推薦機制與軟實力展現", sec1)
    builder.add_section("📊 專業職場素養與時間管理心法：排程紀律、跨世代溝通與人身安全警覺", sec2)
    builder.add_section("💼 海外就業陷阱與求職詐騙防範：高薪外派風險識別與求職登記表填寫須知", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部職涯發展與求職就業輔導工作坊"',
        'event: "大學部職涯發展與求職就業輔導工作坊"\ndate: "2024-11-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "職涯發展-01-求職自我定位人脈媒合與海外求職防詐實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：求職自我定位、專業軟實力展現、內部人脈推薦優勢、職場時間管理與海外高薪求職防詐  
> **授課教授**：授課講師（職涯就業輔導顧問）  
> **核心模組**：Career Positioning, Referral Networking, Time Management, Anti-Fraud Awareness, Job Registration  
> **學習目標**：釐清個人專業優勢與職務適配性，掌握內部推薦求職管道，並建立辨識海外高薪外派詐騙之防禦警覺  
> **關聯文件**：[📄 完整原話逐字稿 (職涯發展-01-求職自我定位人脈媒合與海外求職防詐實務-proofread.md)](./職涯發展-01-求職自我定位人脈媒合與海外求職防詐實務-proofread.md)

---

## 🏛️ 多軌求職管道轉換與媒合成功率比較

```mermaid
flowchart TD
    JobSeeker["求職者 (Job Seeker)"]
    
    subgraph PathA["管道 A：人力銀行公開海投 (Public Job Boards)"]
        A1["投遞 104 / 1111 / LinkedIn"]
        A2["進入數百封履歷海選 (篩選率 < 5%)"]
    end

    subgraph PathB["管道 B：內部人脈推薦 (Internal Referral)"]
        B1["學長姐 / 師長 / 前同事推薦"]
        B2["直達用人主管桌前 (面試機會 > 50%)"]
    end

    JobSeeker --> PathA
    JobSeeker --> PathB
    A2 --> Interview["實體 / 線上面試"]
    B2 --> Interview
```

---

## 🛡️ 海外高薪求職陷阱特徵雷達

```mermaid
flowchart LR
    JobOffer["收到高薪工作邀約 (Overseas Offer)"]
    Check1{"要求無經驗 / 低門檻<br/>卻承諾遠高於市場常態之高薪?"}
    Check2{"工作地點偏遠或具備外派爭議國家<br/>(東南亞園區 / 偏僻境外)?"}
    Check3{"要求扣押護照 / 證件<br/>或要求預先匯款保證金?"}
    Alert["🚨 高度警報：極高機率為人口販運/詐騙水房！立即切斷聯繫"]
    Legit["具備合法跨國合約與正當外派審查"]

    JobOffer --> Check1
    Check1 -- "是" --> Alert
    Check1 -- "否" --> Check2
    Check2 -- "是" --> Alert
    Check2 -- "否" --> Check3
    Check3 -- "是" --> Alert
    Check3 -- "否" --> Legit
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 求職自我定位與「非你莫屬」效應
- **客製化適配（Job Matching）**：切忌一份通用履歷海投到底。應針對目標企業的職務描述（Job Description, JD）逐條對齊，展現出「你的技能正是為此職位量身打造」。
- **內部推薦（Referral）的破局力量**：人脈推薦能大幅降低企業人資的信任成本與背景調查風險，是進入優質企業最具效率的捷徑。

### 2. 職場時間管理與承諾紀律
- **日程排程優先度**：時間管理能力決定了一個人的專業上限。一旦行程預先敲定，應堅守承諾；避免因臨時邀約打亂原本專案節奏。

### 3. 海外求職防詐安全防線
- **海外求職詐騙態樣**：除了眾所皆知的特定東南亞園區，歐洲非典型偏遠據點亦曾查獲詐騙集團洗錢水房。
- **自保金律**：絕不可將護照、身分證件交由非官方機構扣押；凡未經正式專業筆面試即許諾高薪出國者，均屬高風險陷阱。
"""
    summary_file = OUT_DIR / "職涯發展-01-求職自我定位人脈媒合與海外求職防詐實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_career_02():
    print("Building CAREER-02 (週一 上午11點11分)...")
    raw_path = RAW_DIR / "週一 上午11點11分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_career_typos(raw)

    title = "職涯發展與就業輔導 Lesson 02：人資篩選心理學、履歷投遞時機與版面視覺優化"
    talk_id = "CAREER-02-HR-PSYCHOLOGY-LAYOUT"
    event = "大學部職涯發展與求職就業輔導工作坊"

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

    builder.add_section("🎯 人資審查心理學：主管職 vs. 工程師篩選速度與履歷黃金三十秒原則", sec1)
    builder.add_section("📊 個資保護與身分證字號揭露考量：偽冒風險、信任建立與求職平台隱私", sec2)
    builder.add_section("💼 履歷版面結構與視覺排版：字元行距 1.5 倍設定、段落留白與現場閱讀體驗", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部職涯發展與求職就業輔導工作坊"',
        'event: "大學部職涯發展與求職就業輔導工作坊"\ndate: "2024-11-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "職涯發展-02-人資篩選心理學履歷投遞時機與版面視覺優化-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：人資（HR）履歷篩選心理學、30 秒黃金掃描法則、個資去識別化原則與 1.5 倍行距排版美學  
> **授課教授**：授課講師（職涯就業輔導顧問）  
> **核心模組**：HR Resume Screening, 30-Second Rule, Privacy Protection, Typography, Line Spacing  
> **學習目標**：掌握人資篩選技術履歷的關鍵視角，平衡個人隱私防護與求職誠信，並運用專業排版強化閱讀舒適度  
> **關聯文件**：[📄 完整原話逐字稿 (職涯發展-02-人資篩選心理學履歷投遞時機與版面視覺優化-proofread.md)](./職涯發展-02-人資篩選心理學履歷投遞時機與版面視覺優化-proofread.md)

---

## 🏛️ 人資（HR）履歷初篩 30 秒掃描決策模型

```mermaid
flowchart TD
    Resume["收到求職者履歷 (PDF 格式)"]
    Scan["人資黃金 30 秒快速瀏覽"]
    
    Check1{"版面視覺是否清晰？<br/>(有無雜亂擁擠、適度留白)"}
    Check2{"前三分之一版面是否具備<br/>對應職缺的核心技能關鍵字？"}
    Check3{"最高學歷與核心經歷<br/>是否一目了然？"}
    
    Pass["✅ 通過初篩：列入用人主管面試清單"]
    Reject["❌ 淘汰：移入求職資料庫封存"]

    Resume --> Scan
    Scan --> Check1
    Check1 -- "否" --> Reject
    Check1 -- "是" --> Check2
    Check2 -- "否" --> Reject
    Check2 -- "是" --> Check3
    Check3 -- "是" --> Pass
    Check3 -- "否" --> Reject
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 人資履歷篩選速度與心理機制
- **黃金 30 秒法則**：針對初階工程師或一般專員職缺，人資每次面對數百封投遞，平均僅停留 20 到 30 秒掃描關鍵字；主管職位才會逐行研讀。
- **投遞黃金時機**：避免在週五下午或週末深夜投遞，最佳時段為週二至週四上班日早晨，以確保履歷排列在人資收件箱最上方。

### 2. 個資保護與身分證字號揭露考量
- **防範資料外洩與偽冒**：在公開求職平台初期投遞時，身分證字號、完整戶籍地址無須完全暴露，可採去識別化處理（例如僅揭露首字母與前幾碼，後續錄取簽約時再補齊）。

### 3. 版面視覺排版細節
- **行距與留白**：文字間距切忌緊密堆疊，建議設定 **1.5 倍行高**，適度分段並建立視覺層次，大幅減輕審閱者之視覺疲勞。
"""
    summary_file = OUT_DIR / "職涯發展-02-人資篩選心理學履歷投遞時機與版面視覺優化-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_career_03():
    print("Building CAREER-03 (2-10 週一 下午01點05分)...")
    raw_path = RAW_DIR / "2-10 週一 下午01點05分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_career_typos(raw)

    title = "職涯發展與就業輔導 Lesson 03：學經歷倒敘法撰寫規範與面試應對實戰技巧"
    talk_id = "CAREER-03-REVERSE-CHRONO-INTERVIEW"
    event = "大學部職涯發展與求職就業輔導工作坊"

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

    builder.add_section("🎯 履歷基本資料填寫：個資揭露原則、個人特質呈現與面試問題切入點", sec1)
    builder.add_section("📊 學歷與經歷倒敘法核心準則：最高學歷置頂、應徵項目分類與錯誤案例剖析", sec2)
    builder.add_section("💼 面試應對實戰與提問藝術：依據事實回答切忌虛構崩盤、現場模擬演練", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部職涯發展與求職就業輔導工作坊"',
        'event: "大學部職涯發展與求職就業輔導工作坊"\ndate: "2024-11-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "職涯發展-03-學經歷倒敘法撰寫規範與面試應對實戰技巧-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：學經歷倒敘法（Reverse Chronological Order）、職務內容精準對焦、誠信回答原則與面試提問策略  
> **授課教授**：授課講師（職涯就業輔導顧問）  
> **核心模組**：Reverse Chronology, Resume Writing Standards, Behavioral Interview, Fact-Based Answering  
> **學習目標**：熟練運用倒敘法將最具價值的最高學經歷置頂展現，掌握面試誠信應對底線與向主管主動提問之加分技巧  
> **關聯文件**：[📄 完整原話逐字稿 (職涯發展-03-學經歷倒敘法撰寫規範與面試應對實戰技巧-proofread.md)](./職涯發展-03-學經歷倒敘法撰寫規範與面試應對實戰技巧-proofread.md)

---

## 🏛️ 履歷學經歷「倒敘法」標準結構

```mermaid
flowchart TD
    subgraph Header["第一區塊：最高學歷與近期經歷 (Top - Most Important)"]
        H1["碩士學歷 / 最近一份正職或重要實習工作"]
        H2["直接對應應徵職缺之核心研發專案與量化產出"]
    end

    subgraph Mid["第二區塊：次高學歷與過往經歷 (Middle)"]
        M1["學士學歷 / 大學時期重要專案成果"]
    end

    subgraph Bot["第三區塊：高中或早期經歷 (Bottom - Baseline)"]
        B1["高中職基礎學歷 (僅列校名與科系，精簡帶過)"]
    end

    Header --> Mid
    Mid --> Bot
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 學經歷撰寫的「倒敘法」金律
- **最高優先**：履歷表最上方必須是**最新的最高學歷與最近的工作經歷**。人資最關心你當前或近期的技能成熟度，切忌依時間順序從高中或國小開始由前往後寫。
- **慘痛案例借鏡**：部分求職者未採倒敘法，將高中甚至國中學歷排在最顯眼的第一行，將碩士學位淹沒在底端，極易在初篩時遭誤判淘汰。

### 2. 應徵項目分類與職務對焦
- **精確對位職缺內容**：面試前務必徹底熟讀目標職缺的工作內容（Responsibilities），並在履歷中將專案技能分門別類，切忌對應徵職位之具體工作一無所知。

### 3. 面試應對的三大誠信底線
- **依實質事實回答（Fact-Based）**：知之為知之，不知為不知。技術面試中若遇到未接觸過的領域，坦承說明並展現學習路徑，切忌胡亂編造；一旦被資深考官追問細節而崩盤，將直接喪失錄取機會。
- **雙向提問的藝術**：面試尾聲主管詢問「你有什麼問題想問」時，應主動提出關於團隊研發挑戰、專案技術堆疊或部門願景之深度問題，展現強烈的入職企圖心。
"""
    summary_file = OUT_DIR / "職涯發展-03-學經歷倒敘法撰寫規範與面試應對實戰技巧-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_career_01()
    build_career_02()
    build_career_03()
