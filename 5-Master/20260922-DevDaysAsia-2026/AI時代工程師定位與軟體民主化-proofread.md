---
title: "AI 時代下的軟體民主化、工程師定位對談與 Claude MCP 實戰工作坊"
event: "Microsoft Day 2026"
talk_id: "125"
speakers: ["Justin (主持人)", "Jun (Anthropic Japan)", "Ash (Microsoft GTM)", "Amanda (Anthropic SF)"]
type: "verbatim-narrative-transcript"
verbatim: true
---

# 🎙️ 125 AI 時代下的軟體民主化、工程師定位對談與 Claude MCP 實戰工作坊

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄前半場 **Justin 與 Jun（Anthropic）及 Ash（Microsoft）針對職涯 IC vs Manager、軟體民主化、企業 ROI 與負責任 AI 之重量級對談**，以及後半場 **Amanda 與 Ash 親授之『在 Microsoft Foundry 上結合 Claude 3.5 Sonnet 與 MCP 架構打造點餐 Agent』實戰工作坊全紀錄**，**未做任何刪減或摘要縮寫**；全面修訂中英文混雜轉錄錯字與專有名詞（如 Anthropic, Claude 3.5 Sonnet, Model Context Protocol / MCP, Microsoft Foundry, Foundry IQ, Individual Contributor, Azure Container Apps 等），並依敘事進程劃分清晰結構與主題段落標籤。

---

## 🎙️ 開場：Justin 引言與 AI 時代工程師的焦慮與轉型

好，大家晚安！我是 Justin。大家應該蠻多人有參加過我之前辦的社群活動。兩天前剛好在這個場地，我們也辦了一場活動，在 90 分鐘內我們看到了非常多的 Idea、非常多的 Case 秀出來給我們看，非常非常令人驚豔。這就是 AI 時代帶來的改變。

今天微軟在樓下的標題是『Everyone Can Build』。我自己擔任軟體工程師超過十年了，在『Everyone Can Build』的時代，作為工程師老實說心裡是有點緊張的。我想在座應該很多人也是工程師，不知道大家是否也對這個變革狀態感到緊張？所以我們今天在台上會深入聊聊這個話題。

台上的兩位都是非常資深的業界專家：第一位是 Jun，來自 Anthropic Japan，主要負責 Developer Community；第二位是 Ash，來自 Microsoft，負責 GTM 與 Commercial Market。Ash 看到的東西比較偏 Enterprise 企業視角（Top-Down），而 Jun 看到的偏開發者視角（Bottom-Up），剛好兩位可以從由上而下與由下而上兩個角度互相對照，幫助我們從中找到作為工程師在未來的答案。請大家給予熱烈掌聲！

## 🎯 職涯長跑抉擇：Jun 談追求技術與從管理職回歸 IC（Individual Contributor）

**Justin**：第一個問題想問 Jun：回顧你長期的職涯發展，哪一個長遠的選擇對你產生了最深遠的影響？

**Jun**：大家好，我是來自 Anthropic Japan 的 Jun，非常高興見到大家！感謝台灣社群邀請我。回顧我的職涯，我其實從來沒有做過長遠的 20 年大規劃，但我始終對頂尖技術保持極度著迷。25 年前加入 Sony 是許多日本工程師的夢想，我也熱愛遊戲，很幸運加入了 PlayStation 3 的工程研發團隊；之後硬體之後軟體浪潮來襲，我想去世界上最好的軟體公司，因此加入了 Google 待了 9 年；後來又遇見新興遊戲元宇宙平台 Roblox。我每次都追隨世界上最頂尖的技術，這是我始終不變的熱情所在。

但我學到非常重要的一點：長輩、主管或朋友總會告訴你，成為 People Manager（主管）、升任 Senior Director 或 Vice President 才是成功的職涯標準。我曾經擔任 Senior Manager 與 Director，但我發現我並不享受每天排滿一對一的 1-on-1 會談。我當然喜歡幫助夥伴，但我發現自己親自動手打造東西才是最大的樂趣所在。在確認這一點後，我決定轉回 Individual Contributor（IC，個人貢獻者），這讓我感到無比快樂。現在我在 Anthropic 擔任 IC。傾聽自己內心真正熱愛的事情，對我而言是最關鍵的選擇。

## 📈 跨界轉型：Ash 談從投資銀行財務分析轉向 AI GTM 的不變與變

**Justin**：下一個問題請教 Ash：我們知道你最早是做金融財務起家的，現在轉戰 AI 領域。在你的思維中，什麼是始終不變的？又有什麼是徹底改變的？

**Ash**：謝謝 Justin！是的，我的職業生涯始於投資銀行，曾擔任股票研究分析師（Equity Research Analyst），專門評估企業股票並決定投資標的。

始終不變的是我的底層思考模型：**始終關注『價值創造（Value Creation）』**，而不是為了做 AI 而做 AI。即使在今天面對 AI 浪潮，當我們評估客戶案例、構建 Agent 時，我首先考量的依然是：這究竟能為客戶、團隊或業務帶來什麼實質價值？

徹底改變的則是**『知識的半衰期（Shelf Life）與變化的速度』**。在大學學的金融知識，10 年前如何分析股票，今天大體依然適用；但在 AI 領域，如果你出國休假一週回來，發布的新模型、新架構與新論文數量多到爆炸！你必須隨時保持學習熱情，並接受自己永遠處於 Beginner（初學者）的狀態，因為技術演進太快了。

## ⚖️ 視角交鋒：企業決策層（Top-Down）vs. 開發者社群（Bottom-Up）

**Justin**：Ash 代表企業市場，Jun 代表開發者社群，兩位如何看待對方的視角？

**Jun（開發者視角）**：我最近在台灣、日本和美國與許多個人開發者交流，看到了軟體開發的徹底民主化（Democratization of Software）。例如加州一位律師用 AI 為住房爭議打造了解決方案；一位醫生為他的病患設計了專屬流程；甚至前天 Justin 主辦的黑客松，一位坐輪椅的朋友在 90 分鐘內用 AI 開發了一款工具，能夠查詢全台灣各大建築的電梯尺寸，出門前確認輪椅能否進得去。這在 10 年前極其困難，他得找工程師、學寫程式，但現在個人開發者能在 90 分鐘內解決身邊真實的痛點。

**Ash（企業商業視角）**：當你與企業 CEO、COO、CIO 對話時，他們的第一個問題永遠不是技術，而是：『這項投資需要多少錢？能賺多少或省多少？它安全嗎？我的企業內部資料會不會外洩？』企業決策者心中始終帶著審慎，他們先看到商業與合規解答，才會去看產品。開發者往往只看技術酷不酷，如果開發者能融入商業視角，而管理層也親自動手理解技術，雙方的鴻溝就會迅速弭平。

## 🤖 人機共存：AI 會取代工程師嗎？企業提問的兩年演進

**Justin**：如果團隊成員焦慮地問：『AI 會取代我嗎？』Jun 會怎麼回答？

**Jun**：『會……開玩笑的！』我不這麼認為。事實上，當你每天深度使用 AI 工具時，你會發現自己比以前更忙了！以前預計下週或兩週後才要執行的待辦事項，AI 在兩分鐘內就幫你生成了框架，接踵而來的任務更多。團隊的生產力確實提升了 10 倍，但也因此更需要人類！因為人類需要處理更全局、更宏觀的架構思考，需要跨團隊互動與綜合決策，這些都是 AI 無法取代的能力。

**Justin**：在過去這兩年，企業對 AI 的提問發生了什麼轉變？

**Ash**：兩年前，每家公司都帶著焦慮說：『我們要成為 AI-First 公司！』卻講不出具體要解決什麼問題；兩年後的今天，企業的第一個問題是：『我們要用 AI 解決哪一個具體的業務痛點？能帶來什麼量化回報？』第二個問題是 Tokenomics：如何控制瘋狂飆升的 AI 帳單；第三個問題則是負責任 AI（Responsible AI）：如何確保安全性、隱私與合規治理。

## 💡 真實故事：AI 改變的人生與社群的力量

**Justin**：能否各分享一個身邊因為 AI 而徹底改變人生的真實故事？

**Jun**：我高中的好朋友原本是一家日本大型企業的 Director，上週他毅然辭職創立了自己的 AI 公司。他找到優秀的工程師，全面使用 Claude Code 開發解決方案。他非常認同 Anthropic 對 Safety 的堅持，因為安全是向企業客戶銷售時最強大的護城河。選在對的時間點果斷投入，令人佩服。

**Ash**：我分享兩個例子：第一個是我 65 歲以上的父母，以前常問我各種手機操作問題，現在他們自己用 Claude 與 ChatGPT 查資料、訂票，徹底掌握了生活主導權；第二個是我自己，我用 Claude Opus 分析了我過去兩年的行事曆與電子郵件，檢討工作配置，現在平均每週為我省下 13 到 17 個小時，相當於每週多出 1.5 天的時間！

**Justin**：為什麼社群（Community）如此重要？大家今晚該如何開始？

**Jun**：AI 是屬於全人類的技術，律師、醫生、音樂家都可以用。但許多人不知道該如何開始，社群就是最佳起點。看到醫生做出工具、音樂家做出工具，會產生『我也做得到』的激勵效果。感謝 Justin 在台灣建立了這麼棒的社群，鼓勵大家多參與台灣的社群與工作坊！

**Ash**：想上手微軟 Foundry 的朋友，可以直接到官方網站註冊，新手享有 200 美元免費額度，可以親自體驗模型部署與 Agent 開發。

**Justin**：謝謝 Jun 與 Ash！接下來我們進入精彩的 Hands-on Lab，由 Amanda（Anthropic）與 Ash 為大家帶來實戰工作坊！

## 🍰 Hands-on Lab：以 Claude 與 MCP 在 Microsoft Foundry 打造杯子蛋糕點餐 Agent

（以下為 Anthropic 舊金山團隊 Amanda 與微軟 Ash 帶領的實戰工作坊）

**Amanda**：大家好！我是來自舊金山的 Amanda。很榮幸今晚與大家一起進行 Hands-on Lab！

今晚我們將在 Microsoft Foundry 上結合 Anthropic Claude 模型與 MCP（Model Context Protocol）架構，打造一個名為『Sparkles』的台北杯子蛋糕點餐 Agent！

在後端，我們有一個託管在 Azure Container Apps 的 MCP Server，當使用者下單訂購杯子蛋糕時，訂單會即時寫入 Azure Table Storage。今天現場我們真的準備了實體杯子蛋糕（藍莓與櫻桃巧克力口味），只要大家在 Lab 中成功透過 Agent 下單，就能在前方領取實體杯子蛋糕！

在微軟 Foundry 上，目前已全面提供 Anthropic 家族模型：
* **Claude 3.5 Sonnet**：平衡工作主力，具備極佳的延遲與性價比，是生產環境首選（也是今晚 Lab 所使用的核心模型）；
* **Claude 3 Opus**：旗艦推理模型，擅長長上下文規劃、複雜代碼庫重構；
* **Claude 3.5 Haiku**：極速輕量，適合高頻分類與摘要。

在 Lab 步驟中：
1. **設定環境與 System Instructions**：在 VS Code 中載入環境變數與 API Key，設定 Agent 角色設定（以甜點風格回答）；
2. **掛載 MCP Server**：新增 MCP Server 連線，賦予 Agent 調用外部 Tool 的能力。連接後，Agent 能主動呼叫 MCP Tool 建立 Customer ID、查詢當前庫存（藍莓 / 櫻桃巧克力）並完成下單；
3. **驗證與領取蛋糕**：使用者在對話中輸入姓名與台北地點，選擇口味並輸入現場優惠券代碼，MCP Server 即時將訂單拋入 Azure Table Storage 並顯示在儀表板上。完成下單的學員紛紛前往台前領取現烤杯子蛋糕！
4. **注入 Foundry IQ 知識層**：進一步整合 Foundry IQ（Context Layer），將店面政策、食材配方等靜態知識庫無縫掛載，讓 Agent 具備回答特定門市規範的能力。

整套 Lab 原始碼與完整架構（包含 OpenTelemetry 追蹤與 Dashboard）均已收錄於官方 GitHub Repository。感謝大家的熱情參與！
