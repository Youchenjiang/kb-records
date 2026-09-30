#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build CompTIA Security+ Week 1 Part 2 (Lessons 4-7, 11 sessions)
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
    # 1. Lesson4 1~9
    build_and_save_session(
        folder_name="Lesson4 1~9 週三 上午09點05分",
        file_prefix="SecurityPlus-Lesson04-01-09-身分鑑別與存取管理IAM架構",
        title="CompTIA Security+ Lesson 04 頁01~09：身分識別、鑑別與密碼管理原則",
        talk_id="SECPLUS-04-01-09",
        date="2025-01-15",
        sections=[
            ("🎯 身分識別與存取管理（IAM）核心哲學與課堂導引", 0.0, 0.33),
            ("🔑 識別（Identification）與驗證（Authentication）機制剖析", 0.33, 0.66),
            ("🔒 密碼原則設計：長度、複雜度、防碰撞提示與記憶限制", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：身分識別與存取管理（IAM）、驗證概念與企業密碼原則  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 4: Identity & Access Management Fundamentals  
> **學習目標**：釐清 Identification 與 Authentication 差異，掌握企業密碼策略  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson04-01-09-身分鑑別與存取管理IAM架構-proofread.md)](./SecurityPlus-Lesson04-01-09-身分鑑別與存取管理IAM架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["使用者 (Subject) 請求存取"] --> B["身分識別 (Identification)"]
    B --> C["提出身分宣告 (如帳號、員工編號)"]
    C --> D["身分驗證 (Authentication)"]
    D --> E["驗證宣告真偽 (如密碼、私鑰、生物特徵)"]
    E --> F["授權存取 (Authorization)"]
    F --> G["稽核記錄 (Accounting / Auditing)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **IAM 核心四步驟（IAAA）**：識別（Who you are）、鑑別（Prove it）、授權（What you can do）、稽核（What you did）。
2. **密碼策略實務**：單純提高複雜度易導致便利性反噬（如貼便條紙），現代密碼策略更推崇足夠長度（Passphrase）與防暴力破解鎖定機制。
"""
    )

    # 2. Lesson4 18~26
    build_and_save_session(
        folder_name="Lesson4 18~26 週三 上午11點11分",
        file_prefix="SecurityPlus-Lesson04-18-26-多因素驗證MFA與生物辨識技術",
        title="CompTIA Security+ Lesson 04 頁18~26：多因素驗證（MFA）、生物特徵識別與實體權杖",
        talk_id="SECPLUS-04-18-26",
        date="2025-01-15",
        sections=[
            ("🎯 多因素驗證（MFA）五大因子：知、有、在、為、做", 0.0, 0.33),
            ("🧬 生物辨識技術與評估指標：FAR、FRR 與交叉錯誤率 CER", 0.33, 0.66),
            ("📱 實體安全金鑰、FIDO2 晶片與 OTP 一次性密碼機制", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：多因素驗證（MFA）分類、生物辨識效能評估與硬體金鑰  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 4: MFA & Biometric Authentication  
> **學習目標**：理解 MFA 各項要素、掌握 FAR/FRR 權衡與無密碼 FIDO2 趨勢  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson04-18-26-多因素驗證MFA與生物辨識技術-proofread.md)](./SecurityPlus-Lesson04-18-26-多因素驗證MFA與生物辨識技術-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["多因素驗證 (MFA)"] --> B["Something You Know (知識因子: 密碼/PIN)"]
    A --> C["Something You Have (擁有因子: 手機/OTP/硬體金鑰)"]
    A --> D["Something You Are (生物特徵: 指紋/臉部/虹膜)"]
    A --> E["Somewhere You Are (地理位置: GPS/IP)"]
    A --> F["Something You Do (行為特徵: 擊鍵節奏/簽名)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **真正 MFA 定義**：必須跨越「不同因子類別」。輸入兩組密碼不是 MFA，密碼搭配手機 Authenticator App 才是 MFA。
2. **生物辨識指標 CER**：錯誤接受率（FAR）與錯誤拒絕率（FRR）的交會點即為 Crossover Error Rate (CER)，CER 愈低代表系統整體精確度愈高。
"""
    )

    # 3. Security+ Lesson4 27~34
    build_and_save_session(
        folder_name="Security+ Lesson4 27~34 週三 下午01點04分",
        file_prefix="SecurityPlus-Lesson04-27-34-帳號生命週期與目錄服務同盟",
        title="CompTIA Security+ Lesson 04 頁27~34：帳號生命週期管理、目錄服務與身分同盟（SSO）",
        talk_id="SECPLUS-04-27-34",
        date="2025-01-15",
        sections=[
            ("🎯 本地端帳號管理 vs. 集中式目錄服務（Active Directory / LDAP）", 0.0, 0.33),
            ("🔄 帳號生命週期管理：進用（Onboarding）、權限審查與即時停權（Offboarding）", 0.33, 0.66),
            ("🌐 單一登入（SSO）與跨機構身分同盟（Federation - SAML / OIDC）", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：集中式帳號管理、生命週期維運與同盟單一登入（SSO）  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 4: Identity Federation & Lifecycle  
> **學習目標**：掌握 LDAP/Kerberos 目錄運作、員工離退停權程序與 SAML/OIDC 同盟架構  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson04-27-34-帳號生命週期與目錄服務同盟-proofread.md)](./SecurityPlus-Lesson04-27-34-帳號生命週期與目錄服務同盟-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["用戶端 (User Agent)"] --> B["服務提供者 (Service Provider - SP)"]
    B --> C["重新導向至身分提供者 (Identity Provider - IdP)"]
    C --> D["用戶端進行單一登入鑑別 (SSO)"]
    D --> E["IdP 發行安全斷言宣告 (SAML Token / JWT)"]
    E --> B["SP 驗證 Token 並授權存取資源"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **離職即時停權**：員工離職或職務異動時，必須有標準化流程即時停用集中式帳號，防止孤兒帳號（Orphan Accounts）殘留。
2. **身分同盟優勢**：透過 SAML 2.0 或 OpenID Connect (OIDC)，企業員工可用同一身分安全存取外部雲端 SaaS 服務，免去多套密碼之資安風險。
"""
    )

    # 4. Security+ Lesson5 1~8
    build_and_save_session(
        folder_name="Security+ Lesson5 1~8 週三 下午02點10分",
        file_prefix="SecurityPlus-Lesson05-01-08-園區網路架構與安全區域規劃",
        title="CompTIA Security+ Lesson 05 頁01~08：企業園區網路架構、安全區域規劃與邊界隔離",
        talk_id="SECPLUS-05-01-08",
        date="2025-01-15",
        sections=[
            ("🎯 企業園區在地網路拓撲（On-Premises Topology）與安全層級劃分", 0.0, 0.33),
            ("🛡️ 邊界隔離原則：外部網路、內部受信任區與 DMZ 非軍事區架構", 0.33, 0.66),
            ("🧱 虛擬區域網路（VLAN）分段與二層安全隔離最佳實務", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：在地網路安全拓撲、DMZ 邊界規劃與 VLAN 微區段隔離  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 5: Network Architecture & Segmentation  
> **學習目標**：掌握對外公開伺服器 DMZ 配置、內部機敏網段隔離與二層攻擊防禦  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson05-01-08-園區網路架構與安全區域規劃-proofread.md)](./SecurityPlus-Lesson05-01-08-園區網路架構與安全區域規劃-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Internet["外部未受信任網際網路 (Untrusted)"] --> FW1["邊界防火牆 (Perimeter Firewall)"]
    FW1 --> DMZ["DMZ 非軍事區 (Web / Mail / DNS Server)"]
    FW1 --> FW2["內部核心防火牆 (Internal Firewall)"]
    FW2 --> LAN["內部信任區域 (Trusted LAN / ERP / DB)"]
    DMZ -.->|嚴格禁止由 DMZ 主動發起連線| LAN
```

---

## 🔑 重點提要 (Key Takeaways)

1. **DMZ 設計原則**：所有對外提供公開服務之主機皆應置於 DMZ，即使被攻陷亦無法橫向滲透內部資料庫。
2. **網路分段（Segmentation）**：利用 VLAN 與子網劃分將財務、人資、研發與訪客網路隔離，阻斷勒索軟體橫向傳播。
"""
    )

    # 5. Security+ Lesson5 20~23
    build_and_save_session(
        folder_name="Security+ Lesson5 20~23 週四 上午10點41分",
        file_prefix="SecurityPlus-Lesson05-20-23-防火牆檢驗機制與OPNsense實作",
        title="CompTIA Security+ Lesson 05 頁20~23：次世代防火牆狀態檢驗、NAT 與 OPNsense 實作",
        talk_id="SECPLUS-05-20-23",
        date="2025-01-16",
        sections=[
            ("🎯 無狀態封包過濾（Stateless） vs. 狀態檢驗防火牆（Stateful Inspection）", 0.0, 0.33),
            ("🌐 網路位址轉譯（NAT/PAT）隱匿內部拓撲與連接埠轉發實務", 0.33, 0.66),
            ("🔥 開源開源防火牆 OPNsense 實機介面操作、服務規則與管理介面防護", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：防火牆狀態檢查核心、NAT 轉譯與開源 OPNsense 防火牆操作  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 5: Firewalls & OPNsense Hands-on  
> **學習目標**：理解 TCP 連線狀態追蹤表、掌握 NAT/PAT 配置與 OPNsense 防火牆實機維運  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson05-20-23-防火牆檢驗機制與OPNsense實作-proofread.md)](./SecurityPlus-Lesson05-20-23-防火牆檢驗機制與OPNsense實作-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Client["內部用戶端"] -->|TCP SYN (建立連線)| FW["狀態檢驗防火牆 (Stateful Firewall)"]
    FW -->|記錄連線進入狀態表 (State Table)| Server["外部網站伺服器"]
    Server -->|TCP SYN-ACK (回應封包)| FW
    FW -->|檢查符合狀態表已核准連線| Client
    Attacker["外部未經允許偽造連線"] -->|TCP ACK (無先前請求)| FW
    FW -->|狀態表查無紀錄：直接阻斷 (Drop / Reject)| Drop["丟棄封包"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **狀態檢驗（Stateful）優勢**：防火牆動態維護連線狀態表，只要內部發起的連線，其返回之對應流量自動放行，無需對外開放所有 Port。
2. **次世代防火牆（NGFW）**：延伸至應用程式層（L7 DPI）與入侵防禦系統（IPS），能辨識深度封包內容而非僅看 IP 與連接埠。
"""
    )

    # 6. Security+ Lesson5 26~36
    build_and_save_session(
        folder_name="Security+ Lesson5 26~36 週四 下午01點04分",
        file_prefix="SecurityPlus-Lesson05-26-36-遠端存取通道與零信任安全架構",
        title="CompTIA Security+ Lesson 05 頁26~36：遠端桌面連線、VPN 穿隧安全與零信任網路存取",
        talk_id="SECPLUS-05-26-36",
        date="2025-01-16",
        sections=[
            ("🎯 遠端管理通訊協定安全：RDP、SSH、VNC 漏洞與傳輸加密剖析", 0.0, 0.33),
            ("🛡️ 虛擬私有網路（VPN）架構：IPsec（ESP/AH） vs. SSL/TLS VPN 評估", 0.33, 0.66),
            ("🏰 零信任架構（Zero Trust Architecture - ZTA）核心原則：永不信任、始終驗證", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：遠端桌面管理、VPN 加密通道與零信任網路存取（ZTNA）  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 5: Remote Access & Zero Trust  
> **學習目標**：防範 RDP 暴力破解、評估 IPsec/SSL VPN 優劣，落實零信任身分與設備姿態驗證  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson05-26-36-遠端存取通道與零信任安全架構-proofread.md)](./SecurityPlus-Lesson05-26-36-遠端存取通道與零信任安全架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    User["遠端使用者與設備"] --> PEP["策略強制執行點 (Policy Enforcement Point - PEP)"]
    PEP --> PDP["策略決策點 (Policy Decision Point - PDP)"]
    PDP -->|評估身分驗證 + MFA| PDP
    PDP -->|評估設備合規性 (EDR / Patch / 證書)| PDP
    PDP -->|評估環境情境 (時間 / 地點)| PDP
    PDP -->|下達動態存取授權| PEP
    PEP --> Res["最小權限存取內部特定應用服務 (Microsegmentation)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **嚴禁將 RDP 直接暴露於公網**：3389 埠直接掛在公網為勒索軟體最愛之突破口，必須透過 VPN 或跳板機（Bastion Host）並強制 MFA。
2. **零信任本質（Never Trust, Always Verify）**：打破傳統「內網即信任」迷思，每一次存取皆需重新檢驗身分、設備姿態與最小權限。
"""
    )

    # 7. Lesson6 ~18
    build_and_save_session(
        folder_name="Lesson6 ~18週四 下午03點09分",
        file_prefix="SecurityPlus-Lesson06-01-18-密碼學攻擊手法與演算法弱點",
        title="CompTIA Security+ Lesson 06 頁01~18：密碼學攻擊手法、彩虹表碰撞與降級攻擊防禦",
        talk_id="SECPLUS-06-01-18",
        date="2025-01-16",
        sections=[
            ("🎯 暴力破解（Brute Force）、字典攻擊與混合型密碼攻擊分析", 0.0, 0.33),
            ("🌈 離線預先計算攻擊：彩虹表（Rainbow Tables）原理與加鹽（Salting）防禦", 0.33, 0.66),
            ("⚡ 密碼演算法實作弱點：生日碰撞攻擊（Birthday Attack）與 TLS 降級攻擊", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：常見密碼破解攻擊、彩虹表運作原理與演算法弱點防護  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 6: Cryptographic Attacks & Weaknesses  
> **學習目標**：理解線上 vs. 離線密碼攻擊、掌握 Salt+Pepper 雜湊防護與抗碰撞要求  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson06-01-18-密碼學攻擊手法與演算法弱點-proofread.md)](./SecurityPlus-Lesson06-01-18-密碼學攻擊手法與演算法弱點-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["明文密碼 (Password)"] --> B["加入隨機鹽值 (Salt)"]
    B --> C["慢速密鑰衍生雜湊 (PBKDF2 / Argon2 / bcrypt)"]
    C --> D["安全儲存於資料庫"]
    Attacker["攻擊者取得雜湊庫"] --> E{"嘗試使用彩虹表 (Rainbow Table) 破解"}
    E -->|因隨機 Salt 使得預算表無效| F["破解失敗：必須針對單一密碼個別窮舉"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **加鹽（Salting）關鍵價值**：Salt 破壞了預先計算雜湊表（Rainbow Table）的經濟效益，確保相同密碼之不同使用者擁有完全不同的雜湊值。
2. **密鑰延展函數（Key Stretching）**：使用 Argon2 或 PBKDF2 增加單次雜湊運算時間，有效遏制 GPU/ASIC 暴力破解速度。
"""
    )

    # 8. Security+ Lesson6 21~27
    build_and_save_session(
        folder_name="Security+ Lesson6 21~27 週五 上午09點08分",
        file_prefix="SecurityPlus-Lesson06-21-27-資料隱碼混淆與隱寫術防護",
        title="CompTIA Security+ Lesson 06 頁21~27：資料遮蔽、權杖化技術與隱寫術（Steganography）",
        talk_id="SECPLUS-06-21-27",
        date="2025-01-17",
        sections=[
            ("🎯 資訊隱藏學（Steganography）原理：圖片音訊 LSB 最低有效位元嵌入", 0.0, 0.33),
            ("🎭 資料保護與資料遮蔽（Data Masking）：靜態遮蔽 vs. 動態遮蔽實務", 0.33, 0.66),
            ("🎟️ 權杖化技術（Tokenization）：PCI DSS 信用卡交易資料防護架構", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：資訊隱寫術（Steganography）、資料遮蔽與權杖化（Tokenization）  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 6: Data Obfuscation & Steganography  
> **學習目標**：識別機敏資料外洩之隱寫通道、掌握資料遮蔽手法與 PCI DSS 權杖化機制  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson06-21-27-資料隱碼混淆與隱寫術防護-proofread.md)](./SecurityPlus-Lesson06-21-27-資料隱碼混淆與隱寫術防護-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Card["客戶信用卡號 (PAN)"] --> Gateway["安全支付閘道 (Payment Gateway)"]
    Gateway --> Vault["權杖保存庫 (Token Vault - 高規格隔離加密)"]
    Vault -->|隨機生成無數學意義代碼| Token["權杖 (Token)"]
    Token --> Merchant["商家內部系統 (資料庫僅儲存 Token)"]
    Merchant -.->|駭客竊取商家資料庫| Hack["僅取得無效代碼：真實卡號未外洩"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **權杖化（Tokenization） vs. 加密**：加密可透過演算法與金鑰解回明文；權杖化是由隨機代碼對應資料庫，代碼本身毫無數學可逆性，大幅縮小 PCI DSS 稽核範圍。
2. **隱寫術偵測**：隱寫術常被攻擊者用於機敏資料外洩（Exfiltration）或惡意酬載載入，需仰賴行為分析與異常雜湊檢測。
"""
    )

    # 9. Lesson7 6~17
    build_and_save_session(
        folder_name="Lesson7 6~17 週五 下午01點05分",
        file_prefix="SecurityPlus-Lesson07-06-17-三二一備份原則與異地備援",
        title="CompTIA Security+ Lesson 07 頁06~17：3-2-1 備份黃金原則、異地備援距離與加密實務",
        talk_id="SECPLUS-07-06-17",
        date="2025-01-17",
        sections=[
            ("🎯 3-2-1 備份黃金原則：3 份資料副本、2 種不同儲存媒介、1 份異地保存", 0.0, 0.33),
            ("📏 異地備援（Off-site Backup）地理距離規範與區域型天然災害防護考量", 0.33, 0.66),
            ("🔒 備份資料端到端加密、金鑰保管與存取隔離控制", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：3-2-1 備份原則、異地實體距離規劃與機敏備份加密保護  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 7: Backup Strategies & Redundancy  
> **學習目標**：落實 3-2-1 備份拓撲、理解區域性災害對異地距離之要求與加密存放  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson07-06-17-三二一備份原則與異地備援-proofread.md)](./SecurityPlus-Lesson07-06-17-三二一備份原則與異地備援-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Data["企業營運資料庫 (Original Data)"] --> B1["副本 1: 本地高效磁碟陣列 (Media 1)"]
    Data --> B2["副本 2: 本地實體磁帶 / NAS (Media 2)"]
    Data --> B3["副本 3: 異地加密備份 / 雲端儲存 (Off-site / Cloud)"]
    B3 -.->|距離考量| Dist["跨斷層、跨變電所、跨縣市防範天災"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **3-2-1 現代化延伸（3-2-1-1-0）**：加碼 1 份離線/不可變（Air-gapped / Immutable）副本，以及 0 個備份還原錯誤驗證。
2. **異地備援距離**：兩地距離不能僅設在同一園區隔壁棟，須考量地震、停電或淹水等區域天災，確保至少跨電網/跨地理區域。
"""
    )

    # 10. Lesson7 30
    build_and_save_session(
        folder_name="Lesson7 30 週五 下午02點26分",
        file_prefix="SecurityPlus-Lesson07-18-30-災害復原規劃與業務衝擊分析",
        title="CompTIA Security+ Lesson 07 頁18~30：災害復原計畫（DRP）、業務影響分析（BIA）與 RTO/RPO",
        talk_id="SECPLUS-07-18-30",
        date="2025-01-17",
        sections=[
            ("🎯 業務持續性管理（BCP）與業務影響分析（BIA）核心框架", 0.0, 0.33),
            ("⏱️ 關鍵復原指標：復原時間目標（RTO）與復原點目標（RPO）權衡", 0.33, 0.66),
            ("🏢 備援機房站點類型比較：熱站（Hot Site）、溫站（Warm Site）與冷站（Cold Site）", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：災害復原計畫（DRP）、BIA 衝擊評估與 RTO/RPO 復原指標  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 7: Disaster Recovery & BIA  
> **學習目標**：計算 RTO 與 RPO、評估 Hot/Warm/Cold 備援站點建置成本與啟動時間  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson07-18-30-災害復原規劃與業務衝擊分析-proofread.md)](./SecurityPlus-Lesson07-18-30-災害復原規劃與業務衝擊分析-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    Event["發生災害中斷點"]
    LastBackup["最後一次備份時間"] -->|RPO (容許資料流失量)| Event
    Event -->|RTO (容許系統停機復原時間)| Recovered["系統完全復原上線"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **RTO vs. RPO**：RTO 是系統停擺到修好的時間長度；RPO 是最後一次備份到當機之間所丟失之資料量。數值愈接近零，建置成本呈指數上升。
2. **備援站點選擇**：Hot Site 具備即時同步與全套設備（復原時間幾近於零但極貴）；Warm Site 需還原資料；Cold Site 僅有空間電力無預載硬體。
"""
    )

    # 11. Lesson7 週五 下午03點31分
    build_and_save_session(
        folder_name="Lesson7 週五 下午03點31分",
        file_prefix="SecurityPlus-Lesson07-31-40-不可變備份與系統快照驗證演練",
        title="CompTIA Security+ Lesson 07 頁31~40：快照技術、不可變備份（WORM）與勒索軟體防禦演練",
        talk_id="SECPLUS-07-31-40",
        date="2025-01-17",
        sections=[
            ("🎯 快照技術（Snapshots）與完整映像檔備份之效能與空間權衡", 0.0, 0.33),
            ("🔒 不可變儲存（Immutable Storage / WORM）阻斷勒索軟體加密機制", 0.33, 0.66),
            ("🧪 備份還原定時演練實務：驗證備份完整性與避開『備而不測』陷阱", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：不可變儲存（Immutable Backups）、快照機制與定期復原演練  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 7: Immutable Backups & Ransomware Defense  
> **學習目標**：防範勒索軟體破壞備份檔、建立 Write Once Read Many (WORM) 保護並落實驗證  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson07-31-40-不可變備份與系統快照驗證演練-proofread.md)](./SecurityPlus-Lesson07-31-40-不可變備份與系統快照驗證演練-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["主機資料進行備份"] --> B["儲存至不可變儲存庫 (Immutable Storage)"]
    B --> C["設定物件鎖定原則 (Object Lock / WORM 模式)"]
    Ransom["勒索軟體感染內部網路"] --> D["嘗試搜尋並加密/刪除備份檔"]
    D --> B
    B -->|系統拒絕修改指令| Safe["備份檔維持完好無損"]
    Safe --> Recover["管理員立即以未受損備份進行完整復原"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **不可變備份抗勒索**：現代勒索軟體會先潛伏並尋找備份系統刪除之。啟用 WORM 或 S3 Object Lock 確保即使擁有最高管理員權限也無法在設定期限內刪除或竄改。
2. **驗證勝於備份**：沒有經過成功還原測試的備份等於不存在，企業必須排程模擬災害演練確認資料可用。
"""
    )


if __name__ == "__main__":
    run_batch()
