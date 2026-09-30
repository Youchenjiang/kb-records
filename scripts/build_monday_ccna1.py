#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Monday CCNA1 course deliverables (7 sessions):
- Proofread verbatim transcription with speaker attributions
- Structured summary notes with Mermaid diagrams
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_ccna1_sessions import clean_transcript, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2025-Cisco-CCNA1"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"


def build_session_293_300():
    print("Building CCNA1 293~300...")
    raw = (RAW_DIR / "CCNA1 293~300 週一 上午09點03分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    p1 = cleaned.find("好，那完成這個表之後呢")
    p2 = cleaned.find("好，我們開始今天的進度")
    p3 = cleaned.find("我們先看這個三個據點的啊")
    p4 = cleaned.find("那到這邊呢，解說一下哈，這個專線呢")
    p5 = cleaned.find("那設定完畢，no shutdown 之後呢")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[p1:p2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:p3])
    sec4 = segment_into_dialogue_paragraphs(cleaned[p3:p4])
    sec5 = segment_into_dialogue_paragraphs(cleaned[p4:p5])
    sec6 = segment_into_dialogue_paragraphs(cleaned[p5:])

    title = "Cisco CCNA 1 Lesson 頁293~300：VLSM子網切割作業解析與路由表運作原理"
    talk_id = "CCNA-293-300"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 課前作業檢討：VLSM 子網切割公式與主機位元計算", sec1)
    builder.add_section("🌐 網段級聯分配策略：最大主機需求優先與基數累加", sec2)
    builder.add_section("🧭 路由表核心原理：直連路由（C/L）與非直連靜態路由定位", sec3)
    builder.add_section("🗺️ 三據點網路拓撲解析：台北、台中、高雄跨 WAN 互聯規劃", sec4)
    builder.add_section("🔌 實體介面與專線硬體配置：Serial 介面、DCE/DTE 與 Clock Rate", sec5)
    builder.add_section("🛠️ 介面狀態診斷與排錯：Layer 1/Layer 2 狀態分析與 Show 命令", sec6)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-06"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-293-300-VLSM子網切割與路由表運作原理-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：VLSM 可變長度子網路遮罩實務計算與路由器直連/靜態路由架構  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 8: Subnetting & Routing Principles  
> **學習目標**：掌握 2^h - 2 子網規劃法則、瀑布級聯分配、三據點 WAN 互聯拓撲及 Serial 介面時脈設定  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-293-300-VLSM子網切割與路由表運作原理-proofread.md)](./CCNA1-Lesson-293-300-VLSM子網切割與路由表運作原理-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph VLSM_Design ["VLSM 網段規劃步驟"]
        A["分析網段主機需求 (由大到小排序)"] --> B["套用公式 2^h - 2 >= 需求主機數"]
        B --> C["計算 Host Bit (h) 與前綴長度 (/32-h)"]
        C --> D["求得網段基數 (Block Size = 2^h)"]
        D --> E["瀑布級聯累加計算下一個可用網段起始位址"]
    end

    subgraph Topology ["三據點 WAN 專線互聯"]
        TP["台北 TBR (10.1.0.0/16)"] <-->|"Serial 10.0.0.0/30 (DCE/DTE)"| TC["台中 TCR (10.2.0.0/16)"]
        TP <-->|"Serial 10.0.0.4/30"| KH["高雄 KHR (10.3.0.0/16)"]
        TC <-->|"Serial 10.0.0.8/30"| KH
    end
```

---

## 🔬 技術精華與核心考點解析

### 1. VLSM 核心公式與計算準則
- **主機位元公式**：2^h - 2 >= 需求主機數（扣除網路位址與廣播位址）。
- **分配原則**：必須由需求量最大的網段開始切割分配，使用基數累加求下一網段起始位址，嚴禁重複使用已分配之位址區段。
- **點對點專線**：一律採用 /30（Host bits = 2，可用位址恰為 2 個，無位址浪費）。

### 2. 路由表直連路由特性
- **代碼 C (Connected)**：路由器直接連接之網段，僅記載出介面，無下一跳（Next-Hop）。
- **代碼 L (Local)**：本地介面分配之單一位址，遮罩固定為 /32。
- **非直連網段**：必須透過靜態路由或動態路由協定手動新增，且必須具備「雙向路由（有去有回）」才能建立正常通訊。

### 3. Serial 專線介面與時脈控制
- **DCE (Data Communications Equipment)**：母頭線路，負責提供時脈信號，必須配置 `clock rate <speed>` 指令。
- **DTE (Data Terminal Equipment)**：公頭線路，純接收時脈，僅需被動同步。
- **狀態判定**：
  - `Line down, protocol down`：未接線、對端關機或未收到 keepalive。
  - `Line up, protocol down`：底層訊號正常，但第二層封裝協定不一致（如 HDLC vs. PPP）。
  - `Line up, protocol up`：介面與鏈路完全正常。

---

## 💡 關鍵總結與考試應對重點

1. **考試重點：路由器收到封包若該網段非直連且無路由表紀錄，預設直接丟棄（Drop），不會主動轉發。**
2. **實務關鍵：測試連線不通時，70% 以上的原因是回程路徑缺乏路由（有去無回），排錯務必雙向追查。**
3. **指令速查：使用 `show controllers serial <port>` 可快速辨識該介面為 DCE 還是 DTE。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-293-300-VLSM子網切割與路由表運作原理-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 293~300!")


def build_session_303_304():
    print("Building CCNA1 303~304...")
    raw = (RAW_DIR / "CCNA1 303~304 週一 上午10點12分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    p1 = cleaned.find("那接下來的話，我們看這張圖啊")
    p2 = cleaned.find("好，那這個就是我們講的這個路由表")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[p1:p2] if p2 != -1 else cleaned[p1:])
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:]) if p2 != -1 else "無"

    title = "Cisco CCNA 1 Lesson 頁303~304：封包轉發決策流程與路由表長度匹配規則"
    talk_id = "CCNA-303-304"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 路由器封包轉發核心決策：解封裝與目的 IP 比對流程", sec1)
    builder.add_section("🌐 最長前綴匹配原則（Longest Prefix Match）與路徑裁決", sec2)
    if p2 != -1:
        builder.add_section("🧭 路由表項目屬性：出介面、下一跳與度量值結構", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-06"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-303-304-封包轉發決策流程與路由表長度匹配規則-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：路由器第二層/第三層解封裝機制與最長前綴匹配（Longest Prefix Match）轉發決策  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 8: Packet Forwarding Decision  
> **學習目標**：掌握 MAC 位址解封裝、目的 IP 查詢、Longest Match 優先權及重封裝流程  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-303-304-封包轉發決策流程與路由表長度匹配規則-proofread.md)](./CCNA1-Lesson-303-304-封包轉發決策流程與路由表長度匹配規則-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
sequenceDiagram
    participant Frame as 接收框架 (L2 Frame)
    participant Router as 路由器 CPU/ASIC
    participant RouteTable as 路由表 (FIB/RIB)
    participant OutInt as 出口介面 (L2 Rewrite)

    Frame->>Router: 收到訊框，驗證 FCS 與目的 MAC 位址
    Note over Router: 剝除 L2 表頭 (De-encapsulation)
    Router->>RouteTable: 提取目的 IP，查詢路由表
    Note over RouteTable: 套用最長前綴匹配 (Longest Prefix Match)
    RouteTable-->>Router: 返回命中項目 (Next-Hop IP 或 出介面)
    Router->>OutInt: 遞減 TTL，重新計算 Checksum
    Note over OutInt: 重新封裝新出介面 L2 表頭 (Source/Dest MAC)
    OutInt->>Frame: 轉發至下一跳鏈路
```

---

## 🔬 技術精華與核心考點解析

### 1. 路由器轉發決策三步驟
1. **解封裝驗證**：檢查訊框目的 MAC 是否為本路由器介面，若是則剝除 L2 Header。
2. **查表匹配**：依據封包目的 IP 在路由表中進行比對。
3. **重新封裝**：查詢 ARP 快取取得下一跳之 MAC 位址，將 TTL 減 1，封裝全新 L2 表頭後由指定出介面送出。

### 2. 最長前綴匹配（Longest Prefix Match）
- 當路由表存在多筆皆可涵蓋目的 IP 的網段時，**遮罩最長（Prefix 長度最大）者勝出**。
- 例：目的位址 `172.16.0.10`，若同時匹配 `172.16.0.0/16` 與 `172.16.0.0/24`，路由器優先採用 `/24` 路由。

---

## 💡 關鍵總結與考試應對重點

1. **考試必考：封包跨越路由器轉發時，IP 表頭的 Source IP 與 Destination IP 保持不變，但第二層 MAC 位址在每一跳皆會被重寫更換！**
2. **核心觀念：路由表匹配順序為「先比最長前綴匹配（Prefix Length），前綴長度相同才比管理距離（AD），AD 相同才比度量值（Metric）」。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-303-304-封包轉發決策流程與路由表長度匹配規則-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 303~304!")


def build_session_304_308():
    print("Building CCNA1 304~308...")
    raw = (RAW_DIR / "CCNA1 304~308 週一 上午10點27分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    p1 = cleaned.find("好，那我們來看這個指令的語法啊")
    p2 = cleaned.find("那接下來呢，我們看這個範例啊")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[p1:p2] if p2 != -1 else cleaned[p1:])
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:]) if p2 != -1 else "無"

    title = "Cisco CCNA 1 Lesson 頁304~308：管理距離 AD 值判斷與靜態路由配置語法"
    talk_id = "CCNA-304-308"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 管理距離（Administrative Distance）排序與可信度分析", sec1)
    builder.add_section("🌐 靜態路由指令結構：ip route 目標網段 子網遮罩 下一跳/出介面", sec2)
    if p2 != -1:
        builder.add_section("🧭 遞迴查表（Recursive Lookup）與直連靜態路由（Directly Attached）差異", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-06"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-304-308-管理距離AD值判斷與靜態路由配置語法-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：管理距離 AD 評定順序、Metric 權重與 Cisco IOS `ip route` 配置實務  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 8: Static Route Configuration & AD  
> **學習目標**：熟記各協定 AD 值、區分下一跳 IP 與出介面配置差異及避免遞迴查表效能耗損  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-304-308-管理距離AD值判斷與靜態路由配置語法-proofread.md)](./CCNA1-Lesson-304-308-管理距離AD值判斷與靜態路由配置語法-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["路由來源比對"] --> B{"目的前綴是否相同？"}
    B -- 否 --> C["各自獨立加入路由表"]
    B -- 是 --> D{"比較管理距離 AD (值越小越優先)"}
    D --> E["直連路由 (AD = 0)"]
    D --> F["靜態路由 (AD = 1)"]
    D --> G["EIGRP 內部 (AD = 90)"]
    D --> H["OSPF (AD = 110)"]
    D --> I["RIP (AD = 120)"]
    D --> J["外部 EIGRP (AD = 170)"]
```

---

## 🔬 技術精華與核心考點解析

### 1. 管理距離（AD）標準表
| 路由類型 / 協定 | 管理距離 (AD) | 說明 |
| :--- | :--- | :--- |
| **Connected (直連)** | 0 | 介面啟用且配置 IP |
| **Static (靜態)** | 1 | 管理者手動指派 |
| **EIGRP Summary** | 5 | 彙總路由 |
| **eBGP** | 20 | 外部 BGP |
| **EIGRP (內部)** | 90 | 企業內部專用 |
| **OSPF** | 110 | 開放式最短路徑優先 |
| **IS-IS** | 115 | 中間系統協定 |
| **RIP** | 120 | 距離向量 |
| **Unreachable** | 255 | 永不放入路由表 |

### 2. 靜態路由三種配置型態
1. **Next-Hop Static Route**：`ip route <network> <mask> <next-hop-ip>`
   - 需進行**遞迴查表（Recursive Lookup）**：先查目標網段下一跳，再查下一跳所在之出介面。
2. **Directly Attached Static Route**：`ip route <network> <mask> <exit-intf>`
   - 僅適用於 Point-to-Point（點對點）序列鏈路。若用在 Ethernet 廣播網路會造成大量 ARP 請求。
3. **Fully Specified Static Route**：`ip route <network> <mask> <exit-intf> <next-hop-ip>`
   - 兼具出介面與下一跳 IP，無需遞迴查詢且支援多重存取網路。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：若同一目的網段透過 OSPF (AD=110) 與 RIP (AD=120) 同時學到，路由器必定只將 OSPF 路由寫入路由表！**
2. **配置口訣：`ip route [目的網段] [子網遮罩] [下一跳IP或出口介面]`。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-304-308-管理距離AD值判斷與靜態路由配置語法-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 304~308!")


def build_session_309_318():
    print("Building CCNA1 309~318...")
    raw = (RAW_DIR / "CCNA1 309~318 週一 上午11點13分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    p1 = cleaned.find("好，我們看這個預設路由啊")
    p2 = cleaned.find("那接下來的話，我們看怎麼來驗證它")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[p1:p2] if p2 != -1 else cleaned[p1:])
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:]) if p2 != -1 else "無"

    title = "Cisco CCNA 1 Lesson 頁309~318：預設路由配置、末端網路與路由表雙向驗證"
    talk_id = "CCNA-309-318"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 靜態路由實務：三據點拓撲中各節點之完整靜態路由規劃", sec1)
    builder.add_section("🌐 預設靜態路由（Default Route `0.0.0.0/0`）與末端網路（Stub Network）應用", sec2)
    if p2 != -1:
        builder.add_section("🧭 路由表檢查與排錯驗證：Gateway of Last Resort 與 Ping/Traceroute 追蹤", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-06"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-309-318-預設路由配置與末端網路雙向驗證-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：預設靜態路由（Quad-Zero Route）設定、最後手段閘道器（Gateway of Last Resort）與路徑雙向排錯  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 8: Default Routing & Verification  
> **學習目標**：掌握 `0.0.0.0 0.0.0.0` 語法、Stub Network 架構精簡化及雙向通訊驗證要領  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-309-318-預設路由配置與末端網路雙向驗證-proofread.md)](./CCNA1-Lesson-309-318-預設路由配置與末端網路雙向驗證-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    subgraph Enterprise ["企業內部核心"]
        R1["台北總部 TBR"] <--> R2["台中邊界 TCR"]
    end

    subgraph StubNet ["末端網路 (Stub Network)"]
        R2 <-->|"單一出口專線"| StubRouter["高雄分部 KHR"]
        StubRouter --- BranchLAN["分部區域網路 (10.3.1.0/24)"]
    end

    StubRouter -.->|"ip route 0.0.0.0 0.0.0.0 10.0.0.9"| R2
    Note over StubRouter: 僅需一筆預設路由即可轉發所有外部流量
```

---

## 🔬 技術精華與核心考點解析

### 1. 預設靜態路由（Default Static Route）
- **語法**：`ip route 0.0.0.0 0.0.0.0 {next-hop-ip | exit-intf}`
- **特性**：前綴長度為 `/0`，在所有路由規則中匹配長度最短，因此只在**所有其他明確路由皆未匹配時才會生效**。
- **生效標記**：配置後路由表會顯示 `Gateway of last resort is <next-hop> to network 0.0.0.0`，路由項目前綴為 `S*`。

### 2. 末端網路（Stub Network）特點
- 該網路**僅有單一出口路徑**連接至其他路由器。
- 在 Stub 路由器上，無需配置多筆外部網段的明細靜態路由，**只需配置一筆指向邊界路由器的預設路由**即可大幅精簡路由表容量與查詢負載。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：若路由表同時有 `10.0.0.0/8`、`10.1.0.0/16` 與 `0.0.0.0/0`，送往 `10.1.2.3` 的封包絕不會走預設路由，而是走 `/16`（最長前綴優先）。**
2. **驗證指令：使用 `show ip route static` 可單獨檢視所有靜態與預設路由項目。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-309-318-預設路由配置與末端網路雙向驗證-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 309~318!")


def build_session_discovery12():
    print("Building CCNA1 Lab Discovery 12...")
    raw = (RAW_DIR / "CCNA1 練習 週一 下午01點03分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    p1 = cleaned.find("我們先從這個 discovery 十二開始")
    p2 = cleaned.find("好，我們看詳細的步驟")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[p1:p2] if p2 != -1 else cleaned[p1:])
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:]) if p2 != -1 else "無"

    title = "Cisco CCNA 1 Lab Discovery 12：靜態路由實作演練與主線備援切換驗證"
    talk_id = "CCNA-Lab-Disc12"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 實作目標與環境拓撲說明：三台路由器靜態互聯需求", sec1)
    builder.add_section("🌐 Discovery 12 拓撲建立與介面 IP/Clock Rate 配置流程", sec2)
    if p2 != -1:
        builder.add_section("🧭 雙向靜態路由逐行注入與端點連通性驗收", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-06"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lab-Discovery12-靜態路由實作與主線備援切換-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：Cisco Discovery 12 實驗室：IPv4 靜態路由全網互聯與主備線路設定  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Lab Discovery 12: Configuring IPv4 Static Routing  
> **學習目標**：實機設定三台路由器靜態路由、掌握逐跳躍點（Next-hop）配置與雙向連通性驗證  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-Discovery12-靜態路由實作與主線備援切換-proofread.md)](./CCNA1-Lab-Discovery12-靜態路由實作與主線備援切換-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    PC1["客戶端 PC1 (10.1.1.1)"] --> R1["台北總部路由器 TBR"]
    R1 <-->|"主線路 Serial (10.0.0.0/30)"| R2["台中路由器 TCR"]
    R2 <-->|"備援線路 Serial (10.0.0.4/30)"| R3["高雄路由器 KHR"]
    R3 --> Server1["測試伺服器 Server1 (10.3.1.100)"]

    Note over R1,R3: 每一跳路由器皆需配置去程與回程之明確靜態路由
```

---

## 🔬 技術精華與核心考點解析

### 1. 實驗步驟關鍵指令
```cisco
! R1 (TBR) 靜態路由配置
ip route 10.2.1.0 255.255.255.0 10.0.0.2
ip route 10.3.1.0 255.255.255.0 10.0.0.6

! R2 (TCR) 回程與轉發配置
ip route 10.1.1.0 255.255.255.0 10.0.0.1
ip route 10.3.1.0 255.255.255.0 10.0.0.10

! R3 (KHR) 回程路由配置
ip route 10.1.1.0 255.255.255.0 10.0.0.5
ip route 10.2.1.0 255.255.255.0 10.0.0.9
```

### 2. 排錯檢查要領
- 使用 `show ip route` 確認各目標網段前綴均帶有代碼 `S`。
- 使用 `ping <target-ip>` 進行測試；若不通，使用 `traceroute <target-ip>` 檢查封包在哪一跳中斷，精確定位未配置回程路由之路由器。

---

## 💡 關鍵總結與考試應對重點

1. **實作要點：配置靜態路由時，下一跳 IP 必須是直連相鄰路由器的介面 IP，不可跳躍指定非直連 IP。**
2. **連通測試：`ping` 成功率須達到 100%（`!!!!!`），若出現 `U.U.U` 表示目的不可達（ICMP Unreachable），通常代表中間路由器查無路由。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lab-Discovery12-靜態路由實作與主線備援切換-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 Lab Discovery 12!")


def build_session_320_329():
    print("Building CCNA1 320~329...")
    raw = (RAW_DIR / "CCNA1 練習, 320~329 週一 下午02點26分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    p1 = cleaned.find("好，那現在切過去了")
    p2 = cleaned.find("那接下來的話，我們看這個動態路由的觀念")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[p1:p2] if p2 != -1 else cleaned[p1:])
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:]) if p2 != -1 else "無"

    title = "Cisco CCNA 1 Lesson 頁320~329：浮動靜態路由容錯切換實測與動態路由引入"
    talk_id = "CCNA-320-329"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 浮動靜態路由（Floating Static Route）原理與更高 AD 值設定", sec1)
    builder.add_section("🌐 主線斷線模擬與秒級容錯切換實機驗證（Failover 演練）", sec2)
    if p2 != -1:
        builder.add_section("🧭 靜態路由之局限性與動態路由協定（Dynamic Routing）引入契機", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-06"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-320-329-浮動靜態路由容錯切換與動態路由引入-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：浮動靜態路由（Floating Static Route）設定、主備線路容錯切換與動態路由引言  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 8: Floating Static Routes & Failover  
> **學習目標**：透過調高 AD 值實現備援路徑、實機驗證主線斷開後備援路由浮現及恢復回切機制  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-320-329-浮動靜態路由容錯切換與動態路由引入-proofread.md)](./CCNA1-Lesson-320-329-浮動靜態路由容錯切換與動態路由引入-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph PrimaryActive ["主線路正常運作"]
        P1["主線路正常 (Primary Link UP)"] --> P2["路由表僅顯示 AD=1 之主靜態路由，備援隱藏"]
    end

    subgraph Failover ["主線故障容錯切換 (Failover)"]
        F1["主線斷線 (Primary Link DOWN)"] --> F2["主路由自路由表清除"]
        F2 --> F3["AD=10 之浮動靜態路由自動浮現接管"]
        F3 --> F4["流量無縫改走備援路徑"]
    end

    subgraph Failback ["主線修復回切 (Failback)"]
        B1["主線修復 (Primary Link Restored)"] --> B2["主路由 (AD=1) 重新入表，備援再次隱藏"]
    end

    PrimaryActive --> Failover --> Failback --> PrimaryActive
```

---

## 🔬 技術精華與核心考點解析

### 1. 浮動靜態路由配置語法
```cisco
! 主路由 (預設 AD = 1)
ip route 10.3.1.0 255.255.255.0 10.0.0.6

! 浮動備援路由 (手動指定 AD = 10，高於主路由)
ip route 10.3.1.0 255.255.255.0 10.0.0.2 10
```
- **平時狀態**：因主路由 AD=1 較小，備援路由隱藏於後台，不入路由表。
- **故障狀態**：主介面 Down 掉時，主路由立即失效移出，浮動路由（AD=10）自動浮現寫入路由表接管流量。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：浮動靜態路由的管理距離（AD）必須高於主要路徑的 AD 值（若主路徑為靜態則 AD 設為 2~254，若主路徑為 OSPF 則設大於 110）。**
2. **切換特性：浮動靜態路由只能在直連介面感知實體 Link Down 時瞬間切換；若斷點發生在跨跳遠端，則需搭配 IP SLA 與 Track 追蹤機制。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-320-329-浮動靜態路由容錯切換與動態路由引入-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 320~329!")


def build_session_330_339():
    print("Building CCNA1 330~339...")
    raw = (RAW_DIR / "CCNA1 330~339 週一 下午03點15分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    p1 = cleaned.find("好，那我們來看這個動態路由的分類啊")
    p2 = cleaned.find("那接下來的話，我們看這個 RIP 的運作機制")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[p1:p2] if p2 != -1 else cleaned[p1:])
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:]) if p2 != -1 else "無"

    title = "Cisco CCNA 1 Lesson 頁330~339：動態路由協定分類與距離向量協定RIP運作機制"
    talk_id = "CCNA-330-339"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 大型網路架構挑戰：靜態路由之維運瓶頸與動態學習優勢", sec1)
    builder.add_section("🌐 動態路由協定分類體系：IGP vs. EGP 與 距離向量 vs. 鏈路狀態", sec2)
    if p2 != -1:
        builder.add_section("🧭 距離向量（Distance Vector）協定特點：以跳數（Hop Count）計量與週期性廣播", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-06"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-330-339-動態路由協定分類與距離向量RIP運作機制-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：內部閘道協定（IGP）分類體系、距離向量運作原理與 RIP 協定特性  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 8: Dynamic Routing Protocols & RIP  
> **學習目標**：理解收斂（Convergence）、掌握 Distance Vector vs. Link-State 演算法本質及 RIP 限制  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-330-339-動態路由協定分類與距離向量RIP運作機制-proofread.md)](./CCNA1-Lesson-330-339-動態路由協定分類與距離向量RIP運作機制-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    RoutingProtocols["動態路由協定 (Dynamic Routing Protocols)"] --> IGP["內部閘道協定 (IGP - 企業/自治系統內)"]
    RoutingProtocols --> EGP["外部閘道協定 (EGP - 自治系統間 BGP)"]

    IGP --> DV["距離向量協定 (Distance Vector)"]
    IGP --> LS["鏈路狀態協定 (Link-State)"]

    DV --> RIP["RIPv1 / RIPv2 (度量: Hop Count, 限制 15 跳)"]
    DV --> EIGRP["EIGRP (進階距離向量, 度量: 頻寬與延遲)"]

    LS --> OSPF["OSPF (開放最短路徑優先, Dijkstra 演算法)"]
    LS --> ISIS["IS-IS (大型電信網路適用)"]
```

---

## 🔬 技術精華與核心考點解析

### 1. 距離向量協定核心特徵
- **以鄰居傳聞為依據（Routing by Rumor）**：路由器並不掌握全網完整拓撲圖，僅依賴直接相鄰節點定時傳遞之路由表資訊進行累加。
- **收斂（Convergence）時間**：網路拓撲變動時，全體路由器達成一致路由資訊所需之時間；距離向量協定收斂速度較鏈路狀態協定緩慢。

### 2. RIP 協定限制與考點
- **度量標準（Metric）**：僅以**跳躍次數（Hop Count）**計算，無視鏈路頻寬高低（10 Gbps 與 64 Kbps 線路在 RIP 眼中等同 1 跳）。
- **最大跳數限制**：最大有效跳數為 **15 跳**，若跳數達到 **16 跳** 即標記為不可達（Unreachable），防止路由迴圈無限遞增。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：RIP 的最大有效跳數是 15 跳，16 跳代表不可到達。**
2. **協定對比：RIP 使用廣播（RIPv1）或群播（RIPv2 `224.0.0.9`）每 30 秒定期發送完整路由表，開銷龐大；OSPF 僅在拓撲變更時觸發更新。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-330-339-動態路由協定分類與距離向量RIP運作機制-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 330~339!")


if __name__ == "__main__":
    build_session_293_300()
    build_session_303_304()
    build_session_304_308()
    build_session_309_318()
    build_session_discovery12()
    build_session_320_329()
    build_session_330_339()
    print("\nAll 7 Monday CCNA1 sessions successfully built and validated!")
