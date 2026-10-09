# record-list Agent Rules & Developer Guidelines

You are a senior pair-programming AI assistant operating in the **record-list** codebase.
Follow the mandatory rules and engineering constraints outlined below.

## 🎙️ Transcript Proofreading Domain Rules (絕對鐵則，違者重做)

1. **逐字備查稿（`.full.md`）100% 原話保真，嚴禁任何人工總結或改寫**：
   - `.full.md` 的定位是 **100% 原始現場發言的忠實記錄**。
   - **嚴禁在 `.full.md` 中擅自替講者做摘要、總結、列點結論、或用書面語改寫原話！**
   - 所有的結構化分析、核心筆記、架構提煉與總結，**只能出現在主檔（`.md`）中**，絕不可污染 `.full.md`！

2. **同發言人連續發言必須依自然語意合理分段（150～300 字），嚴禁碎裂亦嚴禁千字大文字磚**：
   - 語音辨識（ASR）輸出常每 3~5 秒就切一空行，產生大量破碎單行（例如「對。」「好。」「這代表什麼意思？」單獨一行一行散落）。
   - **亦嚴禁走向另一極端，將講者數千字發言全部黏成一整坨不換行的大方塊！**
   - **正確做法**：在 **100% 保留全部原話** 的前提下，同一講者長發言應按其論述邏輯、主題轉換或投影片停頓，每 **150～300 字** 自然空行分段，維持極佳閱讀節奏。
   - 講者交替發言時換行並加粗角色標籤（如 `**【指導教授】**：`）。

3. **地毯式校對 ASR 語音同音錯字與技術名詞**：
   - 嚴格比對上下文修正同音錯字（如 `打 E S E` / `打頁子一` → `.exe`；`機號` → `GitHub`；`B I T` → `Git`；`第二開發` → `IDE`；`科索` → `Cursor`；`博科會` → `國科會`；`數專班` → `碩專班`）。
   - 詳細模式與規範參照 [`PROOFREAD_RULES.md`](PROOFREAD_RULES.md)。



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
