#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 2026 NCU IM Academic Conference deliverables (NCU-IM-01, NCU-IM-02, NCU-IM-03):
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

OUT_DIR = REPO_ROOT / "5-Master" / "2026-AcademicConference-NCU-IM"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_ncu_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in NCU Conference presentations."""
    replacements = [
        ("中央之廣所論發表會", "中央資管所論文發表會"),
        ("篩選。I", "Session I"),
        ("篩選I", "Session I"),
        ("篩選 I", "Session I"),
        ("C 學 H", "Session H"),
        ("C 學臺", "Session I"),
        ("歐陽崇龍", "歐陽崇榮"),
        ("本一筆", "本益比 (P/E Ratio)"),
        ("歸估風險", "追高估值風險"),
        ("N C U", "NCU"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def segment_conference_dialogue(text: str, default_speaker="發表人") -> str:
    """Segment conference transcript with appropriate academic roles."""
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
        if current_len >= 220 or s.endswith("謝謝。") or s.endswith("請教。"):
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
        if any(trig in p_clean for trig in ["各位來賓，大家好", "歡迎各位蒞臨", "我是今天的主持人", "本間教室下一個場次"]):
            formatted_paras.append(f"**【主持人】**：{p_clean}")
        elif any(trig in p_clean for trig in ["請教一下", "我的問題是", "評審委員", "教授請問", "講評"]):
            formatted_paras.append(f"**【評審委員】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_ncu_01():
    print("Building NCU-IM-01 (週五 08點59分)...")
    raw_path = RAW_DIR / "週五 08點59分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_ncu_typos(raw)

    title = "學術論文發表 Session A：智慧醫療——老年失智症多模態神經與認知特徵預測模型"
    talk_id = "NCU-IM-01-SMART-HEALTHCARE-DEMENTIA"
    event = "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["發表人", "評審委員", "主持人"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_conference_dialogue(cleaned[:s1])
    sec2 = segment_conference_dialogue(cleaned[s1:s2])
    sec3 = segment_conference_dialogue(cleaned[s2:])

    builder.add_section("🎯 高齡化社會與失智症防治：早期篩檢臨床痛點與多模態特徵整合研究背景", sec1)
    builder.add_section("📊 神經資訊與認知評估特徵工程：腦波特徵萃取、認知量表與模型構建", sec2)
    builder.add_section("💼 實驗成果與專家評審講評：分類靈敏度與特異度驗證、臨床落地回饋與合照總結", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"',
        'event: "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"\ndate: "2026-03-27"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "NCU-IM-01-智慧醫療-老年失智症多模態神經與認知特徵預測模型-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **研討會名稱**：第十七屆國立中央大學資訊管理學系學術論文暨專題發表會 (NCU IM Conference 2026)  
> **發表場次**：Session A 智慧醫療專題  
> **核心模組**：Smart Healthcare, Dementia Prediction, Multimodal Features, Cognitive Assessment, Model Evaluation  
> **研究亮點**：整合多模態神經電生理訊號與臨床認知評估量表，構建高靈敏度之早期老年失智症輔助預測架構  
> **關聯文件**：[📄 完整原話逐字稿 (NCU-IM-01-智慧醫療-老年失智症多模態神經與認知特徵預測模型-proofread.md)](./NCU-IM-01-智慧醫療-老年失智症多模態神經與認知特徵預測模型-proofread.md)

---

## 🏛️ 多模態失智症早期篩檢特徵工程架構

```mermaid
flowchart TD
    Patient["老年受試者隊列 (Elderly Cohort)"]
    
    subgraph DataCollection["多模態資料採集層 (Data Collection)"]
        EEG["電生理訊號採集 (EEG / 頻譜能量密度)"]
        Cognitive["臨床認知測驗 (MMSE / MoCA 量表評分)"]
        BioData["人口統計與生活型態特徵 (Demographics)"]
    end

    subgraph FeatureEngineering["特徵工程與前處理 (Preprocessing)"]
        Denoise["訊號去噪與頻段能量分解 (Alpha/Beta/Theta)"]
        Normalize["量表常模標準化與遺漏值插補"]
        FeatFuse["特徵向量拼接與降維融合 (Feature Fusion)"]
    end

    subgraph Modeling["機器學習分類與決策 (Classification)"]
        Model["非線性整合模型 (XGBoost / SVM / MLP)"]
        Predict["早期失智風險分級判定 (Normal / MCI / Dementia)"]
    end

    Patient --> DataCollection
    EEG --> Denoise
    Cognitive --> Normalize
    BioData --> FeatFuse
    Denoise --> FeatFuse
    Normalize --> FeatFuse
    FeatFuse --> Model
    Model --> Predict
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 研究動機與臨床挑戰
- **高齡化社會痛點**：失智症（Dementia）為神經退化性症候群，早期輕度認知障礙（MCI）若能提早偵測，可大幅延緩病程惡化。傳統醫院神經心理量表耗時長且仰賴資深醫師主觀判讀。
- **多模態特徵整合**：本研究結合客觀生理訊號（腦波 EEG 頻段特徵）與結構化認知量表，降低單一檢驗指標之偽陽性。

### 2. 實驗效能與評審委員講評
- **指標權衡**：在生醫診斷領域中，「靈敏度（Sensitivity / Recall）」高於特異度（Specificity），需確保不漏診潛在患者。
- **評審建議**：模型應進一步驗證不同年齡組群與跨院區資料之泛化能力，並朝向穿戴式輕量化設備推展。
"""
    summary_file = OUT_DIR / "NCU-IM-01-智慧醫療-老年失智症多模態神經與認知特徵預測模型-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_ncu_02():
    print("Building NCU-IM-02 (週五 11點35分)...")
    raw_path = RAW_DIR / "週五 11點35分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_ncu_typos(raw)

    title = "學術論文發表 Session H：智慧金融——量化投資多因子選股與動態本益比進出場策略"
    talk_id = "NCU-IM-02-FINTECH-QUANT-INVESTING"
    event = "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["發表人", "評審委員", "主持人"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_conference_dialogue(cleaned[:s1])
    sec2 = segment_conference_dialogue(cleaned[s1:s2])
    sec3 = segment_conference_dialogue(cleaned[s2:])

    builder.add_section("🎯 研討會發表場次啟動：團隊報告心理調適與智慧金融系統研發背景", sec1)
    builder.add_section("📊 量化投資多因子模型：股東權益報酬率 ROE、近四季動態檢驗與本益比估值門檻", sec2)
    builder.add_section("💼 交易策略回測與頒獎典禮：回撤風險控制、使用者友善介面與系辦領獎須知", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"',
        'event: "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"\ndate: "2026-03-27"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "NCU-IM-02-智慧金融-量化投資多因子選股與動態本益比進出場策略-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **研討會名稱**：第十七屆國立中央大學資訊管理學系學術論文暨專題發表會 (NCU IM Conference 2026)  
> **發表場次**：Session H 智慧金融專題  
> **核心模組**：FinTech, Quantitative Investing, Multi-Factor Model, ROE Dynamics, PE Thresholds, Backtesting  
> **研究亮點**：建構結合獲利能力動態趨勢（ROE）與市場估值門檻（動態本益比）之自動化選股與進出場交易決策系統  
> **關聯文件**：[📄 完整原話逐字稿 (NCU-IM-02-智慧金融-量化投資多因子選股與動態本益比進出場策略-proofread.md)](./NCU-IM-02-智慧金融-量化投資多因子選股與動態本益比進出場策略-proofread.md)

---

## 🏛️ 量化多因子選股與動態進出場決策邏輯

```mermaid
flowchart TD
    Universe["全市場股票池 (Equity Universe)"]
    
    subgraph Fundamental["第一層：基本面篩選 (Fundamental Quality)"]
        ROE["股東權益報酬率 (ROE)<br/>檢驗連續四季保持增長或創近期新高"]
    end

    subgraph Valuation["第二層：動態估值防禦 (Valuation Safety)"]
        PE["動態本益比 (Dynamic P/E Ratio)<br/>低於近四季平均，且高於近四季最低點<br/>👉 避免追高估值風險"]
    end

    subgraph Execution["第三層：交易執行 (Execution & Exit)"]
        Entry["產生買入進場訊號 (Buy Signal)"]
        Monitor["動態追蹤停損與出場門檻"]
        Exit["觸發出場條件平倉 (Sell Signal)"]
    end

    Universe --> Fundamental
    Fundamental --> Valuation
    Valuation --> Entry
    Entry --> Monitor
    Monitor --> Exit
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 動態多因子模型架構
- **時間段動態對比 vs. 單一時間點**：傳統價值投資常僅比對單一季度的財務比率，本系統將指標擴展為「近四季滾動時間段（Rolling 4 Quarters）」，檢視公司體質之動態連續性。
- **市場估值防禦機制**：透過疊加動態本益比門檻，有效剔除受市場短期題材過度炒作之泡沫標的。

### 2. 系統架構與使用者體驗
- **黑盒子封裝與直覺化介面**：後端處理極為複雜的跨期財報清洗、因子權重計算與回測演算法，但前端提供直觀的視覺化圖表與簡潔進出場訊號，降低一般非量化投資人之使用門檻。
"""
    summary_file = OUT_DIR / "NCU-IM-02-智慧金融-量化投資多因子選股與動態本益比進出場策略-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_ncu_03():
    print("Building NCU-IM-03 (週五 14點17分)...")
    raw_path = RAW_DIR / "週五 14點17分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_ncu_typos(raw)

    title = "學術論文發表 Session I：機器學習——特徵精簡與實例樣本選取雙向管線效能優化"
    talk_id = "NCU-IM-03-ML-FEATURE-INSTANCE-SELECTION"
    event = "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["發表人", "評審委員", "主持人"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_conference_dialogue(cleaned[:s1])
    sec2 = segment_conference_dialogue(cleaned[s1:s2])
    sec3 = segment_conference_dialogue(cleaned[s2:])

    builder.add_section("🎯 Session I 研討會開場：主持人引言、歐陽崇榮教授評審介紹與發表規範說明", sec1)
    builder.add_section("📊 特徵與實例雙向實驗設計：先特徵選取 vs. 先樣本選取 3x3 矩陣與 20 個資料集評估", sec2)
    builder.add_section("💼 論文答辯與場次交流：分類穩定性提升機制、實驗偏誤防範與會後師生交流", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"',
        'event: "第十七屆國立中央大學資訊管理學系學術論文暨專題發表會"\ndate: "2026-03-27"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "NCU-IM-03-機器學習-特徵精簡與實例樣本選取雙向管線效能優化-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **研討會名稱**：第十七屆國立中央大學資訊管理學系學術論文暨專題發表會 (NCU IM Conference 2026)  
> **發表場次**：Session I 機器學習與資料探勘專題  
> **評審委員**：歐陽崇榮教授（南洋大學 / 專案特聘評審）  
> **核心模組**：Machine Learning, Feature Selection, Instance Selection, Pipeline Optimization, Benchmark Datasets  
> **研究亮點**：系統性探討特徵選取（橫向維度精簡）與實例樣本選取（縱向樣本過濾）之執行順序對模型分類效能與穩定度之影響  
> **關聯文件**：[📄 完整原話逐字稿 (NCU-IM-03-機器學習-特徵精簡與實例樣本選取雙向管線效能優化-proofread.md)](./NCU-IM-03-機器學習-特徵精簡與實例樣本選取雙向管線效能優化-proofread.md)

---

## 🏛️ 雙向資料前處理流水線 (Bi-Directional Pipeline) 實驗設計

```mermaid
flowchart TD
    RawData["高維嘈雜原始資料集 (20 個公開基準資料集)"]
    
    subgraph PathA["路徑 A：先特徵後樣本 (Feature-then-Instance)"]
        FS_A["1. 特徵選取 (Feature Selection)<br/>過濾不相關與冗餘維度"]
        IS_A["2. 實例樣本選取 (Instance Selection)<br/>剔除邊界雜訊與離群樣本"]
    end

    subgraph PathB["路徑 B：先樣本後特徵 (Instance-then-Feature)"]
        IS_B["1. 實例樣本選取 (Instance Selection)<br/>優先純化資料集品質"]
        FS_B["2. 特徵選取 (Feature Selection)<br/>進一步壓縮特徵空間"]
    end

    subgraph Evaluation["3x3 交叉評估與效能度量"]
        Classifiers["分類器評估 (C4.5 / SVM / Naive Bayes)"]
        Metrics["精確率、召回率、模型訓練時間與資料壓縮率"]
    end

    RawData --> PathA
    RawData --> PathB
    PathA --> Evaluation
    PathB --> Evaluation
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 特徵選取 (FS) 與實例選取 (IS) 之交互影響
- **橫向 vs. 縱向精簡**：特徵選取（FS）縮減屬性維度（Columns），降低模型複雜度；實例選取（IS）縮減訓練樣本數（Rows），移除雜訊資料與邊界模糊實例。
- **流水線執行先後順序**：
  - **路徑 A（FS $\to$ IS）**：在低維度空間中計算樣本距離與代表性，大幅降低 IS 演算法之運算時間，並提升代表性樣本選取之準確度。
  - **路徑 B（IS $\to$ FS）**：先淨化樣本分佈以確保特徵重要度評估不受極端離群值扭曲。

### 2. 嚴謹的實驗設計
- **20 個公開 Benchmark 資料集**：橫跨不同特徵維度、樣本規模與類別平衡度，避免演算法結論偏向特定領域資料集。
- **3 $\times$ 3 實驗設計**：各採用三種代表性 FS 演算法與三種 IS 演算法進行全組合驗證，確保實證結論之穩健性。
"""
    summary_file = OUT_DIR / "NCU-IM-03-機器學習-特徵精簡與實例樣本選取雙向管線效能優化-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_ncu_01()
    build_ncu_02()
    build_ncu_03()
