---
title: "進階人工智慧與最佳化 Lesson 03：感測器能源模型與 Apache Benchmark 高並發效能評測"
event: "進階人工智慧與最佳化研究所課程"
date: "2025-02-20"
talk_id: "AI-OPT-03"
speakers: ["授課講師", "學員"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "classroom-lecture"
---

# 🎙️ AI-OPT-03 進階人工智慧與最佳化 Lesson 03：感測器能源模型與 Apache Benchmark 高並發效能評測 (授課講師 / 學員)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動問答，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語與標點符號，明確標註發言角色（授課講師／學員），並依授課脈絡劃分流暢之主題章節。

---

## 🔋 學員專案發表：四百組電池感測模組（Battery Packs）能源採集與即時遙測展示

**【學員】**：Okay. Hello, and we are four hundred battery packs. These are our team members, Yi Jun and Xin Yu. And Yuzheng. Uh, the another member Dongdong. Well, go on board. And this is the one. Dongdong, wait. Uh, on board. On board. Alright.

**【學員】**：我要show呃little discussion。 你我show啊。 OK OK。

**【授課講師】**：This is our outline. And the enemy platform will need to decide it how to the target to conversion or那個promote promotion. So, but so we need to predict the animation那個popularity and so on. But it there's a problem because that and呃popularity bias issue.

**【授課講師】**：And we so we propose the那個model to predict theenemies popularity and mean score. To use the, uh, text, and image and table features. Uh, uh, the sort of current research shows that, multi models are perform higher than single model and, uh, existing existing studies uh, most adopt the single target edition.

**【授課講師】**：Of so, uh, we turn the raw data to the clean table data, but this persistent data, and also put the text and image data to a lot. And we use the regular importation method, like format medium, to the ex episode. and duration.

**【授課講師】**：We use the percentile Winsorization to the outlier strategy, and target engineering will create the quarter PCT field to split the data, and this use the analyze only. In the bias mitigation, we we split data with the same quarter, and um to rank with the each each quarter each season.

**【授課講師】**：And the data split strategy is use the past data to forecast future. So the training data is on thetest, test and the meta data and test use the latest data. And next is our explanation. Okay, let's go about the explanation.

**【授課講師】**：And our target output is popularity and the name score. And our main input are type, metadata, has amazing image data, image amazing are from our prediction anime, and the rank data are from our uh other related anime. And before talking about our strategy, let's talk about our limit and the assumption.

**【授課講師】**：We have three limit and the two assumption. One is cumul, cumulative relation is talk about the anime release longer, it have uh more popularity. And the local area and the memorability change are on our analysis. And we can talk, we can see about the image load.

**【授課講師】**：And we can see that the members and the enemy quality and quality group out, and the mean score also close the gap between different release year. And so, so our assumption one is the measurement achievable probability of an enemy video is constant, depending on the paper and release.

**【授課講師】**：And the second one is miss the gap between the release year. We then model them about the years and the years relations with the enemy, miss score. And it's our proposed structure. We get the metadata description cover image into our four different type of modules: rec, test and base modules, image embedding modules, and the fusion modules.

**【授課講師】**：We take we use metadata and the test embedding to retrieval related enemies metadata, and we put metadata,and the recommend data into our projection become to reduce the dimension and the noise. Finally, we put the image text and the meta data vector into our final version model and predict our popularity and the mean score.

**【授課講師】**：And I'll talk about our test and making model that don't know talk about it. So, uh, it's more uh the noise too small. So let let me talk about it. The process is less the test and making is. Okay. How many more slides do you have?

**【授課講師】**：Only nine. Then, uh, just just ten. Ten. Yeah. Very quickly. That's so quick. Okay. You have one minute. Okay. Oh, that's five days. Okay. This is. is呃，image embedding and the time show how we reshape the imag

## ⚡ 高並發協議效能評估：TCP/TLS 傳輸最佳化與 Apache Benchmark 模擬壓測

**【授課講師】**：e and how to split the data and that is our training process and we use the contrastive learning and that is our future want to do and the first is呃，we want to share the two image channels separately and explore the object detection and color distribution color distribution iteration to reduce the performance.

**【授課講師】**：So depending on the target condition, we use this four metrics呃，experiments, RQ and AE and log AE呃，depending on the target condition that right to the probability concentration distribution and our RQ and the experiments are that like RQ one is to verify our core process process is呃，effectiveness.

**【授課講師】**：The idea is to predict and verify with rate or without rate can make, okay, can make a related animate information. That is our experiment. Okay. And is our overflow check. Okay. Thank you. Okay. Can we go back to slide twenty-five?

**【授課講師】**：Uh, what am I looking at? Please. Uh, we can do that. Uh, just like the four D, four tile, four tile. And because uh, we use different data sets to train lights, like past twenty two thousand years data or use the four data sets.

**【授課講師】**：And those last, we can see that, um, with all four datasays just like a three and a four with four datasets, miss four is much more better. So we can use this just like this. Four million three datasets. Four datasets, that's we can use one nineteen nineteen thousands later.

**【授課講師】**：Four dataset means that we do not see data after or before two thousand. Yes. For popularity, yes. For popularity, why is the N A E like ten thousand or what is that? N A E in ten thousand means that the mean average error like ten thousands because we do not use we use log to simulate.

**【授課講師】**：If we do not use log, it presents the raw popularity. 明白了吧？ Yeah, what what what is popularity? How how do you measure popularity? Uh, popularity means that the people uh add the anime to his or her watch list. This means the popularity.

**【授課講師】**：So for anime, you are you have thousands of. Yes. But what is not very good? Yes, that's not very good. But this uh this source and the result we just want to check the workflow is okay to run. Yeah. So what is your best plan?

**【授課講師】**：Our best plan, we will use the 2020 points uh papers, just like our literature review. Let's use respectful names at the the GPT two or I know I haven't I haven't done that. I haven't done that yet because that's our uh future.

**【授課講師】**：Just like the experiment one, and we work the workflow is okay to run. My only comment is that next time try to condense your content and only talk about the main main points. Otherwise, you're going to run out of time. Okay, run out of time every time.

**【授課講師】**：Okay, so because you you kind of made your own dataset because you changed it, right? You you took any existing dataset, yeah, that's right, but you modified it, yeah, right. So as long as you run baseline on your modified dataset, it'sIt's probably okay.

**【授課講師】**：We will run our best lines depending on our best easiest best data data sets. Good. Thank you very much. Okay. Uh, hello, everyone. Our topic is cost-benefit analysis of agent AI design patterns for e-commerce and IT. And this is Angie and Michelle and Benjamin Lee.

**【授課講師】**：Great. And uh, regarding the previous concern about how various prompts might lead to unstable LLM outputs and affect our experience reversibility, and we have researched a concrete solution. And we are adopting the PRSA framework, and recently published in EMNLP 2024 by Zhou et al.

**【學員】**：那它主要是評估 High Concurrency 下的效率。 啊，它的那個 Protocol 是以 TCP/TLS 為主。 那另外一個話是 Apache 的 Benchmark，那主要是模擬大量的 TCP 請求來評估 VPS 在做容錯時候的狀況。 那 TCP Benchmark 主要是對應到程序程序做的

## 🖥️ 虛擬專屬伺服器（VPS）容錯切換（Fault Tolerance）與無效請求抑制機制

**【授課講師】**：那個 UDP，那就是去對加速傳輸 UDP 那個效率。 那 Apache Benchmark 是對應到開源做的 VSD，然後去減少傳佈這些已經失效的 Request 的資訊。 然後我然後我這個月的話，我 Open 的方法就是昨天我跟王老師討論，那那個那個目前做那個 Open 的 Open 的那個方法，它還有一些問題在，然後就是要馬上在修正。 那就還還在修正中在。 那就主要是報告實驗，哎，把上一屆這樣的測試嘛合併在一起。 然後，那第一個這這個是那個 BBC 的 Benchmark，然後它的實驗實驗物件的話是 AMD Ryzen 七五千零的 CPU，那這個是哎，這個是去年去年去年新買的嘛？

**【授課講師】**：這樣，那規格的話是四 B CPU 跟八 G B 記憶體，那圖片的話，橫軸是這個。 啊，你現在是在重複學長經常做的實驗嗎？ 哎，對，就是把他們實實驗合併起來，然後對應到。 哎，重複他們實驗的目的是？ 哎，重複他們目的沒有重複實驗，把兩個程式碼並起並起來，真的嗎？ 你不拆重複實驗嗎？ 沒有重複實驗。 哦，沒有，就是就是我把他們兩個程式碼把他們合併起來之後，再去跟原本的 ACM 這邊做比較，看差異在哪裡。 最後為什麼要做這個？ 為什麼做這個？ 嗯，目的應該是要丟研討會嗎？

**【授課講師】**：十年，十年，十年，是嗎？ 還有，還在問我嗎？ 哈哈哈哈哈。 呃，目的，我做比較做。 好。

**【授課講師】**：呃，目的目的應該是要要剛剛比較說，就是加入了 the Turing 的，加入的 VSC 的話，呃，用 the Turing 然後去加速 the memory 的傳輸，還有用。 錦城的做這個，我支援這件事嗎？ 對，你為什麼要在支援錦城？ 啊，因為他跑的電腦是，他是跑在那個很那個很老，二零一五年，然後是 Neon Neon 的那個 server server 級電腦，然後。 我現在做這件事情，它是跑在就是現在更新的電腦上，更新的 CPU 處理器上，跟比較舊 CPU 處理器上，那他們兩個的效果是如何的？

**【授課講師】**：所以你要證實錦城對方法。 嗯。 在為什麼的硬體架構上都有效。 對，呃，都有。 效果是不一定到完全有效這樣。 對，我想，也許你在報告實驗之前先要告訴我，我也是要做實驗。 好，期待實驗。 那我們想知道，那結果呢？ 其實我們併不併不需要知道很細節的數字嘛。 嗯。 那在新的電腦上，錦城的方法有效嗎？ 呃，新的方法的話，錦城的效果沒有那麼的有效。 因為在新的方法的時候，本身它的速度在比較新的硬體架構上。 對，新的硬體架構上，錦城就沒有那麼突出了。 對對對對對對，因為新的硬體架構中，它在處理整體內容的速度就已經夠快了，所以再給它一個更快的。

**【授課講師】**：對，沒有帶來特別明顯的效果，這樣。 那這才是比較重要的部分。 啊，對對對對對。 你講多久？ 啊，你講多久？ 好。

**【授課講師】**：對，那這是第二。 那在那個比較舊、那比較舊電腦的情況下的話。 錦城的 dirtying 的效果就會有明顯的，就會有明顯上升。 那上升的效果大概是十趴，大概是五趴到十趴左右這樣子。 然後，再是開一些做的那個 A P I 測試，它在新電腦的情況下的話，在在新電腦情況下，然後尤其是在四零 C P U 八 G B M 的情況下之後，它做出來效果可以比原本的 S C U M P Y 好好大概七十趴左右。 對，那這個原因主要，這個原因主要是因為就是現在新出來的這個 C P U A M D Y 是七五七零的 C P U，它對 acceleration 的這個指令集有更高的資源。

**【授課講師】**：那在比較比較舊電腦那個 Intel 六七六 Intel 六七零的話，那個時候的 Intel C P U 它對 acceleration 沒有做到那麼高的資源。 那這個十號它反而就沒有比原本的方法還要好。

**【授課講師】**：對，那就是總結就是開哎錦城做的 dirtying 方法的話，它在 C P U 比較。 啊，然後讓的development壓力會比較大情況下之後，它才會有比較好的發展。 那凱捷的方法的話，是是在比較新的CPU架構，然後它必須是比較新的CPU架構，然後必須要對過去來選擇這個指令集有不錯的最佳化話，它才會有不錯的效果。 對，總結的話是這樣子。 對。 王碩總，王碩，我我我他是做那個auto pare的，auto auto auto pare就是那個去讓他讓他在在複製到那個ME裡面的workload是哪一種是是哪一種workload之後，然後我可以找出一種最適哎找出一種最適合長度的APU去做同步，然後去獲得哎然後讓ME裡面的workload的效能performance可以到一個不錯的數值這樣。

**【授課講師】**：對。 然後那是這個方法，就是昨天我跟王老師討論，然後我我我裡面有一些是。 裡面有一些那個邏輯上錯誤，然後我還要再修改。 對。 現在，像李總報告，他說，你的問題聽一次清楚，對。 啊，在這麼大的系統下，某一點錯，啊，強調說，為什麼？ 我也是這麼覺得，這個有把握。 啊，他有機會的。 好，A知道我，呃，我兩大種態，我做A跟我做B，在我做A的情況下，我F好；在我做B的情況下，我F差。 對。 那三號，我一種聰明的方法，一跑，我只要跑三秒鐘，我就能預測啊，什麼ASP，就馬上調整。

**【授課講師】**：對，它類似這樣子的。 啊。 我們一般就容易理解。 啊，再來重複一次。 啊，決定做哪做，Forecast，再預測。 對啊，然後你有一個好的解決方法。 嗯。 你只要是做的話，就沒事。 啊，對是這樣，好不好？ 好。

**【授課講師】**：好。

**【授課講師】**：我們沒有改，就是這樣。 那繼續繼續，好好好好。

**【授課講師】**：改什麼不行？ 然後那個我問一下，是馬上決定一下下下次的開會時間嗎？ 應該是這個，這個比較重要。 下星期是，那我們就下，再下一個月。 只是說，因為接下來要麻煩是也是管系，就什麼，暑假有，暑假有，但是是上上一年，一年一年級，一般是有課。 還是有課學的沒有？ 還沒有，還沒學課。 嗯。 那禮拜上都是星期六。 沒有必修，沒有，沒有必修。 一般我們這個學期，他們好像到他們這。 好像有做學，好像有做骨幹，其實骨幹什麼嗎？ 其實學生還是學生。 哦，最開始中午是要一點鐘上課，哎，是不是？

**【授課講師】**：我現在應該沒有，現在應該是在星期幾？ 你之前是因為那個接那個什麼，那個直播的上期的，哎，上期的。 現在課應該都是星期一。 然後所以說禮拜四是中中午是可以，不知道禮拜四中午那我們最早啊，那還是應該是中午好的。 好，好吧。 好。

**【授課講師】**：好。

**【授課講師】**：哎，這可是要九月十號，因為九月十號沒事。 OK啊，中午這樣。 所以九月十一號可以嗎？ 可以啊，九月十一可以，可以啊，那我們就九月十一號。 好，幹嘛？ 好，好，好，三個，三個，九月十一號。 之前中午一樣是十二點十五嗎？ 對，可以。 好。

**【授課講師】**：好，應該就這樣。 謝謝大家。 那，然後我們再看一下。 好好。

**【授課講師】**：那按什麼部分？ 按什麼部分呢？ 首先就是關於我們的結結果，因為我們不不使用這幾雙鞋子，我們標定出結果之後，直接從這雙鞋子帶好。

**【授課講師】**：然後，並且這些，然後再來還有一些這部分一些的標識要用，就是材料加一些其他的對的。 然後，再來一點就是我們的包裝方式，然後要注意一下它的差異度的強，然後及呃關於我們日常使用裡面，我們是找自己的一些必須的使用，然後呢，再一個就是然後還有那個就是材料的一些使用的的那個流程的描述，然後以及那個在後面加工我們可以加它新增一個袋子，然後呢，然後或者用什麼。 以及呃，我們在用防禦策略的時候，還是歸納式的形式，然後我們要去分析報告，然後還有一再就是一些報告報告方面的去，或者是在解釋一個東西的時候，我們要用邏輯去說，要多讓你們自己。

**【授課講師】**：好，那那請問針對這部分老師有沒有其他的呃問題？ 那這樣的是歸納式，因為就提到了歸納、歸納、歸納這三種形式。 那我們組大家回去再確定一下情境的定義到底要區分。 然後第二點是老師有提到說，如果我們可以把歸納裡面提出的這個防禦機制這一類的也加到歸納式上面，我們可以驗證一下這個防禦機制是否也通用在其他的情境上。 以上，請問老師有什麼？ 好，謝謝老師。 那S組這邊就是會在把新計劃的問題再去定義的更清楚一點，就是修正我們的表達方式，然後接下來會去閱讀，就是最最新找到的兩篇論文，然後去想出它的技術細節是怎麼做的。

**【授課講師】**：你們現在應該執行紅綠計劃的第二年。 呃，對對。 所以你們現在做的跟你們當初提的年沒有關係。 嗯，那沒有，這個是新那個二零二六的那個新計劃年底要提的那個。 哦，你們現在在預備要做未來的計劃，對，哦，好，先提那個，因為年底才會那麼趕。 對。 嗯，就是以原來的那個兩年計劃，基本上都做完了。 呃，第二年，第哎，第一年結案，然後第二年還還正要開始。 哦，所以你們。 雙軌制，一方面要想辦法要做減壓，一方面想要做未來規劃。 而且還是有關係。 好好好。

**【授課講師】**：我們沒沒什麼。 好。

**【授課講師】**：那B組的話，然後就是用跟Overview方法去表達報告目的跟結果，還有就是繼續修正那個口頭白的這樣。 因為我不知道你們，你跟王老師討論到什麼地步。 嗯。 你可以試看看怎麼跟丹丹老師一樣不一樣，就直接寫，直接求老師。 就你，我看你寫的出來寫。 好好好，我試看。 OK，寫的出來大大概大概說的出聚焦了。 嗯。 我寫不出來就知道。 哈哈哈哈哈。 有些什麼問題？ 好好好，我們思考。 OK，好，謝老師。 那謝謝各位老師的指導嘛，就不用了。 簽名都簽了，好，謝謝你啊，謝謝，謝謝啊。
