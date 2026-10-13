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
│   ├── 4-Capstone/                      ← 大四（畢業專題、專案管理、成果發表）
│   │   ├── Fall-Semester/               ← 上學期（如 ProjectManagement）
│   │   ├── Spring-Semester/             ← 下學期
│   │   └── Holiday/
│   ├── 5-Extracurricular/               ← 課外考察與實地調查（如 NatureEcologyClub）
│   └── Archive/                         ← 大學部非學術常規與日常行政封存區
│
├── 5-Master/                            ← 碩士班核心領域（2025 年 9 月入學，114 學年度起算）
│   ├── 1-First-Year/                    ← 碩一（課程必選修、專案會議、學術發表、暑假研討）
│   │   ├── Fall-Semester/               ← 碩一上（課程：SoftwareEngineering, DevOps, ComputerNetworkLab；活動：20251205-Deloitte-GenAI-Cybersecurity-Keynote, 20251208-UIC-XAI-Keynote）
│   │   ├── Spring-Semester/             ← 碩一下（課程：MachineLearning, HCI-UX, CTF-Security, AdvancedAI-Optimization, ResearchMethodology；活動：20260318-EnglishAI-Presentation, 20260327-NCU-IM-AcademicConference）
│   │   └── Holiday/                     ← 碩一暑假（活動：20260821-HITCON-2026）
│   ├── 2-Second-Year/                   ← 碩二（專題研討、資安深度選修、產業大會、學位研究）
│   │   ├── Fall-Semester/               ← 碩二上（活動：20260922-DevDaysAsia-2026, 20260927-Intro-to-OSINT-CTI）
│   │   ├── Spring-Semester/             ← 碩二下
│   │   └── Holiday/
│   ├── Laboratory/                      ← 實驗室專屬核心目錄
│   │   ├── Degree-Defense/              ← 碩士學位口試（如 20260714 DRAVILaMA 論文簡報與審查質詢）
│   │   ├── Project-Meeting/             ← 整合型/產學研究專案會議（如 20251003 研究計畫與平台規劃）
│   │   ├── Security-News/               ← 資安與漏洞新聞研討（如 20260914 PostgreSQL 複寫協議提權漏洞）
│   │   ├── Seminar/                     ← 專題討論（如 20260914 自動化漏洞修復 APR 報告）
│   │   └── Thesis-Progress/             ← 碩士論文研究進度研討（如 20260226 Android 惡意程式行為子圖檢測）
│   └── Archive/                         ← 碩士班會前日常閒聊與生活雜務封存區
├── audio/                               ← 音訊生命週期管理（pending: 待處理, processed: 已交付, preserved: 純音樂隔離）
├── transcript_processor/                ← 核心處理器套件（Indexer, Linter, Structurer, Guard, Splitter）
├── tests/                               ← 單元測試與回歸驗證套件（44 項測試）
├── CATALOG.md / CATALOG.zh-TW.md        ← 全局自動化雙語目錄索引（172 場會議與課程）
├── PROOFREAD_RULES.md                   ← 本手冊（校對規範、命名手冊與字彙對照）
└── README.md / README.zh-TW.md          ← 專案總體說明文件
```

### 2. 目錄命名規則

* **年級目錄**：全採連號（連字號）
  * 大學部：`1-Studies`、`2-Curriculum`、`3-Specialization`、`4-Capstone`。
  * 碩士班：`1-First-Year`、`2-Second-Year`。
* **學期目錄**：`Fall-Semester`、`Spring-Semester`，以及存放寒暑假或特殊活動的 `Holiday`。
* **內層課程/活動目錄**：
  * **課程目錄**：直接寫「純課程名稱」，不重複年份或學期（例如 `BasicMathematics/`、`MachineLearning/`、`SoftwareEngineering/`、`ProjectManagement/`）。
  * **活動目錄**：一律以「活動第一天日期 + 活動名稱」命名（例如 `20250106-Cisco-CCNA1/`、`20250113-CompTIA-SecurityPlus/`、`20260318-EnglishAI-Presentation/`、`20260821-HITCON-2026/`）。
* **實驗室目錄**：統一收整在 `5-Master/Laboratory/` 底下，嚴格依會議性質與主講權責區分為以下五大子目錄（嚴禁混放或自創重疊目錄）：

| 實驗室子目錄 | 嚴格收錄判準與邊界定義 | 強制檢驗規則 |
| :--- | :--- | :--- |
| `Degree-Defense/` | **碩博士學位論文口試**：含口試前夕設備架設、評分點交、全真預演、正式口試簡報、口試委員質詢攻防與閉門修訂覆盤。 | 必須為學位論文口試直接相關議程。 |
| `Thesis-Progress/` | **侑宸（Youchen）個人碩士論文進度**：僅限當事人「侑宸」向指導教授報告個人碩論架構、假設公式、測試矩陣與實驗進度之場次。 | 逐字稿內**強制包含 `**【侑宸】**：` 主講段落**；同儕報告或外部資安新聞嚴禁放入。 |
| `Project-Meeting/` | **整合型／產學研究專案與實驗室例會**：多人跨組專案（如容錯系統 VPS、AI 文獻知識圖譜平台、APK 免疫疫苗、AdMIL 感測器防禦）、研究方法訓練、新生交接與經費行政協調。 | 凡屬實驗室全體例會、同儕專案進度或產學合作研討皆歸入此處。 |
| `Security-News/` | **外部資安漏洞與威脅情報研討**：針對真實世界最新 CVE 漏洞、APT 攻擊鏈或惡意軟體案例（如 PostgreSQL 複寫提權、Cursor IDE 路徑劫持、惡意 Custom GPT RAT 釣魚鏈）之技術剖析。 | 主軸為外部真實資安事件或漏洞分析，而非個人學位論文方法。 |
| `Seminar/` | **外部學術論文精讀研討（Paper Reading）**：針對頂會／期刊發表之外部學術論文（如 APR 自動化漏洞修復、RAG 幻覺緩解、Kernel Multi-Hunk 跨檔案修補）進行方法論與實驗精讀。 | 主軸為單篇或多篇外部學術文獻之導讀與批判性討論。 |

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
| **碩一暑期年會活動**<br/>`5-Master/1-First-Year/Holiday/20260821-HITCON-2026/` | `20260821-01-Pixel8A-GPU漏洞挖掘.md` | `20260821-01-Pixel8A-GPU漏洞挖掘.full.md` |
| **碩一學位口試審查**<br/>`5-Master/Laboratory/Degree-Defense/` | `20260714-DRAVILaMA論文簡報.md`<br/>`20260714-DRAVILaMA審查質詢-Part1.md` | `20260714-DRAVILaMA論文簡報.full.md`<br/>`20260714-DRAVILaMA審查質詢-Part1.full.md` |
| **碩二上資安新聞研討**<br/>`5-Master/Laboratory/Security-News/` | `20260914-PostgreSQL複寫協議提權漏洞.md` | `20260914-PostgreSQL複寫協議提權漏洞.full.md` |
| **碩二上微軟技術大會**<br/>`5-Master/2-Second-Year/Fall-Semester/20260922-DevDaysAsia-2026/` | `20260922-AI評測與UL315治理.md` | `20260922-AI評測與UL315治理.full.md` |

---

## 一、核心原則與交付鐵則

1. **嚴禁人工摘要或改寫（Anti-Summarization & Anti-Paraphrasing Protocol）**：
   - 逐字備查稿（`.full.md`）必須 **100% 忠實還原原始發言原話**。
   - **絕對禁止** 在 `.full.md` 中擅自替講者做「總結」、「精簡摘要」、「條列結論」或以人工書面語改寫替代原話！
   - 摘要與結構化筆記只能出現在主檔（`.md`），不得污染 `.full.md`。
2. **同發言人連續發言之自然語意分段（Discourse Paragraphing Protocol，150～300 字）**：
   - **嚴禁兩大極端**：
     - ❌ **嚴禁逐句碎裂斷行**（每一句 3~5 秒就換一行，散落成上千碎行）。
     - ❌ **嚴禁整篇塞成一坨千字大文字磚**（同一講者發言 5~10 分鐘全部不換行黏成巨大方塊）。
   - **正確做法**：
     - 在 **100% 保留所有口語原話** 的前提下，同一位講者長時間連續發言時，應依據其 **論述邏輯、主題轉折、投影片切換或自然語意停頓**，劃分為 **150～300 字左右之清晰自然段落**，段落間以標準空行區隔。
     - 當切換不同講者時，換行並標註加粗角色標籤（如 `**【指導教授】**：`）。同一講者後續連續段落則作為該講者之自然段落延續排版。
3. **保留 100% 原始口語字句**：
   - 講者的語氣轉折、口語贅字、重複、疑問、現場問答互動全部保留，不刪減任何語意。
4. **地毯式校對 ASR 語音同音錯字與技術術語（Rigorous Phonetic & Tech Terminology Proofreading）**：
   - 轉錄文本常出現同音錯字（如 `打 E S E` / `打頁子一` → `.exe`；`機號` → `GitHub`；`B I T` → `Git`；`第二開發` → `IDE`；`科索` → `Cursor`；`博科會` → `國科會`；`數專班` → `碩專班`）。
   - 必須深入結合語境（資安、機器學習、網路、工程架構）將所有同音錯字修正為正確術語，絕不留下錯漏。
5. **語境優先**：同一個縮寫在不同段落可能代表不同東西，必須看上下文決定。
6. **先查原始稿**：遇到不確定的，先去看原始逐字稿比對。
7. **專有名詞與人名確認閘門（Entity Verification Gate）**：語音辨識之人名、教授姓名、指導教授、特定發表題目等專有名詞，嚴禁自行揣測或直接寫入未經確認之同音錯字。產出交付文件前，**必須使用 `EntityGuard` 抽取候選人名清單並向使用者提請確認**，取得確認映射後始得注入校對管線。
8. **機構與活動出處溯源門禁（Institutional Provenance & Zero Hallucination）**：Frontmatter 元資料中之 `event`、`title`、`speakers` 若包含具體學校校名、系所、企業或單位組織（如「國立臺灣科技大學資訊工程系」、「中央大學資管系」），**其主體或關鍵詞必須在逐字稿本文或原始錄音語料中有字面可考的出處（Provenance）**。若錄音中未提及具體學校或系所，**一律嚴格使用客觀中性稱謂**（如 `event: "碩士學位論文口試審查會"`、`event: "技術學術研討會"`），嚴格禁止因其他場次講者之學校而跨場次腦補、推測或擅自掛名。
9. **跨場次名詞隔離原則（Cross-Session Entity Isolation）**：嚴格禁止將 A 演講場次中出現的背景資訊（例如 HITCON 閃電秀講者自稱就讀台科大）套用或遷移至 B 場次（例如學位論文口試）。每個錄音檔的實體皆具備獨立封閉的上下文空間，未經多方交叉驗證絕不互相污染。
10. **IP 位址、子網遮罩與連接埠數字化原則（Network Numeric Formatting）**：課堂口語中提及的 IP 八位元組、子網遮罩、前綴長度與介面網段（例如「點一二九」、「點一」、「十點一開頭」、「二五五點二五五點零」），一律規範化轉換為標準網路數字表示法（如 `.129`、`.1`、`10.1 開頭`、`255.255.255.0`、`/30`），避免中文數字混雜，確保專業技術文檔清晰易讀。
11. **單一主題單一檔案與時序拆分原則（Session Topic Atomicity & Seq Protocol）**：
    - 一個 `.full.md` 與 `.md` 只能承載**單一獨立的研究主題、課堂單元或報告人進度**。
    - 嚴禁為了圖省事，將同一場會議中「不同研究生的論文進度」、「不同講者的獨立演講」黏合成一個幾萬字的大雜燴檔案。
    - 凡出現會議交接信號詞（如：「謝謝上一位同學」、「接下來請...」、「下一位換誰」、「好，那我現在就請...」），必須強制拆分為獨立檔案，並以時序序號（`{YYYYMMDD}-01-...`、`{YYYYMMDD}-02-...`）分別歸檔，各自獨立配對雙版本文件。
12. **多主題邊界與報告人切換檢驗（Multi-Topic & Multi-Presenter Boundary Gate）**：
    - 長錄音（尤其是超過 30 分鐘之會議、實驗室大會、Seminar）嚴禁視為單一講者連續報告。
    - 一旦拆分或偵測到換人發言，必須重新校準該階段的主講者身份標籤，嚴禁整篇沿用單一 `**【報告研究生】**：`。
13. **關鍵人物與當事人實體校準原則（Core Entity & Youchen Identification Protocol）**：
    - 本知識庫之核心主體為「侑宸（Youchen）」，ASR 語音辨識常因口音將「侑宸」辨識為同音異字（如：`右耳`、`又成`、`有成`、`右臣`、`幼辰`）。
    - 稽核時必須建立專屬校準規則：凡出現指導教授點名、同儕稱呼上述同音字時，一律精確修正為 `侑宸`，且該報告段落之發言人標籤必須明確標註為 `**【侑宸】**：`，不得使用模糊的泛稱。
14. **指導教授打斷與交互質詢還原原則（Adviser Interruption & Discourse Turn-Taking）**：
    - 嚴禁透過文字字數強行將一問一答合併為同一角色的大段落！
    - 指導教授之發言特徵極為顯著（例如短句質詢：「所以你意思是？」、「什麼叫增量？」、「這張表是 AI 產生的還是你自己想的？」、「不要急」、「先不要打斷」）。
    - 凡出現質詢句式或角色切換標記，即便該發言只有 10～30 字，亦必須獨立換行並標註 `**【指導教授】**：`，緊接著學生回答標註 `**【侑宸】**：`，完整還原真實口試與 Meeting 的攻防現場。
15. **摘要拒絕空泛套版（Zero Generic Boilerplate in Executive Summary）**：
    - 摘要檔（`.md`）之「關鍵重點」與「核心提要」嚴禁出現「深入檢視問題根源」、「針對演算法提出系統性評估」等泛用套版廢話。
    - 必須提取該場會議的具體實質爭點（如：CVE 編號、H1/H2 優惠券測試矩陣、狀態假設公式、白箱與黑箱假設衝突、口委質詢核心）。
    - 嚴禁在摘要末尾出現「（如需查閱現場一字不漏...）」等生硬指引。
16. **多角色聲紋/話輪交叉驗證防護（Speaker Turn Verification Guard）**：
    - 嚴禁使用「每 N 段自動輪替一次講者」之偽標註腳本。
    - 若錄音環境為師生會議，必須根據詞彙情境（如誰在說「謝謝老師」、誰在說「你們回去改」）進行語意權責對齊。
17. **逐字稿與摘要嚴格序列隔離原則（Strict Sequential Isolation: Verbatim First, Summary Second）**：
    - **絕對禁止同時生成或同時修改 `.full.md`（逐字稿）與 `.md`（摘要）！**
    - **先完成逐字稿（Phase A）**：必須先將 `.full.md` 的單一主題拆分、ASR 同音錯字校正、角色話輪標註、自然語意分段（150～300 字）與**具實質技術語意的 `##`（H2）/ `###`（H3）章節切分**全部整理完畢並通過驗證。
    - **後分段研究寫摘要（Phase B）**：唯有在 `.full.md` 結構 100% 定稿後，才允許逐段研讀 `.full.md` 的各個 `##` 章節，將每個章節的實質技術細節、公式、指令、發表內容與師生問答攻防，**逐章對應提煉**至 `.md` 摘要中。
18. **逐字稿語意章節切分與密度規範（Semantic Chapter Segmentation & Density Protocol for `.full.md`）**：
    - **嚴禁無章節大文字牆**：凡正文字數 `> 2,500` 字之 `.full.md`，全篇必須包含**至少 2 個以上**具實質技術語意的 `##`（H2）章節標題（`Archive/` 簡短日常紀錄除外）。
    - **控制單章節跨度（Chapter Span Cap）**：長篇逐字稿必須隨議程推進、投影片切換、子題轉折或教授質詢階段切分 `##`（H2）與 `###`（H3）標題，平均每個 `##` 章節跨度應控制在 **1,500～5,000 字以內**（單一 H2 區間最高不得超過 8,000 字），嚴禁將數萬字塞在同一個 H2 下而不切分。
    - **嚴禁機械式假標題與重複流水號**：絕對禁止在 `.full.md` 中使用 `## 💻 章節段落 01`、`## 🚀 章節段落 02`、`現場原話實錄與核心論述`、`逐字記錄` 等無實質內容的佔位符標題，亦禁止在同一檔案內重複套用相同名稱之 H2 標題。


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

### 階段三：逐字稿深度語意校對、單一主題拆分與章節切分（Deep Verbatim Proofreading & Semantic Sectioning）
> **【強制序列隔離門禁】**：階段三（`.full.md`）與階段四（`.md`）**絕對禁止同時處理**！必須先將 `.full.md` 100% 整理定稿並通過逐字稿驗證門禁後，始得進入階段四。

1. **單一主題拆分（Topic Atomicity Gate）**：
   - 若原始錄音包含多位報告人進度、多場閃電秀或跨主題議程，必須先依第八節執行無損拆分，確保每份 `.full.md` 僅承載單一主題。
2. **100% 全篇原話保真（Verbatim Fidelity）**：
   - 完整保留現場講者原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**。
   - 講者的語意轉折、思考停頓、口語真實感完全保留，嚴禁擅自改寫為文言或書面簡述。
3. **深度語意聽錯校正（Contextual Semantic Recovery）**：
   - 必須由模型通讀上下文，地毯式修復 ASR 因音近造成的嚴重語意扭曲，例如：
     - `Practice / unpracticed` $\to$ `Proctored / unproctored`（Pearson VUE 監考/非監考測驗）
     - `第二世界` $\to$ `IPv6 世界`、`B六` $\to$ `IPv6`
     - `這波單位點四十個點看` $\to$ `www.cisco.com`
     - `本地IPN` $\to$ `permit ip any any`、`抵耐` $\to$ `deny`
     - `四一萬` $\to$ `現在是一萬`、`巨一下多錢？二十。` $\to$ `巨匠多少錢？兩萬。`
     - `微。看可以看到` $\to$ `Webcam 可以看到`
4. **自然閱讀段落重構與話輪標註（Discourse Paragraphing & Turn-Taking）**：
   - 消除單句成段與突兀斷裂，依論述主題聚合為 150～300 字之流暢段落（單段最高不得超過 800 字）。
   - 遇到指導教授打斷、提問或學員互動，即便僅 10～30 字亦必須獨立換行標註角色（如 `**【指導教授】**：`、`**【侑宸】**：`）。
   - 徹底消除結尾或開頭殘留之孤立狀聲詞（如單獨一行「好。」「嗯。」）。
5. **結構化語意章節切分（Semantic Chapter Segmentation）**：
   - 依授課脈絡、投影片推進或討論轉折，劃分具代表性之 `##`（H2）與 `###`（H3）章節標題，並搭配主題 emoji（🎯、🔑、📊、🖥️、📜、📝、🔄、💡）。
   - **嚴禁機械式假標題**：絕對禁止使用 `## 💻 章節段落 01`、`現場原話實錄與核心論述`、`逐字記錄` 或重複相同標題洗版。
   - **章節密度要求**：正文字數 `> 2,500` 字之 `.full.md` 至少須有 2 個 H2 章節；長篇逐字稿平均每個 H2 章節跨度控制在 1,500～5,000 字以內（單一 H2 區間不得超過 8,000 字）。
6. **元資料與出處溯源門禁（Provenance Verification Gate）**：
   - 補齊完整 YAML Frontmatter（含 title, event, date, talk_id, speakers, type: "verbatim-narrative-transcript", verbatim: true, scenario）。
   - 緊接 H1 下方插入標準排版說明 Blockquote，並通過 `EntityGuard.verify_metadata_provenance()` 出處溯源檢查。
7. **最終產出**：`{YYYYMMDD}[-{Seq}]-{Topic}.full.md`。

### 階段四：基於逐字稿章節之知識體裁摘要提煉（Chapter-Driven Genre Summary Extraction）
> **【前置條件】**：僅在對應之 `.full.md` 已完成階段三之語意章節切分後，方可啟動本階段。

1. **逐章對應精讀（Chapter-by-Chapter Analysis）**：
   - 逐一讀取 `.full.md` 內已切分好的每一個 `##`（H2）/ `###`（H3）章節，提取該章節之實質公式、指令、系統設計、實驗數據與師生攻防問答。
   - **嚴禁脫離逐字稿章節憑空捏造或僅看檔名寫兩句空話**。
2. **套用第七節「五大知識體裁」架構**：
   - 依據場次性質選擇對應體裁（A. 研究進度与口試、B. 資安漏洞與技術演講、C. 理論課程與認證實作、D. 單篇論文研討、E. 多組專題發表），撰寫具高檢索價值的結構化筆記。
3. **最終產出**：`{YYYYMMDD}[-{Seq}]-{Topic}.md`。

### 階段五：全局目錄索引與品質迴歸（Catalog Indexing & Quality Audit）
1. 執行 `python -m transcript_processor index`，自動掃描並更新 `CATALOG.md` 與 `CATALOG.zh-TW.md`。
2. 執行全套自動化測試與防退化驗證（`python -m pytest tests/ -q` 及 `python scripts/self_check.py`），確保 100% 通過。

---

## 四、校對腳本注意事項

1. 腳本只跑一次，同一替換不要跑兩次
2. 用 `replace(old, new, 1)` 只替換第一個
3. 先 `py_compile` 確認語法正確再執行
4. 先做 backup
5. old string 找不到 = 已被之前修過，跳過即可
6. **寫入含 LaTeX 或正則之字串時，一律使用 Python raw string (`r"""..."""`)**，嚴防 `\to`, `\frac`, `\rfloor`, `\theta`, `\times` 被轉義為控制字元（`\x09`, `\x0c`, `\r`）。

---

## 五、容易被忽略的「正確但看起來奇怪」的內容

- `撞爆豬肉` — CTF 答案
- `A49` — DEF CON 亞洲組織
- `S` 作為講者代號 — 真的是 S
- `D1DB` — 參與者 ID
- `4848` — 頭貼解析度
- 講者口語重複 — 保留原話

## 六、Proofread 格式化設計規範（Verbatim Benchmark Standards）

從原始音訊或轉錄初稿生成的 `*.full.md` 必須嚴格遵循「**通用基底規範（Universal Core）＋ 場景適配矩陣（Scenario Adapters）**」之架構體系，確保不同類型活動音訊具備一致的工程化底線與精準的排版形態。

### 1. 通用基底規範（Universal Core Protocol）

無論任何錄音場景，以下四項要求為絕對約束：

1. **YAML Frontmatter 元資料齊全**：
   ```yaml
   ---
   title: "完整演講或研討會主題名稱"
   event: "活動或研討會場次名稱 (如 技術學術研討會 Session G)"
   date: "YYYY-MM-DD"
   talk_id: "場次編號 (如 '20260302-01')"
   speakers: ["發言者清單，含司儀、評審、發表人、指導教授"]
   type: "verbatim-narrative-transcript"
   verbatim: true
   scenario: "classroom-lecture"
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
| `single-talk` | **單人技術演講** | 單一講者主講之研討會演講（如 HITCON、DevDays Asia） | 依講者之**技術演進大綱**切分（背景 $\to$ 成因 $\to$ 攻擊利用 $\to$ 防禦 $\to$ Q&A） | 章節開頭標註講者身分（如 `**【發表者 PK】**：`）；文末 `## ❓ 現場 Q&A 問答交流` 全面啟用角色標籤（`**【現場提問者】**：` / `**【講者】**：`） | 演講開場自介與文末致謝 |
| `multi-paper` | **多論文學術研討會／多組專題發表** | 單一場次包含多名發表者或各小組輪流報告與講評（如 NCU 研討會 Session G/H/I、課堂各組 Proposal 發表） | **雙層樹狀架構**：每篇／每組設 `## 論文/第 X 組：{題目} ({發表人})`，後緊接講評或細分小節 | **全程高密度標籤**：司儀、評審委員、各組發表人、指導教授全程明確標註 | 司儀議程計時規範（舉牌／鈴響）、中場換場、評審總評、優秀論文公告與頒獎合影 |
| `thesis-defense` / `lab-meeting` | **碩博學位口試與實驗室進度會議** | 學位論文口試答辯、實驗室個人碩論進度（`Thesis-Progress`）或專案會議（`Project-Meeting`） | 依**報告模組與質詢攻防主題**切分（嚴禁整場幾萬字只放一個 `章節段落 01`） | **答辯與討論全程密集標註**（召集人／指導教授／口試委員／侑宸／同儕研究生），清楚呈現每一輪問答攻防點 | 口試或會議開場、各階段技術爭點質詢、閉門評定與會後修訂指示 |
| `lightning-talks` | **閃電秀短講（已獨立拆分單場）** | 5-15 分鐘高密度技術短講（如 HITCON 閃電秀各獨立場次） | 依短講內部之**問題背景 $\to$ 核心展示／架構 $\to$ 結論與招募/開源資訊**切分 2～3 個 H2 章節 | 開頭標註主持人引言與講者身分，正文保持原話流暢 | 主持人開場介紹、講者核心展示與結尾呼籲 |

---

### 3. 場景識別第一原則（Scenario-First Identification Rule）

在對任何音訊執行轉錄校對前，必須遵守以下標準作業程序（SOP）：

1. **聽取與掃描特徵**：
   - 是否為課堂授課、包含講師講解、實機操作與學員應答？ $\implies$ 判定為 `classroom-lecture`。
   - 是否出現司儀宣告「下一位發表者是...」或「每位發表者共有二十分鐘」？ $\implies$ 判定為 `multi-paper`。
   - 是否出現召集人主持、口試委員輪流提問或指導教授針對研究進度逐步質詢？ $\implies$ 判定為 `thesis-defense` 或 `lab-meeting`。
   - 是否為單一講者連續報告（僅結尾有短暫問答）？ $\implies$ 判定為 `single-talk`。
2. **嚴禁角色遺漏與模板錯套**：
   - 課堂教學（`classroom-lecture`）嚴禁缺少 `**【授課講師】**：`，嚴禁將學員回應吞沒在講師段落中。
   - 嚴禁將 `multi-paper` 當作 `single-talk` 處理（會導致後續發表論文被截斷遺失）。
   - 標題一律採用生動之「Emoji + 技術主題」，嚴禁使用死板的「一、」「二、」「三、」公文編號，更**嚴禁使用 `章節段落 01`、`現場原話實錄` 等無意義佔位符**。

---

## 七、Summary 摘要主檔（`.md`）設計規範（Genre-Driven Summary Standards）

`.full.md` 的職責是「100% 原話存證」；而 `.md` 主檔存在的唯一目的，是**讓讀者在 30 秒內無須重讀數萬字逐字稿，即可精準檢索該場次的核心知識資產、公式指令、實驗數據與教授決策結論**。

> **【絕對前提】**：撰寫或重構任何 `.md` 摘要前，對應之 `.full.md` **必須已經完成階段三之語意章節切分**。摘要必須透過**逐段研讀 `.full.md` 的各個 `##` 章節**提煉而成，嚴禁只看標題瞎掰兩句套話！

---

### 1. 通用標頭基底（Universal Header Protocol —— 全庫 `.md` 強制統一）

所有 `.md` 摘要檔開頭必須嚴格採用以下格式（**嚴禁在 `.md` 摘要檔放置 YAML Frontmatter，嚴禁使用 `- ` 無縮排列表替代 `>` 引用區塊**）：

```markdown
# {Emoji} {純淨課程／演講／會議主題名稱}

> **場次主題**：{一句話精確定義本場核心內容}  
> **主講／參與者**：{講者、授課教師或與會角色（如：侑宸、指導教授）}  
> **所屬課程／活動**：{課程名稱、研討會或實驗室會議類別}  
> **關鍵技術／核心概念**：{3~6 個具體技術關鍵詞、演算法、數學模型或 CVE 編號}  
> **關聯文件**：[📄 完整原話逐字稿 ({同檔名}.full.md)](./{同檔名}.full.md)
```

* **H1 純淨標題門禁**：`# ` 標題嚴禁出現內部代號與流水號（嚴禁 `MATH-02-EXAM...`、`ML-01-...`、`SECPLUS-03-05-14`、`CCNA-Lab-Disc12`、`Lesson 01`、或孤立議程編號 `# 📱 91 ...`）。
* **超連結 100% 精確門禁**：`關聯文件` 的文字與相對路徑 `(./{同檔名}.full.md)` 必須與同目錄下之 `.full.md` 檔名 **100% 完全一致**，嚴禁殘留舊版 `-proofread.md` 或遺漏連結。

---

### 2. 逐章對應提煉原則（Chapter-by-Chapter Extraction Rule）

1. **章節對齊**：`.full.md` 中切分出的每一個 `##`（H2）核心段落、每一個發表組別、或每一輪關鍵質詢，都必須在 `.md` 的技術剖析章節中設有對應的 `###` 子標題或結構化表格列，**嚴禁遺漏任何章節**。
2. **解釋「為什麼」與「怎麼做」**：嚴禁只列名詞或兩句空泛結論（如「資料集洞察是模型基石」、「演算法公開無妨，安全性繫於金鑰保管」）。必須寫出具體成因、數學定義、參數設定、推導邏輯或師生爭點。

---

### 3. 五大知識體裁適配矩陣（5-Genre Summary Architecture）

為了讓不同性質的錄音具備真實檢索價值，除 `Archive/` 日常行政紀錄外，全庫 `.md` 摘要依知識體裁分為五大類，各類必須包含 **至少 3 個 `##`（H2）主章節**：

| 體裁代碼與名稱 | 適用目錄／場景 | 必備三大 `##`（H2）主章節架構 | 核心章節必須提煉之具體實質內容（缺一不可） |
| :--- | :--- | :--- | :--- |
| **體裁 A**<br/>**研究進度、專案會議與學位口試** | `Laboratory/Thesis-Progress/`<br/>`Laboratory/Project-Meeting/`<br/>`Laboratory/Degree-Defense/` | 1. `## 📌 提案核心與系統／方法設計`<br/>2. `## ⚔️ 指導教授／委員質詢與攻防焦點`<br/>3. `## ✅ 會後修訂決議與待辦事項 (Action Items)` | • **方法設計**：Mermaid 架構圖、具體假設公式（如 $S_t$）、測試矩陣（如 $H_1/H_2/H_3$）或系統模組。<br/>• **質詢攻防**：逐一還原「**教授/口委具體質疑 $\to$ 報告人答辯盲點 $\to$ 教授指導修正方向**」（如詞彙定義不清、實驗缺量化指標）。<br/>• **待辦決議**：明確條列下次會議前需補齊之實驗、圖表或架構調整。 |
| **體裁 B**<br/>**資安漏洞剖析、威脅情報與技術演講** | `HITCON-2026/`<br/>`Laboratory/Security-News/`<br/>`Taiwan-Cybersecurity-Summit/`<br/>`DevDaysAsia-2026/`<br/>`OSINT-CTI/`、`ACE-Exploit/` | 1. `## 🎯 威脅背景與攻擊面／系統全景`<br/>2. `## 💥 漏洞成因與攻擊鏈／技術機制深度拆解`<br/>3. `## 🛡️ 防禦緩解、偵測指標與實務啟示` | • **攻擊/系統全景**：目標環境、信任邊界破口與完整 Mermaid 攻擊鏈/架構圖。<br/>• **技術拆解**：具體 CVE 編號、Root Cause（如 Race Condition / UAF / DLL 側載）、防禦繞過步驟（KASLR/CFI/AMSI/EDR Unhooking）、關鍵指令或時序圖。<br/>• **防禦啟示**：修補方案、偵測規則與現場 Q&A 重點。 |
| **體裁 C**<br/>**理論課程與專業認證實作** | 大學部與碩士班各科課程<br/>`MachineLearning/`、`AdvancedAI/`<br/>`Cisco-CCNA1/`、`SecurityPlus/`<br/>`BasicMathematics/`、`GeneralPhysics/` 等 | 1. `## 🏛️ 核心觀念架構與演算法／協定流程`<br/>2. `## 🔬 關鍵原理、數學推導與實機指令解析`<br/>3. `## 🎯 必考重點與實作避坑指南 (Exam & Lab Pitfalls)` | • **觀念流程**：Mermaid 演算法推導圖、網路拓撲圖或觀念階層圖。<br/>• **原理與實作**：<br/>  - *理論/數學/AI 課*：完整 LaTeX 數學公式、符號定義、定理推導與例題解題步驟。<br/>  - *網路/資安實作課*：完整 CLI 指令區塊（`ip route`, `access-list` 等）、排錯驗證指令或技術規格對照表（如加密演算法比較表）。<br/>• **必考避坑**：講師強調之考點細節與實機常見配置錯誤。 |
| **體裁 D**<br/>**單篇學術論文研討** | `Laboratory/Seminar/`<br/>`UIC-XAI-Keynote/`<br/>`Special-Lecture/` | 1. `## 🎯 研究背景與現有文獻缺口 (Research Gap)`<br/>2. `## 🔬 核心方法論與模型架構`<br/>3. `## 📊 實驗結果、消融分析與研討啟示` | • **文獻缺口**：既有方法為何失效（如 Symptom Bypass vs Root Cause）。<br/>• **方法架構**：Mermaid Pipeline 圖、各階段模組設計、Loss Function 或演算法流程。<br/>• **實驗與啟示**：Baseline 對比與消融實驗（Ablation Study）關鍵數據表，以及實驗室師生對該論文優缺點之批判討論。 |
| **體裁 E**<br/>**多組專題發表與多論文研討會** | `NCU-IM-AcademicConference/`<br/>`20260319` 各組研究提案發表<br/>`AIS3-Club-Training/` 企劃發表 | 1. `## 📋 發表陣容與全場次總覽對照表`<br/>2. `## 🔬 各組／各篇專題深度剖析與講評`<br/>3. `## 💡 跨組共通盲點與總評啟示` | • **全場總覽表**：以 Markdown 表格完整列出每一組/每一篇之「組別/發表人、題目、資料集/工具、核心方法」。<br/>• **逐組深度剖析**：每一組獨立一個 `###` 小節，詳述其問題定義、方法流程、實驗/企劃亮點，以及**教授/評審對該組的具體講評與提問**（嚴禁漏組）。<br/>• **共通啟示**：全場講評點出之共通問題（如 Data Leakage、驗證切分、時間控管）。 |

*(註：`Archive/` 目錄下之非學術日常行政或會前閒聊紀錄，得採精簡之 `## 📌 核心討論事項與行政決議` 結構，不強制套用上述技術體裁。)*

---

### 4. 摘要品質與語法剛性門禁（Summary Quality & Syntax Hard Gates）

1. **章節數與實質字數門檻**：
   - 所有非 `Archive/` 之 `.md` 摘要檔，必須包含 **$\ge 3$ 個 `##`（H2）章節**，且包含多個 `###`（H3）深度剖析子節或結構化表格。
   - 常規場次摘要字數必須 **$\ge 1,500$ 字**（短講或 `< 5,000` 字之短逐字稿對應摘要亦須 **$\ge 1,200$ 字**），徹底杜絕 600～800 字之兩行空殼摘要。
2. **嚴禁控制字元與損毀 LaTeX**：
   - 嚴禁檔案內出現 ASCII 控制字元（`\x07`, `\x08`, `\x09` Tab, `\x0c` Form-feed）。
   - 嚴禁因漏寫反斜線導致之破損 LaTeX 語法（如 `rac{` 應為 `\frac{`、孤立 `floor` 應為 `\rfloor`、`Tab + o` 應為 `\to`）。
3. **Mermaid 圖表語法合法性**：
   - 每個常規 `.md` 摘要至少包含 1 個 `mermaid` 圖表。
   - 在 `flowchart` 或 `graph` 圖表中，**嚴禁混用 `sequenceDiagram` 專屬之 `Note over` 語法**。
   - 節點標籤內若包含半形括號 `()`、方括號 `[]`、冒號 `:` 或特殊數學符號，必須使用雙引號包裹（例如 `A["節點名稱 (補充說明)"]`），確保 GitHub 與 Markdown 渲染器 100% 正常解析。


---

## 八、多主題與混合場次拆分準則（Multi-Scenario Splitting Protocol）

當單一原始錄音檔案或轉錄逐字稿內部收錄了多個相異主題、跨場合或跨議程之內容時，必須依本準則執行無損獨立拆分，確保目錄架構語意清晰、知識檢索精準。

### 1. 拆分觸發判準（Trigger Criteria）

遇到以下任一情況時，**強制執行獨立拆分**：
1. **跨場合混合（Cross-Venue Mixing）**：
   - 單一錄音前後段落分屬不同空間或組織活動。例如：前半段為課堂學生期末專案發表（`classroom-lecture`），後半段為跨校整合型計畫進度研討（`lab-meeting`）。
2. **跨主題與發表人重大轉折（Unrelated Agendas & Distinct Presenters）**：
   - 在實驗室會議或專案研討中，多位發表人依序報告完全獨立的研究方向（如：國際學員報告「對抗性模仿學習 AdMIL」 vs. 研究生發表「APK 免疫疫苗與自動修補」），且各有指導教授與外校評審之深度反饋。
3. **場景適配模式相異（Scenario Mismatch）**：
   - 錄音前後段之角色互動形態完全不同，無法以單一 `scenario` 模板貫徹全文。

---

### 2. 產物規範與命名命名法（Deliverable & Naming Standards）

拆分後的每個子段落均視為獨立標準交付物，必須嚴格遵守以下要求：

1. **Option 3-A 雙軌交付產物**：
   - 每個拆分段落必須獨立產出雙文件：
     - `{YYYYMMDD-序號-主題}.full.md`：100% 完整原話校對逐字稿。
     - `{YYYYMMDD-序號-主題}.md`：高階摘要與核心技術重點筆記。
2. **目錄歸位原則（True Home Directory）**：
   - 拆分後的文件必須移至其真正所屬之領域目錄。課堂報告歸入課程專屬目錄（如 `AdvancedAI-Optimization/`），實驗室專案或產學研討歸入 `5-Master/Laboratory/Project-Meeting/`，資安新聞報告歸入 `5-Master/Laboratory/Security-News/`。
3. **元資料繼承與精準修正（Frontmatter Specialization）**：
   - 獨立設置 YAML Frontmatter：
     - `title`：精準描述該段落之技術核心。
     - `event`：所屬活動或會議名稱。
     - `talk_id`：編訂明確序號（如 `20260226-01`、`20260226-02`）。
     - `speakers`：僅列出該段落實際發言之講師、發表人與教授。
     - `scenario`：套用該段落精確對應之場景代碼（如 `lab-meeting` 或 `classroom-lecture`）。
4. **超連結導航一致性（Relative Link Integrity）**：
   - 摘要筆記（`.md`）開頭之「關聯文件」連結，必須指向該段落新生成的 `.full.md`（如 `[📄 完整原話逐字稿 (20260430-動漫預測模型與偏誤緩解發表.full.md)](./20260430-動漫預測模型與偏誤緩解發表.full.md)`），嚴禁殘留拆分前的舊檔案路徑。

---

### 3. 工具化拆分標準流程（Tooling & SOP）

專案已內建無損拆分引擎（`transcript_processor.splitter`）與 CLI 命令：

1. **檢視段落切分點**：
   ```bash
   python -m transcript_processor split inspect <檔案路徑.full.md>
   ```
   工具將列出檔案內所有 `##` 章節標題及其對應行號，輔助定位精確切分範圍。

2. **撰寫或指定 JSON 拆分規格並執行**：
   ```bash
   python -m transcript_processor split run <拆分配置.json>
   ```
   引擎將自動解析母檔 Frontmatter，截取指定行號之原話正文，產出具備標準標頭之雙軌交付檔。

3. **清理原始混合母檔**：
   確認拆分後檔案無損完整後，自 Git 工作區移除原始混雜之母檔。

4. **全域索引更新與驗證**：
   ```bash
   python -m transcript_processor index
   python -m unittest discover tests
   ```
   自動將新拆分之研討紀錄登錄至 `CATALOG.md` 與 `CATALOG.zh-TW.md`，並確保全套測試通過。

---

## 九、非人聲／純音樂音檔隔離與保留規範（Non-Speech & Music Audio Preservation Protocol）

在錄音歸檔與語音轉錄過程中，若發現輸入之音訊檔案為非課堂、非學術演講、純音樂（如鋼琴曲、背景音樂）、或使用者私人音樂錄音，**絕對禁止視為常規交付音檔隨處理流程刪除**，必須遵循本規範進行嚴格隔離與保留。

### 1. 識別判準（Identification Criteria）

符合以下任一特徵者，強制歸類為「非人聲／純音樂隔離對象」：
1. **純音樂與樂器演奏**：檔名或內容為歌曲、鋼琴演奏（如《夜的鋼琴曲》、《給愛機會》等純樂曲演奏或流行歌曲片段）。
2. **無學術或會議實質口語發言**：轉錄結果為重複歌詞、狀聲詞或無意義之噪音標記，缺乏任何教學、研討、問答對話。
3. **個人生活音訊需遷移行程**：使用者意在將其歸入個人音樂媒體庫而非研究專案紀錄者。

---

### 2. 生命週期隔離防禦機制（Strict Lifecycle Quarantine）

為確保使用者重要音樂資產不因批次清理作業而遺失，系統建立了物理隔離防護：

1. **嚴禁流向 `audio/processed/`**：
   - 非學術音訊**絕對嚴禁**標記為 `finish` 或移入 `audio/processed/`。因 `audio/processed/` 內的所有檔案均會被 `python -m transcript_processor audio clean` 定期清除。
2. **專屬保留隔離區 `audio/preserved/`**：
   - 所有非人聲／音樂檔案**一律強制**移轉至 `audio/preserved/` 存放。
   - `audio clean` 指令在底層架構上**完全排除** `audio/preserved/`，確保保留區檔案受到絕對保護。
3. **自動生成清冊（Quarantine Manifest）**：
   - 每次隔離操作，系統會自動在 [`audio/preserved/MANIFEST.md`](./audio/preserved/MANIFEST.md) 記載檔案名稱、隔離時間戳記與隔離原因。

---

### 3. 操作指引與遷移標準作業程序（SOP）

1. **執行音訊隔離保留**：
   ```bash
   python -m transcript_processor audio preserve <檔案名稱或萬用字元> --reason "非人聲純鋼琴曲/待遷移"
   ```
   *範例：*
   ```bash
   python -m transcript_processor audio preserve "夜的鋼琴曲*.mp3" --reason "私人鋼琴音訊"
   ```
2. **檢視音訊生命週期狀態**：
   ```bash
   python -m transcript_processor audio status
   ```
   狀態輸出將明確區分：
   - 📥 **Pending（待處理）**
   - 📦 **Processed（已交付/可刪除）**
   - 🛡️ **Preserved（非語音/音樂/待遷移保留區 - 安全不刪除）**
3. **使用者安全遷移**：
   使用者可隨時至 `audio/preserved/` 將整批音訊檔案安全複製或遷移至外部儲存裝置，確認離線備份完畢後再視個人需求整理。
