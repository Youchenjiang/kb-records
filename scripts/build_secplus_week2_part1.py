#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build CompTIA Security+ Week 2 Part 1 (Lessons 8-12, 8 sessions)
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
    # 1. Security+ Lesson8 11~13
    build_and_save_session(
        folder_name="Security+ Lesson8 11~13週一 上午09點07分",
        file_prefix="SecurityPlus-Lesson08-11-13-雲端共享責任模型與服務架構",
        title="CompTIA Security+ Lesson 08 頁11~13：雲端運算架構、共享責任模型（SRM）與安全配置",
        talk_id="SECPLUS-08-11-13",
        date="2025-01-20",
        sections=[
            ("🎯 雲端運算服務模型：IaaS、PaaS 與 SaaS 之控制權邊界", 0.0, 0.33),
            ("🤝 雲端共享責任模型（Shared Responsibility Model - SRM）權責劃分", 0.33, 0.66),
            ("🔒 雲端存取安全性代理（CASB）與雲端安全姿態管理（CSPM）實務", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：雲端運算服務架構、共享責任模型（SRM）與企業雲端安全控管  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 8: Cloud Models & Shared Responsibility  
> **學習目標**：釐清 IaaS/PaaS/SaaS 責任歸屬、掌握 CASB/CSPM 雲端合規監控  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson08-11-13-雲端共享責任模型與服務架構-proofread.md)](./SecurityPlus-Lesson08-11-13-雲端共享責任模型與服務架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph SaaS ["軟體即服務 (SaaS)"]
        S1["客戶責任：資料與身分存取 (Data & IAM)"]
        S2["業者責任：應用程式、作業系統、硬體與機房"]
    end
    subgraph PaaS ["平台即服務 (PaaS)"]
        P1["客戶責任：應用程式代碼與資料 (App & Data)"]
        P2["業者責任：作業系統、運行環境、伺服器硬體"]
    end
    subgraph IaaS ["基礎架構即服務 (IaaS)"]
        I1["客戶責任：作業系統、修補、防火牆、資料 (OS & Above)"]
        I2["業者責任：虛擬化底層、伺服器實體硬體與機房"]
    end
```

---

## 🔑 重點提要 (Key Takeaways)

1. **資料責任永遠在客戶**：無論使用 IaaS、PaaS 還是 SaaS，資料擁有權與法規合規性責任永遠歸屬於客戶企業本身。
2. **CASB 守門員角色**：雲端存取安全性代理（CASB）作為地端與雲端間的受控閘道，負責強制執行 DLP、身分認證與威脅防禦。
"""
    )

    # 2. Security+ Lesson8 29~36
    build_and_save_session(
        folder_name="Security+ Lesson8 29~36 週一 上午11點29分",
        file_prefix="SecurityPlus-Lesson08-29-36-弱點評估架構與CVE資料庫",
        title="CompTIA Security+ Lesson 08 頁29~36：弱點管理架構、CVE/NVD 資料庫與 CVSS 風險評分",
        talk_id="SECPLUS-08-29-36",
        date="2025-01-20",
        sections=[
            ("🎯 弱點管理生命週期：探索、評估、修補、驗證與監控", 0.0, 0.33),
            ("📚 弱點公開揭露標準：CVE 編號、NVD 國家弱點資料庫與 CWE 弱點類型", 0.33, 0.66),
            ("📊 通用弱點評分系統（CVSS v3.1）：基礎分數、時間向量與環境衝擊計算", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：弱點管理生命週期、CVE/NVD 資料庫與 CVSS 風險指標計算  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 8: Vulnerability Management & CVSS  
> **學習目標**：理解 CVE 識別碼體系、解讀 CVSS 向量字串並排定修補優先權  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson08-29-36-弱點評估架構與CVE資料庫-proofread.md)](./SecurityPlus-Lesson08-29-36-弱點評估架構與CVE資料庫-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    A["漏洞被研究員/駭客發現"] --> B["指派 CVE 編號 (MITRE CVE)"]
    B --> C["NVD 深入分析與豐富化"]
    C --> D["評定 CVSS 基礎分數 (0.0 ~ 10.0)"]
    D --> E["企業比對受影響資產"]
    E --> F{"依 CVSS 分數排定修補 SLA"}
    F -->|Critical 9.0-10.0| G["24 小時內緊急修補"]
    F -->|High 7.0-8.9| H["7 天內完成排程修補"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **CVSS 指標三維度**：Base Metrics（固有弱點本質）、Temporal Metrics（是否有 Exploit 武器化流傳）、Environmental Metrics（在特定企業內之實際影響）。
2. **CWE vs. CVE**：CWE 為弱點型態分類（如 SQL Injection、Buffer Overflow）；CVE 則是特定軟體特定版本上的具體具名漏洞。
"""
    )

    # 3. Security+ Lesson9 4~20
    build_and_save_session(
        folder_name="Security+ Lesson9 4~20 週一 下午01點07分",
        file_prefix="SecurityPlus-Lesson09-04-20-主機安全強化與作業系統基準",
        title="CompTIA Security+ Lesson 09 頁04~20：作業系統安全強化（Hardening）、服務停用與基準配置",
        talk_id="SECPLUS-09-04-20",
        date="2025-01-20",
        sections=[
            ("🎯 系統強化（System Hardening）黃金法則：最小化曝險與預設安全", 0.0, 0.33),
            ("🚫 預設服務關閉實務：停用不必要連接埠、Telnet/FTP 與移除預設帳密", 0.33, 0.66),
            ("📋 安全配置基準（Baselines）：CIS Benchmarks 與群組原則（GPO）自動化套用", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：作業系統強化（OS Hardening）、服務最小化與 CIS 安全基準  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 9: Host Hardening & Baselines  
> **學習目標**：停用多餘服務、改寫不安全預設值，利用 GPO 落實企業安全 Baseline  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson09-04-20-主機安全強化與作業系統基準-proofread.md)](./SecurityPlus-Lesson09-04-20-主機安全強化與作業系統基準-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["原生乾淨安裝作業系統 (出廠預設狀態)"] --> B["停用/移除預設未用服務 (如 Telnet, SMBv1)"]
    B --> C["停用或重新命名預設 Administrator / Guest 帳號"]
    C --> D["關閉非必要網路連接埠與協定"]
    D --> E["套用 CIS Benchmark / DISA STIG 安全範本"]
    E --> F["透過 Active Directory GPO 全網強制下發"]
    F --> G["產出受合規保護之強化主機基準 (Hardened Baseline)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **預設安全（Secure by Default）**：絕不保留任何預設密碼、示範帳號或預設開放的管理埠號。
2. **CIS Benchmarks**：網路安全中心（CIS）發布的指引為國際公認之作業系統安全強化權威標準，可直接量化主機合規程度。
"""
    )

    # 4. Security+ Lesson10 1~14
    build_and_save_session(
        folder_name="Security+ Lesson10 1~14週一 下午02點17分",
        file_prefix="SecurityPlus-Lesson10-01-14-洋蔥路由Tor與端點磁碟加密實務",
        title="CompTIA Security+ Lesson 10 頁01~14：暗網與洋蔥路由（Tor）、全磁碟加密與更新管理",
        talk_id="SECPLUS-10-01-14",
        date="2025-01-20",
        sections=[
            ("🎯 深網（Deep Web） vs. 暗網（Dark Web）與洋蔥路由（Tor）多層加密運作原理", 0.0, 0.33),
            ("🔒 全磁碟加密（FDE）：BitLocker、FileVault 與 TPM 信任平台模組防盜實務", 0.33, 0.66),
            ("🔄 端點更新與修補管理（Patch Management）：測試環境驗證與安全模式除錯", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：Tor 洋蔥路由匿名機制、全磁碟加密保護與端點修補維運  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 10: Tor, FDE & Endpoint Patching  
> **學習目標**：理解洋蔥多跳路由技術、配置 BitLocker/TPM 保護靜態資料並實施更新管理  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson10-01-14-洋蔥路由Tor與端點磁碟加密實務-proofread.md)](./SecurityPlus-Lesson10-01-14-洋蔥路由Tor與端點磁碟加密實務-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    Client["用戶端 (Tor Browser)"] -->|多層加密包裹| Guard["入口節點 (Guard Relay)"]
    Guard -->|解開第一層| Middle["中繼節點 (Middle Relay)"]
    Middle -->|解開第二層| Exit["出口節點 (Exit Relay)"]
    Exit -->|解開最後一層 (明文)| Target["目標網站 / 服務"]
    Exit -.->|僅出口節點知曉目標，但不知來源| Target
    Guard -.->|僅入口節點知曉來源，但不知目標| Client
```

---

## 🔑 重點提要 (Key Takeaways)

1. **洋蔥路由特性**：每一跳（Hop）節點僅知曉前一個節點與後一個節點，無任何單一節點能完整串接使用者身分與訪問目標。
2. **靜態資料保護（At-Rest）**：全磁碟加密（FDE）結合主機板 TPM 晶片，防止筆電失竊後硬碟直接拔下於其他主機讀取資料。
"""
    )

    # 5. Security+ Lesson10 14~20
    build_and_save_session(
        folder_name="Security+ Lesson10 14~20週一 下午03點21分",
        file_prefix="SecurityPlus-Lesson10-14-20-端點偵測回應EDR與檔案完整性監控",
        title="CompTIA Security+ Lesson 10 頁14~20：端點防護演進、EDR 行為分析與檔案完整性監控（FIM）",
        talk_id="SECPLUS-10-14-20",
        date="2025-01-20",
        sections=[
            ("🎯 傳統防毒特徵碼（Signature）限制與次世代端點防護（NGAV）導入", 0.0, 0.33),
            ("🛡️ 端點偵測與回應（EDR / XDR）：遙測資料收集、行為異常告警與自動隔離", 0.33, 0.66),
            ("📜 檔案完整性監控（File Integrity Monitoring - FIM）核心系統檔防篡改", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：端點偵測與回應（EDR）、XDR 延伸技術與 FIM 完整性監控  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 10: EDR, XDR & File Integrity Monitoring  
> **學習目標**：理解行為啟發式偵測、掌握 EDR 端點遏制指令與核心檔案雜湊監控  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson10-14-20-端點偵測回應EDR與檔案完整性監控-proofread.md)](./SecurityPlus-Lesson10-14-20-端點偵測回應EDR與檔案完整性監控-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Endpoint["端點代理程式 (EDR Agent)"] -->|持續收集處理程序、註冊表、網路遙測| Engine["行為分析引擎 (AI/ML)"]
    Engine --> Check{"是否偏離行為基準線？"}
    Check -->|偵測到勒索特徵 (如大量短時間改副檔名)| Alert["觸發高度資安警報"]
    Alert --> Action1["網路端點即時隔離 (Network Containment)"]
    Alert --> Action2["終止惡意 Process 與記憶體傾印 (Memory Dump)"]
    Alert --> Action3["回傳 SOC 戰情室進行鑑識調閱"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **EDR 行為偵測優勢**：無檔案攻擊（Fileless Malware）與活生生環境利用（Living-off-the-Land）不落地檔案，傳統防毒無效，必須靠 EDR 監控 PowerShell/WMI 行為。
2. **FIM 關鍵性**：監控 `/etc/passwd`、`System32` 等系統關鍵檔案的雜湊變動，一有非經授權改動立刻發報。
"""
    )

    # 6. Security+ Lesson11 4~9
    build_and_save_session(
        folder_name="Security+ Lesson11 4~9 週二 上午09點15分",
        file_prefix="SecurityPlus-Lesson11-04-09-網路偵察技術與Nmap掃描實戰",
        title="CompTIA Security+ Lesson 11 頁04~09：網路偵察（Reconnaissance）、Nmap 掃描技術與服務指紋識別",
        talk_id="SECPLUS-11-04-09",
        date="2025-01-21",
        sections=[
            ("🎯 被動偵察（Passive Recon） vs. 主動偵察（Active Recon）風險與痕跡剖析", 0.0, 0.33),
            ("🧭 網路探索與通訊埠掃描神兵利器：Nmap 原理與 SYN Stealth 掃描（-sS）", 0.33, 0.66),
            ("🔍 服務版本偵測（-sV）、作業系統指紋辨識（-O）與 NSE 腳本引擎應用", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：主動/被動偵察手法、Nmap 掃描參數原理與作業系統指紋探測  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 11: Reconnaissance & Nmap Scanning  
> **學習目標**：熟練 Nmap 常用參數語法、掌握 TCP 半開放掃描（SYN Scan）與防火牆規避  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson11-04-09-網路偵察技術與Nmap掃描實戰-proofread.md)](./SecurityPlus-Lesson11-04-09-網路偵察技術與Nmap掃描實戰-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
sequenceDiagram
    autonumber
    actor Attacker as 掃描發起端 (Nmap)
    participant Target as 目標伺服器 (Target Host)
    Note over Attacker,Target: TCP SYN 半開隱形掃描 (-sS)
    Attacker->>Target: TCP SYN (探測 80 埠)
    alt 埠號開放 (Open)
        Target-->>Attacker: TCP SYN-ACK
        Attacker->>Target: TCP RST (主動中斷不完成交握，不留應用層 Log)
    else 埠號關閉 (Closed)
        Target-->>Attacker: TCP RST
    else 遭防火牆過濾 (Filtered)
        Note over Target: 封包遭 Drop，逾時無回應
    end
```

---

## 🔑 重點提要 (Key Takeaways)

1. **主動 vs. 被動偵察**：被動偵察（Whois、DNS、OSINT、社群網路）不直接碰觸目標主機，無日誌紀錄；主動偵察（Nmap、Ping sweep）封包直接抵達目標，極易觸發 IDS 告警。
2. **SYN Stealth 掃描優勢**：發送 RST 中斷三次交握，避免建立正式 TCP 連線，從而在傳統 Web 應用程式日誌中不留痕跡。
"""
    )

    # 7. Security+ Lesson11 10~14
    build_and_save_session(
        folder_name="Security+ Lesson11 10~14 週二 上午10點06分",
        file_prefix="SecurityPlus-Lesson11-10-14-弱點掃描工具與憑證掃描策略",
        title="CompTIA Security+ Lesson 11 頁10~14：弱點掃描工具（Nessus）、憑證掃描（Credentialed）與誤報排除",
        talk_id="SECPLUS-11-10-14",
        date="2025-01-21",
        sections=[
            ("🎯 自動化弱點掃描器（Nessus, OpenVAS, Qualys）運作架構與 Plugin 外掛機制", 0.0, 0.33),
            ("🔑 憑證掃描（Credentialed Scan） vs. 非憑證外圍掃描（Non-Credentialed Scan）", 0.33, 0.66),
            ("⚖️ 掃描結果分析矩陣：誤報（False Positive）排除與漏報（False Negative）危害", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：弱點掃描器部署、憑證掃描深度分析與誤報/漏報矩陣判讀  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 11: Vulnerability Scanners & Methodology  
> **學習目標**：理解弱點掃描外掛原理、配置管理員憑證提升掃描精準度並剔除偽陽性  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson11-10-14-弱點掃描工具與憑證掃描策略-proofread.md)](./SecurityPlus-Lesson11-10-14-弱點掃描工具與憑證掃描策略-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Scan["弱點掃描排程啟動"] --> Mode{"選擇掃描模式"}
    Mode -->|非憑證掃描 (外部黑箱)| NonCred["僅從外部探測 Banner 與開放服務"]
    NonCred --> Res1["雜訊多、誤報率高、無法檢測內部補丁缺漏"]
    Mode -->|憑證掃描 (內部白箱)| Cred["使用唯讀管理員帳密登入目標主機"]
    Cred --> Res2["清查軟體註冊表版本、系統 Patch 狀態與組態檔案"]
    Res2 --> Res3["高精確度報告，極低誤報率"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **憑證掃描之必要性**：非憑證掃描只能看到表面服務 Banner；提供特定權限憑證才能真正檢查 Windows 登錄檔或 Linux 套件套裝有無修補重大漏洞。
2. **False Negative 最危險**：False Positive 只是浪費工時人工核實；False Negative 則是漏洞真實存在卻未被檢出，給予管理員虛假安全感。
"""
    )

    # 8. Security+ Lesson12 37~43
    build_and_save_session(
        folder_name="Security+ Lesson12 37~43 週三 上午10點10分",
        file_prefix="SecurityPlus-Lesson12-37-43-資安事件應變流程與數位鑑識原則",
        title="CompTIA Security+ Lesson 12 頁37~43：事件應變生命週期（PICERL）、遏制根除與證據監管鏈",
        talk_id="SECPLUS-12-37-43",
        date="2025-01-22",
        sections=[
            ("🎯 NIST SP 800-61 / SANS 資安事件應變六大階段（PICERL）實務架構", 0.0, 0.33),
            ("🛡️ 遏制策略（Containment）：隔離被感染主機、防火牆即時阻斷與記憶體保全", 0.33, 0.66),
            ("⚖️ 數位鑑識與法律證據：證據揮發順序（Order of Volatility）與監管鏈（Chain of Custody）", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：事件應變生命週期（PICERL）、遏制與根除處置、數位鑑識證據保全  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 12: Incident Response & Digital Forensics  
> **學習目標**：熟悉事件應變標準作業程序、掌握證據揮發性順序與法律監管鏈要求  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson12-37-43-資安事件應變流程與數位鑑識原則-proofread.md)](./SecurityPlus-Lesson12-37-43-資安事件應變流程與數位鑑識原則-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    P["準備階段 (Preparation)"] --> I["識別與偵測 (Identification)"]
    I --> C["遏制與圍堵 (Containment)"]
    C --> E["根除威脅 (Eradication)"]
    E --> R["系統復原 (Recovery)"]
    R --> L["經驗檢討總結 (Lessons Learned)"]
    L -.->|回饋優化| P
```

---

## 🔑 重點提要 (Key Takeaways)

1. **證據揮發性順序（Order of Volatility）**：由最易消失至最持久：CPU 快取/暫存器 $\to$ 實體記憶體（RAM） $\to$ 網路狀態/核心快取 $\to$ 磁碟儲存 $\to$ 遠端日誌 $\to$ 實體備份。拔插頭前務必先做記憶體傾印！
2. **監管鏈（Chain of Custody）**：記載何人、何時、何因接觸過該數位證物，中途不得有斷裂，否則法院將判定證物失效不可採信。
"""
    )


if __name__ == "__main__":
    run_batch()
