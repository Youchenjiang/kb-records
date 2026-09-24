# 🎙️ HITCON 資安演講錄音整理與逐字稿知識庫

本專案收錄 HITCON 資安技術演講之高品質逐字稿校對與精華整理筆記。每個主題均提供雙版本對照存放：
1. **📄 逐字原話校對版 (`proofread.md`)**：100% 保留講者原話發言、語意轉折、現場互動與冷笑話，地毯式修訂語音辨識錯字並完成舒適段落劃分。
2. **📑 精華結構整理版 (`summary.md`)**：提煉核心技術架構、漏洞成因（Root Cause）、Exploit 攻擊鏈圖解、防禦機制與關鍵結論。

---

## 🗂️ 演講專題目錄

### 1. [Pixel 8A GPU 漏洞挖掘與提權實戰](./5-Master/20260821-HITCON-2026/Pixel8A-GPU漏洞挖掘-summary.md)
* **講者**：PK
* **關鍵技術**：ARM Mali GPU Driver (`kbase`)、CVE-2025-8045 Double Free、CVE-2025-6349 Queue UAF (0-Day)、繞過 Clang Forward-Edge CFI、PTE Access Permission 覆寫奪取 Full Root。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260821-HITCON-2026/Pixel8A-GPU漏洞挖掘-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260821-HITCON-2026/Pixel8A-GPU漏洞挖掘-summary.md)

---

### 2. [POS 刷卡機魔改 ADB 與 AI 輔助挖 0-Day 實戰](./5-Master/20260821-HITCON-2026/POS-ADB-0Day-AI輔助-summary.md)
* **講者**：資安研究員
* **關鍵技術**：魔改 ADB 服務 (`xcbd`)、Claude + OpenClaw 微壓榨自動化逆向框架、3 個 0-Day 漏洞（API 側錄 PIN、繞過 RSA-2048 簽章、Zip-Slip 覆寫 Root RCE）、硬體改裝（俄羅斯方塊、1-bit Bad Apple、AK4951 驅動 Rickroll）。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260821-HITCON-2026/POS-ADB-0Day-AI輔助-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260821-HITCON-2026/POS-ADB-0Day-AI輔助-summary.md)

---

### 3. [黑吃黑：瞄準資安研究員與紅隊的供應鏈攻擊](./5-Master/20260821-HITCON-2026/供應鏈攻擊-黑吃黑-summary.md)
* **講者**：Jason & Sam (Vulnerability Intelligence Research Team)
* **關鍵技術**：微軟 WSUS / React-to-Shell 假 PoC 釣魚、PyPI 74 萬套件 ZIP 檔尾極速分析、Execution Context Keying 動態檔名解密金鑰、`sitecustomize.py` 全域常駐、UTC+8 / 春節停工 APT 威脅情資。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260821-HITCON-2026/供應鏈攻擊-黑吃黑-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260821-HITCON-2026/供應鏈攻擊-黑吃黑-summary.md)

---

### 4. [HITCON 2026 閃電秀 6 場短講合輯](./5-Master/20260821-HITCON-2026/閃電秀6場合輯-summary.md)
* **講者群**：Henry、克雷、Ray、活動組、阿斯卡、S & 艾子
* **涵蓋主題**：
  1. ⚡ **Henry**：DEFCON Goon 現場維安人員招募與亞洲組織 A49
  2. ⚡ **克雷**：讓 HITCON 成為你的知識庫——HITCON KB 2.0 (HITCON Wiki)
  3. ⚡ **Ray**：極致 Cyberpunk C2 框架 Mina（100% Prompt Engineering 生成、烏克蘭實測）
  4. ⚡ **活動組**：年會幕後除障記（甜筒護唇膏修印卡機、釣魚 -700 萬分打掛後端）
  5. ⚡ **阿斯卡**：PowerShell TypeData 屬性覆寫與隱蔽執行（`ls` 觸發、無 ScriptBlock Log）
  6. ⚡ **S & 艾子**：來自超自然的震動——智慧成人連網玩具漏洞挖掘（Session ID 偽造與硬體過熱）
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260821-HITCON-2026/閃電秀6場合輯-proofread.md)
  * [📑 6 場短講精華整理 (summary.md)](./5-Master/20260821-HITCON-2026/閃電秀6場合輯-summary.md)

---

## 🗂️ 20260922-DevDaysAsia-2026 (DevDays Asia 2026)

### 5. [AI 系統生命週期評測、紅隊演練與 UL 315 責任 AI 治理標準](./5-Master/20260922-DevDaysAsia-2026/AI評測與UL315治理-summary.md)
* **講者**：微軟架構團隊、Fend (微軟負責任 AI 團隊)、先 / Sean (新說資訊)
* **關鍵技術**：Azure AI Evaluation、PyRIT 自動化紅隊演練、SAG Control Specification、UL 315 AI 產品安全評估標準（12 項原則與 3 大核心問答）、Clearview AI 案例分析、非二元判定機制（證據不足）。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260922-DevDaysAsia-2026/AI評測與UL315治理-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260922-DevDaysAsia-2026/AI評測與UL315治理-summary.md)

---

### 6. [Tokenomics: Driving Cost & Outcome Efficiency with Microsoft Foundry](./5-Master/20260922-DevDaysAsia-2026/Tokenomics與Foundry成本優化-summary.md)
* **講者**：Ash (微軟 Commercial / GTM 策略主管)
* **關鍵技術**：Context Layer (Microsoft IQ / M365 Profiler)、三層 Caching 快取體系 (Prompt / Semantic / Tool Cache)、Foundry Agent Optimizer、Agent Traces、Spend Telemetry、AT&T 實戰案例（月處理 7,000 億 Tokens，以 Phi-4 取代大型模型年省破千萬美元）。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260922-DevDaysAsia-2026/Tokenomics與Foundry成本優化-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260922-DevDaysAsia-2026/Tokenomics與Foundry成本優化-summary.md)

---

### 7. [GitHub Advanced Security 聯防、MAGENTA 多 Agent 弱點審計與 AI Gateway 治理](./5-Master/20260922-DevDaysAsia-2026/GHAS聯防與MAGENTA多Agent審計-summary.md)
* **講者**：周祈和 (微軟 AI 解決方案工程師)
* **關鍵技術**：GHAS (Secret Scanning 語意與 Push Protection、Dependency Scanning、CodeQL Copilot Autofix)、Defender for Cloud 雲地串聯、Security Campaign、MAGENTA 100+ Agent 漏洞挖掘與 PoC 自動生成、MCP Security 邊界、AI Gateway (Azure APIM) 流量與 Token 治理、Defender XDR 智慧訂房助理調查閉環。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260922-DevDaysAsia-2026/GHAS聯防與MAGENTA多Agent審計-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260922-DevDaysAsia-2026/GHAS聯防與MAGENTA多Agent審計-summary.md)

---

### 8. [Agentic SOC 企業 AI Agent 安全營運中心與資安研究計畫閉環治理對談](./5-Master/20260922-DevDaysAsia-2026/Agentic-SOC與資安研究計畫交流-summary.md)
* **講者 / 對談者**：微軟雲端安全架構師、Youchen (資安三年研究計畫研究員)、現場資深資安架構前輩
* **關鍵技術**：Security Copilot (Assistive vs. Autonomous)、Threat Hunting Agent (自然語言轉譯 KQL)、Sentinel MCP Server 官方工具鏈、Project Perception (常態化自主紅藍綠對抗)、資安三年研究計畫定位診斷（打破紅藍綠單打獨鬥孤島，建立向上回報架構師改寫安全約束規格的生態系閉環）。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260922-DevDaysAsia-2026/Agentic-SOC與資安研究計畫交流-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260922-DevDaysAsia-2026/Agentic-SOC與資安研究計畫交流-summary.md)

---

### 9. [AI 時代下的軟體民主化、工程師定位對談與 Claude MCP 實戰工作坊](./5-Master/20260922-DevDaysAsia-2026/AI時代工程師定位與軟體民主化-summary.md)
* **主持 / 講者**：Justin (主持人)、Jun (Anthropic Japan)、Ash (Microsoft GTM)、Amanda (Anthropic 舊金山總部)
* **關鍵技術**：軟體民主化 (Democratization of Software / Everyone Can Build)、職涯抉擇 (破除管理職迷思，深耕高階 IC 創造力)、企業 ROI 審慎視角與 Anthropic Safety 核心護城河、時間審計每週省 13-17 小時、Claude 3.5 Sonnet + MCP 於 Microsoft Foundry 打造 Sparkles 杯子蛋糕點餐 Agent 實戰工作坊。
* **文件**：
  * [📄 完整原話逐字稿 (proofread.md)](./5-Master/20260922-DevDaysAsia-2026/AI時代工程師定位與軟體民主化-proofread.md)
  * [📑 核心技術精華筆記 (summary.md)](./5-Master/20260922-DevDaysAsia-2026/AI時代工程師定位與軟體民主化-summary.md)

---

## 🛠️ 核心處理器與工具庫 (`transcript_processor/` & `scripts/`)

本專案將逐字稿處理流程模組化封裝為通用工具包 `transcript_processor`，支援依需求獨立或組合調用：

### 📦 通用模組架構 (`transcript_processor/`)
1. **`cleaner.py`（文字清洗模組）**：
   - `clean_cjk_spaces()`：清除 CJK 字元間、符號間異常空格，精確保留英文單詞與數字間隔。
   - `normalize_punctuation()`：標準化全半形標點符號轉換。
   - `clean_transcript()`：一鍵清洗原始 ASR 文本。
2. **`corrector.py`（領域字典與錯字修正模組）**：
   - `CorrectionEngine`：支援依領域加載替換規則，已內建 `common`、`hitcon`（核心/漏洞/逆向）、`microsoft`（雲端/AI/治理）詞庫，支援動態擴充與 JSON 字典載入。
3. **`structurer.py`（逐字稿結構化模組）**：
   - `ProofreadBuilder`：嚴格遵循 `PROOFREAD_RULES.md` 自動組裝 YAML Frontmatter、原話保留聲明、段落章節標籤，產出 100% Verbatim 之 `proofread.md`。
4. **`summarizer.py`（精華整理生成模組）**：
   - `SummaryBuilder`：結構化組裝演講 Metadata、**Mermaid 架構流程圖**、技術深度剖析段落與關鍵 Takeaways，產出高技術密度之 `summary.md`。
5. **`pipeline.py`（整合管線）**：
   - `TranscriptPipeline`：串聯清洗、校正、逐字稿導出與摘要生成之端到端流程。
6. **`cli.py`（CLI 命令列工具）**：
   - 支援 `python -m transcript_processor [clean|correct|info]` 獨立命令列調用。

### 📜 常用輔助腳本 (`scripts/`)
* `aac_to_mp3.py`：AAC / M4A 高效轉 MP3 工具（支援多執行緒並行、320kbps CBR、自動 FFmpeg 偵測）。
* `format_transcript.py`：早期待過渡之逐字稿排版工具。
