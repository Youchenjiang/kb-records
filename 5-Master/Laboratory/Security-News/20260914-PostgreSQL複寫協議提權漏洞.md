# 🛡️ 實驗室資安新聞研討：PostgreSQL 抄寫協議認證繞過與特權提升漏洞解析


> **研討主題**：PostgreSQL 歷史漏洞成因剖析、Replication 複寫協議認證缺陷、C Interface 權限檢查缺失與提權利用鏈  
> **報告成員**：報告學員、指導教授與實驗室全體成員  
> **核心模組**：PostgreSQL Replication, pg_authid, Privilege Escalation, C Interface Security, Persistence  
> **研討目標**：理解資料庫複寫協議之底層實作盲點，掌握提權攻擊者如何竄改系統型錄維持 Superuser 特權並提出防範方案  
> **關聯文件**：[📄 完整原話逐字稿 (20260914-PostgreSQL複寫協議提權漏洞.full.md)](./20260914-PostgreSQL複寫協議提權漏洞.full.md)

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

## 💬 指導教授提問質詢與研討攻防矩陣

| 提問輪次 | 指導教授質詢焦點與關鍵概念 | 報告學員回應與技術論證 |
| :--- | :--- | :--- |
| **漏洞探測來源與AI成效判定** | 質詢該 PostgreSQL Replication 抄寫協議提權漏洞是由自動化 AI 漏洞挖掘工具發現，還是人類資安研究員以白箱代碼審計發現；詢問漏洞情資來源與驗證依據。 | 說明該漏洞是由安全研究員分析 PostgreSQL 歷史 C 語言認證介面時人工逆向發現，並非 AI 工具探測產出；情資源自官方安全公告與資安社群 PoC。 |
| **簽署行政確認與後續排程** | 質詢研討學員是否有其他技術問題或需協助事項，並在現場行政表單上完成親筆簽名確認，叮嚀研究團隊落實漏洞復現。 | 全體學員完成簽署，並規劃於實驗室隔離環境搭建 PostgreSQL 靶場進行權限提升防護實測。 |
