# 🛡️ SECPLUS-13-19-22 CompTIA Security+ Lesson 13 頁19~22：實體環境社交工程、尾隨入侵（Tailgating）與搜垃圾防禦

> **課程主題**：實體社交工程、尾隨門禁漏洞與機敏廢棄物處理防範  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：CompTIA Security+ Topic 13: Physical Security & Social Engineering  
> **學習目標**：識破尾隨搭訕話術、落實訪客刷卡查驗與 DIN 66399 碎紙銷毀標準  
> **關聯文件**：[📄 完整原話逐字稿 (SecurityPlus-Lesson13-19-22-實體社交工程與尾隨翻垃圾攻擊防禦-proofread.md)](./SecurityPlus-Lesson13-19-22-實體社交工程與尾隨翻垃圾攻擊防禦-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Attacker["社交工程攻擊者 (偽裝訪客/外送員/清潔工)"] --> Step1{"嘗試入侵實體大樓"}
    Step1 -->|手法 1: 尾隨 (Tailgating)| Gate["利用員工熱心開門混入"]
    Step1 -->|手法 2: 搜垃圾 (Dumpster Diving)| Trash["翻找未碎紙機銷毀之內部報表"]
    Step1 -->|手法 3: 肩窺 (Shoulder Surfing)| Screen["在公共場所偷窺密碼與螢幕"]
    Defense["企業對應防禦"] --> D1["防尾隨閘門 (Mantraps / 一人一卡閘門)"]
    Defense --> D2["上鎖廢紙回收桶 + 碎紙十字銷毀"]
    Defense --> D3["防窺保護貼 + 員工資安意識培訓"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **尾隨防禦**：教育員工「不幫任何人扶門刷卡」，並設置捕人陷阱閘門（Mantrap / Security Air Lock），一次只容許單人驗證通過。
2. **搜垃圾情報價值**：企業廢棄之便條紙、會議紀錄、組織架構圖常成為攻擊者拼湊社交工程劇本的黃金情資。
