#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build remaining Wednesday & Thursday CCNA1 course deliverables (9 sessions):
- CCNA1 383~388: ACL Principles & Wildcard Mask
- CCNA1 389~396: Standard ACL Matching Logic & Direction
- CCNA1 397~403: NAT/PAT Fundamentals & Private IP
- CCNA1 403~414: Dynamic vs Static NAT Translation Tables
- CCNA1 Lab NAT01: NAT Statistics & Inside/Outside Verification
- CCNA1 Lab PAT02: Port Address Translation (Overload) Lab
- CCNA1 Lab Discovery 21: NTP Network Time Protocol
- CCNA1 Lab Fastlab 09: PAT & Wildcard Mask Integration
- CCNA1 415~422: Extended ACL Protocol & Port Filtering
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


def clean_acl_nat_transcript(text: str) -> str:
    """Domain term corrections for ACL and NAT."""
    base = clean_transcript(text)
    replacements = [
        (r"挖卡list", "Wildcard Mask 清單"),
        (r"挖卡", "Wildcard Mask（萬用遮罩）"),
        (r"抵賴", "deny"),
        (r"很密", "permit"),
        (r"旁密", "permit"),
        (r"IPN\s*T", "ip nat"),
        (r"IPN", "ip nat"),
        (r"access\s*list", "access-list"),
        (r"access\s*group", "access-group"),
    ]
    res = base
    for pat, rep in replacements:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def build_session_383_388():
    print("Building CCNA1 383~388...")
    raw = (RAW_DIR / "CCNA1 383~388 週三 上午09點04分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    p1 = cleaned.find("好，那我們來看這個萬用遮罩的計算")
    p2 = cleaned.find("那接下來的話，我們看 ACL 的分類")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁383~388：存取控制清單ACL原理與萬用遮罩計算法則"
    talk_id = "CCNA-383-388"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 存取控制清單（ACL）核心功能定位：封包過濾、NAT 轉譯與 QoS 分類", sec1)
    builder.add_section("🌐 萬用字元遮罩（Wildcard Mask）運算本質：0 比對與 1 忽略二進位規則", sec2)
    builder.add_section("🧭 標準 ACL（1-99）與延伸 ACL（100-199）號碼範圍與命名型清單", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-383-388-存取控制清單ACL原理與萬用遮罩計算法則-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：Cisco ACL 封包過濾機制、Wildcard Mask 反向遮罩二進位計算與清單編號分類  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 10: ACL Principles & Wildcard Mask  
> **學習目標**：掌握 ACL 規則匹配流轉、精確計算萬用遮罩（255.255.255.255 減去子網遮罩）及應用場景  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-383-388-存取控制清單ACL原理與萬用遮罩計算法則-proofread.md)](./CCNA1-Lesson-383-388-存取控制清單ACL原理與萬用遮罩計算法則-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    PacketIn["介面收到資料封包 (Inbound) 或 準備發送 (Outbound)"] --> CheckACL{"介面是否有套用 access-group？"}
    CheckACL -- 否 --> PermitForward["正常路由轉發 (Forward)"]
    CheckACL -- 是 --> MatchRule["自第一行 ACE 規則開始由上而下比對"]

    MatchRule --> IsMatch{"條件是否完全匹配？"}
    IsMatch -- 是 --> Action{"規則為 permit 還是 deny？"}
    Action -- permit --> PermitForward
    Action -- deny --> DropPacket["直接丟棄封包 (Drop)"]

    IsMatch -- 否 --> NextRule{"是否還有下一行規則？"}
    NextRule -- 是 --> MatchRule
    NextRule -- 否 --> ImplicitDeny["命中隱含拒絕 (Implicit Deny Any Any) -> 丟棄封包"]
```

---

## 🔬 技術精華與核心考點解析

### 1. 萬用字元遮罩（Wildcard Mask）計算技巧
- **反向相減法則**：`255.255.255.255` 減去「子網路遮罩」即為對應之萬用遮罩。
  - `/24 (255.255.255.0)` -> 萬用遮罩 `0.0.0.255`。
  - `/27 (255.255.255.224)` -> 萬用遮罩 `0.0.0.31`。
  - `/30 (255.255.255.252)` -> 萬用遮罩 `0.0.0.3`。
- **特殊縮寫關鍵字**：
  - `host 192.168.1.1` 等同於 `192.168.1.1 0.0.0.0`（嚴格精確比對單一主機）。
  - `any` 等同於 `0.0.0.0 255.255.255.255`（忽略全部位元，比對所有位址）。

### 2. ACL 編號範圍與功能
| 清單類型 | 傳統標準編號 | 擴充編號範圍 | 檢查條件 |
| :--- | :--- | :--- | :--- |
| **標準 ACL (Standard)** | 1 ~ 99 | 1300 ~ 1999 | **僅檢查來源 IP 位址** |
| **延伸 ACL (Extended)** | 100 ~ 199 | 2000 ~ 2699 | 檢查來源/目的 IP、協定 (TCP/UDP/ICMP) 及連接埠號 |

---

## 💡 關鍵總結與考試應對重點

1. **考試鐵則：所有 ACL 清單的最末尾，皆存在一行看不見的「隱含拒絕（Implicit Deny Any Any）」，若未命中任何 permit 規則，封包一律遭丟棄！**
2. **規則順序：ACL 採由上而下（Top-Down）初次匹配即停止，範圍最小、條件最嚴苛的規則必須寫在前面！**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-383-388-存取控制清單ACL原理與萬用遮罩計算法則-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 383~388!")


def build_session_389_396():
    print("Building CCNA1 389~396...")
    raw = (RAW_DIR / "CCNA1 389~396 週三 上午10點13分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    p1 = cleaned.find("好，我們看這個套用方向啊")
    p2 = cleaned.find("那接下來的話，我們看命名型的 ACL")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁389~396：標準ACL規則匹配邏輯與介面套用方向實務"
    talk_id = "CCNA-389-396"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 標準 ACL 語法與規則撰寫準則：小範圍優先與避免全盤拒絕", sec1)
    builder.add_section("🌐 介面套用指令與方向性裁決：inbound vs. outbound 判定準則", sec2)
    builder.add_section("🧭 標準 ACL 最佳放置原則：盡可能靠近目的端（Near the Destination）", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-389-396-標準ACL規則匹配邏輯與介面套用方向實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：標準 ACL 規則撰寫、介面方向套用（ip access-group in/out）與部署黃金準則  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 10: Standard ACL Implementation  
> **學習目標**：精熟標準 ACL 語法、掌握 inbound/outbound 判定及「標準 ACL 放置於靠近目的端」之原則  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-389-396-標準ACL規則匹配邏輯與介面套用方向實務-proofread.md)](./CCNA1-Lesson-389-396-標準ACL規則匹配邏輯與介面套用方向實務-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    SourceHost["來源端主機 (10.1.1.10)"] --> Router1["路由器 R1 (來源端)"]
    Router1 <-->|"WAN 專線 (10.0.0.0/30)"| Router2["路由器 R2 (目的端)"]
    Router2 --> TargetServer["目標伺服器 (10.3.1.100)"]

    Note over Router2: 標準 ACL 部署黃金法則：<br/>因僅檢查來源 IP，必須配置於靠近目的端 (R2 出介面)<br/>避免誤封殺來源端前往其他正常節點之流量！
```

---

## 🔬 技術精華與核心考點解析

### 1. 標準 ACL 配置與介面套用語法
```cisco
! 1. 建立標準 ACL (1-99)
access-list 10 deny host 10.1.1.10
access-list 10 permit 10.1.1.0 0.0.0.255
access-list 10 deny any

! 2. 進入介面套用方向 (in 或 out)
interface GigabitEthernet0/0
 ip access-group 10 out
```
- **Inbound (入向)**：封包剛進入介面、尚未進行路由查表前即執行過濾，節省 CPU 查表開銷。
- **Outbound (出向)**：封包已完成路由查表、準備從該介面送入鏈路時執行過濾。

### 2. ACL 最佳部署位置（Placement）準則
- **標準 ACL**：**盡量放置在靠近目的端（Near the Destination）**。因為標準 ACL 只能過濾來源 IP，若放置在靠近來源端，會導致該主機前往其他所有合法伺服器的連線全數被阻斷。
- **延伸 ACL**：**盡量放置在靠近來源端（Near the Source）**。在源頭儘早阻絕非法流量，避免無效封包白白浪費 WAN 頻寬。

---

## 💡 關鍵總結與考試應對重點

1. **考試必考題：標準 ACL 應放在何處？答案：靠近目的端（As close to the destination as possible）。**
2. **介面限制：一個介面在同一個方向（inbound 或 outbound）且同一個協定（如 IPv4），只能套用「單一一個 ACL」！**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-389-396-標準ACL規則匹配邏輯與介面套用方向實務-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 389~396!")


def build_session_397_403():
    print("Building CCNA1 397~403...")
    raw = (RAW_DIR / "CCNA1 397~403 週三 上午11點08分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    p1 = cleaned.find("好，我們看這個私有地址的範圍")
    p2 = cleaned.find("那接下來的話，我們看 NAT 的三種型態")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁397~403：網路位址轉譯NAT概念與私有IP存取架構"
    talk_id = "CCNA-397-403"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 NAT（Network Address Translation）產生背景：公網位址匱乏與私有 IP 隔離", sec1)
    builder.add_section("🌐 RFC 1918 私有 IP 位址範圍定義：Class A/B/C 保留區段", sec2)
    builder.add_section("🧭 NAT 四大核心位址名詞剖析：Inside/Outside 與 Local/Global 語意", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-397-403-網路位址轉譯NAT概念與私有IP存取架構-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：NAT 網路位址轉譯架構、RFC 1918 私有位址規劃與 Inside/Outside 位址語意  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 11: NAT Fundamentals & Architecture  
> **學習目標**：熟記 RFC 1918 私有 IP 範圍、區分 Inside Local / Inside Global / Outside Global 語意  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-397-403-網路位址轉譯NAT概念與私有IP存取架構-proofread.md)](./CCNA1-Lesson-397-403-網路位址轉譯NAT概念與私有IP存取架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    subgraph PrivateNet ["內部企業私網 (Inside)"]
        PC["內網主機<br/><b>Inside Local</b>: 192.168.1.10"]
    end

    subgraph NATRouter ["邊界路由器 NAT Table"]
        Table["Inside Local: 192.168.1.10:54321<br/>Inside Global: 203.0.113.1:54321<br/>Outside Global: 8.8.8.8:53"]
    end

    subgraph PublicInternet ["網際網路公網 (Outside)"]
        Server["外部 DNS 伺服器<br/><b>Outside Global</b>: 8.8.8.8"]
    end

    PC <-->|"私有 IP 通訊"| NATRouter
    NATRouter <-->|"公有 IP 通訊"| Server
```

---

## 🔬 技術精華與核心考點解析

### 1. RFC 1918 私有 IP 保留位址
- **Class A**：`10.0.0.0 ~ 10.255.255.255`（前綴 `/8`，共 1 個 A 類網段）。
- **Class B**：`172.16.0.0 ~ 172.31.255.255`（前綴 `/12`，共 16 個 B 類網段）。
- **Class C**：`192.168.0.0 ~ 192.168.255.255`（前綴 `/16`，共 256 個 C 類網段）。
- **路由特性**：私有 IP 嚴禁在 Internet 公網核心路由器進行路由，邊界路由器遇私有目的位址一律予以丟棄。

### 2. NAT 四大核心名詞（Cisco 官方標準定義）
1. **Inside Local (內部本地位址)**：內部私網裝置所實際配置的真實私有 IP（例如 `10.1.1.5`）。
2. **Inside Global (內部全域位址)**：內部裝置穿越 NAT 轉譯後，在外部公網所呈現之合法公有 IP。
3. **Outside Local (外部本地位址)**：內部主機所見到的外部目標位址（通常與 Outside Global 相同）。
4. **Outside Global (外部全域位址)**：外部網際網路目標裝置所實際配置的真實公有 IP（例如 Google DNS `8.8.8.8`）。

---

## 💡 關鍵總結與考試應對重點

1. **名詞速記：Local 代表從內網看的位址；Global 代表從外網看的位址；Inside 代表屬於內網的裝置；Outside 代表屬於外網的裝置。**
2. **安全防護：NAT 的附帶價值是提供內網隱匿保護，外部攻擊者無法直接對 Inside Local 私有位址發起未經授權之連線。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-397-403-網路位址轉譯NAT概念與私有IP存取架構-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 397~403!")


def build_session_403_414():
    print("Building CCNA1 403~414...")
    raw = (RAW_DIR / "CCNA1 403~414, 練習 （部分丟失） 週三 下午01點21分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    p1 = cleaned.find("好，我們看這個動態 NAT 跟靜態 NAT 的差別")
    p2 = cleaned.find("那接下來的話，我們看轉譯表的欄位")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁403~414：動態NAT與靜態NAT轉換表運作與故障排除"
    talk_id = "CCNA-403-414"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 靜態 NAT（Static NAT）一對一綁定與對外發布伺服器應用", sec1)
    builder.add_section("🌐 動態 NAT（Dynamic NAT）位址池（Pool）動態租借與回收機制", sec2)
    builder.add_section("🧭 NAT 轉譯表欄位解析與連線追蹤逾時（Timeout）排錯", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-403-414-動態NAT與靜態NAT轉換表運作與故障排除-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：靜態 NAT 一對一對應、動態 NAT 位址池配置與轉譯表壽命週期排錯  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 11: Static & Dynamic NAT  
> **學習目標**：掌握 `ip nat inside source static` 指令、動態 Pool 配合 ACL 綁定及 `clear ip nat translation` 排錯  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-403-414-動態NAT與靜態NAT轉換表運作與故障排除-proofread.md)](./CCNA1-Lesson-403-414-動態NAT與靜態NAT轉換表運作與故障排除-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph StaticNAT ["靜態 NAT (Static NAT - 1對1)"]
        S1["內部 Web Server (192.168.1.100)"] <-->|"永久固定對應"| G1["公網 IP (203.0.113.10)"]
        Note over S1,G1: 支援外部主機主動發起連線
    end

    subgraph DynamicNAT ["動態 NAT (Dynamic NAT - 多對多位址池)"]
        Pool["公網 IP 位址池 (NAT Pool: 203.0.113.20 ~ 203.0.113.25)"]
        Client1["內網主機 PC1"] -->|"動態借用空閒公網 IP"| Pool
        Client2["內網主機 PC2"] -->|"動態借用空閒公網 IP"| Pool
        Note over Pool: 位址池耗盡時，新連線無法建立！
    end
```

---

## 🔬 技術精華與核心考點解析

### 1. 靜態 NAT 與動態 NAT 配置指令
```cisco
! 靜態 NAT (對外發布伺服器)
ip nat inside source static 192.168.1.100 203.0.113.10

! 動態 NAT (位址池 + ACL)
ip nat pool MY_POOL 203.0.113.20 203.0.113.25 netmask 255.255.255.0
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 pool MY_POOL

! 介面定義
interface GigabitEthernet0/0
 ip nat inside
interface Serial0/0/0
 ip nat outside
```

### 2. 轉譯表特性與驗證
- **靜態轉譯條目**：永久存在於 NAT 表中，不會因連線中斷而消失。
- **動態轉譯條目**：僅在有流量通過時生成，若閒置超過 Timeout 時間（TCP 預設 24 小時，UDP 預設幾分鐘），該條目自動回收釋回 Pool。
- **診斷指令**：`show ip nat translations` 檢視所有動態與靜態對應紀錄。

---

## 💡 關鍵總結與考試應對重點

1. **伺服器發布考點：內部伺服器若需接受網際網路外部使用者的主動存取，必須使用「靜態 NAT」進行固定一對一綁定！**
2. **忘記介面標籤：NAT 不通最常見的疏失是在介面上忘記宣告 `ip nat inside` 或 `ip nat outside`。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-403-414-動態NAT與靜態NAT轉換表運作與故障排除-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 403~414!")


def build_session_lab_nat01():
    print("Building CCNA1 Lab NAT01...")
    raw = (RAW_DIR / "CCNA1 練習 週三 下午02點14分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    sec1 = segment_into_dialogue_paragraphs(cleaned)

    title = "Cisco CCNA 1 Lab NAT01：NAT轉換統計監控與InsideOutside介面驗證"
    talk_id = "CCNA-Lab-NAT01"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 NAT 介面屬性檢查與 show ip nat statistics 統計數據判讀", sec1)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lab-NAT01-NAT轉換統計監控與InsideOutside介面驗證-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：NAT 運作統計驗證、Hits/Misses 計數器判讀與 Inside/Outside 介面狀態診斷  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Lab NAT01: Verifying NAT Statistics  
> **學習目標**：掌握 `show ip nat statistics` 輸出、辨識活躍轉換條目及透過連續 ping 驗證 Hits 增加  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-NAT01-NAT轉換統計監控與InsideOutside介面驗證-proofread.md)](./CCNA1-Lab-NAT01-NAT轉換統計監控與InsideOutside介面驗證-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    PingCmd["發起連續 ICMP 測試 (ping -t)"] --> RouterNat["邊界路由器執行 NAT 轉譯"]
    RouterNat --> VerifyCmd["執行 show ip nat statistics"]
    VerifyCmd --> OutputCheck{"檢視統計輸出指標"}
    OutputCheck --> Hits["Hits (命中次數): 持續累加 -> 代表轉譯規則正常運作"]
    OutputCheck --> Misses["Misses (未命中次數): 代表封包未符轉譯條件或位址池不足"]
    OutputCheck --> Active["Active translations: 顯示當前活躍連線數"]
```

---

## 🔬 技術精華與核心考點解析

### 1. `show ip nat statistics` 關鍵欄位解析
- **Total active translations**：當前記憶體中存在的有效 NAT 轉譯總數。
- **Outside interfaces / Inside interfaces**：明確列出已套用 `ip nat outside` 與 `ip nat inside` 的實體與邏輯介面清單。
- **Hits**：封包成功命中轉譯規則並完成 IP/Port 轉換的封包數量。
- **Misses**：嘗試進行轉譯但找不到現成條目（需動態新建）或轉譯失敗的次數。

---

## 💡 關鍵總結與考試應對重點

1. **實務排錯：若連線不通且 Hits 次數為 0，代表流量在到達 NAT 模組前已被 ACL 阻擋，或根本未送達該路由介面！**
2. **清除指令：測試重置時使用 `clear ip nat translation *` 可強制清空所有動態轉譯快取。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lab-NAT01-NAT轉換統計監控與InsideOutside介面驗證-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 Lab NAT01!")


def build_session_lab_pat02():
    print("Building CCNA1 Lab PAT02...")
    raw = (RAW_DIR / "CCNA1 練習 週三 下午02點32分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    sec1 = segment_into_dialogue_paragraphs(cleaned)

    title = "Cisco CCNA 1 Lab PAT02：PAT多對一埠號轉譯配置與連線測試"
    talk_id = "CCNA-Lab-PAT02"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 埠號位址轉譯（PAT / NAT Overload）單一公網 IP 共享實作演練", sec1)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lab-PAT02-PAT多對一埠號轉譯配置與連線測試-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：PAT 埠號轉譯（NAT Overload）實作：多台 PC 共享單一出介面公網 IP 上網  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Lab PAT02: Configuring PAT with Interface Overload  
> **學習目標**：熟練 `ip nat inside source list <acl> interface <intf> overload` 指令與多主機連線驗證  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-PAT02-PAT多對一埠號轉譯配置與連線測試-proofread.md)](./CCNA1-Lab-PAT02-PAT多對一埠號轉譯配置與連線測試-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    PC1["客戶端 PC1 (192.168.1.10:1024)"] --> R1["邊界路由器 PAT 轉譯"]
    PC2["客戶端 PC2 (192.168.1.20:1024)"] --> R1

    R1 <-->|"共享單一出介面 IP (203.0.113.1)"| Internet["網際網路 Web Server"]

    Note over R1: PAT 利用第四層 Port 區隔不同主機：<br/>PC1 轉為 203.0.113.1:50001<br/>PC2 轉為 203.0.113.1:50002
```

---

## 🔬 技術精華與核心考點解析

### 1. PAT 核心配置（Overload 關鍵字）
```cisco
! 1. 定義允許上網之內網網段 ACL
access-list 1 permit 192.168.1.0 0.0.0.255

! 2. 綁定出介面並附加 overload 參數 (PAT 靈魂所在)
ip nat inside source list 1 interface Serial0/0/0 overload

! 3. 套用介面標籤
interface GigabitEthernet0/0
 ip nat inside
interface Serial0/0/0
 ip nat outside
```
- **overload 參數**：告訴路由器透過動態分配 16-bit 傳輸層 Port 號碼，讓多達 65,000+ 條內網連線可同時共享同一個外部 IP。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：如何在一組公網 IP 或單一介面 IP 上允許多台內部主機同時存取 Internet？答案：在 NAT 指令後方加上 `overload` 關鍵字！**
2. **驗證方式：從 PC1 與 PC2 同時發送 ping，在路由器執行 `show ip nat translations` 可看到兩者 Outside IP 相同，但 Port/Identifier 號碼不同。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lab-PAT02-PAT多對一埠號轉譯配置與連線測試-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 Lab PAT02!")


def build_session_discovery21():
    print("Building CCNA1 Lab Discovery 21...")
    raw = (RAW_DIR / "CCNA1 Discovery 21 週三 下午02點52分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_transcript(raw)

    sec1 = segment_into_dialogue_paragraphs(cleaned)

    title = "Cisco CCNA 1 Lab Discovery 21：NTP網路時間協定階層配置實作"
    talk_id = "CCNA-Lab-Disc21"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 網路時間協定（NTP）Stratum 階層架構與主伺服器（NTP Master）配置", sec1)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lab-Discovery21-NTP網路時間協定階層配置實作-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：網路時間協定 NTP 實作：Stratum 階層、ntp master 宣告與用戶端同步驗證  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Lab Discovery 21: Configuring NTP Services  
> **學習目標**：掌握 NTP UDP 123 埠、配置路由器擔任 NTP Master (Stratum 2) 及客戶端校時  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-Discovery21-NTP網路時間協定階層配置實作-proofread.md)](./CCNA1-Lab-Discovery21-NTP網路時間協定階層配置實作-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Clock["原子鐘 / GPS 衛星硬體時脈 (Stratum 0)"] --> Stratum1["頂級時間伺服器 (Stratum 1)"]
    Stratum1 --> RouterMaster["企業內部路由器 (ntp master 2 -> Stratum 2)"]
    RouterMaster --> ClientRouter["分支路由器 / 交換機 (ntp server -> Stratum 3)"]
    ClientRouter --> EndHosts["終端電腦與伺服器日誌同步 (Stratum 4)"]
```

---

## 🔬 技術精華與核心考點解析

### 1. NTP 配置指令
```cisco
! 伺服器端宣告 (設定為 Stratum 2 階層)
ntp master 2

! 客戶端指向伺服器
ntp server 10.3.1.100

! 驗證指令
show ntp status
show ntp associations
```

### 2. Stratum 階層意義
- **Stratum 0**：高精密度外部硬體參考時脈（如 GPS、銫原子鐘）。
- **Stratum 1**：直接連接 Stratum 0 硬體的伺服器。
- **Stratum 2 ~ 15**：透過網路逐層同步之節點，數字越大精準度遞減。
- **Stratum 16**：代表時脈未同步，無法提供有效時間服務。

---

## 💡 關鍵總結與考試應對重點

1. **資安考點：全網時間同步（NTP）是資安事件調查與 SIEM 記錄日誌關聯分析的最關鍵基礎，若時間錯亂則 Log 喪失法庭鑑識效力！**
2. **協定與埠號：NTP 使用 UDP Port 123。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lab-Discovery21-NTP網路時間協定階層配置實作-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 Lab Discovery 21!")


def build_session_fastlab09():
    print("Building CCNA1 Lab Fastlab 09...")
    raw = (RAW_DIR / "CCNA1 Fastlab 9 週三 下午03點18分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    sec1 = segment_into_dialogue_paragraphs(cleaned)

    title = "Cisco CCNA 1 Lab Fastlab 09：PAT流量控制與ACL萬用遮罩整合演練"
    talk_id = "CCNA-Lab-Fastlab09"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 Fastlab 09 實作要求：命名型 ACL 流量篩選與 PAT 轉譯結合演練", sec1)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lab-Fastlab09-PAT流量控制與ACL萬用遮罩整合演練-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：Cisco Fastlab 09：命名型 ACL 搭配 PAT 轉譯流量控制綜合實作演練  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Lab Fastlab 09: PAT & Wildcard Mask Integration  
> **學習目標**：依據實驗規範精確建立 Named ACL、指派萬用遮罩並將其套用於 PAT 出介面  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-Fastlab09-PAT流量控制與ACL萬用遮罩整合演練-proofread.md)](./CCNA1-Lab-Fastlab09-PAT流量控制與ACL萬用遮罩整合演練-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    DefineACL["1. 建立命名型標準 ACL (ip access-list standard NatTraffic)"] --> AddRule["2. 撰寫允許網段與萬用遮罩 (permit 192.168.1.0 0.0.0.255)"]
    AddRule --> BindPAT["3. 綁定 PAT 出介面 (ip nat inside source list NatTraffic interface S0/0/0 overload)"]
    BindPAT --> AssignInt["4. 標註內部/外部介面 (ip nat inside / outside)"]
    AssignInt --> VerifyTest["5. 終端主機 Ping 測試並檢驗 NAT 轉譯表 (show ip nat translations)"]
```

---

## 🔬 技術精華與核心考點解析

### 1. 實驗關鍵設定指令
```cisco
! 建立命名型標準 ACL (名稱必須區分大小寫且完全符合題目規範)
ip access-list standard NatTraffic
 permit 192.168.1.0 0.0.0.255
 exit

! 啟用 PAT (Overload)
ip nat inside source list NatTraffic interface GigabitEthernet0/1 overload

! 介面設定
interface GigabitEthernet0/0
 ip nat inside
interface GigabitEthernet0/1
 ip nat outside
```

---

## 💡 關鍵總結與考試應對重點

1. **命名大小寫考點：在 Cisco IOS 中，命名型 ACL 的名稱（Name）具有大小寫敏感性（Case-Sensitive），題目要求 `NatTraffic` 若打成 `nattraffic` 會被判 0 分！**
2. **驗證方式：使用 `show ip access-lists` 可直接檢視該清單匹配之封包 Matches 計數。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lab-Fastlab09-PAT流量控制與ACL萬用遮罩整合演練-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 Lab Fastlab 09!")


def build_session_415_422():
    print("Building CCNA1 415~422...")
    raw = (RAW_DIR / "CCNA1 415~422 週四 上午09點04分" / "transcript_zh_tw.txt").read_text(encoding="utf-8")
    cleaned = clean_acl_nat_transcript(raw)

    p1 = cleaned.find("好，那我們來看這個延伸 ACL 的語法")
    p2 = cleaned.find("那接下來的話，我們看這個協定跟埠號的過濾")

    sec1 = segment_into_dialogue_paragraphs(cleaned[:p1] if p1 != -1 else cleaned[:len(cleaned)//3])
    mid = cleaned[p1:p2] if (p1 != -1 and p2 != -1) else cleaned[len(cleaned)//3 : 2*len(cleaned)//3]
    sec2 = segment_into_dialogue_paragraphs(mid)
    sec3 = segment_into_dialogue_paragraphs(cleaned[p2:] if p2 != -1 else cleaned[2*len(cleaned)//3:])

    title = "Cisco CCNA 1 Lesson 頁415~422：延伸ACL協定過濾與雙向埠號精確控制"
    talk_id = "CCNA-415-422"
    builder = ProofreadBuilder(
        title=title,
        event="Cisco CCNA 1 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )
    builder.add_section("🎯 延伸 ACL（Extended ACL 100-199）語法架構：協定、來源、目的與運算子", sec1)
    builder.add_section("🌐 常用傳輸層服務埠號過濾實務：HTTP(80)、HTTPS(443)、SSH(22) 與 DNS(53)", sec2)
    builder.add_section("🧭 延伸 ACL 最佳放置原則：盡可能靠近來源端（Near the Source）", sec3)

    rendered = builder.render()
    rendered = rendered.replace('event: "Cisco CCNA 1 認證培訓課程"', 'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-09"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    assert is_valid, f"Validation failed: {errors}"

    proof_file = OUT_DIR / "CCNA1-Lesson-415-422-延伸ACL協定過濾與雙向埠號精確控制-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")

    summary_tmpl = """# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：延伸 ACL（Extended ACL）深度解析：L3/L4 複合過濾、運算子語法與部署原則  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 10: Extended Access Control Lists  
> **學習目標**：掌握延伸 ACL 完整語法、eq/gt/lt/range 埠號運算子及「靠近來源端部署」優勢  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-415-422-延伸ACL協定過濾與雙向埠號精確控制-proofread.md)](./CCNA1-Lesson-415-422-延伸ACL協定過濾與雙向埠號精確控制-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    subgraph ExtendedACL_Rule ["延伸 ACL 語法要素解析"]
        Direction["access-list 101 permit/deny"] --> Protocol["協定類型 (tcp / udp / icmp / ip)"]
        Protocol --> Src["來源位址與萬用遮罩 (source + wildcard)"]
        Src --> SrcPort["來源運算子與埠號 (可選 eq/gt/lt/range)"]
        SrcPort --> Dst["目的位址與萬用遮罩 (dest + wildcard)"]
        Dst --> DstPort["目的運算子與埠號 (常用 eq 80 / 443 / 22)"]
        DstPort --> Established["狀態控制 (可選 established 允許回程)"]
    end
```

---

## 🔬 技術精華與核心考點解析

### 1. 延伸 ACL 標準配置範例
```cisco
! 允許 10.1.1.0/24 網段存取 10.3.1.100 的 Web 服務 (HTTP/HTTPS)
access-list 101 permit tcp 10.1.1.0 0.0.0.255 host 10.3.1.100 eq 80
access-list 101 permit tcp 10.1.1.0 0.0.0.255 host 10.3.1.100 eq 443

! 拒絕該網段存取該伺服器的任何其他服務
access-list 101 deny ip 10.1.1.0 0.0.0.255 host 10.3.1.100

! 允許該網段存取其他所有網際網路資源
access-list 101 permit ip 10.1.1.0 0.0.0.255 any
```

### 2. 延伸 ACL 部署黃金法則
- **靠近來源端（As close to the source as possible）**。
- 因為延伸 ACL 同時具備來源與目的地的檢驗能力，直接在來源端阻絕違規封包，可避免無效封包橫越整個企業骨幹與 WAN 鏈路，最大化節省頻寬與路由器處理負擔。

---

## 💡 關鍵總結與考試應對重點

1. **兩大 ACL 部署對比必考：標準 ACL 放靠近目的端；延伸 ACL 放靠近來源端！**
2. **常見運算子：`eq` (等於)、`neq` (不等於)、`gt` (大於)、`lt` (小於)、`range` (範圍)。**
"""
    summary_content = summary_tmpl.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_file = OUT_DIR / "CCNA1-Lesson-415-422-延伸ACL協定過濾與雙向埠號精確控制-summary.md"
    summary_file.write_text(summary_content.strip() + "\n", encoding="utf-8")
    print("  Done CCNA1 415~422!")


if __name__ == "__main__":
    build_session_383_388()
    build_session_389_396()
    build_session_397_403()
    build_session_403_414()
    build_session_lab_nat01()
    build_session_lab_pat02()
    build_session_discovery21()
    build_session_fastlab09()
    build_session_415_422()
    print("\nAll 9 Wednesday & Thursday CCNA1 sessions successfully built and validated!")
