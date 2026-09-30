# 校對規則手冊（從實戰中累積）

> 本文件記錄校對逐字稿時發現的辨識錯誤模式與修正規則。
> 後續新檔案校對時，應優先比對這些已知模式。

---

## 零、目錄結構與命名規則

### 1. 全域組織架構

```text
record-list/
├── 4-University/                        ← 大學部核心領域（大一～大四，2025 年 6 月以前畢業）
│   ├── 1-Studies/                       ← 大一（基礎學科、通識先修、職涯發展）
│   │   ├── Fall-Semester/               ← 上學期（如 BasicMathematics, GeneralPhysics, GeneralBiologyLab, CareerDevelopment）
│   │   ├── Spring-Semester/             ← 下學期課程
│   │   └── Holiday/                     ← 寒暑假特殊活動/營隊
│   ├── 2-Curriculum/                    ← 大二（系定核心必修與實驗）
│   │   ├── Fall-Semester/               ← 上學期（如 CloudComputing, ComputerNetworks）
│   │   ├── Spring-Semester/             ← 下學期（如 ManagementInformationSystems）
│   │   └── Holiday/
│   ├── 3-Specialization/                ← 大三（專業領域選修、進階與認證培訓）
│   │   ├── Fall-Semester/               ← 上學期（如 IoTSecurity）
│   │   ├── Spring-Semester/             ← 下學期課程
│   │   └── Holiday/                     ← 寒暑假特殊培訓/活動（如 20250106-Cisco-CCNA1, 20250113-CompTIA-SecurityPlus）
│   └── 4-Capstone/                      ← 大四（畢業專題、專案管理、成果發表）
│       ├── Fall-Semester/               ← 上學期（如 ProjectManagement）
│       ├── Spring-Semester/             ← 下學期
│       └── Holiday/
│
├── 5-Master/                            ← 碩士班核心領域（2025 年 9 月入學，114 學年度起算）
│   ├── 1-First-Year/                    ← 碩一（課程必選修、專案會議、學術發表、暑假研討）
│   │   ├── Fall-Semester/               ← 碩一上（課程：SoftwareEngineering, DevOps, ComputerNetworkLab；活動：20251205-Deloitte-GenAI-Cybersecurity-Keynote, 20251208-UIC-XAI-Keynote）
│   │   ├── Spring-Semester/             ← 碩一下（課程：MachineLearning, HCI-UX, CTF-Security, AdvancedAI-Optimization, ResearchMethodology；活動：20260318-EnglishAI-Presentation, 20260327-NCU-IM-AcademicConference）
│   │   └── Holiday/                     ← 碩一暑假（活動：20260821-HITCON-2026）
│   ├── 2-Second-Year/                   ← 碩二（專題研討、資安深度選修、產業大會、學位研究）
│   │   ├── Fall-Semester/               ← 碩二上（課程：DatabaseSecurity；活動：20260922-DevDaysAsia-2026, 20260927-Intro-to-OSINT-CTI）
│   │   ├── Spring-Semester/             ← 碩二下
│   │   └── Holiday/
│   └── Laboratory/                      ← 實驗室專屬核心目錄
│       ├── Degree-Defense/              ← 碩士學位口試（如 20260714 DRAVILaMA 論文簡報與審查質詢）
│       ├── Project-Meeting/             ← 整合型/產學研究專案會議（如 20251003 研究計畫與平台規劃）
│       ├── Seminar/                     ← 專題討論（如 20260914 自動化漏洞修復 APR 報告）
│       └── Thesis-Progress/             ← 碩士論文研究進度研討（如 20260226 Android 惡意程式行為子圖檢測）
├── transcript_processor/                ← 核心處理器套件（Indexer, Linter, Structurer, Guard）
├── tests/                               ← 單元測試與回歸驗證套件
├── CATALOG.md / CATALOG.zh-TW.md        ← 全局自動化雙語目錄索引
├── PROOFREAD_RULES.md                   ← 本手冊（校對規範、命名手冊與字彙對照）
└── README.md / README.zh-TW.md          ← 專案總體說明文件
```

### 2. 目錄命名規則

* **年級目錄**：全採連號（連字號）
  * 大學部：`1-Studies`、`2-Curriculum`、`3-Specialization`、`4-Capstone`。
  * 碩士班：`1-First-Year`、`2-Second-Year`。
* **學期目錄**：`Fall-Semester`、`Spring-Semester`，以及存放寒暑假或特殊活動的 `Holiday`。
* **內層課程/活動目錄**：
  * **課程目錄**：直接寫「純課程名稱」，不重複年份或學期（例如 `BasicMathematics/`、`MachineLearning/`、`SoftwareEngineering/`、`ProjectManagement/`、`DatabaseSecurity/`）。
  * **活動目錄**：一律以「活動第一天日期 + 活動名稱」命名（例如 `20250106-Cisco-CCNA1/`、`20250113-CompTIA-SecurityPlus/`、`20260318-EnglishAI-Presentation/`、`20260821-HITCON-2026/`）。
* **實驗室目錄**：統一收整在 `5-Master/Laboratory/` 底下，依目的區分為 `Degree-Defense/`、`Project-Meeting/`、`Seminar/`、`Thesis-Progress/` 四大子目錄。

### 3. 檔案命名規範（方案 3-A 主從架構）

每個錄音場次標準化產出兩份純 Markdown 交付物，以「核心筆記為主體、原話逐字稿為備查」：

* **核心筆記/摘要（主檔，主力查閱）**：
  ```text
  {YYYYMMDD}[-{Seq}]-{Topic}.md
  ```
* **完整原話逐字稿（全文備查，100% 原話對照）**：
  ```text
  {YYYYMMDD}[-{Seq}]-{Topic}.full.md
  ```

| 欄位 | 說明與規則 | 範例 |
| :--- | :--- | :--- |
| `YYYYMMDD` | 錄音與課次具體日期。**一律採用 8 碼純數字，嚴禁使用 dash 分割年月日**。 | `20260302`, `20241015`, `20250106` |
| `Seq` | **時序序號**。若同一個目錄在同一天包含多個課次，加入 `01`, `02` 序號以確保檔案管理器依時序排列；若當天僅單一場次則省略。 | `01`, `02` |
| `Topic` | 該節具體核心主軸（2~6 個關鍵詞）。**徹底杜絕內部代號與雜湊殘留**（嚴禁 `NCU-IM-01`、`Lesson-293-300`、`Lab-Discovery12`、`勤業眾信副總` 等雜湊字眼）。 | `決策樹與ID3演算法`, `智慧醫療失智症預測`, `Pixel8A-GPU漏洞挖掘` |
| 副檔名 | 核心筆記主檔為 `.md`；完整逐字備查稿為 `.full.md`。 | `20260302-01-決策樹與ID3演算法.md`<br/>`20260302-01-決策樹與ID3演算法.full.md` |

### 4. 命名範例對照

| 類別與路徑 | 核心筆記（主檔 `.md`） | 完整原話逐字稿（備查 `.full.md`） |
| :--- | :--- | :--- |
| **大一上基礎數學**<br/>`4-University/1-Studies/Fall-Semester/BasicMathematics/` | `20241019-多項式變數代換與試題檢討.md` | `20241019-多項式變數代換與試題檢討.full.md` |
| **大三寒假 CCNA 認證**<br/>`4-University/3-Specialization/Holiday/20250106-Cisco-CCNA1/` | `20250106-01-靜態路由實作與主線備援切換.md`<br/>`20250106-02-VLSM子網切割與路由表運作原理.md` | `20250106-01-靜態路由實作與主線備援切換.full.md`<br/>`20250106-02-VLSM子網切割與路由表運作原理.full.md` |
| **碩一下機器學習**<br/>`5-Master/1-First-Year/Spring-Semester/MachineLearning/` | `20260302-01-決策樹與ID3演算法.md`<br/>`20260302-02-單純貝氏與SVM原理.md` | `20260302-01-決策樹與ID3演算法.full.md`<br/>`20260302-02-單純貝氏與SVM原理.full.md` |
| **碩一下英文專題發表**<br/>`5-Master/1-First-Year/Spring-Semester/20260318-EnglishAI-Presentation/` | `20260318-AI教育表現特徵工程與過濾法預測.md` | `20260318-AI教育表現特徵工程與過濾法預測.full.md` |
| **碩一暑期年會活動**<br/>`5-Master/1-First-Year/Holiday/20260821-HITCON-2026/` | `20260821-Pixel8A-GPU漏洞挖掘.md` | `20260821-Pixel8A-GPU漏洞挖掘.full.md` |
| **碩一學位口試審查**<br/>`5-Master/Laboratory/Degree-Defense/` | `20260714-DRAVILaMA論文簡報.md`<br/>`20260714-DRAVILaMA審查質詢-Part1.md` | `20260714-DRAVILaMA論文簡報.full.md`<br/>`20260714-DRAVILaMA審查質詢-Part1.full.md` |
| **碩二上資料庫安全**<br/>`5-Master/2-Second-Year/Fall-Semester/DatabaseSecurity/` | `20260914-PostgreSQL複寫協議提權漏洞.md` | `20260914-PostgreSQL複寫協議提權漏洞.full.md` |
| **碩二上微軟技術大會**<br/>`5-Master/2-Second-Year/Fall-Semester/20260922-DevDaysAsia-2026/` | `20260922-AI評測與UL315治理.md` | `20260922-AI評測與UL315治理.full.md` |

---

## 一、核心原則

1. **禁止精簡**：不刪減、不改寫任何語句，只修復辨識錯誤或補回缺失字詞
2. **保留原話**：講者的語氣轉折、口語贅字、重複、現場互動全部保留
3. **語境優先**：同一個縮寫在不同段落可能代表不同東西，必須看上下文決定
4. **先查原始稿**：遇到不確定的，先去看原始逐字稿比對
5. **專有名詞與人名確認閘門（Entity Verification Gate）**：語音辨識之人名、教授姓名、指導教授、特定發表題目等專有名詞，嚴禁自行揣測或直接寫入未經確認之同音錯字。產出交付文件前，**必須使用 `EntityGuard` 抽取候選人名清單並向使用者提請確認**，取得確認映射後始得注入校對管線。
6. **機構與活動出處溯源門禁（Institutional Provenance & Zero Hallucination）**：Frontmatter 元資料中之 `event`、`title`、`speakers` 若包含具體學校校名、系所、企業或單位組織（如「國立臺灣科技大學資訊工程系」、「中央大學資管系」），**其主體或關鍵詞必須在逐字稿本文或原始錄音語料中有字面可考的出處（Provenance）**。若錄音中未提及具體學校或系所，**一律嚴格使用客觀中性稱謂**（如 `event: "碩士學位論文口試審查會"`、`event: "技術學術研討會"`），嚴格禁止因其他場次講者之學校而跨場次腦補、推測或擅自掛名。
7. **跨場次名詞隔離原則（Cross-Session Entity Isolation）**：嚴格禁止將 A 演講場次中出現的背景資訊（例如 HITCON 閃電秀講者自稱就讀台科大）套用或遷移至 B 場次（例如學位論文口試）。每個錄音檔的實體皆具備獨立封閉的上下文空間，未經多方交叉驗證絕不互相污染。
8. **IP 位址、子網遮罩與連接埠數字化原則（Network Numeric Formatting）**：課堂口語中提及的 IP 八位元組、子網遮罩、前綴長度與介面網段（例如「點一二九」、「點一」、「十點一開頭」、「二五五點二五五點零」），一律規範化轉換為標準網路數字表示法（如 `.129`、`.1`、`10.1 開頭`、`255.255.255.0`、`/30`），避免中文數字混雜，確保專業技術文檔清晰易讀。


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

## 三、轉錄到交付之標準五階段作業流程（Standard 5-Stage Pipeline）

為確保最終產出具備一致的高規格品質與可讀性，所有轉錄校對工作**必須嚴格分步執行，嚴禁省略或將多步混淆跳過**：

### 階段一：語音辨識與原始轉錄（Raw ASR & CJK Normalization）
1. 透過本地 ASR（Qwen3-ASR 1.7B / Whisper）對音訊切片推論。
2. 產出 `transcribe_outputs/{folder}/raw_transcript.txt` 與初步繁中 `transcript_zh_tw.txt`。
3. **原則**：此階段為機器辨識之未加工語料（Scratch Material），不可直接交付。

### 階段二：標點規範與基底詞庫替換（Automated Pre-processing & Dictionary Normalization）
1. **標點與空白正規化（CJK Normalization）**：
   - 消除中文字元間異常產生的空格（如 `一 些 一 些` $\to$ `一些一些`）。
   - 將英文標點自動正規化為全形標點（`,` $\to$ `，`、`.` $\to$ `。`、`:` $\to$ `：`、`?` $\to$ `？`）。
   - 保留中英交界處之標準單一空格（如 `在 Android 系統中`）。
2. **語氣停頓斷句修復**：
   - 消除純附屬助詞前的誤加標點：`re.sub(r"[。！？，、；：]\s*([的得地著之])", r"\1", text)`。
3. **全域確定性詞庫初步替換**：
   - 對已明確之機構名稱、品牌進行初步替換（如 Cisco、CompTIA、Pearson VUE、OnVUE、巨匠、恆逸、聯成）。
4. **原則**：此階段為自動化腳本前處理，**絕不等同於校對排版完成**。

### 階段三：逐字稿深度語意校對與高可讀性排版（Deep Verbatim LLM Proofreading & Formatting）
1. **100% 全篇原話保真（Verbatim Fidelity）**：
   - 完整保留現場講者原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**。
   - 講者的語意轉折、思考停頓、口語真實感完全保留，嚴禁擅自改寫為文言或書面簡述。
2. **深度語意聽錯校正（Contextual Semantic Recovery）**：
   - 必須由模型通讀上下文，地毯式修復 ASR 因音近造成的嚴重語意扭曲，例如：
     - `Practice / unpracticed` $\to$ `Proctored / unproctored`（Pearson VUE 監考/非監考測驗）
     - `第二世界` $\to$ `IPv6 世界`、`B六` $\to$ `IPv6`
     - `這波單位點四十個點看` $\to$ `www.cisco.com`
     - `本地IPN` $\to$ `permit ip any any`、`抵耐` $\to$ `deny`
     - `四一萬` $\to$ `現在是一萬`、`巨一下多錢？二十。` $\to$ `巨匠多少錢？兩萬。`
     - `微。看可以看到` $\to$ `Webcam 可以看到`
3. **自然閱讀段落重構（Discourse Paragraphing）**：
   - 消除單句成段與突兀斷裂，依論述主題聚合為 150～300 字之流暢段落。
   - 徹底消除結尾或開頭殘留之孤立狀聲詞（如單獨一行「好。」「嗯。」）。
4. **結構化主題標題導航（Thematic Headings with Emojis）**：
   - 依授課脈絡劃分具代表性之 H2/H3 章節標題，並搭配主題 emoji（🎯、🔑、📊、🖥️、📜、📝、🔄、💡）。
5. **元資料與出處溯源門禁（Provenance Verification Gate）**：
   - 補齊完整 YAML Frontmatter（含 title, event, date, talk_id, speakers, type: "verbatim-narrative-transcript", verbatim: true, scenario, category, tags）。
   - 緊接 H1 下方插入標準排版說明 Blockquote。
   - 通過 `EntityGuard.verify_metadata_provenance()` 出處溯源檢查。
6. **最終產出**：`{ShortTitle}-proofread.md`。

### 階段四：技術精華架構提煉（Executive Summary & Architecture Extraction）
1. **提煉核心脈絡**：濃縮演講/課程之核心概念、攻擊情境或學習目標。
2. **視覺化圖表**：使用 Mermaid 繪製系統架構圖、攻擊流轉鏈或協定時序圖。
3. **技術精華深化**：整理核心技術細節、CLI 指令語法、對比表格與考點整理。
4. **關鍵總結與考試應對**：列出 3～5 點核心重點與避坑守則。
5. **最終產出**：`{ShortTitle}-summary.md`。

### 階段五：全局目錄索引與品質迴歸（Catalog Indexing & Quality Audit）
1. 執行 `python -m transcript_processor index`，自動掃描並更新 `CATALOG.md` 與 `CATALOG.zh-TW.md`。
2. 執行全套單元測試與防退化測試（`unittest discover tests`），確保 100% 通過。

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

### 2. 五大場景適配矩陣（Scenario Adapters Matrix）

在符合通用基底的前提下，依據音訊的互動模式與參與人數，動態套用對應的場景排版模板：

| 場景類型代碼 | 場景名稱 | 適用情境與範例 | 標題切分架構 | 發言角色標籤規則 | 儀程紀錄要求 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `classroom-lecture` | **課堂教學與實作工作坊** | 大學、補習班、訓練機構之課程教學（如 CCNA1、Security+、實機配置演練） | 依授課模組、主題技術點或實作階段切分（無生硬公文數字編號） | **明確標註師生互動**：章節開頭標註 `**【授課講師】**：`；遇課堂提問、學員回答、插話或互動，**嚴禁**包裹在同一段內，必須強制斷行標註 `**【學員】**：`（或 `**【學員 A/B】**：`） | 課前點名/設備說明、課堂練習、休息時間與課後問答 |
| `single-talk` | **單人技術演講** | 單一講者主講之研討會演講（如 HITCON 91-93、DevDays Asia 121-125） | 依講者之**技術演進大綱**切分（背景 $\to$ 成因 $\to$ 攻擊利用 $\to$ 防禦 $\to$ Q&A） | 章節開頭標註講者身分（如 `**【發表者 PK】**：`）；文末 `## ❓ 現場 Q&A 問答交流` 全面啟用角色標籤（`**【現場提問者】**：` / `**【講者】**：`） | 演講開場自介與文末致謝 |
| `multi-paper` | **多論文學術研討會** | 單一錄音包含多名發表者輪流報告與評審講評（如 20260327 Session G/H/I） | **雙層樹狀架構**：每篇論文設 `## 論文 X：{題目} ({發表人})`，後緊接 `## 🔬 論文 X 評審講評與 Q&A 交流` | **全程高密度標籤**：司儀、評審委員、各發表人、指導教授全程明確標註 | 司儀議程計時規範（舉牌／鈴響）、中場換場、評審總評、優秀論文公告與頒獎合影 |
| `thesis-defense` | **碩博學位論文口試** | 碩博士學位論文口試答辯（如 20260714 DRAVILaMA 錄音 60、61、62） | 依**口試程序**切分：<br/>• 錄音 60：學生完整報告章節<br/>• 錄音 61：各委員質詢答辯主題<br/>• 錄音 62：閉門審查決議與通過宣布 | 報告篇以章節切分；**答辯篇全程密集標註**（召集人／指導教授／口試委員／研究生），清楚呈現攻防點 | 口試程序開場宣告、閉門退席、復會決議宣讀與成績公布 |
| `lightning-talks` | **閃電秀短講合輯** | 多位講者每人 5-10 分鐘短講合輯（如 HITCON 94 閃電秀） | 採**合輯目錄制**，以 `## ⚡ 閃電秀 1：{題目} ({講者})` 獨立切分各場短講 | 於各短講開頭標註講者身分與自介，正文保持原話流暢 | 主持人開場引言、短講換場計時與閉幕 |

---

### 3. 場景識別第一原則（Scenario-First Identification Rule）

在對任何音訊執行轉錄校對前，必須遵守以下標準作業程序（SOP）：

1. **聽取與掃描特徵**：
   - 是否為課堂授課、包含講師講解、實機操作與學員應答？ $\implies$ 判定為 `classroom-lecture`。
   - 是否出現司儀宣告「下一位發表者是...」或「每位發表者共有二十分鐘」？ $\implies$ 判定為 `multi-paper`。
   - 是否出現召集人主持、口試委員輪流提問「我想請教沈同學兩個問題...」？ $\implies$ 判定為 `thesis-defense`。
   - 是否為多位講者連續簡短分享（5-10 分鐘且主題完全跳躍）？ $\implies$ 判定為 `lightning-talks`。
   - 是否為單一講者連續報告（僅結尾有短暫問答）？ $\implies$ 判定為 `single-talk`。
2. **嚴禁角色遺漏與模板錯套**：
   - 課堂教學（`classroom-lecture`）嚴禁缺少 `**【授課講師】**：`，嚴禁將學員回應吞沒在講師段落中。
   - 嚴禁將 `multi-paper` 當作 `single-talk` 處理（會導致後續發表論文被截斷遺失）。
   - 標題一律採用生動之「Emoji + 技術主題」，嚴禁使用死板的「一、」「二、」「三、」公文編號。

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
