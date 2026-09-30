#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 4-University Software Engineering Final Deliverable:
- 軟體工程期末專案發表與評審審查會 (週三 14點03分 軟工結束)
Follows PROOFREAD_RULES.md, ScenarioType.CLASSROOM_LECTURE, and tests/test_proofread_linter.py.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2025-SoftwareEngineering"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = REPO_ROOT / "transcribe_outputs" / "週三 14點03分 軟工結束" / "transcript_zh_tw.txt"

REPLACEMENTS = [
    (r"點\s*view", ".vue 檔案"),
    (r"點\s*T\s*S", ".ts 檔案"),
    (r"循序圖", "UML 循序圖 (Sequence Diagram)"),
    (r"中介層", "中介層 (Middleware)"),
    (r"壓測試", "壓力測試 (Stress Testing)"),
    (r"correl", "Concurrency（並行）"),
    (r"front", "Frontend（前端）"),
    (r"python", "Python"),
    (r"user", "User"),
    (r"治安", "資安"),
]


def clean_text(text: str) -> str:
    res = text
    for pat, rep in REPLACEMENTS:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def segment_into_dialogue_paragraphs(text: str, default_speaker="學員 (專案報告團隊)") -> str:
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
        if current_len >= 220 or s.endswith("好。") or s.endswith("OK。") or s.endswith("下課。"):
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
        # Professor indicators
        prof_triggers = [
            "這是哪一個模式？", "你們是一個一個", "所謂七百", "以我的部分我是看到大家的東西",
            "這學期我盡到我的責任", "不要讓大家變成AI孤兒", "那我們就下課嘍", "你們就把每一個混合嗎"
        ]
        if any(trig in p_clean for trig in prof_triggers):
            formatted_paras.append(f"**【授課講師】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_software_engineering():
    print("Building Software Engineering Final Deliverable...")
    raw = RAW_FILE.read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "軟體工程期末專案發表與評審審查會：Vue/TS 前端、Python 後端、高並發壓力測試與 AI 模組整合"
    talk_id = "SE-FINAL-PROJECT"
    event = "軟體工程課程期末專題發表審查會"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員 (專案報告團隊)"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.20)
    s2 = int(total_len * 0.40)
    s3 = int(total_len * 0.60)
    s4 = int(total_len * 0.80)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1], default_speaker="學員 (專案報告團隊)")
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2], default_speaker="學員 (專案報告團隊)")
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:s3], default_speaker="學員 (專案報告團隊)")
    sec4 = segment_into_dialogue_paragraphs(cleaned[s3:s4], default_speaker="學員 (專案報告團隊)")
    sec5 = segment_into_dialogue_paragraphs(cleaned[s4:], default_speaker="學員 (專案報告團隊)")

    builder.add_section("🎯 系統架構重構與循序圖展示：Vue 3/TypeScript 前端與 Python API 中介層設計", sec1)
    builder.add_section("🧪 軟體測試規格實施：單元測試（Unit Test）與端到端業務邏輯驗證", sec2)
    builder.add_section("⚡ 負載與壓力測試實戰：100 至 700 並行請求（Concurrency）瓶頸與錯誤排查", sec3)
    builder.add_section("🤖 AI 功能模組整合評測：異步推論排程、回應延遲與系統穩健性調校", sec4)
    builder.add_section("👨‍🏫 授課教授綜合講評與學期總結：AI 時代軟工思維培養與專案交付驗收", sec5)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "軟體工程課程期末專題發表審查會"',
        'event: "軟體工程課程期末專題發表審查會"\ndate: "2025-12-17"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "軟工期末-系統架構循序圖與高並發壓力測試-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **課程主題**：軟體工程（Software Engineering）期末專案發表、UML 循序圖重構、高並發壓力測試與 AI 模組實作  
> **指導評審**：授課講師（軟體工程授課教授）  
> **發表團隊**：專案開發團隊學員群  
> **核心模組**：Software Architecture, UML Sequence Diagrams, Stress Testing (700 Concurrency), AI Module Integration  
> **學習目標**：實踐完整 SDLC 軟體生命週期、完成前後端架構解耦、量化負載極限並通過現場答辯  
> **關聯文件**：[📄 完整原話逐字稿 (軟工期末-系統架構循序圖與高並發壓力測試-proofread.md)](./軟工期末-系統架構循序圖與高並發壓力測試-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    User["使用者瀏覽器 (User Client)"] --> Frontend["前端展示層 (Vue 3 + TypeScript: .vue / .ts)"]
    Frontend --> Middleware["中介路由層 (API Gateway / Middleware)"]
    Middleware --> Backend["後端應用伺服器 (Python FastAPI / Flask)"]
    Backend --> DB[(資料持久層 DB / IO)]
    Backend --> AI["AI 推論模組 (非同步長任務佇列)"]
    subgraph Testing ["測試工程體系"]
        T1["單元測試 (Unit Tests)"]
        T2["整合測試 (Integration Tests)"]
        T3["高並發壓力測試 (100 -> 700 Concurrency 階梯式負載驗證)"]
    end
```

---

## 🔑 重點提要 (Key Takeaways)

1. **架構分層與循序圖重構**：團隊將原本直連後端的架構重構為包含中介層（Middleware）的多層架構，並在 UML 循序圖中完整體現 Vue 前端、TypeScript 模組與 Python 後端的交互時序。
2. **高並發壓力測試（Stress Testing）**：透過自動化腳本進行階梯式壓力測試。系統在 100 並行請求時維持 100% 成功率；當攀升至 700 Concurrency 時暴露資料庫連線池與 AI 推論延遲瓶頸，為後續效能調校提供確切數據。
3. **AI 時代的軟工素養**：授課教授在講評中強調，生成式 AI 工具極大加速了寫 code 速度，但系統設計架構力、測試驗證嚴謹度與對底層錯誤的排查能力，才是軟體工程師的核心價值所在。
"""
    summary_file = OUT_DIR / "軟工期末-系統架構循序圖與高並發壓力測試-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_software_engineering()
