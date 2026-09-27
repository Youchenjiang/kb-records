# 校對規則手冊（從實戰中累積）

> 本文件記錄校對逐字稿時發現的辨識錯誤模式與修正規則。
> 後續新檔案校對時，應優先比對這些已知模式。

---

## 零、目錄結構與命名規則

### 目錄結構

```
record-list/
├── {Category}/                          ← 分類（如 5-Master）
│   └── {YYYYMMDD}-{EventName}/          ← 活動（如 20260821-HITCON-2026）
│       ├── {ShortTitle}-proofread.md    ← 校對版逐字稿
│       └── {ShortTitle}-summary.md      ← 重點整理版
├── transcript_processor/                ← 核心處理器套件
├── scripts/                             ← 工具腳本
├── PROOFREAD_RULES.md
├── README.md
└── requirements.txt
```

### 命名規則

#### 活動目錄

```
{YYYYMMDD}-{EventName}/
```

| 欄位 | 說明 | 範例 |
|------|------|------|
| `YYYYMMDD` | 活動日期 | `20260821` |
| `EventName` | 活動名稱，英文簡寫 | `HITCON-2026` |

#### 檔案命名

```
{ShortTitle}-{type}.md
```

| 欄位 | 說明 | 範例 |
|------|------|------|
| `ShortTitle` | 演講主題簡稱，2-4 個關鍵詞用 `-` 連接，不超過 30 字 | `Pixel8A-GPU漏洞挖掘`、`AI評測與UL315治理` |
| `type` | `proofread`（校對版）或 `summary`（重點整理版） | |

### 當前檔案清單

| 活動 | 檔案 |
|------|------|
| `5-Master/20260821-HITCON-2026/` | 4 個主題共 8 個檔案（4 proofread + 4 summary） |
| `5-Master/20260922-DevDaysAsia-2026/` | 5 個主題共 10 個檔案（5 proofread + 5 summary） |
| `5-Master/20260714-MasterDefense-DRAVILaMA/` | 3 個主題共 6 個檔案（3 proofread + 3 summary） |
| `5-Master/20260327-AcademicConference/` | 3 個主題共 6 個檔案（3 proofread + 3 summary） |


### 新增活動時的步驟

1. 決定 `Category`：放在哪個分類下
2. 決定 `YYYYMMDD` 和 `EventName`
3. 建立目錄：`{Category}/{YYYYMMDD}-{EventName}/`
4. 新檔案可能是以下格式之一：
   - `.aac`（錄音檔）→ 用 `scripts/aac_to_mp3.py` 轉 mp3，再用 `scripts/format_transcript.py` 生成 proofread
   - `-raw.txt`（ASR 原始稿）→ 用 `scripts/run_deep_correction.py` 生成 proofread
   - `-formatted.md`（格式化版）→ 直接當 proofread 基礎，做語句級修正
5. 最終產出：`{ShortTitle}-proofread.md`（純 Markdown 交付物）
6. 從 proofread 提煉：`{ShortTitle}-summary.md`（純 Markdown 交付物）
7. **檔案生命週期與 Git 規範**：
   - 根目錄下的 raw txt、音訊檔皆為「一次性暫存輸入（Scratch Inputs）」，由 `.gitignore` 排除，**絕對不納入 Git 版本控制**。
   - 進入版本控制的只有 `5-Master/...` 底下的交付 Markdown、處理器工具鏈、測試以及說明文件。

### ShortTitle 命名範例

| 原始標題 | ShortTitle |
|---------|------------|
| Google Pixel 8A Mali GPU Driver 漏洞挖掘與提權實戰 | `Pixel8A-GPU漏洞挖掘` |
| POS 刷卡機魔改 ADB 與 AI 輔助挖 0-Day 實戰 | `POS-ADB-0Day-AI輔助` |
| 黑吃黑：瞄準資安研究員與紅隊的供應鏈攻擊 | `供應鏈攻擊-黑吃黑` |
| HITCON 2026 閃電秀全集（6 場短講合輯） | `閃電秀6場合輯` |

---

## 一、核心原則

1. **禁止精簡**：不刪減、不改寫任何語句，只修復辨識錯誤或補回缺失字詞
2. **保留原話**：講者的語氣轉折、口語贅字、重複、現場互動全部保留
3. **語境優先**：同一個縮寫在不同段落可能代表不同東西，必須看上下文決定
4. **先查原始稿**：遇到不確定的，先去看原始逐字稿比對
5. **專有名詞與人名確認閘門（Entity Verification Gate）**：語音辨識之人名、教授姓名、指導教授、特定發表題目等專有名詞，嚴禁自行揣測或直接寫入未經確認之同音錯字。產出交付文件前，**必須使用 `EntityGuard` 抽取候選人名清單並向使用者提請確認**，取得確認映射後始得注入校對管線。


---

## 零之一、硬體防護與 ASR 安全規範

本地執行 ASR 推論（如 Qwen3-ASR、Whisper）時，必須遵守以下硬體防護規範以防止系統崩潰：

1. **GPU 顯存鎖定（VRAM Cap）**：
   - 使用 `SafeASREngine` 或 `torch.cuda.set_per_process_memory_fraction(0.60)`。
   - 在 8GB VRAM 等消費級顯卡上，保留至少 3.2GB 供 Windows Desktop Window Manager (DWM) 與遠端桌面串流使用，**嚴防 GPU TDR 驅動重置引發遠端桌面斷線**。
2. **記憶體主動回收**：
   - 每個處理區塊或滑動窗口推論結束後，必須強制調用 `gc.collect()` 與 `torch.cuda.empty_cache()`。
3. **滑動窗口與重疊邊界（Sliding Window with Overlap）**：
   - 窗口切片長度建議設為 30~45 秒，並保留 1.5~2 秒重疊（Overlap），消除單詞剛好被截斷於窗口邊界的失真。


## 二、已知辨識錯誤模式

### A. 單字母被當成英文字母辨識（最常見、最致命）

| 辨識結果 | 可能是 | 判斷依據 |
|---------|--------|---------|
| `c` (小寫) | `Goon` / `context` / `C` | DEF CON 段落→Goon；kernel 段落→context |
| `d` | `DEF CON` / `device` / `debug` | Goon 段落→DEF CON；驅動段落→device |
| `DC` | `DEF CON` | Goon 相關段落全部改為 DEF CON |
| `S` | `Goons` / `Session` / `slab` | Goon 段落→Goons；漏洞利用→Session |
| `P` (獨立) | `PowerShell` / `page` | PowerShell 講者段落→PowerShell |
| `M` | `Mali` / `Mina` | GPU driver→Mali；Mina C2 講者→Mina |
| `B` | `buffer` / `badge` | 漏洞利用→buffer；Goon Badge→badge |
| `HP` | `Heap Spray` | 漏洞利用技巧 |
| `KP` | `kprobe` | debug 方法 |
| `PF` | `procfs` | debug 方法 |
| `CI` / `CI header` | `CFI` / `CFI header` | Control Flow Integrity |

### B. 截斷詞彙

| 辨識結果 | 應為 | 領域 |
|---------|------|------|
| `fship` | `first shift` | Goon 排班 |
| `reprovement` | `Recruitment` | 招募 |
| `execution` | `execution context` | PowerShell / kernel |
| `lass assembly` | `Inline assembly` | 組語 |
| `cfe` | `config option` | kernel 編譯選項 |
| `cment` | `Command` | C2 指令 |
| `ider` | `freelist` | slab allocator |
| `sebard` | `Sidebar` | UI |

### C. 同音字 / 近音字錯誤

| 辨識結果 | 應為 | 說明 |
|---------|------|------|
| `最超` | `最操` | Goon 工作很累 |
| `明天把` | `Mina C2` | ASR 把 Mina 聽成「明天」 |
| `無克蘭` | `烏克蘭` | 國名 |
| `服務正業` | `不務正業` | 講者自嘲 |
| `sfW` | `NSFW` | 內容警告 |
| `匯 tu` | `匯聚` | ASR 把「聚」聽成英文 |
| `一康` | `HITCON` | 會議名稱 |
| `漢街` | `焊接` | PCB 焊接體驗 |
| `PTB` | `PCB` | 電路板 |

### D. 技術術語被聽錯

| 辨識結果 | 應為 | 領域 |
|---------|------|------|
| `MFIC2` | `Mythic C2` | C2 框架 |
| `hvest` | `Harvest` | C2 功能 |
| `IS2048` | `RSA-2048` | 簽章驗證 |
| `bzvbx` | `BusyBox` | Linux 工具 |
| `公明器` | `蜂鳴器` | 硬體零件 |
| `nbof` / `BOX` | `ngrok` | 內網穿透 |
| `Cver` | `Cobalt Strike` | 紅隊工具 |
| `migation` | `mitigation` | 緩解措施 |

---

## 三、校對流程

1. **詞級替換**：腳本批量修已知單詞錯誤
2. **語句級替換**：腳本批量修上下文相關句子
3. **人工掃描**：檢查每段前兩句、英文夾雜段落、數字段落
4. **比對原始稿**：不確定的地方去原始逐字稿比對

---

## 四、校對腳本注意事項

1. 腳本只跑一次，同一替換不要跑兩次
2. 用 `replace(old, new, 1)` 只替換第一個
3. 先 `py_compile` 確認語法正確再執行
4. 先做 backup
5. old string 找不到 = 已被之前修過，跳過即可

---

## 五、容易被忽略的「正確但看起來奇怪」的內容

- `撞爆豬肉` — CTF 答案
- `A49` — DEF CON 亞洲組織
- `S` 作為講者代號 — 真的是 S
- `D1DB` — 參與者 ID
- `4848` — 頭貼解析度
- 講者口語重複 — 保留原話

## 六、Proofread 格式化設計規範（Verbatim Benchmark Standards）

從原始音訊或轉錄初稿生成的 `*-proofread.md` 必須嚴格遵循「**通用基底規範（Universal Core）＋ 場景適配矩陣（Scenario Adapters）**」之架構體系，確保不同類型活動音訊具備一致的工程化底線與精準的排版形態。

### 1. 通用基底規範（Universal Core Protocol）

無論任何錄音場景，以下四項要求為絕對約束：

1. **YAML Frontmatter 元資料齊全**：
   ```yaml
   ---
   title: "完整演講或研討會主題名稱"
   event: "活動或研討會場次名稱 (如 技術學術研討會 Session G)"
   talk_id: "錄音序號或議程編號 (如 '237', '91')"
   speakers: ["發言者清單，含司儀、評審、發表人、指導教授"]
   type: "verbatim-narrative-transcript"
   verbatim: true
   ---
   ```
2. **標準排版聲明區塊（Blockquote）**：
   緊接 H1 標題下方宣告：
   ```markdown
   > **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄現場所有講者原話發言、語意轉折、現場互動、提問質詢、答辯攻防與評定決議，**未做任何刪減、摘要或人工造假注入**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、術語縮寫與標點符號，明確標註發言角色（口試委員／指導教授／研究生／發表人／大會司儀），並完成舒適流暢的段落劃分與主題標題標註。
   ```
3. **零虛構與零人造注入原則（Zero Hallucination & Zero Injection）**：
   - **嚴禁腦補或插入虛構字句**：絕對不得任意添加未在錄音中發生的開場狀聲詞（如 `呃呃呃！`）或生硬的假問答（如在司儀規則宣導中插入評審問答）。
   - **保留口語真實性**：完整保留講者停頓、玩笑（如「中央大學 NCU 耶」、「反手耶」、「小學長不是大學長」）、即席互動與口頭禪，僅修復語音辨識聲學錯字，絕不改寫為書面語或進行語句壓縮。
4. **專業術語保真度**：
   - 涉及 AI、資訊安全、醫療、金融之領域專有名詞與縮寫（如 FCG、Obfuscapk、wav2vec 2.0、AST、Mel-spectrogram、Granger Causality、ZKP、aMCI 等），必須結合學術上下文嚴謹還原，嚴禁保留拼音或同音錯字（如禁止將「混淆」寫成「回撥」、將「函數呼叫圖」寫成「方圈拓撲」等）。

---

### 2. 四大場景適配矩陣（Scenario Adapters Matrix）

在符合通用基底的前提下，依據音訊的互動模式與參與人數，動態套用對應的場景排版模板：

| 場景類型代碼 | 場景名稱 | 適用情境與範例 | 標題切分架構 | 發言角色標籤規則 | 儀程紀錄要求 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `single-talk` | **單人技術演講** | 單一講者主講之研討會演講（如 HITCON 91-93、DevDays Asia 121-125） | 依講者之**技術演進大綱**切分（背景 $\to$ 成因 $\to$ 攻擊利用 $\to$ 防禦 $\to$ Q&A） | **正文不標註角色前綴**以維持閱讀流暢度；僅文末 `## ❓ 現場 Q&A 問答交流` 啟用角色標籤 | 演講開場自介與文末致謝 |
| `multi-paper` | **多論文學術研討會** | 單一錄音包含多名發表者輪流報告與評審講評（如 20260327 Session G/H/I） | **雙層樹狀架構**：每篇論文設 `## 論文 X：{題目} ({發表人})`，後緊接 `## 🔬 論文 X 評審講評與 Q&A 交流` | **全程高密度標籤**：司儀、評審委員、各發表人、指導教授全程明確標註 | 司儀議程計時規範（舉牌／鈴響）、中場換場、評審總評、優秀論文公告與頒獎合影 |
| `thesis-defense` | **碩博學位論文口試** | 碩博士學位論文口試答辯（如 20260714 DRAVILaMA 錄音 60、61、62） | 依**口試程序**切分：<br/>• 錄音 60：學生完整報告章節<br/>• 錄音 61：各委員質詢答辯主題<br/>• 錄音 62：閉門審查決議與通過宣布 | 報告篇以章節切分；**答辯篇全程密集標註**（召集人／指導教授／口試委員／研究生），清楚呈現攻防點 | 口試程序開場宣告、閉門退席、復會決議宣讀與成績公布 |
| `lightning-talks` | **閃電秀短講合輯** | 多位講者每人 5-10 分鐘短講合輯（如 HITCON 94 閃電秀） | 採**合輯目錄制**，以 `## ⚡ 閃電秀 1：{題目} ({講者})` 獨立切分各場短講 | 於各短講開頭標註講者身分與自介，正文保持原話流暢 | 主持人開場引言、短講換場計時與閉幕 |

---

### 3. 場景識別第一原則（Scenario-First Identification Rule）

在對任何音訊執行轉錄校對前，必須遵守以下標準作業程序（SOP）：

1. **聽取與掃描特徵**：
   - 是否出現司儀宣告「下一位發表者是...」或「每位發表者共有二十分鐘」？ $\implies$ 判定為 `multi-paper`。
   - 是否出現召集人主持、口試委員輪流提問「我想請教沈同學兩個問題...」？ $\implies$ 判定為 `thesis-defense`。
   - 是否為多位講者連續簡短分享（5-10 分鐘且主題完全跳躍）？ $\implies$ 判定為 `lightning-talks`。
   - 是否為單一講者連續報告（僅結尾有短暫問答）？ $\implies$ 判定為 `single-talk`。
2. **嚴禁模板錯套**：
   - 嚴禁將 `multi-paper` 當作 `single-talk` 處理（會導致後續發表論文被截斷遺失）。
   - 嚴禁將 `single-talk` 當作對話體處理（會導致正文充斥冗餘的逐句發言人標籤）。

---

## 七、Summary 格式規範

從 proofread 提煉出的 summary.md 應遵循以下格式：

### 結構

```markdown
# 🎤 {ID} {完整演講標題} ({講者})

> **演講主題**：一句話描述核心內容
> **講者**：名字（背景）
> **關鍵技術**：主要用到的技術/工具
> **達成效果**：最終成果

---

## 🎯 核心概念 / 攻擊情境

（用 Mermaid flowchart 畫出整體架構或攻擊路徑）

---

## 🔬 技術細節

（分段落講解，每段有明確標題）
（關鍵代碼用 code block 展示）
（重要概念用列表或表格整理）

---

## 💡 關鍵總結與啟示

（3-5 個要點，每點一句話）
```

### 格式要點

1. **Mermaid 圖表**：攻擊流程、架構圖用 `mermaid` code block 畫
2. **Metadata 區塊**：開頭用 blockquote 列出講者、主題、效果
3. **技術深度**：不要只列標題，要解釋**為什麼**和**怎麼做**
4. **代碼區塊**：關鍵指令、漏洞成因用 code block 呈現
5. **Emoji 標題**：用 emoji 幫助視覺區分章節
6. **不超過 proofread 的內容**：summary 是提煉，不是重新發明
