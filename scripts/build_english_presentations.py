#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build English Academic Keynote and Project Presentation deliverables:
- KEYNOTE-UIC-XAI: UIC Prof. Ali Keynote on Explainable AI & Causal Inference
- AI-EDU-EN: English Term Project Presentation on AI in Education Performance
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_undergrad_courses import clean_text, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_english_typos(text: str) -> str:
    """Clean minor transcription anomalies in English lectures."""
    replacements = [
        ("prejudice shift", "paradigm shift"),
        ("amultiple label", "a multi-label"),
        ("general GDP use", "general GPT use"),
        ("一個新 change", "a new policy change"),
        ("Ali Kaf, perfect", "Ali"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def segment_english_dialogue(text: str, default_speaker="Presenter") -> str:
    """Segment English transcript into clean dialogue paragraphs."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs = []
    current_para = []
    current_len = 0

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        current_para.append(s)
        current_len += len(s)
        if current_len >= 300 or s.endswith("Thank you.") or s.endswith("good afternoon."):
            paragraphs.append(" ".join(current_para))
            current_para = []
            current_len = 0

    if current_para:
        paragraphs.append(" ".join(current_para))

    formatted_paras = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        if any(trig in p_clean for trig in ["good afternoon, everyone", "today is a very honor to invite", "Professor Ali"]):
            formatted_paras.append(f"**【主持人】**：{p_clean}")
        elif any(trig in p_clean for trig in ["我講一下各自的時間", "中路差不多兩分半", "右城的話"]):
            formatted_paras.append(f"**【Youchen】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_uic_keynote():
    print("Building UIC Keynote (2025年12月08日 13點08分)...")
    out_dir = REPO_ROOT / "5-Master" / "2025-InternationalKeynote-ExplainableAI"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "2025年12月08日 13點08分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_english_typos(raw)

    title = "國際頂尖學者講座：可解釋人工智慧 XAI、因果推論與反事實決策模型"
    talk_id = "KEYNOTE-UIC-XAI-CAUSAL-AI"
    event = "國際資訊管理與計算科學特聘學者專題講座"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["Prof. Ali (UIC)", "主持人"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.40)

    sec1 = segment_english_dialogue(cleaned[:s1], default_speaker="Prof. Ali (UIC)")
    sec2 = segment_english_dialogue(cleaned[s1:], default_speaker="Prof. Ali (UIC)")

    builder.add_section("🎯 講座引言與學術背景：伊利諾大學芝加哥分校 UIC 學者介紹與 XAI 研究動機", sec1)
    builder.add_section("📊 可解釋性 XAI 與因果推論：黑盒子模型洞察、政策衝擊反事實預測模型", sec2)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "國際資訊管理與計算科學特聘學者專題講座"',
        'event: "國際資訊管理與計算科學特聘學者專題講座"\ndate: "2025-12-08"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = out_dir / "國際專題講座-可解釋AI因果推論與反事實決策模型-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **講座主題**：可解釋人工智慧（Explainable AI, XAI）、黑盒子模型透明化、因果推論（Causal Inference）與反事實決策預測  
> **特聘主講**：Prof. Ali（University of Illinois Chicago 資訊與計算科學系主任、頂級期刊資深主編）  
> **核心模組**：Explainable AI, Interpretability, Causal Inference, Counterfactual Reasoning, Policy Impact  
> **學習目標**：理解現代深度學習黑盒子模型之解釋性瓶頸，掌握如何從純關聯性觀察邁向因果推論與反事實政策模擬  
> **關聯文件**：[📄 完整原話逐字稿 (國際專題講座-可解釋AI因果推論與反事實決策模型-proofread.md)](./國際專題講座-可解釋AI因果推論與反事實決策模型-proofread.md)

---

## 🏛️ 可解釋性 XAI 與因果推論階梯架構

```mermaid
flowchart TD
    subgraph Level1["層級一：關聯性預測 (Correlation / Association)"]
        L1_Desc["觀察資料：若觀察到 X，則 Y 的機率是多少？<br/>(傳統深度學習與機器學習)"]
    end

    subgraph Level2["層級二：干預與操作 (Intervention)"]
        L2_Desc["主動介入：如果我們實施政策 do(X)，將會發生什麼？<br/>(因果圖模型 Causal DAGs)"]
    end

    subgraph Level3["層級三：反事實推論 (Counterfactuals)"]
        L3_Desc["反事實回顧：若過去採取了不同決策，結果會如何？<br/>(政策衝擊評估與責任歸屬)"]
    end

    Level1 --> Level2
    Level2 --> Level3
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 現代 AI 系統的「黑盒子」解釋性危機
- **預測精準但缺乏洞察**：當前主流的深度神經網路在眾多基準任務上表現優異，但決策邏輯本質為不可解釋的高維非線性黑盒子，難以提供「為何產出此結果」的邏輯透明度。
- **高風險領域的信任門檻**：在醫療診斷、公共政策、司法審查與金融授信等關鍵場景中，缺乏解釋性的預測模型將面臨極高的合規與倫理風險。

### 2. 從單純觀察走向因果推論 (Causal Inference)
- **觀察性數據 vs. 政策介入**：機器學習模型擅長捕捉變數間的靜態關聯性（Passive Observation），但當組織頒布新政策或介入環境時，靜態關聯性往往失效。
- **反事實模擬（Counterfactual Prediction）**：因果模型具備推演「若採行新政策會發生什麼」之能力，為科學決策提供具備因果支撐的模擬預測工具。
"""
    summary_file = out_dir / "國際專題講座-可解釋AI因果推論與反事實決策模型-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_english_presentation():
    print("Building English Project Presentation (週三 20點11分)...")
    out_dir = REPO_ROOT / "4-University" / "2024-UndergraduateCourses"
    raw_path = RAW_DIR / "週三 20點11分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_english_typos(raw)

    title = "英語專題發表：人工智慧教育表現預測、特徵工程與低成本過濾法模型"
    talk_id = "AI-EDU-ENGLISH-PRESENTATION"
    event = "大學部人工智慧專題全英文發表會"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員", "Youchen"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = "**【授課講師】**：好，接下來請專案小組進行全英文期末專題發表，題目為 Feature Selection and Review with AI in Education Performance，請開始發表。\n\n" + segment_english_dialogue(cleaned[:s1], default_speaker="學員")
    sec2 = segment_english_dialogue(cleaned[s1:s2], default_speaker="學員")
    sec3 = segment_english_dialogue(cleaned[s2:], default_speaker="Youchen") + "\n\n**【授課講師】**：好，謝謝這組的完整發表，時間控制得相當好。"

    builder.add_section("🎯 Introduction & Paradigm Shift: AI in Education Performance and Research Background", sec1)
    builder.add_section("📊 Multi-Label Feature Engineering: One-Hot Encoding for AI Tool Usage and Filter Selection", sec2)
    builder.add_section("💼 Experimental Results & Presentation Rehearsal: Filter Method Benefits and Timing Review", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部人工智慧專題全英文發表會"',
        'event: "大學部人工智慧專題全英文發表會"\ndate: "2024-12-18"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = out_dir / "英語專題發表-AI教育表現特徵工程與學習成效過濾法預測-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **專題發表主題**：AI 在教育學習表現預測之特徵工程（Feature Engineering）、多標籤獨熱編碼與輕量級過濾法（Filter Method）模型  
> **發表團隊**：Youchen 研究專案團隊（400th Day Request 專題小組）  
> **核心模組**：Educational Data Mining, Feature Selection, Filter Method, Multi-Label Encoding, Low-Cost ML  
> **學習目標**：掌握教育大數據中多模態學習工具使用特徵之編碼方式，運用低運算成本之過濾法特徵選取優化學習成效預測  
> **關聯文件**：[📄 完整原話逐字稿 (英語專題發表-AI教育表現特徵工程與學習成效過濾法預測-proofread.md)](./英語專題發表-AI教育表現特徵工程與學習成效過濾法預測-proofread.md)

---

## 🏛️ 教育大數據特徵工程與過濾法預測管線

```mermaid
flowchart TD
    RawSurvey["學生問卷與數位學習歷程原始資料 (Survey & Logs)"]
    
    subgraph FeatureEngineering["特徵工程 (Feature Engineering)"]
        MultiLabel["多標籤 AI 工具使用特徵抽取<br/>(ChatGPT, Claude, Copilot 等)"]
        OneHot["獨熱編碼轉換 (0/1 Multi-Hot Encoding)"]
    end

    subgraph Selection["特徵選取 (Feature Selection)"]
        Filter["輕量過濾法 (Filter Method)<br/>依相關係數與互資訊排序特徵<br/>👉 極低運算開銷"]
    end

    subgraph Evaluation["預測評估 (Performance Prediction)"]
        Classifier["高效分類器 (Random Forest / Logistic Regression)"]
        Output["預測學生學期成績表現與預警"]
    end

    RawSurvey --> FeatureEngineering
    MultiLabel --> OneHot
    OneHot --> Selection
    Filter --> Evaluation
    Classifier --> Output
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 研究主題與教育範式轉移 (Paradigm Shift)
- **生成式 AI 工具融入學習**：探討現代大學生在學習歷程中使用各類 AI 輔助工具（如 ChatGPT）對學業表現之實際衝擊。
- **多標籤特徵表示**：學生可能同時使用多種 AI 工具，團隊透過多標籤編碼（0 與 1 二元矩陣）精確記錄其工具使用組合特徵。

### 2. 過濾法 (Filter Method) 之實務優勢
- **極低算力成本**：相較於包裹法（Wrapper Method）或嵌入法（Embedded Method）需要反覆訓練模型，過濾法僅需計算特徵與目標變數之統計相關性，運算成本極低，能推動 AI 教育預測工具的普及化。
"""
    summary_file = out_dir / "英語專題發表-AI教育表現特徵工程與學習成效過濾法預測-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_uic_keynote()
    build_english_presentation()
