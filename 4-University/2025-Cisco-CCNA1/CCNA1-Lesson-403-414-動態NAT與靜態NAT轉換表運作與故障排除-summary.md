# 🛡️ CCNA-403-414 Cisco CCNA 1 Lesson 頁403~414：動態NAT與靜態NAT轉換表運作與故障排除

> **課程主題**：靜態 NAT 一對一對應、動態 NAT 位址池配置與轉譯表壽命週期排錯  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Chapter 11: Static & Dynamic NAT  
> **學習目標**：掌握 `ip nat inside source static` 指令、動態 Pool 配合 ACL 綁定及 `clear ip nat translation` 排錯  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lesson-403-414-動態NAT與靜態NAT轉換表運作與故障排除-proofread.md)](./CCNA1-Lesson-403-414-動態NAT與靜態NAT轉換表運作與故障排除-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    subgraph StaticNAT ["靜態 NAT (Static NAT - 1對1)"]
        S1["內部 Web Server (192.168.1.100)"] <-->|"永久固定對應"| G1["公網 IP (203.0.113.10)"]
        Note over S1,G1: 支援外部主機主動發起連線
    end

    subgraph DynamicNAT ["動態 NAT (Dynamic NAT - 多對多位址池)"]
        Pool["公網 IP 位址池 (NAT Pool: 203.0.113.20 ~ 203.0.113.25)"]
        Client1["內網主機 PC1"] -->|"動態借用空閒公網 IP"| Pool
        Client2["內網主機 PC2"] -->|"動態借用空閒公網 IP"| Pool
        Note over Pool: 位址池耗盡時，新連線無法建立！
    end
```

---

## 🔬 技術精華與核心考點解析

### 1. 靜態 NAT 與動態 NAT 配置指令
```cisco
! 靜態 NAT (對外發布伺服器)
ip nat inside source static 192.168.1.100 203.0.113.10

! 動態 NAT (位址池 + ACL)
ip nat pool MY_POOL 203.0.113.20 203.0.113.25 netmask 255.255.255.0
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 pool MY_POOL

! 介面定義
interface GigabitEthernet0/0
 ip nat inside
interface Serial0/0/0
 ip nat outside
```

### 2. 轉譯表特性與驗證
- **靜態轉譯條目**：永久存在於 NAT 表中，不會因連線中斷而消失。
- **動態轉譯條目**：僅在有流量通過時生成，若閒置超過 Timeout 時間（TCP 預設 24 小時，UDP 預設幾分鐘），該條目自動回收釋回 Pool。
- **診斷指令**：`show ip nat translations` 檢視所有動態與靜態對應紀錄。

---

## 💡 關鍵總結與考試應對重點

1. **伺服器發布考點：內部伺服器若需接受網際網路外部使用者的主動存取，必須使用「靜態 NAT」進行固定一對一綁定！**
2. **忘記介面標籤：NAT 不通最常見的疏失是在介面上忘記宣告 `ip nat inside` 或 `ip nat outside`。**
