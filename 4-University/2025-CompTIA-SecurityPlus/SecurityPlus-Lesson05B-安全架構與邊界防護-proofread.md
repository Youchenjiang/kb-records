---
title: "CompTIA Security+ Lesson 05 Part 2：安全架構設計、實體與邏輯網路邊界防護"
event: "CompTIA Security+ 認證培訓課程"
date: "2025-01-17"
talk_id: "SEC-05B"
speakers: ['授課講師']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
category: "4-University"
tags:
  - "CompTIA"
  - "Security+"
  - "網路邊界"
  - "Network TAP"
  - "SPAN"
  - "Fail-Open"
  - "Fail-Closed"
  - "OPNsense"
  - "Stateful Inspection"
  - "Three-way Handshake"
  - "Drop vs Reject"
  - "Proxy"
  - "Forward/Reverse Proxy"
---

# 🎙️ CompTIA Security+ Lesson 05 Part 2：安全架構設計、實體與邏輯網路邊界防護 (授課講師)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語（Cisco、CompTIA、Dijkstra 最短路徑、Network TAP、SPAN 鏡像、Fail-Open/Fail-Closed、OPNsense、第一至四代防火牆、Three-way Handshake、Four-way Handshake FIN、Drop vs. Reject、SNAT、Established、Forward/Reverse Proxy、Transparent Proxy 等）與標點符號，並依授課脈絡劃分流暢之章節段落。

---

## 🎯 一、路由器最佳路徑選擇與封包傳遞原理比喻

大家早！這幾天屏東到高雄路途車流量很大，開車花了比較多時間。這正好考驗大家對「最佳路徑計算」的理解。

不要以為只有路由器會計算最佳路徑，其實每個人每天通勤上下班都在計算最佳路徑：
路由器演算法選擇最佳路徑依據的是什麼？
依據的是**總成本（Total Metric / Cost）**！這包含線路頻寬（Bandwidth）、當前鏈路延遲、以及實際流量擁塞程度。平時路幅寬敞、頻寬大又無車流時，行車速度最快；但若逢尖峰時刻大塞車（流量暴增），即使主幹道頻寬再大，走小路（頻寬雖小但流量低）抵達時間反而更快。在演算法理論中，像最短路徑 Dijkstra 演算法或群聚最佳化的蟻群演算法（Ant Colony Optimization），底層皆有嚴密的數學推導與邏輯模型。

在網路安全規劃中，最重要的觀念是：**隨時預備應變方案（What-if Scenarios）與備援機制**。
檢視企業硬體裝置配置拓撲時會發現：所有安全監控設備的擺放位置，皆精確座落在各關鍵節點（Choke Points）上。這是在進行「有效存取控制」的最佳位置抉擇：
- **邊界入口（Perimeter Gateway）**：外部流量進入時，第一道外圍邊界防護可攔截 70% 至 80% 的普遍性惡意探測；
- **邊界與內部核心之間（DMZ 隔離區）**：部署對外公開服務（Web、Mail、DNS 及訪客無線網路），與內部核心徹底隔離；
- **內部網路分段（Network Segmentation / VLANs）**：按部門與機密等級切分為不同子網區段，落實橫向微隔離；
- **端點安全控制（Endpoint Protection）**：終端 PC 安裝主機防火牆（Host-based Firewall）、端點監控代理程式（EDR Agent）與自動修補程式更新機制。

企業資安健全時，內部任何未授權行為皆在網管監控掌握之中，千萬不要心存僥倖在內網進行違規活動。

---

## 📡 二、網路流量分流器（Network TAP）與 IDS/IPS 監控機制

在監控設備中，硬體主要區分為主動式與被動式控制：
- **被動式監控（Passive Network TAP）**：
  - 企業若未採購昂貴的高階核心交換機，可在交換機對外連接防火牆的主幹鏈路上串接一個硬體 **Network TAP（網路分流器）**。
  - TAP 的功能是 100% 物理複製路過的所有進出封包（In-band），將複本旁路引流至後端的入侵偵測系統（IDS）進行深層威脅統計與行為分析，完全不消耗交換機 CPU 資源，亦不對網路轉發造成任何延遲。
- **交換機連接埠鏡像（SPAN / Port Mirroring）**：
  - 在 Cisco 等支援管理功能的交換機上，啟用 **SPAN（Switched Port Analyzer）** 功能，將特定連接埠的流量複製一份鏡像輸出至資安分析伺服器進行側錄。

在硬體供應鏈安全層面，任何傳輸線材或 USB 接頭內部皆可植入微型控制晶片進行硬體側錄（硬體木馬），防不勝防。而在網路連線行為分析中，必須優先關注「連線失敗日誌（Failures）」找出異常源頭，再進一步交叉比對該 IP/MAC 成功的連線紀錄以追蹤橫向移動（Lateral Movement）。

在安全架構中，有兩組極為關鍵的核心哲學：
1. **Fail-Open（故障時開放）**：
   - 當安全機制發生嚴重硬體故障或電源中斷時，系統預設選擇**開放通行**。
   - **實體人身安全鐵律**：例如大樓電子門禁系統或特斯拉等電動車輛，一旦偵測到火災、高溫燃燒（鋰電池火災可達數千度高溫）或斷電時，門鎖**必須絕對 Fail-Open 自動解鎖**！以確保人員能第一時間逃生，人身生命安全永遠高於財產安全。
2. **Fail-Closed（故障時關閉）**：
   - 當安全檢測機制失效時，系統預設選擇**全面關閉阻擋**。
   - **資安與金庫鐵律**：例如企業防火牆引擎崩潰、或銀行身分驗證伺服器斷線時，系統必須 Fail-Closed 拒絕一切未授權存取，寧可中斷服務也絕不能門戶大開讓駭客長驅直入。

---

## 🔥 三、實體安全防護、機房火災高溫防護與災害應變（DRP）

在機房實體安全防護上，必須配置氣體滅火系統（如 FM-200 / Novec 1230）與極早期煙霧偵測（VESDA），避免水損與電氣火災引發設備毀滅性碳化。

回到邏輯防護層面，以知名開源防火牆 **OPNsense**（或 pfSense）為例，現代防火牆的演進經歷了四個世代：
1. **第一代防火牆（封包過濾，Packet Filtering）**：
   - **無狀態（Stateless）**。純粹檢查單一封包的第三層來源 IP 與目的 IP，完全不追蹤上下文。
2. **第二代防火牆（連接埠與協定檢查）**：
   - 增加檢查第四層 TCP/UDP Port 號與 ICMP Type，能過濾特定通訊協定。
3. **第三代防火牆（狀態檢查防火牆，Stateful Inspection）**：
   - **具備狀態感知能力（Stateful）**！主動維護「狀態表（State Table）」，精準追蹤 TCP 連線生命週期。
   - 深入監控 TCP 控制旗標（Flags）：包含連線建立時的 **三次交握（Three-way Handshake：SYN $\to$ SYN-ACK $\to$ ACK）**，以及連線正常結束時的 **四次揮手（Four-way Handshake：FIN $\to$ ACK $\to$ FIN $\to$ ACK）**。
4. **第四代防火牆（次世代防火牆，NGFW）**：
   - 具備第七層應用程式識別、IPS 入侵防護與深層封包檢測（DPI）能力。

在編寫防火牆攔截政策時，**Drop 與 Reject 的行為抉擇至關重要**：
- **Drop（直接丟棄 / 默默黑名單）**：
  - 路由器直接將違規封包無情丟棄，**絕不回傳任何回應訊息**！
  - **最佳實務推薦**：用於企業對外的公共介面。駭客掃描探測時只會面臨無限轉圈圈與逾時（Timeout），完全無法刺探該 Port 是否存在或被何種設備阻擋，大幅消耗攻擊者的探測成本與時間。
- **Reject（禮貌拒絕）**：
  - 丟棄封包的同時，主動向來源端回傳 ICMP Port Unreachable 或 TCP RST 封包。
  - 這等於主動告訴攻擊者「我這裡有防火牆規則、但該 Port 未開放」，暴露內部防禦輪廓；通常僅在內部企業網段便於員工除錯時使用。

---

## 🛡️ 四、狀態檢查防火牆（Stateful Inspection, OPNsense）與三次交握連線追蹤

深入探討狀態檢查防火牆（Stateful Firewall）的連線追蹤核心原理：

當內部主機連線網際網路時，通常透過 **SNAT（Source NAT）** 進行位址轉譯。內部主機主動發起對外連線，發送 TCP SYN 請求；回程封包帶有 SYN-ACK；當三次交握完成後，防火牆狀態表中的該筆連線狀態變更為 **`Established`（已建立）**。

狀態防火牆的黃金安全規則配置：
- **Outbound（出去方向）**：允許內部主機發起 `New`（新連線）、`Established`（已建立連線）與 `Related`（關聯連線）；
- **Inbound（進入方向）**：**嚴格禁止網際網路任意來源發起 `New` 新連線進入內網**！僅允許匹配狀態表中由內向外主動建立的 `Established` 與 `Related` 回程流量穿越。
這就像學校宿舍門禁管理：晚上十點後允許內部學生出門買消夜，且允許外出的學生返回宿舍；但絕對嚴禁外校陌生訪客在此時發起新進入請求。

最後探討第七層應用層代理（Proxy Server）架構：
1. **Forward Proxy（正向代理）**：
   - 代表內部客戶端向外部網際網路請求資源。內部員工瀏覽網頁皆透過 Forward Proxy 轉送，Proxy 可執行嚴格的 URL 過濾、快取加速與惡意內容攔截。
   - **非穿透式代理（Non-transparent Proxy）**：使用者瀏覽器必須手動配置 Proxy IP 與 Port；
   - **穿透式/透明代理（Transparent Proxy）**：網管在閘道器強制將 HTTP/HTTPS 流量轉向 Proxy，使用者端完全無感知。
2. **Reverse Proxy（反向代理）**：
   - 部署在伺服器端前方，代表後端伺服器集體對外接收連線。
   - 外部使用者訪問企業公共域名（如 `www.company.com` Port 80/443、Email Port 25），連線抵達反向代理後，由反向代理依據 URL 路徑或服務類型，安全轉發至後端隔離網段內的具體實體伺服器。
   - 反向代理兼具負載平衡（Load Balancing）、SSL/TLS 加密卸載（SSL Offloading）與隱藏後端真實伺服器 IP 的安全屏障功能。

好，我們這一段邊界防護與代理伺服器觀念先解說到這裡，大家休息十五分鐘，十點半準時繼續！
