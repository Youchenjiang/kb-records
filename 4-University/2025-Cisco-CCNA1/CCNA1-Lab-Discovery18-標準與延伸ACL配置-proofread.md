---
title: "Cisco CCNA 1 Lab Discovery 18：標準 ACL vs 延伸 ACL 實機配置、命名清單與介面套用"
event: "Cisco CCNA 1 認證培訓課程"
date: "2025-01-09"
talk_id: "CCNA-DISC-18"
speakers: ['授課講師']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
category: "4-University"
tags:
  - "Cisco"
  - "CCNA"
  - "ACL"
  - "Packet Tracer"
  - "實驗操作"
  - "存取控制"
  - "Named ACL"
---

# 🎙️ Cisco CCNA 1 Lab Discovery 18：標準 ACL vs 延伸 ACL 實機配置、命名清單與介面套用 (授課講師)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語（Cisco、CompTIA、Standard ACL、Extended ACL、Named ACL、Wildcard Mask、Ethernet 0/0 / 0/1 / 0/3、PC1、Server1/2、Switch1/2、Deny/Permit、Timeout、ARP Request/Cache、Sequence Number、Telnet Port 23/80 等）與標點符號，並依授課脈絡劃分流暢之章節段落。

---

## 🎯 一、實驗拓撲導覽：R1 存取清單規劃與 PC/Device 流量過濾目標

我們將實際來練習並測試驗證 ACL（Access Control List，存取控制清單），包括標準型 ACL（Standard ACL）與延伸型 ACL（Extended ACL），同時也會練習具名清單（Named ACL），大家可以看到 Cisco IOS 向下相容的實作方式。

先看實驗架構拓撲：我們預計在核心路由器 R1 上設定並套用 ACL 規則，達成精準的流量過濾效果。包含從 PC1 所在網段出發，到達右側的 Server 2 與 Server 1。R1 上有三個介面：Ethernet 0/0（E0/0）、Ethernet 0/1（E0/1）以及 Ethernet 0/3（E0/3）。我們必須依據存取控制策略目標，選擇正確的介面與適當的進出方向（Inbound / Outbound）來套用規則。

在第一個 Task 中，我們先練習標準型 ACL。標準型 ACL 邏輯比較單純，只檢查來源 IP 位址。

在 R1 上，Lab 環境已經預先寫好了編號 10 號的標準 ACL（編號 1 到 99 屬於 Standard ACL），但規則尚未套用到任何介面上。執行檢視指令：
```text
R1# show running-config | include access-list
```
可以看到 ACL 10 包含五行語句，範圍由小到大排列：
1. 第一行針對單一主機（未加 Wildcard Mask 時系統預設為 `0.0.0.0` 即 `/32`），僅允許 PC1（IP 結尾 `.10`）；同網段其餘主機（如 Switch 1 結尾 `.4`）將在此被阻擋；
2. 後續幾行分別放寬遮罩為 `/24`、`/16`、`/8`；
3. 最後一行則為 `deny any`。

標準型 ACL 既然只能檢查來源 IP，部署原則就是**必須套用在最靠近目的地端的介面**！在 R1 的三個介面中，最靠近 Server 2 目的地的介面正是 **Ethernet 0/3**，且封包是向外離開 R1 送往伺服器，因此套用方向為 **Outbound**：
```text
R1(config)# interface Ethernet 0/3
R1(config-if)# ip access-group 10 out
```

套用完成後，執行 `show access-lists` 觀察。雖然當初是用號碼 10 建立的規則，但 Cisco IOS 為了向下相容，會自動為每一行規則指派 Sequence Number（序列號，如 10, 20, 30）。這意味著事後可以直接使用具名語法 `ip access-list standard 10` 進入配置模式，將數字 10 當作名稱來進行線上的單行插入、修改與刪除。此時尚未產生任何流量，因此規則後方尚未出現小括號計數器（Matches）。

---

## 🛡️ 二、標準 ACL 驗證：Ping 測試、Match 計數器與 Unreachable 判定

接下來進行流量驗證：
1. **PC1 Ping Server 2**：封包穿過 R1，成功匹配第一行允許規則！查看 `show access-lists`，第一行精準出現 `(5 matches)`。
   - 同學會注意到發送 5 個 Ping 封包時，成功率為 80%（第一個封包出現 `.` 逾時 Timeout）。
   - **為什麼第一次 Ping 會 Timeout？** 因為這是跨網段通訊，PC1 第一次要將 ICMP 封包送往預設閘道時，本地 ARP 快取中尚無 Gateway 的 MAC Address！PC1 必須先暫停 ICMP 傳送，在網段廣播發送 ARP Request 詢問；等待 Gateway 回應 ARP Reply 並寫入 ARP Cache 的過程耗時超過 2 秒，導致第一個 ICMP 封包逾時。後續一旦建立 ARP 快取，Ping 就會全數直通。
2. **Switch 1 Ping Server 2**：Switch 1 的 IP 為 `.4`，不符合第一行 PC1（`.10`）的條件，因而落入第二行被 `deny` 阻擋，螢幕顯示 `U`（Destination Host Unreachable）！
   - 檢查 ACL 計數器，第二行顯示有 Match 命中。
   - 為什麼計數器增加了 8？因為包含 5 個 ICMP 請求與路由器回送的 3 個 ICMP Unreachable 錯誤告警訊息。
3. **Router 2 Ping Server 1**：從 R2 送往 Server 1，回程封包穿過 E0/3 Outbound 介面時受到比對，成功命中第三行允許規則，計數器精確遞增 4 次。
4. **Router 1 本機 Ping Server 2**：在 R1 自身執行 Ping 指令。封包雖然確實從 E0/3 送出，但**路由器本地發出的流量完全不受介面 Outbound ACL 的檢查**！檢查 ACL 計數器完全沒有增加，證實了本機流量不受限的鐵律。

接著 Lab 引導我們進行規則修訂：希望將 `10.2.0.0` 網段也一併封鎖，只保留 PC1 能存取。若直接在全域模式輸入 `access-list 10 deny 10.2.0.0 0.0.255.255`，這行新規則會被系統預設追加到最末端！
由於前面較大範圍的允許規則早已優先匹配，躲在最後面的 `deny` 語句將永遠無法執行，Switch 2 的流量依然暢行無阻。

若使用傳統指令 `no access-list 10`，**整套 ACL 10 將會被系統一口氣全部刪除**！
要精準刪除單一行規則，必須改採具名 ACL（Named ACL）模式：
```text
R1(config)# ip access-list standard 10
R1(config-std-nacl)# no 60
```
僅需輸入 `no <Sequence-Number>`，即可乾淨俐落地單獨移除第 60 行規則，完整保留其餘語句。

---

## 📝 三、命名型 ACL（Named ACL）優勢：插入序號（Sequence Numbers）與線上編修

利用具名 ACL 模式，我們可以在現有規則之間彈性插入新語句：
```text
R1(config)# ip access-list standard 10
R1(config-std-nacl)# 24 permit host 10.2.0.20
R1(config-std-nacl)# 27 deny 10.2.0.0 0.0.255.255
```
序號 27 精確插入在 20 與 30 之間；而序號 24 因為是單一主機的最嚴格條件，Cisco IOS 會自動優化其比對邏輯。再次驗證：Switch 2 成功被攔截阻擋，而終端 PC1 與 Server 1 依然通暢，達成預期安全控制目標。

---

## ⚔️ 四、延伸 ACL 協定過濾驗證：UDP 53 (DNS) 攔截與 IP 直連對比

完成標準 ACL 練習後，我們移除舊規則，進入延伸型 ACL（Extended ACL）實戰。
目標情境：我們要管制 PC1 對外連線，**封鎖所有 UDP 53（DNS 域名解析）請求，僅允許 TCP 23（Telnet）與 ICMP（Ping 直連），其餘 TCP 服務一律拒絕**。

建立具名延伸 ACL：
```text
R1(config)# ip access-list extended BLOCK_DNS_TRAFFIC
R1(config-ext-nacl)# deny udp any any eq 53
R1(config-ext-nacl)# permit tcp host 10.1.0.10 any eq 23
R1(config-ext-nacl)# deny tcp host 10.1.0.10 any
R1(config-ext-nacl)# permit ip any any
```

延伸型 ACL 既然能同時過濾來源 IP、目的 IP 與 Port 號，**最佳部署實務就是套用在最靠近出發地（PC1）的入口介面 Inbound 方向**！
PC1 連接在 R1 的 Ethernet 0/0，因此套用至 E0/0 Inbound：
```text
R1(config)# interface Ethernet 0/0
R1(config-if)# ip access-group BLOCK_DNS_TRAFFIC in
```

實機測試對比：
1. **PC1 Ping 域名 `server2.cisco.com`**：Ping 失敗！因為 Ping 域名必須先發送 UDP 53 封包向 DNS 伺服器進行解析，封包一進入 E0/0 立即被第一行 `deny udp any any eq 53` 攔截阻擋，解析失敗自然無法通訊。
2. **PC1 Ping IP 位址 `10.2.0.20`**：直接 Ping IP 位址完全通暢！因為跳過了 DNS 解析，直接發送 ICMP 封包，前三行不匹配後命中第四行 `permit ip any any`。
3. **PC1 Telnet 至 Server 2**：輸入帳號密碼（預設 `cisco123`），成功連線登入！因為符合第二行 `permit tcp host 10.1.0.10 any eq 23`。
4. **PC1 嘗試以 TCP 80 連線**（`telnet 10.2.0.20 80`）：連線遭拒斷線！因為命中第三行 `deny tcp host 10.1.0.10 any`。
5. **從 Server 1 測試域名解析與連線**：全數正常通暢！因為 Server 1 連接在 E0/1 介面，E0/1 並未套用該過濾規則，流量完全不受影響。

在實驗環境中，Server 2 同時身兼簡易 DNS 伺服器與 NTP 時間伺服器。若在各網路設備上配置 DNS 伺服器位址，後續執行 Traceroute 時，沿途所經過的跳數（第一站 R1、第二站 R2、第三站 Server 2）都會自動解析顯示為直觀的設備名稱，便於全網維運監控。

本實驗完整驗證了 Standard vs. Extended ACL 的機制差異、Inbound/Outbound 套用方位選擇、以及 Named ACL 序列號編修技巧。大家請掌握時間在模擬環境中完成驗證！
