#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 5-Master Research Deliverables:
1. 碩士研究專題報告：基於敏感 API 行為子圖與 GNN/LLM 之 Android 抗混淆惡意程式檢測 (12點32分 + 12點33分 + 12點35分)
2. 實驗室專案會議：新年度整合型產學研究計畫提案、容錯平台架構與資安模組整合 (12點28分)
Follows PROOFREAD_RULES.md, ScenarioType.SINGLE_TALK / MULTI_PAPER, and repository linters.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "5-Master" / "2026-MasterResearch-AndroidMalware"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"

REPLACEMENTS = [
    (r"A\s*B\s*K", "APK"),
    (r"A\s*P\s*K", "APK"),
    (r"工作費的\s*APK", "良性與惡意的 APK"),
    (r"O\s*P\s*code", "Opcode"),
    (r"OB\s*減", "Opcode 頻率"),
    (r"permission", "Permission（權限宣告）"),
    (r"G\s*N\s*N", "GNN（圖神經網路）"),
    (r"G\s*N", "GNN"),
    (r"L\s*M", "LLM / LM"),
    (r"embedding", "Embedding（嵌入向量）"),
    (r"二一測試", "惡意程式測試"),
    (r"二一", "惡意"),
    (r"真確反二一", "偵測反惡意軟體"),
    (r"真確產品", "偵測防毒產品"),
    (r"真確準確率", "偵測準確率"),
    (r"真確", "偵測"),
    (r"抗苗", "抗混淆"),
    (r"扣回的的圖結構", "Call Graph 調用圖結構"),
    (r"V\s*N", "VM"),
    (r"V\s*M", "VM（虛擬主機）"),
    (r"梁永時陳老師", "陳教授與梁老師"),
    (r"治安", "資安"),
    (r"花捲", "專案"),
]


def clean_text(text: str) -> str:
    res = text
    for pat, rep in REPLACEMENTS:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def segment_into_dialogue_paragraphs(text: str, default_speaker="發表研究生") -> str:
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
        if current_len >= 220 or s.endswith("好。") or s.endswith("OK。") or s.endswith("謝謝老師。"):
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
        if any(trig in p_clean for trig in ["老師說", "我想請教", "老師認為", "我的問題是", "為什麼現存的方法"]):
            formatted_paras.append(f"**【指導教授】**：{p_clean}")
        elif any(trig in p_clean for trig in ["梁老師", "陳老師", "我的建議是", "王老師提出"]):
            formatted_paras.append(f"**【陳教授 / 共同指導】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_thesis_seminar():
    print("Building Master Thesis Seminar Deliverable...")
    # Combine 12:32, 12:33, 12:35
    t1 = (RAW_DIR / "週四 12點32分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    t2 = (RAW_DIR / "週四 12點33分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    t3 = (RAW_DIR / "週四 12點35分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    combined = t1 + "\n\n" + t2 + "\n\n" + t3
    cleaned = clean_text(combined)

    title = "碩士研究進度報告：基於敏感 API 行為子圖與 GNN/LLM 之 Android 抗混淆惡意程式檢測"
    talk_id = "MASTER-THESIS-ANDROID-GNN"
    event = "中央資管實驗室專題研究進度研討會"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["發表研究生 (Youchen)", "指導教授", "陳教授 / 共同指導"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.25)
    s2 = int(total_len * 0.55)
    s3 = int(total_len * 0.80)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1], default_speaker="發表研究生 (Youchen)")
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2], default_speaker="發表研究生 (Youchen)")
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:s3], default_speaker="發表研究生 (Youchen)")
    sec4 = segment_into_dialogue_paragraphs(cleaned[s3:], default_speaker="發表研究生 (Youchen)")

    builder.add_section("🎯 參考文獻架構剖析：敏感 API 錨點切分、Call Graph 與 Opcode 頻率特徵限制", sec1)
    builder.add_section("🛡️ Android 市場混淆現況分析：66.4% 混淆率挑戰與傳統防毒檢測崩潰成因", sec2)
    builder.add_section("🔬 靜態檢測 vs. 圖表示學習（GNN）：特徵向量串接與抗對抗混淆策略", sec3)
    builder.add_section("💡 核心創新架構提案：結合行為子圖結構拓撲與 LLM Embedding 強化分類器", sec4)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "中央資管實驗室專題研究進度研討會"',
        'event: "中央資管實驗室專題研究進度研討會"\ndate: "2026-02-26"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "碩士研究專題-Android惡意程式行為子圖與抗混淆GNN檢測-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **研究主題**：Android 惡意程式檢測、代碼混淆（Code Obfuscation）對抗防禦、敏感 API 行為子圖與 GNN/LLM 融合架構  
> **發表報告者**：發表研究生 (Youchen)  
> **指導教授**：實驗室指導教授群、陳教授  
> **核心模組**：Android Static Analysis, Sensitive API Slicing, Graph Neural Networks (GNN), Large Language Models (LLM)  
> **學習目標**：突破傳統防毒在面對 66.4% 混淆代碼時準確率暴跌之瓶頸，提出行為子圖與語意 Embedding 融合檢測模型  
> **關聯文件**：[📄 完整原話逐字稿 (碩士研究專題-Android惡意程式行為子圖與抗混淆GNN檢測-proofread.md)](./碩士研究專題-Android惡意程式行為子圖與抗混淆GNN檢測-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    APK["原始 Android 應用程式 (APK)"] --> CFG["反編譯生成調用圖 (Call Graph / CFG)"]
    CFG --> Anchor["以敏感系統 API (SmsManager, Telephony, Crypto) 為錨點"]
    Anchor --> Slicing["圖切分演算法提取行為子圖 (Behavior Subgraphs)"]
    Slicing --> Feat1["結構拓撲特徵 (Opcode 序列 + 權限 Permission)"]
    Slicing --> Feat2["語意 Embedding (透過預訓練 LLM 提取上下文語意)"]
    Feat1 & Feat2 --> Concat["多模態特徵串接 (Feature Concatenation)"]
    Concat --> GNN["圖神經網路分類器 (GNN / GCN / GAT)"]
    GNN --> Result{"惡意程式分類判定 (Malicious vs. Benign)"}
    Result -.->|抗混淆評測| Test["面對 Identifiers 重命名、控制流平坦化仍維持高精確度"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **混淆對抗痛點**：Android 生態系高達 66.4% 的惡意軟體採用了進階混淆技術（如 ProGuard、Allatori、控制流混淆）。傳統依賴單純 Opcode 頻率或權限聲明的靜態檢測模型在遇到混淆樣本時檢測率大幅驟降。
2. **敏感 API 錨點切分**：不依賴全局易被擾動的代碼結構，而是聚焦於 Android 框架底層無法被混淆的關鍵敏感 API（如收發簡訊、讀取 IMEI、動態載入 Dex），以此為核心向外擴展切分局部行為子圖。
3. **結構與語意的雙重融合**：本研究創新結合行為子圖之拓撲連接關係（GNN）與指令上下文語意特徵（LLM Embedding），使模型能深刻洞察程式真實惡意意圖，具備極強的抗混淆魯棒性。
"""
    summary_file = OUT_DIR / "碩士研究專題-Android惡意程式行為子圖與抗混淆GNN檢測-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_lab_meeting():
    print("Building Lab Project Meeting Deliverable...")
    raw = (RAW_DIR / "週四 12點28分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_text(raw)

    title = "實驗室專案會議：新年度整合型產學研究計畫提案、容錯平台架構與資安模組整合"
    talk_id = "LAB-MEETING-INTEGRATED-PROJECT"
    event = "中央資管實驗室新年度整合型計畫研討會"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["計畫主持人 / 指導教授", "陳教授 / 共同主持", "研究團隊各組成員"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.20)
    s2 = int(total_len * 0.40)
    s3 = int(total_len * 0.60)
    s4 = int(total_len * 0.80)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1], default_speaker="計畫主持人 / 指導教授")
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2], default_speaker="研究團隊各組成員")
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:s3], default_speaker="研究團隊各組成員")
    sec4 = segment_into_dialogue_paragraphs(cleaned[s3:s4], default_speaker="研究團隊各組成員")
    sec5 = segment_into_dialogue_paragraphs(cleaned[s4:], default_speaker="陳教授 / 共同主持")

    builder.add_section("🎯 新年度整合型計畫總體策略：容錯開放平台、使用者生態與資安架構轉型方案", sec1)
    builder.add_section("📱 行動安全與程式碼檢測小組：知識圖譜結合動態 RAG 之即時漏洞分析架構", sec2)
    builder.add_section("🛡️ 單元測試（Unit Test）與開發安全路徑：AI 輔助寫程式之潛在漏洞防範討論", sec3)
    builder.add_section("🖥️ 虛擬化平台與容錯子計畫：VM 忙碌度指標（ROP/IOP）與時序同步效能分析", sec4)
    builder.add_section("📋 教授總結點評與各子計畫交期協調：跨模組資料介接與實驗數據規格統一", sec5)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "中央資管實驗室新年度整合型計畫研討會"',
        'event: "中央資管實驗室新年度整合型計畫研討會"\ndate: "2025-10-03"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "實驗室專案會議-新年度整合型研究計畫與平台架構規劃-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"""# 🛡️ {talk_id} {title}

> **會議主題**：新年度整合型產學研究計畫架構討論、行動資安檢測、知識圖譜 RAG 與 VM 容錯效能指標  
> **主持人 / 指導教授**：指導教授、陳教授、全體碩博士研究團隊  
> **核心模組**：Integrated Research Project, Mobile Security, Fault-Tolerant Cloud, RAG & Knowledge Graph  
> **學習目標**：協同三大子計畫模組、統一跨系統資料格式與 VM 同步度量評估標準  
> **關聯文件**：[📄 完整原話逐字稿 (實驗室專案會議-新年度整合型研究計畫與平台架構規劃-proofread.md)](./實驗室專案會議-新年度整合型研究計畫與平台架構規劃-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Main["新年度整合型研究計畫總架構"] --> Sub1["子計畫一：雲端容錯虛擬化平台 (Fault-Tolerant VM)"]
    Main --> Sub2["子計畫二：行動 App 安全檢測 (Mobile Security & RAG)"]
    Main --> Sub3["子計畫三：AI 輔助代碼安全與知識圖譜治理"]
    Sub1 --> E1["ROP / IOP 效能指標監控與同步收斂"]
    Sub2 --> E2["靜態分析 + 執行階段動態分析雙重把關"]
    Sub3 --> E3["即時漏洞知識庫比對，防範 AI 生成程式碼漏洞"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **整合型計畫三大核心支柱**：容錯雲端底座、行動資安防護與 AI 程式碼安全稽核。確保各子計畫研發成果能無縫介接在統一的開放平台上。
2. **AI 工具輔助開發之風險防範**：針對開發人員日漸仰賴 AI 生成程式碼的趨勢，引入知識圖譜與動態 RAG 技術，在 Unit Test 階段即時阻斷未經修補之安全漏洞。
3. **VM 效能衡量統一化**：利用 IOP/ROP 度量指標量化虛擬機器的資源活躍度與同步延遲，確保容錯切換（Fault Tolerance）時業務不中斷。
"""
    summary_file = OUT_DIR / "實驗室專案會議-新年度整合型研究計畫與平台架構規劃-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_thesis_seminar()
    build_lab_meeting()
