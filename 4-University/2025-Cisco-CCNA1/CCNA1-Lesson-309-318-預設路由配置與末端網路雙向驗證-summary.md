# 🛡️ CCNA-309-318 Cisco CCNA 1 Lesson 頁309~318：預設路由配置、末端網路與路由表雙向驗證

> **課程主題**：預設靜態路由（Quad-Zero Route）設定、最後手段閘道器（Gateway of Last Resort）與路徑雙向排錯  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 8: Default Routing & Verification  
> **學習目標**：掌握 `0.0.0.0 0.0.0.0` 語法、Stub Network 架構精簡化及雙向通訊驗證要領  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-309-318-預設路由配置與末端網路雙向驗證-proofread.md)](./CCNA1-Lesson-309-318-預設路由配置與末端網路雙向驗證-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    subgraph Enterprise ["企業內部核心"]
        R1["台北總部 TBR"] <--> R2["台中邊界 TCR"]
    end

    subgraph StubNet ["末端網路 (Stub Network)"]
        R2 <-->|"單一出口專線"| StubRouter["高雄分部 KHR"]
        StubRouter --- BranchLAN["分部區域網路 (10.3.1.0/24)"]
    end

    StubRouter -.->|"ip route 0.0.0.0 0.0.0.0 10.0.0.9"| R2
    Note over StubRouter: 僅需一筆預設路由即可轉發所有外部流量
```

---

## 🔬 技術精華與核心考點解析

### 1. 預設靜態路由（Default Static Route）
- **語法**：`ip route 0.0.0.0 0.0.0.0 {next-hop-ip | exit-intf}`
- **特性**：前綴長度為 `/0`，在所有路由規則中匹配長度最短，因此只在**所有其他明確路由皆未匹配時才會生效**。
- **生效標記**：配置後路由表會顯示 `Gateway of last resort is <next-hop> to network 0.0.0.0`，路由項目前綴為 `S*`。

### 2. 末端網路（Stub Network）特點
- 該網路**僅有單一出口路徑**連接至其他路由器。
- 在 Stub 路由器上，無需配置多筆外部網段的明細靜態路由，**只需配置一筆指向邊界路由器的預設路由**即可大幅精簡路由表容量與查詢負載。

---

## 💡 關鍵總結與考試應對重點

1. **考試常考：若路由表同時有 `10.0.0.0/8`、`10.1.0.0/16` 與 `0.0.0.0/0`，送往 `10.1.2.3` 的封包絕不會走預設路由，而是走 `/16`（最長前綴優先）。**
2. **驗證指令：使用 `show ip route static` 可單獨檢視所有靜態與預設路由項目。**
