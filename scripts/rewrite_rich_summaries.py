# -*- coding: utf-8 -*-
from pathlib import Path

summaries = {
    '214': {
        'path': '5-Master/2-Second-Year/Fall-Semester/Security-Lab/20261002-Apache路徑穿越與遠端命令執行RCE實機攻防.md',
        'title': 'Apache 2.4.49 路徑穿越與遠端命令執行 RCE 實機攻防演練',
        'event': '碩二秋季學期 資安攻防與系統安全實驗',
        'date': '2026-10-02',
        'speakers': ['授課教師', '助教', '學員'],
        'paired': '20261002-Apache路徑穿越與遠端命令執行RCE實機攻防.full.md',
        'content': '''# 📋 Apache 2.4.49 路徑穿越與遠端命令執行 RCE 實機攻防演練 — 執行摘要

- **活動場次**：碩二秋季學期 資安攻防與系統安全實驗
- **錄音日期**：2026-10-02
- **發言講者**：授課教師 / 助教 / 學員
- **對應完整逐字稿**：[`20261002-Apache路徑穿越與遠端命令執行RCE實機攻防.full.md`](./20261002-Apache路徑穿越與遠端命令執行RCE實機攻防.full.md)

---

## 📌 核心議題與課程提要

本場實驗課程聚焦於 Apache HTTP Server 2.4.49 歷史重大漏洞（CVE-2021-41773）的原理剖析與攻防實作。課程由授課教師引言說明攻擊鏈脈絡，隨後由助教帶領學員登入靶場進行實際弱點驗證與命令執行打擊。

核心探討因 Apache 路徑正規化（Path Normalization）邏輯缺陷，攻擊者如何利用雙重編碼繞過目錄限制進行路徑穿越（Path Traversal），並在啟用 CGI 模組的特定配置下，進一步將任意檔案讀取升級為遠端命令執行（RCE）。

---

## 🏛️ 攻擊鏈與漏洞原理架構

```mermaid
flowchart TD
    Attacker["攻擊機發送惡意請求"] --> PathTraversal["路徑穿越繞過: /icons/%%32%65%%32%65/"]
    PathTraversal --> ConfigCheck{"CGI 模組是否啟用?"}
    ConfigCheck -- 否 --> ArbitraryRead["任意檔案讀取 (如 /etc/passwd)"]
    ConfigCheck -- 是 --> RCE["次生 RCE: 呼叫 /bin/sh 執行指令"]
    RCE --> Defense["安全修補: 升級至 Apache >= 2.4.51 並修正存取控制"]
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 漏洞根因：路徑正規化缺失
- Apache 2.4.49 在處理 URL 解碼時存在瑕疵，未對二次編碼或特定點號編碼（如 `%%32%65`）進行完整過濾，導致目錄限制被跳脫。

### 2. 從資訊洩漏升級至 RCE 實測
- 課堂實機演示從讀取系統敏感檔案，到藉由 POST 請求向 `/cgi-bin/` 傳遞命令參數呼叫 `/bin/sh`，成功在目標主機取得反彈 Shell 或執行系統命令。

### 3. 作業與防禦要求
- 授課教師要求學員於國慶連假前完成靶場環境的攻擊重現錄影，並撰寫修復報告（包含升級補丁至安全版本及設置嚴格的目錄存取權限 `Require all denied`）。
'''
    },
    '215': {
        'path': '5-Master/Laboratory/Seminar/20261005-RAG檢索增強生成架構與LLM幻覺緩解論文研討.md',
        'title': 'RAG 檢索增強生成架構與 LLM 幻覺緩解機制論文研討',
        'event': '網路與資訊安全實驗室 專題文獻研討 (Seminar)',
        'date': '2026-10-05',
        'speakers': ['報告研究生', '指導教授', '實驗室同儕'],
        'paired': '20261005-RAG檢索增強生成架構與LLM幻覺緩解論文研討.full.md',
        'content': '''# 📋 RAG 檢索增強生成架構與 LLM 幻覺緩解機制論文研討 — 執行摘要

- **活動場次**：網路與資訊安全實驗室 專題文獻研討 (Seminar)
- **錄音日期**：2026-10-05
- **發言講者**：報告研究生 / 指導教授 / 實驗室同儕
- **對應完整逐字稿**：[`20261005-RAG檢索增強生成架構與LLM幻覺緩解論文研討.full.md`](./20261005-RAG檢索增強生成架構與LLM幻覺緩解論文研討.full.md)

---

## 📌 核心議題與研討提要

本次專題討論（Seminar）針對大語言模型（LLM）於特定垂直領域落地時面臨的「時效性落後」與「事實幻覺（Hallucination）」問題，深入研讀 RAG（Retrieval-Augmented Generation，檢索增強生成）前沿論文。報告人系統性梳理了 RAG 的七大架構模組，並探討如何將外掛向量資料庫與生成模型無縫結合。

研討過程中，指導教授特別針對知識庫存放機制、檢索命中率（Recall/Precision）以及針對私有模型的知識供給率展開深度質詢與討論。

---

## 🏛️ RAG 檢索增強生成核心管線

```mermaid
flowchart LR
    UserQuery["使用者提問"] --> Retriever["密集檢索器 (Dense Retriever)"]
    VectorDB[("企業私有向量知識庫")] --> Retriever
    Retriever --> PromptInject["相關文檔片段注入 Prompt 上下文"]
    PromptInject --> Generator["大語言模型 (LLM) 推論"]
    Generator --> GroundedAnswer["具備事實佐證之回答"]
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 預訓練模型的固有邊界
- 純粹依賴 Pre-training 獲取知識的模型無法動態更新高時效性或私有架構資訊，強行推論容易產生嚴重的「過時」與「幻覺」。

### 2. 檢索增強三階段流程
- 檢索（Retrieve）：自外部語料庫透過 Embedding 距離比對取出 Top-K 語意相關片段。
- 增強（Augment）：將檢索結果結合任務指令拼接為結構化 Context。
- 生成（Generate）：約束 LLM 僅基於給定事實產生回答，大幅提高可信度。

### 3. 實驗室落地反思
- 教授提醒後續研究應避免僅流於套用現成框架，需關注知識庫的分塊策略（Chunking）、語意漂移抑制，以及在學位論文程式碼生成任務中的實證有效性。
'''
    },
    '216': {
        'path': '5-Master/2-Second-Year/Fall-Semester/Network-Architecture/20261006-無線網路協定分層限制與跨層感知架構研討.md',
        'title': '無線網路協定分層限制與跨層感知架構研討',
        'event': '碩二秋季學期 高等電腦網路與通訊架構研討',
        'date': '2026-10-06',
        'speakers': ['授課教授', '報告學員', '課堂學員'],
        'paired': '20261006-無線網路協定分層限制與跨層感知架構研討.full.md',
        'content': '''# 📋 無線網路協定分層限制與跨層感知架構研討 — 執行摘要

- **活動場次**：碩二秋季學期 高等電腦網路與通訊架構研討
- **錄音日期**：2026-10-06
- **發言講者**：授課教授 / 報告學員 / 課堂學員
- **對應完整逐字稿**：[`20261006-無線網路協定分層限制與跨層感知架構研討.full.md`](./20261006-無線網路協定分層限制與跨層感知架構研討.full.md)

---

## 📌 核心議題與課程提要

本場研討深入探討傳統 OSI 與 TCP/IP 嚴格分層架構在現代無線通訊環境中的瓶頸。報告學員分析了實體層（Physical Layer）與資料鏈結層（Data Link / MAC Layer）的介面特性，說明傳統分層雖具備標準化與模組化優勢，但因「相鄰層資訊傳遞隔離」特性，在動態拓撲、頻寬抖動及具備移動性的無線環境中，極易引發嚴重的次最佳化排程問題。

課程後半段探討了結合跨層感知設計（Cross-Layer Design）與現代 AI 資源排程之演進方向，並由授課教授提出背景交代與實際應用情境的改進反饋。

---

## 🏛️ 傳統分層架構 vs 跨層感知排程

```mermaid
flowchart TD
    subgraph Traditional["傳統分層架構 (資訊孤島)"]
        AppT["應用層"] --> TransT["傳輸層"]
        TransT --> NetT["網路層"]
        NetT --> MACT["MAC / 鏈結層"]
        MACT --> PhyT["實體層"]
    end
    
    subgraph CrossLayer["跨層感知架構 (Cross-Layer Optimization)"]
        SharedInfo["跨層感知共用資訊庫: 頻道狀態 / 隊列長度 / 服務品質 QoS"]
        AppC["應用層"] <--> SharedInfo
        TransC["傳輸層"] <--> SharedInfo
        NetC["網路層"] <--> SharedInfo
        MACC["MAC 層"] <--> SharedInfo
        PhyC["實體層"] <--> SharedInfo
    end
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 傳統分層的無線適應困境
- 在有線網路中，各層封裝獨立運作良好；但在無線通道易受干擾、封包遺失不等於壅塞（Congestion）的情況下，缺乏跨層感知會導致 TCP 錯誤啟動壅塞控制機制。

### 2. 跨層感知與動態排程優勢
- 藉由讓傳輸層與應用層感知實體層的訊雜比（SNR）或 MAC 層的退避（Backoff）狀態，系統可動態調整視窗大小與 QoS 優先等級，大幅降低延遲。

### 3. 課堂反饋與報告建議
- 教授提醒後續報告應加強背景動機的鋪陳，舉出具體的產業網路情境（如車聯網 V2X 或無人機自組網），使理論架構與實務案例更具體連結。
'''
    },
    '217': {
        'path': '5-Master/Laboratory/Project-Meeting/20261007-語言模型Context上下文學習與研究資料假設建立.md',
        'title': '語言模型 Context 上下文學習與研究資料假設建立方法論',
        'event': '產學合作整合型研究計畫 專案研討會議',
        'date': '2026-10-07',
        'speakers': ['計畫主持教授', '核心研究生', '研究團隊成員'],
        'paired': '20261007-語言模型Context上下文學習與研究資料假設建立.full.md',
        'content': '''# 📋 語言模型 Context 上下文學習與研究資料假設建立方法論 — 執行摘要

- **活動場次**：產學合作整合型研究計畫 專案研討會議
- **錄音日期**：2026-10-07
- **發言講者**：計畫主持教授 / 核心研究生 / 研究團隊成員
- **對應完整逐字稿**：[`20261007-語言模型Context上下文學習與研究資料假設建立.full.md`](./20261007-語言模型Context上下文學習與研究資料假設建立.full.md)

---

## 📌 核心議題與會議提要

本場專案會議聚焦於如何利用大型語言模型（LLM）的上下文學習（In-Context Learning）能力，革新傳統學術研究與專案中的「資料收集」與「假設建立」流程。主持教授對比了手動發放問卷、填表的舊式資料收集痛點，強調透過精確的 Prompt 上下文引導與 Few-Shot 少樣本範例，能讓模型模擬目標情境並產出高質量的假設驗證結構。

會議同時深入探討了研究人員在使用 AI 工具時的本質思維：「不能只是工具的操作者，更要理解工具背後的抽象邏輯，並學會自製符合研究需求的客製化流程」。

---

## 🏛️ In-Context Learning 輔助研究假設流程

```mermaid
flowchart LR
    DomainProblem["領域研究痛點 / 需求定義"] --> PromptDesign["情境上下文構建 (Context Framing)"]
    FewShot["注入精準少樣本範例 (Few-Shot Examples)"] --> PromptDesign
    PromptDesign --> LLMEvaluation["LLM 語意歸納與假設演繹"]
    LLMEvaluation --> StructuredOutput["結構化標註資料 / 檢驗指標"]
    StructuredOutput --> HumanVerify["研究員審查與邊界校準"]
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 兩種上下文驅動模式
- 單純背景提示：給定特定真實業務環境與角色設定，約束模型在該脈絡下解釋現象。
- Few-Shot 範例引導：給出正確對齊的「輸入-輸出」標準範例，教導模型識別隱晦的標註規則。

### 2. 工具使用者的心態轉變
- 教授強調，用現成工具（如剪輯軟體或通用 Chatbot）只能解決表面問題；學術專案的核心競爭力在於「拆解問題根因，並利用程式碼或 API 建構專屬的分析管線」。

### 3. 專案時程與執行要求
- 要求團隊成員於近期確立各自子模組的提示詞範本與驗證集，並準時提交期中評估成果。
'''
    },
    '218': {
        'path': '5-Master/Laboratory/Lab-Meeting/20261008-跨組別研究進度彙報與多專案時程覆盤.md',
        'title': '實驗室跨組別研究進度彙報與多專案時程覆盤',
        'event': '網路與系統實驗室 全體定期進度彙報大會',
        'date': '2026-10-08',
        'speakers': ['指導教授', '各組報告代表', '實驗室全體成員'],
        'paired': '20261008-跨組別研究進度彙報與多專案時程覆盤.full.md',
        'content': '''# 📋 實驗室跨組別研究進度彙報與多專案時程覆盤 — 執行摘要

- **活動場次**：網路與系統實驗室 全體定期進度彙報大會
- **錄音日期**：2026-10-08
- **發言講者**：指導教授 / 各組報告代表 / 實驗室全體成員
- **對應完整逐字稿**：[`20261008-跨組別研究進度彙報與多專案時程覆盤.full.md`](./20261008-跨組別研究進度彙報與多專案時程覆盤.full.md)

---

## 📌 核心議題與會議提要

本場大會由指導教授親自主持，全面覆盤實驗室各研究小組（包含 PNS 計畫組、資安模型攻防組與各專案小組）的年度進度與時程規劃。會議開場包含正式英文全三年研究構想提案（Three-Year Proposal Plan）之彩排與簡報，隨後逐組檢驗模型攻防實驗數據、投影片排版及多專案資源配置。

會中針對梯度攻擊（Gradient-based Attack）、黑箱轉移攻擊（Transfer Attack）以及模仿學習（Mimicry Attack）在智慧型手機感測器行為防禦中的效能差異展開了深入技術論證。

---

## 🏛️ 模型攻防評估與專案管理覆盤架構

```mermaid
flowchart TD
    Proposal["三年期研究計畫提案 (Proposal)"] --> Subtopics["三大核心研究子題推進"]
    
    subgraph AttackDefense["感測器模型攻防評估"]
        Gradient["梯度攻擊 (Gradient Attack)"]
        Transfer["黑箱轉移攻擊 (Transfer Attack)"]
        Defense["主動防禦機制 (Adversarial Training)"]
        Gradient --> Defense
        Transfer --> Defense
    end
    
    Subtopics --> AttackDefense
    
    subgraph LabManagement["實驗室專案管理覆盤"]
        Slides["簡報排版與圖表直觀性檢核"]
        Schedule["國慶假期進度調配與下次會期敲定"]
        Budget["差旅與研究經費結算核銷"]
    end
    
    AttackDefense --> LabManagement
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 三年計畫 Proposal 架構確認
- 全英文報告開場，確立未來三年研究主軸，涵蓋感測器隱私防護、資訊隱藏（Information Hiding）與金鑰交換機制的整合。

### 2. 攻防實證發現：梯度攻擊之主導性
- 初步實驗顯示梯度攻擊（Gradient-based）在白箱環境下威脅顯著高於純模仿攻擊；若要防禦梯度攻擊，必須透過轉移攻擊驗證黑箱模型魯棒性。

### 3. 實驗室行政與下次會期敲定
- 教授確認各項報帳、差旅補助等管理事項，並敲定國慶假期過後的下次正式實驗室 Meeting 日期。
'''
    },
    '219': {
        'path': '5-Master/Laboratory/Thesis-Progress/20261008-黑箱API漏洞探測策略與利用鏈前期偵查研討.md',
        'title': '黑箱 API 漏洞探測策略與利用鏈前期偵查研討',
        'event': '碩士學位論文 進度研討與口委質詢覆盤',
        'date': '2026-10-08',
        'speakers': ['論文研究生', '指導教授', '審查委員/口委'],
        'paired': '20261008-黑箱API漏洞探測策略與利用鏈前期偵查研討.full.md',
        'content': '''# 📋 黑箱 API 漏洞探測策略與利用鏈前期偵查研討 — 執行摘要

- **活動場次**：碩士學位論文 進度研討與口委質詢覆盤
- **錄音日期**：2026-10-08
- **發言講者**：論文研究生 / 指導教授 / 審查委員/口委
- **對應完整逐字稿**：[`20261008-黑箱API漏洞探測策略與利用鏈前期偵查研討.full.md`](./20261008-黑箱API漏洞探測策略與利用鏈前期偵查研討.full.md)

---

## 📌 核心議題與會議提要

本場論文進度研討專門針對先前口試/進度報告時審查委員（楊老師）所提出的重大質詢進行深度覆盤。核心矛盾在於：原研究架構在黑箱評測中「直接跳躍至漏洞利用（Exploitation）階段」，缺乏對前期目標系統的偵查與適應過程，導致黑箱假設的合理性受到質疑。

研究生與指導教授在會中全面釐清了黑箱探測的資訊回報判定邏輯，明確區分無原始碼（No Source Code）前提下的回傳值分析方法，徹底消除白箱與黑箱界限混淆的缺陷。

---

## 🏛️ 黑箱 API 探測與漏洞利用鏈完整邏輯

```mermaid
flowchart TD
    TargetSystem["目標系統 (嚴格無原始碼黑箱環境)"] --> ReconPhase["【前期偵查階段】"]
    
    subgraph ReconPhase["前期偵查與適應 (Reconnaissance)"]
        Fuzzing["API 探測與 Payload 發送"]
        Response["分析回報值: 狀態碼 / 錯誤訊息 / 延遲特徵"]
        Decision["判定系統架構、弱點適應性與漏洞端點"]
        Fuzzing --> Response --> Decision
    end
    
    Decision --> ExploitPhase["【後期利用階段】"]
    
    subgraph ExploitPhase["漏洞利用與驗證 (Exploitation)"]
        PayloadExecution["觸發特定安全漏洞"]
        ImpactVerify["實質危害驗證 (拒絕服務 / 權限提升)"]
        PayloadExecution --> ImpactVerify
    end
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 釐清口委核心質疑：補齊前置偵查鏈
- 口委質疑之癥結在於未交代「如何知道哪個系統有漏洞」。黑箱模型必須先透過自動化探測收集回傳特徵，經由特徵判定符合條件後，方能進入利用模組。

### 2. 嚴格杜絕假設衝突
- 論文前半部強調「零原始碼黑箱」，後半部不可突兀出現依賴原始碼（Source Code）的假設。必須始終維持架構的一致性，透過外部觀測量（API Response）完成證明。

### 3. 修訂論文章節脈絡
- 重新調整論文第四章實作流程圖，明確將章節拆分為「探測與目標識別模組」與「漏洞驗證與利用模組」，使整套防禦與評測框架邏輯閉環。
'''
    },
    '220': {
        'path': '5-Master/Laboratory/Thesis-Progress/20261012-Custom-GPT提示詞轉端控制與社工資源關聯標記研究.md',
        'title': 'Custom GPT 提示詞轉端控制與社工資源關聯標記研究',
        'event': '碩士學位論文 核心架構突破與研究進度研討',
        'date': '2026-10-12',
        'speakers': ['論文研究生', '指導教授', '研究團隊同儕'],
        'paired': '20261012-Custom-GPT提示詞轉端控制與社工資源關聯標記研究.full.md',
        'content': '''# 📋 Custom GPT 提示詞轉端控制與社工資源關聯標記研究 — 執行摘要

- **活動場次**：碩士學位論文 核心架構突破與研究進度研討
- **錄音日期**：2026-10-12
- **發言講者**：論文研究生 / 指導教授 / 研究團隊同儕
- **對應完整逐字稿**：[`20261012-Custom-GPT提示詞轉端控制與社工資源關聯標記研究.full.md`](./20261012-Custom-GPT提示詞轉端控制與社工資源關聯標記研究.full.md)

---

## 📌 核心議題與會議提要

本場長達 132 分鐘的深度論文研討，記錄了碩士研究從自然語言提示詞邁向系統端控制的核心突破。報告人詳細闡述了 Custom GPT 的緣由與架構設計，探討如何將大語言模型的純文字對話輸出，轉化為能夠驅動後端 API 與作業系統端點操作（Endpoint Control）的確定性控制信號。

同時，研討探討了在安全審計中結合「社工級資源標記（Social Engineering Resource Tagging）」與威脅情報圖譜的實踐，破除「僅憑 API 回傳 HTTP 200 即判定漏洞成立」的粗糙評估缺陷，提出透過真實業務金流與物流狀態進行二次閉環驗證的嚴密方案。

---

## 🏛️ Custom GPT 提示詞轉端控制與雙重驗證架構

```mermaid
flowchart TD
    UserPrompt["自然語言提示詞 (Prompt)"] --> CustomGPT["Custom GPT 核心語意引擎"]
    KnowledgeBase[("社工級資源關聯圖譜 / 漏洞特徵庫")] --> CustomGPT
    CustomGPT --> StructuredSignal["結構化端點控制指令 (Action Schema)"]
    StructuredSignal --> EndpointExec["後端端點執行 (API / OS Tool Call)"]
    
    EndpointExec --> HTTPResponse["觀測 API 回傳 200 狀態"]
    HTTPResponse --> BusinessVerify{"業務邏輯二次驗證: 金流/物流/權限實質變更?"}
    BusinessVerify -- 是 --> ConfirmedVuln["確認存在實質安全漏洞"]
    BusinessVerify -- 否 --> FalsePositive["排除假警報 (False Positive)"]
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 提示詞工程進化為端點控制
- Custom GPT 不只是客製化聊天介面，其核心價值在於透過 Function Calling 與 Action 協議，將模糊的語意意圖轉換為具有確定性、原子性的端點執行指令。

### 2. 破除 API 假警報：業務狀態二次驗證
- 安全檢測不能只看「API 回傳 200 OK」。報告人強調必須引導代理人深入檢查後端金流、物流或帳號權限的實際持久化狀態，確認實質危害已經發生，杜絕誤報。

### 3. 社工級標記與論文定位
- 將社工情資與資源關係網引入攻擊路徑分析，精準標定受害者特徵與弱點位置。教授高度認可右圖架構圖的改進，並指導其在整篇論文創新點中的精準學術定位。
'''
    }
}

for sid, d in summaries.items():
    p = Path(d['path'])
    p.write_text(d['content'], encoding='utf-8')
    print(f"Updated Session {sid}: {p.name}")

print("All 7 summaries perfectly rewritten without boilerplate!")
