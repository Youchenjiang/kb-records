#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Research Methodology Week 01 Deliverables from 文件2.md lines 1491 to 2605:
- 20260225-研究方法-01-課程導論與研究動機.full.md
- 20260225-研究方法-01-課程導論與研究動機.md
"""

from pathlib import Path
import re
import sys
import opencc

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

cc = opencc.OpenCC('s2twp')

DOC2_PATH = REPO_ROOT / "文件2.md"
raw_lines = [l.strip() for l in DOC2_PATH.read_text(encoding="utf-8").splitlines()]
rm_lines = raw_lines[1491:2605]


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
        ("中華電氣", "中華電信"),
        ("寫城績", "寫程式"),
        ("寫城市", "寫程式"),
        ("AR寫的", "AI 寫的"),
    ]
    for old, new in replacements:
        t = t.replace(old, new)
    return t


def segment_into_paragraphs(lines_subset, min_chars=300):
    paragraphs = []
    curr_lines = []
    curr_len = 0
    curr_speaker = "授課講師"

    for l in lines_subset:
        if not l:
            continue
        cleaned = clean_tw(l)
        
        # Check student triggers
        if any(trig in cleaned for trig in ["老師請問", "我想問", "請問老師", "是不是"]):
            if curr_lines:
                text_p = "".join(curr_lines)
                paragraphs.append((curr_speaker, text_p))
                curr_lines = []
                curr_len = 0
            curr_speaker = "學員" if any(trig in cleaned for trig in ["老師請問", "我想問", "請問老師"]) else "授課講師"

        curr_lines.append(cleaned)
        curr_len += len(cleaned)

        if curr_len >= min_chars and any(cleaned.endswith(p) for p in ["。", "！", "？", "；", "."]):
            text_p = "".join(curr_lines)
            paragraphs.append((curr_speaker, text_p))
            curr_lines = []
            curr_len = 0
            curr_speaker = "授課講師"

    if curr_lines:
        text_p = "".join(curr_lines)
        paragraphs.append((curr_speaker, text_p))

    formatted = []
    for spk, text in paragraphs:
        formatted.append(f"**【{spk}】**：{text}")
    return "\n\n".join(formatted)


def build_research_methodology():
    print("Building Research Methodology Week 01 Deliverables...")
    out_dir = REPO_ROOT / "5-Master/1-First-Year/Spring-Semester/ResearchMethodology"
    out_dir.mkdir(parents=True, exist_ok=True)

    t_len = len(rm_lines)
    s1 = int(t_len * 0.33)
    s2 = int(t_len * 0.66)

    sec1 = segment_into_paragraphs(rm_lines[:s1])
    sec2 = segment_into_paragraphs(rm_lines[s1:s2])
    sec3 = segment_into_paragraphs(rm_lines[s2:])

    builder = ProofreadBuilder(
        title="資訊管理研究方法論 Week 01：課程導論、研究動機與 AI 時代下的學者競爭力",
        event="資訊管理研究所研究方法論課程",
        talk_id="RES-METH-00-ORIENTATION",
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    builder.add_section("🎯 研究所為什麼要做研究？研究動機、學術獨立思考與研究生核心價值", sec1)
    builder.add_section("🤖 生成式 AI 時代下的學者競爭力：專業淘汰危機與管理學院應用研究本質", sec2)
    builder.add_section("📜 嚴謹研究設計準則與學術誠信：研究倫理審查、研究限制與清晰論文寫作", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "資訊管理研究所研究方法論課程"',
        'event: "資訊管理研究所研究方法論課程"\ndate: "2026-02-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"RM validation failed: {errors}")

    full_path = out_dir / "20260225-研究方法-01-課程導論與研究動機.full.md"
    full_path.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {full_path.name}")

    summary_content = """# 🎙️ RES-METH-00-ORIENTATION 資訊管理研究方法論 Week 01：課程導論、研究動機與 AI 時代下的學者競爭力

> **課程主題**：碩士班研究方法導論、研究動機與問題意識、生成式 AI 衝擊與管理學院實務價值  
> **日期**：2026-02-25  
> **授課教授**：授課講師（資管系資深講座教授、教育部學術獎得主）  
> **對談學員**：資管所碩一全體研究生、大四直升預研生  
> **核心領域**：研究方法論（Research Methodology）、問題導向研究（Problem-Oriented）、生成式 AI 替代性、管理學院應用價值、研究倫理  
> **學習目標**：理解研究生撰寫論文之本質與學術思維訓練，掌握在 AI 時代如何聚焦具備企業實務價值與理論深度的研究題目  
> **關聯文件**：[📄 完整原話逐字稿 (20260225-研究方法-01-課程導論與研究動機.full.md)](./20260225-研究方法-01-課程導論與研究動機.full.md)

---

## Executive Summary

本篇為國立中央大學資訊管理研究所 114 學年度第二學期碩士班核心必修課程——**《研究方法論》（Research Methodology）**開學第一堂導論課之完整雙軌紀錄。

授課教授開宗明義拋出靈魂提問：**「研究生為什麼要念研究所？為什麼要做研究、寫論文？」**。教授犀利指出，現代社會「越純技術、越單一專業的技能，越容易被 AI 迅速取代」；大型科技企業已大幅縮減純初階工程師需求。管理學院資訊管理研究生的核心立足點在於**「問題導向（Problem-Oriented）」**——理解真實企業組織如何運作，並運用資訊科技、數據模型與系統架構去解決實際瓶頸。本堂課詳細梳理了學術嚴謹度、可復現性、研究倫理委員會審查，以及論文寫作必須「清晰、直接了當（Straightforward）」之基本要求。

---

## 🏛️ 研究思維與 AI 時代競爭力定位

```mermaid
flowchart TD
    Reality["現實挑戰: 生成式 AI 高效產出代碼與文字<br/>👉 純技術執行人員面臨嚴峻替代危機"] --> Reflection{"研究生核心價值反思"}
    
    Reflection --> CoreValue["學術研究方法論的核心素養"]
    
    subgraph CoreValue["研究方法三大支柱"]
        Problem["1. 敏銳問題意識 (Problem-Oriented)<br/>洞察真實組織與產業痛點"]
        Logic["2. 嚴密因果邏輯與推論 (Inference)<br/>不盲信表面相關性，建立因果鏈"]
        Rigor["3. 周延研究設計 (Rigor & Ethics)<br/>可復現實驗、倫理審查與誠實限制"]
    end

    CoreValue --> Solution["企業實務賦能 (Business Value)"]
    Solution --> Output["產出具備長遠學術價值與產業效益之碩士論文"]
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 為什麼要念碩士與做研究？
- **從被動解題走向主動命題**：大學部多為吸收已知知識與照表操課，研究所的精髓在於「學會探索未知的科學方法」。撰寫論文是訓練研究生獨立邏輯推演與批判性思考的最佳沙盤推演。
- **管理學院的本質是「應用」**：我們不做無人問津的象牙塔空談，所有資訊管理研究最終必須落地於協助企業提升營運效能與決策品質。

### 2. 生成式 AI 時代的「專家危機」
- **單一專業最易淘汰**：當前 AI 寫程式不會累且產出飛快。只會撰寫基礎代碼的初階人力正被大量取代，唯有具備跨領域整合、商業洞察與嚴謹因果論證能力的研究者才能立於不敗之地。

### 3. 論文寫作的黃金法則：直接了當 (Straightforward)
- **拒絕晦澀堆砌**：好的學術寫作應當乾淨、精準、毫不拖泥帶水。所有推論必須透明交代實驗過程以確保可復現性（Replicability），誠實揭露研究限制而非隱瞞瑕疵。
"""
    summary_path = out_dir / "20260225-研究方法-01-課程導論與研究動機.md"
    summary_path.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_path.name}")


if __name__ == "__main__":
    build_research_methodology()
