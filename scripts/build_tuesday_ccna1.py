#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Tuesday CCNA1 course deliverables (3 sessions):
- CCNA1 340~347: OSPF Fundamentals & Link-State Routing
- CCNA1 348~353: OSPF Multi-Area & Backbone Area 0 Architecture
- CCNA1 354~364: OSPF Single-Area Configuration & Router ID Election
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


def clean_ospf_transcript(text: str) -> str:
    """Specialized cleaning for OSPF technical vocabulary."""
    base = clean_transcript(text)
    replacements = [
        (r"OSB", "OSPF"),
        (r"Ruby", "RIP"),
        (r"area\s*零", "Area 0"),
        (r"area\s*一", "Area 1"),
        (r"area\s*二", "Area 2"),
        (r"backbone\s*router", "Backbone Router（骨幹路由器）"),
        (r"inter\s*router", "Internal Router（內部路由器）"),
        (r"hop\s*count", "Hop Count（跳數）"),
    ]
    res = base
    for pat, rep in replacements:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def build_session_340_347():
    print("Building CCNA1 340~347...")
    raw = (RAW_DIR / "CCNA1 340~347 週二 上午09點06分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_ospf_transcript(raw)

    p1 = cleaned.find("好，那現在我們看這個鏈路狀態")
    p2 = cleaned.find("那接下來呢，我們看這個 OSPF 的特色")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁340~347：鏈路狀態路由協定與OSPF演算法核心架構"
    talk_id = "CCNA-340-347"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 距離向量限制回顧：RIP 15 跳瓶頸與鏈路狀態協定演進", sec1)
    builder.add_section("🌐 鏈路狀態協定（Link-State）原理：LSA 泛洪與全網拓撲樹建立", sec2)
    builder.add_section("🧭 Dijkstra SPF 最短路徑優先演算法與 OSPF 階層化收斂優勢", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-07"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-340-347-鏈路狀態路由與OSPF演算法核心架構-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：鏈路狀態路由（Link-State Routing）與 OSPF 協定核心機制  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 9: OSPF Fundamentals & Link-State  
> **學習目標**：理解 LSA 泛洪、掌握 LSDB 資料庫同步原理及 SPF 最短路徑優先演算法  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-340-347-鏈路狀態路由與OSPF演算法核心架構-proofread.md)](./CCNA1-Lesson-340-347-鏈路狀態路由與OSPF演算法核心架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["鏈路狀態通告 (LSA - Link-State Advertisement)"] --> B["全網泛洪 (LSA Flooding to Neighbors)"]
    B --> C["彙整建立鏈路狀態資料庫 (LSDB)"]
    C --> D["全區域所有路由器具備 100% 相同之 LSDB 拓撲圖"]
    D --> E["獨立執行 Dijkstra SPF 演算法"]
    E --> F["以本路由器為根生成最短路徑樹 (SPF Tree)"]
    F --> G["最佳無迴圈路徑注入路由表 (RIB)"]
```

---

## 🔬 技術精華與核心考點解析

### 1. 鏈路狀態 vs. 距離向量核心差異
- **全域視野**：距離向量僅知鄰居傳聞（Routing by Rumor）；鏈路狀態路由器掌握全網完整拓撲地圖（LSDB）。
- **觸發更新**：平時僅傳遞微小 Hello 封包維持鄰居關係，僅在鏈路狀態改變時才觸發傳送增量 LSA，節省頻寬。
- **無跳數限制**：OSPF 度量標準採用**成本（Cost = 參考頻寬 / 介面頻寬）**，不受 RIP 15 跳之規模限制。

### 2. OSPF 三張核心表
1. **鄰居表（Neighbor Table / Adjacency Database）**：記錄所有建立鄰接關係的相鄰路由器（`show ip ospf neighbor`）。
2. **拓撲表（Topology Database / LSDB）**：記錄全區域所有路由器及鏈路狀態資訊（`show ip ospf database`）。
3. **路由表（Routing Table / Forwarding Database）**：SPF 運算後產生的最佳轉發路徑（`show ip route ospf`）。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：同一 OSPF Area 內的所有路由器，其鏈路狀態資料庫（LSDB）內容必定 100% 完全相同！**
2. **管理距離：OSPF 的預設 AD 值為 110。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-340-347-鏈路狀態路由與OSPF演算法核心架構-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 340~347!")


def build_session_348_353():
    print("Building CCNA1 348~353...")
    raw = (RAW_DIR / "CCNA1 348~353 週二 上午10點21分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_ospf_transcript(raw)

    p1 = cleaned.find("好，那我們來看這個多區域的架構")
    p2 = cleaned.find("那接下來的話，我們看路由器的角色")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁348~353：OSPF區域架構設計與骨幹Area0階層模型"
    talk_id = "CCNA-348-353"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 OSPF 階層化區域劃分動機：抑制 LSA 泛洪與隔離拓撲震盪", sec1)
    builder.add_section("🌐 骨幹區域（Backbone Area 0）核心樞紐與非骨幹區域連接規範", sec2)
    builder.add_section("🧭 OSPF 路由器角色定義：內部路由器（Internal）、ABR 與 ASBR 職責", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-07"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-348-353-OSPF區域架構設計與骨幹Area0階層模型-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：OSPF 階層化區域（Hierarchical Routing）、骨幹 Area 0 與路由器角色分工  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 9: Multi-Area OSPF Architecture  
> **學習目標**：掌握區域劃分對 CPU/LSDB 的減負效益、骨幹區域 Area 0 星狀拓撲及 ABR/ASBR 定位  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-348-353-OSPF區域架構設計與骨幹Area0階層模型-proofread.md)](./CCNA1-Lesson-348-353-OSPF區域架構設計與骨幹Area0階層模型-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph Backbone ["骨幹區域 (Backbone Area 0)"]
        BB_R1["骨幹路由器 Backbone Router"]
        ABR1["區域邊界路由器 (ABR 1)"]
        ABR2["區域邊界路由器 (ABR 2)"]
        BB_R1 <--> ABR1
        BB_R1 <--> ABR2
    end

    subgraph Area1 ["標準非骨幹區域 (Area 1)"]
        ABR1 <--> IR1["內部路由器 (Internal Router 1)"]
    end

    subgraph Area2 ["標準非骨幹區域 (Area 2)"]
        ABR2 <--> IR2["內部路由器 (Internal Router 2)"]
        IR2 <--> ASBR["自治系統邊界路由器 (ASBR)"]
        ASBR <-->|"重發布 (Redistribute)"| External["外部網路 (BGP/EIGRP/Internet)"]
    end
```

---

## 🔬 技術精華與核心考點解析

### 1. 多區域 OSPF 核心優勢
- **縮小 LSDB 容量**：各區域內的拓撲細節由 ABR 進行摘要，單一區域內的鏈路變動不會引起全網 SPF 重算。
- **限制 LSA 泛洪範圍**：Type 1/Type 2 LSA 嚴格限制在區域內部，跨區由 ABR 生成 Type 3 網路摘要 LSA。
- **提升路由彙總彈性**：可在 ABR 邊界執行跨區網段彙總（Route Summarization），大幅縮減全網路由表條目。

### 2. 路由器四種角色定義
1. **內部路由器（Internal Router）**：所有介面皆屬於同一個非骨幹區域。
2. **骨幹路由器（Backbone Router）**：至少有一個介面屬於 Area 0。
3. **區域邊界路由器（ABR - Area Border Router）**：連接 Area 0 與一個或多個非骨幹區域，維護多個獨立的 LSDB。
4. **自治系統邊界路由器（ASBR - Autonomous System Boundary Router）**：連接外部其他路由網域（如 RIP、BGP、靜態路由）並執行路由重發布（Redistribution）。

---

## 💡 關鍵總結與考試應對重點

1. **架構鐵則：多區域 OSPF 設計中，所有非骨幹區域（Area 1, 2...）在實體或邏輯上必須直接連接至骨幹區域 Area 0！**
2. **單區域考點：若企業僅配置單一區域（Single-Area），該區域依法規推薦一律配置為 Area 0。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-348-353-OSPF區域架構設計與骨幹Area0階層模型-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 348~353!")


def build_session_354_364():
    print("Building CCNA1 354~364...")
    raw = (RAW_DIR / "CCNA1 354~364 週二 上午11點13分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_ospf_transcript(raw)

    p1 = cleaned.find("好，那我們看這個 router-id 啊")
    p2 = cleaned.find("那接下來的話，我們看 network 指令")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁354~364：OSPF單區域配置指令與RouterID選任機制"
    talk_id = "CCNA-354-364"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 OSPF 啟動指令語法：router ospf <process-id> 本地有效性說明", sec1)
    builder.add_section("🌐 Router ID 選任三部曲：手動指定 vs. Loopback vs. 實體活動介面", sec2)
    builder.add_section("🧭 network 指令與反向遮罩（Wildcard Mask）精確啟用介面與 Area 指派", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-07"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-354-364-OSPF單區域配置指令與RouterID選任機制-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：Cisco IOS OSPFv2 單區域配置、Router ID 判定優先權與 Wildcard Mask 匹配實務  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 9: OSPFv2 Configuration & Router ID  
> **學習目標**：掌握 `router ospf` 程序 ID、`router-id` 指派優先順序、`network` 萬用遮罩宣告及狀態檢查  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-354-364-OSPF單區域配置指令與RouterID選任機制-proofread.md)](./CCNA1-Lesson-354-364-OSPF單區域配置指令與RouterID選任機制-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Start["Router ID 選任判定流程"] --> CheckManual{"是否手動配置 router-id 指令？"}
    CheckManual -- 是 --> UseManual["直接採用手動指定之 32-bit IPv4 位址"]
    CheckManual -- 否 --> CheckLoopback{"是否存在任何啟動之 Loopback 介面？"}
    CheckLoopback -- 是 --> UseLoopback["採用數值最大之 Loopback 介面 IP (Highest IP)"]
    CheckLoopback -- 否 --> UsePhysical["採用數值最大且處於 UP 狀態之實體介面 IP (Highest Physical IP)"]
```

---

## 🔬 技術精華與核心考點解析

### 1. OSPF 基礎設定標準範例
```cisco
router ospf 10
 router-id 1.1.1.1
 network 10.1.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0
```
- **Process ID**：僅在本地路由器具有意義（Local Significance），相鄰路由器之間的 Process ID **無需相同**。
- **Wildcard Mask**：反向遮罩，`0` 代表嚴格比對，`1` 代表忽略（如 `0.0.0.255` 對應 `/24`）。
- **Passive Interface**：被動介面，該介面所屬網段會通告給 OSPF 鄰居，但該介面**停止發送與接收 OSPF Hello 封包**，保護內網安全並節省頻寬。

### 2. 驗證與診斷指令
- `show ip ospf neighbor`：檢視鄰居狀態（正常應達到 `FULL/DR` 或 `FULL/BDR` 或 `FULL/DROTHER`）。
- `show ip protocols`：檢視目前啟動之 OSPF Process ID、Router ID、通告之網段與管理距離（110）。
- `clear ip ospf process`：強制重啟 OSPF 程序以套用新變更之 Router ID。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：OSPF 的 Process ID 不需要全網一致，但 Area ID 必須與相鄰介面所屬區域完全相符才能建立鄰居關係！**
2. **優先權陷阱：變更 Router ID 後不會立即生效，必須執行 `clear ip ospf process` 或重新開機才會生效。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-354-364-OSPF單區域配置指令與RouterID選任機制-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 354~364!")


if __name__ == "__main__":
    build_session_340_347()
    build_session_348_353()
    build_session_354_364()
    print("\nAll 3 Tuesday CCNA1 sessions successfully built and validated!")
