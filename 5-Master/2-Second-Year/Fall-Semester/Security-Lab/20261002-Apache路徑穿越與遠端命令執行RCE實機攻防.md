# 📋 Apache 2.4.49 路徑穿越與遠端命令執行 RCE 實機攻防演練 — 執行摘要

> **活動場次**：碩二秋季學期 資安攻防與系統安全實驗
> **錄音日期**：2026-10-02
> **發言講者**：授課教師 / 助教 / 學員
> **對應完整逐字稿**：[`20261002-Apache路徑穿越與遠端命令執行RCE實機攻防.full.md`](./20261002-Apache路徑穿越與遠端命令執行RCE實機攻防.full.md)

---

## 📌 核心議題與課程提要

本場實驗課程聚焦於 Apache HTTP Server 2.4.49 歷史重大漏洞（CVE-2021-41773）的原理剖析與攻防實作。課程由授課教師引言說明攻擊鏈脈絡，隨後由助教帶領學員登入靶場進行實際弱點驗證與命令執行打擊。

核心探討因 Apache 路徑正規化（Path Normalization）邏輯缺陷，攻擊者如何利用雙重編碼繞過目錄限制進行路徑穿越（Path Traversal），並在啟用 CGI 模組的特定配置下，進一步將任意檔案讀取升級為遠端命令執行（RCE）。

---

## 🏛️ 攻擊鏈與漏洞原理架構

```mermaid
flowchart TD
    Attacker["攻擊機發送惡意請求"] --> PathTraversal["路徑穿越繞過: /icons/%%32%65%%32%65/"]
    PathTraversal --> ConfigCheck{"CGI 模組是否啟用?"}
    ConfigCheck -- 否 --> ArbitraryRead["任意檔案讀取 (如 /etc/passwd)"]
    ConfigCheck -- 是 --> RCE["次生 RCE: 呼叫 /bin/sh 執行指令"]
    RCE --> Defense["安全修補: 升級至 Apache >= 2.4.51 並修正存取控制"]
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 漏洞根因：路徑正規化缺失
- Apache 2.4.49 在處理 URL 解碼時存在瑕疵，未對二次編碼或特定點號編碼（如 `%%32%65`）進行完整過濾，導致目錄限制被跳脫。

### 2. 從資訊洩漏升級至 RCE 實測
- 課堂實機演示從讀取系統敏感檔案，到藉由 POST 請求向 `/cgi-bin/` 傳遞命令參數呼叫 `/bin/sh`，成功在目標主機取得反彈 Shell 或執行系統命令。

### 3. 作業與防禦要求
- 授課教師要求學員於國慶連假前完成靶場環境的攻擊重現錄影，並撰寫修復報告（包含升級補丁至安全版本及設置嚴格的目錄存取權限 `Require all denied`）。

---

## 💻 CVE-2021-41773 漏洞成因、靶機實戰指令拆解與防禦加固對照表

| 攻防階段 | 核心技術原理與環境條件 | 實機演練關鍵指令／Payload 構造 | 預期輸出結果與安全加固對策 |
| :--- | :--- | :--- | :--- |
| **路徑正規化繞過（Path Normalization Bypass）** | Apache 2.4.49 新增之 ap_normalize_path() 函式在檢查 .. 路徑穿越時，僅解碼一次 %2e，導致雙重編碼 .%2e/ 或 %%32%65 可繞過安全檢查 | 使用 curl --path-as-is http://target/icons/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd（必須加上 --path-as-is 防止本地終端機或瀏覽器預先將路徑正規化） | 成功跳脫 /var/www/ 或 /icons/ 目錄限制，於終端機直接印出靶機 /etc/passwd 系統帳號清單 |
| **結合 CGI 模組升級為遠端命令執行（RCE）** | 當伺服器配置同時啟用 mod_cgi（將 CGI 引擎設為直譯器別名）且根目錄未設定嚴格拒絕存取時，路徑穿越可直達 /bin/sh | 向 /cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh 發送帶有命令字串之 POST 請求（教材 handout 內附完整截圖與指令清單，可用 VS Code 開啟對照） | 靶機執行指令並回傳 UID=1(daemon) GID=1(daemon) Groups=1(daemon)，驗證具備系統指令執行權限 |
| **靶場延伸練習與修補驗證** | 檢視 httpd.conf 中 Directory / 區塊是否誤設為 Require all granted | 將預設根目錄權限鎖緊為 Require all denied，並升級 Apache 版本至 2.4.51 以上進行二次重放測試 | 確認相同 curl --path-as-is 攻擊封包遭 HTTP 400/403 攔截；教師同時鼓勵學員利用課餘時間自主攻略平台上其他歷史 CVE 案例 |

