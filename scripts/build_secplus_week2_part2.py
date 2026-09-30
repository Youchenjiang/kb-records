#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build CompTIA Security+ Week 2 Part 2 (Lessons 13-16, 10 sessions)
Follows PROOFREAD_RULES.md, ScenarioType.CLASSROOM_LECTURE, and tests/test_proofread_linter.py.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2025-CompTIA-SecurityPlus"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"

from scripts.build_secplus_week1_part1 import (
    clean_sec_transcript,
    segment_into_dialogue_paragraphs,
    build_and_save_session,
)


def run_batch():
    # 1. Security+ Lesson13 1~6
    build_and_save_session(
        folder_name="Security+ Lesson13 1~6 週三 上午11點14分",
        file_prefix="SecurityPlus-Lesson13-01-06-傳統產業資安轉型與工控系統安全",
        title="CompTIA Security+ Lesson 13 頁01~06：企業資安人力配置、法規合規與舊版工控系統防護",
        talk_id="SECPLUS-13-01-06",
        date="2025-01-22",
        sections=[
            ("🎯 傳統製造業資訊環境生態與政府資安專職人力法規強制要求", 0.0, 0.33),
            ("🏭 工控與半導體舊版作業系統（Legacy Systems）維運現實與實體隔離（Air-gap）", 0.33, 0.66),
            ("🚀 太空晶片耐用性要求與舊硬體架構之安全修補限制", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：傳產資安轉型現況、舊系統（Legacy/OT）防護挑戰與法規要求  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Operational Technology & Legacy Security  
> **學習目標**：理解企業規模門檻資安人力法規、掌握半導體與航太舊架構補丁難題  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-01-06-傳統產業資安轉型與工控系統安全-proofread.md)](./SecurityPlus-Lesson13-01-06-傳統產業資安轉型與工控系統安全-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["政府資安管理法規強制力"] --> B["百人/特定資本額企業強制配置專職資安長與人員"]
    B --> C["傳統產業資安轉型挑戰"]
    C --> D["產線舊系統 (Legacy OT: Win95/XP) 無法連網更新"]
    C --> E["半導體/航太特用晶片高可靠性 vs. 不易修補"]
    D --> F["實體隔離 (Air-gapped) + 專屬補償控制措施 (Compensating Controls)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **舊系統維運現實**：許多高精密度半導體機台與航太系統運作於舊版 OS 上，無法直接升級或聯網修補，必須採用實體隔離與嚴格周邊設備管控。
2. **法規驅動資安就業**：政府法規強制要求中大型企業設置資安專責人員，帶動傳統產業強勁的資安合規人才需求。
"""
    )

    # 2. Security+ Lesson13 7~14
    build_and_save_session(
        folder_name="Security+ Lesson13 7~14 週三 下午01點06分",
        file_prefix="SecurityPlus-Lesson13-07-14-惡意軟體特徵與間諜廣告軟體分析",
        title="CompTIA Security+ Lesson 13 頁07~14：惡意程式分類、廣告軟體（Adware）與特洛伊木馬潛伏",
        talk_id="SECPLUS-13-07-14",
        date="2025-01-22",
        sections=[
            ("🎯 惡意程式多樣化型態：病毒（Virus）、蠕蟲（Worm）與特洛伊木馬（Trojan）", 0.0, 0.33),
            ("📢 灰色軟體（Grayware）威脅：廣告軟體（Adware）綁架與間諜軟體（Spyware）潛伏", 0.33, 0.66),
            ("💣 隱蔽式後門（Backdoor）與邏輯炸彈（Logic Bomb）觸發條件分析", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：惡意軟體家族分類、廣告間諜軟體誘裝與後門潛伏機制  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Malware Classifications & Indicators  
> **學習目標**：識別病毒/蠕蟲自我複製特性、掌握木馬偽裝手法與邏輯炸彈防範  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-07-14-惡意軟體特徵與間諜廣告軟體分析-proofread.md)](./SecurityPlus-Lesson13-07-14-惡意軟體特徵與間諜廣告軟體分析-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Malware["惡意軟體家族 (Malware)"] --> V["病毒 (Virus: 需依附宿主執行檔)"]
    Malware --> W["蠕蟲 (Worm: 具主動自我複製與跨網路傳播)"]
    Malware --> T["木馬 (Trojan: 偽裝成正常實用工具)"]
    Malware --> S["間諜/廣告 (Spyware/Adware: 側錄鍵盤與綁架瀏覽器)"]
    Malware --> L["邏輯炸彈 (Logic Bomb: 等待特定時間/事件條件引爆)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **病毒 vs. 蠕蟲本質差異**：病毒必須仰賴使用者點擊執行或宿主程式啟動；蠕蟲利用網路通訊協定弱點具備自主跨主機擴散能力。
2. **邏輯炸彈防禦**：多見於內部員工心懷不滿埋藏程式碼，須透過程式碼同儕審查（Peer Review）與離職停權機制防範。
"""
    )

    # 3. Security+ Lesson13 14~18
    build_and_save_session(
        folder_name="Security+ Lesson13 14~18 週三 下午02點21分",
        file_prefix="SecurityPlus-Lesson13-14-18-勒索軟體運作機制與殭屍網路C2架構",
        title="CompTIA Security+ Lesson 13 頁14~18：勒索軟體攻擊鏈、殭屍網路（Botnet）與中繼控制站（C2）",
        talk_id="SECPLUS-13-14-18",
        date="2025-01-22",
        sections=[
            ("🎯 現代雙重勒索（Double Extortion）：資料加密 + 竊取暗網外洩雙軌施壓", 0.0, 0.33),
            ("🤖 殭屍網路（Botnet）拓撲架構：集中式 C2 伺服器 vs. P2P 去中心化控制", 0.33, 0.66),
            ("⚡ 阻斷服務攻擊（DoS/DDoS）：放大攻擊（Amplification）與分散式洪氾防禦", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：現代勒索軟體攻擊生態、殭屍網路 C2 基礎設施與 DDoS 防護  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Ransomware & Botnets  
> **學習目標**：防禦雙重勒索威脅、掌握 C2 域名生成演算法（DGA）與流量清洗機制  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-14-18-勒索軟體運作機制與殭屍網路C2架構-proofread.md)](./SecurityPlus-Lesson13-14-18-勒索軟體運作機制與殭屍網路C2架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Attacker["殭屍網路主控者 (Botmaster)"] --> C2["中繼指揮伺服器 (C2 Server)"]
    C2 -->|下達攻擊指令| Bot1["受控殭屍電腦 (Zombie 1)"]
    C2 -->|下達攻擊指令| Bot2["受控物聯網設備 (Zombie 2)"]
    C2 -->|下達攻擊指令| Bot3["受控伺服器主機 (Zombie 3)"]
    Bot1 & Bot2 & Bot3 -->|集中發送巨量惡意流量 (SYN/UDP Flood)| Target["受害企業目標伺服器 (DDoS Target)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **雙重勒索轉變**：傳統只加密檔案（可用備份還原）；現代勒索軟體先偷偷打包機敏資料至外部伺服器，若不付贖金即於暗網拍賣公開。
2. **C2 偵測指標**：監控 DNS 查詢頻率與可疑隨機網域名稱（DGA），切斷 Bot 與 C2 之間的指令傳遞通道。
"""
    )

    # 4. Security+ Lesson13 19~22
    build_and_save_session(
        folder_name="Security+ Lesson13 19~22週三 下午03點22分",
        file_prefix="SecurityPlus-Lesson13-19-22-實體社交工程與尾隨翻垃圾攻擊防禦",
        title="CompTIA Security+ Lesson 13 頁19~22：實體環境社交工程、尾隨入侵（Tailgating）與搜垃圾防禦",
        talk_id="SECPLUS-13-19-22",
        date="2025-01-22",
        sections=[
            ("🎯 人性弱點漏洞利用：社交工程（Social Engineering）核心心理學原理", 0.0, 0.33),
            ("🚪 實體門禁攻防：尾隨（Tailgating/Piggybacking）與旋轉柵門（Turnstiles）防禦", 0.33, 0.66),
            ("🗑️ 實體廢棄物洩密：搜垃圾（Dumpster Diving）、肩窺（Shoulder Surfing）與碎紙機規範", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：實體社交工程、尾隨門禁漏洞與機敏廢棄物處理防範  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Physical Security & Social Engineering  
> **學習目標**：識破尾隨搭訕話術、落實訪客刷卡查驗與 DIN 66399 碎紙銷毀標準  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-19-22-實體社交工程與尾隨翻垃圾攻擊防禦-proofread.md)](./SecurityPlus-Lesson13-19-22-實體社交工程與尾隨翻垃圾攻擊防禦-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Attacker["社交工程攻擊者 (偽裝訪客/外送員/清潔工)"] --> Step1{"嘗試入侵實體大樓"}
    Step1 -->|手法 1: 尾隨 (Tailgating)| Gate["利用員工熱心開門混入"]
    Step1 -->|手法 2: 搜垃圾 (Dumpster Diving)| Trash["翻找未碎紙機銷毀之內部報表"]
    Step1 -->|手法 3: 肩窺 (Shoulder Surfing)| Screen["在公共場所偷窺密碼與螢幕"]
    Defense["企業對應防禦"] --> D1["防尾隨閘門 (Mantraps / 一人一卡閘門)"]
    Defense --> D2["上鎖廢紙回收桶 + 碎紙十字銷毀"]
    Defense --> D3["防窺保護貼 + 員工資安意識培訓"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **尾隨防禦**：教育員工「不幫任何人扶門刷卡」，並設置捕人陷阱閘門（Mantrap / Security Air Lock），一次只容許單人驗證通過。
2. **搜垃圾情報價值**：企業廢棄之便條紙、會議紀錄、組織架構圖常成為攻擊者拼湊社交工程劇本的黃金情資。
"""
    )

    # 5. Security+ Lessson13 22~25
    build_and_save_session(
        folder_name="Security+ Lessson13 22~25週四 上午09點11分",
        file_prefix="SecurityPlus-Lesson13-22-25-線上密碼攻擊與憑證填充防護",
        title="CompTIA Security+ Lesson 13 頁22~25：線上密碼破解手法、密碼噴灑（Spraying）與憑證填充防護",
        talk_id="SECPLUS-13-22-25",
        date="2025-01-23",
        sections=[
            ("🎯 線上密碼攻擊（Online） vs. 離線密碼攻擊（Offline）之風險與網路環境限制", 0.0, 0.33),
            ("🌧️ 規避帳號鎖定機制：密碼噴灑（Password Spraying）對抗傳統鎖定策略", 0.33, 0.66),
            ("📦 外洩憑證重複利用：憑證填充（Credential Stuffing）與 CAPTCHA/MFA 縱深防禦", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：線上密碼攻擊手法、密碼噴灑技術與防範外洩憑證填充  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Password Attacks & Credential Stuffing  
> **學習目標**：理解密碼噴灑如何繞過「連續錯三次鎖定」、部署 MFA 與行為驗證遏止攻擊  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-22-25-線上密碼攻擊與憑證填充防護-proofread.md)](./SecurityPlus-Lesson13-22-25-線上密碼攻擊與憑證填充防護-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph Spraying ["密碼噴灑 (Password Spraying)"]
        Pwd["單一常見弱密碼 (如 Summer2025!)"] --> U1["嘗試使用者 A (第 1 次)"]
        Pwd --> U2["嘗試使用者 B (第 1 次)"]
        Pwd --> U3["嘗試使用者 C (第 1 次)"]
        Note["每個帳號皆只嘗試一次：完全不會觸發鎖定閾值！"]
    end
    subgraph Defense ["有效反制策略"]
        D1["強制全面啟用 MFA"]
        D2["基於風險的情境驗證 (異地登入阻斷)"]
        D3["比對外洩密碼庫 (Have I Been Pwned 阻斷常見弱密碼)"]
    end
```

---

## 🔑 重點提要 (Key Takeaways)

1. **密碼噴灑巧妙處**：傳統暴力破解是對「單一帳號嘗試千百種密碼」（立即鎖定）；密碼噴灑則是對「千百個帳號嘗試同一組常見密碼」，完美隱藏在正常登入雜訊中。
2. **憑證填充根源**：利用大眾「跨站使用同一組帳密」之壞習慣，拿暗網外洩的帳密庫自動化撞庫。
"""
    )

    # 6. Security+ Lesson13 26~32
    build_and_save_session(
        folder_name="Security+ Lesson13 26~32 週四 上午10點19分",
        file_prefix="SecurityPlus-Lesson13-26-32-網路中間人攻擊與ARP毒化防禦",
        title="CompTIA Security+ Lesson 13 頁26~32：網路層中間人攻擊（MitM）、ARP 欺騙毒化與 Rogue DHCP 防禦",
        talk_id="SECPLUS-13-26-32",
        date="2025-01-23",
        sections=[
            ("🎯 局域網路二層攻擊：ARP 快取毒化（ARP Poisoning）與中間人監聽原理", 0.0, 0.33),
            ("📡 未授權 Rogue DHCP 伺服器劫持 Default Gateway 與 DNS 導向攻擊", 0.33, 0.66),
            ("🛡️ 交換器二層安全硬化：動態 ARP 檢驗（DAI）與 DHCP 窺探（DHCP Snooping）", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：局域網中間人攻擊（MitM）、ARP 快取毒化與交換器二層防護實務  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Layer 2 Network Attacks & MitM  
> **學習目標**：剖析 ARP Spoofing 劫持流量機制、配置 DHCP Snooping 與 DAI 交換器防護  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-26-32-網路中間人攻擊與ARP毒化防禦-proofread.md)](./SecurityPlus-Lesson13-26-32-網路中間人攻擊與ARP毒化防禦-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Attacker["中間人攻擊者 (Attacker)"] -->|發送偽造無故 ARP 回應| Host["受害者主機 (Victim)"]
    Attacker -->|發送偽造無故 ARP 回應| GW["預設閘道 (Default Gateway)"]
    Host -->|誤認攻擊者 MAC 為閘道| Traffic1["所有對外流量流經攻擊者"]
    Traffic1 --> Attacker
    Attacker -->|側錄/修改機敏封包後轉發| GW
    GW -->|誤認攻擊者 MAC 為受害主機| Traffic2["所有返回流量流經攻擊者"]
    Traffic2 --> Attacker
    Attacker --> Host
```

---

## 🔑 重點提要 (Key Takeaways)

1. **ARP 協定先天無驗證**：ARP 設計上信任所有接收到的 ARP Reply，導致局域網任何一台電腦都能聲稱自己是 Gateway。
2. **DHCP Snooping + DAI 鐵三角**：交換器啟用 DHCP Snooping 建立 IP-MAC-Port 綁定表，動態 ARP 檢驗（DAI）即以此表為基準丟棄非法 ARP 封包。
"""
    )

    # 7. Security+ Lesson14 1~9
    build_and_save_session(
        folder_name="Security+ Lesson14 1~9 週四 上午11點21分",
        file_prefix="SecurityPlus-Lesson14-01-09-Web應用程式漏洞與目錄周遊防禦",
        title="CompTIA Security+ Lesson 14 頁01~09：Web 應用程式攻擊面、目錄遍歷（Directory Traversal）與注入防禦",
        talk_id="SECPLUS-14-01-09",
        date="2025-01-23",
        sections=[
            ("🎯 Web 應用程式安全防線：根目錄限制（Document Root）與存取沙箱機制", 0.0, 0.33),
            ("📂 目錄遍歷（Directory Traversal - dot-dot-slash）漏洞與越權讀取系統檔實務", 0.33, 0.66),
            ("💉 注入攻擊（Injection）防護核心：輸入驗證（Input Validation）與參數化查詢（Parameterized Query）", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：Web 應用程式安全、目錄遍歷（Directory Traversal）與注入攻擊防護  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 14: Web Application Vulnerabilities  
> **學習目標**：理解目錄周遊路徑解析漏洞、掌握 WAF 過濾與嚴格白名單輸入驗證  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson14-01-09-Web應用程式漏洞與目錄周遊防禦-proofread.md)](./SecurityPlus-Lesson14-01-09-Web應用程式漏洞與目錄周遊防禦-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    Browser["攻擊者瀏覽器"] -->|輸入包含 ../../../etc/passwd 之參數| Web["Web 應用程式伺服器"]
    Web --> Check{"是否有路徑淨化與白名單驗證？"}
    Check -->|無防護：直接傳入檔案讀取 API| Exploit["越權讀取系統敏感檔案 (Directory Traversal 成功)"]
    Check -->|有防護：正規化路徑並限於 DocumentRoot| Safe["攔截並記錄非法路徑攻擊 (回傳 403 Forbidden)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **目錄遍歷本質**：利用作業系統之相對路徑符號（`../`）逃逸出 Web Server 的根目錄限制，存取未經授權之主機系統設定檔。
2. **根本防禦思維**：絕不可將使用者傳入的字串直接拼接為作業系統指令或檔案路徑，必須進行 Canonicalization（路徑規範化）與白名單限制。
"""
    )

    # 8. Security+ Lesson14 10~25
    build_and_save_session(
        folder_name="Security+ Lesson14 10~25 週四 下午01點08分",
        file_prefix="SecurityPlus-Lesson14-10-25-法規遵循框架與台灣資安法個資法實務",
        title="CompTIA Security+ Lesson 14 頁10~25：法規遵循框架、GDPR、台灣資通安全管理法與個資法",
        talk_id="SECPLUS-14-10-25",
        date="2025-01-23",
        sections=[
            ("🎯 企業資安治理委員會職責與避免觸犯法規之防禦架構", 0.0, 0.33),
            ("🌐 國際隱私權法規標竿：歐盟一般資料保護規則（GDPR）與罰則機制", 0.33, 0.66),
            ("🇹🇼 台灣在地資安法制矩陣：資通安全管理法責任分級與個人資料保護法落實", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：資安合規框架、歐盟 GDPR 隱私規範與台灣資安法制實務  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 14: Compliance, Governance & Privacy Laws  
> **學習目標**：理解資通安全管理法 A~E 分級責任、個資法侵害民刑事風險與內部稽核  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson14-10-25-法規遵循框架與台灣資安法個資法實務-proofread.md)](./SecurityPlus-Lesson14-10-25-法規遵循框架與台灣資安法個資法實務-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Board["董事會 / 資安委員會 (Governance)"] --> Compliance["法規遵循架構 (Compliance Framework)"]
    Compliance --> Laws["適用法規矩陣"]
    Laws --> L1["歐盟 GDPR (跨國資料傳輸 / 被遺忘權 / 72hr 通報)"]
    Laws --> L2["台灣資通安全管理法 (關鍵基礎設施 / 專職人力配置)"]
    Laws --> L3["個人資料保護法 (違法蒐集處理利用罰則 / 損害賠償)"]
    Compliance --> Audit["內部稽核與外稽合規查核 (ISO 27001 / SOC 2)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **資安法責任分級**：公務機關與特定非公務機關（關鍵基礎設施）依 A、B、C、D、E 級承擔不同等級的資安人員配置、通報時限與演練責任。
2. **GDPR 巨額罰款**：最高可達全球營業額 4% 或 2000 萬歐元，倒逼全球企業全面重構資料隱私保護架構。
"""
    )

    # 9. Security+ Lesson15 1~13
    build_and_save_session(
        folder_name="Security+ Lesson15 1~13 週四 下午02點21分",
        file_prefix="SecurityPlus-Lesson15-01-13-資安工程師職涯發展與技能高原突破",
        title="CompTIA Security+ Lesson 15 頁01~13：資安專業職涯地圖、算力發展高原與不可替代核心技能",
        talk_id="SECPLUS-15-01-13",
        date="2025-01-23",
        sections=[
            ("🎯 AI 算力演進發展高原期觀察與底層 IT 技術之長青不可替代性", 0.0, 0.33),
            ("🗺️ 資安工程師職涯發展路徑：紅隊攻擊、藍隊防禦與合規治理三叉路", 0.33, 0.66),
            ("🚀 網路與系統底層基本功打底：掌握通訊協定才是應對新威脅的終極解法", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：資安專業職涯規劃、AI 發展趨勢與底層網路系統不可替代價值  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 15: Career Pathways & Industry Trends  
> **學習目標**：建立長遠資安技能樹、掌握紅藍隊專業分工與核心通訊底層技術  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson15-01-13-資安工程師職涯發展與技能高原突破-proofread.md)](./SecurityPlus-Lesson15-01-13-資安工程師職涯發展與技能高原突破-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Base["IT 核心基石：網路 (CCNA) + 系統 (Linux/Windows) + 通訊協定 (TCP/IP)"] --> SecBase["資安核心通用知識 (CompTIA Security+)"]
    SecBase --> Path1["藍隊 (Blue Team / SOC 戰情 / 事件應變 / 威脅獵捕)"]
    SecBase --> Path2["紅隊 (Red Team / 滲透測試 / 逆向工程 / 弱點研究)"]
    SecBase --> Path3["治理與合規 (GRC / 資安長 / 政策顧問 / 隱私稽核)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **底層技術永遠長青**：即使 AI 時代工具更迭劇烈，真正深刻理解作業系統核心、封包結構與交換路由的工程師永遠無法被輕易取代。
2. **T 型人才發展**：先以 Security+ 建立資安通識之廣度（橫杠），再挑選熱愛之專精領域（縱深）鑽研原廠進階證照。
"""
    )

    # 10. Security+ Lesson15 19~ Lesson16 8
    build_and_save_session(
        folder_name="Security+ Lesson15 19~ Lesson16 8 週五 上午09點15分",
        file_prefix="SecurityPlus-Lesson15-19-16-08-安全控制評估與第三方供應商風險",
        title="CompTIA Security+ Lesson 15/16：安全控制成效評估、內外部資源比例與供應鏈風險管理",
        talk_id="SECPLUS-15-19-16-08",
        date="2025-01-24",
        sections=[
            ("🎯 企業資安資源分配比例權衡：內部自建評估團隊 vs. 外部專業顧問採購", 0.0, 0.33),
            ("📦 第三方供應鏈安全與外部供應商風險評估（Vendor Risk Management）", 0.33, 0.66),
            ("🔒 供應商合約約束與服務等級協定（SLA / SOW / NDA）法律實務", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：安全控制評估策略、內外部資源配置與供應鏈第三方風險管理  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 15/16: Vendor Risk & Security Assessments  
> **學習目標**：評估企業內建 vs. 委外資安效益、建立第三方合約防護網並管控供應鏈風險  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson15-19-16-08-安全控制評估與第三方供應商風險-proofread.md)](./SecurityPlus-Lesson15-19-16-08-安全控制評估與第三方供應商風險-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Enterprise["企業核心業務"] --> Vendor["第三方軟硬體與雲端供應商 (Vendors / Suppliers)"]
    Vendor --> Risk{"供應鏈潛在破口 (如 SolarWinds 事件)"}
    Enterprise --> Defense["供應鏈風險管理防線"]
    Defense --> D1["資安合約協定 (SLA, NDA, SOW 載明資安義務)"]
    Defense --> D2["定期外部資安審查與第三方 SOC 2 報告調閱"]
    Defense --> D3["軟體物料清單 (SBOM) 盤點開源套件依賴"]
    Defense --> D4["最小權限委外遠端維護通道"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **軟體供應鏈風險防不勝防**：攻擊者不再直攻大企業，而是攻陷具備信任連線的下游廠商。必須落實嚴格的 Vendor Assessment。
2. **合約是最後一道防線**：在委外契約中必須明確載明資安事件之通報時效、賠償上限與稽核權利（Right to Audit）。
"""
    )


if __name__ == "__main__":
    run_batch()
