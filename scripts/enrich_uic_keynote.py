#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enrich 20251208 UIC Keynote with the missing second half from 文件2.md:
- Section 3: Judea Pearl's Ladder of Causality (Association, Intervention, Counterfactuals)
- Section 4: Causal Diagrams, Transportability/Generalization across domains, and Q&A
"""

from pathlib import Path
import re
import sys
import opencc

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import validate_transcript_structure

cc = opencc.OpenCC('s2twp')

DOC2_PATH = REPO_ROOT / "文件2.md"
raw_lines = [l.strip() for l in DOC2_PATH.read_text(encoding="utf-8").splitlines()]

part_a_lines = raw_lines[1:439]
part_b_lines = raw_lines[880:1149]

KEYNOTE_DIR = REPO_ROOT / "5-Master/1-First-Year/Fall-Semester/20251208-UIC-XAI-Keynote"
FULL_FILE = KEYNOTE_DIR / "20251208-可解釋AI因果推論與反事實決策.full.md"
SUMMARY_FILE = KEYNOTE_DIR / "20251208-可解釋AI因果推論與反事實決策.md"


def clean_tw(text: str) -> str:
    t = cc.convert(text)
    replacements = [
        ("人工智能", "人工智慧"),
        ("信息管理", "資訊管理"),
        ("數據庫", "資料庫"),
        ("代碼", "程式碼"),
        ("服務器", "伺服器"),
        ("內存", "記憶體"),
        ("總線", "匯流排"),
        ("猶大·珀爾", "猶太·珠爾（Judea Pearl，圖靈獎得主）"),
        ("猶大·珠爾", "猶太·珠爾（Judea Pearl）"),
        ("為何之書", "《The Book of Why》（為什麼之書）"),
    ]
    for old, new in replacements:
        t = t.replace(old, new)
    return t


def parse_and_consolidate(lines_subset, speaker="Prof. Ali (UIC)", min_chars=320):
    pairs = []
    i = 0
    while i < len(lines_subset):
        line = lines_subset[i]
        if not line:
            i += 1
            continue
        has_cjk = any('\u4e00' <= c <= '\u9fff' for c in line)
        if not has_cjk:
            en = line
            zh = ""
            if i + 1 < len(lines_subset):
                next_l = lines_subset[i + 1]
                if any('\u4e00' <= c <= '\u9fff' for c in next_l):
                    zh = next_l
                    i += 1
            pairs.append((en, zh))
        else:
            pairs.append(("", line))
        i += 1

    consolidated = []
    curr_en = []
    curr_zh = []
    curr_len = 0

    for en, zh in pairs:
        curr_en.append(en)
        curr_zh.append(zh)
        curr_len += len(en)

        if curr_len >= min_chars and en.rstrip().endswith(('.', '?', '!', '。', '？', '！')):
            en_p = " ".join(curr_en)
            zh_clean = " ".join([clean_tw(z) for z in curr_zh if z])
            zh_clean = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', zh_clean)
            consolidated.append((en_p, zh_clean))
            curr_en = []
            curr_zh = []
            curr_len = 0

    if curr_en:
        en_p = " ".join(curr_en)
        zh_clean = " ".join([clean_tw(z) for z in curr_zh if z])
        zh_clean = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', zh_clean)
        consolidated.append((en_p, zh_clean))

    paras = []
    for en_p, zh_p in consolidated:
        md = f"**【{speaker}】**：{en_p}\n\n> **繁中翻譯**：{zh_p}"
        paras.append(md)

    return "\n\n".join(paras)


def enrich_keynote():
    print("Enriching UIC Keynote with missing second half...")
    sec3_content = parse_and_consolidate(part_a_lines, speaker="Prof. Ali (UIC)")
    sec4_content = parse_and_consolidate(part_b_lines, speaker="Prof. Ali (UIC)")

    existing_content = FULL_FILE.read_text(encoding="utf-8")
    
    # Check if section 3 already present
    if "因果推論階梯" in existing_content:
        print("  Keynote already enriched!")
        return

    enriched_content = existing_content.rstrip() + "\n\n" + \
        "## 🏛️ 因果推論階梯（Ladder of Causality）：關聯、干預與反事實決策\n\n" + \
        sec3_content + "\n\n" + \
        "## 🗺️ 因果圖模型、跨情境遷移學習（Transportability）與學術問答\n\n" + \
        sec4_content + "\n"

    is_valid, errors = validate_transcript_structure(enriched_content, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Enriched Keynote validation failed: {errors}")

    FULL_FILE.write_text(enriched_content, encoding="utf-8")
    print(f"  [OK] Saved {FULL_FILE.name}")

    # Update summary
    new_summary = """# 🎙️ KEYNOTE-UIC-XAI-CAUSAL-AI 國際頂尖學者講座：可解釋人工智慧 XAI、因果推論與反事實決策模型

> **講座主題**：可解釋人工智慧（Explainable AI, XAI）、因果推論（Causal Inference）、猶太·珠爾因果之梯與反事實決策  
> **日期**：2025-12-08  
> **特聘主講**：Prof. Ali（University of Illinois Chicago 資訊與計算科學系主任、MIT 頂級期刊資深主編）  
> **對談主持**：資管系主任、全體與會學者  
> **核心模組**：Explainable AI, Judea Pearl Ladder of Causality, Do-Calculus, Transportability, Counterfactual Reasoning  
> **學習目標**：理解現代深度學習在黑盒子預測與偏誤來源之根本瓶頸，掌握如何從純關聯性觀察跨越至干預（Intervention）與反事實政策模擬  
> **關聯文件**：[📄 完整雙語原話逐字稿 (20251208-可解釋AI因果推論與反事實決策.full.md)](./20251208-可解釋AI因果推論與反事實決策.full.md)

---

## Executive Summary

本場特聘學者國際專題講座由**伊利諾大學芝加哥分校（UIC）**資訊與計算科學系主任 **Prof. Ali** 蒞臨主講，深入剖析當前主流深度學習與大語言模型（LLMs）在「可解釋性（Explainability）」與「決策可信度」上的內生瓶頸。

講座深刻指出，當前機器學習系統本質僅能捕捉數據間的**統計關聯性（Correlations）**，而無法回答「**為什麼（Why）**」以及「**若政策介入改變環境時會發生什麼（What If）**」。Prof. Ali 系統性引介了圖靈獎得主猶太·珠爾（Judea Pearl）於《The Book of Why》中提出的**因果之梯（Ladder of Causality）**三大層級（觀察關聯 ➔ 主動干預 ➔ 反事實推演），並示範如何運用因果圖（Causal DAGs）與 Do-Calculus 克服遺漏變數偏誤（如抽菸混淆咖啡與癌症關聯），進而實現跨領域、跨國界的**模型遷移學習（Transportability / Generalization）**。演講下半場完整收錄現場學者關於醫療給藥、公共政策模擬與因果 AI 未來研究方向之精彩深度問答。

---

## 🏛️ 猶太·珠爾因果推論階梯 (The Ladder of Causality)

```mermaid
flowchart TD
    subgraph Level3["層級三：反事實推論 (Counterfactuals)"]
        L3_Act["反事實回顧：若當初採取不同決策，結果會如何？<br/>(What if we had acted differently?)"]
        L3_App["應用：醫療個人化用藥歸因、法律責任判定、政策回溯評估"]
    end

    subgraph Level2["層級二：干預與操作 (Intervention)"]
        L2_Act["主動介入：如果我們實施政策 do(X)，將會發生什麼？<br/>(What will happen if we take action?)"]
        L2_App["應用：A/B 測試、因果圖模型 Causal DAGs、Do-Calculus"]
    end

    subgraph Level1["層級一：關聯與觀察 (Association)"]
        L1_Act["被動觀察：若觀察到 X，則 Y 的機率是多少？<br/>(What does a symptom tell us about a disease?)"]
        L1_App["應用：傳統機器學習、統計相關性、深度神經網絡預測"]
    end

    Level1 -->|引入主動介入 do(X)| Level2
    Level2 -->|引入反事實想像與回顧| Level3
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 關聯性不等於因果性 (Correlation ≠ Causation)
- **遺漏變數偏誤（Omitted Variable Bias）**：數據顯示喝咖啡者罹癌率較高，但背後的真實混淆變數為吸菸習慣。若缺乏因果圖模型梳理機制，模型將給出「禁止喝咖啡以防癌」的荒謬建議。
- **大模型的預測極限**：ChatGPT 等基於關聯性統計預測的模型，在面對「從未發生過之政策衝擊（Policy Shifts）」時必然失效，必須結合因果 AI 架構。

### 2. 因果圖模型與 Do-Calculus
- **Do-Calculus 數學推導**：Judea Pearl 開發之介入運算體系，能將含有 `do(X)` 介入項的因果機率，轉譯為可在純觀察性數據上計算的統計表達式。
- **跨情境遷移能力（Transportability）**：當研究在某一國家或族群完成後，藉由因果圖比對兩地環境的特徵差異，能精確推估該成果是否能無偏轉移至新環境中應用。

### 3. 醫療與決策洞察的反事實推演
- **個人化醫療（Personalized Medicine）**：針對特定年齡、病史病患評估每日服用阿司匹靈之淨效益，需要層級三的反事實推演能力，而非僅看大群體統計平均值。
"""
    SUMMARY_FILE.write_text(new_summary, encoding="utf-8")
    print(f"  [OK] Saved {SUMMARY_FILE.name}")


if __name__ == "__main__":
    enrich_keynote()
