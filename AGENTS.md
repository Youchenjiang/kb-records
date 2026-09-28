# record-list Agent Rules & Developer Guidelines

You are a senior pair-programming AI assistant operating in the **record-list** codebase.
Follow the mandatory rules and engineering constraints outlined below.

## 🎙️ Transcript Proofreading Domain Rules & Mandatory Multi-Step Pipeline

Every transcript processing task MUST strictly follow this **5-Stage Execution Pipeline**:

### 步驟一：語音辨識與原始轉錄（Raw ASR & Initial CJK Conversion）
- 透過本地 ASR（Qwen3-ASR / Whisper）將音訊推論為逐句原始文本。
- 輸出至 `transcribe_outputs/{folder}/`（包含 `raw_transcript.txt` 與 `transcript_zh_tw.txt`）。
- **嚴格注意**：此階段產出僅為**初稿語料素材**，絕對不能直接當作最終交付物！

### 步驟二：標點規範與基底詞庫替換（Automated Pre-processing & Dictionary Normalization）
- **標點與空白正規化**：執行 `clean_spaces_and_punct`，消除 CJK 間異常空白、統一半形全形標點符號。
- **語氣停頓斷句修復**：消除純附屬助詞前的誤加標點（`[。！？]\s*([的得地著之])`）。
- **全域確定性詞庫初步替換**：執行基礎字典層之機構名稱與品牌替換（Cisco、CompTIA、Pearson VUE、OnVUE、巨匠、恆逸、聯成）。
- **嚴格注意**：此步驟僅為自動化前處理腳本，**絕不可替代步驟三之深層語意校對**！

### 步驟三：逐字稿深度語意校對與高可讀性排版（Deep Verbatim LLM Proofreading & Formatting）
- **100% 全篇原話保真**：完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**嚴禁任何刪減、摘要或文言縮寫**。
- **深度語意聽錯校正**：通讀上下文地毯式修正語音辨識荒謬同音字與專有名詞（如 `Proctored/unproctored`、`IPv6 世界`、`www.cisco.com`、`permit ip any any`、`deny`、`現在是一萬`、`巨匠多少錢？兩萬。`、`Webcam 可以看到` 等）。
- **自然語流排版**：消除破碎單句與突兀行尾，按 150～300 字組織為流暢閱讀段落，並消除孤立無意義狀聲詞。
- **結構化主題標題**：依授課脈絡插入 H2/H3 標題與語意 emoji。
- **元資料與防偽門禁**：補齊完整 YAML Frontmatter 與標準 Blockquote 宣告，並通過 `EntityGuard` 出處溯源檢查。
- 產出最終高品質純 Markdown：`{ShortTitle}-proofread.md`。

### 步驟四：技術精華架構提煉（Executive Summary & Architecture Extraction）
- 從完成之 `proofread.md` 提煉關鍵脈絡與心智模型。
- 繪製 Mermaid 概念圖、攻擊鏈或流程架構圖。
- 整理核心技術細節、代碼指令、重要表格與考試/實戰避坑重點。
- 產出結構化精華筆記：`{ShortTitle}-summary.md`。

### 步驟五：全局目錄索引與品質迴歸（Catalog Indexing & Quality Audit）
- 執行 `python -m transcript_processor index` 更新 `CATALOG.md` 與 `CATALOG.zh-TW.md`。
- 執行全套單元測試（`unittest discover tests`）確認零迴歸、零幻覺。

- **Proofreading Manual**: Detailed speech-to-text error correction patterns and directory/file naming conventions are defined in [`PROOFREAD_RULES.md`](PROOFREAD_RULES.md). Always consult it when proofreading transcripts or generating executive summaries.
- **Proofread Benchmark Standards**: All `*-proofread.md` deliverables must strictly adhere to the Verbatim Benchmark Formatting Standards defined in Section 6 of [`PROOFREAD_RULES.md`](PROOFREAD_RULES.md), including YAML Frontmatter, the standardized Blockquote statement, zero hallucination/injection, multi-paper sectioning, and explicit speaker attribution.
- **Scenario Profile First**: Agent must identify scenario profile (`single-talk`, `multi-paper`, `thesis-defense`, `lightning-talks`) before drafting proofread documents. Never treat multi-paper conference recordings as single-talk presentations.
- **Entity Verification Gate**: Proper nouns and person names (speakers, professors, advisors) MUST be verified with the user before writing final proofread documents. Never assume or write unverified ASR homophones directly.
- **Hardware & VRAM Safety**: Local ASR scripts MUST clamp CUDA memory allocation fraction (<= 0.60) to avoid GPU TDR resets and remote desktop disconnections.




## 🛡️ Mandatory Authorization Gate & Safety Boundaries

This is a hard safety boundary for every agent session.

### 1. Action Classification Before Any Tool Call
Before performing any tool call, categorize the intended action into one of three tiers:

- **Read-only**:
  - Inspect files, Git status/history, build/test logs, CI status, or external state.
  - *Status*: **Allowed by default**.
- **Local edit**:
  - Modify or create files only when explicitly requested by the user.
  - *Status*: Allowed for the requested scope. **Does NOT imply permission to commit, push, or publish**.
- **External mutation / Remote State Change**:
  - Any branch creation/switching, commit, push/force-push, tag modification, PR creation/merge, GitHub Actions workflow dispatch/cancel, release publishing, or external store deployment.
  - *Status*: **Requires explicit authorization from the user** in the current conversation turn.

### 2. Scope Non-Transitivity
- Authorization for operation A never extends to operation B. (e.g., authorizing a tag push does not authorize creating a PR or bumping versions).
- If an authorized operation fails and a different operation is needed, report the failure evidence and stop. Never expand authorization autonomously.
- If the user revokes or objects to an action, stop immediately. Never execute autonomous "cleanup" (such as deleting branches or force-pushing) without separate explicit authorization.

---

## 🧠 Problem-Solving Approach (Stop Brute Force)

When you encounter an error, test failure, build break, or unexpected state:

- **Do NOT** blindly guess or try random trial-and-error fixes. Each failed attempt without understanding the root cause is wasted effort.
- **DO** stop and observe the underlying mechanism first. Read the exact error stack trace, inspect the relevant source code, and consult documentation. Understand *why* it fails before attempting a fix.
- **DO** normalize the problem to its minimum reproducible unit. Verify the smallest possible piece first, then scale up.
- **DO** ask yourself: *"Am I diagnosing the root cause, or just hoping random edits will make it pass?"*


## 🧠 Persistent Memory Protocol

Every agent session must maintain continuity across sessions via `MEMORY.md`:

### 1. Start of Session (CRITICAL — Execute First)
- Read `MEMORY.md` in the workspace root at the beginning of the session.
- Absorb recorded user preferences, active tasks, project architectural context, and prior decisions.
- Do not ask the user to re-explain background details already documented in `MEMORY.md`.

### 2. End of Session
- Update `MEMORY.md` before ending:
  - Record new architectural decisions and rationale.
  - Update current active tasks and blockers.
  - Append a concise session history entry.
  - Preserve critical technical lessons learned and platform pitfalls.


## 📐 Git Discipline & Conventional Commits

### 1. Atomic Commits & Revert Test
- **One purpose per commit**: Never mix functional logic updates with formatting, comment cleanups, or asset moves in a single commit.
- **The Revert Test**: If change A can be reverted without breaking change B, they represent separate purposes and must be committed in separate batches.
- Even within the same file, split logically independent hunks (e.g. using `git add -p`).

### 2. Conventional Commit Formatting
All commit messages must strictly follow the Conventional Commits format:
```
<type>(<scope>): <subject>
or
<type>: <subject>

1. <Numbered English detail line 1>
2. <Numbered English detail line 2>
```

- **Allowed Types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `style`, `perf`, `security`
- **Rules**:
  - Header length: Maximum 72 characters.
  - No trailing period (`.`) at the end of the subject.
  - Avoid vague descriptions (`update`, `misc`, `fix bug`, `changes`).
  - Body must be a numbered list in English explaining technical rationale.

### 3. Safety Rules
- **NEVER** run `git push` or `git push --force` automatically. Only commit locally unless explicit push authorization is granted.
