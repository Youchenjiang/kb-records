# 🛡️ SECPLUS-13-14-18 CompTIA Security+ Lesson 13 頁14~18：勒索軟體攻擊鏈、殭屍網路（Botnet）與中繼控制站（C2）

> **課程主題**：現代勒索軟體攻擊生態、殭屍網路 C2 基礎設施與 DDoS 防護  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Ransomware & Botnets  
> **學習目標**：防禦雙重勒索威脅、掌握 C2 域名生成演算法（DGA）與流量清洗機制  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-14-18-勒索軟體運作機制與殭屍網路C2架構-proofread.md)](./SecurityPlus-Lesson13-14-18-勒索軟體運作機制與殭屍網路C2架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Attacker["殭屍網路主控者 (Botmaster)"] --> C2["中繼指揮伺服器 (C2 Server)"]
    C2 -->|下達攻擊指令| Bot1["受控殭屍電腦 (Zombie 1)"]
    C2 -->|下達攻擊指令| Bot2["受控物聯網設備 (Zombie 2)"]
    C2 -->|下達攻擊指令| Bot3["受控伺服器主機 (Zombie 3)"]
    Bot1 & Bot2 & Bot3 -->|集中發送巨量惡意流量 (SYN/UDP Flood)| Target["受害企業目標伺服器 (DDoS Target)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **雙重勒索轉變**：傳統只加密檔案（可用備份還原）；現代勒索軟體先偷偷打包機敏資料至外部伺服器，若不付贖金即於暗網拍賣公開。
2. **C2 偵測指標**：監控 DNS 查詢頻率與可疑隨機網域名稱（DGA），切斷 Bot 與 C2 之間的指令傳遞通道。
