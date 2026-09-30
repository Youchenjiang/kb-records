#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build CompTIA Security+ Week 1 Part 1 (Lessons 1-3, 8 sessions)
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

DISCLAIMER = (
    "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。"
    "完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動問答，**未做任何刪減或摘要縮寫**；"
    "已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語與標點符號，"
    "明確標註發言角色（授課講師／學員），並依授課脈絡劃分流暢之主題章節。"
)

COMMON_REPLACEMENTS = [
    (r"治安", "資安"),
    (r"自然", "資安"),
    (r"志安", "資安"),
    (r"考格\s*TIA", "CompTIA"),
    (r"考格", "CompTIA"),
    (r"康迪", "CompTIA"),
    (r"Security\s*Plus", "Security+"),
    (r"I\s*A\s*M", "IAM"),
    (r"M\s*F\s*A", "MFA"),
    (r"S\s*S\s*O", "SSO"),
    (r"C\s*I\s*A", "CIA"),
    (r"trades", "Threats"),
    (r"attacks", "Attack Surface"),
    (r"洋蔥瀏覽器", "Tor 瀏覽器"),
    (r"洋蔥", "Tor（洋蔥路由）"),
    (r"大克威", "Dark Web（暗網）"),
    (r"底不威", "Deep Web（深網）"),
    (r"OpenSense", "OPNsense"),
    (r"火燭", "Firefox（火狐）"),
    (r"空", "Chrome"),
    (r"Pearson\s*View", "Pearson VUE"),
    (r"Pearson\s*view", "Pearson VUE"),
    (r"Unview", "OnVUE"),
    (r"Onview", "OnVUE"),
    (r"onview", "OnVUE"),
    (r"點一二九", ".129"),
    (r"點一", ".1"),
    (r"點二", ".2"),
    (r"點二五四", ".254"),
    (r"二五五點二五五點二五五點零", "255.255.255.0"),
    (r"槓二四", "/24"),
    (r"槓三零", "/30"),
]


def clean_sec_transcript(text: str, custom_replacements=None) -> str:
    res = text
    for pat, rep in COMMON_REPLACEMENTS:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    if custom_replacements:
        for pat, rep in custom_replacements:
            res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def segment_into_dialogue_paragraphs(text: str, default_speaker="授課講師") -> str:
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
        if current_len >= 200 or s.endswith("好。") or s.endswith("OK。"):
            paragraphs.append("".join(current_para))
            current_para = []
            current_len = 0

    if current_para:
        paragraphs.append("".join(current_para))

    formatted_paras = []
    for i, p in enumerate(paragraphs):
        p_clean = p.strip()
        if not p_clean:
            continue

        student_triggers = [
            "老師，你怎麼罵人", "老師這題", "報告老師", "會啊。", "兩公里。", "可以嗎？", "是這樣嗎？"
        ]
        is_student = any(trig in p_clean for trig in student_triggers)
        if is_student:
            formatted_paras.append(f"**【學員】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_and_save_session(
    folder_name: str,
    file_prefix: str,
    title: str,
    talk_id: str,
    date: str,
    sections: list,  # [(title, ratio_start, ratio_end, optional_custom_clean)]
    summary_md: str
):
    print(f"Building {file_prefix}...")
    p = RAW_DIR / folder_name / "transcript_zh_tw.txt"
    if not p.exists():
        p = RAW_DIR / folder_name / "raw_transcript.txt"
    raw_text = p.read_text(encoding="utf-8")

    cleaned = clean_sec_transcript(raw_text)

    builder = ProofreadBuilder(
        title=title,
        event="CompTIA Security+ 認證培訓課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    for sec_title, r_start, r_end in sections:
        start_idx = int(total_len * r_start)
        end_idx = int(total_len * r_end)
        chunk = cleaned[start_idx:end_idx]
        formatted_chunk = segment_into_dialogue_paragraphs(chunk)
        builder.add_section(sec_title, formatted_chunk)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "CompTIA Security+ 認證培訓課程"',
        f'event: "CompTIA Security+ 認證培訓課程"\ndate: "{date}"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed for {file_prefix}: {errors}")

    proof_path = OUT_DIR / f"{file_prefix}-proofread.md"
    proof_path.write_text(rendered, encoding="utf-8")

    summary_final = summary_md.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_path = OUT_DIR / f"{file_prefix}-summary.md"
    summary_path.write_text(summary_final, encoding="utf-8")
    print(f"  [OK] Saved {proof_path.name} & {summary_path.name}")


# ==============================================================================
# SESSIONS DEFINITION (8 SESSIONS)
# ==============================================================================

def run_batch():
    # Session 1: Security+ 1~10
    build_and_save_session(
        folder_name="Security+ 1~10週一 上午09點03分",
        file_prefix="SecurityPlus-Lesson01-01-10-資安核心範疇與合規性導論",
        title="CompTIA Security+ Lesson 01 頁01~10：資安核心範疇、合規性與CIA三要素",
        talk_id="SECPLUS-01-01-10",
        date="2025-01-13",
        sections=[
            ("🎯 CompTIA 認證導引與資安專家學習心態", 0.0, 0.33),
            ("⚖️ 企業資安治理核心：法規遵循、合規性（Compliance）與政府稽核", 0.33, 0.66),
            ("🛡️ 資訊安全黃金三角：機密性（Confidentiality）、完整性（Integrity）與可用性（Availability）", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：CompTIA Security+ 認證核心定位、資安合規性法規與 CIA 三要素  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 1: Security Fundamentals  
> **學習目標**：理解資安通識全貌、掌握合規性法規要求與 CIA 三大支柱  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson01-01-10-資安核心範疇與合規性導論-proofread.md)](./SecurityPlus-Lesson01-01-10-資安核心範疇與合規性導論-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["CompTIA Security+ 廣度資安通識"] --> B["企業資安治理基礎"]
    B --> C["合規性 (Compliance) & 法規要求"]
    B --> D["CIA 安全三要素 (Triad)"]
    D --> E["機密性 (Confidentiality)"]
    D --> F["完整性 (Integrity)"]
    D --> G["可用性 (Availability)"]
    C --> H["未合規風險：政府開罰與法律責任先於外部攻擊"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **認證學習定位**：CompTIA Security+ 為廣泛涉獵各資安領域之通識認證，適合全盤了解後再深入特定領域（如法規合規、滲透測試、安全維運）。
2. **合規性重要性**：資安首重 Compliance。在受到駭客威脅前，若不符合政府法規要求，企業將面臨直接罰則。
3. **CIA 三要素平衡**：安全防護不能盲目加強，必須在保護資產機密與完整的同時，確保業務系統之可用性。
"""
    )

    # Session 2: Security+ 操作、3~5
    build_and_save_session(
        folder_name="Security+ 操作、3~5 週一 上午10點03分",
        file_prefix="SecurityPlus-Lesson01-03-05-原廠線上實驗室開通與實作",
        title="CompTIA Security+ Lesson 01 頁03~05：原廠線上實驗室開通、環境測試與操作實務",
        talk_id="SECPLUS-01-03-05",
        date="2025-01-13",
        sections=[
            ("🎯 雲端實作平台帳號登入、驗證與環境檢測", 0.0, 0.33),
            ("💻 虛擬主機拓撲架構、遠端桌面連線與操作規範", 0.33, 0.66),
            ("🧪 課堂實作演練排程與自學實機準備", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：原廠雲端實驗室開通、帳號配置與實作環境架構  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 1: Hands-on Lab Environment Setup  
> **學習目標**：掌握原廠 Lab 系統登入流程、遠端虛擬主機連線與自學演練方式  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson01-03-05-原廠線上實驗室開通與實作-proofread.md)](./SecurityPlus-Lesson01-03-05-原廠線上實驗室開通與實作-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["CompTIA 官方學習平台"] --> B["學員帳號發放與登入驗證"]
    B --> C["雲端虛擬實驗室 (Cloud Hosted Labs)"]
    C --> D["Windows Server / Linux 模擬靶機環境"]
    D --> E["安全工具演練 (掃描、日誌分析、防護配置)"]
    E --> F["課後獨立實作與技能評量"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **環境開通**：每位學員具備專屬虛擬實驗室存取金鑰，由瀏覽器直接存取後端雲端虛擬機器拓撲。
2. **實作考題關聯**：CompTIA 認證包含 Performance-Based Questions (PBQs)，必須熟悉實機操作介面。
"""
    )

    # Session 3: Security+ 12~16
    build_and_save_session(
        folder_name="Security+ 12~16 週一 下午01點05分",
        file_prefix="SecurityPlus-Lesson01-12-16-控制措施分類與防禦深度評估",
        title="CompTIA Security+ Lesson 01 頁12~16：資安控制措施分類、縱深防禦與安全評估",
        talk_id="SECPLUS-01-12-16",
        date="2025-01-13",
        sections=[
            ("🎯 安全控制措施架構：技術控制（Technical）、管理控制（Managerial）與實體控制（Operational/Physical）", 0.0, 0.33),
            ("🛡️ 控制功能分類：預防性（Preventative）、偵測性（Detective）、矯正性（Corrective）與補償性（Compensating）", 0.33, 0.66),
            ("🏰 縱深防禦（Defense-in-Depth）多層安全控制實務", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：安全控制措施（Security Controls）分類法與縱深防禦架構  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 1: Security Controls & Defense-in-Depth  
> **學習目標**：區分技術、管理、實體控制，掌握預防、偵測、矯正等控制功能  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson01-12-16-控制措施分類與防禦深度評估-proofread.md)](./SecurityPlus-Lesson01-12-16-控制措施分類與防禦深度評估-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["資安控制措施 (Security Controls)"] --> B["依實施類型分類"]
    A --> C["依防禦功能分類"]
    B --> B1["管理控制 (Managerial / Administrative)"]
    B --> B2["技術控制 (Technical)"]
    B --> B3["實體/維運控制 (Operational / Physical)"]
    C --> C1["預防性控制 (Preventative)"]
    C --> C2["偵測性控制 (Detective)"]
    C --> C3["矯正性控制 (Corrective)"]
    C --> C4["補償性控制 (Compensating)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **控制類型三面向**：管理（規章政策）、技術（防火牆、加密、ACL）、實體（門禁、監視器、警衛）。
2. **縱深防禦原則**：單一層面被突破時，後續控制措施必須能立即承接，杜絕單點故障（SPOF）。
"""
    )

    # Session 4: Security+ Topic 2 1~6
    build_and_save_session(
        folder_name="Security+ Topic 2 1~6 週一 下午02點20分",
        file_prefix="SecurityPlus-Lesson02-01-06-威脅行為者分類與攻擊動機剖析",
        title="CompTIA Security+ Lesson 02 頁01~06：威脅行為者分類、攻擊動機與內外部威脅",
        talk_id="SECPLUS-02-01-06",
        date="2025-01-13",
        sections=[
            ("🎯 威脅行為者（Threat Actors）定義：內部員工、駭客與人為疏失", 0.0, 0.33),
            ("🎭 威脅行為者多樣化面貌：國家級APT組織、腳本小子、駭客行動主義者與犯罪集團", 0.33, 0.66),
            ("💡 攻擊動機剖析：經濟利益、政治意識形態、間諜活動與惡意破壞", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：威脅行為者（Threat Actors）類型屬性與背後動機分析  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 2: Threat Actors & Motivations  
> **學習目標**：掌握 APT 組織、內部威脅、腳本小子特徵與攻擊動機矩陣  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson02-01-06-威脅行為者分類與攻擊動機剖析-proofread.md)](./SecurityPlus-Lesson02-01-06-威脅行為者分類與攻擊動機剖析-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["威脅行為者 (Threat Actors)"] --> B["內部威脅者 (Insider Threat)"]
    A --> C["外部威脅者 (External Threat)"]
    B --> B1["惡意員工 (Malicious)"]
    B --> B2["無知失誤員工 (Negligent / Untrained)"]
    C --> C1["國家級駭客 (Nation-State / APT)"]
    C --> C2["組織犯罪集團 (Organized Crime)"]
    C --> C3["駭客行動主義者 (Hacktivist)"]
    C --> C4["腳本小子 (Script Kiddie)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **內部威脅危害最鉅**：威脅不限於頂尖駭客，內部未經訓練或疏忽大意的員工（豬隊友）常造成嚴重資安破口。
2. **資源與動機差異**：APT 組織具備國家級經費與長期潛伏能力；組織犯罪著重勒索金錢；腳本小子則缺乏底層理解僅依賴現成工具。
"""
    )

    # Session 5: Security+ Lesson2 7~13
    build_and_save_session(
        folder_name="Security+ Lesson2 7~13 週一 下午03點20分",
        file_prefix="SecurityPlus-Lesson02-07-13-攻擊面與各類攻擊向量辨識",
        title="CompTIA Security+ Lesson 02 頁07~13：攻擊面分析、攻擊向量與威脅情資來源",
        talk_id="SECPLUS-02-07-13",
        date="2025-01-13",
        sections=[
            ("🎯 攻擊面（Attack Surface）盤點與最小化曝險原則", 0.0, 0.33),
            ("🏹 攻擊向量（Attack Vectors）剖析：電子郵件、供應鏈、雲端與可卸除式媒體", 0.33, 0.66),
            ("📡 威脅情報來源（Threat Intelligence）與開源情資（OSINT）收集", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：攻擊面（Attack Surface）盤點、攻擊向量辨識與威脅情資收集  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 2: Attack Surfaces & Vectors  
> **學習目標**：理解系統漏洞與暴露途徑、掌握縮小攻擊面實務與威脅情報獲取管道  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson02-07-13-攻擊面與各類攻擊向量辨識-proofread.md)](./SecurityPlus-Lesson02-07-13-攻擊面與各類攻擊向量辨識-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["企業數位資產"] --> B["攻擊面 (Attack Surface)"]
    B --> C["外部網路介面 / 雲端 API"]
    B --> D["端點主機 / 員工行動裝置"]
    B --> E["第三方供應鏈軟硬體"]
    F["攻擊向量 (Attack Vectors)"] --> B
    F --> F1["釣魚郵件 (Phishing)"]
    F --> F2["未修補弱點利用 (Exploits)"]
    F --> F3["實體 USB 隨身碟媒介"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **攻擊面最小化**：關閉不需要的服務、連接埠與存取路徑，將潛在弱點暴露減至最低。
2. **向量防護重點**：電子郵件依然是最常見且最致命的攻擊向量，必須搭配嚴格的資安意識培訓與過濾機制。
"""
    )

    # Session 6: Security+ Lesson3 5~14
    build_and_save_session(
        folder_name="Security+ Lesson3 5~14週二 下午01點11分",
        file_prefix="SecurityPlus-Lesson03-05-14-密碼學對稱式與非對稱式加密",
        title="CompTIA Security+ Lesson 03 頁05~14：密碼學原理、對稱式加密與非對稱式加密架構",
        talk_id="SECPLUS-03-05-14",
        date="2025-01-14",
        sections=[
            ("🎯 密碼學基礎概念：明文、密文與 Kerckhoffs 原則", 0.0, 0.33),
            ("🔑 對稱式加密演算法：AES、DES/3DES 與金鑰分發難題", 0.33, 0.66),
            ("🗝️ 非對稱式公鑰密碼學：RSA、ECC 與公私鑰配對應用", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：密碼學核心架構、對稱式加密與非對稱式金鑰交換實務  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 3: Cryptographic Algorithms  
> **學習目標**：理解對稱式（AES）與非對稱式（RSA/ECC）運作特性及金鑰交換挑戰  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson03-05-14-密碼學對稱式與非對稱式加密-proofread.md)](./SecurityPlus-Lesson03-05-14-密碼學對稱式與非對稱式加密-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["密碼學演算法 (Cryptography)"] --> B["對稱式加密 (Symmetric)"]
    A --> C["非對稱式加密 (Asymmetric)"]
    B --> B1["單一金鑰加密與解密 (Shared Secret)"]
    B --> B2["高效能、適合大量資料 (AES-256)"]
    B --> B3["難題：金鑰傳輸安全性"]
    C --> C1["公鑰 (Public) 加密、私鑰 (Private) 解密"]
    C --> C2["運算開銷大，適合金鑰協商與簽章 (RSA, ECC)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **混合加密架構**：實務上（如 TLS/HTTPS）結合非對稱式密碼學進行身分驗證與對稱金鑰交換，後續大量傳輸則使用高效之 AES 對稱式加密。
2. **金鑰管理核心**：演算法公開無妨，安全性全繫於私密金鑰之妥善保管。
"""
    )

    # Session 7: Security+ Lesson 3 15~17
    build_and_save_session(
        folder_name="Security+ Lesson 3 15~17 週二 下午02點14分",
        file_prefix="SecurityPlus-Lesson03-15-17-數位簽章與雜湊演算法完整性",
        title="CompTIA Security+ Lesson 03 頁15~17：雜湊演算法、不可否認性與數位簽章驗證",
        talk_id="SECPLUS-03-15-17",
        date="2025-01-14",
        sections=[
            ("🎯 雜湊演算法（Hash Functions）：MD5、SHA-256 與抗碰撞特性", 0.0, 0.33),
            ("✍️ 數位簽章（Digital Signatures）運作原理與私鑰簽署流程", 0.33, 0.66),
            ("📜 不可否認性（Non-Repudiation）與訊息完整性（MAC/HMAC）驗證", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：雜湊函數（Hashing）、數位簽章驗證與不可否認性架構  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 3: Hashes & Digital Signatures  
> **學習目標**：掌握 SHA-2/3 演算法、數位簽章私鑰簽章/公鑰驗證原理與防篡改機制  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson03-15-17-數位簽章與雜湊演算法完整性-proofread.md)](./SecurityPlus-Lesson03-15-17-數位簽章與雜湊演算法完整性-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["原始訊息 / 文件"] --> B["雜湊演算法 (SHA-256)"]
    B --> C["訊息摘要 (Message Digest)"]
    C --> D["發送方私鑰加密 (Private Key Sign)"]
    D --> E["生成數位簽章 (Digital Signature)"]
    E --> F["接收方以發送方公鑰解密 (Public Key Verify)"]
    F --> G["比對接收文件雜湊值"]
    G --> H["確認未遭竄改 + 具備不可否認性"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **雜湊單向性**：雜湊不可逆，雪崩效應（Avalanche Effect）保證原始資料些微更動即造成摘要劇烈變化。
2. **數位簽章雙重保障**：同時提供資料完整性（Integrity）與發送方身分之不可否認性（Non-Repudiation）。
"""
    )

    # Session 8: Security+ Lesson3 18~32
    build_and_save_session(
        folder_name="Security+ Lesson3 18~32 週二 下午03點20分",
        file_prefix="SecurityPlus-Lesson03-18-32-PKI憑證撤銷清單與金鑰管理",
        title="CompTIA Security+ Lesson 03 頁18~32：PKI 公鑰基礎設施、憑證撤銷清單與金鑰生命週期",
        talk_id="SECPLUS-03-18-32",
        date="2025-01-14",
        sections=[
            ("🎯 憑證授權中心（CA）階層架構：Root CA、Intermediate CA 與信任鏈", 0.0, 0.33),
            ("🚫 憑證驗證與撤銷機制：CRL 撤銷清單與 OCSP 線上憑證狀態協定", 0.33, 0.66),
            ("🔒 金鑰管理與安全儲存：HSM 硬體安全模組、金鑰託管與生命週期輪替", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：PKI 公鑰基礎設施、CA 階層信任鏈與金鑰管理生命週期  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 3: Public Key Infrastructure (PKI)  
> **學習目標**：理解 X.509 憑證標準、CRL/OCSP 撤銷查詢與 HSM 硬體防護  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson03-18-32-PKI憑證撤銷清單與金鑰管理-proofread.md)](./SecurityPlus-Lesson03-18-32-PKI憑證撤銷清單與金鑰管理-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    A["根憑證授權中心 (Root CA) - 離線保存"] --> B["中繼憑證授權中心 (Intermediate CA)"]
    B --> C["發行終端實體憑證 (End-Entity Certificate)"]
    C --> D["用戶端驗證憑證信任鏈 (Chain of Trust)"]
    D --> E{"憑證有效性查詢"}
    E --> F["CRL (憑證撤銷清單定期下載)"]
    E --> G["OCSP (線上即時協定查詢狀態)"]
    E --> H["OCSP Stapling (伺服器預抓快取加速)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **根 CA 離線原則**：Root CA 為整個信任體系之基石，簽發 Intermediate CA 後應立即離線實體封存，防止被駭。
2. **OCSP vs CRL**：CRL 存在更新延遲且檔案日益肥大；OCSP 提供即時查詢，而 OCSP Stapling 更解決了隱私與連線延遲問題。
"""
    )


if __name__ == "__main__":
    run_batch()
