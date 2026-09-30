# 🛡️ CCNA1-LAB-GRE-TUNNEL Cisco CCNA 1 Lab 補充實作：GRE Tunnel 點對點穿隧配置與跨網段封包封裝演練

> **課程主題**：GRE Tunnel 點對點穿隧技術、Underlay 實體路由先決條件與 Overlay 虛擬通道配置  
> **授課講師**：授課講師（資安與網路認證原廠認證講師）  
> **核心模組**：Cisco CCNA 1 Generic Routing Encapsulation (GRE) Tunneling  
> **學習目標**：理解「路由未通則穿隧不通」、配置 Tunnel 介面並達成私網跨公網互通  
> **關聯文件**：[📄 完整原話逐字稿 (CCNA1-Lab-Tunnel-GRE穿隧與跨網段端對端路由-proofread.md)](./CCNA1-Lab-Tunnel-GRE穿隧與跨網段端對端路由-proofread.md)

---

## 🏛️ 核心架構與概念流轉圖

```mermaid
flowchart LR
    PC1["私網 PC 1 (192.168.1.0/24)"] --> R1["邊界路由器 R1 (Tunnel 0)"]
    R1 -->|GRE 封裝 (Protocol 47)| WAN["公網網際網路 (Underlay IP 路由可達)"]
    WAN --> R2["邊界路由器 R2 (Tunnel 0)"]
    R2 -->|解封裝原生 IP 封包| PC2["私網 PC 2 (192.168.3.0/24)"]
```

---

## 🔑 重點提要 (Key Takeaways)

1. **Underlay 路由是先決條件**：Tunnel 終點實體 IP（tunnel destination）若無法透過公網路由 Ping 通，Tunnel 介面絕對無法 Up。
2. **GRE 封裝開銷**：GRE 會額外增加 24 位元組標頭（20-byte IP + 4-byte GRE），實務上須注意調整 MTU 與 MSS 防止封包碎片化。
