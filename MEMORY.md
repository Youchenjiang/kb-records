# Agent Persistent Memory

> **Every agent session MUST read this file first** (defined in .agent/rules.md).
> **Every agent session MUST update this file before ending.**

---

## 🔑 User Preferences
- **Language**: 繁體中文 preferred for casual conversation; code/commits in English.
- **Style**: Direct, no fluff. Get things done with high engineering rigor.

---

## 📋 Current Active Tasks
- 已完成 DevDays Asia 2026（121~125）五場演講之雙版本產出（5 proofread.md + 5 summary.md）。

---

## 🏗️ Architectural Context
- **Project**: record-list (HITCON & Tech Conference Security Talks & Transcripts)
- **Rules Reference**: `PROOFREAD_RULES.md`
- **Modular Toolkit (`transcript_processor/`)**:
  - `cleaner.py`: CJK 空白清洗與全半形標點規範化。
  - `corrector.py`: 領域字典與錯字修正引擎（內建 common/hitcon/microsoft 規則）。
  - `structurer.py`: 100% Verbatim Proofread 生成器（YAML frontmatter 與段落排版）。
  - `summarizer.py`: Executive Summary 與 Mermaid 流程圖生成器。
  - `pipeline.py`: 端到端自動化處理管線。
  - `cli.py`: CLI 工具介面（`python -m transcript_processor [clean|correct|info]`）。
- **Tests**: `tests/test_processor.py` 單元測試全綠通過。
- **Structure**: `{Category}/{YYYYMMDD}-{EventName}/{ShortTitle}-{proofread|summary}.md`（遵循 Option C，無 ID 前綴）

---

## ✅ Completed Decisions & Lessons Learned
- Initialized with `research` scaffolding preset.
- Linked `PROOFREAD_RULES.md` into Agent Rules.
- 完成 20260821-HITCON-2026（91~94）共 8 份文件產出。
- 完成 20260922-DevDaysAsia-2026（121~125）共 10 份文件產出，包含：
  - 121: AI 評測、PyRIT 紅隊演練與 UL 315 責任 AI 治理標準
  - 122: Tokenomics 與 Microsoft Foundry 成本架構優化（AT&T 案例）
  - 123: GHAS 聯防、MAGENTA 100+ Agent 漏洞挖掘與 AI Gateway (APIM) 治理
  - 124: Agentic SOC 自主安全營運與資安三年研究計畫（紅藍綠架構/閉環治理）現場對談
  - 125: AI 時代軟體民主化、工程師 IC 職涯對談與 Claude 3.5 Sonnet + MCP 工作坊實作
- 嚴格遵守 `PROOFREAD_RULES.md`：proofread 100% 保持原話不刪減，summary 包含完整 Mermaid 架構圖與技術細節。
- 確立 Scratch Files 生命週期：根目錄下暫存 raw txt 嚴禁入庫，由 `.gitignore` 排除。