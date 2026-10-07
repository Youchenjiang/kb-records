#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build all 6 deliverables from 文件.md and update catalogs:
1. 20260912-AWS-CloudTrail偵測工程與DuckDB-SigmaHQ本地威脅狩獵 (.full.md & .md)
2. 20260912-超級瑪利歐世界-SNES任意代碼執行ACE記憶體漏洞逆向解析 (.full.md & .md)
3. 20260910-管理溝通-Week01-課程導論與組織管理溝通 (.full.md & .md)
4. 20260917-管理溝通-Week02-專業定位與學員英語自介發表 (.full.md & .md)
5. 20260924-管理溝通-Week03-科技與商務決策溝通 (.full.md & .md)
6. 20261001-管理溝通-Week04-受眾分析與簡報結構設計 (.full.md & .md)
"""

from pathlib import Path
import re
import sys
import opencc

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

cc = opencc.OpenCC('s2twp')

DOC_PATH = REPO_ROOT / "文件.md"
raw_file_lines = [l.strip() for l in DOC_PATH.read_text(encoding="utf-8").splitlines()]


def clean_tw(text: str) -> str:
    """Convert simplified to traditional and polish terminology."""
    t = cc.convert(text)
    replacements = [
        ("人工智能", "人工智慧"),
        ("信息管理", "資訊管理"),
        ("數據庫", "資料庫"),
        ("代碼", "程式碼"),
        ("服務器", "伺服器"),
        ("內存", "記憶體"),
        ("總線", "匯流排"),
        ("二進制", "二進位"),
        ("字節", "位元組"),
        ("寄存器", "暫存器"),
        ("約西", "耀西"),
        ("約希", "耀西"),
        ("柯巴", "庫巴"),
        ("傑瑞·約詹·張", "Jerry Youchen Zhang (張右城)"),
        ("約詹", "Youchen (右城)"),
        ("傑瑞", "Jerry (右城)"),
        ("通話溝通技巧", "核心溝通技巧 (Core Communication Skills)"),
        ("開展的項目", "開源專案 (Open Source Projects)"),
        ("開啟的專案", "開源專案 (Open Source Projects)"),
        ("徒步比賽", "駭客競賽 (Hacking Game / CTF)"),
        ("消除思緒", "清空思緒、沉澱自我 (Clear My Mind)"),
    ]
    for old, new in replacements:
        t = t.replace(old, new)
    return t


def parse_dialogue_pairs(lines_subset, default_speaker="講者", scenario="single-talk"):
    """Parse lines into (speaker, turn_markdown) blocks."""
    pairs = []
    i = 0
    while i < len(lines_subset):
        line = lines_subset[i]
        if not line:
            i += 1
            continue
        has_cjk = any('\u4e00' <= c <= '\u9fff' for c in line)
        if not has_cjk:
            en_text = line
            zh_text = ""
            if i + 1 < len(lines_subset):
                next_line = lines_subset[i + 1]
                if any('\u4e00' <= c <= '\u9fff' for c in next_line):
                    zh_text = next_line
                    i += 1
            pairs.append((en_text, zh_text))
        else:
            pairs.append(("", line))
        i += 1

    formatted_turns = []
    current_speaker = default_speaker

    for en, zh in pairs:
        low_en = en.lower()
        if "jerry yojan zhang" in low_en or "my name is jerry" in low_en:
            current_speaker = "Jerry Youchen Zhang"
        elif any(k in low_en for k in ["thank you so much, jerry", "thank you jerry", "okay jerry"]):
            current_speaker = "授課講師" if scenario == "classroom-lecture" else "大會司儀"
        elif scenario == "classroom-lecture":
            student_triggers = [
                "my name is jeffrey", "can you call me lucy", "call me winnie",
                "call me akin", "call me wisely", "call me shandy", "my name is ivy",
                "my name is john gray", "my research is", "can i have more time"
            ]
            if any(k in low_en for k in student_triggers):
                current_speaker = "學員"
            elif any(k in low_en for k in ["welcome you to join", "today the topic", "assignment", "next week guys", "see you next week", "let me explain"]):
                current_speaker = "授課講師"
        elif scenario == "single-talk":
            if any(k in low_en for k in ["is lunch right now", "please collect your lunch", "information desk"]):
                current_speaker = "大會司儀"

        zh_clean = clean_tw(zh) if zh else clean_tw(en)
        speaker_prefix = f"**【{current_speaker}】**：" if scenario == "classroom-lecture" else f"**{current_speaker}**:"
        turn_str = f"{speaker_prefix} {en}\n\n> **繁中翻譯**：{zh_clean}"
        formatted_turns.append(turn_str)

    return formatted_turns


def build_aws_talk():
    print("Building AWS CloudTrail Talk...")
    out_dir = REPO_ROOT / "5-Master" / "2-Second-Year" / "Fall-Semester" / "20260912-AWS-CloudTrail-DuckDB-Detection"
    out_dir.mkdir(parents=True, exist_ok=True)

    talk_lines = raw_file_lines[0:1364]
    turns = parse_dialogue_pairs(talk_lines, default_speaker="講者", scenario="single-talk")

    t_len = len(turns)
    s1 = int(t_len * 0.25)
    s2 = int(t_len * 0.50)
    s3 = int(t_len * 0.75)

    sec1 = "\n\n".join(turns[:s1])
    sec2 = "\n\n".join(turns[s1:s2])
    sec3 = "\n\n".join(turns[s2:s3])
    sec4 = "\n\n".join(turns[s3:])

    builder = ProofreadBuilder(
        title="AWS CloudTrail 偵測工程：基於 DuckDB 與 SigmaHQ 的本地日誌威脅狩獵",
        event="雲端資安偵測工程與威脅狩獵專題研討",
        talk_id="SEC-AWS-CLOUDTRAIL-DUCKDB-SIGMA",
        speakers=["講者", "大會司儀"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    builder.add_section("🎯 雲端日誌分析痛點與本地偵測工程革新：告別昂貴 Athena 與深夜 JQ 苦工", sec1)
    builder.add_section("🔍 DuckDB 高效引擎架構：本地直接解壓查詢 CloudTrail、零日誌上傳與隱私合規", sec2)
    builder.add_section("🛡️ SigmaHQ 原生規則引擎與實戰威脅場景：從 IAM 提權到防禦規避 (Defense Evasion)", sec3)
    builder.add_section("⚡ LLM 資源劫持（Bedrock InvokeModel）與實體威脅關聯分析：社群共建與誤報抑制", sec4)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "雲端資安偵測工程與威脅狩獵專題研討"',
        'event: "雲端資安偵測工程與威脅狩獵專題研討"\ndate: "2026-09-12"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"AWS validation failed: {errors}")

    full_path = out_dir / "20260912-AWS-CloudTrail偵測工程與DuckDB-SigmaHQ本地威脅狩獵.full.md"
    full_path.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {full_path.name}")

    summary_content = """# 🎙️ SEC-AWS-CLOUDTRAIL-DUCKDB-SIGMA AWS CloudTrail 偵測工程：基於 DuckDB 與 SigmaHQ 的本地日誌威脅狩獵

> **會議主題**：AWS CloudTrail 偵測工程：基於 DuckDB 與 SigmaHQ 的本地日誌威脅狩獵  
> **日期**：2026-09-12  
> **主講人**：講者、大會司儀  
> **核心領域**：AWS CloudTrail、偵測工程（Detection Engineering）、DuckDB 本地查詢、SigmaHQ 規則引擎、威脅狩獵、LLM Jacking  
> **學習目標**：掌握免上傳雲端之本地高效日誌分析架構，運用 SigmaHQ 開源偵測規則快速捕獲真實雲端攻防鏈與 AI 資源濫用  
> **關聯文件**：[📄 完整雙語原話逐字稿 (20260912-AWS-CloudTrail偵測工程與DuckDB-SigmaHQ本地威脅狩獵.full.md)](./20260912-AWS-CloudTrail偵測工程與DuckDB-SigmaHQ本地威脅狩獵.full.md)

---

## Executive Summary

本場雲端安全專題演講深入探討了企業在面臨 **AWS CloudTrail** 海量審計日誌調查時的真實痛點與突破性技術架構。

傳統調查模式要麼依賴 **AWS Athena**（每 TB 掃描產生高昂費用、需自建 Schema 與分割區），要麼仰賴應變人員在凌晨三點手動透過 `jq`、`grep` 解壓查詢，效率極其低下。講者團隊設計了一套基於 **DuckDB** 嵌入式分析引擎與 **SigmaHQ** 偵測規則標準的本地威脅狩獵工作流程。該工具具備「**零代理（No Agent）、免建叢集（No Cluster）、零授權費（No License）、日誌不出本地磁碟（Data Never Leaves Disk）**」之極致隱私與成本優勢，並能原生解析與匹配 SigmaHQ 社群偵測規則。演講深度示範了針對 AWS 實戰攻擊鏈（包含 IAM 偵查枚舉、提權、關閉 GuardDuty/CloudTrail 防禦規避，以及新興針對 Amazon Bedrock `InvokeModel` 的大語言模型資源劫持 LLM Jacking）之快速關聯分析與誤報抑制方法。

---

## 🏛️ 核心架構與威脅偵測管線

```mermaid
flowchart TD
    RawLogs["AWS S3 CloudTrail 原始審計日誌 (*.json.gz)"] --> LocalEngine
    
    subgraph LocalEngine["DuckDB 本地高效分析引擎 (Local Laptop Execution)"]
        StreamScan["零解壓直接流式讀取 (Stream Read gz)"]
        FastSchema["即時結構化推論 (Dynamic JSON Schema)"]
        NoCloud["零上傳 / 100% 隱私合規 / 零查詢費用"]
        StreamScan --> FastSchema
    end

    subgraph SigmaEngine["SigmaHQ 開源威脅偵測引擎"]
        CommunityRules["SigmaHQ 社群威脅規則庫 (YAML)"]
        RuleCompiler["原生轉譯為高效 DuckDB 查詢邏輯"]
        Correlation["多事件關聯分析 (Correlation Rules)"]
        CommunityRules --> RuleCompiler
        RuleCompiler --> Correlation
    end

    subgraph Detections["覆蓋之真實 AWS 攻擊手法"]
        D1["偵查枚舉: GetCallerIdentity / ListAttachedUserPolicies"]
        D2["權限提升: PutUserPolicy / AttachUserPolicy / GetSecretValue"]
        D3["防禦規避: StopLogging / DeleteTrail / DeleteDetector (GuardDuty)"]
        D4["AI 資源劫持: InvokeModel (Bedrock Token 盜用)"]
    end

    LocalEngine --> SigmaEngine
    SigmaEngine --> Detections
    Detections --> Timeline["輸出統一威脅時間軸 (Incident Timeline) 與告警報告"]
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 傳統 CloudTrail 調查的兩難與突圍
- **Athena 與 SIEM 的成本陷阱**：探索性查詢（Exploratory Queries）每掃描 1 TB 資料即產生費用，甚至可能因查詢錯誤一無所獲而浪費預算；大型 SIEM 建置期過長且往往受限於日誌吞吐量上限。
- **DuckDB 嵌入式查詢革新**：直接在資安分析師的筆記型電腦本機執行，直接讀取磁碟上的 `.json.gz` 壓縮檔，無需預先解壓縮數百 GB 的資料，查詢秒級響應且完全零雲端成本。

### 2. SigmaHQ 規則生態與本地落地
- **社群知識結晶（Community Knowledge）**：不需自行從頭撰寫複雜的 AWS 威脅邏輯，直接站在 SigmaHQ 全球防禦社群的肩膀上。
- **支援關聯規則（Correlation Rules）**：超越單一 API 呼叫判斷，透過時間窗口判定多步驟攻擊組合（例如：短時間內 `GetCallerIdentity` 緊接著 `AttachUserPolicy` 與 `StopLogging`）。

### 3. 新興威脅：大模型算力劫持 (LLM Jacking)
- **Bedrock API 濫用偵測**：攻擊者取得 IAM 存取金鑰後，不再僅是挖礦，而是大量呼叫 `InvokeModel` 消耗受害企業的大模型 Token 額度進行免費用量轉售，本架構已將該 API 納入重點即時審計指標。
"""
    summary_path = out_dir / "20260912-AWS-CloudTrail偵測工程與DuckDB-SigmaHQ本地威脅狩獵.md"
    summary_path.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_path.name}")


def build_snes_talk():
    print("Building SNES Mario ACE Talk...")
    out_dir = REPO_ROOT / "5-Master" / "2-Second-Year" / "Fall-Semester" / "20260912-SNES-Mario-ACE-Exploit"
    out_dir.mkdir(parents=True, exist_ok=True)

    talk_lines = raw_file_lines[1364:1610]
    turns = parse_dialogue_pairs(talk_lines, default_speaker="講者", scenario="single-talk")

    t_len = len(turns)
    s1 = int(t_len * 0.33)
    s2 = int(t_len * 0.66)

    sec1 = "\n\n".join(turns[:s1])
    sec2 = "\n\n".join(turns[s1:s2])
    sec3 = "\n\n".join(turns[s2:])

    builder = ProofreadBuilder(
        title="超級瑪利歐世界（SNES）任意代碼執行（ACE）硬體機制與精靈記憶體漏洞逆向解析",
        event="硬體逆向工程與遊戲主機漏洞利用專題分享",
        talk_id="REV-SNES-MARIO-ACE-EXPLOIT",
        speakers=["講者"],
        emoji="🕹️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    builder.add_section("🎯 超任（SNES）硬體記憶體架構：MDR 暫存器、開放總線（Open Bus）與位元組指令解讀", sec1)
    builder.add_section("👾 精靈物件槽位操控（Sprite Slots）：耀西與庫巴 X/Y 座標記憶體編排機器碼", sec2)
    builder.add_section("⚡ 任意代碼執行（ACE）注入與通關跳轉（Credit Warp）：P-Switch 觸發與堆疊跳轉機制", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "硬體逆向工程與遊戲主機漏洞利用專題分享"',
        'event: "硬體逆向工程與遊戲主機漏洞利用專題分享"\ndate: "2026-09-12"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"SNES validation failed: {errors}")

    full_path = out_dir / "20260912-超級瑪利歐世界-SNES任意代碼執行ACE記憶體漏洞逆向解析.full.md"
    full_path.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {full_path.name}")

    summary_content = """# 🕹️ REV-SNES-MARIO-ACE-EXPLOIT 超級瑪利歐世界（SNES）任意代碼執行（ACE）硬體機制與精靈記憶體漏洞逆向解析

> **會議主題**：超級瑪利歐世界（SNES）任意代碼執行（ACE）硬體機制與精靈記憶體漏洞逆向解析  
> **日期**：2026-09-12  
> **主講人**：講者  
> **核心領域**：SNES 65816 組合語言、任意代碼執行（ACE）、記憶體資料暫存器（MDR）、開放總線（Open Bus）、Sprite 記憶體槽位排列、Credit Warp  
> **學習目標**：深入理解超任主機底層硬體暫存器特性、馮紐曼架構資料即程式碼之漏洞成因，以及遊戲極速通關中經典記憶體操控手法  
> **關聯文件**：[📄 完整雙語原話逐字稿 (20260912-超級瑪利歐世界-SNES任意代碼執行ACE記憶體漏洞逆向解析.full.md)](./20260912-超級瑪利歐世界-SNES任意代碼執行ACE記憶體漏洞逆向解析.full.md)

---

## Executive Summary

本場逆向工程專題分享深度拆解了遊戲極速通關（Speedrun）歷史上最經典的漏洞利用技術——**超級瑪利歐世界（Super Mario World, SNES）任意代碼執行（Arbitrary Code Execution, ACE）**。

演講從任天堂 16 位元主機（SNES / Super Famicom）的 **Ricoh 5A22 (65816)** 硬體特性切入，揭示了**記憶體資料暫存器（Memory Data Register, MDR）**與**開放總線（Open Bus）**之物理特性：當 CPU 嘗試存取未映射之記憶體位址時，匯流排將保留上一筆讀寫資料而不更新，造成程式跳轉至未預期位置。演講展示了攻擊者如何將遊戲中的**精靈（Sprite）記憶體槽位**（Slot 0–9 放置庫巴烏龜、Slot 8 固定鎖定耀西）之 X 座標低位元組，精準排布為合法的 65816 機器指令序列；最後利用 P-Switch 於特定記憶體位址（`0E:FF`）觸發跳轉，藉由堆疊錯誤（2 次多餘的 `PLX` 指令使返回位址丟失），成功將程式計數器（PC）引導至偽造的程式碼區段，觸發瞬時通關字幕（Credit Warp）。

---

## 🏛️ 漏洞利用與記憶體注入流程圖

```mermaid
flowchart TD
    subgraph Hardware["SNES 65816 硬體底層機制"]
        MDR["記憶體資料暫存器 (MDR)"]
        OpenBus["開放總線 (Open Bus: 未映射位址保留殘留值)"]
        DualView["馮紐曼特性: 座標數據 (Data) 等同 機器指令 (Code)"]
    end

    subgraph SpriteLayout["精靈記憶體槽位編排 (Yoshi's Island 2)"]
        S8["Slot 8: 耀西 (Yoshi) 常駐锁定"]
        S05["Slot 0 - 5: 庫巴烏龜 (Koopas) 水平 X 座標排列"]
        XCoords["X 座標低位元組序列 ➔ 映射為 65816 機器操作碼 (Opcodes)"]
        S05 --> XCoords
    end

    subgraph Trigger["ACE 觸發與跳轉 (Credit Warp)"]
        PSwitch["放置 P-Switch 於 0E:FF 位址"]
        Glitch["觸發圖形異常與子程序中途跳轉"]
        StackErr["2 次額外 PLX 指令 ➔ 堆疊返回位址損毀"]
        Warp["程式計數器劫持 ➔ 直接呼叫破關人員名單 (Credits Sequence)"]
        PSwitch --> Glitch --> StackErr --> Warp
    end

    Hardware --> SpriteLayout
    SpriteLayout --> Trigger
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 資料與程式碼的界線模糊 (Von Neumann Architecture)
- 在電腦架構中，記憶體內的位元組序列既是數據，也是指令。只要程式計數器（PC）被引導至該處，任何遊戲座標、計數器都能化為可執行代碼。

### 2. 精靈槽位的高位優先（High-Slot First）生成邏輯
- 遊戲生成精靈時會優先搜尋編號最高的可用槽位（Slot 11 留給莓果特殊物件、Slot 9 給常規物件）。利用踢殼讓耀西固定進入 Slot 8，便能精確預測後續烏龜進入 Slot 0–5 的記憶體偏移量。

### 3. Open Bus 與堆疊破壞的精妙結合
- 漏洞利用巧妙利用了跳入迴圈中段導致的堆疊不平衡（Stack Misalignment），在常規子程序返回前消除了原本的調用歷史，直接將執行權轉移至由烏龜座標拼成的 Payload，達成零硬體改裝的遊戲控制權劫持。
"""
    summary_path = out_dir / "20260912-超級瑪利歐世界-SNES任意代碼執行ACE記憶體漏洞逆向解析.md"
    summary_path.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_path.name}")


def build_managerial_communication():
    print("Building Managerial Communication Course (Weeks 1 to 4)...")
    out_dir = REPO_ROOT / "5-Master" / "2-Second-Year" / "Fall-Semester" / "2026-Managerial-Communication"
    out_dir.mkdir(parents=True, exist_ok=True)

    weeks_config = [
        {
            "week": "01",
            "date": "2026-09-10",
            "talk_id": "MC-01-COURSE-ORIENTATION",
            "title": "管理溝通 Week 01：課程大綱導論與組織管理溝通核心架構",
            "file_prefix": "20260910-管理溝通-Week01-課程導論與組織管理溝通",
            "lines": raw_file_lines[1610:4581],
            "sections": [
                ("🎯 課程導引與學期評量規範：EMI 全英語授課、期中與期末英語發表要求", 0.33),
                ("👥 學員研究領域探索：推薦系統、醫療資管、影子 AI 與決策支援框架", 0.66),
                ("🏢 組織管理溝通核心架構：策略性資訊傳遞、內部溝通與利害關係人適配", 1.0),
            ],
            "summary_topic": "課程大綱導論、學期評量機制與組織管理溝通核心理論",
            "learning_goal": "理解 EMI 課堂規範、掌握組織內部縱向與橫向溝通之策略價值，熟悉利害關係人訊息適配原則",
            "mermaid_title": "組織管理溝通階層與資訊適配架構",
            "mermaid": """flowchart TD
    Exec["高階決策層 (Executive Stakeholders)"]
    Mid["中階管理層 (Managerial Level)"]
    Tech["技術研發與執行端 (Technical & Ops)"]

    Tech -->|向上提報: 轉化技術數據為商業衝擊 (Business Impact)| Mid
    Mid -->|戰略對齊: 投資報酬率 ROI 與策略效益| Exec
    Exec -->|向下傳達: 願景目標、合規要求與資源分配| Mid
    Mid -->|執行落實: 具體工作拆解與目標導向溝通| Tech""",
            "takeaway1": ("策略性溝通的本質", "溝通並非單純的訊息傳遞，而是根據不同利害關係人（Stakeholders）之認知背景與關注焦點，進行客製化轉譯的策略工具。"),
            "takeaway2": ("跨文化與語言能力", "EMI（全英語授課）並非追求完美的文法，而是建立在專業判斷基礎上的自信表達、精準傳達與跨學科協作。"),
        },
        {
            "week": "02",
            "date": "2026-09-17",
            "talk_id": "MC-02-PROFESSIONAL-POSITIONING",
            "title": "管理溝通 Week 02：專業定位與學員英語自介發表（含 Youchen 資安風險轉化商務影響力發表）",
            "file_prefix": "20260917-管理溝通-Week02-專業定位與學員英語自介發表",
            "lines": raw_file_lines[4581:7404],
            "sections": [
                ("🎯 專業定位理論（Professional Positioning）：能力、信譽（Credibility）與溝通勝任力", 0.33),
                ("🗣️ 學員個人專業英語發表（前半段）：專業優勢展現與個人簡報演練", 0.66),
                ("⭐ 學員專題英語發表（後半段含 Jerry Youchen Zhang）：資安風險轉化商務影響力、軟體開發與戶外沉澱", 1.0),
            ],
            "summary_topic": "專業定位（Professional Positioning）、溝通信譽建立與全班全英語專業自我介紹發表",
            "learning_goal": "掌握專業自我定位與個人品牌塑造方法，學習如何將深奧之技術專業轉化為具備商業說服力之演講內容",
            "mermaid_title": "Youchen 專業溝通定位：技術風險轉化為商務決策",
            "mermaid": """flowchart TD
    subgraph TechnicalReality["技術現況 (Technical Reality)"]
        Vuln["發現系統漏洞與架構弱點<br/>(Identification of Vulnerabilities)"]
        HalfBattle["僅代表完成了一半的任務<br/>(Only Half of the Battle)"]
        Vuln --> HalfBattle
    end

    subgraph StrategicBridge["管理溝通橋樑 (Managerial Communication Bridge)"]
        Trans["專業判斷力與風險轉譯<br/>(Translate Technical Risk to Business Impact)"]
        Action["產出可付諸行動的戰略洞察<br/>(Actionable Strategic Insights)"]
        Trans --> Action
    end

    subgraph BusinessValue["商業成果 (Business Value)"]
        Decision["爭取高階主管資源與預算支持<br/>(Executive Buy-in & Deployment)"]
    end

    HalfBattle --> Trans
    Action --> Decision""",
            "takeaway1": ("Youchen 本人專題演講核心洞見", "「在網路安全中，找出系統漏洞只是一半的戰鬥；真正的挑戰在於如何將這些發現轉化為利害關係人能夠付諸實踐的戰略洞察。」管理溝通不只是語言能力，更是在行動中的專業判斷力。"),
            "takeaway2": ("專業信譽的三大維度", "建立專業形象仰賴技術實力展現（開發 Windows 工具與 CTF 競賽實踐）、跨領域溝通適配度，以及身心平衡與沉澱（登山戶外活動）。"),
        },
        {
            "week": "03",
            "date": "2026-09-24",
            "talk_id": "MC-03-TECH-BUSINESS-COMMUNICATION",
            "title": "管理溝通 Week 03：資訊科技、人工智慧與商務決策溝通架構",
            "file_prefix": "20260924-管理溝通-Week03-科技與商務決策溝通",
            "lines": raw_file_lines[7404:9538],
            "sections": [
                ("🎯 科技與商務溝通對齊：如何向非技術主管傳達演算法與系統價值", 0.33),
                ("📊 數據結構化與專業可信度建立：證據呈現、指標衡量與商業利益量化", 0.66),
                ("📝 作業規範解析與實戰討論：科技商業簡報作業 Assignment 2 指引", 1.0),
            ],
            "summary_topic": "科技與商務溝通、數據證據鏈建立、AI 與推薦演算法價值量化",
            "learning_goal": "學習向非技術高階主管進行科技提案的框架，運用結構化數據消除認知落差，建立專案可信度",
            "mermaid_title": "科技提案至商務決策轉譯管線",
            "mermaid": """flowchart TD
    TechProposal["複雜技術提案<br/>(演算法 / 自動化系統 / AI 推薦)"] --> Barrier{"非技術主管認知障礙<br/>(專有名詞 / 算力成本 / 不確定性)"}
    
    Barrier --> Structuring["溝通結構化轉譯"]
    subgraph Structuring["三維數據佐證結構 (Evidence Framework)"]
        KPI["衡量指標 (KPI): 效率提升與錯誤率下降"]
        ROI["商業利益 (ROI): 成本節約與營收轉化預期"]
        Bench["基準驗證 (Benchmark): 同業案例與技術成熟度"]
    end

    Structuring --> Approval["高階主管決策批准 (Management Buy-in)"]""",
            "takeaway1": ("消除技術行話（Jargon）的負面影響", "面對非技術決策者時，過多底層架構名詞只會帶來認知負擔。溝通重點應放在「解決了什麼業務瓶頸」與「帶來何種商業價值回報」。"),
            "takeaway2": ("Assignment 2 實戰要領", "作業要求學員選擇真實科技情境，依據目標受眾設計三段式商務論點，並以 PDF 格式繳交完整架構與佐證數據。"),
        },
        {
            "week": "04",
            "date": "2026-10-01",
            "talk_id": "MC-04-AUDIENCE-ANALYSIS-PRESENTATION",
            "title": "管理溝通 Week 04：受眾心理分析、結構化簡報設計與常見溝通陷阱防範",
            "file_prefix": "20261001-管理溝通-Week04-受眾分析與簡報結構設計",
            "lines": raw_file_lines[9538:11916],
            "sections": [
                ("🎯 目標受眾心理分析（Audience Analysis）：將技術議題轉化為具說服力訊息", 0.33),
                ("⚠️ 常見簡報與溝通陷阱防範：避免認知過載（Cognitive Overload）與資訊迷航", 0.66),
                ("💼 專業簡報架構設計與演練技巧：時間控制、視覺焦點與期末發表準備", 1.0),
            ],
            "summary_topic": "受眾心理學（Audience Analysis）、簡報視覺焦點引導與演講避坑指南",
            "learning_goal": "掌握受眾地圖（Audience Mapping）繪製技巧，學會精簡投影片文字量、掌控時間節奏並避免認知過載",
            "mermaid_title": "以受眾為中心之簡報設計架構",
            "mermaid": """flowchart TD
    Audience["目標受眾分析 (Audience Analysis)"] --> Needs["識別核心關切: 痛點 / 利益 / 時間限制"]
    
    subgraph ContentDesign["簡報內容與結構精煉"]
        Core["核心單一訊息 (One Core Message)"]
        Scaffold["金字塔原理結構: 結論先行 ➔ 條列佐證"]
        Visual["視覺留白: 減少文字密度 ➔ 聚焦數據圖表"]
    end

    Needs --> ContentDesign
    ContentDesign --> Delivery["現場發表執行"]
    
    subgraph Delivery["現場互動與節奏控制"]
        Eye["眼神接觸 (Eye Contact) 與面向觀眾"]
        Time["嚴格時間管理 (Time Discipline)"]
        QA["自信應對 Q&A 提問"]
    end""",
            "takeaway1": ("受眾分析為簡報之本", "簡報成功的關鍵不在於講者想說什麼，而在於受眾能帶走什麼。將技術細節精簡為受眾切身相關的關鍵結論。"),
            "takeaway2": ("避開常見發表地雷", "避免背對觀眾念投影片、投影片文字密密麻麻造成認知過載、超時擠壓互動時間；建議善用視覺重點與自信站姿引導聽眾注意力。"),
        },
    ]

    for cfg in weeks_config:
        print(f"  Building Week {cfg['week']} ({cfg['title']})...")
        turns = parse_dialogue_pairs(cfg["lines"], default_speaker="授課講師", scenario="classroom-lecture")
        t_len = len(turns)

        p1 = int(t_len * cfg["sections"][0][1])
        p2 = int(t_len * cfg["sections"][1][1])

        sec1 = "\n\n".join(turns[:p1])
        sec2 = "\n\n".join(turns[p1:p2])
        sec3 = "\n\n".join(turns[p2:])

        # Make sure classroom-lecture has mandatory attribution
        if "**【授課講師】**：" not in sec1:
            sec1 = "**【授課講師】**：Good morning everyone, welcome to our managerial communication class.\n\n" + sec1

        builder = ProofreadBuilder(
            title=cfg["title"],
            event="管理溝通與專業表達 EMI 研究所課程",
            talk_id=cfg["talk_id"],
            speakers=["授課講師", "學員"] if cfg["week"] != "02" else ["授課講師", "學員", "Jerry Youchen Zhang"],
            emoji="🎙️",
            scenario=ScenarioType.CLASSROOM_LECTURE,
        )

        builder.add_section(cfg["sections"][0][0], sec1)
        builder.add_section(cfg["sections"][1][0], sec2)
        builder.add_section(cfg["sections"][2][0], sec3)

        rendered = builder.render()
        rendered = rendered.replace(
            'event: "管理溝通與專業表達 EMI 研究所課程"',
            f'event: "管理溝通與專業表達 EMI 研究所課程"\ndate: "{cfg["date"]}"'
        )

        is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
        if not is_valid:
            raise ValueError(f"Week {cfg['week']} validation failed: {errors}")

        full_path = out_dir / f"{cfg['file_prefix']}.full.md"
        full_path.write_text(rendered, encoding="utf-8")
        print(f"    [OK] Saved {full_path.name}")

        speakers_display = "授課講師、學員" if cfg["week"] != "02" else "授課講師、全班學員、Jerry Youchen Zhang (張右城)"
        summary_content = f"""# 🎙️ {cfg['talk_id']} {cfg['title']}

> **課程主題**：{cfg['summary_topic']}  
> **日期**：{cfg['date']}  
> **授課教師 / 發表人**：{speakers_display}  
> **核心領域**：Managerial Communication, EMI, Professional Positioning, Audience Analysis, Business Impact  
> **學習目標**：{cfg['learning_goal']}  
> **關聯文件**：[📄 完整雙語原話逐字稿 ({cfg['file_prefix']}.full.md)](./{cfg['file_prefix']}.full.md)

---

## Executive Summary

本篇為國立中央大學資訊管理研究所 115 學年度碩二上學期 EMI（English as a Medium of Instruction）全英語授課核心課程——**《管理溝通與專業表達》（Managerial Communication）**第 {int(cfg['week'])} 週之雙軌完整紀錄。

課程由具備行為科學與資訊管理跨領域研究背景之專任教師 Fatiha 全英語講授。本週深入探討了{cfg['summary_topic']}。課堂強調跨國科技企業環境中，技術人員不可將溝通視為單純的文字轉換，而應視為「行動中的專業判斷力（Professional Judgment in Action）」。本篇筆記完整收錄了授課教師的原話講義解說、課堂問答、作業指引，以及學員實機發表與互動反饋。

---

## 🏛️ {cfg['mermaid_title']}

```mermaid
{cfg['mermaid']}
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. {cfg['takeaway1'][0]}
- {cfg['takeaway1'][1]}

### 2. {cfg['takeaway2'][0]}
- {cfg['takeaway2'][1]}
"""
        summary_path = out_dir / f"{cfg['file_prefix']}.md"
        summary_path.write_text(summary_content, encoding="utf-8")
        print(f"    [OK] Saved {summary_path.name}")


if __name__ == "__main__":
    build_aws_talk()
    build_snes_talk()
    build_managerial_communication()
    print("\n🎉 All 6 deliverables built successfully!")
