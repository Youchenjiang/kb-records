---
title: "CompTIA Security+ Lesson 08：雲端應用程式安全、攻擊防禦、弱點掃描與威脅情資"
event: "CompTIA Security+ 認證培訓課程"
date: "2025-01-22"
talk_id: "SEC-08"
speakers: ['授課講師']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
category: "4-University"
tags:
  - "CompTIA"
  - "Security+"
  - "雲端安全"
  - "CASB"
  - "SBOM"
  - "OpenVAS"
  - "Greenbone"
  - "Tenable Nessus"
  - "威脅情資"
  - "Dark Web"
  - "滲透測試"
---

# 🎙️ CompTIA Security+ Lesson 08：雲端應用程式安全、攻擊防禦、弱點掃描與威脅情資 (授課講師)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語（Cisco、CompTIA、PHP/.NET/C#、CSP、CASB、軟體供應鏈安全、SBOM、OpenVAS / Greenbone、Tenable Nessus、Credentialed Scan、Check Point / Kaspersky Threat Map、IBM X-Force、Recorded Future、abuse.ch、ISAC、Dark Web / AlphaBay、Tor/Freenet/I2P、滲透測試 黑箱/白箱/灰箱等）與標點符號，並依授課脈絡劃分流暢之章節段落。

---

## 🎯 一、雲端應用程式威脅模型與兩大攻擊向量（雲端伺服端 vs. 使用者端）

雲端應用程式的威脅模型主要區分為兩大攻擊面向：
1. **伺服端應用程式本體漏洞**：
   - 攻擊者鎖定目標主機所運行的 Web 框架與原始碼進行漏洞探測。例如檢測系統是採用 PHP、C# 還是特定版本的 .NET Core，針對已知 CVE 未修補漏洞或邏輯缺陷（如忘記密碼身分繞過、越權存取等）進行滲透。
2. **雲端基礎架構與 CSP 平台弱點**：
   - 包含底層雲端服務供應商（CSP）的配置失誤、權限配置不當或老舊基礎設施。發動攻擊時，駭客絕不會傻傻用自家家用寬頻發起攻擊，而是利用雲端巨頭（如 AWS、Azure）租賃彈性運算實例發動高速內部滲透。

在雲端存取控管架構中，廣泛採用 **CASB（Cloud Access Security Broker，雲端存取安全代理人）**。CASB 作為企業端與各類 SaaS/公有雲之間的安全性閘道，提供端到端的可視性、資料外洩防護（DLP）、合規稽核與異常行為攔截。

在供應鏈安全（Supply Chain Security）方面：
企業必須同時進行「向上管理」與「向下管理」。以台積電（TSMC）供應鏈為例，上游廠商必須通過極其嚴苛的資安稽核報告才能取得供應商資格。
對於軟體供應鏈，核心控制措施是要求第三方廠商交付 **SBOM（Software Bill of Materials，軟體物料清單）**！
SBOM 詳實記錄了軟體內部所引用的所有開源函式庫（Libraries）、第三方組件與具體版本號碼。一旦日後某個開源組件爆發零日漏洞（Zero-day），企業網管可瞬間透過 SBOM 精準定位受影響的系統模組並強制供應商修補。

---

## 📦 二、軟體供應鏈安全、SBOM（軟體物料清單）與弱點掃描排程

弱點掃描（Vulnerability Scanning，簡稱弱掃）是資安健診的基本常態作業。大型企業通常每季執行一次（Q1 至 Q4），中小型企業至少每年執行兩次。

弱點掃描的核心精神在於：**先於駭客之前，主動全面清查全網公開資產與內部網路的安全缺陷**，評估風險等級（Critical、High、Medium、Low），做為防火牆設定校正與修補更新的依據。

常見的兩大業界標準弱點掃描工具包含：
1. **OpenVAS / Greenbone Community Edition（GVM）**：
   - 歷史悠久的知名開源弱點掃描平台，如今整合發展為 Greenbone 弱點管理系統。
   - 在專業滲透測試系統 Kali Linux 中原生內建支援，能精準掃描全網段主機、識別開放連接埠、列舉運行服務，並自動對齊國際 CVE 漏洞資料庫產出結構化評估報告。
2. **Tenable Nessus**：
   - 業界市占率極高的商用標準弱點掃描器，具備龐大且即時更新的漏洞特徵外掛庫（Plugins）。

---

## 🔍 三、弱點掃描實戰：憑證掃描（Credentialed） vs. 無憑證非侵入式掃描

在弱點掃描實務中，主要區分為兩種掃描模式：
- **無憑證掃描（Non-credentialed Scan，外部黑箱式）**：
  - 不提供掃描器任何主機登入帳號密碼，模擬外部陌生駭客視角，從網路層進行連接埠探測與外部服務 Banner 抓取，誤報率較高。
- **具憑證掃描（Credentialed Scan，內部白箱授權式）**：
  - 事先在掃描器中配置具有稽核權限的管理員帳號，掃描器直接登入作業系統內部，深入檢查本地註冊表、系統修補程式安裝紀錄（Hotfixes）、本地安全政策與後門組態，準確度極高且能大幅降低誤判。

此外，必須區分通用傳統應用程式與 Web 應用程式的掃描差異：
- **DAST（動態應用程式安全測試）**：針對運行中的 Web 應用程式發起輸入注入測驗；
- **SAST（靜態應用程式安全測試）**：針對原始碼進行靜態代碼走查。

在威脅監控與可視化方面，各大資安巨頭皆建置了即時全球威脅地圖：
- **Check Point ThreatCloud Cyber Threat Map**；
- **Kaspersky Cyberthreat Real-Time Map**。
兩者以動態 3D 地球視覺化展現全球即時發生的跨國 DDoS 攻擊、惡意連線與殭屍網路流向。

---

## 🌐 四、威脅情資共享架構（ISAC）與暗網情資探索

若要持續強化企業防禦，資安團隊必須積極介接外部威脅情資（Threat Intelligence）：
- **IBM X-Force Exchange**：國際級威脅情資社群平台，支援 STIX/TAXII 標準格式進行 IOC（侵害指標）交換；
- **Recorded Future**、**Mandiant Threat Intelligence**；
- **abuse.ch（URLhaus, MalwareBazaar, ThreatFox）**：瑞士著名的非營利惡意軟體黑名單平台，提供最新惡意網址與 C2 伺服器 IP 黑名單；
- **ISAC（資訊分享與分析中心，如金融 F-ISAC、半導體 S-ISAC）**：同業公會跨機構威脅情資即時聯防共享機制。

在情資收集的深水區，包含深網與暗網情資：
- **Deep Web（深網）**：無法被 Google、Yahoo 等傳統搜尋引擎爬蟲索引的私有網路資源（如需身分認證的內部系統、私有資料庫）；
- **Dark Web（暗網）**：必須透過特定匿名網路覆蓋協定（如 **Tor 洋蔥網路、Freenet、I2P**）才能存取的地下網路空間。暗網中充斥著違法地下黑市（如惡名昭彰的 AlphaBay Market）、遭竊企業帳密資料庫、未公開外洩原始碼交易與零日漏洞買賣。資安專家會透過匿名通道進行外洩情資監控（Threat Hunting）。

最後探討軟體安全評估中的 **滲透測試（Penetration Testing）** 三大維度：
1. **黑箱測試（Black Box Testing）**：測試團隊完全無受測目標的內部資訊，全靠外部情報蒐集發起攻擊；
2. **白箱測試（White Box Testing）**：測試團隊持有完整原始碼、架構設計圖與高權限帳密進行全方位代碼審查；
3. **灰箱測試（Gray Box Testing）**：介於兩者之間，賦予測試者一般使用者帳密權限，模擬內部普通員工越權與攻擊情境。

在企業內部推動漏洞回報機制（Bug Bounty）時，必須建立客觀公平的稽核驗證流程，避免演變為研發與品保部門之間的利益衝突與惡性內耗。大家先稍作休息，稍後繼續探討具體的 Web 漏洞防護！
