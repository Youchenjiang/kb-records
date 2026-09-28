---
title: "Cisco CCNA 1 Fastlab 08 Part 1：萬用字元遮罩（Wildcard Mask）心算推導與 ACL 範圍匹配"
event: "Cisco CCNA 1 認證培訓課程"
date: "2025-01-09"
talk_id: "CCNA-FAST-08A"
speakers: ['授課講師']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
category: "4-University"
tags:
  - "Cisco"
  - "CCNA"
  - "Wildcard Mask"
  - "萬用字元遮罩"
  - "ACL"
  - "子網計算"
  - "Supernet"
  - "IP SLA"
---

# 🎙️ Cisco CCNA 1 Fastlab 08 Part 1：萬用字元遮罩（Wildcard Mask）心算推導與 ACL 範圍匹配 (授課講師)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語（Cisco、CompTIA、Wildcard Mask、Common Bits、Supernet / CIDR、Proof of Concept / POC-1/2/3、Ethernet 0/0 / 0/1、Loopback、IP SLA、Traceroute 等）與標點符號，並依授課脈絡劃分流暢之章節段落。

---

## 🎯 一、萬用字元遮罩（Wildcard Mask）心算法則與 172.16.16.0/20 範圍匹配實練

大家先心算一下，什麼樣的 Wildcard Mask（萬用字元遮罩）才能精準匹配特定連續網段？

我們來做個經典練習：假設今天要在 ACL 中匹配連續的 16 個 Class C 子網：
從 `172.16.16.0` 一路涵蓋到 `172.16.31.0`（即 `172.16.16.0/20`）。
你的 ACL 規則要怎麼寫？

若不懂得善用 Wildcard Mask，你可能會寫出 16 行規則（`172.16.16.0`、`172.16.17.0` ... 一路寫到 `172.16.31.0`）。如果路由器會說話，它會抗議：「我沒有那麼笨！一行就能搞定的事情，為什麼要寫 16 行？」規則行數越多，路由器對路過封包進行逐行循序比對所耗費的 CPU 運算與延遲就越高。

我們如何只用短短**一行語句**，就能精準涵蓋這 16 個網段？
**推導核心在於「尋找二進位共同位元（Common Bits）」**：
1. 觀察這 16 個網段的前兩個 Byte，完全固定為 `172.16`，因此遮罩前兩碼必須精確為 `0.0`（0 代表必須完全吻合）；
2. 第四個 Byte 涵蓋整段主機空間（`.0` 到 `.255`），完全不在乎，因此遮罩第四碼為 `255`（255 代表忽略不檢查）；
3. 關鍵在第三個 Byte：將十進位 16 到 31 展開為 8 個二進位 Bit：
   - 16 為 `0001 0000`
   - 31 為 `0001 1111`
   - 展開後清楚發現：**前 4 個 Bit 完全相同，皆為 `0001`（共同位元）**；而後 4 個 Bit 則從 `0000` 連續變動至 `1111`！
   - 因此，前 4 個 Bit 必須嚴格比對，遮罩值為 `0000`；後 4 個 Bit 完全不在乎，遮罩值為 `1111`！
   - 二進位 `0000 1111` 轉換為十進位正是 **15**！

因此，第三個 Byte 的萬用字元遮罩就是 **15**。整行 ACL 規則寫作：
```text
Router(config)# access-list 1 permit 172.16.16.0 0.0.15.255
```
封包到達時，路由器僅需執行單一行比對，就能瞬間判定是否落在這 16 個網段內，比對效率提升 16 倍！這正是善用 Wildcard Mask 抓取 Common Bits 的精髓。

同樣的數學原理完全適用於 **路由濃縮（Route Summarization / Supernet 超網）**。當我們想將這 16 筆詳細路由匯聚為單一筆路由通告給鄰居時，原本 Class B 預設為 `/16`，向主機端借 4 個 Bit 涵蓋 16 個子網（$2^4 = 16$），前綴長度即為 $16 + 4 = 20$，匯聚為 `172.16.16.0/20`。這種遮罩比傳統類別網段更靈活的匯聚技術正是 CIDR / Supernetting，能有效抑制全球網際網路路由表的無限制膨脹。

---

## 🧪 二、實驗拓撲解析：三套 ACL 規則與 POC-2 核心路由器設定

觀念確立後，我們進入挑戰性極高的 **Fastlab 08** 實機實驗。

實驗架構採用典型的 **POC（Proof of Concept，概念驗證）拓撲**：
拓撲包含三台路由器：左側 **POC-1**、中央核心 **POC-2**、右側 **POC-3**。
所有過濾控制規則全數部署在中央的 POC-2 上；POC-1 與 POC-3 純粹作為發送與接收測試流量的端點主機。在正式環境上線前，網管人員必定在封閉的 POC 實驗室中反覆驗證 ACL 行為，確認符合預期後再移植至 Production 正式營運網路。

POC-2 上需要配置三套獨立的 ACL 規則：
- **第一套規則（編號 1 號標準 ACL）**：
  - 阻擋來自 `192.168.1.1` 的單一主機流量，但允許 `192.168.1.0/24` 的其餘主機；
  - 封鎖整段 `192.168.2.0/24` 網段；
  - 其餘所有流量一律放行（`permit any`）；
  - 既然是標準型 ACL，依據「最靠近目的地」原則，套用在 POC-2 連接 POC-1 方向的 **Ethernet 0/0 Outbound** 介面。
- **第二套規則（具名標準 ACL `STANDARD_TRAFFIC`）**：
  - 由 POC-1 往 POC-3 方向發送；
  - 要求僅用**一行語句**允許連續的三個特定 IP（`10.1.1.1`、`10.1.1.2`、`10.1.1.3`）。利用後 2 個 Bit 作為萬用字元（$2^2 = 4$，涵蓋 0 到 3），遮罩推導為 `0.0.0.3`；
  - 要求僅用**一行語句**允許 `10.1.2.0/24` 與 `10.1.3.0/24` 兩個網段。利用第三個 Byte 的最後 1 個 Bit（$2^1 = 2$），遮罩推導為 `0.0.1.255`；
  - 套用於 POC-2 的 **Ethernet 0/0 Inbound** 介面（同介面但方向相反，互不衝突）。
- **第三套規則（具名延伸 ACL `PING_3_1`）**：
  - 管制 POC-3 往 POC-1 的流量；
  - 僅允許帶特定實體介面 IP 的 ICMP Ping 直連，其餘帶 Loopback 虛擬介面來源的 ICMP 流量全數阻擋；但允許 Traceroute（UDP）正常通過；
  - 延伸型 ACL 依據「最靠近來源端」原則，套用在 POC-2 的 **Ethernet 0/1 Inbound** 介面。

**關鍵部署鐵律**：
同一個介面的同一個進出方向，只能綁定一套 ACL！若在同一介面同一方向重複套用新規則，舊規則會被直接覆蓋替換，導致原有過濾功能徹底失效。

---

## 🧭 三、介面套用方位（In vs. Out）與靠近目的地原則實作

在 POC-2 核心路由器上落實各項配置：
```text
! 第一套規則：標準 ACL 1
POC-2(config)# access-list 1 deny host 192.168.1.1
POC-2(config)# access-list 1 permit 192.168.1.0 0.0.0.255
POC-2(config)# access-list 1 deny 192.168.2.0 0.0.0.255
POC-2(config)# access-list 1 permit any
POC-2(config)# interface Ethernet 0/0
POC-2(config-if)# ip access-group 1 out

! 第二套規則：具名標準 ACL
POC-2(config)# ip access-list standard STANDARD_TRAFFIC
POC-2(config-std-nacl)# permit host 10.1.1.10
POC-2(config-std-nacl)# permit 10.1.1.0 0.0.0.3
POC-2(config-std-nacl)# permit 10.1.2.0 0.0.1.255
POC-2(config-std-nacl)# deny any
POC-2(config)# interface Ethernet 0/0
POC-2(config-if)# ip access-group STANDARD_TRAFFIC in

! 第三套規則：具名延伸 ACL
POC-2(config)# ip access-list extended PING_3_1
POC-2(config-ext-nacl)# permit icmp host 192.168.23.3 host 192.168.12.1
POC-2(config-ext-nacl)# deny icmp any any
POC-2(config-ext-nacl)# permit ip any any
POC-2(config)# interface Ethernet 0/1
POC-2(config-if)# ip access-group PING_3_1 in
```

特別提醒學員：原廠投影片簡報中的答案在第二套規則的遮罩寫成 `0.0.3.255` 是錯誤的筆誤！因為要涵蓋 2.0 與 3.0 兩個網段，僅需借 1 個 Bit，正確的 Wildcard Mask 必須是 **`0.0.1.255`**（基準網段為 `10.1.2.0`）。請大家在實驗時務必以我講義更正後的標準答案為準。

為了節省大家手動反覆打字測試的時間，我已經在學員記事本中分享了基於 **Cisco IP SLA** 技術撰寫的自動化測試腳本。大家直接複製貼上至 POC-1 與 POC-3 終端，設備會自動模擬產生各類 ICMP、UDP 與特定 Port 號的流量穿透 POC-2。稍後大家只要在 POC-2 上執行 `show access-lists`，就能清楚觀察各行規則後方累計的命中匹配次數（Matches），驗證過濾邏輯是否 100% 精準無誤！
