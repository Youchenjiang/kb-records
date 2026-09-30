#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 5-Master Industry Keynote Deliverable:
- 勤業眾信資安執行副總返校專題演講：生成式 AI 產業浪潮、企業資安治理與職場數位競爭力
Follows PROOFREAD_RULES.md, ScenarioType.CLASSROOM_LECTURE / SINGLE_TALK, and repository linters.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "5-Master" / "2026-IndustryKeynote-GenAI-Cybersecurity"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = REPO_ROOT / "transcribe_outputs" / "週五 15點03分 ai 演講" / "transcript_zh_tw.txt"

REPLACEMENTS = [
    (r"興業中心會計師事務所", "勤業眾信聯合會計師事務所"),
    (r"興業中心", "勤業眾信"),
    (r"捲簾\s*I", "GenAI（生成式 AI）"),
    (r"卷\s*AI", "GenAI"),
    (r"卷買商", "GenAI 商務應用"),
    (r"AI\s*A\s*卷", "AI Agent"),
    (r"治安", "資安"),
    (r"正大院畢業", "政大 EMBA"),
    (r"正大畢業", "政大 EMBA"),
    (r"一名老師", "主持教授"),
    (r"機械手背", "機械手臂"),
    (r"這也是治安社團", "資安社團"),
    (r"圍棋學長", "資安學長"),
    (r"偏攻棋研究", "攻防安全研究"),
]


def clean_text(text: str) -> str:
    res = text
    for pat, rep in REPLACEMENTS:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def segment_into_dialogue_paragraphs(text: str) -> str:
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
        if current_len >= 200 or s.endswith("好。") or s.endswith("OK。") or s.endswith("謝謝！"):
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
        if "先生，我這一說他是我們這一批" in p_clean or "我們先坐下，好不好" in p_clean:
            formatted_paras.append(f"**【主持教授】**：{p_clean}")
        elif "請問學長" in p_clean or "學長想請教" in p_clean:
            formatted_paras.append(f"**【現場學員】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【勤業眾信資安執行副總】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_keynote():
    print("Building Industry Keynote Deliverable...")
    raw = RAW_FILE.read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "產學大師講座：生成式 AI 產業浪潮、企業資安治理與職場數位競爭力"
    talk_id = "KEYNOTE-GENAI-SEC"
    event = "中央資管碩士班產業前瞻專題演講"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["勤業眾信資安執行副總", "主持教授", "現場學員"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.18)
    s2 = int(total_len * 0.40)
    s3 = int(total_len * 0.62)
    s4 = int(total_len * 0.82)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:s3])
    sec4 = segment_into_dialogue_paragraphs(cleaned[s3:s4])
    sec5 = segment_into_dialogue_paragraphs(cleaned[s4:])

    builder.add_section("🎯 勤業眾信校友開場：全台最大200人資安顧問團隊與政大EMBA進修分享", sec1)
    builder.add_section("🤖 生成式 AI（GenAI）爆發浪潮：企業大老闆核心焦慮與生產力變革實務", sec2)
    builder.add_section("⚠️ AI 雙面刃危機：新型資安威脅、人身安全風險與倫理規範防線", sec3)
    builder.add_section("🏢 企業 AI 轉型落地難題：文化阻力、組織慣性與殺手級應用醞釀", sec4)
    builder.add_section("🎓 給中央資管學弟妹的職涯指引：跨域財務能力、證照投資與實習管道", sec5)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "中央資管碩士班產業前瞻專題演講"',
        'event: "中央資管碩士班產業前瞻專題演講"\ndate: "2025-12-05"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "勤業眾信副總-生成式AI浪潮與企業資安治理-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **演講主題**：生成式 AI 爆發浪潮、企業數位轉型困境、新型資安風險防禦與職涯發展  
> **主講貴賓**：勤業眾信聯合會計師事務所（Deloitte）資安執行副總（中央資管系所校友）  
> **主辦單位**：國立中央大學資訊管理學系碩士班 前瞻產業專題講座  
> **核心模組**：Generative AI, Enterprise Cybersecurity Governance, IT Career Pathways  
> **學習目標**：理解企業大老闆對 AI 的真實焦慮、掌握跨域顧問職能與 AI 時代不可替代核心競爭力  
> **關聯文件**：[📄 完整原話逐字稿 (勤業眾信副總-生成式AI浪潮與企業資安治理-proofread.md)](./勤業眾信副總-生成式AI浪潮與企業資安治理-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["生成式 AI (GenAI) 浪潮襲來"] --> B["企業大老闆的真實關注點"]
    B --> B1["生產力百倍提升 vs. 殺手級應用尚未普及"]
    B --> B2["推動轉型的最大阻力：人與企業文化"]
    A --> C["新時代企業資安治理挑戰"]
    C --> C1["資料隱私外洩 (員工將機敏 Prompt 餵入公有雲模型)"]
    C --> C2["模型對抗攻擊 (Jailbreak, Prompt Injection)"]
    C --> C3["實體世界連動：從軟體漏洞蔓延至機器人與人身安全"]
    D["中央學弟妹未來競爭力打造"] --> E["技術深耕 (Cybersecurity / SAP / 網路底層)"]
    D --> F["跨域賦能 (商業思維 / 財務會計理解 / 溝通表達)"]
    D --> G["善用 AI 加速產出，但保留核心批判性思考"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **AI 轉型的最大阻力永遠是「人」**：工具推陳出新極其快速，但企業內部既有流程、組織官僚文化與員工抗拒改變的心態，是 GenAI 無法在短期內轉化為殺手級應用的主要癥結。
2. **資安諮詢的高門檻與市場需求**：勤業眾信擁有全台最大的 200 人資安顧問團隊，負責政府核心機關與跨國企業的高規格資安審查與合規建置，資安業務是全事務所成長最迅猛、營收最高的業務板塊之一。
3. **不可替代的跨域 T 型人才**：純懂寫 Code 或純懂調包的工程師極易被 AI 替代。未來的頂尖顧問必須一手掌握網路與系統資安技術底層，另一手具備財務會計、法律合規與管理溝通的綜合治理視野。
"""
    summary_file = OUT_DIR / "勤業眾信副總-生成式AI浪潮與企業資安治理-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_keynote()
