---
title: "Introduction to OSINT & Cyber Threat Intelligence (CTI) Sharing Session"
event: "20260927-Intro-to-OSINT-CTI"
date: "2026-09-27"
speakers: ["Tunku Irfan", "foxy"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
category: "5-Master"
tags:
  - "OSINT"
  - "Cyber Threat Intelligence"
  - "CTI"
  - "Google Dorking"
  - "Sherlock"
  - "Passive Reconnaissance"
  - "MyCERT"
  - "Doxxing"
  - "Defamation"
---

# 🎙️ Introduction to OSINT & Cyber Threat Intelligence (CTI) Sharing Session (Tunku Irfan / foxy)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。保留講者所有原話發言、語意轉折、現場互動對話、幕後故事與問答，**未做任何刪減或摘要縮寫**；本篇逐字稿將口說馬來語/英語混雜之現場語音，轉譯為專業技術英文原話 Verbatim，並於每段落下方附上精準繁體中文對照翻譯，全面修訂語音辨識錯字、同音字與專有名詞，並完整收錄文檔末端之會議即時文字聊天室互動記錄。

---

## 🎙️ Part 1: Introduction to OSINT & Passive Reconnaissance (Tunku Irfan)

### 00:00 - The Boundary Between OSINT, Curiosity, and Criminal Doxxing

**Tunku Irfan**: Some people might think of this as stalking, right? I know some of you are smiling right now—as soon as someone mentions "crushes", you start smiling, right? Who knows, right? But please, even if you are curious, don't let it escalate to doxxing. Doxxing is an entirely different matter. For instance, imagine you get into a heated debate or argument on social media in the comments section with someone you don't agree with. Then you decide to "OSINT" them, uncover their private residential address, and expose it publicly in the comment section. Please never do that—that is unequivocally a criminal offense.

> **繁中翻譯**：有些人可能會覺得這就像肉搜跟蹤狂對吧？我知道有些人已經在笑了，一提到暗戀對象大家就開始會心一笑，對吧？誰知道呢。但拜託大家，就算出於好奇，也千萬不要升級成惡意起底（Doxxing）。Doxxing 是完全兩回事。比方說，你在社群媒體的留言區跟某個人吵架、產生爭執，因為看對方不順眼，你就去對他做「OSINT」，查出人家的私人住家地址並公佈在留言區——千萬不要這麼做，這絕對是犯法行為。

**Tunku Irfan**: Doxxing someone by publishing their private address in comments is illegal. Beyond that, OSINT (Open-Source Intelligence) has countless legitimate use cases. Today, I'll share around ten key points, but there are far more in reality. The most valuable application of OSINT is in Threat Intelligence (CTI), which is a vital branch of cybersecurity. Red Teams and penetration testers may also utilize OSINT depending on the company scope. When I was an intern doing penetration testing, I didn't personally conduct much OSINT, but that varies by organization.

> **繁中翻譯**：在留言裡公開他人私人地址這叫做惡意起底（Doxxing）。除此之外，OSINT（開源網路情報）還有無數正當的應用場景。今天我會列舉大概十個要點，但實際上遠遠不止。其中最具價值的應用是在威脅情資（Cyber Threat Intelligence, CTI），這是資安非常重要的分支。紅隊與滲透測試員也會根據公司需求使用 OSINT。我當初實習做滲透測試時雖然沒做太多 OSINT，但這主要取決於各家公司的業務範疇。

---

### 01:27 - Practical Personal Use Cases & Passive Reconnaissance

#### 01:27 Tunku Irfan {#01:27-speaker}

**Tunku Irfan**: OSINT isn't restricted to corporate work; you can use it for personal use cases. For example, before I started my internship, I wanted to do some reconnaissance. When I received the onboarding email, I found out the name of the manager who would be supervising me. What did I do? I ran an OSINT lookup on my manager's name! I was simply curious, and through that search, I found a video of their university assignment from years ago. Looking at their face, they seemed genuinely kind, and when I actually joined the company, they truly were very nice.

> **繁中翻譯**：另一個例子是，OSINT 不一定只能用在公事上，私底下也有實用場景。舉例來說，在我去實習之前，我想先做個背景瞭解。收到報到錄取信時，我知道了未來主管的名字。我做了什麼呢？我就去 OSINT 了主管的名字！我只是想看看，結果搜到了他當年大學時期做專題作業的影片。看面相感覺人很好，實際去報到後發現主管真的非常和藹。

**Tunku Irfan**: It is genuinely useful. For instance, when you have children in the future and want to evaluate a potential son-in-law, you would naturally conduct a background check, right? That is one legitimate personal use case where you want to verify someone's background.

> **繁中翻譯**：真的很有用。舉例來說，未來大家成家立業、有了女兒要找女婿，你肯定會想做背景調查對吧？這就是合法的個人使用場景之一，確認對方的底細。

---

### 02:33 - Data Exposure Demonstration & Self-OSINT Findings

**Tunku Irfan**: What kind of information can we actually uncover through OSINT? Look at this slide. Anyone here played the game *Watch Dogs*? I used to play *Watch Dogs*, and that game was actually what sparked my initial interest in cybersecurity. Through OSINT, you might obtain full names, IC numbers (identity card numbers), birth certificate numbers, and addresses. Of course, OSINT doesn't guarantee you will find all of this, but the possibility exists.

> **繁中翻譯**：我們透過 OSINT 究竟能查到什麼樣的資訊？大家看這張投影片。這裡有人玩過《看門狗》（Watch Dogs）這款遊戲嗎？我以前常玩《看門狗》，正是因為這款遊戲才讓我對資安領域產生濃厚興趣。透過 OSINT，你有可能查到全名、身分證號（IC）、出生證明編號等等。當然 OSINT 不能保證每次都能全數查出，但確實存在這種可能性。

**Tunku Irfan**: In this example screenshot, I censored the IC and birth certificate numbers myself for personal privacy reasons—not because the original sources were censored. Here is an experiment where I performed OSINT on myself. Notice the address and phone digits exposed? My personal details were publicly exposed. When I was doing my Diploma Final Year Project (FYP) on OSINT, during our faculty showcase, the Deputy Dean of our computing faculty happened to visit my booth.

> **繁中翻譯**：在這個截圖範例中，我自己把身分證與出生證明編號打碼了，這是出於個人隱私保護，而不是原本外洩的網站有打碼。這是我對自己進行 OSINT 的實測。大家看到地址跟號碼了嗎？這代表我的個人資料已經外洩了。當年我在做五專專題（Diploma FYP）研究 OSINT 時，在成果展當天，資工系的副院長剛好走到我的攤位。

**Tunku Irfan**: I demonstrated my OSINT technique on myself right in front of the Deputy Dean. I showed that our own university (UPSI) had accidentally exposed tuition fee payment receipts online. Anyone clicking that link could see my full tuition payments, student ID, and personal records! After I alerted the Deputy Dean, the university took down those exposed records within a few days, which was the exact positive outcome I wanted. If you discover exposed records at your university or institution, inform responsible staff immediately so they can purge them from public access.

> **繁中翻譯**：我當著副院長的面直接對自己做 OSINT 展示。我展示出我們大學（蘇丹依德理斯師範大學，UPSI）居然在網路上公開暴露了學費繳費收據！只要任何人點擊該連結，就能看見我繳交了多少學費、學號等所有個資。向副院長反映之後，學校幾天內就下架並清除了這些公開記錄，這正是我想達成的正向改善。各位如果在自己的大學或機構發現外洩個資，請務必通報給權責人員，讓他們從公開網路中撤除。

---

### 05:23 - The Identity Pivot Chain: Truecaller, Getcontact, DuitNow, and SSM

**Tunku Irfan**: Someone in chat asked if this is Google Dorking—I will demonstrate Google Dorking shortly. Before jumping into search dorks, we need to know our target's name. How do we pivot to find a full name? We have several practical techniques:

1. **Truecaller & Getcontact**: If you have a target's mobile phone number, caller ID apps like Truecaller or Getcontact can provide associated names or tags. These might be real names, nicknames, or aliases. For instance, if a number is tagged with "Seremban", we can infer geographical presence. If tagged with "Car Wash" or "KL", that gives valuable context. However, these are often just nicknames.

> **繁中翻譯**：聊天室有人問這是 Google Dorking 嗎——我等等馬上展示。在開始用 Dorking 搜尋前，我們必須先獲取目標的名字。我們該如何跳轉（Pivot）出真實姓名？有幾種非常實用的技巧：
> 1. **Truecaller 與 Getcontact**：如果你有目標的手機號碼，像 Truecaller 或 Getcontact 這類來電辨識 App 能查出關聯名稱或標籤。這可能是本名、小名或化名。比方說標籤出現「Seremban（芙蓉市）」，我們就能推斷居住地；如果標記「洗車」或「KL（吉隆坡）」，就能得到相關脈絡。但這些往往只是暱稱。

**Tunku Irfan**: 2. **DuitNow & Banking Transfer Previews (Maybank / Touch 'n Go)**:
If you want to discover someone's 100% verified legal full name, you can leverage DuitNow mobile transfer previews! When you initiate a peer-to-peer transfer to a mobile number via Maybank or Touch 'n Go (TnG) eWallet, the system displays the recipient's registered legal full name for payment verification before you confirm the transaction. You don't actually transfer any money—you simply view the recipient verification screen.

> **繁中翻譯**：2. **DuitNow 與銀行轉帳預覽（Maybank / Touch 'n Go）**：
> 如果你想獲取對方 100% 真實合法的全名，可以利用 DuitNow 手機轉帳預覽功能！當你在 Maybank 或 Touch 'n Go 電子錢包輸入目標手機號碼準備發起轉帳時，系統在確認交易前會顯示收款人的法定真實全名以供核對。你根本不需要真的轉帳，只要停在確認收款人姓名的預覽畫面即可。

**Tunku Irfan**: I personally prefer Maybank because Touch 'n Go tends to mask recipient names if you repeatedly check or back out of the transaction flow. With Maybank, the full name appears directly.

> **繁中翻譯**：我個人更推薦使用 Maybank，因為 Touch 'n Go 如果你頻繁點入查詢或退回，後續幾次可能會將名字打碼隱藏；而在 Maybank 上，收款人全名會直接完整顯示。

**Tunku Irfan**: 3. **SSM (Suruhanjaya Syarikat Malaysia - Companies Commission of Malaysia)**:
If your target runs a business and you possess their company registration number, you can query the official SSM e-Search portal. Entering the business registration number returns the registered proprietor's legal name and business addresses. If you log into the official SSM e-Info portal, you can even search directly by person's name to enumerate all companies registered under their identity.

> **繁中翻譯**：3. **SSM（馬來西亞公司委員會企業註冊查詢）**：
> 如果目標有在做生意，而且你擁有他的公司或商業註冊號碼，你可以利用馬來西亞 SSM e-Search 官方入口網站查詢。輸入商業登記號，就會列出法定獨資/合夥負責人全名與營業地址。如果你登入 SSM e-Info 系統，甚至可以直接輸入人名反查該人名下登記的所有企業。

---

### 08:47 - Google Dorking (Advanced Search Operators)

**Tunku Irfan**: Once you have the target's name, you can proceed to the next step: **Google Dorking** (also colloquially called "Google Hacking", though it is not actual hacking of servers—it is utilizing advanced search query operators to index exposed information).

Key Google Dorking operators:
- **`intext:`**: Searches for specific keywords appearing within the page body. For example, `intext:"Tunku Irfan"` forces Google to only return pages containing that exact phrase, rather than matching any random person named "Tunku" (like Tunku Abdul Rahman) or "Irfan".
- **`intitle:`**: Searches for terms specifically located within the page's HTML title tag. For example, `intitle:"UPSI"` filters pages whose HTML title contains that institution.
- **`site:`**: Restricts results to a specific domain or top-level domain (TLD). For example:
  - `site:tiktok.com intext:"Tunku Irfan"` filters strictly within TikTok.
  - `site:.my` restricts searches to Malaysian domains.
  - `site:.il` restricts searches to Israeli domains.
- **`inurl:`**: Requires the specified string to exist inside the URL path itself.
- **`link:`**: Finds web pages that link to a designated URL, which helps trace who is disseminating or promoting a specific portal.
- **`filetype:`**: Locates specific file formats. For example, `filetype:png` or `filetype:pdf intext:"cybersecurity" site:linkedin.com`.

> **繁中翻譯**：拿到目標全名後，就可以邁入下一步：**Google Dorking**（口語常稱 Google Hacking，但這並非直接駭入伺服器，而是運用進階搜尋運算子抓出公開索引的敏感資料）。
> 核心運算子：
> - **`intext:`**：搜尋網頁正文中包含的特定關鍵字。例如 `intext:"Tunku Irfan"`，強制 Google 精確比對該完整字串，而不會去搜出其他隨處可見的「Tunku」（如國父東姑阿都拉曼）或「Irfan」。
> - **`intitle:`**：限定網頁 HTML `<title>` 標題包含特定關鍵字，例如 `intitle:"UPSI"`。
> - **`site:`**：限制在特定網域或國碼頂級網域（TLD）。例如：
>   - `site:tiktok.com intext:"Tunku Irfan"` 嚴格只搜尋 TikTok 站內。
>   - `site:.my` 搜尋馬來西亞境內網站。
>   - `site:.il` 搜尋以色列網域。
> - **`inurl:`**：要求特定字串必須出現在網址 URL 路徑中。
> - **`link:`**：搜尋引用或超連結連向指定網址的頁面，可用於反查誰在協助推廣或散播特定網站。
> - **`filetype:`**：定位特定檔案格式，例如尋找透明背景圖示 `filetype:png`，或尋找敏感文件 `filetype:pdf intext:"cybersecurity" site:linkedin.com`。

**Tunku Irfan**: Boolean operators are also vital:
- **`AND`** (default space): Both terms must appear (`intext:UPSI intext:sulit`, where "sulit" means confidential, often exposing restricted university examination papers that were mistakenly indexed).
- **`OR`**: Matches either keyword.
- **`-` (NOT operator)**: Excludes specific keywords. For example, in Malaysia there are multiple public figures named Tunku Irfan (including the famous pianist Tunku Shafiq and another designer named Tunku Ismail). By appending `-intext:"Ismail"`, we filter out false positives and focus exclusively on the intended target.

> **繁中翻譯**：布林邏輯運算子同樣至關重要：
> - **`AND`**（預設空格）：兩組關鍵字皆須存在（例如 `intext:UPSI intext:sulit`，「sulit」代表機密，往往能抓出本應只給學生看、卻遭公開索引的期末考卷）。
> - **`OR`**：比對任一關鍵字。
> - **`-`（NOT 排除運算子）**：排除特定干擾名詞。例如馬來西亞有數位同名同姓的公眾人物（如著名鋼琴家或設計師），透過加上 `-intext:"Ismail"` 排除非目標人選，迅速縮小調查範圍。

---

### 20:52 - Username Enumeration with Sherlock & Permanent Social Media IDs

**Tunku Irfan**: Beyond search engines, username reconnaissance is critical. We use **Sherlock**, an open-source tool designed to hunt down social media accounts by username across hundreds of platforms.

How to deploy Sherlock:
- Run locally on Kali Linux, or inside a virtual machine (VirtualBox / VMware).
- Run on Google Cloud Shell (quick, web-based, no local setup required).
- Syntax: `sherlock --timeout 1 [target_username]` (you can filter specific sites like `--site spotify`).

> **繁中翻譯**：除了搜尋引擎，使用者名稱（Username）偵蒐也非常關鍵。我們使用開源工具 **Sherlock**，它能跨數百個社群平台自動獵捕特定帳號名稱。
> 部署方式：
> - 在本機 Kali Linux 或虛擬機（VirtualBox/VMware）執行。
> - 在 Google Cloud Shell 雲端環境執行（免本機環境、快速免安裝）。
> - 語法範例：`sherlock --timeout 1 [目標帳號]`（亦可指定特定平台如 `--site spotify`）。

**Tunku Irfan**: However, usernames can be changed by users. What stays permanent?
Social media platforms maintain permanent backend numeric IDs! For example, on TikTok, an account has three identifiers:
1. Display Name (can be changed anytime).
2. Username (`@handle`, can be changed periodically).
3. **Backend User ID (UID)**: A permanent numeric ID assigned at account creation that **never changes**.

Even if a target changes their username to evade tracking, if an investigator recorded their numeric User ID via tools like `tokcounter` or TikTok ID lookup utilities, querying that persistent ID will immediately resolve to their newly changed username.

> **繁中翻譯**：然而，使用者隨時可以更改帳號名稱。那有什麼是不會變的？
> 社群平台底層都維護著永久數值 ID！以 TikTok 為例，一個帳號擁有三重標識：
> 1. 顯示名稱（Display Name，隨時可改）。
> 2. 使用者帳號（`@handle`，可定期修改）。
> 3. **底層用戶 ID（UID）**：註冊時分配的永久固定數字，**終生不變**。
> 即便目標為了躲避追蹤而更換了帳號名稱，只要調查員先前透過 TikTok ID 查詢工具記錄了他的永久 UID，輸入該 UID 就能立即反查出他改名後的最新帳號。

---

### 34:06 - High-Impact Vulnerability Vectors: IC Numbers, SAPS, and Exposed CCTV

**Tunku Irfan**: Why is safeguarding your IC (National Identity Card) number so critical? In Malaysia, countless public and institutional portals historically relied solely on an IC number for authentication:
- **MySPR Semak**: Verifies voting constituency and residential district from just an IC number.
- **SAPS (Sistem Analisis Peperiksaan Sekolah)**: The Ministry of Education's school exam system. Historically, entering a student's IC number (along with school code/district) exposed their exact class, academic grades, and academic progression for every single year from primary through secondary school!
- **Tax & Travel Ban Portals**: LHDN / Immigration portals that expose whether a person has unpaid taxes or active travel restrictions based on IC queries.

> **繁中翻譯**：為什麼保護身分證號（IC）如此至關重要？因為馬來西亞過去有無數公共與政府系統，僅憑 IC 號碼就能查詢敏感資料：
> - **MySPR 選民登記查詢**：輸入 IC 即可查出戶籍選區與城鎮。
> - **SAPS（學校考試分析系統）**：教育部中小學成績系統。早期只要輸入學生 IC 號碼（搭配學校/地區代碼），就能查出該名學生小學到中學每一年在哪個班級、歷年考試成績與排名！
> - **出入境限制與稅務查驗**：移民局與稅務局（LHDN）系統，能憑 IC 查出是否有欠稅或限制出境紀錄。

**Tunku Irfan**: Furthermore, look at Google Dorking for exposed hardware:
`intitle:"webcam 7" inurl:"8080"` or querying RTSP / VNC streams. This indexes publicly exposed surveillance cameras (CCTV) that were configured without authentication. This is not hacking—the devices were misconfigured by their owners to face the public internet without credentials.

> **繁中翻譯**：此外，看看針對連網硬體的 Google Dorking：
> 像是 `intitle:"webcam 7" inurl:"8080"`，或者搜尋 RTSP 串流、VNC 遠端連線。這能檢索出大量未設密碼、公開暴露在公網上的監視器（CCTV）。這完全不是駭客入侵，而是設備擁有者自身配置不當，將設備直接暴露於公網所致。

---

## 🛡️ Part 2: Cyber Threat Intelligence (CTI) in Practice (foxy)

### 48:33 - Speaker Introduction & CTI Philosophy: Integrity Over Speed

**foxy**: Good evening everyone! Before I begin, I want to ask: are you comfortable with Malay, English, or Manglish (mixed)? Manglish it is! My slides are fully in English, but feel free to ask questions anytime.

I recently completed a 6-month internship as a Cyber Threat Intelligence (CTI) researcher. Tonight, this is not a vendor pitch, nor is it a dogmatic lecture where I claim my way is the only truth. I want to share the inside scoop on what CTI work looks like, what we actually use OSINT for, and why **research integrity matters far more than publishing quickly**.

> **繁中翻譯**：各位晚安！在開始前我想確認大家習慣馬來語、英語還是混合語（Manglish）？那就混著講吧！投影片完全是英文，但有任何問題隨時歡迎提問。
> 我剛結束為期六個月的威脅情資（CTI）實習研究員工作。今晚這不是廠商行銷推銷，也不是自以為是地說只有我說的才算數。我想帶大家深入瞭解 CTI 工作的真實日常、我們到底拿 OSINT 來做什麼，以及為什麼**研究誠信遠比搶快發布重要千百倍**。

**foxy**: Disclaimer: The views shared tonight are solely based on my personal experience and self-study; I do not represent any company or institution. Always conduct your own research. In cybersecurity, whatever you post online stays there indefinitely. If you publish unverified claims or false attributions, it can severely damage your personal reputation or your employer's standing.

> **繁中翻譯**：免責聲明：今晚分享的內容純屬個人經驗與自學心得，不代表任何公司或機構。請大家務必保持獨立思考與驗證。在資安領域，發布在網路上的東西會永久留存。如果你發布了未經核實的主張或錯誤的威脅歸因，可能會對你個人或公司的聲譽造成毀滅性打擊。

---

### 53:31 - What CTI Actually Does with OSINT: Discover, Connect, Enrich, Warn

**foxy**: In Threat Intelligence, what do we actually use OSINT for?
1. **Discover**: Monitoring public sources for leaked credentials, newly registered phishing domains, brand typosquatting, forum chatter, and emerging scams. When people post on social media saying "I got scammed," that is raw cybercrime telemetry. But you must not blindly jump into the drama—analyze objectively whether malware was involved, or if it was credential harvesting.
2. **Connect**: Identifying correlations across disparate indicators. For instance, in QR code phishing campaigns, are different domains using the same phishing kit? Are they operated by the same threat actor? You perform deep dives into DNS infrastructure, certificates, and source code patterns.
3. **Enrich**: When a Security Operations Center (SOC) receives an internal alert on an IP or domain, CTI enriches that alert with external threat context—historical passive DNS, WHOIS artifacts, and related campaigns.
4. **Warn**: Translating raw telemetry into actionable early warnings for SOC teams, internal stakeholders, or the public to block malicious infrastructure before the next victim is compromised.

> **繁中翻譯**：在威脅情資（CTI）中，我們到底把 OSINT 用在哪裡？
> 1. **發現（Discover）**：監控公開管道上的憑證外洩、新註冊的釣魚網域、品牌仿冒網頁、暗網論壇對話與新興詐騙。當民眾在社群發文說「我被騙了」，這本身就是第一手的犯罪情資。但絕不能盲目跟風瞎攪和，必須客觀分析究竟是惡意軟體感染還是釣魚憑證遭竊。
> 2. **關聯（Connect）**：找出零散指標之間的關聯性。例如在 QR Code 釣魚活動中，不同網域是否使用了相同的釣魚工具包（Phishing Kit）？是否由同一威脅行為者主導？這需要對 DNS 基礎設施、SSL 憑證及網頁源碼進行特徵深度比對。
> 3. **豐富化（Enrich）**：當資安維運中心（SOC）內部收到某個 IP 或網域告警時，CTI 負責調用外部情資予以豐富化——查詢歷史 Passive DNS、WHOIS 關聯記錄及過往活動脈絡。
> 4. **預警（Warn）**：將原始威脅特徵轉化為具體的防禦預警，通知內部 SOC 或公眾，在下一個受害者受害前封鎖這批惡意基礎設施。

---

### 58:48 - The Operational Lifecycle: When to Stop & The Repetitive Nature of Scams

**foxy**: Why do we use OSINT? Because it is fast, legal (as long as you stay within public sources), and represents the frontline where local threat campaigns emerge long before expensive commercial threat feeds (like Recorded Future or VirusTotal Enterprise) ever care about regional Malaysian campaigns. Commercial feeds often don't prioritize local WhatsApp or Telegram scams.

However, you must know **when to stop**:
- Never scan malicious QR codes using your personal banking app.
- Never access stolen databases via illegal intrusions.
- Never publicly attribute a threat actor if your evidentiary chain cannot withstand legal scrutiny. If you acquired evidence through questionable means, you cannot defend it publicly.

> **繁中翻譯**：為什麼要用 OSINT？因為它快速、完全合法（只要你停留在公開領域），而且是本地威脅活動的最前線，往往在昂貴的商業威脅情報源（如 Recorded Future 等付費情資）關注馬來西亞本地攻擊前，威脅就已經在社群公開擴散了。商業情報庫通常不會優先處理本地的 WhatsApp 或 Telegram 釣魚。
> 但你必須清楚知道**何時該踩煞車**：
> - 絕不要用自己真實的網銀 App 去掃描惡意 QR Code。
> - 絕不要透過非法入侵管道去取得外洩資料庫。
> - 如果你的證據鏈經不起法律檢驗，絕不可在公開場合指名道姓歸因威脅行為者。若你的情資來源站不住腳，在公眾面前你根本無法為自己辯護。

**foxy**: Threat actors operate on budgets. Creating entirely novel infrastructure for every single campaign is economically prohibitive. Therefore, threat actors heavily recycle their infrastructure:
- They stand up dozens of subdomains under a single parent domain hosted behind Cloudflare.
- When one phishing subdomain is taken down, they instantly spin up another.
- Phishing payloads follow repetitive patterns: fake Touch 'n Go giveaways, fake wedding invitation APKs (`Wedding.apk`), or double-extension malicious files sent over WhatsApp (`document.pdf.vbs` or `.apk.exe`).

> **繁中翻譯**：威脅行為者也是有預算考量的。為每次攻擊都從零打造全新基礎設施，成本過於高昂。因此，攻擊者大量重複回收利用現有資源：
> - 他們會在託管於 Cloudflare 背後的一個主網域下，建立數十個釣魚子網域。
> - 當其中一個子網域被檢舉下線，他們立刻啟用下一個。
> - 釣魚手法高度重複：假冒 Touch 'n Go 發錢、假結婚喜帖惡意安裝包（`Wedding.apk`），或者透過 WhatsApp 傳送雙重副檔名的惡意檔案（如 `document.pdf.vbs` 或 `.apk.exe`）。

---

### 01:06:31 - Case Study: QR Code Phishing & Active Infrastructure Breakdown

#### 01:06:31 foxy {#01:06:31-foxy}

**foxy**: I personally analyzed a widespread campaign targeting the Malaysian public around festive seasons. Threat actors deployed phishing pages mimicking Touch 'n Go eWallet login pages, stealing SMS OTPs and Telegram sessions.

All of this active infrastructure was mapped out. The most critical lesson I learned: **Screenshots and immutable evidence preservation are paramount!**
Why? Because malicious infrastructure exists today and vanishes tomorrow. Threat actors pull down servers or hosting providers suspend them within hours. If you don't take timestamped screenshots and archive raw network artifacts immediately, your entire evidence base disappears, and your findings cannot be independently audited.

> **繁中翻譯**：我曾親自分析過一起在節慶期間專門針對馬來西亞民眾的高度目標化攻擊。攻擊者架設了仿冒 Touch 'n Go 電子錢包登入頁面的釣魚網站，竊取受害者的簡訊 OTP 與 Telegram 登入權限。
> 當時我拆解了所有活躍的惡意基礎設施。我在這次調查中學到最深刻的教訓：**螢幕截圖與固定證據至關重要！**
> 為什麼？因為惡意基礎設施今天還在，明天可能就完全消失了。攻擊者會自行關閉主機，或者雲端業者幾小時內就將其停權。如果你沒有第一時間截圖並完整備份原始網路封包與日誌，你的整個證據鏈就徹底蒸發了，你的研究結論也將無法被任何人獨立審查。

**foxy**: What happens when an account is hijacked via Telegram or WhatsApp takeover? Threat actors don't stop at one victim. They immediately inspect recent chat logs, identify family and close friends (parents, siblings), and send urgent requests: "Please transfer money to this QR code." The recipient assumes it's their friend, scans the QR, and gets fleeced or compromised as well. It forms an infectious chain.

> **繁中翻譯**：當 Telegram 或 WhatsApp 帳號被盜（Account Takeover）後會發生什麼？攻擊者絕不會止步於單一受害者。他們會立即翻查最近的聊天紀錄，鎖定家人與至親好友（父母、手足），發送緊急求助訊息：「請幫忙轉帳到這個 QR Code。」親友誤以為是本人求助，一掃碼轉帳就落入圈套，甚至也被盜號，形成滾雪球般的傳播鏈。

---

### 01:10:26 - Threat Intelligence Publishing Ethics, Defamation, & MyCERT Reporting

#### 01:10:26 foxy {#01:10:26-foxy}

**foxy**: If you write public threat reports, craft them with extreme care and humility:
- If you assert a claim, be 100% certain of your evidence. Readers, peer researchers, and the accused entities will scrutinize you: "How did you verify this? Where is your proof?"
- If your conclusions are flawed, peers will cite counter-evidence in the comments, and your professional credibility will be destroyed.

> **繁中翻譯**：如果你撰寫公開的威脅情報報告，請務必極度謹慎與克制：
> - 如果你要做出某項結論，必須對自己的證據有 100% 的把握。讀者、同行研究員以及被你指涉的機構一定會嚴格質詢：「你是怎麼驗證的？證據在哪裡？」
> - 如果你的推論有漏洞，同行會在留言區貼出反面反駁文章，你的專業信譽將在一瞬間毀於一旦。

#### 01:11:23 foxy {#01:11:23-foxy}

**foxy**: Think twice before publishing. Always seek a **human second opinion**. Don't keep findings completely to yourself out of fear, but have trusted industry peers or seniors review your draft.

Never publicly accuse a legitimate entity of being compromised without verified confirmation. For example, never post: "Bank X has been 100% hacked, here is the proof," when the financial institution hasn't made an official disclosure. Even if you believe your technical evidence is sound, sensational public accusations risk serious **legal defamation (Public Defamation)** lawsuits.

> **繁中翻譯**：發布之前請三思。務必尋求**專業同行的第二意見（Human Second Opinion）**。不要因為害怕就完全不敢分享，但一定要讓信賴的資安前輩或同事審閱你的草稿。
> 絕不能在未經官方證實前，公開指控某家合法機構遭入侵。比方說，絕對不要在社群大喊：「某某銀行 100% 被駭客攻陷了，證據在此」，而該銀行根本尚未官方公告。即使你認為自己的技術證據確鑿，過度誇大的公開指控很可能會引來嚴重的**民刑事名譽毀損（Defamation）官司**。

#### 01:24:17 foxy {#01:24:17-foxy}

**foxy**: What should you do with high-value local threat intelligence?
Submit your findings to **MyCERT (Malaysia Computer Emergency Response Team)**!
A senior researcher advised me early on to submit campaign findings to MyCERT. Whether it directly leads to the arrest of the threat actors or phishing kit developers is uncertain, but it enables national cert coordinators to issue official advisories, sinkhole domains, and notify telecommunication providers.

> **繁中翻譯**：當你掌握了高價值的本地威脅情資，應該怎麼做？
> 請將你的調查結果提交給 **MyCERT（馬來西亞電腦緊急應變小組）**！
> 在我剛入行時，一位前輩就建議我把調查發現提交給 MyCERT。這份報告是否能直接逮捕幕後的威脅行為者或釣魚工具包開發者，我們無法保證；但這能協助國家級應變中心發布官方警訊、下架惡意網域並協調電信業者採取防禦阻斷。

---

### 01:33:48 - Context vs. Raw IOCs & AI Hallucination Pitfalls

#### 01:33:48 foxy {#01:33:48-foxy}

**foxy**: Someone asked: "Does CTI simply involve collecting Indicators of Compromise (IOCs)?"
No! Different organizations have vastly different job scopes. From my experience, **raw IOCs (IPs and hashes) are far less valuable than the narrative evidence and operational context**.
An IP address can be reassigned in 10 minutes. A file hash changes with a single byte modification. But the phishing workflow, the social engineering lure, the victim targeting pattern, and the adversary infrastructure lifecycle—that context is what enables security teams to make strategic decisions.

> **繁中翻譯**：聊天室有人問：「CTI 是不是就是到處收集入侵指標（IOC）？」
> 完全不是！不同組織的職責天差地別。以我的經驗來看，**單純的 IOC（如 IP 或雜湊值）遠不如背後的攻擊脈絡（Context）與證據鏈有價值**。
> IP 位址十分鐘內就能更換，檔案雜湊值只要改動一個位元組就完全不同。但釣魚的手法流程、社交工程話術、目標受害族群的特徵、以及攻擊者基礎設施的生命週期——這些情境脈絡才是真正能協助資安團隊做出戰略決策的核心情資。

#### 01:21:13 foxy {#01:21:13-foxy}

**foxy**: Beware of relying on Large Language Models (AI) for threat intelligence verification.
AI will agree with you regardless of whether you are right or wrong! AI outputs fluent, authoritative-sounding paragraphs, but **fluency is not evidence**. Asking an LLM "Does this evidence prove Actor X did this?" and receiving an affirmative response is not verification. Your professional name remains attached to your report long after the campaign dies. Protect your integrity above all else.

> **繁中翻譯**：千萬要警惕依賴大型語言模型（AI）來驗證威脅情資。
> 不論你的推論是對是錯，AI 往往都會迎合並附和你的說法！AI 能生成文筆流暢、看似權威的長篇大論，但**文筆流暢不等於事實證據**。拿著線索去問 LLM「這份證據是不是證明了某黑客組織所為？」然後 AI 回答「是的」，這根本不是科學驗證。當攻擊活動結束多年後，你的名字依然永遠掛在該份報告上。請把你的專業誠信置於一切之上。

---

## 💬 Part 3: Career Guidance & Community AMA (foxy & Tunku Irfan)

### 01:34:55 - Breaking into Cybersecurity & CTI as a Student / Fresh Graduate

**foxy**: We received several career questions from attendees:
1. **Can a Diploma or TVET / SKM student break into cybersecurity?**
   Yes! Cybersecurity is vast. While some corporate job postings express preferences for degree holders, many security teams care primarily about fundamental competencies, curiosity, and practical problem-solving. If you hold a Diploma or come from a Polytechnic, build a strong portfolio: write well-documented technical writeups, build home labs, explore cloud fundamentals (like AWS), and reach out directly to security team leads on LinkedIn.
2. **Are Capture The Flag (CTF) competitions essential?**
   CTFs demonstrate problem-solving and persistence. If a job description specifically seeks offensive security or technical assessment skills, CTF achievements will significantly strengthen your resume. However, building personal analytical projects—such as building a memory forensics tool or conducting original malware analysis—shows initiative that sets you apart.
3. **Do you need to start in a SOC before moving to CTI?**
   Not necessarily. While a SOC tier-1 analyst background provides solid exposure to real alert volumes, some firms hire junior CTI interns directly. However, junior CTI openings are relatively rare, so applying for SOC positions remains a solid stepping stone.

> **繁中翻譯**：我們收到了幾位與會者的求職提問：
> 1. **專科（Diploma）或技職（SKM）背景有機會進入資安圈嗎？**
>    絕對有機會！資安領域非常寬廣。雖然有些大企業在招聘簡章上寫偏好學士學位，但許多第一線資安團隊最看重的是基礎紮實度、求知欲與實務解決問題的能力。如果你是專科或理工學院背景，請建立扎實的作品集：撰寫高水準的技術分析文章、搭建自建靶場（Home Lab）、考取雲端基礎認證（如 AWS），並在 LinkedIn 上主動且有禮貌地向資安主管自我推薦。
> 2. **打 CTF 比賽是必備條件嗎？**
>    CTF 能證明你的逆向解題思維與毅力。如果應徵職缺偏重紅隊或技術評估，CTF 獎項在履歷篩選時確實加分。但親自動手打造獨立分析專案——例如基於 Volatility 開發記憶體鑑識工具，或對新型惡意程式做深入分析——更能展現主動研究能力，讓你脫穎而出。
> 3. **一定要先當過 SOC 監控分析師才能轉做 CTI 嗎？**
>    不一定。雖然 SOC 一線監控經驗能讓你熟悉真實告警量，但也有企業直接招收 CTI 實習生。不過初階 CTI 職缺相對較少，先從 SOC 切入依然是非常穩健踏實的途徑。

---

## 🎮 Part 4: Interactive Kahoot Quiz & Closing Session (Tunku Irfan)

### 01:58:12 - Reviewing Core Concepts Through Live Competition

#### 01:58:12 Tunku Irfan {#01:58:12-tunku-irfan}

**Tunku Irfan**: Let's launch our Kahoot game to review what we covered tonight! The questions are straightforward:
- **Question 1**: What does OSINT stand for? (Open-Source Intelligence — overwhelmingly answered correctly!).
- **Question 2**: What is the primary use case of OSINT? (Information gathering for security defense and research — not "telepathic mind reading"!).
- **Question 3**: What is Google Dorking? (Utilizing advanced search query operators to uncover exposed information — not actual server cracking).
- **Question 4**: What tool is used to enumerate usernames across social media? (Sherlock — not watching movies!).
- **Question 5**: What must you do before publishing findings online? (Think twice, preserve evidence, verify sources, and obtain a human second opinion).

> **繁中翻譯**：我們來玩 Kahoot 測驗，複習今晚的所有核心概念！題目都很生活化：
> - **第 1 題**：OSINT 代表什麼？（Open-Source Intelligence，開源網路情報——全場絕大多數人都答對！）。
> - **第 2 題**：OSINT 最主要的用途是什麼？（資安防禦與研究中的資訊蒐集——可不是讀心術能看穿別人大腦！）。
> - **第 3 題**：什麼是 Google Dorking？（運用進階搜尋運算子抓出暴露的資訊——而非入侵伺服器）。
> - **第 4 題**：哪套工具能跨社群平台枚舉帳號名稱？（Sherlock——不是看福爾摩斯電影！）。
> - **第 5 題**：在公開發布調查前必須做什麼？（三思而後行、留存固定證據、獨立核對來源，並尋求同行的第二意見）。

**Tunku Irfan**: Congratulations to everyone on the leaderboard! Thank you all so much for spending your Sunday evening with us. Even though tomorrow is Monday and we have work and classes, you dedicated your time to learn together. Insha Allah, if opportunities arise, we will organize another session. Thank you so much, goodnight everyone!

> **繁中翻譯**：恭喜登上排行榜前幾名的朋友！非常感謝大家在週日晚上撥空跟我們聚在一起。雖然明天週一大家都要上班上課，但大家依舊投入心力一同交流學習。未來若有機緣，我們一定會再舉辦交流活動。非常感謝大家，祝大家晚安！

---

## 💬 Part 5: In-Meeting Live Chat Log (會議即時文字聊天室互動記錄)

本節完整收錄並清洗來自 Google Meet / Teams 即時文字聊天室之聽眾交流、提問與技術回覆，忠實保留現場社群之真實互動歷程：

| 時間戳 (Time) | 發言者 (User) | 英文發言記錄 (Original / English Content) | 繁體中文語意對照 (Traditional Chinese Translation) |
| :--- | :--- | :--- | :--- |
| **21:01** | Shahrul Nizam | Free knowledge is rare, definitely won't miss joining hehehe. | 免費吸收知識的機會很難得，肯定不能錯過呵呵呵。 |
| **21:02** | piwww | Join for free knowledge 🔥🔥🔥 | 一起為了免費知識加入學習 🔥🔥🔥 |
| **21:03** | Ahmed | Hi, I'm transcribing this call with my Tactiq AI Extension. | 嗨，我正使用 Tactiq AI 擴充套件為這場會議進行即時逐字轉錄。 |
| **21:04** | piwww | ok 🫡🫡 | 收到 🫡🫡 |
| **21:04** | MUHAMMAD AMMAR | Me too. | 我也是。 |
| **21:05** | asfandyar | I can't see the screen shared. | 我這邊看不到分享的螢幕畫面耶。 |
| **21:06** | Ahmad Naqiuddin | Joe Goldberg (referencing the stalker character from the series *You*). | 喬·高德伯格（影集《安眠書店》裡的跟蹤狂主角）。 |
| **21:06** | piwww | Social media. | 社群媒體。 |
| **21:08** | piwww | Yes, because it is part of passive reconnaissance. | 沒錯，因為這屬於被動偵蒐（Passive Reconnaissance）的一環。 |
| **21:09** | asfandyar | Good thing you're not malicious! | 幸好你不是壞心腸的黑帽駭客！ |
| **21:10** | asfandyar | Why are universities not proactive about students' personal data privacy? | 為什麼大學對學生的個人隱私資料這麼不重視啊？ |
| **21:12** | piwww | In case anyone is wondering, this technique is called Google Dorking. | 如果有人在好奇的話，這套搜尋技術叫做 Google Dorking。 |
| **21:19** | mann | il (Israel country code TLD). | `.il`（以色列國碼頂級網域）。 |
| **21:19** | asfandyar | Is it `.il`? | 是不是 `.il` 啊？ |
| **21:23** | asfandyar | But sometimes AI provides really detailed answers too. | 但有時候 AI 給出的細節答案也真的非常豐富。 |
| **21:28** | foxy | Take your time, I don't have too much to share xD. | 慢慢來不急，我等等要分享的內容也不算太多 xD。 |
| **21:33** | piwww | And that's exactly why you should never use your real legal name online. | 這就是為什麼大家在網路上千萬不要用真實法定本名。 |
| **21:36** | piwww | And that's why you should never post personal matters on social media ahahaha. | 這也是為什麼大家不要在社群上發布私人生活瑣事，哈哈哈。 |
| **21:39** | piwww | Extra knowledge: if you search email OSINT, you can pivot to anything tied to that email address. | 額外補充：如果做 Email OSINT，你可以以此為支點反查關聯的所有帳號與足跡。 |
| **21:39** | asfandyar | The instructor is handsome and brilliant! | 講師又帥又聰明！ |
| **21:39** | piwww | Also search Caghi: an old breach repository where you can query IC numbers. Requires VPN; data originates from ~2012-2014 leaks. | 也可以查查 Caghi：一個能輸入身分證號反查外洩個資的舊資料庫網站。需要掛 VPN，資料大概是 2012 到 2014 年左右的外洩。 |
| **21:40** | Mohamed izzath | Is the audio breaking up for everyone? | 大家的聲音聽起來有在破音卡頓嗎？ |
| **21:41** | MUHAMMAD DANIAL | OMG Tunku freestyle! | 天啊 Tunku 開始即興 Freestyle 了！ |
| **21:42** | Imran | Will we receive these slides afterward? | 之後能拿到今晚這份投影片嗎？ |
| **21:42** | danish | Is there a class covering Maltego? | 有專門教 Maltego 圖形化情報工具的課程嗎？ |
| **21:43** | Ahmed | Back then SAPS had a flaw—you could find school and state details with only the IC number. | 當年 SAPS 成績系統有缺陷，只要輸入身分證號碼就能查出就讀學校與所在州別。 |
| **21:46** | Abdul Shukur | Shodan is considered OSINT too, right? | Shodan 搜尋引擎也算是 OSINT 的工具對吧？ |
| **21:46** | ZULAIKHA | By the way, is there an attendance certificate provided? | 請問這場有發放研習參與證書嗎？ |
| **21:47** | Abdul Shukur | Will the recording be shared later? I joined slightly late. | 稍後會提供錄影檔嗎？因為我剛剛比較晚進來。 |
| **21:47** | Khairul Zuhaili | (Replying to Zulaikha): Sorry, for free sharing sessions we do not issue certificates. | （回覆 Zulaikha）：抱歉喔，社群免費分享會我們不發放證書。 |
| **21:47** | Ahmed | Regarding that SAPS bug I found—you didn't even need the school name! Entering random IC numbers worked directly without knowing the school. | 關於我當年發現的 SAPS 漏洞——甚至根本不需要學校名稱！隨機輸入身分證號碼就能直接調出資料，完全免選學校。 |
| **21:48** | Adam Iskandar | Live demo right now haha 😂 | 現場直接實機 Live Demo 啦 😂 |
| **21:49** | asfandyar | Extremely clear and understandable, I would rate it 9/10! | 講得非常清楚易懂，我給 9/10 的高分！ |
| **21:49** | nazrul | If someone performs doxxing, can they be arrested by the police? | 如果有人惡意起底肉搜（Doxxing），會被警方逮捕法辦嗎？ |
| **21:49** | IZZWAN SYAHFIQ | Same here, 9/10 comprehension! | 我也是，理解度給 9/10！ |
| **21:49** | Ahmad Naqiuddin | 9/10! | 9/10！ |
| **21:49** | Abdul Shukur | We definitely need hands-on practice to really feel the concepts. | 一定要親自動手實作才能真正體會這些手法。 |
| **21:49** | piwww | Share doxxing tricks 😉😉😉 | 分享點肉搜技巧吧 😉😉😉 |
| **21:50** | MUHAMMAD AMMAR | Usually found on Threads. | 通常這些爭執都在 Threads 平台上面發生。 |
| **21:50** | Imran | Is there an OSINT method for car license plates? | 有針對汽車車牌進行 OSINT 反查的方法嗎？ |
| **21:51** | Jomo | I once hacked my friend on TikTok. | 我以前曾經在 TikTok 上破解過我朋友的帳號。 |
| **21:51** | piwww | A tip in case someone wants to know: scroll through someone's old photos, look for family pictures or housing neighborhood backgrounds, and run reverse image search. With luck, you can locate their neighborhood. | 分享一個技巧給想知道的人：翻目標以前的舊照片，找跟家人的合照或社區街景背景，拿去做以圖搜圖（Reverse Image Search）。運氣好的話能直接定位他家社區。 |
| **21:51** | Abdul Shukur | For car plates, maybe check the JPJ (Road Transport Dept) website or police traffic summons portals? | 車牌的話，或許可以查馬來西亞陸路交通局（JPJ）網站或交警罰單查詢系統？ |
| **21:52** | FARIS | Car repossession agents ("geng tarik kereta") probably know how to trace plates! | 那些專門幫銀行拖吊欠款車輛的拖車獵人（Geng Tarik Kereta）肯定最懂怎麼查車牌！ |
| **21:52** | nazrul | Very interesting and thank you for sharing, tuan! | 非常有趣，感謝兩位講師的無私分享！ |
| **21:52** | piwww | Trust me, it works! | 相信我，反向搜圖這招真的管用！ |
