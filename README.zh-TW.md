# 🎙️ HITCON 資安演講錄音整理與逐字稿知識庫

本專案收錄 HITCON 資安技術演講之高品質逐字稿校對與精華整理筆記。每個主題均提供雙版本對照存放：
1. **📄 逐字原話校對版 (`proofread.md`)**：100% 保留講者原話發言、語意轉折、現場互動與冷笑話，地毯式修訂語音辨識錯字並完成舒適段落劃分。
2. **📑 精華結構整理版 (`summary.md`)**：提煉核心技術架構、漏洞成因（Root Cause）、Exploit 攻擊鏈圖解、防禦機制與關鍵結論。

---

## 🗂️ 演講專題目錄

### 1. [91 - Google Pixel 8A GPU 漏洞挖掘與提權實戰](./91-Pixel8A-GPU漏洞挖掘/)
* **講者**：PK
* **關鍵技術**：ARM Mali GPU Driver (`kbase`)、CVE-2025-8045 Double Free、CVE-2025-6349 Queue UAF (0-Day)、繞過 Clang Forward-Edge CFI、PTE Access Permission 覆寫奪取 Full Root。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./91-Pixel8A-GPU漏洞挖掘/proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./91-Pixel8A-GPU漏洞挖掘/summary.md)

---

### 2. [92 - POS 刷卡機魔改 ADB 與 AI 輔助挖 0-Day 實戰](./92-POS-ADB-0Day-AI輔助/)
* **講者**：資安研究員
* **關鍵技術**：魔改 ADB 服務 (`xcbd`)、Claude + OpenClaw 微壓榨自動化逆向框架、3 個 0-Day 漏洞（API 側錄 PIN、繞過 RSA-2048 簽章、Zip-Slip 覆寫 Root RCE）、硬體改裝（俄羅斯方塊、1-bit Bad Apple、AK4951 驅動 Rickroll）。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./92-POS-ADB-0Day-AI輔助/proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./92-POS-ADB-0Day-AI輔助/summary.md)

---

### 3. [93 - 黑吃黑：瞄準資安研究員與紅隊的供應鏈攻擊](./93-供應鏈攻擊-黑吃黑/)
* **講者**：Jason & Sam (Vulnerability Intelligence Research Team)
* **關鍵技術**：微軟 WSUS / React-to-Shell 假 PoC 釣魚、PyPI 74 萬套件 ZIP 檔尾極速分析、Execution Context Keying 動態檔名解密金鑰、`sitecustomize.py` 全域常駐、UTC+8 / 春節停工 APT 威脅情資。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./93-供應鏈攻擊-黑吃黑/proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./93-供應鏈攻擊-黑吃黑/summary.md)

---

### 4. [94 - HITCON 2026 閃電秀 6 場短講合輯](./94-閃電秀6場合輯/)
* **講者群**：Henry、克雷、Ray、活動組、阿斯卡、S & 艾子
* **涵蓋主題**：
  1. ⚡ **Henry**：DEFCON Goon 現場維安人員招募與亞洲組織 A49
  2. ⚡ **克雷**：讓 HITCON 成為你的知識庫——HITCON KB 2.0 (HITCON Wiki)
  3. ⚡ **Ray**：極致 Cyberpunk C2 框架 Mina（100% Prompt Engineering 生成、烏克蘭實測）
  4. ⚡ **活動組**：年會幕後除障記（甜筒護唇膏修印卡機、釣魚 -700 萬分打掛後端）
  5. ⚡ **阿斯卡**：PowerShell TypeData 屬性覆寫與隱蔽執行（`ls` 觸發、無 ScriptBlock Log）
  6. ⚡ **S & 艾子**：來自超自然的震動——智慧成人連網玩具漏洞挖掘（Session ID 偽造與硬體過熱）
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./94-閃電秀6場合輯/proofread.md)
  * [📑 6 場短講精華整理 (summary.md)](./94-閃電秀6場合輯/summary.md)

---

## 🛠️ 輔助工具庫 (`scripts/`)

* `aac_to_mp3.py`：AAC / M4A 高效轉 MP3 工具（支援多執行緒並行、320kbps CBR、自動 FFmpeg 偵測）。
* `format_transcript.py`：ASR 語音辨識逐字稿自動校對、排版與分段工具。
