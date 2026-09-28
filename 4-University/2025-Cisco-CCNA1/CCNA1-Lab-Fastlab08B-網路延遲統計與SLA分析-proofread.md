---
title: "Cisco CCNA 1 Fastlab 08 Part 2：網路效能監控、RTT 延遲統計與電信專線 SLA 實務驗證"
event: "Cisco CCNA 1 認證培訓課程"
date: "2025-01-09"
talk_id: "CCNA-FAST-08B"
speakers: ["授課講師", "學員"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "classroom-lecture"
---

# 🎙️ Cisco CCNA 1 Fastlab 08 Part 2：網路效能監控、RTT 延遲統計與電信專線 SLA 實務驗證 (授課講師)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動問答，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語與標點符號，明確標註發言角色（授課講師／學員），並依授課脈絡劃分流暢之主題章節。

---

## 🎯 Cisco IP SLA 統計資料（Statistics）檢視與電信專線合約驗收

**【授課講師】**：我們來看 IP SLA 的統計資料。除了 `show ip sla summary` 檢視概況外，將指令換成 `show ip sla statistics`，就可以看到非常詳細的量測統計數據：包含發送測試總次數、成功次數、失敗次數，以及來回往返時間（Round-Trip Time, RTT）的平均值、最大值與最小值。

這在業界實務維運上極為實用！例如企業向電信業者（如中華電信）租賃專線或 MPLS VPN，合約通常載明 SLA（服務層級協定）保證延遲上限在多少毫秒以內。網管工程師利用 Cisco 設備內建的 IP SLA 工具，長週期持續量測總公司到各分公司的專線線路，若長期統計平均值嚴重超出合約規範，就能提出客觀數據要求電信商排錯改善、賠償或降價。電信業者遇到懂得用 IP SLA 實測調證的網管人員都會特別謹慎。

IP SLA 常用檢視指令包含三種：
1. `show ip sla summary`：快速掌握各量測編號的執行狀態與是否超時（Timeout）；
2. `show ip sla statistics`：深入分析 RTT 延遲、Jitter（抖動）與掉包率；
3. `show ip sla configuration`：檢視詳細的探針排程與探測頻率設定。

在 POC-1 與 POC-3 終端執行 `show ip sla summary`，會看到部分探針狀態顯示 Timeout。這完全符合預期！因為 POC-2 上套用的 ACL 規則刻意阻擋了特定來源的流量，超時正好證實了該流量確實被 ACL 精準攔截丟棄。

Cisco IP SLA 的巨大優勢在於：**企業完全不需額外斥資購買昂貴的專用硬體封包產生器（Traffic Generator）**！只要在總公司與分公司的思科路由器上打上遠端目的 IP，就能隨時由本機動態模擬產生 ICMP、UDP、TCP 等各類封包。甚至早期我們還會利用它長時間監測各大公開 DNS 伺服器的解析回應速度，評估何者表現最佳。

---

## ⏱️ Jitter（抖動）測試原理與 SLA Responder（回應者）角色配置

**【授課講師】**：進行一般 ICMP Echo、TCP 連線或 DNS 查詢測試時，目標端只需要是一個具備 IP 位址的普通網路節點，**完全不需要目的設備具備 Cisco 系統**。

但若要精確量測即時多媒體通訊所需的 QoS 關鍵指標——**Jitter（抖動，封包到達間隔的變異度）**、單向延遲與精確掉包率時，目的地端就必須是一台支援 Cisco IOS 的設備，並在該設備上配置啟用 **`ip sla responder`（SLA 回應者）**！

為什麼 Jitter 測試必須依賴 SLA Responder？
因為單純的 Ping 僅能得知雙向總時間，無法拆解「去程單向時間」與「回程單向時間」；若目的地系統本身處理繁忙產生內部延遲，也會被誤計入網路傳輸時間。而當目的地啟用 SLA Responder 後，它會在封包接收與回送的微秒瞬間壓上硬體時間戳記（Timestamp），將設備內部停留時間扣除，精確計算出網路鏈路真實的 Jitter 與單向延遲。

在 POC 實驗中，POC-1 與 POC-3 互為發送端與 Responder，流量往返穿透中央的 POC-2，成為演練與驗證 ACL 過濾邏輯的最佳實戰環境。在每次測試前，建議先執行 `clear access-list counters` 清除舊計數器，以便精準觀察最新流量匹配情形。

---

## ⚡ 網路效能測試流量生成法與 Cisco 舊設備廢品再利用

**【授課講師】**：在路由器配置模式下輸入 `ip sla <編號>`，打問號 `?` 可以看到琳瑯滿目的測試類型：支援 ICMP Echo、UDP Echo、UDP Jitter、TCP Connect、DNS、HTTP、FTP、VoIP 等豐富通訊協定。

這使 Cisco 設備成為現成的流量產生利器。在實務企業環境中，即使是倉庫中報廢淘汰的舊款路由器或第二層/第三層交換機，只要支援 IP SLA 功能，都可以廢物利用拿來當作專屬的「效能探針與流量產生器」，隨插即用進行鏈路壓測。

雖然 Cisco 網管系統提供了圖形化操作介面（GUI），但底層本質上依然是將這些指令下發至設備運行。

IP SLA 的另一大優點是 **全自動背景非同步執行（Background Daemon Execution）**。它不會像傳統 Ping 指令佔用終端控制台畫面，工程師可以一邊放任探針每隔數秒在背景發送探測，一邊自由檢視路由表、介面狀態與排錯，完全不影響日常管理操作。

ACL 是管理思科網路設備不可或缺的核心基本功，建議各位同學把 Discovery 18 與 Fastlab 08 兩個實驗至少反覆實作兩次以上，徹底熟悉規則編寫、萬用字元遮罩推導與 In/Out 方向抉擇。

今天課程先到這邊告一段落。明天我們將進入 IPv6 完整架構剖析與考古題解析。大家明天早上九點準時繼續！
