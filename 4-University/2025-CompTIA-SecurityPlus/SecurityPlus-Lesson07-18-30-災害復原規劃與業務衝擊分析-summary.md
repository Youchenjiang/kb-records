# 🛡️ SECPLUS-07-18-30 CompTIA Security+ Lesson 07 頁18~30：災害復原計畫（DRP）、業務影響分析（BIA）與 RTO/RPO

> **課程主題**：災害復原計畫（DRP）、BIA 衝擊評估與 RTO/RPO 復原指標  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 7: Disaster Recovery & BIA  
> **學習目標**：計算 RTO 與 RPO、評估 Hot/Warm/Cold 備援站點建置成本與啟動時間  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson07-18-30-災害復原規劃與業務衝擊分析-proofread.md)](./SecurityPlus-Lesson07-18-30-災害復原規劃與業務衝擊分析-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    Event["發生災害中斷點"]
    LastBackup["最後一次備份時間"] -->|RPO (容許資料流失量)| Event
    Event -->|RTO (容許系統停機復原時間)| Recovered["系統完全復原上線"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **RTO vs. RPO**：RTO 是系統停擺到修好的時間長度；RPO 是最後一次備份到當機之間所丟失之資料量。數值愈接近零，建置成本呈指數上升。
2. **備援站點選擇**：Hot Site 具備即時同步與全套設備（復原時間幾近於零但極貴）；Warm Site 需還原資料；Cold Site 僅有空間電力無預載硬體。
