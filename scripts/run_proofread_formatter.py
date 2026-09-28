#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Runner for Verbatim Proofread Formatting across all 4-University Deliverables
Executes Step 2 of the 4-Stage Pipeline:
- Deep CJK and phonetic correction
- Natural narrative paragraphing (150-300 chars, no sentence fragmentation)
- Semantic emoji section headers
"""

from pathlib import Path
from format_university_transcripts import format_single_proofread

REPO_ROOT = Path(__file__).resolve().parent.parent
CCNA_DIR = REPO_ROOT / "4-University" / "2025-Cisco-CCNA1"
SEC_DIR = REPO_ROOT / "4-University" / "2025-CompTIA-SecurityPlus"


def run_all_formatting():
    print("=== Step 2: Running Deep Proofread Formatting on all 17 deliverables ===\n")

    # 1. CCNA-00
    format_single_proofread(
        raw_folder_name="CCNA 考試方式 週五 下午02點39分",
        target_proofread_path=CCNA_DIR / "CCNA1-00-認證報考與OnVUE考試規則-proofread.md",
        title="Cisco CCNA 1 認證報考流程、Pearson VUE 帳號註冊與 OnVUE 居家線上考試指南",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-00",
        date="2025-01-10",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "Pearson VUE", "OnVUE", "證照考試", "報考指南"],
        section_markers=[
            ("🎯 一、國際原廠認證考試生態系與 Pearson VUE 平台架構", "考試相關"),
            ("🔑 二、Cisco 原廠帳號建立、Single Sign-On (SSO) 與個人檔案設定", "Single Sign-On"),
            ("📊 三、個人儀表板（Dashboard）導覽、考試排定（Schedule Exam）與證照管理", "Dashboard"),
            ("🖥️ 四、測驗交付模式對比：實體考試中心 vs. OnVUE 居家線上監考", "OnVUE的方法"),
            ("📜 五、Cisco 認證體系階梯與 200-301 CCNA 考試代號", "CCT"),
            ("📝 六、考場證件準備、語言選擇與預約改期規範", "各有它的優缺點"),
            ("🔄 七、多元認證（CE 學分）制度與證照生命週期維護", "CE學分"),
            ("💡 八、題型拆解（拖曳題、實作題）、考古題準備與職涯發展建議", "拖曳題"),
        ],
    )

    # 2. CCNA-423-433
    format_single_proofread(
        raw_folder_name="CCNA1 423~433 週四 上午10點05分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lesson-423-433-傳輸層TCP與UDP協定-proofread.md",
        title="Cisco CCNA 1 Lesson 頁423~433：傳輸層 TCP 與 UDP 協定、三次交握與流量控制",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-423-433",
        date="2025-01-09",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "TCP", "UDP", "傳輸層", "三次交握", "Port"],
        section_markers=[
            ("🎯 一、傳輸層在 TCP/IP 模型之定位與 TCP/UDP 核心差異", "深入的來了解"),
            ("🚪 二、連接埠（Port Number）架構：Source Port vs. Destination Port 與多工分流", "source port"),
            ("🤝 三、TCP 雙掛號 vs. UDP 平信比喻與連線交握機制", "像平信"),
            ("🔄 四、雙向通訊 Port 號翻轉與防火牆/ACL 進出規則匹配實務", "反的就相反的是"),
        ],
    )

    # 3. CCNA-433-444
    format_single_proofread(
        raw_folder_name="CCNA1 433~444 週四 上午11點16分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lesson-433-444-ICMP協定與網路診斷-proofread.md",
        title="Cisco CCNA 1 Lesson 頁433~444：ICMP 協定運作、Ping、Traceroute 與網路診斷",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-433-444",
        date="2025-01-09",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "ICMP", "Ping", "Traceroute", "網路排錯"],
        section_markers=[
            ("🎯 一、ICMP 錯誤回報機制與 Destination Unreachable 類型解析", "回送訊息"),
            ("🛡️ 二、封包過濾策略：集中式套用 vs. 分散式邊界部署與 WAN 頻寬節省", "浪費"),
            ("⚙️ 三、延伸 ACL 介面套用方位（Inbound vs. Outbound）實戰", "一百號"),
            ("🔒 四、關鍵伺服器（財務部門）存取控制與 Implicit Deny（隱含拒絕）防坑", "財務"),
        ],
    )

    # 4. CCNA-445-452
    format_single_proofread(
        raw_folder_name="CCNA1 445~452 週五 上午09點05分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lesson-445-452-IPv6協定架構與設計-proofread.md",
        title="Cisco CCNA 1 Lesson 頁445~452：IPv6 協定架構、128位元定址與擴充標頭設計",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-445-452",
        date="2025-01-10",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "IPv6", "定址架構", "標頭設計", "網路協定"],
        section_markers=[
            ("🎯 一、IPv6 誕生背景：從 32 位元到 128 位元與全局唯一性", "四倍大"),
            ("📐 二、固定標頭（Header）結構改良與硬體線速轉發", "Header"),
            ("🌉 三、IPv4 到 IPv6 三大過渡技術：Dual-Stack（雙堆疊）、Tunneling（隧道）與 NAT64", "最佳的解決"),
            ("✂️ 四、IPv6 地址表示法與雙冒號（::）零壓縮單次限制原則", "規則二"),
        ],
    )

    # 5. CCNA-451-457
    format_single_proofread(
        raw_folder_name="CCNA1 451~457 週五 上午10點24分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lesson-451-457-IPv6地址縮寫與簡化規則-proofread.md",
        title="Cisco CCNA 1 Lesson 頁451~457：IPv6 地址縮寫簡化兩大黃金規則與實務練習",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-451-457",
        date="2025-01-10",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "IPv6", "地址縮寫", "雙冒號規則", "前導零省略"],
        section_markers=[
            ("🎯 一、IPv6 地址簡化兩大黃金規則與試題練習", "簡化的就是原則"),
            ("📡 二、廢除廣播機制與 Multicast（群播）替代方案", "沒有廣播地址"),
            ("🌐 三、Global Unicast vs. Unique Local：IPv6 定址哲學", "global"),
            ("🔗 四、Link-Local 位址生成與 EUI-64（FFFE 插入與位元翻轉）實務", "EUI-64"),
        ],
    )

    # 6. CCNA-458-467
    format_single_proofread(
        raw_folder_name="CCNA1 458~467 週五 上午11點23分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lesson-458-467-IPv6地址分類與私有範圍-proofread.md",
        title="Cisco CCNA 1 Lesson 頁458~467：IPv6 地址類型分類、Unique Local (FC00::/7) 與鏈路本地位址",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-458-467",
        date="2025-01-10",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "IPv6", "Global Unicast", "Link-Local", "Unique Local"],
        section_markers=[
            ("🎯 一、Unique Local Address (FC00::/7) 私有空間與內網規劃", "隱匿"),
            ("🔀 二、任播（Anycast）特性：相同 IP 負載平衡與多路徑容錯機制", "anycast"),
            ("🗺️ 三、IPv6 靜態路由（::/0 Default Route）與路由表結構解析", "Default Route"),
            ("🔍 四、ICMPv6 鄰居發現（NDP）與自動設定：NS/NA 與 RS/RA 訊息類型", "運作原理"),
        ],
    )

    # 7. CCNA-DISC-18
    format_single_proofread(
        raw_folder_name="CCNA1 Discovery 18 週四 下午01點02分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lab-Discovery18-標準與延伸ACL配置-proofread.md",
        title="Cisco CCNA 1 Lab Discovery 18：標準 ACL vs 延伸 ACL 實機配置、命名清單與介面套用",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-DISC-18",
        date="2025-01-09",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "ACL", "Packet Tracer", "實驗操作", "存取控制"],
        section_markers=[
            ("🎯 一、實驗拓撲導覽：R1 存取清單規劃與 PC/Device 流量過濾目標", "詳細的說明"),
            ("🛡️ 二、標準 ACL 驗證：Ping 測試、Match 計數器與 Unreachable 判定", "switch one"),
            ("📝 三、命名型 ACL（Named ACL）優勢：插入序號（Sequence Numbers）與線上編修", "線上編輯"),
            ("⚔️ 四、延伸 ACL 協定過濾驗證：UDP 53 (DNS) 攔截與 IP 直連對比", "UDP五十三"),
        ],
    )

    # 8. CCNA-FAST-08A
    format_single_proofread(
        raw_folder_name="CCNA1 Fastlab 8 週四 下午02點37分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lab-Fastlab08A-萬用字元遮罩計算-proofread.md",
        title="Cisco CCNA 1 Fastlab 08 Part 1：萬用字元遮罩（Wildcard Mask）心算推導與 ACL 範圍匹配",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-FAST-08A",
        date="2025-01-09",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "Wildcard Mask", "萬用字元遮罩", "ACL", "子網計算"],
        section_markers=[
            ("🎯 一、萬用字元遮罩（Wildcard Mask）心算法則與 172.16.16.0/20 範圍匹配實練", "一七二點十六"),
            ("🧪 二、實驗拓撲解析：三套 ACL 規則與 POC-2 核心路由器設定", "做三套規則"),
            ("🧭 三、介面套用方位（In vs. Out）與靠近目的地原則實作", "最靠近目的地"),
        ],
    )

    # 9. CCNA-FAST-08B
    format_single_proofread(
        raw_folder_name="CCNA1 Fastlab 8週四 下午03點32分",
        target_proofread_path=CCNA_DIR / "CCNA1-Lab-Fastlab08B-網路延遲統計與SLA分析-proofread.md",
        title="Cisco CCNA 1 Fastlab 08 Part 2：網路效能監控、RTT 延遲統計與電信專線 SLA 實務驗證",
        event="Cisco CCNA 1 認證培訓課程",
        talk_id="CCNA-FAST-08B",
        date="2025-01-09",
        speakers=["授課講師"],
        tags=["Cisco", "CCNA", "RTT", "SLA", "延遲監控", "電信專線", "效能評估"],
        section_markers=[
            ("🎯 一、Cisco IP SLA 統計資料（Statistics）檢視與電信專線合約驗收", "Statistic"),
            ("⏱️ 二、Jitter（抖動）測試原理與 SLA Responder（回應者）角色配置", "UDP 的 jitter"),
            ("⚡ 三、網路效能測試流量生成法與 Cisco 舊設備廢品再利用", "流量產生器"),
        ],
    )

    # 10. SEC-04
    format_single_proofread(
        raw_folder_name="Lesson4 10~17 週三 上午10點16分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson04-PKI與數位憑證-proofread.md",
        title="CompTIA Security+ Lesson 04：PKI 公鑰基礎設施、數位憑證與金鑰生命週期",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-04",
        date="2025-01-15",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "PKI", "數位憑證", "非對稱加密", "CA"],
        section_markers=[
            ("🎯 一、自然人憑證私章概念與 OTP（一次性密碼）防禦", "證人憑證"),
            ("🧬 二、多因子身份驗證（MFA）與生物特徵識別（Biometrics）", "雙重生物驗證"),
            ("🛡️ 三、存取控制清單（ACL）、讀寫權限管理與最小權限原則", "修改他的權"),
        ],
    )

    # 11. SEC-05A
    format_single_proofread(
        raw_folder_name="Security+ Lesson5 9~13 週三 下午03點16分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson05A-認證備考與雙軌防禦-proofread.md",
        title="CompTIA Security+ Lesson 05 Part 1：認證備考策略、CCNA/Security+ 雙軌聯防與安全架構",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-05A",
        date="2025-01-16",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "CCNA", "認證備考", "網路安全", "縱深防禦"],
        section_markers=[
            ("🎯 一、密集訓練心態、CCNA 考照與 OnVUE 防作弊機制", "疲勞"),
            ("🧱 二、消除單點故障（SPOF）、複雜依賴與 CIA 三要素權衡", "SPOF"),
            ("💰 三、網路架構安全設計原則：成本預算、冗餘備援與邊界隔離", "考慮成本"),
        ],
    )

    # 12. SEC-05B
    format_single_proofread(
        raw_folder_name="Security+ Lesson5 15~20 週四 上午09點07分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson05B-安全架構與邊界防護-proofread.md",
        title="CompTIA Security+ Lesson 05 Part 2：安全架構設計、實體與邏輯網路邊界防護",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-05B",
        date="2025-01-17",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "網路邊界", "DMZ", "防火牆", "實體安全"],
        section_markers=[
            ("🎯 一、路由器最佳路徑選擇與封包傳遞原理比喻", "最佳路徑"),
            ("📡 二、網路流量分流器（Network TAP）與 IDS/IPS 監控機制", "入侵偵測系統"),
            ("🔥 三、實體安全防護、機房火災高溫防護與災害應變（DRP）", "氣化"),
            ("🛡️ 四、狀態檢查防火牆（Stateful Inspection, OPNsense）與三次交握連線追蹤", "OPNsense"),
        ],
    )

    # 13. SEC-06
    format_single_proofread(
        raw_folder_name="Security+ 6~11 週一 上午11點13分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson06-密碼學與資料混淆-proofread.md",
        title="CompTIA Security+ Lesson 06：資安治理思維、Gap Analysis 差距分析與企業合規稽核實務",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-06",
        date="2025-01-20",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "資安治理", "Gap Analysis", "合規稽核", "供應鏈安全"],
        section_markers=[
            ("🎯 一、武俠哲學與資安思維", "俠客行"),
            ("✈️ 二、紀律與稽核缺失分析（以重大飛機維修空難為例）", "不依紀律"),
            ("📊 三、Gap Analysis（差距分析）與資安制度合規性落實", "gap"),
            ("🏭 四、企業資安治理與供應鏈商業利益驅動（以日月光為例）", "日月光"),
        ],
    )

    # 14. SEC-08
    format_single_proofread(
        raw_folder_name="Security+ Lesson8 16~26 週一 上午10點25分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson08-雲端應用安全與API防護-proofread.md",
        title="CompTIA Security+ Lesson 08：雲端應用程式安全、攻擊防禦與 API 防護",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-08",
        date="2025-01-22",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "雲端安全", "API", "Web安全", "SQL Injection"],
        section_markers=[
            ("🎯 一、雲端應用程式威脅模型與兩大攻擊向量（雲端伺服端 vs. 使用者端）", "分兩個方向"),
            ("📦 二、軟體供應鏈安全、SBOM（軟體物料清單）與弱點掃描排程", "軟體服務的清單"),
            ("🔍 三、弱點掃描實戰：憑證掃描（Credentialed） vs. 無憑證非侵入式掃描", "Credential"),
            ("🌐 四、威脅情資共享架構（ISAC）與惡意軟體黑名單機制", "malware"),
        ],
    )

    # 15. SEC-12
    format_single_proofread(
        raw_folder_name="Security+ Lesson12 23~36 週三 上午09點15分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson12-SIEM與SOC戰情室-proofread.md",
        title="CompTIA Security+ Lesson 12：資安日誌記錄器、SIEM 架構與 SOC 戰情室事件監控",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-12",
        date="2025-01-24",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "SIEM", "SOC", "日誌分析", "事件回應"],
        section_markers=[
            ("🎯 一、SOC 戰情室架構與多來源日誌收集綜述", "戰情室"),
            ("📋 二、作業系統日誌標準：Windows Event Viewer、Linux Syslog 與 macOS Unified Logging", "統一的"),
            ("✉️ 三、電子郵件標頭分析與釣魚郵件防禦實務", "信件的標題"),
            ("🛠️ 四、開源日誌分析與網路掃描工具庫（Nmap、Wireshark、VLog）實務專題", "掃描工具"),
        ],
    )

    # 16. SEC-15
    format_single_proofread(
        raw_folder_name="Security+ Lesson15 13~18 週四 下午03點17分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson15-實作環境安裝與演練-proofread.md",
        title="CompTIA Security+ Lesson 15：資安實驗環境安裝配置與實機實作排程",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-15",
        date="2025-01-27",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "實驗環境", "虛擬化", "實作演練"],
        section_markers=[
            ("🎯 一、實作安裝排程規劃與時程分配", "這個時間"),
            ("🎓 二、業界資安工程師生涯、研究所經歷與創業故事", "研究所"),
            ("🏎️ 三、科技業高薪生態與資安人才投資報酬率（ROI）談", "全球限量"),
        ],
    )

    # 17. SEC-16
    format_single_proofread(
        raw_folder_name="Security+ Lesson16 8~24、考試規則 週五 上午10點45分",
        target_proofread_path=SEC_DIR / "SecurityPlus-Lesson16-隱私法規與考試須知-proofread.md",
        title="CompTIA Security+ Lesson 16：隱私權法規、資料保護規範與認證考試須知",
        event="CompTIA Security+ 認證培訓課程",
        talk_id="SEC-16",
        date="2025-01-28",
        speakers=["授課講師"],
        tags=["CompTIA", "Security+", "隱私法規", "GDPR", "個人資料保護", "考試規則"],
        section_markers=[
            ("🎯 一、隱私權定義、未經授權讀改刪法律責任與個人資料保護原則", "侵犯你的隱私權"),
            ("🔒 二、資料三態安全防護：傳輸中（In-Transit）、使用中（In-Use）與靜止時（At-Rest）", "傳送過程當中"),
            ("👥 三、企業內部資安意識培訓與分層級教育訓練矩陣", "訓練的目標"),
            ("💻 四、CompTIA 認證考場電腦配置規範與應試環境準備", "檢查你的電腦"),
        ],
    )

    print("\n🎉 Step 2 (Deep Proofread Formatting) completed for all 17 deliverables!")


if __name__ == "__main__":
    run_all_formatting()
