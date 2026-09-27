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

---

## 六、Summary 格式規範

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
