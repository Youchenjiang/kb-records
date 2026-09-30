# 🛡️ SECPLUS-08-11-13 CompTIA Security+ Lesson 08 頁11~13：雲端運算架構、共享責任模型（SRM）與安全配置

> **課程主題**：雲端運算服務架構、共享責任模型（SRM）與企業雲端安全控管  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 8: Cloud Models & Shared Responsibility  
> **學習目標**：釐清 IaaS/PaaS/SaaS 責任歸屬、掌握 CASB/CSPM 雲端合規監控  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson08-11-13-雲端共享責任模型與服務架構-proofread.md)](./SecurityPlus-Lesson08-11-13-雲端共享責任模型與服務架構-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph SaaS ["軟體即服務 (SaaS)"]
        S1["客戶責任：資料與身分存取 (Data & IAM)"]
        S2["業者責任：應用程式、作業系統、硬體與機房"]
    end
    subgraph PaaS ["平台即服務 (PaaS)"]
        P1["客戶責任：應用程式代碼與資料 (App & Data)"]
        P2["業者責任：作業系統、運行環境、伺服器硬體"]
    end
    subgraph IaaS ["基礎架構即服務 (IaaS)"]
        I1["客戶責任：作業系統、修補、防火牆、資料 (OS & Above)"]
        I2["業者責任：虛擬化底層、伺服器實體硬體與機房"]
    end
```

---

## 🔑 重點提要 (Key Takeaways)

1. **資料責任永遠在客戶**：無論使用 IaaS、PaaS 還是 SaaS，資料擁有權與法規合規性責任永遠歸屬於客戶企業本身。
2. **CASB 守門員角色**：雲端存取安全性代理（CASB）作為地端與雲端間的受控閘道，負責強制執行 DLP、身分認證與威脅防禦。
