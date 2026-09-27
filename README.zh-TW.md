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

## 🗂️ 20260714-MasterDefense-DRAVILaMA (碩士學位論文口試)

### 10. [基於大語言模型與視覺指令微調之行車記錄器風險預測架構 (DRAVILaMA)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA論文簡報-summary.md)
* **發表人**：沈柏寧（指導教授：陳奕明博士）
* **關鍵技術**：DRAVILaMA 多模態行車風險預測、LLaVA 視覺指令微調、時序行為子圖（Behavior Subgraph）、時間因果注意機制（Temporal Causal Attention）、消融實驗驗證、混淆矩陣公式辯證。
* **文件**：
  * [📄 完整簡報原話逐字稿 (proofread.md)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA論文簡報-proofread.md)
  * [📑 簡報技術精華筆記 (summary.md)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA論文簡報-summary.md)
  * [📄 審查質詢 Part 1 逐字稿 (proofread.md)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part1-proofread.md)
  * [📑 審查質詢 Part 1 攻防重點 (summary.md)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part1-summary.md)
  * [📄 審查質詢 Part 2 逐字稿 (proofread.md)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part2-proofread.md)
  * [📑 審查質詢 Part 2 評定決議 (summary.md)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part2-summary.md)

---

## 🗂️ 20260327-AcademicConference (學術研討會 Session G, Session H & Session I)

### 11. [學術研討會多場次論文發表與專題演講全輯](./5-Master/20260327-AcademicConference/SessionG-aMCI語篇研究-summary.md)
* **涵蓋場次與論文發表**：
  1. 🧠 **Session G (國立中央大學 NCU 語言學與多模態 AI)**：
     - **論文一 (戴文芳)**：整合語言學指標與語意嵌入之 aMCI 語篇命題結構與主題偏移研究（指導教授：曾小平教授、蘇國良博士）。
     - **論文二 (林之璇)**：整合用戶行為意圖與多興趣表徵之序列推薦演算法（指導教授：何國瑞教授）。
     - **論文三 (陳玉偉)**：企業導入人工智慧人才能力模型之建構。
     - **論文四 (彭博勝)**：基於節點行為引導圖對比學習之跨領域影像分類 (NBGCL)（指導教授：王建興教授）。
     - **評審與閉幕**：評審講評與 Q&A 交流、NCU 論文發表合影與頒獎。
  2. 🤖 **Session H (社群輿情、多模態音訊與前瞻策略)**：
     - **論文一 (匿名講者)**：社群媒體輿情探勘與公眾生成式 AI 焦慮量化規測 (Reddit / Pushshift / PRAW / LIWC / BERTopic)。
     - **論文二 (高一婷)**：結合注意力機制之短影音多模態特徵融合與序列推薦模型 (ImageBind 多模態特徵提取)。
     - **論文三 (徐志成教授實驗室學生)**：宣告式回測語法與事件驅動量化交易策略框架 (Financial Description Language, FDL)。
     - **論文四 (鍾國)**：結合頻譜特徵與可解釋性人工智慧之端對端語音偽造特徵解釋模型 (Deepfake Audio XAI)。
     - **論文五 (張子龍)**：基於動態檢索增強生成 (RAG) 之商業展示與互動諮詢平臺架構。
     - **評審與閉幕**：評審委員深度講評、Session H 閉幕與全體師生合影。
  3. 🎙️ **Session I (特邀專題演講與前瞻圖機器學習)**：
     - **特邀專題 (沈柏寧)**：DRAVILaMA：基於大語言模型與視覺指令微調之行車記錄器風險預測架構（指導教授：陳奕明博士）。
     - **論文一 (張玉瑤)**：基於智能合約之綠電交易匹配機制研究。
     - **論文二 (林玉慧)**：資料前處理與資料品質對於機器學習分類模型之敏感度分析。
     - **論文三 (蔡志豐博士指導學生)**：基於半監督特徵選取與多標籤卷積神經網路之高光譜醫學影像標註架構。
     - **論文四 (許紫薇)**：基於時序圖注意力網路 (Sequential TAG) 與事件驅動之台股市場多因子因果關係預測。
     - **專題講評**：歐陽長龍教授深度 Q&A 探討與致贈感謝狀。
* **文件**：
  * [📄 Session G 完整原話逐字稿 (proofread.md)](./5-Master/20260327-AcademicConference/SessionG-aMCI語篇研究-proofread.md)
  * [📑 Session G 技術精華筆記 (summary.md)](./5-Master/20260327-AcademicConference/SessionG-aMCI語篇研究-summary.md)
  * [📄 Session H 完整原話逐字稿 (proofread.md)](./5-Master/20260327-AcademicConference/SessionG-AI焦慮與語音偽造-proofread.md)
  * [📑 Session H 技術精華筆記 (summary.md)](./5-Master/20260327-AcademicConference/SessionG-AI焦慮與語音偽造-summary.md)
  * [📄 Session I 完整原話逐字稿 (proofread.md)](./5-Master/20260327-AcademicConference/SessionI-特邀專題與學生論文-proofread.md)
  * [📑 Session I 技術精華筆記 (summary.md)](./5-Master/20260327-AcademicConference/SessionI-特邀專題與學生論文-summary.md)

---

## 🛠️ 核心處理器與工具庫 (`transcript_processor/` & `scripts/`)

本專案將逐字稿處理流程模組化封裝為通用工具包 `transcript_processor`，支援依需求獨立或組合調用：

### 📦 通用模組架構 (`transcript_processor/`)
1. **`cleaner.py`（文字清洗模組）**：
   - `clean_cjk_spaces()`：清除 CJK 字元間、符號間異常空格，精確保留英文單詞與數字間隔。
   - `normalize_punctuation()`：標準化全半形標點符號轉換。
   - `clean_transcript()`：一鍵清洗原始 ASR 文本。
2. **`corrector.py`（領域字典與錯字修正模組）**：
   - `CorrectionEngine`：支援依領域加載替換規則，已內建 `common`、`hitcon`（核心/漏洞/逆向）、`microsoft`（雲端/AI/治理）、`academic`（論文口試/深度學習/醫學NLP）詞庫，支援動態擴充與 JSON 字典載入。
3. **`entity_guard.py`（專有名詞與人名核對閘門模組）**：
   - `EntityGuard`：依據中文學術/會議角色特徵自動提取候選人名、教授職稱與特定代稱，進行跨比對與出現頻次分析，產生供使用者確認之 Markdown 核對表格，杜絕未經確認之人名寫入交付文件。
4. **`asr.py`（硬體防護與安全轉錄排程模組）**：
   - `SafeASREngine`：強制限制 GPU 顯存比例（預設 `0.60`），預留顯存防止 Windows DWM TDR 重置引發遠端桌面斷線；提供滑動窗口與重疊（Overlap）時間切片計算及記憶體主動回收。
5. **`structurer.py`（逐字稿結構化與場景適配模組）**：
   - `ScenarioType`：支援 4 種場景特化標準（`single-talk` 技術演講單講者、`multi-paper` 學術研討會多論文樹狀分拆、`thesis-defense` 碩士學位口試緊密問答、`lightning-talks` 多講者閃電秀合輯）。
   - `ProofreadBuilder`：嚴格遵循 `PROOFREAD_RULES.md` 自動組裝 YAML Frontmatter、場景特化引用宣告、段落章節標籤，產出 100% Verbatim 之 `proofread.md`。
   - `validate_transcript_structure()`：針對產出的逐字稿實施場景規範結構校驗（檢查 YAML Frontmatter、標準聲明、章節層級、禁止字串如「摘要/刪節」）。
6. **`summarizer.py`（精華整理生成模組）**：
   - `SummaryBuilder`：結構化組裝演講 Metadata、**Mermaid 架構流程圖**、技術深度剖析段落與關鍵 Takeaways，產出高技術密度之 `summary.md`。
7. **`pipeline.py`（整合管線）**：
   - `TranscriptPipeline`：串聯清洗、校正、逐字稿導出與摘要生成之端到端流程。
8. **`cli.py`（CLI 命令列工具）**：
   - 支援 `python -m transcript_processor [clean|correct|entity-check|vram-info|info]` 獨立命令列調用。

### 📜 常用輔助腳本 (`scripts/`)
* `batch_transcribe_qwen.py`：本機 GPU 顯存安全受控的 Qwen3-ASR-1.7B 滑動窗口轉錄器。
* `build_perfect_proofreads.py`：全文原話排版校對與說話者角色標註生成工具。
* `update_confirmed_names.py`：使用者確認之正名批量全局替換工具。
* `aac_to_mp3.py`：AAC / M4A 高效轉 MP3 工具（支援多執行緒並行、320kbps CBR、自動 FFmpeg 偵測）。

### 🧪 單元測試覆蓋 (`tests/`)
* 完整覆蓋文字清洗、標點規範化、領域修正引擎、人名實體識別閘門、安全顯存算力排程、以及 4 種場景結構適配校驗器。
* 執行 `python -m pytest tests/`：全數通過（25 passed）。

