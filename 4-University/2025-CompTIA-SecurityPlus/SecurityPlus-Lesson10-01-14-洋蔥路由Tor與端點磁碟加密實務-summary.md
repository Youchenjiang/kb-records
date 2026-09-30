# 🛡️ SECPLUS-10-01-14 CompTIA Security+ Lesson 10 頁01~14：暗網與洋蔥路由（Tor）、全磁碟加密與更新管理

> **課程主題**：Tor 洋蔥路由匿名機制、全磁碟加密保護與端點修補維運  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 10: Tor, FDE & Endpoint Patching  
> **學習目標**：理解洋蔥多跳路由技術、配置 BitLocker/TPM 保護靜態資料並實施更新管理  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson10-01-14-洋蔥路由Tor與端點磁碟加密實務-proofread.md)](./SecurityPlus-Lesson10-01-14-洋蔥路由Tor與端點磁碟加密實務-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    Client["用戶端 (Tor Browser)"] -->|多層加密包裹| Guard["入口節點 (Guard Relay)"]
    Guard -->|解開第一層| Middle["中繼節點 (Middle Relay)"]
    Middle -->|解開第二層| Exit["出口節點 (Exit Relay)"]
    Exit -->|解開最後一層 (明文)| Target["目標網站 / 服務"]
    Exit -.->|僅出口節點知曉目標，但不知來源| Target
    Guard -.->|僅入口節點知曉來源，但不知目標| Client
```

---

## 🔑 重點提要 (Key Takeaways)

1. **洋蔥路由特性**：每一跳（Hop）節點僅知曉前一個節點與後一個節點，無任何單一節點能完整串接使用者身分與訪問目標。
2. **靜態資料保護（At-Rest）**：全磁碟加密（FDE）結合主機板 TPM 晶片，防止筆電失竊後硬碟直接拔下於其他主機讀取資料。
