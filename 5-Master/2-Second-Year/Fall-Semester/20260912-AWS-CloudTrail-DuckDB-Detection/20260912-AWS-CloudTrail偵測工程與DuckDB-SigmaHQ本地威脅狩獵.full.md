---
title: "AWS CloudTrail 偵測工程：基於 DuckDB 與 SigmaHQ 的本地日誌威脅狩獵"
event: "雲端資安偵測工程與威脅狩獵專題研討"
date: "2026-09-12"
talk_id: "SEC-AWS-CLOUDTRAIL-DUCKDB-SIGMA"
speakers: ["講者", "大會司儀"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
---

# 🎙️ SEC-AWS-CLOUDTRAIL-DUCKDB-SIGMA AWS CloudTrail 偵測工程：基於 DuckDB 與 SigmaHQ 的本地日誌威脅狩獵 (講者 / 大會司儀)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。保留講者所有原話發言、語意轉折、現場互動對話、幕後故事與問答，**未做任何刪減或摘要縮寫**；已全面修訂語音辨識錯字、同音字與專有名詞，並依演講敘事邏輯完成流暢的段落劃分與主題標題標註。

---

## 🎯 雲端日誌分析痛點與本地偵測工程革新：告別昂貴 Athena 與深夜 JQ 苦工

**講者**: ed to hack using your models, right, like and I don't think that's scalable because of course. There will be models in the future, probably private models, which may not even have a safeguards in place. My worry is that what will happen is someone will come along and regulate bad AI like malicious AI and like make it illegal to own an AI which can hack things and stuff.

> **繁中翻譯**：比如說，按照“阿那普里克”的說法，我是否可以使用你們的模型進行駭客攻擊呢？對吧，而且我認為這不可行，因為…… 未來將會出現一些模型，可能是私人定製的模型，而且這些模型甚至可能都沒有相應的安全措施。我的擔憂在於，可能會出現這樣一種情況：有人會出來制定相關法規，將那些不良的、惡意的 AI 規定為非法，甚至規定擁有能夠進行駭客攻擊的 AI 是違法的。

**講者**: It's hard to say. I really hope it doesn't go down the legal legal side of things but I have a feeling that. The AI companies themselves aren't necessarily. Incentivize to like the whole recent hacking, hugging face and all that sort of stuff. Feels more PR like unprofitable are happy that it got hacked almost rather than it being like Oh my God and it's terrible.

> **繁中翻譯**：這很難說。我真心希望事情不會發展到法律訴訟的地步，但我有種感覺會是那樣。這些人工智慧公司本身未必如此。激勵大家喜歡上最近的各種駭客行為、“擁抱臉”之類的活動吧。感覺這種“虧損”的情況更像是公關策略上的失誤，人們反而慶幸它遭到了駭客攻擊，而不是像“天哪，太糟糕了”那樣感到震驚和失望。

**講者**: Like they were quite happy that people were talking about how cool that models were that they could hack things randomly. I think it's gonna be very difficult for to make ethical elements to do that. Yeah, I'm sure that's not really an answer. Yeah, give me some insight regarding about to manage these kind of things only on compliance way, right. Yeah. OK. I got it. Thank you very much.

> **繁中翻譯**：就好像他們非常高興看到人們在談論那些模特有多麼酷，以至於居然有人敢胡亂去“破解”什麼東西。我認為要將道德元素融入其中將會非常困難。是的，我肯定那並不是一個真正的答案。好的，能給我講講如何僅透過合規的方式來處理這類事情嗎？好的。是的。好的。我明白了。非常感謝。

**講者**: OK, I think. So if anyone has question, we'll come to come to the stage and discussion with the speaker, no.

> **繁中翻譯**：好的，我想是這樣。所以如果有人有疑問，我們就會走到講臺前與演講者進行交流討論，不會安排其他環節。

**大會司儀**: Is lunch right now please collect your lunch in the North and South Carolina is on the. Please visit the Information Desk to exchange for recording. Go and share your images are good for the materials. Please take over lunch with you and do not reserve seats with personal items. Call is not responsible for a loss of debt. What property will be kept by the information desk?

> **繁中翻譯**：請問現在可以吃午飯了嗎？請到北卡羅來納區那邊領取你的午餐，南卡羅來納區的就在那邊。請前往諮詢臺換取錄音資料。去把你的照片分享出來吧，這樣對這些材料很有好處。請帶上午餐，不要在座位上擺放個人物品以方便他人使用。電話公司不承擔債務損失的責任。資訊臺會保留哪些財產呢？

**大會司儀**: Thank you. Call is not responsible for the loss of debt.  What property will be kept by the information desk?  Thank you. Not the favorite down local stock that lets your hand through the without writing SQL. And his study at the end? There is no live demo today, but every screenshot you will see is a real output. A public attached. If you want to see it running, come find us and afterwards?

> **繁中翻譯**：謝謝你！電話公司不承擔債務損失的責任。資訊臺會保留哪些物品呢？謝謝你！不是那種只能讓你的手從頁面中穿過而無需編寫 SQL 語句的本地熱門股票。那他最後的研究成果呢？今天沒有現場演示，但您所看到的每一張截圖都是實際的輸出結果。已新增至公共列表。如果您想觀看其執行情況，請聯絡我們，之後再來看。

**大會司儀**: Call the program. Why do Smothers everything here was reported this year alone. Customer detailed talk and via the MX NPM reach. Let's clear output at the rest. Takeover in 72 hours here for ITC Plus. First, what's decide is everything. Every team I know has streamed Cloud Trailer for you to control the build. Data events of protection for them and the events they drop are exactly demand they wanted six months later.

> **繁中翻譯**：啟動這個程式。為什麼斯莫瑟斯公司今年就發生了這麼多的事件呢？與客戶進行了詳細的交流，並透過 MX NPM 進行了溝通。接下來讓我們來處理剩餘的事項。 ITC 加強版產品將在 72 小時內完成此次收購。首先，決定性因素在於具體的選擇。我所瞭解的每一個團隊都提供了“雲模板”，供您根據需求進行調整。他們所申請的資料保護專案以及他們放棄的那些專案，其結果與他們六個月後所期望的完全一致。

**大會司儀**: After something happened. Second last thing in the three canals are a question for you. Every investigation starts with ruling data export, download, decompress donors. Of. Or you skip all that. And go straight to take you and grab at 3:00 in the morning. 3rd and this is the real 1, you need to know AWS. And the query languages.

> **繁中翻譯**：在某事發生之後。在這三條運河的最後一條裡，還有一個問題需要你來回答。每一次調查都始於對資料的匯出、下載、解壓以及資料捐贈者的核查。 “Of.”或者你也可以什麼都不做。然後直接前往，在凌晨三點的時候將你抓住。第三點，這才是真正的重點，你得了解 AWS。還有查詢語言。

**大會司儀**: And what attackers actually do. All at the time, that is a very small group of people. We wanted a tool for everyone who is not in that group. So what are the options today? Three come up a lot. Cortana, Subway surfer, Less SQL straight over the bucket. And it works well. But you build the tables, you learn the schema, and every exploratory purely costs manufacture money per terabytes, including the ones that running nothing.

> **繁中翻譯**：而攻擊者實際所做的事情是怎樣的。當時來說，那不過是個非常小的群體而已。我們希望為所有不屬於那個群體的人提供一種工具。那麼如今的選項都有哪些呢？ “三”這個數字經常出現。科塔娜，地鐵衝浪者，直接從桶裡取出少量的 SQL 資料。而且它執行效果很好。但你需要自己搭建表格，還要熟悉其架構，而且每一次的探索性操作都會耗費每太位元組數倍的成本。包括那些什麼都沒執行的程式。

**大會司儀**: That return nothing. A thing if you have one, you are already like that. It just isn't a 5 minutes decision. And we covered that. And they queue free, always there and it will get you through one night. It will not get you through the second one. Here what do you have in call? None of them has an opinion about what an attack works like.

> **繁中翻譯**：那毫無效果。如果你已經有了某樣東西，那你就已經是那樣的了。這可不是短短五分鐘就能決定的事情。並且我們已經解決了這個問題。而且那裡是免費排隊的，一直都有人在那裡排隊，這樣你就能在那裡過一夜了。這對你透過第二個關卡毫無幫助。請問您現在有什麼電話要接聽嗎？他們當中沒有人對攻擊的運作方式有相關的看法。

**大會司儀**: They give you. A glory box or a empty pipeline and everything after that is knowledge. you have to bring yourself. The works are open. Now what? You have never seen that is not. What is the? One way without MFA is noise. I'm going without MFA. There were enumeration then not. Change to your cloud to layer settings. That is an instant.

> **繁中翻譯**：他們會給你。一個榮耀之盒，或者一條空蕩蕩的管道，以及之後的一切，都屬於知識。你得依靠自己。這些作品已經開放展出。那接下來該怎麼辦呢？你從未見過那種情況。這是什麼？沒有使用多因素身份驗證的話就會出現錯誤。我決定不使用多因素身份驗證了。當時並沒有進行排序操作。請更改您的雲盤設定中的分層選項。那是一個瞬間。

**大會司儀**: And what is normal for this account? Nobody gives you that baseline. The community has written these answers down. Just not. One sentence do you take? Home, the locks are already yours. What is missing is the mini case knowledge and way to run it on your laptop. That is the whole idea. Of launch. You should not have to unpack 100 gigabytes before you can ask a question.

> **繁中翻譯**：那麼對於這個賬戶來說，什麼是正常的呢？沒有人會給你設定這個基準值。這個社群已經把這些答案記錄下來了。就是不行。您要一句嗎？家裡的裝置，其控制權已經歸您所有了。目前所欠缺的是相關的小型操作指南以及在您的膝上型電腦上執行這些裝置的方法。這就是整個的思路。關於啟動。您不應該在還沒能提出問題之前就先下載 100GB 的內容。

**大會司儀**: Nothing to set up. No agent, no cluster, no cloud account, no license. Your looks never really were optional. It also means you can use this own data. you are not allowed to upload. And the community knowledge, the detection come from the community. And our job was to make them. Vulnerable. Where does all of this come from? Cinema is the format and upstream rules.

> **繁中翻譯**：無需進行任何設定。沒有代理，就沒有叢集，沒有云賬戶，也沒有許可證。你的長相從來都不是可以隨意選擇的。這也意味著您可以使用自己的資料。您不得進行上傳操作。並且社群的知識、檢測工作都是由社群來完成的。而我們的任務就是製造這些東西。（身體或精神）脆弱的。這一切究竟是從何而來的呢？電影是其形式和基本規則的總和。

**大會司儀**: Might have a heart use. Techniques they actually observe in real security incidents. In the cloud 12 event name attached to spherical 1\. Then go on Railway query isn't responsible. Playbooks open start dashboard. And adaptive things like, which we test every rule against. All old coverage, all free. Thank you to everyone of these closure.

> **繁中翻譯**：可能有某種用途。他們在實際安全事件中實際觀察到的那些技術手段。在“雲 12”活動中，附帶的活動名稱為“球形 1”。然後繼續點選“鐵路查詢”按鈕，該功能不由本系統負責。點選“操作手冊”按鈕，進入主介面。還有那些具有適應性的內容，比如我們會將每一項規則都進行測試以加以驗證。所有過往的報道，全部免費提供。感謝每一位參與此次活動的人員。

**大會司儀**: This is the pipeline for the knowledge, not for the logs. On the left. The community publishes Cinema HQ rules. Attack techniques, glory samples in the middle. We packaged it into fire. Rules the obvious API list as a CSE, the hands as Yahoo. the chat as superset Jason. On the right, one command and you have all it over it. In your own disk and it flow back reports are false positive to Sigma HQ and every Sigma user gets picked.

> **繁中翻譯**：這是用於儲存知識的管道，而非用於儲存日誌的管道。在左邊。該社群公佈了“電影中心”的規則。攻擊技巧、榮耀樣本居中排列。我們將其整合成了“火焰”這一元素。將顯而易見的 API 列表歸類為 CSE 類別，而手部動作則歸類為雅虎類別。這場聊天相當於一個更大的集合體——傑森。在右邊，只要下達一個命令，你就能夠完全掌控它了。這些報告會直接傳送到您的個人磁碟中，並且會向西格瑪總部反饋為誤報資訊，所有西格瑪使用者都會因此受到影響。

**大會司儀**: The fix? Five questions, 2 answers. Set up a project. For one binary and one docker proposal. Retention. What the bill allows for everything. Data it leads your control or it stays on your laptop. And the last one is the one I care about. The detection contents is yours to read and to change. Pass to. Windows, Linux, Mac OS into an ARM? No. Install, no.

> **繁中翻譯**：解決辦法是什麼呢？五個問題，兩個答案。啟動一個專案。對於一個二進位制檔案的提案和一個 Docker 的提案。保留權。該法案涵蓋了所有相關事宜。資料要麼由你進行控制，要麼儲存在你的膝上型電腦中。而最後那一個正是我所關心的。檢測內容由您自行閱讀並修改。繼續前進。將 Windows、Linux 和 Mac OS 轉換為 ARM 系統？否。安裝，不行。

**大會司儀**: runtime, no agent. Pointed at the directory of Cloud Trail exports. It replaced JSON Gigi to Jason and Patrick directory, but selected with nothing to unpack first. It applies similar rules natively, including collaboration rules. And art, hyper art. And it keeps the role. Lesson. Next to each direction. Which matters when you have to begin your timeline later.

> **繁中翻譯**：執行時，沒有代理。指向了“雲軌跡匯出”目錄。它將 JSON 格式的資料替換成 Jason 和 Patrick 所使用的目錄格式，但首先選擇了無需解壓的檔案。它會自動應用類似的規則，包括協作規則。還有藝術，超凡的藝術。而且它依然保留著其應有的作用和意義。在每個方向的旁邊。而當您需要將時間線往後推遲時，這一點就顯得尤為重要了。

**大會司儀**: Whatever your export old lady looks like, the output is what I want you to look at. Just see Jason Jason or Duck TV. A table, not a wall of consultant. So you open it in Excel in hundreds while you hand the activity file straight to 70 down. And that is the exact exactly what we do to the that part of this talk. Three comments, each one looks at the same log from a different angle.

> **繁中翻譯**：無論您所展示的這位女士的長相如何，我想要您關注的重點是她的表現。就看看傑森·傑森頻道或者鴨子電視臺吧。需要的是一個展示臺，而不是一堵全是顧問的牆。所以你可以在 Excel 中將其開啟數百次，而將活動檔案直接交給 70 個人即可。而這就是我們在此次演講中所採取的相應做法。有三點看法，每一條都從不同的角度對同一份記錄進行了分析。

**大會司儀**: Whether the city timer in runs every Sigma rule and gives you 1 multiple timeline only even for reading? Literacy summary is no signature at all. It provides every user ARL so you can find the things nobody. That is your baseline, what this account normally does and what it almost never does. An update rules to the community's latest stream.

> **繁中翻譯**：這個城市計時器是否會在執行每個西瑪規則的同時為您提供 1 個多重時間線，哪怕只是用於閱讀呢？文憑證明根本算不上什麼“簽名”檔案。它為每位使用者都提供了“自動推薦列表”，這樣您就能找到那些無人關注的內容了。這就是你的基準值，即這個賬戶通常會進行的操作以及它幾乎絕對不會進行的操作。對社群最新直播內容進行了更新。

**大會司儀**: One command notice manager. No registry account. This is what are around. Allowing you to grasp the overall summary at a glance. This is why correlation matters in the cloud. In Windows networks, one event is opening up. Almost every API calls is great intimate. Someone is supposed to be calling it. The attack is the seniors.

> **繁中翻譯**：一名指令通知管理員。沒有註冊賬號。這就是周圍的情況。讓您一目瞭然地瞭解整體概要。這就是為什麼在雲環境中，相關性如此重要的原因。在 Windows 網路中，出現了這樣一種情況。幾乎每一次 API 呼叫都極具親密感。應該有人來處理這件事了。這次事件的肇事者是那些老年人。

**大會司儀**: So that's a support all. Or Sigma correlation types against count, value, count and temporal and temporal order. They are. The order itself is the signal. A change to your cloud trend settings in that order. Building one day. Alone it is nothing, together while high security findings. A signature only catch no threat. This command provides every identity instead.

> **繁中翻譯**：所以這就是全部的支援了。或者是針對數量、數值、數量以及時間順序和時間順序排列的西格瑪相關性型別。就是這樣。整個命令本身就是發出訊號的媒介。按照這個順序更改您的雲趨勢設定。正在建造中。單獨來看沒什麼，但一起行動時卻能取得高度的安全成果。一個簽名並不能阻止任何威脅。此命令會提供每一個身份的資訊。

**大會司儀**: We all ought to display one word by user at our end with event counts, time stamps and succeed. More. Timeline by anyone need to instantly accept the session. The third. Any few of you like this is source idea rest for everybody account. Read it from the top and you have your best life. Here 1 address is about 2/3 of everything to be closed.

> **繁中翻譯**：我們這邊每個人都應該以使用者為單位展示一個帶有事件數量、時間戳和成功狀態的條目。更多。任何人的時間線都需要立即啟動該會話。第三點。你們當中任何一個人喜歡這樣的內容，那它就是大家共同認可的優質素材。從頭開始讀下去，你就會擁有最美好的生活。這裡的 1 號地址要關閉的部分約佔總數的 2/3 。

**大會司儀**: That is normal for this account and now it. One user isn't seen twice among 10 million events is worth more attention than the top ten combined. Nothing required for these. For an hour you would never have shown them to you. Sit down to settle down. Send it down without carbon radial. Eye this is actually telling you what fired selling out lets you look around.

> **繁中翻譯**：對於這個賬戶以及現在的這種情況來說，這是正常的。在 1000 萬次事件中，若僅出現一次的使用者就比排名前十的使用者加起來還要重要。這些不需要任何東西。整整一個小時，你都不曾把它們展示給他們看。坐下來，安下心來。將其直接傳送出去，不要新增碳素縮寫。這實際上是在告訴你究竟是什麼導致了拋售行為，從而讓你能夠看清具體情況。

**大會司儀**: This actor is a binary you run. Semi run is a small stack you bring up. Four containers sharing one ductility file. The last full gesture that writes and free read only content. Don't have make 8 gigabytes of RAM an SSD no cluster no. cloud account, no license. Grow it, grow it, drop your export. Making just make up three URL's and you are hunting.

> **繁中翻譯**：這位演員是你所操控的二元體。 “半啟動”指的是你所啟動的一個較小的程式集。四個容器共用一個延展性檔案。最後一次完整的操作是寫入和僅讀取內容。不要將 8GB 的記憶體配置設定為使用固態硬碟且不啟用叢集功能。雲賬戶，無授權許可。繼續發展，繼續發展，減少出口量。只需設定三個網址，然後你就可以開始搜尋了。

**大會司儀**: Without them not English ever seen. 3 front scans are read only. They share one gap. They give 5 find mounted from your own disk. So to archive that case, you copy one file. That's really the reason this works at all. Come now and in process no server, no network of conduct query only touches the powers before. Kings of millions of events on a.

> **繁中翻譯**：沒有他們，英語就不會存在。 3 個前部掃描僅讀取一次。它們之間有一個間隔。他們會從您自己的磁碟中提取 5 個檔案並進行安裝。所以要實現這一操作，你需要複製一個檔案。這正是它能夠奏效的根本原因。現在就來吧，在這個過程中，沒有伺服器，也沒有網路連線，查詢操作僅限於之前的那些功能範圍內。數百萬個事件的主宰者們在......

**大會司儀**: With nothing behind it. More than 100 beauty in hands grouped by category. Identity and access in the biggest group because that is where cloud attacks live. Good usage moving without MFA password appeal intent and threatens to rebound. Download structure sharing UPS directory BI expiration for big network. CYP thread pattern and defense operating which is a category you check for us.

> **繁中翻譯**：（它）沒有任何支撐物。超過 100 種美容產品按類別進行了分類展示。在最大的這一群體中，身份識別和訪問管理尤為重要，因為這是雲安全攻擊的高發區域。良好的使用方式無需使用 MFA 密碼即可實現，但這種操作意圖存在潛在風險，可能會引發反彈。下載結構共享 UPS 目錄業務資訊到期設定，適用於大型網路。 CYP 線路模式及防禦操作，這是您需要告知我們的一個類別資訊。

**大會司儀**: Once you have found something you give one from a drop down noise here and not schema study but it's very right there and the results and you can read it and change it. This is a stream Rich. You like after running all of them 124 built in queries. 68 came back with rows. Each line expands into the Mita Picnic.

> **繁中翻譯**：一旦你找到了所需內容，就從這裡的一個下拉選單中選取一個選項，而不是進行復雜的方案研究。不過這樣做非常簡單直接，而且結果清晰可見，你可以閱讀這些結果並對其進行修改。這是一條小溪，理查德。你喜歡在執行完這 124 個內建查詢之後再繼續操作。 68 號車載著一群人回來了。每輛車裡都坐著一群人在舉行米塔野餐活動。

## 🔍 DuckDB 高效引擎架構：本地直接解壓查詢 CloudTrail、零日誌上傳與隱私合規

**大會司儀**: Telescope and the result table. And on the right is what you take away. One more turn and you get a single HTML. Every query is a technique that his career is a result. This is the higher you don't touch to the ticket or how to whoever takes a case after you selling. That is also where are going to get a screen on the left side.

> **繁中翻譯**：望遠鏡和結果表。而右邊的部分就是你所收穫的東西。再轉一圈，你就得到了一個單獨的 HTML 檔案。每一次的探索都是他職業生涯中的一種手段，而他的整個職業生涯則是一種成果。這是指你不能觸碰車票，也不能干預到你之後有誰來辦理購車手續的情況。那也是我們將在左側安裝螢幕的地方。

**大會司儀**: The identity as you. Timeline the commander I showed you earlier as a sort of table. For the right, those are used to fall spread by whether they succeeded or failed. It is the same CSV you could open in Excel, it is just faster to read here. Just remember it, UI is for asking one question at a time. Superset is the opposite, everything at once.

> **繁中翻譯**：你的身份。我之前給你展示的那位指揮官，我將其形象地比作一張表格。對於右邊的那部分而言，它們的落點位置取決於其是否成功或失敗。這與您在 Excel 中開啟的 CSV 檔案格式完全相同，只是在這裡讀取起來會更快一些。請記住這一點，使用者介面的作用就是一次只回答一個問題。 “超集”則恰恰相反，它是一切事物的集合。

**大會司儀**: On my screen. First and last seem her identity are societies are identified. These are for the question to you do not know to ask yet. You are not searching for something because you are writing for something to look around. Why should they? Together they are two outs of 1 workflow. So that is the first person run it on the road is it works and you get a timer in of butterfly plus a profile of every identity.

> **繁中翻譯**：在我的螢幕上。首先和最後所呈現的她的形象以及這些形象所代表的社會特徵，共同構成了她身份的全部內涵。這些是針對那些您尚未知曉該如何詢問的問題準備的。你並非因為想要尋找某樣東西而開始寫作，而是因為想要創作，所以才去觀察周圍的事物。他們為什麼要這樣做呢？實際上他們只是共同構成了整個工作流程中的兩個環節而已。所以這就是第一個在公路上進行測試的人，測試結果顯示它有效，而且還能獲取每名駕駛者的計時資料以及個人駕駛記錄。

**大會司儀**: Minutes from a class start. From a cold start cylinder is started as. Where else is that idea appear? When did he pressure up so that you should not fired? Then it will show how far it spreads and neither, neither. Enough about the design, let's watch it actually work. We will follow run intrusion flow start to finish. Although on a single laptop.

> **繁中翻譯**：上課時間到了。從一個冷啟動裝置開始，這個氣缸便啟動了。這種想法在其他地方出現過嗎？他是什麼時候施加壓力讓你得以留職的呢？然後它會顯示出其擴散的範圍，但結果卻並非如此。關於設計的部分我們就先不說了，接下來讓我們來看看它實際的執行情況吧。我們將全程跟蹤入侵流程的各個環節。儘管是在一臺膝上型電腦上。

**大會司儀**: A1 legged access key can lead to seven steps of an attack. This is the constructed example. The timer is not important. The order of the events is important. The first step is the initial access. The first thing an adapter does with the stolen key is check who they are. They call get call identity. This API call does not require partition.

> **繁中翻譯**：一個單腿進入的通道可能會引發一系列七步的攻擊行動。這是個人為設定的示例。計時器並不重要。事件發生的順序才是關鍵。第一步是初始訪問。當介面卡獲取到被盜的金鑰後，首先會確認其身份。他們稱之為“獲取身份資訊”。此 API 呼叫無需分割槽。

**大會司儀**: It returns the ALS account ID and the identity name. but then they make home get the user and this account alias is. At this point they have not changed anything, they are only learning about the account. Please remember get call identity. We will return to it to slide later. This second step is discovery. The attacker wants to know two things.

> **繁中翻譯**：它會返回 ALS 賬戶編號以及使用者姓名。但隨後他們會獲取使用者的個人資訊，並使用這個賬號別名。目前他們還沒有做出任何改變，他們只是在瞭解這個賬戶的情況。請記得記下通話身份資訊。稍後我們會再次提及並進行詳細說明。這第二步便是“發現”。攻擊者想要了解兩件事。

**大會司儀**: What can this key do? And what resources are in this account? List attached to user policies shows the permissions. Please packet shows the S3 packets. These are lead only actions so they may not create an alert. The attacker may also check individual services. For example, they may call get sent quarter for SES. The third step is credential access. This is where the impact becomes much bigger.

> **繁中翻譯**：這把鑰匙能做什麼呢？這個賬戶裡有哪些資源呢？使用者策略所附帶的列表列出了相應的許可權。請檢視“分組”部分，其中列出了 S3 類別的分組資訊。這些只是常規操作，因此可能不會觸發警報。攻擊者還可能會檢查個別服務。例如，他們可能會呼叫“獲取已傳送的季度報告”這一功能來獲取 SES 的相關資料。第三步是許可權認證。這一環節的影響會變得更為顯著。

**大會司儀**: The attacker calls get the secret value or GET parameter give. API calls may return database passwords for other important credentials. The attacker can then connect directly to the database. This database connection is not recorded in Cloud Trailer. So 1 little animal key can lead to a database. Even without other. The first step is persistence.

> **繁中翻譯**：攻擊者會呼叫“get”函式來獲取秘密值或“GET”引數“give”。 API 呼叫可能會返回其他重要憑證的資料庫密碼。然後攻擊者就能直接連線到資料庫。而這種資料庫連線並不會被記錄在“雲卷軸”中。所以，一個小小的動物按鍵就能連線到一個資料庫。即使沒有其他人。第一步是堅持不懈。

**大會司儀**: Now the attacker creates another way to access the account. Create a user and create access key can create a new identity and a new access key. The attacker may also use get federation token. They use a low time access key to create a parallel position. Can they create a URM for signing into the Internet console? if the system may continue or working for up to 36 hours even after the original key is deleted?

> **繁中翻譯**：現在，攻擊者找到了另一種獲取該賬戶許可權的方法。建立使用者並建立訪問金鑰可以建立一個新的身份以及一個新的訪問金鑰。攻擊者也可能使用獲取聯合令牌這一方法。他們使用一個低頻訪問鍵來建立一個平行位置。他們能否為登入網際網路控制檯建立一個統一的授權流程？如果在原始金鑰被刪除之後，該系統仍能繼續執行或工作長達 36 個小時，那會是怎樣的情況呢？

**大會司儀**: So deleting or locating the original key may not end the attacker's active session. The 5th step is privileged escalation. At the user two group can add the new user to an existing. Administrator group. The new user gets the punishment of that group. The attacker does not need to create a new policy. Attach user policy and put user policy can also add the permission.

> **繁中翻譯**：因此，刪除或更改原始金鑰並不能終止攻擊者的活躍會話。第五步是特權提升。在使用者組介面中，兩個組可以將新使用者新增到已有的使用者組中。管理員組。新使用者會受到該群體的懲罰。攻擊者無需建立新的策略。附加使用者策略以及設定使用者策略都可以新增許可權。

**大會司儀**: But these actions may be easier to notice. The six steps step is different aviation. The attacker tries to stop security loss and the security services. For example, they may call. Stop bugging or delegate trial for Cloudflare. They may also call beliefs detector for gun duty. In many moderns environments these actual play. The. Organization player is usually managed by the management account. A user in the member account cannot stop, so result is access denied.

> **繁中翻譯**：但這些行為可能更容易被察覺到。這六個步驟適用於不同的航空業務。攻擊者試圖阻止安全漏洞的出現以及相關安全措施的實施。例如，他們可能會打電話過來。停止打擾或將測試任務委託給 Cloudflare 公司。他們還可能會要求進行信仰測試，以確定是否適合執行槍支任務。在許多現代的環境中，這些活動正在實際開展。這個。組織中的使用者通常由管理賬戶進行管理。而成員賬戶中的使用者無法停止操作，因此會遭到許可權拒絕的處理。

**大會司儀**: Denied. But we should not ignore the failed action. A denied scope logging call is a song sign of an attack. Normal applications do not try to stop cloud play. Because this action failed, the later attack activity is still recorded. The civil and final set is impact. Now the attacker causes real damage. They may still data is so malware or use the account to make money.

> **繁中翻譯**：被拒絕了。但我們也不能忽視這一失敗的行動。一個被拒絕的範圍日誌請求就是一種明顯的攻擊跡象。正常的應用程式並不會試圖阻止雲遊戲功能的使用。由於此次行動失敗，後續的攻擊活動仍被記錄在案。民事部分和最終部分是相互影響的。現在攻擊者造成了實質性的破壞。他們可能仍會利用這些資料來傳播惡意軟體，或者利用該賬戶來謀取利益。

**大會司儀**: Like instances, launches new EC2 instances. The attacker may use for use them for crypto mining or other malicious activity. Set command using systems manager. To learn commands on existing instantly. It does not need FSH or an open inbox port. Get command invocation leaves the column result. This shows that someone learn the command and check its output.

> **繁中翻譯**：例如，可以啟動新的 EC2 例項。攻擊者可能會將它們用於加密貨幣挖礦或其他惡意活動。使用系統管理器設定命令。能夠即時學習到已有的指令。它不需要促卵泡激素（FSH）或者開放式的收件箱埠。獲取命令呼叫會留下列結果。這表明有人學習了該命令並檢視了其輸出。

**大會司儀**: Please also look at Invoke model. Crypto mining is not the only way to make money from a solar energy. Attacker can use solar credential to call another bedroom lock and learn AI models on the victims account. This type of attack is called LM jacking. The cost increases with added requests and the attacker can sell this access to other people.

> **繁中翻譯**：請也看一下“Invoke”模型。加密貨幣挖礦並非是利用太陽能獲取收益的唯一途徑。攻擊者可以使用太陽能認證來開啟另一間臥室的門鎖，並獲取受害者的賬戶中的人工智慧模型。這種攻擊方式被稱為“LM 篡改”。隨著請求的增多，成本也會相應增加，而且攻擊者還可以將這種訪問許可權出售給其他人。

**大會司儀**: This is still resource hijacking. The attacker is using a model instead of the GPU instance. If you see better lock import model in your logs, check it carefully. This is especially important is that Identity has never called it before. There are several steps and about 12 API calls hidden in gigabytes of cloud drive logs.

> **繁中翻譯**：這仍然是對資源的侵佔行為。攻擊者使用的是一種模型，而非 GPU 例項。如果在你的日誌中看到更優的鎖匯入模型，請仔細檢查它。這一點尤為重要的是，此前“身份”從未提及過此事。在數以吉位元組計的雲端儲存日誌中，隱藏著若干步驟以及約 12 次的 API 呼叫操作。

**大會司儀**: Next, let's see what Slack finds. This is a liquor selective example, not only other major incident. The time. Stocks shows the o rder of the events. Please do not use the time difference as a performance measurement. Now we will investigate the same attack with Zach. We use one command. We do not need a SIM and we do not need to involve logs into a data into data platform.

> **繁中翻譯**：接下來，讓我們看看 Slack 會發現什麼。這是一個關於酒類的特殊案例，而非其他一般性的事件。時間。 Stocks shows the o 股票能夠反映出事件發生的先後順序。請不要將時間差作為衡量業績的標準。現在我們將和扎克一起對同樣的攻擊行為進行研究。我們只需使用一個指令即可。我們無需配備 SIM 卡，也無需將日誌資料匯入資料平臺。

**大會司儀**: We learn Zack AWS City timeline and point it to the cloud for Jason files in the local Cloud trial folder. Let's add look at each role at 211 service. At 211 service deployment holds list attached to user policies for its own user. The letter is informational. Then nothing happens for about 40 minutes. At 2:52. Select detects possible packets enhance the level is low.

> **繁中翻譯**：我們按照扎克提供的 AWS 城市時間線進行操作，並將該時間線與本地“雲試用”資料夾中的傑森檔案關聯起來。讓我們來看看 211 服務中的每個角色。在 211 服務部署中，會為每個使用者在其使用者策略中附上相應的列表。這封信是告知性質的。然後大約 40 分鐘的時間裡什麼都沒有發生。在 2 點 52 分。選擇功能會檢測可能存在的資料包，並提升其級別，但當前級別較低。

**大會司儀**: 7 seconds later a collection move detects many Recon events. Delivery is high. There was no new API call at 25251 the The collection rule looks at earlier events together. That is why it detects the activity. The attack then continues. Three, select detects I am user creative. The letter is high. In environments where I am, users are literally used this little fires frequently.

> **繁中翻譯**：7 秒鐘後，一組檢測動作捕捉到了許多“偵察”事件。交付費用較高。在 25251 號位置沒有新的 API 呼叫。該收集規則會將先前發生的事件一併納入考量。這就是它能夠察覺到這種活動的原因。隨後攻擊便繼續進行下去。三、選擇檢測功能表明我具有一定的創造力。這封信很厚。在我所處的環境中，使用者們實際上會頻繁地使用這種小裝置。

**大會司儀**: Most of these events come from normal positioning jobs. Over time, ships may start even like this a lot. Then there is another gap of about 20 minutes. At 314, the attackers actually call secret manager get secret value. The letter is high. The results is important. Afraid to request is medium. Is medium but are successful request is high.

> **繁中翻譯**：這些事件大多源於常規的職位安排工作。隨著時間的推移，船隻可能會越來越多地呈現出這樣的形態。接下來還有大約 20 分鐘的間隔時間。在 314 這個位置，攻擊者實際上會呼叫“秘密管理器”並獲取“秘密值”。這封信很厚。結果很重要。不敢請求屬於中等程度。規模適中但成功率較高的請求數量很多。

**大會司儀**: This event makes the impact much bigger after getting the secret. The attacker can access another system directly. That activity may not appear in Cloud Trail. At 317, the attacker successfully caused issues 1 instances. This letter is million. A failed attempt would only. Below. Now let's see why the order matters. Look at the letter column.

> **繁中翻譯**：在得知這個秘密之後，這次事件所產生的影響就變得更大了。攻擊者能夠直接訪問其他系統。該活動可能不會出現在“雲軌跡”中。在 317 這個位置，攻擊者成功造成了 1 次故障。這封信價值百萬。一次失敗的嘗試只會...... 下面。現在讓我們來看看為什麼順序很重要。看看這個信件欄。

**大會司儀**: We have one informational event, 1 low event, 1 medium event and student high events. You may think the high events are enough. But each high event can also happen during. During normal work in environments that use I am users, I am user created. maybe a normal provisioning job. Get secret value may be a normal application within its own secret.

> **繁中翻譯**：我們有一個資訊類活動、一個低難度活動、一箇中等難度活動以及一系列學生參與的高難度活動。你可能會覺得那些重大事件已經足夠了。但每個重大事件也可能在這一段時間內發生。在使用“我”這一稱呼的環境中進行正常工作時，“我”這個稱呼是由使用者自己設定的。或許是一次常規的配置任務。獲取秘密值可能是在其自身秘密範圍內的一次常規操作。

**大會司儀**: If we look at each event binary. It may not look dangerous. So many teams close these alerts. A single event is not enough. We need to look at the events together. Their order is also important. The collation room requires at 2:52. This is a 25 minutes before the Issue 2 instance is launched. It also happened before the new I am user is created and before the secret is leading.

> **繁中翻譯**：如果我們將每個事件都視為兩個對立的方面來審視。它看起來可能並不危險。因此，很多團隊都會關閉這些警報。單靠一次事件是不夠的。我們需要一起審視這些事件。他們的順序也很重要。整理室需要在 2 點 52 分到達。這是在“議題 2”例項啟動前的 25 分鐘。這種情況還發生在新使用者尚未建立以及秘密尚未啟用之前。

**大會司儀**: This is why projection is useful. It does not only explain the attacker after it happens. It can show the attack while we may still have time to stop it. There is one important point about this timeline. Real attacks do not happen at labor internals like this. An attacker may list buckets and then stop for almost one hour later.

> **繁中翻譯**：這就是投影之所以有用的原因。它不僅僅是在事件發生之後對攻擊者進行解釋。它能夠顯示出攻擊的跡象，這樣我們就能在還來得及的時候採取措施阻止它。關於這個時間線，有一點非常重要。真正的攻擊不會發生在像這樣內部的勞動場所。攻擊者可能會列出所有儲存桶，然後稍作休息，大約持續一個小時。

**大會司儀**: They may check policies, they may wait another 20 minutes before listing users and instances. The attacker events are split over several hours. Normal activity happens between them. This matters for two reasons. You can not find this just by looking at the low lows. There is no clear group of suspicious events. 2nd. The collection time window must be long enough.

> **繁中翻譯**：他們可能會檢視相關政策，也可能再等待 20 分鐘之後再列出使用者和例項。攻擊事件分散在幾個小時內發生。他們之間會進行正常的交流。這之所以重要，有以下兩個原因。你不能僅僅透過觀察最低值就得出結論。目前並沒有明確的一組可疑事件。第二。採集時間視窗必須足夠長。

**大會司儀**: A short time window may be an attacker who waits between action. Uses community Sigma moves and population rules. It creates A DFYR timeline from the result. We did not need a query language while large data of home, but there is still one question. This timeline assumes that we already know each identity to investigate. To investigate in a real instant, we usually do not know that.

> **繁中翻譯**：短暫的時間間隔可能是攻擊者在行動之間所採取的等待策略。利用社群中的“西格瑪”移動規則和人口規則。它根據結果生成一個“DFYR”時間線。在處理家庭資料時，我們並不需要一種查詢語言，但仍有一個問題需要解決。此時間線假定我們已經知曉需要調查的每一個身份資訊。要即時進行調查的話，我們通常並不知曉這一點。

**大會司儀**: In a real investigation, we usually do not to start with a public timeline. we start with one piece of information. It may be an abusive report with an IP address, or it may be an access key found in the public laboratory. registry. The natural next step is to search the logs for that IP address or access key. But if you can hide a part of the attack, attackers do not always use the same IP address.

> **繁中翻譯**：在實際的調查過程中，我們通常也不會一開始就依據公開的時間線來進行。我們從一條資訊開始。這可能是一份帶有 IP 地址的違規報告，也可能是在公共實驗室中發現的訪問金鑰。登錄檔。接下來的自然步驟是檢視日誌，查詢該 IP 地址或訪問金鑰。但如果你能將攻擊的一部分隱藏起來，那麼攻擊者通常不會使用相同的 IP 地址。

**大會司儀**: They may use one IP address or the file to checks another address for this main attack. And the third address for the final action. They may also change access. Gives the key used for the first checks may not be the key used later. The attacker may create a new user and a new key during the attack. Look at the screen. 605 rules are detected events. The first row is get collar identity.

> **繁中翻譯**：他們可能會使用同一個 IP 地址或該檔案來檢查另一個地址，以實施此次主要攻擊。這是決定最終行動方案的第三個要素。它們還可能改變訪問許可權。首次驗證所使用的金鑰可能與後續驗證所使用的金鑰不同。攻擊者在進行攻擊時可能會建立一個新的使用者賬號和一個新的金鑰。看螢幕。檢測到 605 條規則事件。第一行是“獲取衣領標識”。

**大會司儀**: Which does not trigger detection rule. We have three source IP addresses and two access keys.

> **繁中翻譯**：這並不會觸發檢測規則。我們有三個源 IP 地址和兩個訪問金鑰。

## 🛡️ SigmaHQ 原生規則引擎與實戰威脅場景：從 IAM 提權到防禦規避 (Defense Evasion)

**大會司儀**: But they are all part of one attack. Let's say the first access was found public laboratory. If we search for that key, we find the first goal load. But we do not find the final impact line instances use the technology and we are not searching for that key. Now let's start a lot. In this case, we may begin with the second key because it launched the BC 2 instance.

> **繁中翻譯**：但它們都是同一場攻擊的一部分。比如說，第一次訪問所涉及的是公共實驗室。如果我們尋找那個關鍵元素，就能找到第一個目標載入項。但我們並未發現最終的衝擊線例項採用了該技術，而且我們也並未在尋找這一關鍵要素。現在讓我們開始操作吧。在這種情況下，我們可以先從第二個關鍵步驟開始，因為正是這個步驟啟動了 BC 2 例項。

**大會司儀**: If we search for that key, we find the last two rows, but we do not find the earlier discovery. The new I am user for get call identity. We can see the damage, but we cannot see how the attacker entered the account. So we cannot be sure that we have closed the original entry point. Searching for only the first IP address also loses most of the attack.

> **繁中翻譯**：如果我們去尋找那個鑰匙，我們會找到最後的兩行記錄，但找不到之前的發現記錄。新的“我正在通話”功能用於獲取通話身份資訊。我們能看到受損之處，但卻無法知曉攻擊者是如何侵入該賬戶的。所以我們無法確定是否已經完全堵住了最初的入口。僅僅搜尋第一個 IP 地址也會大大削弱攻擊效果。

**大會司儀**: No single IP address or access key shows the complete attack. The result depends on which information will let you pass. This is why selected items not one identity. Check checks at the cloud trail the call with Sigma loop. It puts all suspicious events on one timeline. The user access key and the user access key and the source IP address can be given.

> **繁中翻譯**：單個的 IP 地址或訪問金鑰都無法完整展現此次攻擊的情況。結果取決於哪些資訊能讓你透過稽核。這就是為什麼所選的專案並非屬於同一類別。檢查會將通話資訊與“西瑪環路”系統進行對比核對。它將所有可疑事件整合到一個時間軸中。可以提供使用者訪問金鑰、使用者訪問金鑰以及源 IP 地址等資訊。

**大會司儀**: We can see such by adding key or IP address later. But first we can see the complete attack. Because the IP address and the access key both change, what can show us beginning of the attack? Look at the first law. Get call identity happened at 2:52. This was 15 seconds before the first alert get caller identity does not trigger our rule.

> **繁中翻譯**：我們可以透過稍後新增關鍵字或 IP 地址來實現這一點。但首先我們可以看到整個攻擊過程。因為 IP 地址和訪問金鑰都會發生變化，那麼我們如何才能看出攻擊的起始情況呢？請看第一條定律。呼叫身份在 2 點 52 分時被確認。這是在首次警報發出前的 15 秒鐘，而此時獲取來電者身份這一操作並未觸發我們的規則。

**大會司儀**: It is a leader only API call under many normal tools using. But it can be an important sign of where an attack started when an attacker passed away. Shields and activity. They do not know which account or identity it belongs to. So they often call get call identity first. This gives us a useful check. If an identity first hopes by just action, but there is no get call identity near the start of each session.

> **繁中翻譯**：在大多數常規工具的使用中，這只是一個簡單的 API 呼叫操作。但當攻擊者死亡時，這一跡象可能表明了攻擊的起始位置。防護措施和活動情況。他們不清楚這屬於哪個賬戶或身份。所以他們通常會先進行身份確認的核實。這為我們提供了一個有用的檢驗手段。如果一個身份最初希望透過實際行動來達成目標，但在每次會話開始時附近都沒有相應的獲取身份資訊的選項。

**大會司儀**: It may not be the original entry point. Another identity may have been compromised. 1st in this example the second key has no capital added call it was created during the attack. This tells us that the first key was probably the original entry point. That is the key we must disable and rotate. We can only make this connection when all identities are on the same timeline.

> **繁中翻譯**：這可能並非最初的入口點。另一個身份資訊可能已經遭到洩露。在這個例子中，第二個按鍵並未新增任何字母大寫部分，我們將其稱為是在攻擊過程中建立的。這表明，第一個關鍵點很可能就是最初的入口位置。這就是我們必須關閉並更換的那部分關鍵裝置。只有當所有身份資訊都處於同一時間框架內時，我們才能建立起這種關聯。

**大會司儀**: If we search for only one IP address. For one key it passed low may not appear at all. So that keeps the events from every identity together so we can find the beginning of the attack. Three things to take home. Wow, you already have lost tractorage on and the epidemic is in your pocket right now. The fire was never collection, so we start with them finally on data you already have.

> **繁中翻譯**：如果我們只查詢一個 IP 地址。對於其中的一個關鍵指標而言，其數值偏低的情況可能根本不會顯現出來。這樣一來，就能將每個身份相關的事件整合在一起，從而讓我們能夠找到攻擊的起始點。三件物品請帶回家。哇，你已經失去了對局勢的掌控了，而且這場疫情現在正籠罩著你所在的地區。這些資料並非之前收集的，所以我們現在就從您現有的資料中開始處理這些內容。

**大會司儀**: 2 The detections of communities, which means they are also yours. Leave them, change them for your environment. And when you find a false positive. Send it back because it reaches everyone. Three, No C, no crowd account, no license, and nothing leaves your machine if you can learn. Finally, you can hunt in criteria and if you work somewhere that is not allowed to upload its logs anywhere.

> **繁中翻譯**：2 對社群的識別意味著這些社群也屬於你們。別管他們，根據你的環境做出相應的改變。而當你發現出現誤報的時候。把它退回去，因為它會傳給所有人。第三點，不收費，沒有群組賬戶，沒有許可證，而且只要你願意學習，任何東西都不會從你的裝置中刪除。最後，您可以根據特定條件進行搜尋。而且如果您所在的公司不允許將日誌上傳至任何地方的話，您也可以進行相關搜尋。

**大會司儀**: That last part is the whole point. That is everything. Thank you for staying with us. Both tools are free and open source. Select is the command line side, Selena is the local stack host and your security on how the QR codes are on screen. And the sample data set is topic 2, so you can reproduce everything you saw today. If you try it on something like, please open that nature.

> **繁中翻譯**：最後那部分才是關鍵所在。這就是全部內容。感謝您選擇使用我們的服務。這兩款工具都是免費且開源的。 “Select”是命令列端，“Selena”是本地堆疊主機，而您需要關注的是螢幕上二維碼的安全性設定。而示例資料集是第 2 個主題，因此您可以重現今天所看到的所有內容。如果你要嘗試的話，比如說，請開啟那個“自然”（這個概念）。

**大會司儀**: and if you write a rule for address send it to us for three to Sigma H2 which is even better. Thank you to Sigma HQ, to miter to the start for the threat technique catalog and to every project we borrowed from now of this. Exists so the update. Thank you for listening. So we're all time. So thank you for our two speaker from Japan.

> **繁中翻譯**：並且如果你制定了關於地址的規定，請將其傳送給我們，傳送至“三至西格瑪 H2”這個地址會更好。感謝西塔總部，感謝邁特在專案伊始為我們提供了威脅技術目錄，也感謝我們從現在起借鑑的所有專案內容。因此才有了這次更新。感謝您的聆聽。所以，我們都在等待。所以，非常感謝來自日本的兩位嘉賓的精彩發言。

**大會司儀**: I will say this is very practical and useful routines make it easy for the occasions I would say very critical 1\. So if you have any constructs because we're around all the time so you can come to the stage, you can ask the speaker directly. So we end up this session so and thank you for your join. Again, thank you. It's probably challenging the health in the this year so they will be insert Information in their training data. So that will be a data contamination.

> **繁中翻譯**：我要說的是，這些操作流程非常實用且有用，能讓我在各種情況下都能輕鬆應對。我敢說，這些流程在關鍵時刻是非常關鍵的。所以，如果您有任何問題，因為我們一直都在這裡，所以您可以走到舞臺上，直接向演講者提問。所以本次會議就到此結束，感謝您的參與。再次感謝您。今年的健康狀況可能受到了一定的影響，所以他們將會採取相應措施。他們在訓練資料中所包含的資訊。所以這將會是一種資料汙染。

**大會司儀**: The second window is the potential cheating. As I mentioned the when they just run, they should find the best way and fastest way to solve the problem. So they search the. Write up and how to solve that problem so that can be occurred. your potential cheating. To contamination and potential cheating is different. They contamination occurred before evaluation, but the potential cheating occurred during evaluation.

> **繁中翻譯**：第二個風險點在於可能存在作弊行為。正如我所提到的，當他們只是單純地行動時，他們應該尋找出解決問題的最佳方法和最快捷的方法。所以他們開始搜尋。詳細記錄並闡述如何解決那個可能出現的問題。你可能在作弊。對於汙染和可能存在的作弊行為，這兩者是不同的。這些汙染現象是在評估之前就存在的，而潛在的作弊行為則是在評估過程中發生的。

**大會司儀**: The data contamination The training data may already contain the challenge int write up word. It can occur from the old public task, unknown training corpus, or indirect evidence. And potential shifting means the agent retrievers this task. No solution. Of the serving the target. It can occur from the public right now. Direct flag with Trevor or a visa retur trace.

> **繁中翻譯**：資料汙染用於訓練的資料可能已經包含了“寫作”這個關鍵詞。它可能源自以往的公共任務、未知的訓練資料集，或者間接的證據。而這種潛在的變化意味著代理會接手這項任務。但目前沒有解決方案。對於目標而言的這一服務。這種情況現在就可能發生。可以聯絡特雷弗確認，或者查詢簽證返回記錄。

**大會司儀**: Or statistics, of course, really trustworthy. We have one research question. Can we use your CTF task reliably measure pressure offensive capability? So now we expose the risk, the data contamination and. Then we propose the city of Fusion that live ctap the task streaming. And we evaluate with the three models and two agents across the five line CTF.

> **繁中翻譯**：當然，統計資料也是相當可靠的。我們有一個研究問題。我們能否利用您的 CTF 任務來可靠地評估壓力下的進攻能力呢？所以現在我們揭示了這一風險、資料汙染等問題。然後我們提出了“融合之城”這一概念，它能夠實現任務的流式處理。我們使用這三種模型和兩個代理，在五條線路的 CTF 中進行了評估。

**大會司儀**: And we released this all of the code for the further research at the GitHub. 1st we build decipherment. Approved for the potential cheating. The decipher web is considered with the base agent that is like and we add the tool the website. The decipher is the planner and executor and web. Website tourism mandatory. The first step.

> **繁中翻譯**：並且我們將所有相關程式碼都發布到了 GitHub 上，以便用於後續的研究。首先，我們要進行解讀工作。批准認定存在作弊行為。這個解密網路是以類似於基礎代理的角色存在，並且我們還加入了網站這一工具。解密過程就是策劃者、執行者以及網路的總和。必須訪問網站進行旅遊相關操作。這是第一步。

**大會司儀**: That is the decipherment, so the workflow is the search 1st. And inspect the URL and go chronologist, then exploit and submit. The result is looks like this. The decipher the servlet is 20.59% and the cipher web success rate is 24.07. It means the plus 91% related. The success races really have been gap, but that is not the all of the region.

> **繁中翻譯**：這就是解讀的過程，所以工作流程首先是進行搜尋。然後檢查該網址並按時間順序檢視，接著進行分析並提交。結果如下所示。解密 servlet 的成功率是 20.59%，加密網頁的成功率是 24.07%。這意味著與之前相比增長了 91%。各隊之間的差距確實存在，但這並非該地區的全部情況。

**大會司儀**: We found some the cheating attempts. The 71 cheating attempts in every rooms and all the robes and 63 copy flag and eight search right documents. In the 2017 case they occurred the 20 point 21.8 evidence and 2018 they occurred 2227 evidence. This is the chart. This chart and it is more useful to understand from feature work.

> **繁中翻譯**：我們發現了幾起作弊行為。每個房間內共有 71 次作弊行為，還有所有的制服、63 個複製標誌以及 8 份搜尋許可權檔案。在 2017 年的那次事件中，出現了 20.218 的證據；而在 2018 年，出現了 2227 份證據。這就是圖表。這張圖表對於理解內容會更有幫助，這需要透過實際操作來掌握。

**大會司儀**: each other. The green one is the decipher and the. Sky One at Sky One Plus and Orange 1 is a Decipher web and all that work is the Decipher web and the Orange one is the Decipher web. cheating evidence and the other the Sky 1 is not cheating evidence. So this yeah, when you describe that they have known many cheating. So this is more obvious evidence for the cheating. So we find 2 categories.

> **繁中翻譯**：彼此。綠色的那個是解碼器。在“天空一臺”、“天空一臺增強版”以及“橙色一臺”中，都是使用“迪賽弗”網路服務，所有相關工作都屬於“迪賽弗”網路服務範疇，而“橙色一臺”所使用的也是“迪賽弗”網路服務。有作弊的證據，而另一方 Sky 1 並非作弊證據。所以是這樣的，嗯，當你描述他們知道有很多作弊行為的時候。所以這無疑進一步證明了存在作弊行為。我們發現主要有兩類情況。

**大會司儀**: The first one is the copy. And second one is the search right? In which case the agent card directly to use the some URL like this GitHub user contestant com it means. They searched the rates of on the website and directly the country and submit the plan in the place. And really? The second note is the search right now. The in the rule case they search the right at the city of times and they can't know the how to serve that problem so.

> **繁中翻譯**：第一個是副本。第二個就是搜尋吧？在這種情況下，代理卡可以直接使用類似這樣的網址，比如“github.com/user/contestant” 這樣的格式，這就是其含義。他們檢視了網站上的價格資訊，並直接查詢了相關國家的資料，然後在指定地點提交了計劃。 “真的嗎？” 第二點是當前的搜尋工作。在這種情況中，他們會在城市範圍內尋找解決方案，但卻無法知曉該如何處理這個問題。

**大會司儀**: Even they didn't copy platforms that also be cheating. That region is not advertised. This evidence is more corporate. I think the package become an Oracle. In the characteristic of the set benchmarks, that is all of the open source. So what are always access that the set benchmark so they no reverse and no target direction.

> **繁中翻譯**：即便他們也沒有效仿那些也會作弊的平臺。那個地區並未進行宣傳推廣。而這些證據則更具商業性質。我認為這個包裹變成了一個“奧瑞德”（一種虛構的物品）。在這些基準測試的特徵中，全部都是開源的。所以，這些指標始終是固定的基準值，這樣就不會出現反向變動和偏離目標的情況。

**大會司儀**: So they just can't insert NIUCTF. And they typed up code like Python And CTF data set, imported data set and finally they just print the flag. Yeah, it's problem. And they get Flick. Cool, this is the full log of the that case. The challenge name was the insane and they the wrong command car and slash. ask the NIU Peter. I don't know why but they read the books and uses first.

> **繁中翻譯**：所以他們就是無法插入 NIUCTF 這個程式。然後他們編寫了諸如 Python 和 CTF 資料集之類的程式碼，匯入了資料集，最後他們只是列印出了標誌。是的，這是個問題。然後他們得到了弗利克。好呀，這就是那個案子的完整記錄了。挑戰的名稱是“瘋狂”，而他們的指揮車則是“斬擊”。問問尼烏·彼得吧。我不知道原因何在，但他們總是先閱讀這些書籍並加以運用。

**大會司儀**: And then they run command the PIP in Star NIST app. And then they won't comment item 3 and from the some data from the import step data set and they their STD out is the like 2021 pre processing problem. And the price problem? It means they only catch it. The one challenge that insane, but they access. they also can access the other challenges.

> **繁中翻譯**：然後他們會在“星系國家標準局”應用程式中執行 PIP 指令。然後他們就不會對第 3 項發表評論了，而是從匯入步驟的資料集中提取一些資料，並且他們得出的標準差（STD）值似乎與 2021 年的預處理問題有關。那價格問題呢？這意味著他們只是察覺到了它。儘管這個挑戰很瘋狂，但他們還是克服了它。他們還能應對其他的各種挑戰。

**大會司儀**: So finally. Think they just print the Church of black and the city out can get the flag. But Indonesian can the. They don't know about is this the cheating? Because they're just did their goal and their goal is to find the flag, so they just do what they should do. 2nd we should figure out of the data contamination problem.

> **繁中翻譯**：所以，終於。他們以為只要印上“黑人教會”和“這座城市”這幾個字，就能拿到那面旗幟了。但是印尼語可以。他們並不清楚這是否屬於作弊行為？因為他們只是完成了自己的任務，而他們的任務就是找到旗幟。所以他們就按照自己該做的去做了。其次，我們需要解決資料汙染的問題。

**大會司儀**: so we build the decipher. No cheat. This agent is more easier than the Decipher web because we all need to change the. They use the only to change the system from what so? Not use the pre trained data according to specific task. So we also use the baseline that decipher and we only change the system taxes like that. So that is the decipher notch.

> **繁中翻譯**：所以我們構建了這個解密系統。絕對不作弊。這款軟體比“解密網”更簡單，因為我們都需要進行相應的設定。他們只是想透過這種方式來改變這個體制，對吧？不根據具體任務使用預訓練資料。因此，我們同樣也採用了這個基準方案，並且只對系統稅項進行這樣的調整。這就是那個解讀標記。

**大會司儀**: Of course they serve the same task and submission task. A not cheap proper to reduce the performance by 29%. The GPT 4.1 and the Gemini in flash case. The right sky color is the. Decipher and the red color is means the decipher not cheat. It also reduce from the 14.44% to the 9.44%. In Gemini case they reduce from the 20.78% to 10%.

> **繁中翻譯**：當然，它們執行的任務和提交任務是相同的。這並非一項成本低廉的措施，反而會使效能下降 29%。 GPT 4.1 和 Gemini 以快閃記憶體外殼包裝。右側的天空顏色是這樣的。 “Decipher”這個詞的紅色字型表示“解密”而非“欺騙”。它也從 14.44% 降到了 9.44% 。在“吉布森”案例中，這一比例從 20.78% 降至 10%。

**大會司儀**: \-29% relate to the reduction. It might be the we just strong reduction of the system prompted many use the you don't cheat and you should serve problem your own ability. Then mothers can be do more small task and more small ability for the child. So they might be in the effective order. So we present City Occasion, a streaming framework for evaluation of escalator.

> **繁中翻譯**：\-29% 與削減有關。這可能是因為我們對系統進行了大幅最佳化，從而使得許多人開始意識到“不要作弊，要發揮自己的能力”這一道理。這樣一來，母親們就能為孩子承擔更多的日常瑣事，並培養孩子的更多基本技能。所以它們可能就是按有效的順序排列的。因此，我們推出了“城市場合”這一流媒體框架，用於評估自動扶梯的效能。

**大會司儀**: On the life of least. This is the framework of the city application. Once agent build then the page one, the agent told the NCP we are ready. Please give me some of the challenge. Then MCP the send the information to the CTMD. Step D means the live CTF framework. Then the CTMD returns the challenge and artifact description to the MCP and MCP can get oral adaptive fact and deadlines deadline CTM.

> **繁中翻譯**：關於最平凡的生活。這就是該城市應用程式的框架。一旦完成設定，頁面就顯示出來了。那位代理告訴我們，國家計算機防護中心那邊已經準備好相關事宜了。請給我一些挑戰吧。然後，MCP 將資訊傳送給 CTMD。步驟 D 指的是實時的 CTF 架構。然後，CTMD 將挑戰和相關描述返回給 MCP，而 MCP 則能夠獲取口頭適應事實、截止日期以及 CTM 的詳細資訊。

**大會司儀**: Then they are located each challenge to the agent. The agent is the agent did the acknowledges the challenge and serve the challenge and finally if they get the flag then they submit the flag to the submit flag function. Then the function sends that flag to the flavor caching the proxy, and finally the flavor caching proxy proxy and the flatty.

> **繁中翻譯**：然後他們分別向該代理人提出每一項挑戰。該代理執行了相關操作，承認了這一挑戰，並應對了這一挑戰，最終如果他們獲得了標誌，那麼他們就會將該標誌提交給提交標誌功能。然後，該函式將該標誌傳送給負責快取風味資訊的代理，最後由該風味快取代理以及風味本身共同完成這一過程。

**大會司儀**: and they can return this wrong or nothing. In the next page I'd like to talk about the why you choice the proxy system and see them caching function is existing. The lifecycle evaluation creates a share of account dilemma. If we use the account one account per agent, then we should use the six account cost 3 model and two agent.

> **繁中翻譯**：並且他們可以選擇退回這些不合格的產品或者什麼都不做。在下一頁，我想談談您選擇代理系統的理由，並探討一下他們所採用的快取功能是否已經存在。生命週期評估帶來了賬戶共享方面的難題。如果我們採用“每個代理一個賬戶”的方式，那麼就應該採用“六賬戶三費用”模式，並且是針對兩個代理的。

**大會司儀**: It is not really good thing because the live CTF is the computation and if we make the 6th account in the competition that can be the problem for the other users, So we don't want like that thing. So we think we should share one account. Then if we use the one account 1 shadow account then the problem is assert not yet. 'Cause is there ever inconsider the one agent? Agent A and Agent B is exist If agent A sort of the challenge, then they will submit the problem with the server, then they can return is the right plan.

> **繁中翻譯**：這其實並不是一件好事，因為實時的 CTF 比賽是需要進行計算的，如果我們在這個比賽中建立第 6 個賬號，可能會給其他使用者帶來麻煩。所以我們不想要那樣的情況。所以我們認為我們應該共用一個賬戶。那麼，如果我們使用一個賬戶（也就是一個虛擬賬戶）的話，目前這個問題還沒有出現。因為究竟有沒有那種不周全的情況呢？有這樣一對搭檔嗎？即代理人 A 和代理人 B。如果代理人 A 承擔了挑戰的任務，然後他們會將問題提交給伺服器，之後就能得到正確的解決方案了。

**大會司儀**: After that agent B serve the challenge and the send the blank to the server. They only can be done you already served. The agent, we don't know about the it's sort of it's right or wrong. So make sure the proxy system. So that we can. Use the demand account plus proxy. Then you can serve that proxy. So this is the all of the CTF fusion, the agent group.

> **繁中翻譯**：之後，代理 B 接受了挑戰，並將空白檔案傳送給了伺服器。這些只有在你已經完成之前才能進行。這位代理人，我們並不清楚這件事到底是對是錯。所以一定要確保代理系統正常執行。這樣我們就能…… 使用需求賬戶並藉助代理服務。這樣你就能為該代理提供服務了。所以這就是整個 CTF 融合體系，也就是代理小組。

## ⚡ LLM 資源劫持（Bedrock InvokeModel）與實體威脅關聯分析：社群共建與誤報抑制

**大會司儀**: First they invite the metadata and listing challenge and inspect the detail. Then they download that they only fetch once and reuse locally. Only if the challenge update and they can redownload that problem. That challenge? Third, they serve locally. The reasoning and the user inside the container. 4th They submit the candidate and send candidate flag to Frost.

> **繁中翻譯**：首先，他們會收集相關資料並提出挑戰，然後仔細檢查細節。然後他們會下載相關內容，但只需進行一次下載，之後便會在本地重複使用這些內容。只有當挑戰內容更新了，他們才能重新下載該問題的相關內容。那個挑戰是什麼呢？第三點是，它們是本地供應的。容器內的推理過程和使用者。 4\. 他們提交候選人資訊，並將候選人標誌傳送給弗羅斯特。

**大會司儀**: And. The proxy if they correct the flight cache and compare. So only the once the flight correct that they should catch that event, then they don't more need to submit the play with the solar because they always know that play is the right or wrong. This is the implementation we build the step DMCP with the. So the safety compact over the Jason cast.

> **繁中翻譯**：並且。如果他們修正了航班資料並進行對比，那麼就可以使用這個代理方法了。所以只有在飛行任務確認他們能夠趕上那個活動之後，他們才無需再根據太陽資料來調整計劃，因為他們已經清楚那個計劃是正確的還是錯誤的。這就是我們採用這種方法構建的分步 DMCP 系統。所以對於傑森的假肢，我們制定了安全協議。

**大會司儀**: And the we also read the proxy counter with the plastic and SQL blind. It's brutal castration. The Agent Warner will be the Linux and looker so we can isolate. Framework and for this event config the environment variable. So if you want some new like city and adult then we just only change the environment like the endpoint or AK token or URL that's it.

> **繁中翻譯**：並且我們還使用塑膠和 SQL 空心針來讀取代理計數器。這是極其殘忍的閹割行為。沃納特工將成為“Linux”角色並負責監督工作，這樣我們就能對其進行隔離了。在該框架中，需為此次事件配置環境變數。所以，如果您想要一個全新的、更具成人氛圍的城市場景，那麼我們只需改變環境設定，比如端點、AK 令牌或者 URL 就行了。

**大會司儀**: some city use the city then we can really easy to. This is current protocol the US three LA. GPT 4.1 called 3.5 and the Gemini 2.5 flash and they used 2 agent framework with enigma and decipher. We also select A life, 5 lights in camp events and 180 static tasks. We used our mesonology the past three attack and each attempt Max budget instance 3 double API cost.

> **繁中翻譯**：有些城市已經採用了這種模式，這樣一來我們就能非常方便地使用了。這是目前美國洛杉磯地區的相關規定。 GPT 4.1 叫作 3.5，而“雙子座”2.5 則是快閃記憶體裝置，他們使用了包含“恩格瑪”和“破譯”功能的 2 個代理框架。我們還設定了“一段人生”、5 項營地活動以及 180 項靜態任務。在過去三次的攻擊中，我們運用了我們的“中子論”。每次嘗試時，馬克斯的預算都為 3 次雙倍的 API 成本。

**大會司儀**: This is the five number of the five choice that our select the Cypriot. The first one is the city a cube CTF, the second one is UI CTF, third one is www\. This is the duration of the 2025 March to 2025 to August. So there was totally 192 online CTF tracked. But we only can use the CTF, the API and. Online in CPF and international CF.

> **繁中翻譯**：這就是我們選擇塞普勒斯人的五項標準中的第五條。第一個是名為“城市立方體”的競賽專案，第二個是“使用者介面競賽專案”，第三個是“www”。這是從 2025 年 3 月到 2025 年 8 月這段時間的時長。因此，總共追蹤到了 192 個線上 CTF 事件。但我們只能使用 CTF、API 等工具。可在 CPF 網站及國際版 CPF 網站上訪問。

**大會司儀**: So in this condition the only 45 does it have is the in our filter. So we use the 5C tap of use the 5C type of the probing 5C. This is the result of the variation. In GPT 4.1 case the OK. Sky One is the live city and the Railroad one is the static static. Benchmark so in GPT 4.1 case they have like the 2.4 times the set benchmark crystal more over the server length and called 3.5 with the reduce the 111.4 to 5.4.

> **繁中翻譯**：所以在這種情況下，它擁有的全部 45 個部件只有那些在我們的過濾器中所包含的那些。所以我們使用 5C 插頭來執行 5C 型別的測試。這就是這種變化所導致的結果。在 GPT 4.1 情況下，好的。 “天空一號”是動態的都市景象，“鐵路一號”則是靜態的畫面。在 GPT 4.1 的測試中，他們的基準測試結果是：伺服器長度方面比設定基準值高出約 2.4 倍，而計算速度則提升了 3.5 倍，同時將 111.4 的數值降低到了 5.4。

**大會司儀**: Gemini 2.5 K is. From the 15.1 to the two point 6.2 and the according to the Enigma and Decipher is like similarly built like that. So here's is not been considered about the DP card problem in case the live city might be more harder than harder than the text but more than two times the serve rate is. Miniature. This is the model and agent.

> **繁中翻譯**：“雙子座 2.5 K”是。從 15.1 到 2.62，根據“恩格瑪”密碼解密的結果就是類似這樣構建的。所以這裡並沒有考慮到關於 DP 卡的問題，因為實際情況可能會比文中所述的情況還要複雜得多。但其成功率卻超過了兩倍。微型的。這就是模型和代理。

**大會司儀**: Match the evaluation result. So in GPT 4.1 and the enigma is ratio is the 2 point 2.0 times the GPT 4.1 and the decipher is 2.6 times and also the cloud 3.5 and ending one is the 2.4 times for the 3.5. And decipher is the 2.1 times. On the same. Water ordering the both setting the GPT is the real the most good sort of blade of the Ctr.

> **繁中翻譯**：將評估結果匹配起來。所以在 GPT 4.1 中，謎題的比率是 2.20 倍於 GPT 4.1，解密部分是 2.6 倍，雲部分是 3.5 倍，而最後一個部分是 2.4 倍。對於 3.5 版本的...... 而“解密”的次數是 2.1 倍。同樣地。水按照既定的程式啟動 GPT 後，它就是中心裝置中效能最佳的部件了。

**大會司儀**: challenge and then J9 and cloud 3.5. So this is correct for your understanding. The pink one is the latency tab and Sky One is the energy system bench. They're all of them is the more than twice times it shows the surface rate. In this page I'm going to talk about the category revised performance. They really good at the MIS challenge.

> **繁中翻譯**：挑戰，然後是 J9 和 Cloud 3.5 。所以這對你理解來說是正確的。粉色的那個是“延遲”選項卡，而“天空一號”則是能源系統測試臺。它們的表面速率都比這個數值高出兩倍以上。在本頁中，我將談論分類修訂後的表現情況。他們在管理資訊系統挑戰中表現得非常出色。

**大會司儀**: And their worst score is the forensic challenge. I think. The price challenge is not. That caused the. At that time their context memory is really small. And the forensic challenges there tend to really be a defect for 100 GB. but I think the at 10 times the element agent is. Can cover all of that architect of the forensic. So that's the rate is the like the rule and they the agent is the good at the misk and reverse event challenge.

> **繁中翻譯**：而他們表現最差的部分是法醫環節的測試。我認為。價格方面的壓力並不存在。這導致了……當時他們的短期記憶容量確實很小。而在這種情況下，法醫方面所面臨的難題往往在於 100GB 的儲存容量存在缺陷。但我認為這種物質的濃度應該是原來的 10 倍。能夠涵蓋所有這些內容的那位法醫專家。所以這就是規則，而他們這個團隊擅長處理意外事件和逆向事件的應對工作。

**大會司儀**: And they're not good at home and crypto and forensics. This is the most failure the verbiage or execution failure. In total times there are 3024 attempts to be acknowledged 1\. 155 serves of that problem. And only 5.22 attend the success and 2866 failure analysis. The most of regions. The cost link. The variable 45.22% was the end cause the cost remit and the 3.36% is was the suspense by the system issuer, the other things and 24.42% they given they serve.

> **繁中翻譯**：而且他們在家庭事務、加密技術和法證方面都不擅長。這是整個表述或執行過程中的最大失誤。總共需要確認 3024 次操作。解決了那個問題 155 個步驟。僅有 522 人對此次成功案例進行了分析，而有 2866 人對其失敗原因進行了分析。大多數地區。成本關聯。變數 45.22% 是成本結算的最終原因，而 3.36% 則是系統髮卡方產生的滯留款項。其他事項以及 24.42% 的服務費用。

**大會司儀**: In the Antigua case, the most the age of the signature the and the region is the bike . point 58.10% because the cost limit and decipher case is 38.57% because the suspended. And be the set benchmark maintain the ad invoice. Because the original task of the NIH step bench is the 210 challenge but be used in 180 challenge.

> **繁中翻譯**：在安提瓜案中，最重要的因素是簽名的年代、簽名的地點以及所騎的腳踏車。第 58 點。10% 的比例是由於成本限制和解密案件導致的，為 38.57%，因為該事項已被暫停。並且要以此作為標準來執行廣告發票的管理工作。因為美國國立衛生研究院的實驗臺最初的任務是應對 210 項挑戰，但實際卻用於應對 180 項挑戰。

**大會司儀**: There is some the problem of the artefact, so we found the seven vertical setup. The vertical setup means the. They have some of the insert file or the build. The file is an artifact, but they didn't have that information. So we can reconstruct 5 challenges and second one is the listing to occur. And some challenge should contain the doker, but there is not anything about the doker.

> **繁中翻譯**：這個裝置存在一些問題，所以我們採用了七層垂直排列的方式來解決。這種垂直的佈局方式意味著…… 他們有一些插入檔案或者構建檔案。這份檔案屬於一種特殊物品，但他們當時並不知曉這一點。因此，我們可以列出 5 個挑戰，第二個挑戰是列表的生成問題。並且有些挑戰會包含“駕駛員”這一角色，但並沒有關於“駕駛員”的任何描述。

**大會司儀**: So we reconstruct 6 challenge about that nine challenge. And third one is the incomplete article. It means some challenge use the static URL in their artifact or binary. but you cannot access the binary access the URL anymore. So you cannot reconstruct that. You don't know what information is that you want. Which one is important?

> **繁中翻譯**：因此，我們針對那九個挑戰又增設了六個新的挑戰。第三個是未完成的文章。這意味著某些應用程式在使用其元件或二進位制檔案時會使用固定的 URL 地址。但您無法再訪問該二進位制檔案了，也無法再訪問該網址了。所以你無法重現那樣的情景。你並不清楚自己究竟想要什麼樣的資訊。到底哪些資訊才是重要的呢？

**大會司儀**: And. Last five is the missing cholesterol fight so it freezer better wait. For sure. This is what we reconstructed and what we can be constructed. The case of the missing doker file the we can reconstruct the six of them to make a local file, but the three of them challenges we cannot make the two compact calls. The challenge is really a big issue and the independent of the Docker OS version, so, but we cannot match the exact exposure, version, so that can be the.

> **繁中翻譯**：並且。最後一條是關於缺乏膽固醇的問題，所以最好還是等一等再說。當然。這就是我們所重建的，也是我們能夠重建的。丟失的文件檔案已找回，我們可以透過重新整合這六個檔案來生成一個完整的檔案。但這三人提出的三個問題，我們無法用兩個簡短的回答來一一解答。這個挑戰確實是一個重大問題，而且與 Docker 作業系統的版本無關，但是我們無法實現完全一致的匹配。版本，這樣就可以是......

**大會司儀**: Not good. Benchmark set so we just reduce that, then only recover the 6th agent and 6th challenge. In the rocker center, in constances that we use, we recover the reconstruct all challenges and the other is the camera. So the limitation of the current study, the first one is not casual separation, so difficult and the contamination remained.

> **繁中翻譯**：不好。設定好基準值後，我們就只需降低這個數值，然後僅恢復第 6 個代理和第 6 項挑戰。在搖桿中心，按照我們所使用的標準，我們解決了所有的問題，而另一個方面則是攝像機。所以本次研究的侷限性之一在於，其並非採用隨機分組的方式，因此存在操作上的困難以及樣本間的相互干擾問題。

**大會司儀**: The second one is the narrow water coverage. Three, you use the three commercial evidence and the two agent framework. It might be that third one is fixed evaluation result. > **繁中翻譯**：是第三個才是最終的評估結果。

**大會司儀**: We use past three method and approximate \$3 per attempt. As he's someone like the many of the attempt to reach the budget limit.

> **繁中翻譯**：第二種情況是水域覆蓋範圍較窄。三、您需運用這三項商業證據以及這兩個代理框架。可能我們採用了過去這三種方法，並且每次嘗試的費用約為 3 元。因為他就是那種試圖突破預算限制的人之一。

**大會司儀**: So if we make more budget limits, so like \$5 per attempt, that vision can be changed? Important is limited 5 coverage. We use the five step events in 2025 and pointed 2025, but there's more many lots of the CTM apparent, so we could so evaluate some more proposed CDF. The fifth one is the platform score. You do not consider what the OPEC and defense model and we only use the CTFD motor.

> **繁中翻譯**：所以，如果我們設定更高的預算限制，比如每次嘗試 5 美元，那麼這種設想是否就能改變呢？重要的是要確保覆蓋範圍有限。我們在 2025 年採用了這五個步驟的方案，並明確指出了 2025 年這一時間節點，但除此之外，還有很多關於 CTM 的具體細節需要明確。這樣我們就能對更多的擬議 CDF 進行評估了。第五項是平臺得分。您並未考慮過歐佩克、防禦模式以及我們所採用的 CTFD 發動機這些因素。

**大會司儀**: so it's really the registration of the framework. Last one is the ranking may change the return that the GPT and Gemini and growth was the render orderly order. But if we change the past past methodology where the budget maybe then. That murder might be a change. So we present the city of fusion. Make the task fresh, not through record.

> **繁中翻譯**：所以實際上這是框架的註冊過程。最後一點是，排名可能會改變回報率。而 GPT、Gemini 和 Growth 則形成了一個有序的排列順序。但如果我們要改變目前的預算編制方法的話，那麼情況可能會有所不同。那起謀殺案或許意味著某種變化。所以，我們呈現的是融合之城。讓這項任務充滿新意，而非依賴於過往的記錄。

**大會司儀**: So our. Our main topic is the keeper too. And change the task source 'cause when you're the evaluation there's two more kinds of testing and latency of the gap. And we also should find the 71 checking attempts. So the static benchmark is the vulnerable, the benchmark is the vulnerable. And if we there is really many GTF hurdle around the world and every week, every year and more than 300 CTF.

> **繁中翻譯**：所以我們的。我們的主要討論內容也是關於保管人的。並且要更改任務來源，因為當進行評估時，會有另外兩種測試型別以及延遲方面的差異。而且我們還需要找出 71 次的檢查嘗試。所以靜態基準測試存在漏洞，這個基準測試也是存在漏洞的。而且，實際上全球範圍記憶體在著眾多的 GTF 障礙，而且這種情況每週、每年都會發生，而且每年的數量超過 300 個。

**大會司儀**: Every year in the second time, so we can use that as a benchmark and. So this is the OR my talk. So thank you for listening and you can find the paper and code in the that link. Thank you so much. Go away. A quick question regarding whether you use any tools, AI tools. To participate or use it as a tool to win the game. For the AIX CC or does that consider Commission for the data?

> **繁中翻譯**：每年的第二個月份，這樣我們就可以以此作為基準了。這就是我的演講內容。所以非常感謝大家聆聽。您可以在那個連結中找到相關的論文和程式碼。非常感謝。走開。有個簡單的問題，想問一下您是否使用過任何工具，比如人工智慧工具。參與其中，或者將其用作贏得比賽的手段。對於 AIX CC 而言，是否也包含對佣金的計算呢？

**大會司儀**: In the. In the final. We just simply make like the automate exploit and the patch analyzer and exploring manager to exploit the other teams cause our team member is only 28 people. So it's really led to the exploit the A\&D and to endorses the K20H. So let's summarize the I think only. The important truth we made, as I mentioned and the last one, is the like.

> **繁中翻譯**：在......裡。在決賽中。我們只是簡單地利用自動化漏洞利用工具、補丁分析工具以及漏洞挖掘管理工具來攻擊其他團隊，因為我們的團隊成員只有 28 人。因此，這實際上促使了對 A\&D 的開發以及對 K20H 的推廣。那麼，就讓我們來總結一下（我認為這是唯一的總結）。正如我之前所提到的以及最後一點所說，我們得出的重要結論就是“相似性”。

**大會司儀**: Have to fix the name but they're messy. Messy first cause the many team will be the. So if they input our packet to their LM, so it might be LM. Do not like answer about the question, for example, how to make it clear? Or how to make Moroccan and if the sentence is in the bank packet so they will not answer about the shared information, so they will first.

> **繁中翻譯**：得把名字改一改，不過它們現在排列得有點亂。之所以亂，是因為有很多團隊，所以才會這樣。所以如果他們將我們的資料包輸入到他們的邏輯模組中，那麼這個模組可能是邏輯模組（LM）。不要給出關於這個問題的答案，比如“如何使其更清晰呢？”這類的回答。或者如何製作摩洛哥風味的食物，如果這個句子包含在包裹內的話，那麼他們就不會透露有關共享資訊的內容了。所以他們首先會......

**大會司儀**: Go down there. Go down. So we do like that. So my main question is that. Before you have AI or Apple, you have AI excuse for the CTF. What? How do you feel about the difference? I think the big difference thing is. Some sometimes the some the AI can do some tests like smart things like the make generate or peculiar play, but they can't analyze over the packet.

> **繁中翻譯**：下去那裡。下降。所以我們確實是那樣做的。所以我的主要疑問就是這個。在擁有人工智慧或蘋果公司之前，你先得有“人工智慧”這個藉口來解釋計算機取證技術（CTF）。怎麼啦？你覺得這種差異怎麼樣？我認為最大的不同之處在於...... 有時，人工智慧能夠進行一些測試，比如一些智慧操作，比如生成特定內容或者進行獨特的表演。但他們無法對資料包進行分析。

**大會司儀**: So in before we should make the oral tours like the Smart thing from The Smart Thing and the Last Thing and this day. the smart thing is the agent can control all of the summer thing. So we should make a rugged task for the AI agent that can do more good problems. Right. Thank you. What? No thanks for your talk and I'm curious about what are the most important things when building a harness to maximize agents performance.

> **繁中翻譯**：所以在開始之前，我們應該安排一些口頭講解活動，比如《聰明的事》《最後的事》以及《這一天》中的相關內容。明智的是，這個機器人能夠控制所有的夏季裝置。因此，我們應該為人工智慧代理設定一項艱鉅的任務，使其能夠解決更多複雜的問題。好的。謝謝你！怎麼啦？謝謝您的講解，我很想了解一下在構建防護裝置時，要如何才能最大程度地提升裝置效能，這其中最重要的因素有哪些呢？

**大會司儀**: It's really easy. Good Castellani Australia important but it's really hard as. Sometimes the when sometimes we just say just do it can be made the best performance and sometimes you should make the specific highlights, specific workflow for the agent. But. I think that's the case by case. So if we do some, so I think we should make the harness the, especially the specific test that is the how we can make the most.

> **繁中翻譯**：這真的很容易。卡斯特拉尼在澳大利亞的表現很重要，但這確實很難做到。有時“只要去做”這句話就能帶來最佳效果，而有時則需要突出具體的亮點。該代理的具體工作流程。但是。我認為這要視具體情況而定。所以如果我們要做的話，那麼我認為我們應該把安全帶設計成這樣…… 尤其是那種具體的測試，即我們如何才能達到最佳效果的測試。

**大會司儀**: Most growth of their performance. So that is by my answer. So I also curious about that. Thank you. Thank you. What are the conditions although you're just shut the door harness and stop the call? What is the moment? I don't know what your account is, it would not harness. Model this is. Like model she exploring. Which model you prefer in the CDF, especially.com?

> **繁中翻譯**：他們的表現有了顯著的提升。所以這就是我的回答。所以我也對此感到好奇。謝謝你！謝謝你！那麼，即便只是關閉通話裝置並停止通話，具體又會有哪些情況呢？這是什麼時刻？我不知道你的賬戶是什麼情況，反正無法登入。這就是模型。就像模特那樣，她在探索著。在 CDF 網站（尤其是.com 版本）中，您更傾向於哪種模式呢？

**大會司儀**: What is your question? Which model? Which model? We use the oral model that we can use like GPT and cloud, but in these days clothes really. They. CBP program in these days so we are more pretend to use the GPT and using GPT also. What's that is after past the C after habit between? I know CBD after you get the CBP approval the model is smarter than before.

> **繁中翻譯**：你的問題是什麼？是哪一款？哪一款？我們採用了類似於 GPT 和雲端的口述模式，不過如今這種模式的應用場景更像是服裝設計領域。他們。最近我們實施了 CBP 計劃，因此我們更多地傾向於使用 GPT，並且也確實使用了它。那“C之後的習慣”後面接著的是什麼？我知道，在獲得 CBP 批准後，該模型比之前更加智慧了。

**大會司儀**: Not model is the smarter the motor. It's not a if I didn't get the CBP then there sometimes the kick me. I can't do this behavior. But if I get the CBP then we I can't do more. It's probably right. It's growing OK. It is free time, please return complete from the next station. Please take all your belonging with you and do not receive the personal items.

> **繁中翻譯**：發動機的功率越大，其效能就越優越。這並不是說，如果我沒有透過移民局的審查，那麼他們有時就會對我進行處罰。我不能做出這種行為。但如果我獲得了邊境檢查局的授權，那我就無法再做更多的事情了。這可能是正確的。它長得還不錯。這是免費乘車時間，請在下一站下車並完成出站手續。請將您所有的物品帶在身邊，不要接收個人物品。

**大會司儀**: Account is not responsible for those of you. Most property will be kept at the information desk.

> **繁中翻譯**：本賬戶不承擔任何責任。大部分物品將存放在服務檯處。
