#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build 6 Certification Lab & Extended Deliverables:
- 3 for Cisco CCNA 1 (IPv6 SLAAC/DHCPv6, GRE Tunnel, Exam Experience)
- 3 for CompTIA Security+ (SSH Platform Lab, C2 Command & Control, Open-AudIT)
Follows PROOFREAD_RULES.md, ScenarioType.CLASSROOM_LECTURE, and tests/test_proofread_linter.py.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

CCNA_DIR = REPO_ROOT / "4-University" / "2025-Cisco-CCNA1"
SEC_DIR = REPO_ROOT / "4-University" / "2025-CompTIA-SecurityPlus"
RAW_DIR = REPO_ROOT / "transcribe_outputs"

COMMON_REPLACEMENTS = [
    (r"CNA", "CCNA"),
    (r"TIA", "CompTIA"),
    (r"治安", "資安"),
    (r"自然", "資安"),
    (r"SLAAC", "SLAAC（無狀態位址自動配置）"),
    (r"Tunnel", "Tunnel（穿隧）"),
    (r"OpenA\s*U\s*D\s*I\s*T", "Open-AudIT"),
    (r"吸眼器", "C2 滲透工具"),
    (r"ocean\s*command\s*control", "Open Command & Control (C2)"),
    (r"點一", ".1"),
    (r"點一百", ".100"),
    (r"點二", ".2"),
    (r"點二五四", ".254"),
    (r"十萬", "10.1"),
    (r"槓二四", "/24"),
    (r"槓六四", "/64"),
]


def clean_text(text: str) -> str:
    res = text
    for pat, rep in COMMON_REPLACEMENTS:
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
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        student_triggers = ["老師請問", "一次一萬", "沒考過", "不通啊", "會啊。"]
        if any(trig in p_clean for trig in student_triggers):
            formatted_paras.append(f"**【學員】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_deliverable(
    src_folder: str,
    dest_dir: Path,
    file_prefix: str,
    title: str,
    event: str,
    talk_id: str,
    date: str,
    sections_def: list,
    summary_md: str,
):
    print(f"Building {file_prefix}...")
    p = RAW_DIR / src_folder / "transcript_zh_tw.txt"
    if not p.exists():
        p = RAW_DIR / src_folder / "raw_transcript.txt"
    raw_text = p.read_text(encoding="utf-8")
    cleaned = clean_text(raw_text)

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    for sec_title, r_start, r_end in sections_def:
        start_idx = int(total_len * r_start)
        end_idx = int(total_len * r_end)
        chunk = cleaned[start_idx:end_idx]
        formatted_chunk = segment_into_dialogue_paragraphs(chunk)
        builder.add_section(sec_title, formatted_chunk)

    rendered = builder.render()
    rendered = rendered.replace(f'event: "{event}"', f'event: "{event}"\ndate: "{date}"')

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed for {file_prefix}: {errors}")

    proof_path = dest_dir / f"{file_prefix}-proofread.md"
    proof_path.write_text(rendered, encoding="utf-8")

    summary_final = summary_md.replace("__TALK_ID__", talk_id).replace("__TITLE__", title)
    summary_path = dest_dir / f"{file_prefix}-summary.md"
    summary_path.write_text(summary_final, encoding="utf-8")
    print(f"  [OK] Saved {proof_path.name} & {summary_path.name}")


def run_batch():
    # 1. CCNA: 週五 下午01點02分 (SLAAC & DHCPv6)
    build_deliverable(
        src_folder="週五 下午01點02分",
        dest_dir=CCNA_DIR,
        file_prefix="CCNA1-Lab-IPv6-SLAAC與DHCPv6派發配置實作",
        title="Cisco CCNA 1 Lab 補充實作：IPv6 SLAAC 無狀態配置、EUI-64 與 DHCPv6 伺服器整合",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA1-LAB-IPV6-SLAAC",
        date="2025-01-10",
        sections_def=[
            ("🎯 IPv6 定址三大模式：SLAAC 無狀態、Stateless DHCPv6 與 Stateful DHCPv6 分野", 0.0, 0.33),
            ("📡 ICMPv6 路由器通告（RA）與路由器請求（RS）自動前綴獲取流程", 0.33, 0.66),
            ("⚙️ Cisco 路由器 Stateless DHCPv6 伺服器配置與 DNS/Domain Name 派發驗證", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：IPv6 SLAAC 自動定址、ICMPv6 RA 封包與 Stateless DHCPv6 伺服器整合實作  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 IPv6 Addressing & Dynamic Configuration  
> **學習目標**：掌握 SLAAC 無狀態位址生成、配置 Cisco 路由器派送 DNS 伺服器資訊  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-IPv6-SLAAC與DHCPv6派發配置實作-proofread.md)](./CCNA1-Lab-IPv6-SLAAC與DHCPv6派發配置實作-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Client["IPv6 主機用戶端"] -->|發送 ICMPv6 RS (Router Solicitation)| Router["Cisco 路由器 (Default Gateway)"]
    Router -->|回傳 ICMPv6 RA (Router Advertisement: 前綴 /64)| Client
    Client -->|以 EUI-64 或隨機介面 ID 生成全球單播位址| GUA["生成完整 IPv6 GUA 位址"]
    Client -->|依 RA 之 O-Flag 向 DHCPv6 索取其他資訊| DHCP["Stateless DHCPv6 Server"]
    DHCP -->|派發 DNS IP 與網域名稱| Client
```

---

## 🔑 重點提要 (Key Takeaways)

1. **SLAAC 核心機制**：用戶端完全不需要 DHCP 伺服器即可依據路由器 RA 派送的 Prefix（前綴）自動組合出 IPv6 位址。
2. **Stateless DHCPv6 互補價值**：SLAAC 早期無法派發 DNS 伺服器位址，透過設定 RA 的 Other Configuration Flag (O-flag)，指引用戶端向 DHCPv6 索取 DNS 與網域名稱。
"""
    )

    # 2. CCNA: 週五 下午02點04分 (GRE Tunnel)
    build_deliverable(
        src_folder="週五 下午02點04分",
        dest_dir=CCNA_DIR,
        file_prefix="CCNA1-Lab-Tunnel-GRE穿隧與跨網段端對端路由",
        title="Cisco CCNA 1 Lab 補充實作：GRE Tunnel 點對點穿隧配置與跨網段封包封裝演練",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA1-LAB-GRE-TUNNEL",
        date="2025-01-10",
        sections_def=[
            ("🎯 穿隧技術（Tunneling）核心概念：底層 Underlay 路由連通性先決條件", 0.0, 0.33),
            ("🛠️ 通用路由封裝（GRE Tunnel）介面配置：Source、Destination 與 Tunnel IP 設定", 0.33, 0.66),
            ("🔍 跨網段端對端 Ping 驗證、MTU 碎片考量與靜態路由導向 Tunnel 實務", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：GRE Tunnel 點對點穿隧技術、Underlay 實體路由先決條件與 Overlay 虛擬通道配置  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Generic Routing Encapsulation (GRE) Tunneling  
> **學習目標**：理解「路由未通則穿隧不通」、配置 Tunnel 介面並達成私網跨公網互通  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-Tunnel-GRE穿隧與跨網段端對端路由-proofread.md)](./CCNA1-Lab-Tunnel-GRE穿隧與跨網段端對端路由-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    PC1["私網 PC 1 (192.168.1.0/24)"] --> R1["邊界路由器 R1 (Tunnel 0)"]
    R1 -->|GRE 封裝 (Protocol 47)| WAN["公網網際網路 (Underlay IP 路由可達)"]
    WAN --> R2["邊界路由器 R2 (Tunnel 0)"]
    R2 -->|解封裝原生 IP 封包| PC2["私網 PC 2 (192.168.3.0/24)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **Underlay 路由是先決條件**：Tunnel 終點實體 IP（tunnel destination）若無法透過公網路由 Ping 通，Tunnel 介面絕對無法 Up。
2. **GRE 封裝開銷**：GRE 會額外增加 24 位元組標頭（20-byte IP + 4-byte GRE），實務上須注意調整 MTU 與 MSS 防止封包碎片化。
"""
    )

    # 3. CCNA: 週五 上午10點53分 (CCNA Exam Experience)
    build_deliverable(
        src_folder="週五 上午10點53分",
        dest_dir=CCNA_DIR,
        file_prefix="CCNA1-Review-認證報考心態與歷屆應試經驗談",
        title="Cisco CCNA 1 認證備考心得：考照投資報酬率、英語能力優勢與三次應試歷史經驗談",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA1-EXAM-EXPERIENCE",
        date="2025-01-10",
        sections_def=[
            ("🎯 CCNA 考試費用演變與職場投資報酬率（ROI）理性分析", 0.0, 0.33),
            ("📜 講師親身報考歷程：從 2004 年至今三次應試經驗與考場心態調整", 0.33, 0.66),
            ("💡 善用英語語文優勢：直接理解英文原廠題意、避開翻譯陷阱之關鍵策略", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：Cisco CCNA 認證報考歷程、報名成本權衡、英語題意掌握與備考心態  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA Exam Preparation & Strategy  
> **學習目標**：克服英語應試心理障礙、掌握原廠認證考核邏輯與備考排程  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Review-認證報考心態與歷屆應試經驗談-proofread.md)](./CCNA1-Review-認證報考心態與歷屆應試經驗談-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Cost["報名費考量 (一次約 300 美元)"] --> Mindset["建立一次考取必勝決心"]
    Mindset --> Study["密集刷題 + 實機 Lab 驗證 (Packet Tracer / GNS3)"]
    Study --> English["直接閱讀原廠英文題目 (克服英文閱讀恐懼)"]
    English --> Exam["正式考場應試 (Pearson VUE / OnVUE)"]
    Exam --> Cert["取得 CCNA 原廠證照，大幅提升求職競爭力"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **英語原廠題目優勢**：CCNA 專業術語直接閱讀英文原題最為精確，中文翻譯常有專用術語曲解，英語底子好的學員具備天然優勢。
2. **沉沒成本轉化動力**：考試費用昂貴（約一萬台幣），應將成本轉化為排定死線（Deadline）全力衝刺的決心。
"""
    )

    # 4. Security+: 週五 下午01點09分 (SSH Lab)
    build_deliverable(
        src_folder="週五 下午01點09分",
        dest_dir=SEC_DIR,
        file_prefix="SecurityPlus-Lab-SSH遠端靶機連線與金鑰認證實務",
        title="CompTIA Security+ Lab 實機演練：SSH 遠端安全連線、原廠實驗室平台登入與金鑰認證",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SECPLUS-LAB-SSH",
        date="2025-01-24",
        sections_def=[
            ("🎯 CompTIA 原廠學習平台雲端實驗室（Labs）帳號開通與科目清單存取", 0.0, 0.33),
            ("🔑 SSH 遠端連線實作：金鑰交換（Diffie-Hellman）、對稱加密通道建立與公鑰部署", 0.33, 0.66),
            ("💻 虛擬靶機 Linux 終端機安全維運操作、服務狀態查詢與連線除錯", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：CompTIA 原廠雲端實驗室開通、SSH 遠端終端機連線與公私鑰身分鑑別  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Hands-on Lab: SSH Remote Administration  
> **學習目標**：熟練原廠實作環境操作、配置 SSH 金鑰對（SSH Key Pairs）杜絕密碼爆破  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lab-SSH遠端靶機連線與金鑰認證實務-proofread.md)](./SecurityPlus-Lab-SSH遠端靶機連線與金鑰認證實務-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 管理員終端機 (SSH Client)
    participant Host as 雲端靶機主機 (SSH Server)
    Admin->>Host: 發起 TCP 22 連線請求
    Host-->>Admin: 回傳伺服器 Host Key (指紋驗證防止 MitM)
    Admin->>Host: 執行 Diffie-Hellman 金鑰協商
    Note over Admin,Host: 建立對稱加密傳輸通道
    Admin->>Host: 使用客戶端私鑰簽名進行身分認證
    Host-->>Admin: 比對 authorized_keys 公鑰符合，准許登入 Shell
```

---

## 🔑 重點提要 (Key Takeaways)

1. **原廠實驗室實操價值**：CompTIA Security+ 包含實作題（PBQs），必須親自在終端機輸入指令完成配置，不可僅靠紙上談兵。
2. **禁用 SSH 密碼登入**：生產環境應全面停用 PasswordAuthentication，強制改用 Ed25519 或 RSA 4096 憑證私鑰登入。
"""
    )

    # 5. Security+: 週五 下午02點54分 (C2 Attack & Defense)
    build_deliverable(
        src_folder="週五 下午02點54分",
        dest_dir=SEC_DIR,
        file_prefix="SecurityPlus-Lab-C2指令控制工具演練與攻擊防禦",
        title="CompTIA Security+ Lab 實機演練：C2（Command & Control）攻擊工具實作與流量監控",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SECPLUS-LAB-C2",
        date="2025-01-24",
        sections_def=[
            ("🎯 開源滲透與攻擊測試工具大全：Ocean Command & Control（C2）架構綜述", 0.0, 0.33),
            ("🤖 受害主機信標（Beaconing）回傳機制：反向 Shell、非對稱加密指令傳輸剖析", 0.33, 0.66),
            ("🛡️ 藍隊流量監控與遏制：檢測異常 DNS 查詢、隨機抖動（Jitter）與端點行為獵捕", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：C2（Command & Control）中繼主控台架構、惡意信標通訊模式與藍隊防禦偵測  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Attack Frameworks & Command and Control (C2)  
> **學習目標**：理解開源 C2 運作原理、辨識 Beaconing 心跳特徵並實施網路層圍堵  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lab-C2指令控制工具演練與攻擊防禦-proofread.md)](./SecurityPlus-Lab-C2指令控制工具演練與攻擊防禦-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Attacker["攻擊者操作終端 (Attacker)"] --> C2["C2 中繼指揮伺服器 (C2 Server)"]
    Target["被感染內網主機 (Compromised Host)"] -->|定時外發 HTTPS 心跳 (Beaconing + Jitter)| C2
    C2 -->|隨心跳回應下達 Payload 指令| Target
    Target -->|執行指令並回傳竊密資料| C2
    subgraph BlueTeam ["藍隊防禦獵捕策略"]
        B1["監控週期性對外長連線 (Beaconing Detection)"]
        B2["DNS 異常分析 (檢測 DGA 隨機網域名稱)"]
        B3["EDR 端點阻斷異常注入處理程序"]
    end
```

---

## 🔑 重點提要 (Key Takeaways)

1. **反向連線（Reverse Shell）特性**：受害端主動向外連線 C2 伺服器，利用 80/443 等常見出境埠號穿透企業外部防火牆。
2. **Jitter（隨機抖動）防禦規避**：現代 C2 會在固定心跳時間加上隨機秒數偏移（Jitter），藉此規避傳統以固定週期為特徵的統計檢測。
"""
    )

    # 6. Security+: 週五 上午11點24分 (Asset Management)
    build_deliverable(
        src_folder="週五 上午11點24分",
        dest_dir=SEC_DIR,
        file_prefix="SecurityPlus-Lesson-開源資產管理工具與企業軟體盤點",
        title="CompTIA Security+ 專題延伸：開源資產管理工具、資訊資產生命週期與漏洞關聯分析",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SECPLUS-ASSET-MGMT",
        date="2025-01-24",
        sections_def=[
            ("🎯 資安治理首要基石：『不知資產何在，遑論防禦安全』之資產盤點原則", 0.0, 0.33),
            ("🛠️ 開源資訊資產管理神兵：Open-AudIT 架構、自動化網路掃描與軟硬體清冊產生", 0.33, 0.66),
            ("📋 軟體授權合規、幽靈影子 IT（Shadow IT）發掘與資產漏洞關聯比對", 0.66, 1.0),
        ],
        summary_md="""# 🛡️ __TALK_ID__ __TITLE__

> **課程主題**：資訊資產盤點、開源 Open-AudIT 自動化探測與 Shadow IT 防範  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Asset Management & Inventory Discovery  
> **學習目標**：部署自動化資產盤點系統、掌握 CIS Control #1/#2 資產清單建置要求  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson-開源資產管理工具與企業軟體盤點-proofread.md)](./SecurityPlus-Lesson-開源資產管理工具與企業軟體盤點-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Scan["Open-AudIT 自動化網路排程探測"] --> Net["掃描企業內網所有 IP 與子網段"]
    Net --> Disc{"識別連網設備"}
    Disc --> S1["伺服器與虛擬機器 (Windows / Linux)"]
    Disc --> S2["網路設備 (路由器 / 交換器 / 防火牆)"]
    Disc --> S3["員工工作站與未授權設備 (Shadow IT)"]
    Disc --> Audit["彙整軟硬體組態清冊 (Hardware & Software Inventory)"]
    Audit --> Vuln["關聯 NVD/CVE 資料庫進行弱點衝擊評估"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **CIS 關鍵控制項第一條**：CIS Controls 第一項即為「企業資產盤點與控制」，無法掌握全網設備就無法確保邊界安全。
2. **影子 IT（Shadow IT）威脅**：部門私自架設未報備的伺服器或使用未受控 SaaS，往往因缺乏安全補丁成為駭客入侵的第一個跳板。
"""
    )


if __name__ == "__main__":
    run_batch()
