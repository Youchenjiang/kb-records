#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Certification Sprint deliverables:
- Cisco CCNA1: NAT & PAT Address Translation Configuration
- CompTIA Security+: Network Services Security, DNS, Cookies, and Sandbox Analysis
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_undergrad_courses import clean_text, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_cert_sprint_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in Certification Sprint lectures."""
    replacements = [
        ("BCL", "ACL (存取控制清單)"),
        ("應賽介面", "Inside (內部) 介面"),
        ("inside 介面", "Inside (內部) 介面"),
        ("outside 的介面", "Outside (外部) 介面"),
        ("醫生類", "Ethernet (乙太網路)"),
        ("Siri", "Serial (序列埠)"),
        ("S零零零", "Serial 0/0/0"),
        ("零一零", "Serial 0/1/0"),
        ("拼多少點二", "Ping 66.66.1.2"),
        ("六十六點六十六點一點二", "66.66.1.2"),
        ("十點一點一點一", "10.1.1.1"),
        ("拼點二的", "Ping 66.66.1.2"),
        ("拼點三的", "Ping 66.66.1.3"),
        ("NAT 的 table", "NAT 轉換表 (NAT Table)"),
        ("秒秀", "show ip nat translations"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_ccna_sprint():
    print("Building CCNA Sprint NAT/PAT (2025年01月08日 下午01點02分)...")
    out_dir = REPO_ROOT / "4-University" / "2025-Cisco-CCNA1"
    raw_path = RAW_DIR / "2025年01月08日 下午01點02分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_cert_sprint_typos(raw)

    title = "Cisco CCNA 1 認證衝刺：靜態 NAT、動態 NAT 與 PAT 連接埠位址轉換配置實務"
    talk_id = "CCNA-SPRINT-NAT-PAT"
    event = "Cisco CCNA 1 認證培訓課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.45)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:])

    builder.add_section("🎯 NAT 核心架構：靜態 NAT、動態 NAT、PAT 原理與邊界路由器介面宣告", sec1)
    builder.add_section("📊 實機測試與轉換表驗證：流量觸發、Ping 測試與 show ip nat translations 條目解析", sec2)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "Cisco CCNA 1 認證培訓課程"',
        'event: "Cisco CCNA 1 認證培訓課程"\ndate: "2025-01-08"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = out_dir / "CCNA1-認證衝刺-靜態動態NAT與PAT位址轉換實務配置-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：網路位址轉換（NAT）、連接埠位址轉換（PAT）、靜態 vs. 動態 NAT、邊界路由器介面宣告與 NAT Table 檢查  
> **授課教授**：授課講師（Cisco 認證原廠講師）  
> **核心模組**：Static NAT, Dynamic NAT, PAT (NAT Overload), ip nat inside/outside, show ip nat translations  
> **學習目標**：精熟 Cisco 路由器之 NAT 核心指令與運作原理，正確配置 Inside/Outside 介面並透過流量觸發驗證轉譯表  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-認證衝刺-靜態動態NAT與PAT位址轉換實務配置-proofread.md)](./CCNA1-認證衝刺-靜態動態NAT與PAT位址轉換實務配置-proofread.md)

---

## 🏛️ NAT / PAT 運作模型與位址映射拓撲

```mermaid
flowchart LR
    subgraph InsideNetwork["內部私有網路 (Inside Local)"]
        PC1["PC 1: 10.1.1.1"]
        PC2["PC 2: 10.1.1.2"]
    end

    subgraph BorderRouter["邊界路由器 (Border Router)"]
        IntInside["Inside 介面<br/>ip nat inside"]
        NAT_Engine["NAT/PAT 轉譯引擎<br/>維護 NAT Table"]
        IntOutside["Outside 介面<br/>ip nat outside"]
    end

    subgraph PublicInternet["外部網際網路 (Inside Global)"]
        Web["外部伺服器: 66.66.1.2"]
    end

    PC1 --> IntInside
    PC2 --> IntInside
    IntInside --> NAT_Engine
    NAT_Engine --> IntOutside
    IntOutside -- "公有 IP: 66.66.1.1:Port" --> Web
```

---

## 📋 三種 NAT 轉換模式對照表

| NAT 類型 | 轉換對應關係 | 公有 IP 需求 | 典型應用場景 |
| :--- | :--- | :--- | :--- |
| **靜態 NAT (Static NAT)** | 1 對 1 固定映射 | 1 個私網對應 1 個公網 | 內部 Web/Mail 伺服器對外公開服務 |
| **動態 NAT (Dynamic NAT)** | 1 對 1 動態共享池 | 依池內公有 IP 數量決定並發數 | 內部主機有限度訪問外網 |
| **PAT (NAT Overload)** | 多對 1 (以連接埠區分) | 單一或極少數公有 IP 支援數萬連線 | 企業與家庭最普遍之連網模式 |

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 介面角色宣告 (Interface Configuration)
- **`ip nat inside`**：定義私有網路入口介面（如 Ethernet 0/0）。
- **`ip nat outside`**：定義連接網際網路之公網介面（如 Serial 0/0/0 或 Ethernet 0/1）。
- **注意**：介面宣告錯誤將導致轉譯引擎無法識別流量流向，造成封包直接被丟棄。

### 2. 驗證與障礙排除
- **動態條目生成**：動態 NAT 與 PAT 僅在內部主機主動發起外向流量（如 Ping 或 HTTP 請求）時，才會在轉譯表中建立動態映射紀錄。
- **檢查指令**：
  ```bash
  Router# show ip nat translations
  Router# show ip nat statistics
  Router# clear ip nat translation *
  ```
"""
    summary_file = out_dir / "CCNA1-認證衝刺-靜態動態NAT與PAT位址轉換實務配置-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_secplus_sprint():
    print("Building Security+ Sprint (週二 上午11點11分)...")
    out_dir = REPO_ROOT / "4-University" / "2025-CompTIA-SecurityPlus"
    raw_path = RAW_DIR / "週二 上午11點11分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_cert_sprint_typos(raw)

    title = "CompTIA Security+ 考前衝刺：網路服務安全、DNS 防護、Cookie 機制與雲端沙箱分析"
    talk_id = "SECPLUS-SPRINT-NETSERVICES-SANDBOX"
    event = "CompTIA Security+ 國際資安認證培訓"

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

    builder.add_section("🎯 網路服務掃描與考題場景：服務通訊協定、攻擊向量識別與解題關鍵", sec1)
    builder.add_section("📊 DNS 安全與 Web 狀態管理：DNSSEC 數位簽章、HTTP 無狀態性與 Cookie 禮物比喻", sec2)
    builder.add_section("💼 惡意程式沙箱動態分析：虛擬機器隔離、雲端 Sandbox 爆破與安全防禦決策", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "CompTIA Security+ 國際資安認證培訓"',
        'event: "CompTIA Security+ 國際資安認證培訓"\ndate: "2025-01-14"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = out_dir / "SecurityPlus-重點衝刺-網路服務安全DNS與雲端沙箱分析-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：CompTIA Security+ 核心考點衝刺、網路服務弱點掃描、DNS 安全防護、HTTP Cookie 狀態維護與惡意軟體沙箱動態分析  
> **授課教授**：授課講師（資安認證原廠講師）  
> **核心模組**：Network Services Security, DNSSEC, HTTP Stateless, Session Cookies, Dynamic Sandbox Analysis  
> **學習目標**：掌握網路服務通訊安全之核心考題解題要領，深入理解 Cookie 維持無狀態連線機制與沙箱隔離引爆惡意程式之原則  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-重點衝刺-網路服務安全DNS與雲端沙箱分析-proofread.md)](./SecurityPlus-重點衝刺-網路服務安全DNS與雲端沙箱分析-proofread.md)

---

## 🏛️ HTTP 無狀態性 (Stateless) 與 Cookie 會話維護

```mermaid
flowchart TD
    Client["客戶端瀏覽器 (Client)"]
    Server["Web 伺服器 (Server)"]

    Req1["1. 初次請求 (無 Cookie)"] --> Server
    Server --> Resp1["2. 回應內容 + Set-Cookie: session_id=XYZ<br/>（伺服器發放識別證/禮物）"]
    Resp1 --> Client
    Client --> Req2["3. 後續連線請求 + Cookie: session_id=XYZ<br/>（客戶端攜帶禮物驗證身份）"]
    Req2 --> Server
    Server --> Resp2["4. 識別出登入狀態，回應用戶個人化數據"]
```

---

## 🔬 惡意程式沙箱 (Sandbox) 動態引爆分析流程

```mermaid
flowchart LR
    Malware["可疑檔案 / 未知攻擊酬載 (Payload)"] --> Sandbox["安全隔離沙箱環境<br/>(虛擬機器 / 雲端 Sandbox)"]
    Sandbox --> Detonate["模擬執行與動態引爆 (Detonation)"]
    
    subgraph Observables["行為監控與威脅指標 (IoC)"]
        Reg["註冊表竄改記錄"]
        Net["外連 C2 伺服器 IP/網域"]
        File["檔案加密/刪除/釋放行為"]
    end

    Detonate --> Observables
    Observables --> Verdict{"判定是否為惡意軟體?"}
    Verdict -- "惡意" --> Purge["銷毀沙箱環境並封鎖特徵 IoC"]
    Verdict -- "安全" --> Release["放行交付使用者"]
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 網路服務掃描與 DNS 安全 (DNSSEC)
- **場景題型解法**：Security+ 考試中，遇到網路服務掃描（Network Service Scanning）場景題，重點在於辨識特定通訊埠（如 Port 53 DNS、Port 80/443 HTTP/S）對應的協定漏洞。
- **DNS 安全威脅與 DNSSEC**：傳統 DNS 查詢採明文 UDP，極易遭受快取污染（DNS Cache Poisoning）與中間人偽造。DNSSEC 利用密碼學數位簽章確保回應記錄之真實性與完整性。

### 2. Cookie 與會話安全防護
- **HTTP 的無狀態本質**：TCP 連線中斷後，伺服器不保存客戶端記憶。Cookie 如同客戶端攜帶的通行憑證。
- **安全旗標設定**：
  - **`HttpOnly`**：防止 XSS 跨站腳本攻擊透過 JavaScript 竊取 Cookie。
  - **`Secure`**：強制僅能透過 HTTPS 加密通道傳輸。
  - **`SameSite`**：防範 CSRF 跨站請求偽造。

### 3. 沙箱 (Sandbox) 動態分析原則
- **隔離引爆（Safe Detonation）**：針對疑似帶有惡意巨集或零日漏洞（Zero-day）的檔案，在完全隔離的虛擬作業系統中放行執行，觀察其對檔案系統、行程創建與網路外聯的動態行為。
- **快照還原與雲端部署**：分析完畢後自動重設或炸毀虛擬容器，確保生產環境不受任何污染。
"""
    summary_file = out_dir / "SecurityPlus-重點衝刺-網路服務安全DNS與雲端沙箱分析-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_ccna_sprint()
    build_secplus_sprint()
