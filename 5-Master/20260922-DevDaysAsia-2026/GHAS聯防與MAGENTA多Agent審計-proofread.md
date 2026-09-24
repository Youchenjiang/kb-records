---
title: "GitHub Advanced Security 聯防、MAGENTA 多 Agent 弱點審計與 AI Gateway 治理"
event: "Microsoft Day 2026"
talk_id: "123"
speaker: "周祈和 (微軟 AI 解決方案工程師)"
type: "verbatim-narrative-transcript"
verbatim: true
---

# 🎙️ 123 GitHub Advanced Security 聯防、MAGENTA 多 Agent 弱點審計與 AI Gateway 治理 (周祈和)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整保留講者周祈和所有原話論述、架構拆解、現場實機展示、攻擊場景模擬與有獎徵答互動，**未做任何刪減或縮寫**；全面校正語音辨識錯字與專有名詞（如 GHAS、CodeQL、Copilot Autofix、Defender for Cloud、Security Campaign、MAGENTA、MCP Security、AI Gateway / APIM、Defender XDR 等），並依演講敘事邏輯完成精確段落劃分與主題標題標註。

---

## 🛠️ 開發流程安全化：GitHub Advanced Security (GHAS) 與 Copilot Autofix

這個其實是會非常非常的危險。所以我們在寫這些程式碼的時候，應該是我要把問題拆得拆得很乾淨，然後呢要透過一個系統去做專案管理，還是得要做專案管理。那拆很乾淨之後呢，我們讓這每一次的 Commit 都要進到 Security 的一個流程裡面。所以我們這 DevSecOps 呢，剛剛講的重要環節，這個呢就是我們在第一步的時候會有一個叫 Custom Agent，這我們自己就可以做了，這 Coding Agent 呢進去的時候它會幫你去掃，但是呢大語言模型它的知識是會過期的，它沒辦法即時 Update，所以我們還是要靠其他專門功能幫忙找。

進來之後我們還有叫 Secret Scanning，看你的金鑰有沒有被暴露了。那我們在寫 Code 用 AI 寫 Code 時，它輸入太快，有時候金鑰真的不小心被暴露了，那它可以幫你偵測到你金鑰暴露了。它還可以幫你跟另外一個廠商，比如說 AWS 聯動，跟他們講說金鑰洩漏了要直接 Revoke，它可以做到這樣的事情。

那另外一個就是我們剛剛前面講說，我的程式碼越多，我的弱點就越多。這個地方的問題是什麼？不是只有我們自己公司的程式碼，是每一個開源專案的程式碼都有一樣的問題。在之前呢，寫 Linux 的作者 Linus Torvalds 就說，他以前是幾個禮拜才來幾個 Patch 單，那現在則是天天都有修補進來，那有的是真的、有的是假的，因為所有的 Open Source 不論是被攻擊或是被惡意提交不斷進來，所以它會有很多的問題。因此在整個流程裡面，Dependency Scanning 也非常重要，要不然你就是把炸彈綁在身上等著爆炸。那最後一個呢就是 Code Scanning，Code Scanning（CodeQL）在掃的時候會看到你程式碼中的弱點，它就可以直接幫你去做一個 Check，找到問題就直接解掉。

那我們來看一個展示。這個展示呢就是我們現在有一段程式碼寫好了，把它 Commit 上去。Commit 上去的時候呢，我們前面在講這件事情，就是說雖然我們每一個人他都已經可以做到很大幅度 End-to-End 的開發了，但是我們其實還是需要有一個系統來幫忙做把關，要不然的話會亂掉。

那我再分享一下微軟內部怎麼樣做這件事情。微軟的人也是蠻會用 AI 的嘛，他們怎麼樣去做到這樣子的流程？事實上就是說做 PM 的訪談完需求之後，就把需求變成一個規格版本；那前端工程師拿到需求，把它整合變成一個 Commit 的版本；再給到後端、再給到 DB 的同仁，每個人的交付都是程式碼的交付。程式碼交付雖然 AI 可以寫很多程式碼，但 PM、前端、後端在理解這些需求時都會把自己的專業放上去。

好，那我們現在把程式碼丟上去之後，第一個動作要 Code Review。看到右上角這邊 Reviewer 呢，我們就用 AI 來幫忙做 Code Review。AI 在 Code Review 的時候事實上在後面會起一個 PR Review Agent 去掃，掃完之後跟你講說這邊有問題。有問題的話呢，下面就可以看到有個叫做『Fix with Copilot』，AI 找到的弱點就交給 AI 修復！展示給大家看這種有 UI 介面的，事實上沒有 UI 介面也可以直接跟 Copilot 對話直接把弱點全部修掉。Commit 上去自動由 AI 做 Review，綁定 Issue 單號，再透過雲端 Coding Agent 在乾淨環境極速修復，速度非常快。

以前我們拆專案任務要拆得很乾淨，10 個 Task 不能 Overlap，要不然 Merge 會很麻煩；現在不會有這個問題，因為 Agent 寫完之後即使 Conflict，它自己可以去 Resolve Conflict，非常方便。

那程式碼上去之後，GitHub Advanced Security（GHAS）幫你掃到問題。GHAS 的知識來自於哪裡呢？整個 GitHub 平台上有 1.3 億開發者在使用，只要是 Open Source，這些安全功能都是直接免費提供給開源專案使用的！它就是在保證我們整個 Open Source 的安全。掃私有專案要付費，但掃開源是免費的，所以大家用開源都應該把 GHAS 打開。

在 Secret Protection 方面細節非常多：以前是用 Regex Pattern，現在則是結合語意 AI，在上下文裡感覺像是金鑰就會發出警示；而且在 Push 的當下（Push Protection）就能在前門直接擋下來不讓你推上去。如果客戶有自訂的金鑰格式，也支援自訂 Regex 規則。在 Security 方面除了 Dependency Scanning、Autofix，還可以透過 Security Campaign 進行整體控管。

## 🔗 DevSecOps 雲地串聯：Defender for Cloud 與 Security Campaign 實戰

除了程式碼本身之外，程式碼要部署在某個地方 Run，底層有 Runtime 環境、容器 Image 與外掛套件，正式環境還要持續追蹤，所以這不會只是開發單位的責任，而是開發單位與 SecOps 運維單位共同看的。

這兩個團隊看事情的方向往往不一樣：開發團隊看的是程式碼追蹤、套件依賴；運維 SecOps 看的是上線程式安不安全、Runtime 有沒有攻擊路徑、被攻擊時會掉什麼、要通報誰。以前這兩個團隊溝通會有摩擦：開發要快推新功能，資安要穩定要監控。怎麼把這兩個方向拉成一條線？在微軟內部我們就是『Design with Security by Default』，讓安全成為預設選項。

現在我們有一個功能，把 Defender for Cloud 跟我們的 Coding 流程拉成一條線。Defender for Cloud 掌握底層容器映像安全與 Advisory Database。當 SecOps 團隊從安全 Dashboard（Defender for Cloud）看到關鍵風險時，可以直接與 GitHub 串聯！

來看實際演示：作為 Security Admin，在 Attack Path Analysis 中，看到一個潛在攻擊路徑：Zav Webshop 容器暴露於網際網路，有三條不同路由可以存取該容器，進而連向後端的 Storage Account，而儲存體內存放了敏感資料（如美國社會安全號碼 SSN）。管理者點擊建議，看到關聯的 CVE 弱點，直接在 Defender 內將這些 CodeQL Findings 關聯到對應的 GitHub Repository。

現在切換成開發者視角：在 GitHub Packages 的 Linked Artifacts 中，開發者清楚看見 Webshop 容器 Registry、部署區域甚至是 Commit Signature 的完整映射。SecOps 管理者建立一個『Security Campaign』，透過 Runtime Risk 篩選器（如 Internet-exposed 與 Attack Path），將原本 114 個待修問題精準收斂至最致命的 9 個！發布 Campaign 後，每個風險項目都附帶 AI 建議修復方案（Copilot Autofix），開發者可以直接批次指派給 Copilot 自動修復並提交 PR！SecOps 掌握全貌開單，開發者迅速修復，形成完美的雲地聯防。

## 🧠 MAGENTA：100+ 多模型 Agent 自主弱點挖掘與 PoC 驗證框架

除了內部的 GHAS 之外，今天早上的議程講者也跟大家分享到一個非常重要的系統——多模型代理型弱點掃描系統：MAGENTA（Multi-Agent Generative Exploit & Vulnerability Assessment）。

這個功能非常強悍！它採用 Multi-Model 架構，透過超過 100 個專精的自定義 Agent 進行協同掃描，而且沒有綁定任何單一底層模型，可以靈活抽換。

它的運作流程至關重要：
1. 完整掃描整個數位資產（可能是 10 個關聯 Repository）並建立 Threat Modeling；
2. 啟動 100+ 個專精 Agent，各自從不同維度進行弱點探測。每個 Agent 的視角不同、採用的模型不同，驗證完後模型之間還會互相對話辯論（Debate）！這極為關鍵，因為單一模型在訓練時天生帶有偏見與盲點，透過多模型交叉驗證才能消除冗餘；
3. 最重要的一步：自動生成可執行的 PoC（Proof of Concept）去驗證弱點是否真的可以被 Exploit！確認能打穿之後再產出修復方案。它看的不是單一孤立點，而是整個攻擊面。

我們將過去五年微軟歷史測試案例拿來跑 MAGENTA，發現基準檢驗能力提升了 96.5%，121 個歷史重大缺陷 100% 全數抓出！這代表在防守團隊中，我們不再使用單一 Prompt，而是透過『Agent Harness』框架整合上百個 Agent 協同作戰，且掃描後一定有 PoC 驗證基礎。

現場展示中，MAGENTA 既能作為獨立 CLI 執行，也能整合進 GitHub Copilot 應用。除了找出傳統程式碼錯誤與硬編碼金鑰，更具備辨識 AI 專屬安全漏洞的能力。由 100+ 專精 Agent 共同發現、辯論並驗證可利用弱點，幫助開發者從一開始就打造安全程式碼。

最近大家看到新聞，美國政府找各大科技廠商喝咖啡，就是因為這種 AI 漏洞挖掘工具的能力太強悍了！如果攻擊者掌握這種工具，拿去自動掃描開源專案抓 0-Day，後果不堪設想。因此在開發中導入安全防護，防守的已不僅是 IP，更是整個身分與數位資產。

## 🌐 MCP 安全邊界與 AI Gateway (Azure APIM) 流量治理

講完 GitHub 與 Defender for Cloud 串聯後，我們來講今天比較複雜但也至關重要的一部分：MCP（Model Context Protocol）安全性與 AI Gateway。

在企業內部，大家都在思考如何掛載 MCP Service 供內部同仁使用。但掛載 MCP 有三大安全邊界考量：
1. **連線外洩風險**：本機端 Coding 工具（如 Cursor、Claude Desktop 等）連向未知的外部 MCP Server 時必須嚴格控管，防止被惡意植入指令或竊取資料；
2. **本機使用 vs. 企業共享**：本機端僅供個人使用，但一旦要在企業內部跨部門共享，就必須具備集中管理機制；
3. **自建 Server 跳板風險**：若同仁自建 MCP Server 作為連向後端服務的跳板，中間的存取控制至關重要。

因此，各大企業紛紛提出導入『AI Gateway』的需求。AI Gateway 的使命就是：所有 AI 應用（無論是呼叫模型 API、Agent 協調還是 MCP 呼叫）要存取資料，都必須通過中央控管的流量中心。

微軟的 AI Gateway 是基於成熟的 **Azure API Management（APIM）** 演進而來。APIM 原本就負責 API 全生命週期管理，而 Agent 的通訊、模型的調用、MCP 的通訊本質上都是 API！

在 APIM 中，我們賦予它 AI Gateway 的能力：
* **一鍵封裝 MCP Server**：企業既有的 10 個 API 服務，只要匯入 APIM 並勾選啟用，立刻轉化為 10 個標準且安全的 MCP Server；
* **統一身分與稽核控管**：具備完整的帳號認證（RBAC）、稽核軌跡、並發與 Rate Limiting 防護；
* **FinOps 與 Token 計費管理**：精確記錄每個部門、專案的 Token 消耗量，支援內部 Chargeback 計費。

## 🛡️ Defender XDR 實戰：智慧訂房助理 Prompt Injection 攻擊調查閉環

在整體安全防護中，Microsoft Defender for Cloud 與 Defender XDR 是 SecOps 掌握全貌的核心工具。來看一個真實攻擊防禦演示：

一家連鎖旅館推出了智慧訂房助理，但面臨全新安全挑戰。資安團隊透過 Defender 看見威脅轉化為調查線索的完整流程：
1. **資產盤點**：內建查詢跨雲盤點模型與關聯資源；
2. **攻擊路徑剖析**：一台對外開放且存在弱點的 VM，透過認證與權限連向另一朵雲的模型服務；
3. **即時攻擊攔截**：訂房對話中，攻擊者從詢問付款方式，突變為冒充系統管理員索取信用卡的 Prompt Injection（提示詞注入越獄）。雖然提示防護即時擋下，但 Defender XDR 不會就此停止調查；
4. **關聯活動還原**：將敏感資料暴露、憑證竊取、越獄嘗試串成單一 Incident，比對來源 IP、驗證方式與可疑 Prompt；
5. **架構根因修復**：改用受控受限的受控識別碼（Managed Identity）、停用共用金鑰、限縮網路存取範圍，並對模型接觸個人金融資料的權限實施最小化授權。

這就是完整的防護循環：看見資產 $\rightarrow$ 理解風險 $\rightarrow$ 調查事件 $\rightarrow$ 持續改善。

## 🎁 現場問答 QA 互動與閉幕

演講尾聲進行了熱烈的有獎徵答：
* **Q1：GitHub 安全防護服務的名稱是什麼？**
  * 現場觀眾回答：『GHAS（GitHub Advanced Security）！』——答對獲獎！
* **Q2：剛剛介紹的多模型代理型弱點掃描系統名稱是？**
  * 現場觀眾回答：『MAGENTA！』——答對獲獎！
* **Q3：Azure API Management 作為 AI Gateway 的核心功能是什麼？**
  * 現場觀眾回答：『管控所有 AI 與 MCP 流量、權限審計與 Token 配額！』——答對獲獎！

主持人結語：非常感謝微軟 AI 解決方案工程師 周祈和 為大家帶來精彩深入的技術分享！下一場議程將於 4:50 PM 展開，由微軟雲端安全架構師分享今日壓軸講題：《Agentic SOC 企業 AI Agent 的安全營運中心》，請大家準時回座！
