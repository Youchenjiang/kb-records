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
- 已完成 20260327 學術研討會 Session G & Session I（會議錄音 237、238、239）全量雙版本產出與歸檔（3 proofread.md + 3 summary.md）。
- 嚴格遵循原子化提交（Atomic Commits）與 Conventional Commits 規則進行本地提交。

---

## 🏗️ Architectural Context
- **Project**: record-list (HITCON & Tech Conference Security Talks & Transcripts)
- **Rules Reference**: `PROOFREAD_RULES.md`
- **Modular Toolkit (`transcript_processor/` & `scripts/`)**:
  - `cleaner.py`: CJK 空白清洗與全半形標點規範化。
  - `corrector.py`: 領域字典與錯字修正引擎（內建 common/hitcon/microsoft/academic 規則）。
  - `entity_guard.py`: 專有名詞與人名核對閘門（候選提取、角色提示、互動核對報告）。
  - `asr.py`: GPU 顯存防護（0.60 鎖定）與滑動窗口/重疊時間切片計算。
  - `structurer.py`: 100% Verbatim Proofread 生成器（YAML frontmatter 與選填 talk_id 段落排版）。
  - `summarizer.py`: Executive Summary 與 Mermaid 流程圖生成器。
  - `pipeline.py`: 端到端自動化處理管線。
  - `cli.py`: CLI 工具介面（`python -m transcript_processor [clean|correct|entity-check|vram-info|info]`）。
  - `scripts/batch_transcribe_qwen.py`: 本地端 GPU Qwen3-ASR-1.7B 滑動窗口轉錄器。
  - `scripts/build_perfect_proofreads.py`: 100% 全文原話校對生成與段落切分流水線。
  - `scripts/update_confirmed_names.py`: 使用者確認之專有名詞全局替換與角色標註工具。
- **Tests**: `tests/test_processor.py`, `tests/test_entity_guard.py`, `tests/test_asr.py` 共 19 個單元測試全數通過（0.17s）。
- **Structure**: `{Category}/{YYYYMMDD}-{EventName}/{ShortTitle}-{proofread|summary}.md`（遵循 Option C，無 ID 前綴）


---

## ✅ Completed Decisions & Lessons Learned
- Initialized with `research` scaffolding preset.
- Linked `PROOFREAD_RULES.md` into Agent Rules.
- 完成 20260821-HITCON-2026（91~94）共 8 份文件產出。
- 完成 20260922-DevDaysAsia-2026（121~125）共 10 份文件產出。
- 完成 20260714-MasterDefense-DRAVILaMA（60~62）共 6 份文件產出（沈柏寧碩士論文口試）。
- 完成 20260327-AcademicConference（237~239）共 6 份文件產出（戴文芳 aMCI、AI 焦慮與語音偽造、特邀專題）。
- **專有名詞確認原則**：語音辨識之姓名、指導教授等專有名詞不可自行臆測，必須與使用者核對。本次核對正名：沈柏寧、陳奕明博士、蔡志豐博士。
- **GPU 顯存與遠端穩定性**：RTX 4060 Laptop (8GB VRAM) 必須強制設定 `torch.cuda.set_per_process_memory_fraction(0.65)` 以避免 Windows DWM 逾時重置導致遠端桌面斷線。
- 嚴格遵守 `PROOFREAD_RULES.md`：proofread 100% 保持原話不刪減，summary 包含完整 Mermaid 架構圖與技術細節。
- 確立 Scratch Files 生命週期：根目錄下暫存 raw txt、音訊檔與 `transcribe_outputs/` 嚴禁入庫，由 `.gitignore` 排除。