---
title: "Cisco CCNA 1 Lesson 頁458~467：IPv6 地址類型分類、Unique Local (FC00::/7) 與鏈路本地位址"
event: "Cisco CCNA 1 認證培訓課程"
date: "2025-01-10"
talk_id: "CCNA-458-467"
speakers: ['授課講師']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
category: "4-University"
tags:
  - "Cisco"
  - "CCNA"
  - "IPv6"
  - "Global Unicast"
  - "Link-Local"
  - "Unique Local"
  - "NDP"
  - "SLAAC"
  - "DHCPv6"
---

# 🎙️ Cisco CCNA 1 Lesson 頁458~467：IPv6 地址類型分類、Unique Local (FC00::/7) 與鏈路本地位址 (授課講師)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語（Cisco、CompTIA、Unique Local FC00::/7、FD00::/8、NDP、Neighbor Solicitation/Advertisement、Solicited-Node Multicast FF02::1:FFxx:xxxx、Multicast FF02::1/2/5/6/9/A、Anycast、SLAAC、EUI-64、DAD、Stateless DHCPv6 Lite、Stateful DHCPv6 等）與標點符號，並依授課脈絡劃分流暢之章節段落。

---

## 🎯 一、Unique Local Address (FC00::/7) 私有空間與內網規劃

IPv6 的 **Unique Local Address（唯一本地位址，ULA）** 規範前綴為 **`FC00::/7`**，實務上目前多使用 `FD00::/8` 區段。這個位址區段專門保留給企業內部私有網路規劃使用。

Unique Local 的核心特性在於：**該位址嚴格禁止路由至公共 Internet 網際網路**。它的定位完全等同於 IPv4 中的 RFC 1918 私有位址（如 `10.0.0.0/8`、`192.168.0.0/16`）。如果企業內部希望維持與外部網路實體隔離、內外有別的安全架構，即可選擇以 `FD` 開頭的 Unique Local 位址進行內部各子網的規劃與配置。

稍早提到 IPv6 能夠實現全自動「Plug and Play（隨插即用）」的背後功臣，正是 **NDP（Neighbor Discovery Protocol，鄰居探索協定）**。NDP 完全基於 ICMPv6 運作，因此 IPv6 對 ICMPv6 具有極高的依賴度。

在 IPv6 環境中，即便沒有配置任何動態路由協定，系統依然會自動維護一張「鄰居表（Neighbor Table）」。在 Windows 命令提示字元中輸入指令：
```cmd
netsh interface ipv6 show neighbors
```
即可檢視本機的 IPv6 鄰居表。觀察鄰居表會發現：左側是第三層 IPv6 位址（不論是 Global Unicast `2001::` 還是 Link-Local `FE80::`），右側直接對應著該主機的第二層 MAC Address。這正是傳統 IPv4 中 ARP 的職責！如今在 IPv6 中全權由 NDP 接手，因此 **IPv6 世界徹底廢除了 ARP 廣播協定**。

NDP 主要透過兩種訊息來建立鄰居關係：
1. **Neighbor Solicitation（NS，鄰居請求）**：功能等同於 ARP Request，主動向網段發送詢問；
2. **Neighbor Advertisement（NA，鄰居通告）**：功能等同於 ARP Reply，由目標設備回應自身的 MAC 位址。

發送 NS 時，送往的是特殊的 **Solicited-Node Multicast Address（請求節點群播位址，`FF02::1:FFxx:xxxx`）**。群播位址在 IPv6 中一律以 **`FF`** 開頭（如同 Link-Local 為 `FE80::`、Unique Local 為 `FC00::`）。

為了無縫銜接工程師在 IPv4 上的習慣，IPv6 的群播位址設計具有高度對照性：
- 所有節點群播（All Nodes）：IPv4 為 `224.0.0.1` $\to$ IPv6 為 **`FF02::1`**；
- 所有路由器群播（All Routers）：IPv4 為 `224.0.0.2` $\to$ IPv6 為 **`FF02::2`**；
- OSPF 路由器群播：IPv4 為 `224.0.0.5` 與 `224.0.0.6` $\to$ IPv6 OSPFv3 為 **`FF02::5`** 與 **`FF02::6`**；
- RIP 路由協定：IPv4 為 `224.0.0.9` $\to$ IPv6 RIPng 為 **`FF02::9`**；
- EIGRP 路由協定：IPv4 為 `224.0.0.10` $\to$ IPv6 EIGRP 為 **`FF02::A`**（十六進位 `A` 代表 10）。

---

## 🔀 二、任播（Anycast）特性：相同 IP 負載平衡與多路徑容錯機制

接下來深入說明 **Anycast（任播）** 位址。
在 Cisco IOS 設定中，管理員可以在多台不同設備的多個介面上配置完全相同的 IP 位址，並在結尾加上關鍵字 `anycast` 進行宣告。

若未加上 `anycast` 關鍵字，系統在進行重複位址檢測時會判定衝突報錯；加上 `anycast` 宣告後，路由器便知曉該位址專門用於任播負載平衡。

Anycast 的轉發邏輯是 **Nearest Routing（最近路徑繞送）**：終端主機發往該 Anycast IP 時，動態路由協定會自動將封包引導至路由成本（Metric/Cost）最低、跳數最近的實體設備。
例如：拓撲中靠左側的三台 PC 距離 Router 1 最近，其流量自動由 Router 1 承擔；靠右側的 PC 距離 Router 2 最近，其流量自動由 Router 2 承擔。平時自然實現流量負載分流；當 Router 1 發生故障時，路由協定收斂後會自動將所有流量切換至 Router 2 接手，同時兼具容錯備援高可用性。

在 Cisco 路由器上配置 IPv6 的第一道鐵律：**必須先開啟 IPv6 路由總開關**！
在全域配置模式下執行：
```text
Router(config)# ipv6 unicast-routing
```
若未先執行 `ipv6 unicast-routing`，路由器預設僅具備 IPv6 主機轉發功能，無法啟用 IPv6 路由轉發與宣告，許多 IPv6 路由指令將無法正常輸入。

開啟總開關後，進入介面配置 IPv6 位址並啟用介面：
```text
Router(config-if)# ipv6 address 2001:DB8:ACAD:1::1/64
Router(config-if)# no shutdown
```
在設定靜態路由時，語法比 IPv4 更加簡練，不再需要繁複輸入 4 組十進位遮罩，直接使用前綴長度即可：
```text
Router(config)# ipv6 route 2001:DB8:ACAD:2::/64 <Next-Hop-IPv6-Address>
```

---

## 🗺️ 三、IPv6 靜態路由（::/0 Default Route）與路由表結構解析

檢視介面狀態使用 `show ipv6 interface <介面名稱>` 指令。在輸出中可清楚看到：
- 由管理員手動配置的 Global Unicast 位址；
- 系統依據 **EUI-64 規則自動生成的 Link-Local 位址（`FE80::`，中間固定夾帶 `FFFE`）**；
- 該介面所加入的群播群組（如 `FF02::1`、`FF02::2` 等）。

檢視路由表使用 `show ipv6 route`：
- 代號 `S` 代表靜態路由（Static Route）；
- 代號 `C` 代表直連網段（Connected Route）；
- 代號 `L` 代表本地介面位址（Local Route，長度固定為 `/128`，等同於 IPv4 的 `/32` 主機路由）；
- 預設路由（Default Route）標記為 **`::/0`**，其預設 AD 值為 1、Metric 為 0。直連網段路由僅有出口介面，非直連靜態路由則具備 Next-Hop 下一跳位址。

---

## 🔍 四、ICMPv6 鄰居發現（NDP）與自動設定：NS/NA 與 RS/RA 訊息類型

在 IPv6 隨插即用架構中，預設的核心配置機制稱為 **SLAAC（Stateless Address Autoconfiguration，無狀態位址自動配置）**。

SLAAC 的「無狀態（Stateless）」意義在於：**路由器完全不記錄、不維護各主機取得的具體 IP 位址租約**。這與傳統 DHCP 伺服器記錄每一筆 IP 與 MAC 對應表（Stateful，有狀態）形成鮮明對比。

SLAAC 的運作流程如下：
1. 路由器介面會週期性（預設每隔 60 秒）向全網段廣播發送 **Router Advertisement（RA，路由器通告，ICMPv6 Type 134）**，通告當前網段 Prefix 與自身作為預設閘道的 Link-Local 位址；
2. 當終端 PC 剛接上網路線時，不必苦等下一次 60 秒週期，PC 會主動發送 **Router Solicitation（RS，路由器請求，ICMPv6 Type 133）** 將路由器喚醒，要求立即回送 RA；
3. PC 接收到 RA 攜帶的 `/64` 網段前綴後，在本地端利用 EUI-64 規則（或隨機演算法）自動生成後半段 64-bit Interface ID，拼接組合為完整的 128-bit IPv6 位址；
4. PC 透過 **DAD（Duplicate Address Detection，重複位址檢測）** 確認無衝突後，正式啟用該位址，並將 Router 的 Link-Local 位址設為預設閘道。

總結 IPv6 位址配置的完整選項光譜：
1. **純手動靜態配置（Full Static）**：手動輸入完整的 128 位元位址與前綴；
2. **靜態前綴 + EUI-64 自動補齊**：手動配置前 64 位元網段，後半段加關鍵字 `eui-64` 自動生成；
3. **SLAAC 純無狀態自動配置**：透過 RS/RA 完全自動生成位址與預設閘道（缺點：預設無法派送 DNS 伺服器等進階參數）；
4. **Stateless DHCPv6（DHCPv6 Lite）**：SLAAC 負責生成 IP 與 Default Gateway，DHCPv6 僅負責補充派送 DNS 伺服器位址與 Domain Name 參數；
5. **Stateful DHCPv6（完整有狀態 DHCPv6）**：完全由 DHCPv6 伺服器統一管理派發 IP、Gateway、DNS 及全部進階網路參數並記錄租約。

好，我們這一段先講到前三種位址配置方式，大家先下課休息十分鐘，下午我們再深入討論 Stateless 與 Stateful DHCPv6 的實務架構！
