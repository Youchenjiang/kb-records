---
title: "Cisco CCNA 1 Lesson 頁423~433：傳輸層 TCP 與 UDP 協定、三次交握與流量控制"
event: "Cisco CCNA 1 認證培訓課程"
date: "2025-01-09"
talk_id: "CCNA-423-433"
speakers: ['授課講師']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
category: "4-University"
tags:
  - "Cisco"
  - "CCNA"
  - "TCP"
  - "UDP"
  - "傳輸層"
  - "三次交握"
  - "Port"
---

# 🎙️ Cisco CCNA 1 Lesson 頁423~433：傳輸層 TCP 與 UDP 協定、三次交握與流量控制 (授課講師)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語（Cisco、CompTIA、Three-way Handshake、SYN、ACK、FIN、RST、Sliding Window、DoS、TFTP、SSH、Kerberos、DNS Recursive Lookup、TLD 等）與標點符號，並依授課脈絡劃分流暢之章節段落。

---

## 🎯 一、傳輸層在 TCP/IP 模型之定位與 TCP/UDP 核心差異

我們深入來了解 TCP/IP。畢竟在前面我們已經都講完子網路由（Routing），那現在已經到了傳輸層（Transport Layer）以上。網路層（Network Layer）這邊主要就是 IP 地址規劃設計還有路由，靜態路由、動態路由都講過，所以繼續往上的話就是傳輸層跟應用層。

傳輸層這邊主要就是兩個協議，也就是 TCP 跟 UDP。上層所開發的各種應用，基本上都是基於 TCP 或 UDP 開發出來的。TCP 跟 UDP 這兩個各有它的強項，各有它的訴求點。

當你今天需要做很多控制的時候，要做各種控制，比如說錯誤檢查、確認回應（ACK）或者是流量控制等等，那這時候就會選擇 TCP。但是如果你今天要求快，不希望延遲太大，比如說像我們的視訊會議、語音 IP 電話（網路 IP 電話），那些都是要越快越好。如果單向延遲超過 150 毫秒（0.15 秒），它的通話品質就會下降甚至掉包。

所以像這種屬於 Real-time（即時）的應用，語音、影像，它選擇的就是 UDP，因為 UDP 的負擔（Overhead）很輕，這樣才能確保每一個語音或影像封包的負擔維持最低，所造成的延遲才會低。各有這樣的訴求，要求多控制還是求快，你就會選擇不同的協定來開發。

現代化的應用越來越複雜，所以你會看到一個現象，就是兩個都用。不像早期的話可能就是二選一，現在因為應用太複雜了，變成兩個都需要。比如說一開始要做好連線控制，但是往後大量的資料傳輸就改用 UDP，這樣才快。

最好的一個例子就是我們名稱解析的 DNS。大家都熟悉 DNS，DNS 名稱解析在我們使用者 Client 端是用 UDP Port 53；但是在 Server 跟 Server 之間要做資料庫的同步（兩台以上的 DNS 伺服器做 Database Replication），那個就是要嚴格控制交換過程，確定它是一個穩定可靠的同步，所以 Server 間用的是 TCP Port 53。一樣是 Port 53，看你今天用在哪裡：用在 Server 與 Server 之間就是 TCP 53，用在 Client 到 Server 的查詢則是 UDP 53，這就是雙管齊下的好處。

現代化的應用幾乎都是類似這樣子雙管齊下。當然 Port Number 也不見得一定相同，可能會錯開，因為畢竟早期 1024 以前的 Well-known Port 早就被用光了。後來開發的應用通常都在 1024 以後，微軟或是各家廠商開發完應用之後要去向 IANA 註冊 Port Number，保留給該應用專用。

我們這裡重點會擺在傳輸層到應用層，對應到 OSI 七層模型中的第四層到第七層。常見的協定與應用像檔案傳輸 FTP 用的是 TCP Port 21；事實上不止 21，還有 Port 20，Port 20 是用來傳輸資料（Data）的。這就是我跟各位講過的，一般會分成 Control Plane（控制層）與 Data Plane（資料層），通常會錯開不同的 Port。

像 Telnet、HTTP，甚至後來改用的 SSH、HTTPS 都是走 TCP。SSH 是 Port 22，HTTPS 是 Port 443，這些都是走 TCP。右邊這種簡易型的檔案傳輸叫 TFTP（Trivial FTP），它走的是 UDP Port 69。同樣是檔案傳輸，FTP 走 TCP 20/21，簡易型的 TFTP 就敢用 UDP，因為走 TCP 的負擔總是比較重。光是看它的 Header 欄位就非常龐大，UDP 的欄位才四個，非常簡單；TCP 湊一湊超過十個欄位，負擔當然重，但它可以做很多精細控制。

另外像網管專用的 SNMP，走的也是 UDP。比較特別的是剛剛介紹的 DNS，它同時動用到 TCP 跟 UDP，在示意圖中故意畫在中間，因為兩者都有用到：Server 間用 TCP 53 做資料庫同步，Client 到 Server 查詢用 UDP 53。後來很多新開發的應用也是類似這種情形，一開始建立 Session 需要控制先走 TCP，建立起來之後改走 UDP 傳輸資料以求快速。天天在用的 DHCP 也是屬於 UDP，還有時間同步的 NTP 也是走 UDP。

在常用通訊協定清單中：Email 收發中的 SMTP 走 TCP Port 25；遠端連線管理 SSH 走 Port 22；Domain 指的是 DNS，走 TCP/UDP Port 53；動態路由協定 RIP 走 UDP；還有 Web 的 HTTP、早期 Gopher；做 Single Sign-On（SSO）單一簽入的 Kerberos 也是 TCP 與 UDP 兩者都有用；Email 收信還有 IMAP 與 POP3。

現在絕大部分都改走安全加密的協定，盡量摒棄不安全的明文協定。早期設計協定時沒有考慮到加密問題，後來走在 Internet 這種公開環境，資料很容易被攔截竊聽，所以逐步改用安全協定。遠端管理從 Telnet 改用 SSH（Port 22）；網頁瀏覽 HTTP 改用 HTTPS（Port 443，搭配 SSL/TLS 加密）；檔案傳輸從明文 FTP 改用 SFTP（基於 SSH）或 FTPS（基於 SSL/TLS）。

Telnet 做遠端管理是 Port 23，因為完全沒有加密，傳輸帳號密碼都暴露在網路上，已經不再安全，現在都會改用安全的 Port 22 SSH。簡易檔案傳輸 TFTP 走 UDP Port 69，例如在 Cisco 設備上把 Running Config 備份複製到 TFTP Server，在封閉獨立的安全管理網段內用 TFTP 傳檔速度最快。

當伺服器為眾多使用者提供服務時，多個使用者同時連到伺服器，且伺服器本身也會同時跑多個應用。伺服器身兼多職，可能同時是 Web Server、FTP Server 甚至 Mail Server。當使用者的封包到達時，伺服器必須辨識該封包要存取哪一個應用程式，這就必須檢查封包內的 Destination Port Number（目的連接埠號），看它是 TCP 還是 UDP 的哪一個 Port，才能正確交付給對應的應用程式進一步處理。

---

## 🚪 二、連接埠（Port Number）架構：Source Port vs. Destination Port 與多工分流

當使用者同時連線到伺服器，封包有走 TCP 的、也有走 UDP 的。封包內會帶有 Port 號碼，例如 Destination Port 是 80 或 443，而後面隨機產生的則是 Source Port（來源連接埠）。

Source Port 通常是一個比較大的數字，必定是 1024 以後、甚至是好幾萬（三萬以後）的動態連接埠。Port 的欄位長度為 16 個 bit，所以最大範圍是 $2^{16} = 65536$（0 到 65535）。Source Port 一般使用數字較大的動態 Port；至於 Destination Port 通常是數字較小、早已定義好的知名連接埠（1024 以前）。

在傳輸層與網路層的協定號碼（Protocol Number）中：ICMP 是 1 號，TCP 是 6 號，UDP 是 17 號，各自有明確的協定編號。

TCP 與 UDP 的運作原理與表頭結構有顯著差異。TCP 本身的 Header 固定有 20 個 Bytes。所謂的 Segment（區段），就是表頭（Header）加上後面的 Payload Data。TCP Segment 與 UDP Segment 的表頭欄位差異極大：TCP 為了提供各種控制與可靠傳輸服務，表頭固定耗掉 20 個 Bytes；而 UDP 的表頭只有 8 個 Bytes，不到 TCP 的一半。

TCP 表頭包含：Source Port、Destination Port、Sequence Number（序號）、Acknowledgment Number（確認號碼）、Data Offset（標頭長度/偏移量）、Reserved、Control Flags（控制旗標）、Window Size（視窗大小）、Checksum（校驗和）、Urgent Pointer（緊急指標）以及 Options。

控制旗標共有多個 Bit 用來決定目前的連線行為，例如建立連線所用的 Three-way Handshake（三次交握）：SYN Bit、ACK Bit、FIN Bit、RST Bit 等。如果是純連線請求，SYN Bit 等於 1；如果是回應連線，SYN 與 ACK 兩個 Bit 都等於 1；收到確認則是 ACK Bit 等於 1。

---

## 🤝 三、TCP 雙掛號 vs. UDP 平信比喻與連線交握機制

TCP 表頭中的 Window Size 是用來做流量控制（Flow Control）。Window Size 告訴傳送端「我目前一次最多可以接收多少資料量」，由接收端根據自身 Buffer（緩衝區）的承受能力動態告知傳送端。如果接收端緩衝區充足，Window Size 就開大，一次可以傳多一點，減少往返次數以提升傳輸效率；如果接收端負擔吃緊，Window Size 就調小，傳送端就必須降低發送量，避免接收端緩衝區溢位（Buffer Overflow）而爆掉。

TCP 共有 11 個欄位，表頭負擔非常重。因此像語音、影像等求快的 Real-time 應用絕不適合用 TCP，因為語音小封包如果光 Header 就吃掉 20 Bytes，表頭甚至比資料本體還大，效率極差。因此求控制與可靠性的用 TCP，求快的用 UDP。

TCP 的核心行為稱為連線導向（Connection-Oriented）。它的定義是：通訊雙方必須先成功建立連線，之後才會開始交換資料。如果前置的三次交握（Three-way Handshake）沒有完成，後續資料完全不會傳送。在 Cisco 設備上使用指令 `show control-plane host open-ports` 可以檢視目前成功建立（Established）的連線狀態。

此外，TCP 是點對點的單播（Unicast）傳輸，無法直接做到多播/群播（Multicast）。連線導向建立連線的主要目的，就是讓雙方事先協調通訊參數（例如 Initial Sequence Number、Window Size 等）。雙方協調好之後，後續的封包重傳（Retransmission）與確認（Acknowledgment）全部依賴 Sequence Number 來辨識。掉了哪一個序號就要求重傳哪一個序號，確認收到哪些序號也是依賴序號確認。

我們可以用郵政系統做個生動比喻：**TCP 就像「雙掛號信」**，寄出去必須有簽收回條（ACK），確認對方確實收到；**UDP 就像「平信」**，寄出去完全不保證送達，途中掉包也沒有任何通知與補償。

在 TCP 建立連線的三次交握（Three-way Handshake）流程中：
1. **第一次交握（SYN）**：Client 端主動送出帶有 SYN 旗標的封包（例如目的 Port 80，隨機 Source Port），SYN bit = 1。
2. **第二次交握（SYN-ACK）**：Server 端收到後，回應帶有 SYN 與 ACK 旗標的封包（Source Port 80，Destination Port 回到 Client 的 Port），SYN 與 ACK bit 均為 1。
3. **第三次交握（ACK）**：Client 端收到後，回傳最後的 ACK 確認封包，ACK bit = 1。

完成這三次交握後，連線即正式進入 Established 狀態，開始交換資料。

駭客常見的 DoS 阻斷服務攻擊手法之一，就是著名的 **SYN Flood（半開連線攻擊，Half-open Attack）**。駭客故意只做前三分之二，送出大量 SYN 請求，當 Server 回應 SYN-ACK 後，駭客故意不送最後的三分之一 ACK。這會導致 Server 的 Session Table（連線狀態表）中掛滿大量的 Half-open 連線，持續佔用系統資源與記憶體，最後造成 Server 記憶體耗盡而崩潰當機。防範這種 Half-open 攻擊是防火牆的重要職責，防火牆會監控連線狀態，一旦發現半開連線超量或逾時未完成，會主動拆除中斷，保護後端 Web Server。

在連線正常終止時，雙方會使用 **FIN（Finish）** 旗標（FIN bit = 1），彼此禮貌性告知通訊完畢並確認關閉；而在異常或強制中斷時，則會使用 **RST（Reset）** 旗標，瞬間強行切斷連線，不再等待對方的確認回應。

在資料傳輸確認機制中，Sequence Number 與 Acknowledgment Number 的長度相同。傳送端送出資料時附帶序號，接收端確認無誤後，回傳的 ACK 號碼即為「期望收到的下一個序號」。如果中途掉包，接收端回傳的 ACK 會停留在遺失區段的起始序號，要求傳送端重新補傳。

Window Size 採用 **滑動視窗（Sliding Window）** 機制，它是動態伸縮調整的。當網路暢通且接收端緩衝區充裕時，Window Size 會動態放大；當接收端負擔繁重、緩衝區吃緊時，Window Size 會主動縮小，動態調節發送速率。

---

## 🔄 四、雙向通訊 Port 號翻轉與防火牆/ACL 進出規則匹配實務

當封包從 Client 發往 Server 時，Source Port 是動態 Port，Destination Port 是服務 Port（如 80）；當 Server 回傳封包時，兩者會完全對調翻轉，原本的 Destination Port 變成 Source Port，原本的 Source Port 變成 Destination Port。

這個原理在設定防火牆與 ACL（存取控制清單）進出規則時至關重要：
- 如果是在介面套用 **Inbound（進入）** 規則，檢查的是封包的目的地 Port；
- 如果是在介面套用 **Outbound（出去）** 規則，檢查的對象就會翻轉為來源 Port。
必須搞清楚 In/Out 方向與匹配標的，否則過濾規則必定寫錯。

UDP 協定表頭僅有 8 個 Bytes，欄位極其精簡，僅包含：Source Port、Destination Port、Length（長度）與 Checksum（校驗和）四個欄位。負擔極低，非常適合語音（VoIP）與視訊會議等 Real-time 即時多媒體傳輸。

在即時多媒體傳輸品質保障中，有三大關鍵 QoS 網路參數：
1. **One-way Delay（單向延遲）**：必須控制在 150 毫秒（0.15 秒）以內；
2. **Jitter（抖動）**：封包間隔時間的變異度，一般不能超過 20 毫秒；
3. **Packet Loss Rate（掉包率）**：必須壓在 1% 以下。

若超出這三個參數限制，語音就會出現雜音破音甚至斷線，視訊畫面則會模糊停頓。

UDP 屬於非連線導向（Connectionless），不需預先握手即可直接傳送資料。雖然傳輸層 UDP 本身不提供重傳機制，但應用程式可在 Application Layer（應用層）自行設計補傳邏輯。

最後探討 DNS（網域名稱解析系統）。由於 IP 位址（尤其 IPv6 128-bit 位址）極難記憶，人類習慣使用 URL 與域名（例如 `www.cisco.com`）。

DNS 的查詢行為稱為 **遞迴式查詢（Recursive Query）**：
1. 本地端先檢查優先權最高的主機對應檔（**Host Table / hosts 檔案**）；
2. 若無則查詢作業系統的 **Local DNS Cache**；
3. 若無則向設定的 DNS Server 提出查詢；
4. DNS Server 先查本身的 **Server Cache**；
5. 若無快取，DNS Server 會展開階層式遞迴查詢：從全球 13 組 **Root Server（根伺服器）** 開始，依序指引至 **TLD Server（頂級網域名稱伺服器，如 .com、.org、.gov 或國碼 .tw）**，再轉介至企業授權維護的 **Authoritative DNS Server（授權 DNS 伺服器）**，最終取得解析結果回傳 Client，並在各級 Cache 中快取該紀錄以加速後續查詢。

必須特別注意解析順序的安全意涵：Host Table 的優先權高於 DNS 快取與外部查詢。如果駭客入侵竄改了系統的 Host Table，將域名直接指向惡意釣魚主機，系統根本不會發動 DNS 查詢就會直接連上駭客伺服器。因此解析順序必定是：**Host Table 優先 $\to$ Local Cache $\to$ Server Cache $\to$ Authoritative Database**。

好，我們這一段先講到這裡，大家休息十分鐘。
