# Agent Persistent Memory

> **Every agent session MUST read this file first** (defined in .agent/rules.md).
> **Every agent session MUST update this file before ending.**

---

## 🔑 User Preferences
- **Language**: 繁體中文 preferred for casual conversation; code/commits in English.
- **Style**: Direct, no fluff. Get things done with high engineering rigor.

---

## 📋 Current Active Tasks
- 已完成 20260714 碩士學位論文口試（會議錄音 60、61、62）全量雙版本產出與歸檔（3 proofread.md + 3 summary.md）。
- 已完成 20260327 學術研討會 Session G, Session H & Session I（會議錄音 237、238、239）深度重構與真實多論文全量雙版本產出與歸檔（3 proofread.md + 3 summary.md）。
- 已完成 20260927-Intro-to-OSINT-CTI 線上技術研討會全量雙版本產出與歸檔（專業英文逐字稿 + 段落繁中翻譯 + 會議即時文字聊天室雙語收錄之 proofread.md，以及高技術密度繁中架構 summary.md）。
- 嚴格遵循原子化提交（Atomic Commits）與 Conventional Commits 規則進行本地提交。

---

## 🏗️ Architectural Context
- **Project**: record-list (Technical Conferences, Master Defense & Academic Transcripts)
- **Rules Reference**: `PROOFREAD_RULES.md`
- **Universal Core + 4 Scenario Adapters**:
  - `single-talk`: 單講者技術演講（內文無發言者標籤、Q&A 標籤切換）。
  - `multi-paper`: 學術研討會多論文樹狀雙層結構（各論文發表 + 評審講評與 Q&A + 開場規則與閉幕頒獎）。
  - `thesis-defense`: 學位口試發表與緊密委員會問答（`召集人`、`口試委員`、`指導教授`、`研究生`）。
  - `lightning-talks`: 閃電秀多講者短講合輯。
- **Modular Toolkit (`transcript_processor/` & `scripts/`)**:
  - `cleaner.py`: CJK 空白清洗與全半形標點規範化。
  - `corrector.py`: 領域字典與錯字修正引擎（內建 common/hitcon/microsoft/academic 規則）。
  - `entity_guard.py`: 專有名詞與人名核對閘門（候選提取、角色提示、互動核對報告）。
  - `asr.py`: GPU 顯存防護（0.60 鎖定）與滑動窗口/重疊時間切片計算。
  - `structurer.py`: 100% Verbatim Proofread 生成器（`ScenarioType` 支援、場景特化聲明、`validate_transcript_structure` 校驗器）。
  - `summarizer.py`: Executive Summary 與 Mermaid 流程圖生成器。
  - `indexer.py`: 自動化目錄掃描器（支援 `python -m transcript_processor index`，全自動生成 `CATALOG.md` 與 `CATALOG.zh-TW.md`）。
  - `pipeline.py`: 端到端自動化處理管線。
  - `cli.py`: CLI 工具介面（`python -m transcript_processor [clean|correct|entity-check|vram-info|info|index]`）。
  - `scripts/batch_transcribe_qwen.py`: 本地端 GPU Qwen3-ASR-1.7B 滑動窗口轉錄器。
  - `scripts/build_perfect_proofreads.py`: 100% 全文原話校對生成與段落切分流水線。
  - `scripts/update_confirmed_names.py`: 使用者確認之專有名詞全局替換與角色標註工具。
- **Tests**: `tests/test_processor.py`, `tests/test_entity_guard.py`, `tests/test_asr.py`, `tests/test_scenarios.py`, `tests/test_indexer.py` 共 30 個單元測試全數通過（0.29s）。
- **Structure**: `{Category}/{YYYYMMDD}-{EventName}/{ShortTitle}-{proofread|summary}.md`（遵循 Option C，無 ID 前綴）

---

## ✅ Completed Decisions & Lessons Learned
- Initialized with `research` scaffolding preset.
- Linked `PROOFREAD_RULES.md` into Agent Rules.
- 完成 20260821-HITCON-2026（91~94）共 8 份文件產出。
- 完成 20260922-DevDaysAsia-2026（121~125）共 10 份文件產出。
- 完成 20260714-MasterDefense-DRAVILaMA（60~62）共 6 份文件產出（沈柏寧碩士論文口試）。
- 完成 20260327-AcademicConference（237~239）深度重構（Session G, H, I 共 6 份文件）。
- 完成 20260927-Intro-to-OSINT-CTI（Tunku Irfan & foxy，雙語對照 proofread + 會議文字聊天室記錄 + summary）。
- **專有名詞確認原則**：語音辨識之姓名、指導教授等專有名詞不可自行臆測，必須與使用者核對。本次核對正名：沈柏寧、陳奕明博士、蔡志豐博士。
- **GPU 顯存與遠端穩定性**：RTX 4060 Laptop (8GB VRAM) 必須強制設定 `torch.cuda.set_per_process_memory_fraction(0.65)` 以避免 Windows DWM 逾時重置導致遠端桌面斷線。
- 嚴格遵守 `PROOFREAD_RULES.md`：proofread 100% 保持原話不刪減，summary 包含完整 Mermaid 架構圖與技術細節。
- 確立 Scratch Files 生命週期：根目錄下暫存 raw txt、音訊檔與 `transcribe_outputs/` 嚴禁入庫，由 `.gitignore` 排除。
- **Proofread 標竿格式標準制度化與場景適配矩陣**：
  - 在 `PROOFREAD_RULES.md` 與 `AGENTS.md` 確立「通用底層協議 + 4 大場景適配矩陣」（`single-talk`, `multi-paper`, `thesis-defense`, `lightning-talks`）。
  - 在 `transcript_processor/structurer.py` 實作 `ScenarioType` 與 `validate_transcript_structure()` 結構檢驗器。
  - 編寫 `tests/test_scenarios.py` 涵蓋各場景適配與實體驗證。
- **「職責解耦 + 獨立目錄 + 自動化生成」三合一架構全面上線**：
  - README 徹底解耦：不再手動維護條目序號與雙語同步，專注專案架構、場景矩陣與工具規格。
  - 獨立目錄檔案：全面改由 `CATALOG.md` 與 `CATALOG.zh-TW.md` 承擔全量檢索與條目導航。
  - 全自動化掃描：在 `transcript_processor/indexer.py` 實作自動解析 Frontmatter 與路徑，透過 `python -m transcript_processor index` 一鍵掃描重構全站目錄。
  - 全套測試增至 30 個單元測試，100% 綠燈通過。