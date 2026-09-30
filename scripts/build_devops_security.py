#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build DevOps, Database Security, and CTF deliverables:
- DEVOPS-01: Ansible Agentless Architecture & Playbook Automation
- DB-SEC-01: PostgreSQL Replication Protocol Auth Bypass & Privilege Escalation
- SEC-CTF-01: CTF Image Steganography & OSINT Geolocation
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_undergrad_courses import clean_text, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2024-UndergraduateCourses"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_devops_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in DevOps and Security lectures."""
    replacements = [
        ("Endless 的架構", "Agentless (無代理) 架構"),
        ("搭個的底層", "Docker 底層"),
        ("duck 的主題", "Docker 主機"),
        ("fine tune", "微調 (Fine-tuning)"),
        ("明寫數", "隱寫術 (Steganography)"),
        ("T T F D N C T F U U 點", "CTF 競賽平台網址"),
        ("零三A A", "0x03AA"),
        ("零零D D", "0x00DD"),
        ("一零八後面的那四個百", "0x108 後面的 4 個 Bytes"),
        ("magic的時候", "Magic Number (魔術數字)"),
        ("南頭新月天空", "南投星月天空"),
        ("南都星月天空", "南投星月天空"),
        ("星月天空景觀餐廳", "星月天空景觀餐廳"),
        ("super user", "Superuser (超級使用者)"),
        ("login flag", "LOGIN 旗標"),
        ("pginit", "pg_init"),
        ("pgauthid", "pg_authid"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_devops_01():
    print("Building DEVOPS-01 (週二 15點05分)...")
    raw_path = RAW_DIR / "週二 15點05分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_devops_typos(raw)

    title = "DevOps 自動化維運實務 Lesson 01：Ansible 無代理架構、Playbook 宣告式部署與 Docker 容器整合"
    talk_id = "DEVOPS-01-ANSIBLE-AUTOMATION"
    event = "大學部系統維運與自動化實務課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 Ansible 四大核心優勢：開源生態、Agentless 無代理架構、YAML Playbook 與冪等性", sec1)
    builder.add_section("📊 實機部署展示與架構展望：Docker 容器環境初始化、Inventory 群組與 AI 指令碼輔助", sec2)
    builder.add_section("💼 授課教授講評指導：專案價值點提煉、AI 落地可靠度評估與課堂進度推進", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部系統維運與自動化實務課程"',
        'event: "大學部系統維運與自動化實務課程"\ndate: "2025-12-09"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "DevOps自動化維運-01-Ansible無代理架構與Playbook宣告式部署-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：Ansible 自動化組態管理、無代理架構（Agentless）、Playbook 語法、冪等性與容器化維運  
> **授課教授**：授課講師（系統架構授課教授）  
> **核心模組**：Ansible Architecture, Agentless SSH, Playbook YAML, Idempotency, Docker Deployment  
> **學習目標**：掌握 Ansible 基礎架構原理，理解宣告式語法與冪等性對大規模基礎架構維運（IaC）之關鍵價值  
> **關聯文件**：[📄 完整原話逐字稿 (DevOps自動化維運-01-Ansible無代理架構與Playbook宣告式部署-proofread.md)](./DevOps自動化維運-01-Ansible無代理架構與Playbook宣告式部署-proofread.md)

---

## 🏛️ Ansible 無代理 (Agentless) 自動化部署拓撲

```mermaid
flowchart TD
    ControlNode["Ansible 控制節點 (Control Node)<br/>安裝 Ansible, 存放 Inventory 與 Playbooks"]
    
    subgraph TargetHosts["受管節點叢集 (Managed Nodes / Target Hosts)"]
        Host1["Web Server 1<br/>(僅需 Python 與 SSH)"]
        Host2["Web Server 2<br/>(僅需 Python 與 SSH)"]
        Host3["Database Server<br/>(僅需 Python 與 SSH)"]
        DockerHost["Docker 容器主機<br/>(Container Runtime)"]
    end

    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> Host1
    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> Host2
    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> Host3
    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> DockerHost
```

---

## ⚙️ 冪等性 (Idempotency) 與宣告式狀態維護模型

```mermaid
flowchart LR
    Task["執行 Ansible Playbook 任務"]
    CheckState{"檢查目標主機目前狀態<br/>是否與 Playbook 定義一致?"}
    NoChange["狀態已符合 (OK)<br/>不做任何修改，系統保持原樣"]
    ApplyChange["狀態不符 (Changed)<br/>執行變更使其達到期望狀態"]

    Task --> CheckState
    CheckState -- "一致" --> NoChange
    CheckState -- "不一致" --> ApplyChange
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. Ansible 的四大核心技術特色
- **無代理架構 (Agentless)**：受管主機端完全不需要預先安裝專屬 Agent 或啟動背景守護程式（Daemon），僅需標準 OpenSSH 服務與 Python 直譯器即可受控。
- **宣告式 Playbook (YAML)**：以清晰結構化之 YAML 檔案描述基礎架構的「最終期望狀態（Desired State）」，而非傳統指令碼的程序式指令（Imperative Commands）。
- **冪等性 (Idempotency)**：重複執行相同的 Playbook 任意多次，系統狀態將始終保持一致且不會造成副作用或重複安裝錯誤。
- **豐富模組生態**：內建包含套件管理（apt/yum）、檔案模板（template/jinja2）、服務管理（systemd）、Docker/Kubernetes 等數千種官方模組。

### 2. 容器化環境與 Inventory 動態管理
- **Docker 整合**：透過 Ansible Docker 模組實現容器映像檔自動建置、環境變數注入與叢集服務編排。
- **AI 輔助維運指令碼生成評估**：小組專題探討利用本地大型語言模型生成自動化維運 YAML 指令碼，但需嚴防模型「幻覺（Hallucination）」所造成的無效指令或資安組態漏洞。
"""
    summary_file = OUT_DIR / "DevOps自動化維運-01-Ansible無代理架構與Playbook宣告式部署-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_db_sec_01():
    print("Building DB-SEC-01 (週一 20點00分)...")
    raw_path = RAW_DIR / "週一 20點00分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_devops_typos(raw)

    title = "資料庫資安實務 Lesson 01：PostgreSQL 抄寫協議認證繞過與特權提升漏洞解析"
    talk_id = "DB-SEC-01-POSTGRES-PRIVILEGE-ESCALATION"
    event = "大學部資訊安全專題研究課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.50)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:])

    builder.add_section("🎯 PostgreSQL 主從複寫架構：Replication 協議帳號與 C Interface 安全檢查缺失", sec1)
    builder.add_section("📊 提權利用鏈與持久化機制：pg_authid 修改、超級使用者維持與防禦建議", sec2)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部資訊安全專題研究課程"',
        'event: "大學部資訊安全專題研究課程"\ndate: "2026-09-14"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "資料庫資安-01-PostgreSQL抄寫協議認證繞過與特權提升漏洞解析-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：PostgreSQL 歷史漏洞成因剖析、Replication 複寫協議認證缺陷、C Interface 權限檢查缺失與提權利用鏈  
> **授課教授**：授課講師（資訊安全專題教授）  
> **核心模組**：PostgreSQL Replication, pg_authid, Privilege Escalation, C Interface Security, Persistence  
> **學習目標**：理解資料庫複寫協議之底層實作盲點，掌握提權攻擊者如何竄改系統型錄維持 Superuser 特權並提出防範方案  
> **關聯文件**：[📄 完整原話逐字稿 (資料庫資安-01-PostgreSQL抄寫協議認證繞過與特權提升漏洞解析-proofread.md)](./資料庫資安-01-PostgreSQL抄寫協議認證繞過與特權提升漏洞解析-proofread.md)

---

## 🏛️ PostgreSQL 複寫協議提權攻擊利用鏈

```mermaid
flowchart TD
    Attacker["低權限攻擊者 (具備 Replication 角色)"]
    Connect["連線至 PostgreSQL Replication Protocol"]
    FlagCheck["登入檢查 (LOGIN 旗標通過)"]
    C_Interface["進入 C Interface 底層調用層<br/>(缺失權限存取控制安全檢查)"]
    ExecInit["執行內部常式 pg_init<br/>切換為內部信任執行層"]
    TamperAuth["直接存取並竄改系統目錄 pg_authid<br/>將帳號旗標修改為 rolsuper = true"]
    Escalate["成功取得 Superuser 超級管理員特權<br/>並建立多重持久化後門機制"]

    Attacker --> Connect
    Connect --> FlagCheck
    FlagCheck --> C_Interface
    C_Interface --> ExecInit
    ExecInit --> TamperAuth
    TamperAuth --> Escalate
```

---

## 🛡️ 資料庫權限檢查深度防禦模型

```mermaid
flowchart LR
    Client["客戶端 SQL / 協議請求"] --> Parser["語法解析器 (Parser)"]
    Parser --> PrivilegeCheck["標準權限檢查機制 (ACL Check)"]
    PrivilegeCheck --> C_Engine["C Interface 核心引擎"]
    C_Engine --> HookCheck["加強防禦：底層二次權限校驗 (Internal Check)"]
    HookCheck --> Storage["系統型錄與儲存引擎 (pg_authid)"]
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 漏洞成因與歷史背景
- **潛伏十二年歷史缺陷**：PostgreSQL 為了支援主從庫同步、異地備份與 CDC（Change Data Capture）資料流，提供了一組 Replication 協議。
- **安全檢查繞過**：正常使用者透過 SQL 查詢時會受到嚴格的存取控制列表（ACL）檢查；但當使用帶有 Replication 屬性的帳號連線並通過 LOGIN 旗標驗證後，請求進入 C Interface 底層層級，缺乏後續操作權限檢查。

### 2. 提權至 Superuser 的攻擊鏈
- **`pg_init` 內部切換**：攻擊者利用複寫協議介面執行初始化常式，將進程權限 context 切換至內部信任層。
- **竄改 `pg_authid`**：直接修改記錄資料庫使用者身份與權限的系統型錄 `pg_authid`，將攻擊者帳號標記為 `rolsuper = true`，完成縱向權限提升（Vertical Privilege Escalation）。
- **持久化維護**：攻擊者通常會佈署多種後門持久化機制，即便管理員事後修復部分設定，仍可持續保有超級使用者存取。
"""
    summary_file = OUT_DIR / "資料庫資安-01-PostgreSQL抄寫協議認證繞過與特權提升漏洞解析-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_ctf_01():
    print("Building SEC-CTF-01 (週三 19點18分)...")
    raw_path = RAW_DIR / "週三 19點18分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_devops_typos(raw)

    title = "資安實戰 Lesson 01：CTF 圖片隱寫術分析、十六進位結構竄改與 OSINT 地理定位解題實務"
    talk_id = "SEC-CTF-01-STEGANOGRAPHY-OSINT"
    event = "大學部資訊安全競賽培訓課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 圖片隱寫術導論：EXIF 詮釋資料、GPS 地理標籤與十六進位檔案標頭 Magic Number", sec1)
    builder.add_section("📊 影像結構深度竄改：PNG/JPEG 尺寸高度位元組修正與尾端附加隱藏檔案", sec2)
    builder.add_section("💼 OSINT 開源情報實戰：以圖搜圖、建築外觀特徵比對與精確座標判定解題", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部資訊安全競賽培訓課程"',
        'event: "大學部資訊安全競賽培訓課程"\ndate: "2026-04-08"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "資安實戰-01-CTF圖片隱寫術分析與OSINT地理定位解題實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：CTF 搶旗賽資安實務、數位隱寫術（Steganography）、HEX 檔案結構分析、EXIF 詮釋資料與 OSINT 開源情報地理定位  
> **授課教授**：授課講師（資安戰隊指導教練）  
> **核心模組**：CTF Misc, Steganography, EXIF Metadata, Hex Editing, OSINT Geolocation, Google Lens  
> **學習目標**：掌握數位圖片隱寫偵測與還原技術（修改尺寸、附加封包），熟練運用開源情報（OSINT）比對地理座標解出競賽 Flag  
> **關聯文件**：[📄 完整原話逐字稿 (資安實戰-01-CTF圖片隱寫術分析與OSINT地理定位解題實務-proofread.md)](./資安實戰-01-CTF圖片隱寫術分析與OSINT地理定位解題實務-proofread.md)

---

## 🏛️ CTF Misc 圖片隱寫與開源情報分析工作流程

```mermaid
flowchart TD
    Challenge["取得 CTF 題目目標圖片"]
    
    subgraph Step1["階段一：詮釋資料分析 (Metadata Analysis)"]
        ExifTool["執行 exiftool 檢查 EXIF 資訊"]
        GPS["檢查是否包含 GPS 經緯度座標、相機型號與拍攝時間"]
    end

    subgraph Step2["階段二：十六進位結構檢查 (Hex Inspection)"]
        Hex["檢查 Magic Number (JPEG: FFD8FFE0, PNG: 89504E47)"]
        IHDR["檢查 PNG IHDR 區塊高度與寬度 Bytes (修復尺寸顯示隱藏資訊)"]
        Trailer["檢查檔案結尾後是否附加壓縮包 (PK / Zip 隱寫)"]
    end

    subgraph Step3["階段三：開源情報蒐集 (OSINT Geolocation)"]
        Crop["框選特徵建築物或地標進行以圖搜圖"]
        MapSearch["Google Maps / 衛星地圖街景實景對照"]
        Pinpoint["鎖定精確拍攝位置 (如星月天空景觀餐廳停車場) 提交 Flag"]
    end

    Challenge --> Step1
    Challenge --> Step2
    Step1 --> Step3
    Step2 --> Step3
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 圖片檔案結構與隱寫術常見手法
- **EXIF 詮釋資料抽取**：相機或智慧型手機拍照時會自動將裝置型號、光圈快門與 GPS 經緯度直接嵌入圖片檔案標頭。隱寫題目中常隱藏 Flag 或提示訊息。
- **IHDR 尺寸位元組竄改 (PNG Chunk Tampering)**：
  - PNG 檔案在 `IHDR` Chunk 中定義了圖片寬度（4 Bytes）與高度（4 Bytes）。
  - 出題者常將高度修改為較小值，使圖片顯示時隱藏下方帶有 Flag 的區域。解題時透過十六進位編輯器（如 010 Editor、HxD）將高度 Bytes 還原或改大，即可重新顯示被遮蔽的內容。
- **檔案尾端夾帶 (File Carving / Append)**：在 JPEG 檔案結尾標記 `FF D9` 之後附加壓縮檔（`50 4B 03 04`），可使用 `binwalk` 或 `foremost` 自動抽離被隱藏之資料檔案。

### 2. OSINT (Open Source Intelligence) 地理定位實戰技術
- **圖像局部反搜**：當全圖搜尋無法精確比對時，使用裁切工具鎖定「非自然景觀之獨特人造建物、招牌或欄杆裝飾」，利用 Google Lens 等逆向圖庫比對出目標景點（案例：南投星月天空景觀餐廳）。
- **衛星地圖視角校正與精確定位**：比對照片拍攝視角、陰影方位與停車場地坪標線，判定拍攝者實際站立位置，以符合 CTF 題目對特定經緯度或地標名稱之檢驗要求。
"""
    summary_file = OUT_DIR / "資安實戰-01-CTF圖片隱寫術分析與OSINT地理定位解題實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_devops_01()
    build_db_sec_01()
    build_ctf_01()
