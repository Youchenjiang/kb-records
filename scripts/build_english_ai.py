#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 5-Master Advanced AI & Optimization Deliverables:
- EMI 全英語授課 AI 機器學習與最佳化課程 (週四 09:11, 09:36, 10:03, 10:10, 11:30, 11:51)
Follows PROOFREAD_RULES.md, ScenarioType.CLASSROOM_LECTURE, and repository linters.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "5-Master" / "2025-AdvancedAI-Optimization"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"

REPLACEMENTS = [
    (r"optimization\s*股份", "Optimization 最佳化部分"),
    (r"股份", "部分"),
    (r"蒙特卡羅迴圈", "蒙特卡羅模擬迴圈 (Monte Carlo Loops)"),
    (r"貝葉斯", "貝葉斯模型 (Bayesian Model)"),
    (r"empirical\s*機制", "經驗驗證機制 (Empirical Mechanism)"),
    (r"TCPS", "TCP/TLS"),
    (r"程式程序", "傳輸程序"),
    (r"治安", "資安"),
]


def clean_text(text: str) -> str:
    res = text
    for pat, rep in REPLACEMENTS:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def segment_into_dialogue_paragraphs(text: str, default_speaker="授課講師") -> str:
    sentences = re.split(r"(?<=[。！？\.\?\!])", text)
    paragraphs = []
    current_para = []
    current_len = 0

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        current_para.append(s)
        current_len += len(s)
        if current_len >= 220 or s.endswith("好。") or s.endswith("OK。") or s.endswith("Alright.") or s.endswith("thank you."):
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
        student_triggers = ["Hello, and we are", "These are our team members", "我要show", "另外一個話是 Apache", "老師請問"]
        if any(trig in p_clean for trig in student_triggers):
            formatted_paras.append(f"**【學員】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_lesson1():
    print("Building AI Optimization Lesson 1...")
    # 09:11 + 10:03
    t1 = (RAW_DIR / "週四 09點11分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    t2 = (RAW_DIR / "週四 10點03分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    combined = t1 + "\n\n" + t2
    cleaned = clean_text(combined)

    title = "進階人工智慧與最佳化 Lesson 01：EMI 全英語課程導論、課堂行為準則與評量規範"
    talk_id = "AI-OPT-01"
    event = "進階人工智慧與最佳化研究所課程"

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

    builder.add_section("🎯 EMI 全英語授課導引：國際生修課政策、跨語言溝通與課程核心定位", sec1)
    builder.add_section("📜 學術誠信與課堂行為守則（Code of Conduct）：作業規範、AI 工具使用限制與評分標準", sec2)
    builder.add_section("🗺️ 課程學期全景地圖：機器學習、對抗性防禦、感測器模型與蒙特卡羅最佳化", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "進階人工智慧與最佳化研究所課程"',
        'event: "進階人工智慧與最佳化研究所課程"\ndate: "2025-02-20"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "AI-Optimization-01-課程導論與學術倫理規範-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：全英語授課（EMI）導論、課堂行為守則（Code of Conduct）與學術誠信規範  
> **授課教授**：授課講師（AI 與資訊工程領域講座教授）  
> **核心模組**：Course Orientation, Academic Integrity, Grading Policy, EMI Policy  
> **學習目標**：了解跨國學生 EMI 課堂規範、掌握學術誠信底線與學期 AI 最佳化專案要求  
> **關聯文件**：[📄 完整原話逐字稿 (AI-Optimization-01-課程導論與學術倫理規範-proofread.md)](./AI-Optimization-01-課程導論與學術倫理規範-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Course["進階 AI 與最佳化課程 (EMI Course)"] --> Ori["課程導引與修課規範 (Orientation)"]
    Ori --> P1["雙語友善環境：以英文為主，兼顧國際生與在地學生溝通"]
    Ori --> P2["行為準則 (Code of Conduct)：團隊合作、準時出缺席、相互尊重"]
    Ori --> P3["學術誠信政策 (Academic Integrity)：生成式 AI 輔助邊界與獨立思考"]
    Ori --> P4["學期評量體系：理論作業 + 蒙特卡羅實作 + 期末高並發系統專題"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **EMI 全英語教學目標**：透過全英文講述與國際生分組協作，建立學員在國際學術研討會與跨國科技產業的專業英文溝通力。
2. **AI 工具輔助準則**：鼓勵使用 AI 提升學習效率，但必須在繳交作業中誠實揭露使用的 Prompt 與模型版本，杜絕直接抄襲生成結果。
"""
    summary_file = OUT_DIR / "AI-Optimization-01-課程導論與學術倫理規範-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_lesson2():
    print("Building AI Optimization Lesson 2...")
    # 09:36 + 10:10
    t1 = (RAW_DIR / "週四 09點36分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    t2 = (RAW_DIR / "週四 10點10分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    combined = t1 + "\n\n" + t2
    cleaned = clean_text(combined)

    title = "進階人工智慧與最佳化 Lesson 02：感測器資料模型、對抗性機器學習（Adversarial ML）與蒙特卡羅貝葉斯最佳化"
    talk_id = "AI-OPT-02"
    event = "進階人工智慧與最佳化研究所課程"

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

    builder.add_section("🎯 感測器原始資料特徵增強（Raw Sensors Feature Enhancement）與模型極限", sec1)
    builder.add_section("🛡️ 抗攻擊模型需求剖析：黑箱（Black-box）、灰箱（Gray-box）與白箱（White-box）防禦架構", sec2)
    builder.add_section("🎲 蒙特卡羅模擬迴圈（Monte Carlo Loops）與貝葉斯驗證模型（Bayesian Verification）抗模仿攻擊設計", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "進階人工智慧與最佳化研究所課程"',
        'event: "進階人工智慧與最佳化研究所課程"\ndate: "2025-02-20"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "AI-Optimization-02-對抗性機器學習與蒙特卡羅最佳化-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：感測器特徵工程、對抗性機器學習（Adversarial Machine Learning）、蒙特卡羅迴圈與貝葉斯最佳化  
> **授課教授**：授課講師（AI 與資訊工程領域講座教授）  
> **核心模組**：Adversarial ML, Black/Gray/White Box Threat Models, Monte Carlo Simulation, Bayesian Optimization  
> **學習目標**：理解模型在面對擾動攻擊與模仿攻擊時的脆弱性，設計具備極高穩定性與抗性之驗證模型  
> **關聯文件**：[📄 完整原話逐字稿 (AI-Optimization-02-對抗性機器學習與蒙特卡羅最佳化-proofread.md)](./AI-Optimization-02-對抗性機器學習與蒙特卡羅最佳化-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Raw["物聯網感測器原始資料 (Raw Sensors Data)"] --> Feat["特徵工程與指數量級增強"]
    Feat --> Model["機器學習基準模型 (Baseline Model)"]
    Attacker["對抗性攻擊者 (Adversarial Attacker)"] --> Threat{"威脅威脅假定等級"}
    Threat -->|白箱攻擊| T1["完全掌握架構與權重梯度"]
    Threat -->|灰箱/黑箱攻擊| T2["模仿攻擊 (Imitation / Surrogate Attack)"]
    Model --> Defense["強健性防禦最佳化框架"]
    Defense --> MC["蒙特卡羅模擬迴圈 (Monte Carlo Loops: 大量隨機擾動取樣)"]
    MC --> Bayes["貝葉斯最佳化驗證模型 (Bayesian Optimization)"]
    Bayes --> Robust["輸出高穩定度、抗模仿攻擊之強健 AI 模型"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **不能盲目依賴黑箱防禦假設**：現實攻防中，攻擊者可藉由查詢輸出訓練代理模型（Surrogate Model）實施高效的遷移性模仿攻擊，模型必須在數學架構上具備內生抗性。
2. **蒙特卡羅與貝葉斯聯手**：透過 Monte Carlo 迴圈生成海量擾動樣本，搭配貝葉斯機率架構動態調整模型超參數，能在有限算力下找到抵禦攻擊之全局最優防護解。
"""
    summary_file = OUT_DIR / "AI-Optimization-02-對抗性機器學習與蒙特卡羅最佳化-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_lesson3():
    print("Building AI Optimization Lesson 3...")
    # 11:30 + 11:51
    t1 = (RAW_DIR / "週四 11點30分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    t2 = (RAW_DIR / "週四 11點51分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    combined = t1 + "\n\n" + t2
    cleaned = clean_text(combined)

    title = "進階人工智慧與最佳化 Lesson 03：感測器能源模型與 Apache Benchmark 高並發效能評測"
    talk_id = "AI-OPT-03"
    event = "進階人工智慧與最佳化研究所課程"

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

    builder.add_section("🔋 學員專案發表：四百組電池感測模組（Battery Packs）能源採集與即時遙測展示", sec1)
    builder.add_section("⚡ 高並發協議效能評估：TCP/TLS 傳輸最佳化與 Apache Benchmark 模擬壓測", sec2)
    builder.add_section("🖥️ 虛擬專屬伺服器（VPS）容錯切換（Fault Tolerance）與無效請求抑制機制", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "進階人工智慧與最佳化研究所課程"',
        'event: "進階人工智慧與最佳化研究所課程"\ndate: "2025-02-20"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "AI-Optimization-03-感測器能源模型與高並發基準測試-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：感測器電池能源管理、高並發通訊協定（High Concurrency）、Apache Benchmark 壓力測試與 VPS 容錯  
> **授課教授**：授課講師（AI 與資訊工程領域講座教授）  
> **發表團隊**：國際學生專案團隊（Battery Packs Team）  
> **核心模組**：IoT Battery Sensing, Apache Benchmark, High Concurrency Protocol, VPS Fault Tolerance  
> **學習目標**：掌握物聯網感測節點低功耗採集、評估高並發情境下 TCP/TLS 傳輸瓶頸與伺服器故障轉移  
> **關聯文件**：[📄 完整原話逐字稿 (AI-Optimization-03-感測器能源模型與高並發基準測試-proofread.md)](./AI-Optimization-03-感測器能源模型與高並發基準測試-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Sensors["感測器硬體節點 (400 Battery Packs)"] --> Telemetry["低功耗遙測資料傳輸 (UDP / TCP Acceleration)"]
    Telemetry --> Load["高並發壓力模擬 (Apache Benchmark ab 工具)"]
    Load --> Test{"模擬大規模並發 TCP/TLS 請求"}
    Test --> VPS["虛擬主機叢集 (VPS Cluster)"]
    VPS --> FT["容錯切換架構 (Fault Tolerance)"]
    FT --> Filter["無效過期 Request 快速抑制 (避免雪崩效應)"]
    FT --> Result["達成微秒級切換與服務不中斷"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **大規模物聯網節點能源管理**：針對多達 400 組電池模組進行狀態監控，核心在於兼顧取樣頻率與節點省電模式，防止感測器因頻繁喚醒而過早耗盡電量。
2. **Apache Benchmark 壓測指引**：在模擬 High Concurrency 時，TCP 交握與 TLS 密鑰協商常成為瓶頸。藉由優化傳輸程序與早期丟棄失效請求，可大幅維持系統在極限狀態下的吞吐量。
"""
    summary_file = OUT_DIR / "AI-Optimization-03-感測器能源模型與高並發基準測試-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_lesson1()
    build_lesson2()
    build_lesson3()
