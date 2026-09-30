# 🛡️ CCNA1-LAB-IPV6-SLAAC Cisco CCNA 1 Lab 補充實作：IPv6 SLAAC 無狀態配置、EUI-64 與 DHCPv6 伺服器整合

> **課程主題**：IPv6 SLAAC 自動定址、ICMPv6 RA 封包與 Stateless DHCPv6 伺服器整合實作  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 IPv6 Addressing & Dynamic Configuration  
> **學習目標**：掌握 SLAAC 無狀態位址生成、配置 Cisco 路由器派送 DNS 伺服器資訊  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-IPv6-SLAAC與DHCPv6派發配置實作-proofread.md)](./CCNA1-Lab-IPv6-SLAAC與DHCPv6派發配置實作-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart TD
    Client["IPv6 主機用戶端"] -->|發送 ICMPv6 RS (Router Solicitation)| Router["Cisco 路由器 (Default Gateway)"]
    Router -->|回傳 ICMPv6 RA (Router Advertisement: 前綴 /64)| Client
    Client -->|以 EUI-64 或隨機介面 ID 生成全球單播位址| GUA["生成完整 IPv6 GUA 位址"]
    Client -->|依 RA 之 O-Flag 向 DHCPv6 索取其他資訊| DHCP["Stateless DHCPv6 Server"]
    DHCP -->|派發 DNS IP 與網域名稱| Client
```

---

## 🔑 重點提要 (Key Takeaways)

1. **SLAAC 核心機制**：用戶端完全不需要 DHCP 伺服器即可依據路由器 RA 派送的 Prefix（前綴）自動組合出 IPv6 位址。
2. **Stateless DHCPv6 互補價值**：SLAAC 早期無法派發 DNS 伺服器位址，透過設定 RA 的 Other Configuration Flag (O-flag)，指引用戶端向 DHCPv6 索取 DNS 與網域名稱。
