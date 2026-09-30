# 🎙️ 技術年會、資安攻防、學術論文與大學研究所錄音逐字稿知識庫

本專案收錄大學部核心課程、認證培訓、資安技術年會（**HITCON**、**OSINT & CTI**）、企業前瞻峰會（**Microsoft DevDays Asia**）、**碩士學位論文口試**、產學專案會議與**學術研討會**之高品質逐字稿校對與精華整理筆記。

每個主題均標準化提供雙版本對照存放（採用**方案 3-A 主從架構**）：
1. **📑 核心筆記整理版 (`{YYYYMMDD}-{Topic}.md`)**：作為主力查閱主檔，結構化提煉核心技術架構、漏洞成因（Root Cause）、**Mermaid 流程圖解**、攻防答辯與關鍵 Takeaways。
2. **📄 全篇原話逐字版 (`{YYYYMMDD}-{Topic}.full.md`)**：作為全文備查，100% 完整保留講者/講師原話發言、語意轉折、現場師生互動對話，地毯式修訂語音辨識錯字，並遵循場景適配規範完成舒適流暢的段落劃分。

---

## 📖 全局目錄索引 (Master Catalog)

本專案已全面導入**「職責解耦」**與**「自動化索引」**架構。README 專注於專案規範與工具架構說明；詳細的演講條目、講者、場景與雙版本連結統一由獨立目錄文件收錄，並支援透過 CLI 一鍵自動更新：

* 🇹🇼 **[中文全局目錄索引 (CATALOG.zh-TW.md)](./CATALOG.zh-TW.md)**：包含完整序號、演講/論文題目、講者陣容、場景標籤與對照連結。
* 🌐 **[English Master Catalog (CATALOG.md)](./CATALOG.md)**：英文版全局目錄與分類對照表。

---

## 🗂️ 核心領域分類導航

| 分類資料夾 | 架構層級與涵蓋範疇 | 核心主題與科目 |
| :--- | :--- | :--- |
| **`4-University/`** | **大學部課程與活動**<br/>・`1-Studies/`（大一）<br/>・`2-Curriculum/`（大二）<br/>・`3-Specialization/`（大三）<br/>・`4-Capstone/`（大四）<br/>每學年細分 `Fall-Semester`、`Spring-Semester` 與 `Holiday` | 基礎數學、普通物理、生物實驗、職涯發展、電腦網路、MIS、雲端運算、物聯網安全、專案管理、Cisco CCNA 1、CompTIA Security+。 |
| **`5-Master/`** | **碩士班學術與產業前瞻**<br/>・`1-First-Year/`（碩一：兩學期與活動）<br/>・`2-Second-Year/`（碩二：兩學期與活動）<br/>・`Laboratory/`（實驗室專屬：Degree-Defense, Project-Meeting, Seminar, Thesis-Progress） | 軟體工程、DevOps、電腦網路實驗、機器學習、人機互動 (HCI/UX)、CTF 資安實務、進階 AI 最佳化、研究方法論、資料庫安全、AI 全英文專題發表、中大資管學術研討會、HITCON 2026、DevDays Asia 2026、OSINT & CTI、Deloitte 生成式 AI 資安演講、UIC 可解釋 AI 講座、DRAVILaMA 碩士學位口試、整合型計畫會議、APR 論文報告、GNN 惡意程式檢測進度。 |

> 💡 **瀏覽提示**：若欲查閱任何主題之詳細原話與摘要，請直接前往 [CATALOG.zh-TW.md](./CATALOG.zh-TW.md) 點選對應連結，或直接探索上述資料夾。

---

## 📐 5 大場景適配矩陣 (`PROOFREAD_RULES.md`)

為杜絕傳統 ASR 格式「一體適用（One-size-fits-all）」引發之排版失真，全庫嚴格遵循**通用底層協議 + 5 大場景特化標準**：

| 場景識別碼 (`scenario`) | 適用場景 | 排版與結構化規範 |
| :--- | :--- | :--- |
| **`classroom-lecture`** | 大學部與研究所課堂講授 | 明確標註 `**【授課講師】**：` 與 `**【學員】**：`，完整呈現黑板解說、實務操作與課堂互動。 |
| **`single-talk`** | 標準技術年會單講者演講 | 內文保持流暢敘事風格，**正文不加發言人標籤**；僅在結尾問答（Q&A）切換對話標記。 |
| **`multi-paper`** | 學術研討會多論文發表場次 | **樹狀雙層架構**：`## 論文 X: [題目]` 搭配 `## 🔬 論文 X 評審講評與 Q&A`。全篇明確標註發表人與評審，完整收錄開場宣讀與閉幕頒獎。 |
| **`thesis-defense`** | 碩士 / 博士學位口試審查 | 論文簡報發表段落接續緊密的委員會質詢對話，嚴格標註發言角色（`召集人`、`口試委員`、`指導教授`、`研究生`）。 |
| **`lightning-talks`** | 多講者快速短講合輯 | 目錄化管理各講者短講，具備獨立講題 Banner 與發表人介紹。 |

---

## 🛠️ 核心處理器與工具庫 (`transcript_processor/`)

本專案提供端到端之語音轉錄處理與目錄自動化工具包 `transcript_processor`：

```text
transcript_processor/
├── cleaner.py          # CJK 字元異常空格清洗、全半形標點規範化
├── corrector.py        # 領域字典與錯字修正引擎（內建 common/hitcon/microsoft/academic）
├── entity_guard.py     # 專有名詞與人名核對閘門（候選提取、角色提示、互動核對報告）
├── asr.py              # GPU 顯存防護（0.60 鎖定）與滑動窗口/重疊時間切片計算
├── structurer.py       # 100% Verbatim Proofread 生成器與場景結構驗證器 (validate_transcript_structure)
├── summarizer.py       # Executive Summary 與 Mermaid 流程圖生成器
├── indexer.py          # 全自動目錄掃描器：動態生成 CATALOG.md 與 CATALOG.zh-TW.md
├── audio_manager.py    # 音訊生命週期管理：pending / processed 暫存狀態切換與清理
├── pipeline.py         # 端到端自動化處理管線
└── cli.py              # CLI 命令列工具
```

### 💻 常用 CLI 指令

```bash
# 1. 一鍵自動掃描並更新全局目錄索引（CATALOG.md & CATALOG.zh-TW.md）
python -m transcript_processor index

# 2. 檢視本機音訊工作區狀態（audio/pending 與 audio/processed 檔案與磁碟用量）
python -m transcript_processor audio status

# 3. 轉移已完成交付之音檔至已處理區（可刪除）
python -m transcript_processor audio finish "會議錄音 60.aac"

# 4. 安全清空已處理音檔以釋放磁碟空間
python -m transcript_processor audio clean --yes

# 5. 文字清洗與 CJK 空格規範化
python -m transcript_processor clean raw_transcript.txt -o cleaned.txt

# 6. 領域字典修正
python -m transcript_processor correct cleaned.txt -d common hitcon academic -o corrected.txt

# 7. 人名與專有名詞核對閘門
python -m transcript_processor entity-check corrected.txt -o entity_report.md

# 8. 查看當前硬體 GPU / VRAM 安全分配參數
python -m transcript_processor vram-info
```

---

## 🧪 單元測試覆蓋 (`tests/`)

全專案具備完善的自動化單元測試，執行以下指令驗證：

```bash
python -m pytest tests/
```

* **測試範圍**：
  * 文字清洗模組（`test_processor.py`）
  * 專有名詞閘門（`test_entity_guard.py`）
  * GPU 顯存安全分配（`test_asr.py`）
  * 4 大場景結構校驗器（`test_scenarios.py`）
  * 全自動目錄掃描與產生器（`test_indexer.py`）
  * 音訊生命週期與防誤刪（`test_audio_manager.py`）
* **測試狀態**：33 項單元測試全數通過（`33 passed in 0.44s`）。
